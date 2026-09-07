from .image_line import Picture_line,Picture_Merge
from .image_paste import Picture_Paste
from .image_opacity import Picture_Opacity
from .image_trans import picture_Trans,Picture_Color_Grade,Picture_fill_color,Picture_fill_color_Custom,AC_ColorPicker,AC_ImageSharp
from .image_inline import picture_inline
from .image_custom_inline import picture_custom_inline
from .image_trans import (AC_Image_pixel,AC_Image_blur_Simple, AC_ColorTransferRange,
                           Ac_ImageColorTransfer, AC_RGBTransfer, AC_HEXTransfer)
from .layer_shadow import AC_layer_shadow
from .image2mask import AC_Image2board,AC_MaskPreview, AC_Image2mask, AC_ImageCropByMask

NODE_CLASS_MAPPINGS = {
    "AC_颜色选择器":AC_ColorPicker,
    "AC_图像转线稿":Picture_line,
    "AC_图像合并":Picture_Merge,
    "AC_图像拼接":Picture_Paste,
    "AC_图像透明度":Picture_Opacity,
    "AC_图像变换":picture_Trans,
    "AC_图像内联描边":picture_inline,
    "AC_图像内联描边(自定义)":picture_custom_inline,
    "AC_图像色阶":Picture_Color_Grade,
    "AC_图像填色":Picture_fill_color,
    "AC_图像填色(自定义)":Picture_fill_color_Custom,
    "AC_图像锐化":AC_ImageSharp,
    "AC_图像像素化":AC_Image_pixel,
    "AC_径向模糊(简易)":AC_Image_blur_Simple,
    "AC_图层阴影(调试)":AC_layer_shadow,
    "AC_图像转黑白板":AC_Image2board,
    "AC_颜色范围":AC_ColorTransferRange,
    "AC_RGB转换":AC_RGBTransfer,
    "AC_HEX转换":AC_HEXTransfer,
    "AC_图像颜色迁移":Ac_ImageColorTransfer,
    "AC_Mask(预览)":AC_MaskPreview,
    "AC_Img2Mask":AC_Image2mask,
    "AC_遮罩裁切":AC_ImageCropByMask,
}

 
