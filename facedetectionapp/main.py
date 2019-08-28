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
import time
import sys
import mind_camera_datasets as datasetengine
import face_detection_inference as inferenceengine
import face_detection_post_process as postprocessengine
from hiaiapp.appgraph import *
from hiaiapp.message import*

if __name__ == "__main__":
    #1.创建APP图
    faceDetectGraph = AppGraph(graphConfigFile='graph.config')

    engineList = []
    #2.获取配置文件graph.config中的camera engine配置并创建engine
    cameraConfig = faceDetectGraph.GetAIConfig("Mind_camera_datasets")
    if cameraConfig == None:
        print("Get camera engine configuration failed!")
        sys.exit(0)
    cameraEngine = datasetengine.MindCameraDatasets(cameraConfig.ai_config)
    cameraEngine.SubscribleMsg(['start', ])
    engineList.append(cameraEngine)

    #3.获取配置文件graph.config中的inference engine配置并创建engine
    inferenceConfig = faceDetectGraph.GetAIConfig("face_detection_inference")
    if inferenceConfig == None:
        print("Get inference engine configuration failed!")
        sys.exit(0)
    inferenceEngine = inferenceengine.FaceDetectionInference(inferenceConfig.ai_config)
    inferenceEngine.SubscribleMsg(['BatchImageParamWithScale', ])
    engineList.append(inferenceEngine)

    #4.获取配置文件graph.config中的post process engine配置并创建engine
    postConfig = faceDetectGraph.GetAIConfig("face_detection_post_process")
    if postConfig == None:
        print("Get post process engine configuration failed!")
        sys.exit(0)
    postEngine = postprocessengine.FaceDetectionPostProcess(postConfig.ai_config)
    postEngine.SubscribleMsg(['EngineTrans', ])
    engineList.append(postEngine)

    faceDetectGraph.StartupEngines(engineList)
    SendData('start', 'start work')

    while True:
        time.sleep(20)

