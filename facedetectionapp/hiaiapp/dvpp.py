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

import ctypes
from ctypes import *
from hiaiapp import *
import image


kVpcWidthAlign = 128
kVpcHeightAlign = 16

def AlignUP(length, alignValue):
    if length % alignValue > 0:
        length = alignValue * (length // alignValue + 1)
    return length

def AlignUpScaleRatio(width, height, isAligned = True):
    if isAligned:
        widthScaleRatio = round(float(AlignUP(width, kVpcWidthAlign))/float(width), 3)
        heightScaleRatio = round(float(AlignUP(height, kVpcHeightAlign))/float(height), 3)
    else:
        widthScaleRatio = 1.0
        heightScaleRatio = 1.0

    return widthScaleRatio, heightScaleRatio
		
def ResizeImage(destImage, srcImageParam, modeResution,  isAligned = True):
    srcImageC = image.CreateImageDataC(srcImageParam.imageId, srcImageParam.imageData)
    modeResolutionC = image.CreateResolutionC(modeResution)
    destImageC = image.ImageDataC()
    ret = hiaiApp.ResizeImage(byref(destImageC), byref(modeResolutionC), byref(srcImageC), isAligned)
    if ret != HIAI_APP_OK:
        print("Resize image failed, return ", ret)
        return HIAI_APP_ERROR

    if isAligned:
        destImage.width = AlignUP(modeResolutionC.width, kVpcWidthAlign)
        destImage.height = AlignUP(modeResolutionC.height, kVpcHeightAlign)
    else:
        destImage.width = modeResolutionC.width
        destImage.height = modeResolutionC.height
    destImage.size = destImageC.size
    destImage.data = destImageC.data

    return HIAI_APP_OK

def ConvertImageYuvToJpeg(destImageParam, srcImageParam):
    srcImageC = image.CreateImageDataC(srcImageParam.imageId, srcImageParam.imageData)
    destImageC = image.ImageDataC()
    ret = hiaiApp.ConvertImageToJpeg(byref(destImageC), byref(srcImageC))
    if ret != HIAI_APP_OK:
        print("Convert image failed!")
        return HIAI_APP_ERROR

    destImageParam.imageId = srcImageParam.imageId
    destImageParam.imageData.width = srcImageParam.imageData.width
    destImageParam.imageData.height = srcImageParam.imageData.height
    destImageParam.imageData.size = destImageC.size
    destImageParam.imageData.data = destImageC.data

    return HIAI_APP_OK







