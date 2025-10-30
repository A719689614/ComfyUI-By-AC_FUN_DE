from.AC_FUN import AC_FUN
from.image_factory import pil2tensor, tensor2pil
from PIL import ImageDraw

MAX = 8920

class picture_custom_inline(AC_FUN):
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                {
                    "image":("IMAGE",),
                    "stroke_width":("INT",{"min":0, "max":MAX, "step":1,"default":1}),
                    "stroke_color": ("STRING", {"default": "0, 0, 0"}),
                    "stroke_opacity": ("INT", {"min": 0, "max": 255, "default": 255})
                }
                }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "picture_custom_inline"

    def picture_custom_inline(self, image, stroke_width, stroke_color, stroke_opacity):
        image = tensor2pil(image)
        draw = ImageDraw.Draw(image)
        width, height = image.size

        # 解析自定义颜色字符串
        stroke_color_str = str(stroke_color)
        stroke_color = tuple(map(int, stroke_color_str.strip('()').split(',')))

        new_stroke_color = (stroke_color[0], stroke_color[1], stroke_color[2], stroke_opacity)  # 创建包含透明度的新颜色

        for x in range(width):
            for y in range(0, stroke_width):
                draw.point((x, y), fill=new_stroke_color)
                draw.point((x, height - 1 - y), fill=new_stroke_color)

        for y in range(height):
            for x in range(0, stroke_width):
                draw.point((x, y), fill=new_stroke_color)
                draw.point((width - 1 - x, y), fill=new_stroke_color)

        image = pil2tensor(image)
        return (image,)