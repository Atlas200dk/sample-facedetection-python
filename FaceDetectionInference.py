#! /usr/bin/env python
# coding=utf-8

import hiai
import hiai_media.image as image
import hiai_media.dvpp as dvpp
import hiai_media.engineobject as engineobject
import DataType as datatype

kModelWidth = 300  # face detection model input width
kModelHeight = 300  # face detection model input height
kDvppProcSuccess = 0  # call dvpp success
kDvppToJpegLevel = 100  # level for call DVPP
# vpc input image offset
kImagePixelOffsetEven = 1
kImagePixelOffsetOdd = 2

class FaceDetectionInference(engineobject.EngineObject):
    def __init__(self,  aiConfig):
        for item in aiConfig._ai_config_item:
            if item._AIConfigItem__name == "model_path":
                modePath = item._AIConfigItem__value
                break
        self.fd_mode_desc = hiai.AIModelDescription("face_detect", modePath)
        self.aiConfig = aiConfig
        self.subscribMsgList = ["BatchImageParaWithScaleT", ]
        self.dvpp = dvpp.Dvpp()
        self.imageIndex = 0
        

    def ImageSizeAlign(self, size):
        if size % 2 == 0:
            return size - kImagePixelOffsetEven
        else:
            return size - kImagePixelOffsetOdd

    def ImagePreProcess(self, srcImg, resizedImg):
        if srcImg.format != image.IMAGEFORMAT.YUV420SP:
            print("[InferenceEngine] input image type does not match")
            return -1
        resolution = image.ResolutionRatio(kModelWidth, kModelHeight)
        return self.dvpp.ResizeImage(resizedImg, srcImg, resolution)


    def ConvertImage(self, dstImg, srcImg):
        if srcImg.format != image.IMAGEFORMAT.YUV420SP:
            print("[Conv]Format %d is not supported!", srcImg.img.format)
            return -1
        return self.dvpp.ConvertImageYuvToJpeg(dstImg, srcImg)


    def ResizeImageOfFrames(self, srcFrames):
        resizedImgList = []
        for i in range(0, srcFrames.b_info.batch_size):
            resizedImg = image.ImageData()
            ret = self.ImagePreProcess(srcFrames.v_img[i].img, resizedImg)
            if ret != 0:
                print("image pre process error")
                continue
            resizedImgList.append(resizedImg)
        return resizedImgList

    def ConvImageOfFramesToJpeg(self, srcFrames):
        jpegImgList = []
        for i in range(0, srcFrames.b_info.batch_size):
            jpegImg = image.ImageData()
            ret = self.ConvertImage(jpegImg, srcFrames.v_img[i].img)
            if ret != 0:
                print("Convert YUV Image to Jpeg failed!")
                return -1, None
            jpegImgList.append(jpegImg)

        return 0, jpegImgList

    def ExcuteInference(self, images):
        #tensors = []
        #for i in range(0, len(images)):
        #    print("trans ", "./" + str(self.imageIndex) + '.yuv', " to nntensor")
        #    imgTensor = hiai.NNTensor("./" + str(self.imageIndex) + '.yuv', height=300, width=300, channel=3, size=230400)
        #    tensors.append(imgTensor)
        tensorList = hiai.NNTensorList(hiai.NNTensor("./" + str(self.imageIndex) + '.yuv', height=300, width=300, channel=3,data_type=hiai.nn_tensor_lib.DataType.UINT8_T, size=135000))
        g1 = hiai.Graph("./graph.config")
        res = g1.create_graph()
        if res != hiai.HiaiPythonStatust.HIAI_PYTHON_OK:
            print("create graph error: ", res)
            return None 
  
        #return hiai.proc(tensorList, self.fd_mode_desc, self.aiConfig)
        return g1.proc(input_nntensorlist = tensorList)
       

    def GetInferenceOutput(self, inferenceResult):
        output = []

        tensorNum = inferenceResult.get_tensor_num()
        if tensorNum == 0:
            return -1, None

        for i in range(0, tensorNum):
            tensor = inferenceResult.__getitem__(i)
            outputData = datatype.OutputT()
            outputData.size = tensor.size()
            outputData.data = tensor.data_list()
            output.append(outputData)
        return 0, output

    def Process(self, data):
        print("Inference engine recv msg, start process!")
        self.imageIndex += 1
        print("image index ", self.imageIndex)
        resizedImgList = self.ResizeImageOfFrames(data)
        ret, jpegImgList = self.ConvImageOfFramesToJpeg(data)
        if ret != 0:
            return -1

        transData = datatype.EngineTransT()
        transData.imgs = jpegImgList
        transData.b_info = data.b_info
        transData.status = False

        outputTensorList = self.ExcuteInference(resizedImgList)
        ret, output = self.GetInferenceOutput(outputTensorList)
        if ret == 0:
            transData.status = True
            transData.output_datas = output
        else:
            transData.status = False
            transData.msg = "HiAIInference Engine Process failed"

        self.SendData("EngineTransT", transData)
        print("Inference engine process msg end")

        return ret

