import time
import ctypes
from ctypes import *
from multiprocessing import Process, Lock
import DataType as datatype
import hiai_media.image as image
import hiai_media.camera as camera
import hiai_media.engineobject as engineobject

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
        self.frame_id = 0
        self.channel_id = PARSEPARAM_FAIL
        self.image_format = PARSEPARAM_FAIL
        self.resolution_width = 0
        self.resolution_height = 0


class MindCameraDatasets(engineobject.EngineObject):
    def __init__(self, aiConfig):
        print("I am camera")
        self.mutex = Lock()
        self.subscribMsgList = ['start', ]
        self.SetExitFlag(CAMERADATASETS_INIT)
	print('info:Starting Parse Config')
        self.ParseConfig(aiConfig)
        self.param = None
	print('info:Starting Init Camera')
        self.cap = camera.Camera()
        if self.CheckConfig():
            return

    def ParseConfig(self, aiConfig):
        self.param = {"Channel-1": CAMERAL_1,
                      "Channel-2": CAMERAL_2,
                      "YUV420SP": camera.CameraImageFormat.CAMERA_IMAGE_YUV420_SP.value}

        self.config = CameraDatasetsConfig()
        for item in aiConfig._ai_config_item:
            if item._AIConfigItem__name == "fps":
                self.config.fps = int(item._AIConfigItem__value)
            elif (item._AIConfigItem__name == "image_format"):
                self.config.image_format = self.param[item._AIConfigItem__value]
            elif item._AIConfigItem__name == "data_source":
                self.config.channel_id = self.param[item._AIConfigItem__value]
            elif item._AIConfigItem__name == "image_size":
                resolutionStr = item._AIConfigItem__value.split('x')
                self.config.resolutionWidth = int(resolutionStr[0])
                self.config.resolutionHeight = int(resolutionStr[1])
            else:
                print("unused config name:", item._AIConfigItem__name)

    def CheckConfig(self):
        ret = 0
        if (self.config.image_format == PARSEPARAM_FAIL
                or self.config.channel_id == PARSEPARAM_FAIL
                or self.config.resolutionWidth == 0 or self.config.resolutionHeight == 0):
            print("config data invalid: ", self.config)
            ret = -1

        return ret

    def Process(self, recv_data=""):
        print("I am camera process msg")
        print("[CameraDatasets] start process!")
        self.DoCapProcess()
        print("[CameraDatasets] end process!")
        return 0

    def PreCapProcess(self):
        status = self.cap.QueryCameraStatus(self.config.channel_id)
	print('info:Camera Id %d status %d'%(self.config.channel_id,status))
        if status != camera.CameraStatus.CAMERA_STATUS_CLOSED.value:
            print("[CameraDatasets]Camera stuts error: ", status)
            return CAMERA_NOT_CLOSED
	print("info:Starting Open Camera")
        if 0 == self.cap.OpenCamera(self.config.channel_id):
            print("[CameraDatasets]Open camera %d faild", self.config.channel_id)
            return CAMERA_OPEN_FAILED
	print("info:Starting Set CameraProperty FPS")
        if 0 == self.cap.SetCameraProperty(self.config.channel_id,
                                           camera.CameraProperties.CAMERA_PROP_FPS, self.config.fps):
            print("[CameraDatasets]Set fps:%d failed", self.config.fps)
            return CAMERA_SET_PROPERTY_FAILED
	print("info:Starting Set CameraProperty IMAGE_FORMAT")
        if 0 == self.cap.SetCameraProperty(self.config.channel_id, camera.CameraProperties.CAMERA_PROP_IMAGE_FORMAT,
                                           self.config.image_format):
            print("[CameraDatasets]Set image fromat:%d failed", self.config.image_format)
            return CAMERA_SET_PROPERTY_FAILED

        resolution = camera.CameraResolution(self.config.resolution_width, self.config.resolution_height)
	print("info:Starting Set CameraProperty RESOLUTION")
        if 0 == self.cap.SetCameraProperty(self.config.channel_id,
                                           camera.CameraProperties.CAMERA_PROP_RESOLUTION, resolution):
            print("[CameraDatasets]Set resolution{width:%d, height:%d} failed",
                  self.config.resolution_width, self.config.resolution_height)
            return CAMERA_SET_PROPERTY_FAILED
	print("info:Starting Set CameraProperty CAP MODE")
        if 0 == self.cap.SetCameraProperty(self.config.channel_id, camera.CameraProperties.CAMERA_PROP_CAP_MODE,
                                           camera.CameraCapMode.CAMERA_CAP_ACTIVE):
            print("[CameraDatasets]Set cap mode:%d failed", camera.CameraCapMode.CAMERA_CAP_ACTIVE)
            return CAMERA_SET_PROPERTY_FAILED

        return CAMERA_OK

    def CreateBatchImageParaObj(self):
        pobj = datatype.BatchImageParaWithScaleT()
        pobj.b_info.is_first = (self.config.frame_id == 0)
        pobj.b_info.is_last = False  # handle one batch every time
        pobj.b_info.batch_size = 1
        pobj.b_info.max_batch_size = 1
        pobj.b_info.batch_ID = 0
        pobj.b_info.channel_ID = self.config.channel_id
        pobj.b_info.processor_stream_ID = 0
        self.config.frame_id = self.config.frame_id + 1
        pobj.b_info.frame_ID.append(self.config.frame_id)
        pobj.b_info.timestamp.append(time.time())

        img_data = datatype.NewImageParaT()
        # channel begin from zero
        img_data.img.channel = 0
        img_data.img.format = image.IMAGEFORMAT.YUV420SP
        img_data.img.width = self.config.resolution_width
        img_data.img.height = self.config.resolution_height
        # YUV size in memory is width * height * 3 / 2
        img_data.img.size = self.config.resolution_width * self.config.resolution_height * 3 / 2
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
        while self.GetExitFlag() == CAMERADATASETS_RUN:
            imagePatch = self.CreateBatchImageParaObj()
            imgData = imagePatch.v_img[0]
            imgSize = imgData.img.size

            # do read frame from camera
            ret, readSize = self.cap.ReadFrameFromCamera(self.config.channel_id, imgData.img.data, imgSize)
            if ret != 1:
                print("[CameraDatasets]Read frame from camera failed {camera:%d, ret:%d, size:%d, expectsize:%d}",
                      self.config.channel_id, ret, readSize, imgData.img.size)
                break
            f = open(str(i) + '.png', 'wb')
            f.write(imgData.img.data)
            f.close()

            ret = self.SendData("BatchImageParaWithScaleT", imagePatch)
            if ret != 0:
                print("[CameraDatasets] senddata failed! {frameid:%d, timestamp:%lu}", imagePatch.b_info.frame_ID[0],
                      imagePatch.b_info.timestamp[0])
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

