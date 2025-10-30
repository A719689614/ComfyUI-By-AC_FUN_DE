from .AC_FUN import AC_FUN
from .image_factory import pil2tensor,tensor2pil
from nodes import SaveImage 
import folder_paths
import random
import torch
import hashlib
import numpy as np
from PIL import ImageFile, UnidentifiedImageError
from PIL import Image, ImageOps, ImageSequence

# def pillow(fn, arg):
#     prev_value = None
#     try:
#         x = fn(arg)
#     except (OSError, UnidentifiedImageError, ValueError):
#         prev_value = ImageFile.LOAD_TRUNCATED_IMAGES
#         ImageFile.LOAD_TRUNCATED_IMAGES = True
#         x = fn(arg)
#     finally:
#         if prev_value is not None:
#             ImageFile.LOAD_TRUNCATED_IMAGES = prev_value
#     return x

# 图像转遮罩
class AC_Image2mask(AC_FUN):
    black_threshold =0
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "image": ("IMAGE",),
                "channel": (["red", "green", "blue", "alpha"],)
            }
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = 'image2mask'

    def image2mask(self, image,channel):
        image = tensor2pil(image)
        img = image.convert("RGB")
        pixels = img.load()
        width, height = img.size

        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                if r <= self.black_threshold and g <= self.black_threshold and b <= self.black_threshold:
                    continue
                else:
                    pixels[x, y] = (255, 255, 255)
        img = pil2tensor(img)
        channels = ["red", "green", "blue", "alpha"]
        mask = img[:, :, :, channels.index(channel)]
        return (mask,)

    
# 图像转白板
class AC_Image2board(AC_FUN):
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "image": ("IMAGE",),
                "black_threshold": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = 'image2board'

    def image2board(self, image, black_threshold=0):
        image = tensor2pil(image)
        img = image.convert("RGB")
        pixels = img.load()
        width, height = img.size

        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                if r <= black_threshold and g <= black_threshold and b <= black_threshold:
                    continue
                else:
                    pixels[x, y] = (255, 255, 255)
        image = pil2tensor(img)
        return(image,)
    

class AC_MaskPreview(SaveImage,AC_FUN):
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz1234567890") for x in range(5))
        self.compress_level = 4
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {"mask": ("MASK",), },
        }

    FUNCTION = "mask_preview"
    CATEGORY = AC_FUN.CATEGORY

    def mask_preview(self, mask):
        if mask.dim() == 2:
            mask = torch.unsqueeze(mask, 0)
        preview = mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])).movedim(1, -1).expand(-1, -1, -1, 3)
        return self.save_images(preview, "MaskPreview")