from .AC_FUN import AC_FUN
from .image_factory import pil2tensor,tensor2pil
from  PIL import ImageFilter,Image,ImageDraw

MAX = 8920

class picture_inline(AC_FUN):
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                {
                "image":("IMAGE",),
                "stroke_width":("INT",{"min":0, "max":MAX, "step":1,"default":1})
                }
                }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "picture_inline"

    def picture_inline(self, image,stroke_width ):
        image = tensor2pil(image)
        stroke_image = image.copy()
        blurred_image = stroke_image.filter(ImageFilter.GaussianBlur(radius=stroke_width))
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        width, height = image.size

        for x in range(width):
            for y in range(0, stroke_width):
                draw.point((x, y), fill=255)
                draw.point((x, height - 1 - y), fill=255)
        for y in range(height):
            for x in range(0, stroke_width):
                draw.point((x, y), fill=255)
                draw.point((width - 1 - x, y), fill=255)

        image.paste(blurred_image, mask=mask)
        image_result = pil2tensor(image)
        return (image_result,)
        
