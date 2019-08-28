#! /usr/bin/env python
#coding=utf-8
#   =======================================================================
#
# Copyright (C) 2018, Hisilicon Technologies Co., Ltd. All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   1 Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#   2 Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#   3 Neither the names of the copyright holders nor the names of the
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#   =======================================================================
#
from enum import Enum
import ctypes
from ctypes import *
import numpy as np
from datetime import *


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
    def __init__(self, width = 0, height = 0, size = 0):
        self.format = IMAGEFORMAT.YUV420SP #图像格式
        self.width = width #图像宽
        self.height = height #图像高
        self.channel = 0 #图像通道数
        self.depth = 0 #位深
        self.heightStep = 0 #对齐高度
        self.widthStep = 0 #对齐宽度
        self.size = size #数据大小（Byte
        self.data = None #数据指针

class ImageDataC(Structure):
    _fields_ = [
        ('id',          c_uint),
        ('width',       c_uint),
        ('height',      c_uint),
        ('size',        c_int),
        ('data',        POINTER(c_ubyte))
    ]

def CreateImageDataC(imageId, imageData):
    imageC = ImageDataC()
    imageC.id = imageId
    imageC.width = imageData.width
    imageC.height = imageData.height
    imageC.size = imageData.size
    imageC.data = imageData.data

    return imageC

class Resolution:
    def __init__(self, w = 0, h = 0):
        self.width = w
        self.height = h

class ResolutionC(Structure):
    _fields_ = [('width', c_int),
                ('height', c_int)]

def CreateResolutionC(resolution):
    resolutionC = ResolutionC()
    resolutionC.width = resolution.width
    resolutionC.height = resolution.height
    return resolutionC


def YuvImageSize(resolution):
    return resolution.width * resolution.height * 3 / 2

def Yuv2Array(yuvImg):
    nArray = np.zeros(shape=(yuvImg.size/8,), dtype='uint64', order='C')
    newdata = cast(yuvImg.data, POINTER(c_ulonglong))
    for i in range(0, yuvImg.size/8):
        nArray[i]=newdata[i]

    nArray.dtype=np.uint8
    nArray = nArray.reshape((yuvImg.height * 3 // 2, yuvImg.width)).astype('uint8')  # YUV 的存储格式为：NV12（YYYY UV）

    return nArray

