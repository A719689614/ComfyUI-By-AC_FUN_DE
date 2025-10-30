from .AC_FUN import AC_FUN
from .image_factory import pil2tensor,tensor2pil
from PIL import Image

MAX_RESOLUTION = 8196

class Picture_Paste(AC_FUN):
  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
         "image_1":("IMAGE",),
         "image_2":("IMAGE",),
         "paste_x":("INT", {"default": 0, "min": 1, "max": MAX_RESOLUTION, "step": 1}),
         "paste_y":("INT", {"default": 0, "min": 1, "max": MAX_RESOLUTION, "step": 1}),
         "image_1_x_axis":("INT", {"default": 0, "min": -MAX_RESOLUTION, "max": MAX_RESOLUTION, "step": 1}),
         "image_1_y_axis":("INT", {"default": 0, "min": -MAX_RESOLUTION, "max": MAX_RESOLUTION, "step": 1}),
         "image_2_x_axis":("INT", {"default": 1024, "min":-MAX_RESOLUTION, "max": MAX_RESOLUTION, "step": 1}),
         "image_2_y_axis":("INT", {"default": 768, "min": -MAX_RESOLUTION, "max": MAX_RESOLUTION, "step": 1}),
      },
    }
  RETURN_TYPES = ("IMAGE",)
  FUNCTION = "picture_paste"

  def picture_paste(self,image_1,image_2,paste_x,paste_y,image_1_x_axis,image_1_y_axis,
                    image_2_x_axis,image_2_y_axis):
        
        image_1 = tensor2pil(image_1)
        image_2 = tensor2pil(image_2)

        new_image = Image.new('RGB', (paste_x, paste_y))
        new_image.paste(image_1, (image_1_x_axis, image_1_y_axis))
        new_image.paste(image_2, (image_2_x_axis, image_2_y_axis))
        image = pil2tensor(new_image)
        return (image, )
