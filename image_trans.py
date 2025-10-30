from .AC_FUN import AC_FUN
from .image_factory import pil2tensor,tensor2pil
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

if __name__ == '__main__':
    
    pass