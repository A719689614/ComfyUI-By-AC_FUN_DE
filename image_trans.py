from .AC_FUN import AC_FUN
import torch
from .image_factory import pil2tensor, tensor2pil, recolor_image, transfer_rgb
from  PIL import Image,ImageFilter
import cv2
import numpy as np

# def Hex_to_RGB(inhex) -> tuple:
#     rval = inhex[1:3]
#     gval = inhex[3:5]
#     bval = inhex[5:]
#     rgb = (int(rval, 16), int(gval, 16), int(bval, 16))
#     return tuple(rgb)


class picture_Trans(AC_FUN):
    math = ["vertical","horizontal"]
    boolean = ["flip","rotate","scale","None"]
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                {
                "image":("IMAGE",),
                "boolean":(s.boolean,),
                "math":(s.math,),
                "rotate":("INT",{"min":-360, "max":360, "step":1,"default":0}),
                "scale_percent":("INT",{"min":0, "max":100, "step":1,"default":1})
                }
                }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "ac_trans"

    def ac_trans(self, image, math="vertical",boolean="None",rotate=0,scale_percent=0):
        pil = tensor2pil(image)
        image = pil
        if boolean == "flip":
            if math == "vertical":
                vertical_image = image.transpose(Image.FLIP_TOP_BOTTOM)
                return (pil2tensor(vertical_image),)
            if math == "horizontal":
                horizontal_image = image.transpose(Image.FLIP_LEFT_RIGHT)
                return (pil2tensor(horizontal_image),)
        
        if boolean == "None":
            return (image,)
        
        if boolean == "rotate":
            rotated_image = image.rotate(rotate)
            return (pil2tensor(rotated_image),)
        
        if boolean == "scale":
            scale_percent = 50 
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            return (pil2tensor(resized_image),)
        


# 图像色阶调整
class Picture_Color_Grade(AC_FUN):
    @classmethod
    def INPUT_TYPES(self):
        return {"required": {
            "image": ("IMAGE",), 
            "in_max": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
            "in_min": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
            "out_max": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
            "out_min": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                             }}
    

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "picture_color_grade"

    def picture_color_grade(self, image, in_max, in_min, out_max, out_min):
        image = tensor2pil(image)
        img_array = np.array(image)

        for channel in range(img_array.shape[2]):
            in_range = (in_max - in_min)
            out_range = (out_max - out_min)
            img_array[:, :, channel] = ((img_array[:, :, channel] - in_min) * out_range / in_range) + out_min

        adjusted_img = Image.fromarray(np.uint8(img_array))
        image = pil2tensor(adjusted_img)
        return(image,)
        

# 图像填黑白
class Picture_fill_color(AC_FUN):
    @classmethod
    def INPUT_TYPES(self):
        return {"required": 
                {
                "image": ("IMAGE",)
                    }}


    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "picture_fill_color"

    def picture_fill_color(self, image):
        img = tensor2pil(image)
        if img.mode!= 'RGBA':
            img = img.convert('RGBA')
        new_img = Image.new('RGB', img.size, (255, 255, 255))
        pixels = new_img.load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                r, g, b, a = img.getpixel((i, j))
                if a > 0:
                    pixels[i, j] = (0, 0, 0)
                else:
                    pixels[i, j] = (255, 255, 255)
        image = pil2tensor(new_img)
        return(image,)

# 图像填黑白(自定义)
class Picture_fill_color_Custom(AC_FUN):
    @classmethod
    def INPUT_TYPES(self):
        return {"required": 
                {
                "image": ("IMAGE",),
                "background": ("STRING",{"forceInput": True}),
                "foreground": ("STRING",{"forceInput": True}),
                
                    }}


    RETURN_TYPES = ("IMAGE","STRING","STRING")
    RETURN_NAMES = ("IMAGE","BACKGROUND","FOREGROUND")
    FUNCTION = "picture_fill_color_custom"

    def picture_fill_color_custom(self, image, background, foreground):
        background = tuple(int(item) for item in background.split(','))
        foreground = tuple(int(item) for item in foreground.split(','))
        br, bg, bb = background[0], background[1], background[2]
        fr, fg, fb = foreground[0], foreground[1], foreground[2]
        img = tensor2pil(image)
        # 如果图像不是 RGBA 模式，转换为 RGBA 模式
        if img.mode!= 'RGBA':
            img = img.convert('RGBA')
        new_img = Image.new('RGB', img.size, (255, 255, 255))
        pixels = new_img.load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                r, g, b, a = img.getpixel((i, j))
                if a > 0:
                    pixels[i, j] = (fr, fg, fb)
                else:
                    pixels[i, j] = (br, bg, bb)
        image = pil2tensor(new_img)
        preview_1 = br, bg, bb
        preview_2 = fr, fg, fb
        return (image,preview_1,preview_2)


# 颜色自定义
class AC_ColorPicker(AC_FUN):
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "r":("INT",{"default": 255, "min": 0, "max": 255,"step": 1}), 
                "g":("INT",{"default": 255, "min": 0, "max": 255,"step": 1}), 
                "b":("INT",{"default": 255, "min": 0, "max": 255,"step": 1}), 
            },
        }
    RETURN_TYPES = ("INT","INT","INT","STRING")
    RETURN_NAMES = ("r","g","b","rgb")
    FUNCTION = 'picker'
    def picker(self,r, g, b):
        r = r
        g = g 
        b = b
        rgb = f"{r},{g},{b}"
        return (r,g,b,rgb)   

