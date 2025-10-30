from .AC_FUN import AC_FUN
from .image_factory import pil2tensor,tensor2pil
from  PIL import Image,ImageFilter


# 图像像素化
class AC_layer_shadow(AC_FUN):
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "image": ("IMAGE",),
                "blur_radius": ("INT", {"default": 10, "min": 0, "max": 9999, "step": 1}),
                "x_axis": ("INT", {"default": 10, "min": 0, "max": 9999, "step": 1}),
                "y_axis": ("INT", {"default": 10, "min": 0, "max": 9999, "step": 1}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = 'layer_shadow'

    def layer_shadow(self, image, x_axis, y_axis, blur_radius, shadow_color=(0, 0, 0, 128)):
        image = tensor2pil(image)
        width, height = image.size
        offset=(x_axis, y_axis)
        shadow_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        shadow_layer = shadow_img.copy()
        pasted_layer = shadow_layer.paste(shadow_color, [0, 0, width, height])
        if pasted_layer is None:
            print(f"Error: Paste operation returned None. Shadow color: {shadow_color}, Image size: {width}x{height}")
            print(f"Shadow image: {shadow_img}")
            raise ValueError("Paste operation returned None")
        else:
            shadow_layer = pasted_layer
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(blur_radius))
        shadow_img.paste(shadow_layer, offset, shadow_layer)
        result_img = Image.alpha_composite(image.convert('RGBA'), shadow_img)
        image = pil2tensor(result_img)
        return(image,)