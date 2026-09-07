from __future__ import annotations
import torch
from PIL import Image,ImageDraw, ImageFilter
import numpy as np
import argparse
from pathlib import Path

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def rgb_to_hsv(rgb: np.ndarray):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx = np.max(rgb, axis=-1)
    mn = np.min(rgb, axis=-1)
    diff = mx - mn

    h = np.zeros_like(mx)
    mask = diff > 1e-6
    rmask = mask & (mx == r)
    gmask = mask & (mx == g)
    bmask = mask & (mx == b)

    h[rmask] = ((g[rmask] - b[rmask]) / diff[rmask]) % 6
    h[gmask] = ((b[gmask] - r[gmask]) / diff[gmask]) + 2
    h[bmask] = ((r[bmask] - g[bmask]) / diff[bmask]) + 4
    h /= 6.0

    s = np.zeros_like(mx)
    nonzero = mx > 1e-6
    s[nonzero] = diff[nonzero] / mx[nonzero]
    return h, s, mx


def rgb_to_hue_range(rgb, spread=20):
    arr = np.array([[rgb]], dtype=np.float32) / 255.0
    h, s, v = rgb_to_hsv(arr)
    hue_deg = float(h[0, 0] * 360.0)
    h_min = max(0, int(hue_deg - spread))
    h_max = min(360, int(hue_deg + spread))
    return (h_min, h_max)


def make_blue_clothing_mask(arr: np.ndarray, 
                            color_range=(198, 248),
                            dominance_threshold=0.035,
                            saturation_threshold=0.075,
                            # value_threshold: float = 0.15,
                            max_filter_size=3,
                            blur_radius=0.7
                            ) -> np.ndarray:
    """Build a soft mask for the original blue garment area."""
    try:
        h, s, v = rgb_to_hsv(arr)
        r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
        hue_deg = h * 360.0
        # mask = blue_hue & blue_dominance & enough_color & enough_value & not_white
        color_hue = (hue_deg >= color_range[0]) & (hue_deg <= color_range[1])
        color_dominance = (b > r + dominance_threshold) & (b > g - dominance_threshold)
        not_white = ~((r > 0.86) & (g > 0.86) & (b > 0.86) & (s < 0.20))
        enough_color = s > saturation_threshold
        enough_value = v > 0.15

        mask = color_hue & color_dominance & enough_color & enough_value & not_white

        # Expand slightly, then blur for natural edges around hair, hands and seams.
        mask_img = Image.fromarray((mask.astype(np.uint8) * 255), "L")
        mask_img = mask_img.filter(ImageFilter.MaxFilter(max_filter_size))
        mask_img = mask_img.filter(ImageFilter.GaussianBlur(blur_radius))
        return np.asarray(mask_img).astype(np.float32) / 255.0
    except Exception as e:
        print(e)


def recolor_image(
    arr: np.ndarray,
    color_range=(198, 248),
    target_rgb=(98, 100, 80),
    shadow_strength=1.0,
    dominance_threshold=0.035,
    saturation_threshold=0.075,
    max_filter_size=3,
    blur_radius=0.7,
) -> np.ndarray:
    if arr.dtype != np.float32 or arr.max() > 1.0:
        arr = arr.astype(np.float32) / 255.0
    target = np.array(target_rgb, dtype=np.float32) / 255.0

    alpha = make_blue_clothing_mask(arr, color_range, dominance_threshold, saturation_threshold,
                                    max_filter_size, blur_radius)
    solid = alpha > 0.2

    lum = arr[..., 0] * 0.299 + arr[..., 1] * 0.587 + arr[..., 2] * 0.114
    median_lum = float(np.median(lum[solid])) if np.any(solid) else 0.72
    shade = lum / max(median_lum, 0.35)
    shade = 1.0 + (shade - 1.0) * shadow_strength

    target_brightness = float(np.max(target))
    min_shade = 0.58 if target_brightness > 0.85 else 0.50
    max_shade = 1.12 if target_brightness > 0.85 else 1.22
    shade = np.clip(shade, min_shade, max_shade)

    recolored = np.clip(target * shade[..., None], 0.0, 1.0)
    result = arr * (1.0 - alpha[..., None]) + recolored * alpha[..., None]
    result = np.clip(result * 255.0 + 0.5, 0, 255).astype(np.uint8)
    return result


def recolor_garment(
    src_path: Path,
    out_path: Path,
    color_range=(198, 248),
    target_rgb=(98, 100, 80),
    shadow_strength=1.0,
    dominance_threshold=0.035,
    saturation_threshold=0.075,
    max_filter_size=3,
    blur_radius=0.7,
) -> None:
    image = Image.open(src_path).convert("RGB")
    arr = np.asarray(image).astype(np.float32) / 255.0

    result = recolor_image(arr, color_range, target_rgb, shadow_strength,
                           dominance_threshold, saturation_threshold, max_filter_size, blur_radius)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(result, "RGB").save(out_path, quality=96, subsampling=0)


def make_preview(paths: list[Path], out_path: Path) -> None:
    thumbs = []
    for idx, p in enumerate(paths, start=1):
        im = Image.open(p).resize((360, 360))
        canvas = Image.new("RGB", (360, 392), "white")
        canvas.paste(im, (0, 0))
        ImageDraw.Draw(canvas).text((10, 368), f"image {idx}", fill=(0, 0, 0))
        thumbs.append(canvas)

    cols = 3
    rows = int(np.ceil(len(thumbs) / cols))
    preview = Image.new("RGB", (cols * 360, rows * 392), "white")
    for idx, thumb in enumerate(thumbs):
        preview.paste(thumb, ((idx % cols) * 360, (idx // cols) * 392))
    preview.save(out_path, quality=92)


def parse_rgb(value: str) -> tuple[int, int, int]:
    parts = [int(x.strip()) for x in value.split(",")]
    if len(parts) != 3 or any(x < 0 or x > 255 for x in parts):
        raise argparse.ArgumentTypeError("RGB must look like 186,204,190")
    return parts[0], parts[1], parts[2]
    

def transfer_rgb(rgb, spread: int = 20) -> tuple[int, int]:
    if isinstance(rgb, str):
        rgb = tuple(int(x.strip()) for x in rgb.split(","))
    return rgb_to_hue_range(rgb, spread)