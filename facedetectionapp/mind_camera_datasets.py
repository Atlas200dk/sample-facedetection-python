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

import sys
from hiaiapp.hiaiapp import *
from hiaiapp.appgraph import *
from hiaiapp.camera import *
from hiaiapp.image import *
from hiaiapp.message import*
from datatype import *
import time
import datetime
import math

CAMERADATASETS_INIT = 0
CAMERADATASETS_RUN = 1
CAMERADATASETS_STOP = 2
CAMERADATASETS_EXIT = 3

CAMERAL_1 = 0
CAMERAL_2 = 1
PARSEPARAM_FAIL = -1

CAMERA_OK = 0
CAMERA_NOT_CLOSED = -1
CAMERA_OPEN_FAILED = -2
CAMERA_SET_PROPERTY_FAILED = -3

class CameraDatasetsConfig:
    def __init__(self):
        self.fps = 0
        self.frameId = 0
        self.cameraId = PARSEPARAM_FAIL
        self.imageFormat = PARSEPARAM_FAIL
        self.resolution = Resolution(0, 0)

class MindCameraDatasets(AppEngine):
    def __init__(self, aiConfig):
        print("Create camera engine start..")
        self.ParseConfig(aiConfig)
        if self.CheckConfig():
            print("Camera configuration invalid!")
            sys.exit(0)

        self.interval = round(1/self.config.fps, 3)

        print("Create camera engine success")
        
    def ParseConfig(self, aiConfig):
        param = {"Channel-1": CAMERAL_1,
                 "Channel-2": CAMERAL_2,
                 "YUV420SP": CameraImageFormat.CAMERA_IMAGE_YUV420_SP.value}

        self.config = CameraDatasetsConfig()
        #get camera configuration from graph.config
        for item in aiConfig._ai_config_item:
            if item._AIConfigItem__name == "fps":
                self.config.fps = int(item._AIConfigItem__value)
            elif (item._AIConfigItem__name == "image_format"):
                self.config.imageFormat = param[item._AIConfigItem__value]
            elif item._AIConfigItem__name == "data_source":
                self.config.cameraId = param[item._AIConfigItem__value]
            elif item._AIConfigItem__name == "image_size":
                resolutionStr = item._AIConfigItem__value.split('x')
                self.config.resolution.width = int(resolutionStr[0])
                self.config.resolution.height = int(resolutionStr[1])
            else:
                print("unused config name:", item._AIConfigItem__name)
    
    def CheckConfig(self):
        ret = HIAI_APP_OK
        if (self.config.imageFormat == PARSEPARAM_FAIL or
            self.config.cameraId == PARSEPARAM_FAIL or
            self.config.resolution.width == 0 or
            self.config.resolution.height == 0):
            print("config data invalid: ", self.config)
            ret = HIAI_APP_ERROR

        return ret
    
    #The camera engine Entry
    def Process(self, data):
        print("Camera engine recv msg: ", data)
        self.DoCapProcess()        
       
        if GetExitFlag() == True:
            print("Camera engine exit for exit flag be set")
            sys.exit(0)

 
    def DoCapProcess(self):
        #open the camera end set camera property
        if HIAI_APP_OK != self.PreCapProcess():
            CloseCamera(self.config.cameraId)
            raise Exception("Pre process camera failed")
            
        SetExitFlag(False)
        print("start get frame from camera, exitflag is ", GetExitFlag())
        #The loop of get image from camera
        while GetExitFlag() == False:
            #create the object instance 
            imagePatch = BatchImageParamWithScale(self.config.frameId, self.config.cameraId,
                                                 self.config.resolution.width, self.config.resolution.height,
                                                 YuvImageSize(self.config.resolution))
            imageParam = imagePatch.imageList[0]
            #get the image from camera
            ret = ReadFrameFromCamera(self.config.cameraId, imageParam)
            if ret == 0:
                print("Read frame from camera failed")
                continue
            #send image data to inference engine
            SendData("BatchImageParamWithScale", imagePatch)
            self.config.frameId += 1
        CloseCamera(self.config.cameraId)

    def PreCapProcess(self):
        ret = InitCamera()
        print("Init camera return ", ret)

        status = QueryCameraStatus(self.config.cameraId)
        print("Camera Id %d status %d"%(self.config.cameraId,status))
        if status != CameraStatus.CAMERA_STATUS_CLOSED.value:
            print("Query camera stuts error: ", status)
            return HIAI_APP_ERROR

        print("Starting open camera")
        if 0 == OpenCamera(self.config.cameraId):
            print("Open camera %d faild"%(self.config.cameraId))
            return HIAI_APP_ERROR

        print("Starting Set camera property FPS")
        if 0 == SetCameraProperty(self.config.cameraId,
                                           CameraProperties.CAMERA_PROP_FPS, self.config.fps):
            print("Set camera fps:%d failed"%self.config.fps)
            return HIAI_APP_ERROR

        print("Starting set camera property IMAGE_FORMAT")
        if 0 == SetCameraProperty(self.config.cameraId, CameraProperties.CAMERA_PROP_IMAGE_FORMAT,
                                           self.config.imageFormat):
            print("Set image fromat:%d failed"%(self.config.imageFormat))
            return HIAI_APP_ERROR

        print("Starting set camera property RESOLUTION")
        if 0 == SetCameraProperty(self.config.cameraId,
                                           CameraProperties.CAMERA_PROP_RESOLUTION, self.config.resolution):
            print("Set camera resolution{width:%d, height:%d} failed"%(self.config.resolution_width, self.config.resolution_height))
            return HIAI_APP_ERROR

        print("info:Starting Set CameraProperty CAP MODE")
        if 0 == SetCameraProperty(self.config.cameraId, CameraProperties.CAMERA_PROP_CAP_MODE, CameraCapMode.CAMERA_CAP_ACTIVE.value):
            print("[CameraDatasets]Set cap mode:%d failed"%(CameraCapMode.CAMERA_CAP_ACTIVE))
            return HIAI_APP_ERROR

        print("camera preprocess ok!")
        return CAMERA_OK

