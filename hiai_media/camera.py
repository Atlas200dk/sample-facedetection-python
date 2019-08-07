#! /usr/bin/env python
#coding=utf-8

import ctypes
from ctypes import *
from enum import Enum

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



#分辨率.
class CameraResolution:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class CameraResolution_C(Structure):
    _fields_ = [('width', c_int),
                ('height', c_int)]

class Camera:
    def __init__(self):
        self.camera = ctypes.CDLL("/usr/lib64/libmedia_mini.so")
        self.camera.MediaLibInit()

    def QueryCameraStatus(self, cameraId):
        return self.camera.QueryCameraStatus(cameraId)

    def OpenCamera(self, cameraId):
        return self.camera.OpenCamera(cameraId)

    def SetCameraProperty(self, cameraId, prop, val):
        
        if (prop == CameraProperties.CAMERA_PROP_RESOLUTION):
            arg = CameraResolution_C(val.width, val.height)
            #arg.width = val.width
            #arg.height = val.height
            print("resulution width ", arg.width, " height ", arg.height)
            pArg = byref(arg)
            #pArg = cast(arg, POINTER(CameraResolution_C))
            #print(pArg.contents.width, pArg.contents.height)
            
            
        else:
            arg = c_int(val)
            pArg = pointer(arg)
        print("property: ", prop, " val ", arg)
        return  self.camera.SetCameraProperty(cameraId, prop.value, pArg)

    def ReadFrameFromCamera(self, cameralId, dataBuf, size):
        #pdata = c_byte__p(dataBuf)
        imgSize = c_int(size)
        #psize =  pointer(imgSize)
        ret = self.camera.ReadFrameFromCamera(cameralId, byref(dataBuf), pointer(imgSize))
        print("Camer Data Received:",dataBuf)
        print("Data Lengh",imgSize)
        return ret, imgSize

    def CloseCamera(self, cameralId):
        return self.camera.CloseCamera(cameralId)
