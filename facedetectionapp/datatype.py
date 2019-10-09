#! /usr/bin/env python
# coding=utf-8
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

from hiaiapp.image import *
import time

class ScaleInfo:
    def __init__(self):
        self.scaleWidth = 1
        self.scaleHeight = 1

class NewImageParam:
    def __init__(self, width = 0, height = 0, size = 0, imageId = 0):
        self.imageId = imageId
        self.frameInfo = FrameInfo()
        self.imageData = ImageData(width, height, size)
        self.scaleInfo = ScaleInfo()

class FrameInfo:
    def __init__(self):
        self.isFirst = False  # 是否为第一个frame
        self.isLast = False  # 是否为最后一个frame
        self.channelId = 0  # 处理当前frame的通道ID号
        self.processorStreamId = 0  # 处理器计算流ID号
        self.frameId = 0  # 图像帧ID号
        self.sourceId = 0  # 图像源ID号
        self.timestamp = 0  # 图像的时间戳

class BatchInfo:
    def __init__(self, frameId = 0, cameraId = 0):
        self.isFirst = (frameId == 0)
        self.isLast = False
        self.batchSize = 1
        self.maxBatchSize = 1
        self.batchId = 0
        self.channelId = cameraId
        self.processorStreamId = 0
        self.frameId = [frameId, ]
        self.timestamp = [time.time(), ]

class BatchImageParamWithScale:
    def __init__(self, frameId = 0, cameraId = 0, width = 0, height = 0, size = 0, imageId = 0):
        self.batchInfo = BatchInfo(frameId, cameraId)
        imageParam = NewImageParam(width, height, size, imageId)
        self.imageList = [imageParam, ]

class EngineTrans:
    def __init__(self):
        self.status = 0
        self.msg = None
        self.batchInfo = None
        self.outputData = None
        self.widthScale = 1.0
        self.heightScale = 1.0
        self.imageParamList = None

exitFlag = False

def SetExitFlag(flag):
    exitFlag = flag

def GetExitFlag():
    return exitFlag
