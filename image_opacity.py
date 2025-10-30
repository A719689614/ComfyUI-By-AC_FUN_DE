from .AC_FUN import AC_FUN
from .image_factory import pil2tensor,tensor2pil
# from PIL import Image

MAX_RESOLUTION = 255

class Picture_Opacity(AC_FUN):
  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
         "image":("IMAGE",),
         "opacity":("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
      },
    }
  RETURN_TYPES = ("IMAGE",)
  FUNCTION = "picture_opacity"

  def picture_opacity(self,image,opacity):
        
        img= tensor2pil(image)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        data = img.getdata()
        new_data = []
        for item in data:
            new_data.append((item[0], item[1], item[2], opacity))
        img.putdata(new_data)
        image = pil2tensor(img)
        return (image, )
