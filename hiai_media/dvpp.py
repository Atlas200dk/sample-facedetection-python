#! /usr/bin/env python
#coding=utf-8
from enum import Enum
from enum import Enum
import ctypes
from ctypes import *
import copy
import image

#jpege supports the following format input
class JPEGFORMAT(Enum):
    JPGENC_FORMAT_UYVY = 0x0,
    JPGENC_FORMAT_VYUY = 0x1,
    JPGENC_FORMAT_YVYU = 0x2,
    JPGENC_FORMAT_YUYV = 0x3,
    JPGENC_FORMAT_NV12 = 0x10,
    JPGENC_FORMAT_NV21 = 0x11


class VpcInputFormat(Enum):
    INPUT_YUV400 = 0
    INPUT_YUV420_SEMI_PLANNER_UV = 1
    INPUT_YUV420_SEMI_PLANNER_VU = 2
    INPUT_YUV422_SEMI_PLANNER_UV = 3
    INPUT_YUV422_SEMI_PLANNER_VU = 4
    INPUT_YUV444_SEMI_PLANNER_UV = 5
    INPUT_YUV444_SEMI_PLANNER_VU = 6
    INPUT_YUV422_PACKED_YUYV = 7
    INPUT_YUV422_PACKED_UYVY = 8
    INPUT_YUV422_PACKED_YVYU = 9
    INPUT_YUV422_PACKED_VYUY = 10
    INPUT_YUV444_PACKED_YUV = 11
    INPUT_RGB = 12
    INPUT_BGR = 13
    INPUT_ARGB = 14
    INPUT_ABGR = 15
    INPUT_RGBA = 16
    INPUT_BGRA = 17
    INPUT_YUV420_SEMI_PLANNER_UV_10BIT = 18
    INPUT_YUV420_SEMI_PLANNER_VU_10BIT = 19

class VpcOutputFormat(Enum):
    OUTPUT_YUV420SP_UV = 0
    OUTPUT_YUV420SP_VU = 1



class ImageData_C(Structure):
    _fields_ = [
        ('format',      c_uint),
        ('width',       c_uint),
        ('height',      c_uint),
        ('channel',     c_uint),
        ('depth',       c_uint),
        ('height_step', c_int),
        ('width_step',  c_int),
        ('size',        c_int),
        ('data',        POINTER(c_byte))
    ]

class ResolutionC(Structure):
    _fields_ = [
        ('width', c_uint),
        ('height', c_uint)
    ]

class Dvpp:
    def __init__(self):
        self.dvpp = ctypes.cdll.LoadLibrary("/usr/lib64/libascend_ezdvpp.so")


    def ImageParamDataCopy(self, destImage, srcImage, isObject2Structure = False):
        #destImage.format = srcImage.format
        destImage.width = srcImage.width
        destImage.height = srcImage.height
        destImage.channel = srcImage.channel
        destImage.depth = srcImage.depth
        destImage.height_step = srcImage.height_step
        destImage.width_step = srcImage.width_step
        destImage.size = srcImage.size
        if isObject2Structure:
            destImage.data = cast(srcImage.data, POINTER(c_byte))
        else:
            destImage.data = srcImage.data

    def ResizeImage(self, destImage, srcImage, destResution):
        srcImageC = ImageData_C()
        self.ImageParamDataCopy(srcImageC, srcImage, True)
        srcImageC.format = srcImage.format.value

        resolution = ResolutionC()
        resolution.width = destResution.width
        resolution.height = destResution.height

        resizedImageBufSize = srcImage.size / 6
        destImage.data = create_string_buffer(sizeof(c_byte) * resizedImageBufSize)
        print("call dvpp.ResizeImage start, image buffer size ", resizedImageBufSize)
        resizedImageSize = self.dvpp.ResizeImage(byref(destImage.data), resizedImageBufSize, pointer(resolution), pointer(srcImageC))
        if resizedImageSize <= 0:
            print("Resize image failed, return ", resizedImageSize)
            return 1
        print("call dvpp.ResizeImage end, resized image size ", resizedImageSize)
        destImage.size = resizedImageSize
        destImage.format = srcImage.format
        print("resize end")
        return 0

    def ConvertImageYuvToJpeg(self, destImage, srcImage):
        print("start convert image, start data ",
              ord(srcImage.data[0]), ord(srcImage.data[1]), ord(srcImage.data[2]), ord(srcImage.data[3]),
              ord(srcImage.data[4]), ord(srcImage.data[5]), ord(srcImage.data[6]), ord(srcImage.data[7]))

        srcImageC = ImageData_C()

        self.ImageParamDataCopy(srcImageC, srcImage, True)
        srcImageC.format = srcImage.format.value

        jpegImageBufSize = srcImage.size  * 2 / 3
        destImage.data = create_string_buffer(sizeof(c_byte) * jpegImageBufSize)
        print("call dvpp.ConvertImageToJpeg start, image buffer size ", jpegImageBufSize)
        jpegSize = self.dvpp.ConvertImageToJpeg(byref(destImage.data), jpegImageBufSize, pointer(srcImageC))
        if jpegSize <= 0:
            print("Convert image failed, return ", jpegSize)
            return 1
        print("call dvpp.ConvertImageToJpeg end, jpeg image size ", jpegSize)
        destImage.width = srcImage.width
        destImage.height = srcImage.height
        destImage.size = jpegSize

        return 0







