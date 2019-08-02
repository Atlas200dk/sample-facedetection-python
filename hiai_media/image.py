#! /usr/bin/env python
#coding=utf-8

from enum import Enum
import ctypes
from ctypes import *

class IMAGEFORMAT(Enum):
    RGB565 = 0 #Red 15:11, Green 10:5, Blue 4:0
    BGR565 = 1 #Blue 15:11, Green 10:5, Red 4:0
    RGB888 = 2 #Red 24:16, Green 15:8, Blue 7:0
    BGR888 = 3 #Blue 24:16, Green 15:8, Red 7:0
    BGRA8888 = 4 #Blue 31:24, Green 23:16, Red 15: 8, Alpha 7:0
    ARGB8888 = 5 #Alpha 31:24, Red 23:16, Green 15:8, Blue 7:0
    RGBX8888 = 6
    XRGB8888 = 7
    YUV420Planar = 8 #I420
    YVU420Planar = 9 #YV12
    YUV420SP = 10 #NV12
    YVU420SP = 11 #NV21
    YUV420Packed = 12  #YUV420 Interleaved
    YVU420Packed = 13 #YVU420 Interleaved
    YUV422Planar = 14 #Three arrays Y, U, V.
    YVU422Planar = 15
    YUYVPacked = 16 #422 packed per payload in planar slices
    YVYUPacked = 17 #422 packed
    UYVYPacket = 18 #422 packed
    VYUYPacket = 19 #422 packed
    YUV422SP = 20 #422 packed
    YVU422SP = 21
    YUV444Interleaved = 22 #Each pixel contains equal parts YUV
    Y8 = 23
    Y16 = 24
    H264 = 25
    H265 = 26
    JPEGRAW = 27
    RAW = 28


class ImageData:
    def __init__(self):
        self.format = IMAGEFORMAT.YUV420SP #图像格式
        self.width = 0 #图像宽
        self.height = 0 #图像高
        self.channel = 0 #图像通道数
        self.depth = 0 #位深
        self.height_step = 0 #对齐高度
        self.width_step = 0 #对齐宽度
        self.size = 0 #数据大小（Byte
        self.data = c_char_p(0) #数据指针

class ResolutionRatio:
    def __init__(self, w = 0, h = 0):
        width = w
        height = h



