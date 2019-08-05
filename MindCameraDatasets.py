#! /usr/bin/env python
# coding=utf-8

import time
import ctypes
from ctypes import *
from multiprocessing import Process,Lock
import DataType as datatype
import hiai_media.image as image
import hiai_media.camera as camera
import hiai_media.engineobject as engineobject

CAMERADATASETS_INIT = 0
CAMERADATASETS_RUN  = 1
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
        self.channelId = PARSEPARAM_FAIL
        self.imageFormat = PARSEPARAM_FAIL
        self.resolutionWidth = 0
        self.resolutionHeight = 0

class MindCameraDatasets(engineobject.EngineObject):
    def __init__(self, aiConfig):
        print("I am camera")
        self.mutex = Lock()
        self.subscritMsgType = ['start', ]
        self.SetExitFlag(CAMERADATASETS_INIT)
        self.config = CameraDatasetsConfig()
        self.ParseConfig(aiConfig)
        if self.CheckConfig():
            return

    def ParseConfig(self, aiConfig):
        self.param = {"Channel-1": str(CAMERAL_1),
                      "Channel-2": str(CAMERAL_2),
                      "YUV420SP":  str(camera.CameraImageFormat.CAMERA_IMAGE_YUV420_SP)}

        self.config = CameraDatasetsConfig()
        itemList = aiConfig.AiConfigItem()
        for item in itemList:
            itemName = item.name()
            if itemName == "fps":
                self.config.fps = int(item.value())
            elif (itemName == "image_format"):
                self.config.image_format = str(self.param[item.value()])
            elif itemName == "data_source":
                self.config.channel_id = int(self.param[item.value()])
            elif itemName == "image_size":
                resolutionStr = item.value().split('x')
                self.config.resolutionWidth = int(resolutionStr[0])
                self.config.resolutionHeight = int(resolutionStr[1])
            else:
                print("unused config name:", itemName)

    def CheckConfig(self):
        ret = 0
        if (self.config.imageFormat == PARSEPARAM_FAIL
            or self.config.channelId == PARSEPARAM_FAIL
            or self.config.resolutionWidth == 0 or self.config.resolutionHeight == 0):
            print("config data invalid: ", self.config)
            ret = -1

        return ret

    def Process(self, recv_data = ""):
        print("I am camera process msg")
        print("[CameraDatasets] start process!")
        self.DoCapProcess()
        print("[CameraDatasets] end process!")
        return 0

    def PreCapProcess(self):
        self.cap = camera.Camera()

        status = self.cap.QueryCameraStatus(self._config.channel_id)
        if status != camera.CameraStatus.CAMERA_STATUS_CLOSED:
            print("[CameraDatasets]Camera stuts error: ", status)
            return CAMERA_NOT_CLOSED

        if 0 == self.cap.OpenCamera(self.config.channelId):
            print("[CameraDatasets]Open camera %d faild", self.config.channelId)
            return CAMERA_OPEN_FAILED

        if 0 == self.cap.SetCameraProperty(self.config.channelId,
                                           camera.CameraProperties.CAMERA_PROP_FPS, self.config.fps):
            print("[CameraDatasets]Set fps:%d failed", self._config.fps)
            return CAMERA_SET_PROPERTY_FAILED

        if 0 == self.cap.SetCameraProperty(self._config.channel_id, camera.CameraProperties.CAMERA_PROP_IMAGE_FORMAT,
                                           self._config.image_format):
            print("[CameraDatasets]Set image fromat:%d failed", self.config.image_format)
            return CAMERA_SET_PROPERTY_FAILED

        resolution = camera.CameraResolution(self.config.resolution_width, self.config.resolution_height)
        if 0 == self.cap.SetCameraProperty(self.config.channel_id,
                                           camera.CameraProperties.CAMERA_PROP_RESOLUTION, resolution):
            print("[CameraDatasets]Set resolution{width:%d, height:%d} failed",
                  self._config.resolution_width, self.config.resolution_height)
            return CAMERA_SET_PROPERTY_FAILED

        if 0 == self.cap.SetCameraProperty(self.config.channel_id, camera.CameraProperties.CAMERA_PROP_CAP_MODE,
                                           camera.CameraCapMode.CAMERA_CAP_ACTIVE):
            print("[CameraDatasets]Set cap mode:%d failed", camera.CameraCapMode.CAMERA_CAP_ACTIVE)
            return CAMERA_SET_PROPERTY_FAILED

        return CAMERA_OK

    def CreateBatchImageParaObj(self):
        pobj = datatype.BatchImageParaWithScaleT()
        pobj.b_info.is_first = (self.frame_id == 0)
        pobj.b_info.is_last = False #handle one batch every time
        pobj.b_info.batch_size = 1
        pobj.b_info.max_batch_size = 1
        pobj.b_info.batch_ID = 0
        pobj.b_info.channel_ID = self.channel_id
        pobj.b_info.processor_stream_ID = 0
        self.frame_id_ = self.frame_id_ + 1
        pobj.b_info.frame_ID.append(self.frame_id_)
        pobj.b_info.timestamp.append(time.time())

        img_data = image.NewImageParaT()
        #channel begin from zero
        img_data.img.channel = 0
        img_data.img.format = image.IMAGEFORMAT.YUV420SP
        img_data.img.width = self.resolution_width
        img_data.img.height = self.resolution_height
        # YUV size in memory is width * height * 3 / 2
        img_data.img.size = self.resolution_width * self.resolution_height * 3 / 2
        img_data.img.data = (c_byte * img_data.img.size)()

        pobj.v_img.append(img_data)

        return pobj

    def DoCapProcess(self):
        if CAMERA_SET_PROPERTY_FAILED == self.PreCapProcess():
            self.cap.CloseCamera(self.config.channel_id)
            print("[CameraDatasets]Pre process camera failed")
            return False

        self.SetExitFlag(CAMERADATASETS_RUN)
        i = 0
        while (self.GetExitFlag() == CAMERADATASETS_RUN):
            imagePatch = self.CreateBatchImageParaObj()
            imgData = imagePatch.v_img[0]
            imgSize = imgData.img.size

            # do read frame from camera
            ret, readSize = self.cap.ReadFrameFromCamera(self.config.channelId, imgData.img.data, imgSize)
            if ret != 1:
                print("[CameraDatasets]Read frame from camera failed {camera:%d, ret:%d, size:%d, expectsize:%d}",
                       self.config.channelId, ret, readSize, imgData.img.size)
                break
            #f = open(str(i) + '.png', 'wb')
            #f.write(imgData.img.data)
            #f.close()

            ret = self.SendData("BatchImageParaWithScaleT", imagePatch)
            if ret != 0:
                print("[CameraDatasets] senddata failed! {frameid:%d, timestamp:%lu}", imagePatch.b_info.frame_ID[0], imagePatch.b_info.timestamp[0]);
                break
        self.cap.CloseCamera(self.config.channel_id)

    def SetExitFlag(self, flag):
        self.mutex.acquire()
        self.exitFlag = flag
        self.mutex.release()

    def GetExitFlag(self):
        self.mutex.acquire()
        flag = self.exitFlag
        self.mutex.release()
        return flag