# 图像锐化
class AC_ImageSharp(AC_FUN):
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
            "image": ("IMAGE",),
            "sharpness_factor": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
            "radius": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
            "threshold":("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
        }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = 'image_sharp'

    def image_sharp(self, image, sharpness_factor,radius,threshold):
        img = tensor2pil(image)
        sharpened_img = img.filter(ImageFilter.UnsharpMask(radius=radius, percent=sharpness_factor*100, threshold=threshold))
        image = pil2tensor(sharpened_img)
        return(image,)
    
# 图像像素化
class AC_Image_pixel(AC_FUN):
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
            "image": ("IMAGE",),
            "pixel_size": ("INT", {"default": 0, "min": 0, "max": 9999, "step": 1}),
           
        }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = 'image_pixel'

    def image_pixel(self, image, pixel_size):
        img = tensor2pil(image)
        width, height = img.size
        new_width = width // pixel_size
        new_height = height // pixel_size
        resized_img = img.resize((new_width, new_height), Image.NEAREST)
        pixelated_img = resized_img.resize((width, height), Image.NEAREST)
        image = pil2tensor(pixelated_img)
        return(image,)

# 径向模糊简易
class AC_Image_blur_Simple(AC_FUN):
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
            "image": ("IMAGE",),
            "strength": ("INT", {"default": 0, "min": 0, "max": 9999, "step": 1}),
           
        }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = 'image_blur_simple'

    def image_blur_simple(self, image, strength):
        img = tensor2pil(image)
        if img.mode!= 'RGBA':
            img = img.convert('RGBA')
        width, height = img.size
        blurred_img = Image.new('RGBA', (width, height))
        for x in range(width):
            for y in range(height):
                total_r, total_g, total_b, total_a = 0, 0, 0, 0
                count = 0
                for i in range(-strength, strength + 1):
                    for j in range(-strength, strength + 1):
                        new_x = x + i
                        new_y = y + j
                        if 0 <= new_x < width and 0 <= new_y < height:
                            r, g, b, a = img.getpixel((new_x, new_y))
                            total_r += r
                            total_g += g
                            total_b += b
                            total_a += a
                            count += 1
                if count > 0:
                    blurred_img.putpixel((x, y), (total_r // count, total_g // count, total_b // count, total_a // count))
 
        image = pil2tensor(blurred_img)
        return(image,)

class AC_ColorTransferRange(AC_FUN):
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "rgb": ("STRING", {"default": "100,120,200"}),
                "spread": ("INT", {"default": 20, "min": 1, "max": 60, "step": 1}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = 'get_color_range'

    def get_color_range(self, rgb, spread):
        try:
            color_range = transfer_rgb(rgb, spread)
            return (f"{color_range[0]},{color_range[1]}",)
        except Exception as e:
            print(f"[AC_ColorTransferRange] error: {e}")
            return ("198,248",)

def _parse_tuple(text, expected_len):
    text = text.strip().strip("()[]{}")
    parts = [p.strip() for p in text.split(",")]
    if len(parts) != expected_len:
        raise ValueError(f"Expected {expected_len} values, got {len(parts)}: {text}")
    return tuple(int(p) for p in parts)

class Ac_ImageColorTransfer(AC_FUN):
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "image": ("IMAGE",),
                "color_range": ("STRING", {"default": "198,248"}),
                "target_rgb": ("STRING", {"default": "98,100,80"}),
                "shadow_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.05}),
                "dominance_threshold": ("FLOAT", {"default": 0.035, "min": 0.0, "max": 0.5, "step": 0.005}),
                "saturation_threshold": ("FLOAT", {"default": 0.075, "min": 0.0, "max": 0.5, "step": 0.005}),
                "max_filter_size": ("INT", {"default": 3, "min": 1, "max": 11, "step": 2}),
                "blur_radius": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 5.0, "step": 0.1}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = 'imagecolortransfer'

    def imagecolortransfer(self, image, color_range, target_rgb,
                           shadow_strength, dominance_threshold,
                           saturation_threshold, max_filter_size, blur_radius):
        color_range = _parse_tuple(color_range, 2)
        target_rgb = _parse_tuple(target_rgb, 3)

        batches = []
        for i in range(image.shape[0]):
            pil_img = tensor2pil(image[i:i+1])
            arr = np.asarray(pil_img.convert("RGB"))
            result_arr = recolor_image(
                arr,
                color_range=color_range,
                target_rgb=target_rgb,
                shadow_strength=shadow_strength,
                dominance_threshold=dominance_threshold,
                saturation_threshold=saturation_threshold,
                max_filter_size=max_filter_size,
                blur_radius=blur_radius,
            )
            batches.append(pil2tensor(Image.fromarray(result_arr, "RGB")))

        return (torch.cat(batches, dim=0),)

# RGB 转换
class AC_RGBTransfer(AC_FUN):
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "r": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "g": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "b": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = 'rgb_transfer'

    def rgb_transfer(self, r, g, b):
        result = f"{r},{g},{b}"
        return (result,)

# 16进制转换RGB
class AC_HEXTransfer(AC_FUN):
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "hex": ("STRING", {"default": "#FF0000"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = 'hex_transfer'
    
    def hex_transfer(self, hex):
        try:
            h = hex.strip().lstrip("#").strip().lower()
            if len(h) == 3:
                h = "".join(c * 2 for c in h)
            if len(h) != 6:
                raise ValueError(f"Invalid hex length: {hex}")
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            return (f"{r},{g},{b}",)
        except Exception:
            return ("0,0,0",)

if __name__ == '__main__':
    
    pass