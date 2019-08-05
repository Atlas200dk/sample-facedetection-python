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

class DvppBasicVpcPara:
    def __init__(self):
        input_image_type = VpcInputFormat.INPUT_YUV420_SEMI_PLANNER_UV
        src_resolution = image.ResolutionRatio(0, 0)
        crop_left = 0
        crop_up = 0
        crop_right = 0
        crop_down = 0
        output_image_type = VpcOutputFormat.OUTPUT_YUV420SP_UV
        dest_resolution = image.ResolutionRatio(0, 0)
        is_input_align = False
        is_output_align = True

class DvppVpcOutput:
    def __init__(self, buf = None, sz = 0):
        buffer = c_char_p(buf)
        size = sz

class DvppVpcOutput_C(Structure):
    _fields_ = [('buffer', c_char_p),
                ('size', c_uint)]


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
        ('data',        c_char_p)
    ]

class ResolutionC:
    _fields_ = [
        ('width', c_uint),
        ('height', c_uint)
    ]

class Dvpp:
    def __init__(self):
        self.dvpp = ctypes.cdll.LoadLibrary("face_detection_dvpp.so")

    def ImageParamDataCopy(self, destImage, srcImage):
        destImage.format = srcImage.format
        destImage.width = srcImage.width
        destImage.height = srcImage.height
        destImage.channel = srcImage.channel
        destImage.depth = srcImage.depth
        destImage.height_step = srcImage.height_step
        destImage.width_step = srcImage.width_step
        destImage.size = srcImage.size
        destImage.data = srcImage.data

    def ResizeImage(self, destImage, srcImage, destResution):
        srcImageC = ImageData_C()
        self.ImageParamDataCopy(srcImageC, srcImage)

        resolution = ResolutionC()
        resolution.width = destResution.width
        resolution.height = destResution.height

        destImageC = ImageData_C()
        self.dvpp.ResizeImage(destImageC, srcImageC, resolution)
        self.ImageParamDataCopy(destImage, destImageC)

    def ConvImageYuvToJpeg(self, destImage, srcImage):
        srcImageC = ImageData_C()

        self.ImageParamDataCopy(srcImageC, srcImage)
        destImageC = ImageData_C()
        self.dvpp.ResizeImage(destImageC, srcImageC)
        self.ImageParamDataCopy(destImage, destImageC)

