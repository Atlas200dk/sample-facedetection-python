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
from enum import Enum
from hiaiapp import *
from image import *

#摄像头图片格式
class CameraImageFormat(Enum):
    CAMERA_IMAGE_YUV420_SP = 1

#查询摄像头状态.
class CameraStatus(Enum):
    CAMERA_STATUS_OPEN = 1         # 摄像头处于打开状态
    CAMERA_STATUS_CLOSED = 2       # 摄像头处于关闭状态
    CAMERA_NOT_EXISTS = 3          # 该摄像头不存在
    CAMERA_STATUS_UNKOWN = 4       # 摄像头状态未知

#摄像头数据获取模式
class CameraCapMode(Enum):
    CAMERA_CAP_ACTIVE  = 1  #主动模式.
    CAMERA_CAP_PASSIVE = 2 #被动模式.

#设置摄像头参数
class CameraProperties(Enum):
    CAMERA_PROP_RESOLUTION              =1          #【Read/Write】分辨率  数据类型 CameraResolution* 长度为1
    CAMERA_PROP_FPS                     =2          #【Read/Write】帧率, 数据类型为uint32_t
    CAMERA_PROP_IMAGE_FORMAT            =3          #【Read/Write】帧图片的格式.  数据类型为CameraImageFormat
    CAMERA_PROP_SUPPORTED_RESOLUTION    =4          #【Read】用于获取摄像头支持的所有的分辨率列表.数据类型为CameraResolution*, 数组长度为HIAI_MAX_CAMERARESOLUTION_COUNT
    CAMERA_PROP_CAP_MODE                =5          #【Read/Write】帧数据获取的方式，主动或者被动.数据类型为CameraCapMode
    CAMERA_PROP_BRIGHTNESS              =6          #【Read/Write】亮度，数据类型为uint32_t
    CAMERA_PROP_CONTRAST                =7          #【Read/Write】对比度，数据类型为uint32_t
    CAMERA_PROP_SATURATION              =8          #【Read/Write】饱和度，数据类型为uint32_t
    CAMERA_PROP_HUE                     =9          #【Read/Write】色调，数据类型为uint32_t
    CAMERA_PROP_GAIN                    =10         #【Read/Write】增益，数据类型为uint32_t
    CAMERA_PROP_EXPOSURE                =11         #【Read/Write】曝光，数据类型为uint32_t

def InitCamera():
    return hiaiApp.HiaiApp_MediaLibInit()

def QueryCameraStatus(cameraId):
    return hiaiApp.HiaiApp_QueryCameraStatus(cameraId)

def OpenCamera(cameraId):
    return hiaiApp.HiaiApp_OpenCamera(cameraId)

def SetCameraProperty(cameraId, prop, val):
    if (prop == CameraProperties.CAMERA_PROP_RESOLUTION):
        arg = ResolutionC(val.width, val.height)
        print("Set camera resulution width ", arg.width, ", height ", arg.height)
        pArg = byref(arg)
    else:
        arg = c_int(val)
        pArg = pointer(arg)

    return hiaiApp.HiaiApp_SetCameraProperty(cameraId, prop.value, pArg)

def ReadFrameFromCamera(cameralId, imageParam):
    imgDataC = ImageDataC()
    imgDataC.size = imageParam.imageData.size
    ret = hiaiApp.HiaiApp_ReadFrameFromCamera(cameralId, byref(imgDataC))
    if ret == 0:
        print("Read frame image failed")
        return ret

    imageParam.imageData.data = imgDataC.data
    imageParam.imageId = imgDataC.id

    return ret

def CloseCamera(cameralId):
    return hiaiApp.HiaiApp_CloseCamera(cameralId)
