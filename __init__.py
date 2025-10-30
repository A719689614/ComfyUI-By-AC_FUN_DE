from .image_line import Picture_line,Picture_Merge
from .image_paste import Picture_Paste
from .image_opacity import Picture_Opacity
from .image_trans import picture_Trans,Picture_Color_Grade,Picture_fill_color,Picture_fill_color_Custom,AC_ColorPicker,AC_ImageSharp
from .image_inline import picture_inline
from .image_custom_inline import picture_custom_inline
from .image_trans import AC_Image_pixel,AC_Image_blur_Simple
from .layer_shadow import AC_layer_shadow
from .image2mask import AC_Image2board,AC_MaskPreview, AC_Image2mask

NODE_CLASS_MAPPINGS = {
    "AC颜色选择器":AC_ColorPicker,
    "AC图像转线稿":Picture_line,
    "AC图像合并":Picture_Merge,
    "AC图像拼接":Picture_Paste,
    "AC图像透明度":Picture_Opacity,
    "AC图像变换":picture_Trans,
    "AC图像内联描边":picture_inline,
    "AC图像内联描边(自定义)":picture_custom_inline,
    "AC图像色阶":Picture_Color_Grade,
    "AC图像填色":Picture_fill_color,
    "AC图像填色(自定义)":Picture_fill_color_Custom,
    "AC图像锐化":AC_ImageSharp,
    "AC图像像素化":AC_Image_pixel,
    "AC径向模糊(简易)":AC_Image_blur_Simple,
    "AC图层阴影(调试)":AC_layer_shadow,
    "AC图像转黑白板":AC_Image2board,
    "AC_Mask(预览)":AC_MaskPreview,
    "AC_Img2Mask":AC_Image2mask,
}

 
