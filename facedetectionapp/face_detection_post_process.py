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
import sys
import hiai
from hiaiapp.appgraph import *
from hiaiapp.presenteragent import *
from datatype import *
from datetime import *

# constants
# face label font
kFaceLabelFontSize = 0.7  # double
kFaceLabelFontWidth = 2  # int

# confidence range
kConfidenceMin = 0.0  # doulbe.
kConfidenceMax = 1.0
# need to deal results when index is 2
kDealResultIndex = 2
# each results size
kEachResultSize = 7
# attribute index
kAttributeIndex = 1
# score index
kScoreIndex = 2
# anchor_lt.x index
kAnchorLeftTopAxisIndexX = 3
# anchor_lt.y index
kAnchorLeftTopAxisIndexY = 4
# anchor_rb.x index
kAnchorRightBottomAxisIndexX = 5
# anchor_rb.y index
kAnchorRightBottomAxisIndexY = 6
# face attribute
kAttributeFaceLabelValue = 1.0  # float.
kAttributeFaceDeviation = 0.00001
# percent
kScorePercent = 100  # int32

# face label text prefix
kFaceLabelTextPrefix = 'Face:'
kFaceLabelTextSuffix = '%'

class FaceDetectPostConfig:
    def __init__(self):
        self.confidence = None     #The confidence of face detection
        self.presenterIp = None    #The presenter server ip
        self.presentPort = None    #The presenter server port
        self.channelName = None    #The presenter server channel, default is vedio

class FaceDetectionPostProcess(AppEngine):
    def __init__(self, aiConfig):
        print("Create post process engine start...")
        self.config = FaceDetectPostConfig()
        self.ParseConfig(aiConfig)
        self.channel = self.OpenChannel()
        if self.channel < 0:
            raise Exception("Open presenter channel failed")

        print("Create post process engine success")

    def ParseConfig(self, aiConfig):
        #Get config from graph.config
        for item in aiConfig._ai_config_item:
            if item._AIConfigItem__name == "Confidence":
                self.config.confidence = float(item._AIConfigItem__value)
            if item._AIConfigItem__name == "PresenterIp":
                self.config.presenterIp = item._AIConfigItem__value
            if item._AIConfigItem__name == "PresenterPort":
                self.config.presenterPort = int(item._AIConfigItem__value)
            if item._AIConfigItem__name == "ChannelName":
                self.config.channelName = item._AIConfigItem__value
    
    #Create link socket with presenter server
    def OpenChannel(self):
        openchannelparam = OpenChannelParam()
        openchannelparam.host_ip = self.config.presenterIp
        openchannelparam.port = self.config.presenterPort
        openchannelparam.channel_name = self.config.channelName
        openchannelparam.content_type = 1
        return OpenChannel(openchannelparam)
 
    def IsInvalidConfidence(self, confidence):
        return (confidence <= kConfidenceMin) or (confidence > kConfidenceMax)

    def IsInvalidResults(self, attr, score, point_lt, point_rb):
        if abs(attr - kAttributeFaceLabelValue) > kAttributeFaceDeviation:
            return True
        #Face detection confidence too low
        if (score < self.config.confidence or self.IsInvalidConfidence(score)) :
	        return True
            
        #Face rectangle in the image is invalid
        if (point_lt.x == point_rb.x) and (point_lt.y == point_rb.y):
            return True
        return False

    #When inference failed, we just send origin jpeg image to presenter server to display
    def HandleOriginalImage(self, inference_res):
        imgParam = inference_res.imageParamList[0]
        
        ret = SendImage(self.channel, imgParam.imageId, imgParam.imageData, [])
        if ret != HIAI_APP_OK:
            print("Send image failed, return ")
  
    #Parse the face detection confidence and face position in the image from inference result
    def HandleResults(self, inferenceData):
        jpegImageParam = inferenceData.imageParamList[0]
        inferenceResult = inferenceData.outputData[0][0]
        widthWithScale = round(inferenceData.widthScale * jpegImageParam.imageData.width, 3)
        heightWithScale = round(inferenceData.heightScale * jpegImageParam.imageData.height, 3)

        detectionResults = []
        for i in range(0, inferenceResult.shape[0]):
            for j in range(0, inferenceResult.shape[1]):
                for k in range(0, inferenceResult.shape[2]):
                    result = inferenceResult[i][j][k]
                    attr = result[kAttributeIndex]
                    score = result[kScoreIndex] #face detection confidence
                    
                    #Get the face position in the image
                    one_result = DetectionResult()
                    one_result.lt.x = result[kAnchorLeftTopAxisIndexX] * widthWithScale
                    one_result.lt.y = result[kAnchorLeftTopAxisIndexY] * heightWithScale
                    one_result.rb.x = result[kAnchorRightBottomAxisIndexX] * widthWithScale
                    one_result.rb.y = result[kAnchorRightBottomAxisIndexY] * heightWithScale
                    if self.IsInvalidResults(attr, score, one_result.lt, one_result.rb):
                        continue
                    print("score=%f, lt.x=%d, lt.y=%d, rb.x=%d rb.y=%d",
                          score, one_result.lt.x, one_result.lt.y,one_result.rb.x, one_result.rb.y)

                    score_percent = score * kScorePercent
                    #Construct the face detection confidence string
                    one_result.result_text = kFaceLabelTextPrefix + str(score_percent) + kFaceLabelTextSuffix
                    detectionResults.append(one_result)
        #Send the face position, confidence string and image to presenter server
        ret = SendImage(self.channel, jpegImageParam.imageId, jpegImageParam.imageData, detectionResults)
        if ret != HIAI_APP_OK:
            print("Post process engine send image failed")

        return True
    #The post process engine Entry
    def Process(self, data):
        start = datetime.now()

        if data.outputData == None or data.outputData[0] == None or data.status == False:
            print("post engine handle original image.")
            ret = self.HandleOriginalImage(data)
        else:
            ret = self.HandleResults(data)


        end = datetime.now() - start
        print("Post process exhoust ", end.total_seconds())

        if GetExitFlag() == True:
            print("Camera engine exit for exit flag be set")
            sys.exit(0)

        return ret
