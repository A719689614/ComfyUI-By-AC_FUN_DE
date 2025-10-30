from PIL import Image,ImageEnhance,Image, ImageFilter, ImageEnhance
from .AC_FUN import AC_FUN
from .image_factory import pil2tensor,tensor2pil

MAX_RESOLUTION = 8096

class Picture_line(AC_FUN):
  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
         "image":("IMAGE",),
         "radius":("FLOAT", {"default": 0.5, "min": 0.0, "max": 360, "step": 0.01}),
         "contrast":("FLOAT", {"default": 0.5, "min": 0.0, "max": 10, "step": 0.01}),
      },
    }
  RETURN_TYPES = ("IMAGE",)
  FUNCTION = "picture_line"

  def picture_line(self,image,contrast,radius):
        
        image = tensor2pil(image)
        # 对图像进行高斯模糊处理
        blurred = image.filter(ImageFilter.GaussianBlur(radius=radius))

        gray_image = blurred.convert('L')

        edges = gray_image.filter(ImageFilter.FIND_EDGES)

        inverted_edges = Image.eval(edges, lambda x: 255 - x)
        enhancer = ImageEnhance.Contrast(inverted_edges)
        final_image = enhancer.enhance(contrast)
        image = pil2tensor(final_image)
        return (image, )


class Picture_Merge(AC_FUN):
  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
         "layer_image":("IMAGE",),
         "background_image":("IMAGE",),
         "x_axis":("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
         "y_axis":("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
      },
    }
  RETURN_TYPES = ("IMAGE",)
  FUNCTION = "picture_Merge"

  def picture_Merge(self,layer_image,background_image,x_axis,y_axis):
      x = x_axis
      y = y_axis
      image1 = tensor2pil(layer_image)  # Assuming layer_image is a tensor
      image2 = tensor2pil(background_image)  # Assuming background_image is a tensor

      # Convert to RGBA mode (assuming images already have alpha channel)
      image1 = image1.convert('RGBA')
      image2 = image2.convert('RGBA')

      # Create a new RGBA image object with the same size as image2
      composite_image = Image.new('RGBA', image2.size)

      # Paste image2 onto the new image object
      composite_image.paste(image2, (x, y))

      # Paste image1 onto image2 (preserving original size and position of image1)
      composite_image.paste(image1, (x, y), mask=image1)

      # Convert composite_image back to tensor if needed
      composite_image_tensor = pil2tensor(composite_image)


      return (composite_image_tensor, )