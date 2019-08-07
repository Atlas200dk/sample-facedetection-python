#! /usr/bin/env python
# coding=utf-8

#import hiai_media.hiai as hiai
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
    def __init__(self,  engineConfig):
        self.fd_model_desc = engineConfig.ai_model
        #for item in aiConfig._ai_config_item:
        #    if item.__name == "model_path":
        #        self.fd_model_desc.path(item.__value)
        #        break
        #self.aiConfig = aiConfig
        self.subscribMsgList = ["BatchImageParaWithScaleT", ]
        self.dvpp = dvpp.Dvpp()

    def ImageSizeAlign(self, size):
        if size % 2 == 0:
            return size - kImagePixelOffsetEven
        else:
            return size - kImagePixelOffsetOdd

    def ImagePreProcess(self, srcImg, resizedImg):
        if srcImg.format != image.IMAGEFORMAT.YUV420SP:
            print("[ODInferenceEngine] input image type does not match")
            return -1
        resolution = image.ResolutionRatio(kModelWidth, kModelHeight)
        self.dvpp.ResizeImage(resizedImg, srcImg, resolution)

        return 0

    def ConvertImage(self, dstImg, srcImg):
        if srcImg.img.format != image.IMAGEFORMAT.YUV420SP:
            print("Format %d is not supported!", srcImg.img.format)
            return -1
        ret = dvpp.ConvImageYuvToJpeg(dstImg, srcImg.img)
        return ret

    def ResizeImageOfFrames(self, srcFrames):
        resizedImgList = []
        for i in range(0, srcFrames.b_info.batch_size):
            resizedImg = IMG.ImageData()
            ret = self.ImagePreProcess(srcFrames.v_img[i].img, resizedImg)
            if ret != 0:
                print("image pre process error")
                continue
            resizedImgList.push_back(resizedImg);
        return resizedImgList

    def ConvImageOfFramesToJpeg(self, srcFrames):
        jpegImgList = []
        for i in range(0, srcFrames.b_info.batch_size):
            jpegImg = IMG.ImageData()
            ret = self.ConvertImage(jpegImg, srcFrames.v_img[i].img)
            if ret != 0:
                print("Convert YUV Image to Jpeg failed!")
                return -1, None
            jpegImgList.append(jpegImg)
        return 0, jpegImgList

    def ExcuteInference(self, images):
        tensors = []
        for i in range(0, len(images)):
            imgTensor = hiai.NNTensor(images[i].data, encoding = dvpp.JPEGFORMAT.JPGENC_FORMAT_NV12)
            tensors.append(imgTensor)
        tensorList = hiai.NNTensorList(tensors)

        return hiai.engine.inference(tensorList, self.fd_model_desc, self.aiConfig)

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
        print("Start process!")
        resizedImgList = self.ResizeImageOfFrames(data)
        ret, jpegImgList = self.ConvImageOfFramesToJpeg(data)
        if ret != 0:
            return -1

        transData = datatype.EngineTransT()
        transData.imgs = jpegImgList
        transData.b_info = data.b_info

        outputTensorList = self.ExcuteInference(resizedImgList)
        ret, output = self.GetInferenceOutput(outputTensorList, self)
        if ret == 0:
            transData.status = True
            transData.output_datas = output
        else:
            transData.status = False
            transData.msg = "HiAIInference Engine Process failed"

        self.SendData("EngineTransT", transData)
        print("End process!")

        return ret

