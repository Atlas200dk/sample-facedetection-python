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
from image import *
from datetime import *

class OpenChannelParam:
    def __init__(self):
      self.host_ip = None
      self.port = 0
      self.channel_name = None
      self.content_type = 127

class OpenChannelParamC(Structure):
    _fields_ = [('port', c_ushort),
                ('content_type', c_ushort),
                ('host_ip', c_char_p),
                ('channel_name', c_char_p)]

class Point:
    def __init__(self):
        self.x = None
        self.y = None

class PointC(Structure):
    _fields_ = [('x', c_uint32),
                ('y', c_uint32)]

class DetectionResult:
    def __init__(self):
        self.lt = Point()
        # The coordinate of left top point
        self.rb = Point()
        # The coordinate of the right bottom point
        self.result_text = None  # Face:xx%

class DetectionResultC(Structure):
    _fields_ = [('lt', PointC),
                ('rb', PointC),
                ('result_text', c_char_p)]

def OpenChannel(channelParam):
    param = OpenChannelParamC()
    param.host_ip = channelParam.host_ip
    param.port = channelParam.port
    param.channel_name = channelParam.channel_name
    param.content_type = channelParam.content_type

    return hiaiApp.OpenChannelEx(byref(param))

def SendImage(channel, imageId, imageData, detectionResult):
    imageDataC = CreateImageDataC(imageId, imageData)
    size = len(detectionResult)
    detectionResultC = (DetectionResultC * size)()
    #print("SendImage, result size", size, ", channel ", channel)
    for i in range(0, size):
        detectionResultC[i].lt.x = int(detectionResult[i].lt.x)
        detectionResultC[i].lt.y = int(detectionResult[i].lt.y)
        detectionResultC[i].rb.x = int(detectionResult[i].rb.x)
        detectionResultC[i].rb.y = int(detectionResult[i].rb.y)
        detectionResultC[i].result_text = detectionResult[i].result_text
    ret = hiaiApp.SendImage(channel, byref(imageDataC), byref(detectionResultC), size)

    return ret

