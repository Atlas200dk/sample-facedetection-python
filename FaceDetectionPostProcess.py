import re
import hiai
import struct
import DataType as datatype
from ctypes import *
from ConstManager import  *
from multiprocessing import Process,Lock
from presenteragent.presenter_channel import *
import hiai_media.engineobject as engineobject
import DataType as datatype



class FaceDetectPostConfig:
    def __init__(self):
        self.confidene = None
        self.presenter_ip = None
        self.present_port = None
        self.channel_name = None


class Point_p:
    def __init__(self):
        self.x = None
        self.y = None


class DetectionResult_p:
    def __init__(self):
        self.lt = Point_p()
        # The coordinate of left top point
        self.rb = Point_p()
        # The coordinate of the right bottom point
        self.result_text = None  # Face:xx%

class FaceDetectionPostProcess(engineobject.EngineObject):
    def __init__(self, aiConfig):
        print("I am PostProcess")
        self.mutex = Lock()
        self.subscribMsgList= ['EngineTransT', ]
        self.fd_post_process_config_ = FaceDetectPostConfig()
        #self.libc = cdll.LoadLibrary("libface_detection_post_process.so")
        self.fd_post_process = {}
        # read config
        for item in aiConfig._ai_config_item:
            if item._AIConfigItem__name == "Confidence":
                if self.IsInvalidConfidence(float(item._AIConfigItem__value)):
                    print("Confidence=%s which configured is invalid.".item.__value)
                    return HIAI_ERROR
                self.fd_post_process_config_.confidence = float(item._AIConfigItem__value)
            if item._AIConfigItem__name == "PresenterIp":
                if self.IsInvalidIp(str(item._AIConfigItem__value)):
                    print("Presenter=%s which configured is invalid.", item._AIConfigItem__value)
                    return HIAI_ERROR
                self.fd_post_process_config_.presenter_ip = item._AIConfigItem__value
            if item._AIConfigItem__name == "PresenterPort":
                if self.IsInvalidPort(int(item._AIConfigItem__value)):
                    print("PresentPort=%s which configured is invalid.", item._AIConfigItem__value)
                    return HIAI_ERROR
                self.fd_post_process_config_.presenter_port = int(item._AIConfigItem__value)
            if item._AIConfigItem__name == "ChannelName":
                if self.IsInvalidChannelName(str(item._AIConfigItem__value)):
                    print("ChannelName=%s which configured is invalid.", item._AIConfigItem__value)
                    return HIAI_ERROR
                self.fd_post_process_config_.channel_name = item._AIConfigItem__value
        # read config end
        openchannelparam = OpenChannelParam()
        openchannelparam.host_ip = self.fd_post_process_config_.presenter_ip
        openchannelparam.port = self.fd_post_process_config_.presenter_port
        openchannelparam.channel_name = self.fd_post_process_config_.channel_name
        openchannelparam.content_type = ContentType_kVideo
        self.channel=OpenChannel_p(openchannelparam)
        print("End initialize")
        #return HIAI_OK

    def IsInvalidIp(self, ip):
        # if you think the comparison is bug, please amend the Regular expression or verify in manual
        return not re.match(kIpRegularExpression, ip)

    def IsInvalidPort(self, port):
        return (port <= kPortMinNumber) or (port > kPortMaxNumber)

    def IsInvalidChannelName(self, channel_name):
        # if you think the comparison is bug, please amend the Regular expression or verify in manual
        return not re.match(kChannelNameRegularExpression, channel_name)

    def IsInvalidConfidence(self, confidence):
        return (confidence <= kConfidenceMin) or (confidence > kConfidenceMax)

    def IsInvalidResults(self, attr, score, point_lt, point_rb):
        if abs(attr - kAttributeFaceLabelValue) > kAttributeFaceDeviation:
            return True
        if (score < self.fd_post_process_config_.confidence or self.IsInvalidConfidence(score)) :
	    return True
        if (point_lt.x == point_rb.x) and (point_lt.y == point_rb.y):
            return True
        return False

    def SendImage(self, height, width, size, data, detection_results):
        status = kFdFunSuccess
        sendimagedata = ImageFrame()
        sendimagedata.ImageFormat = ImageFormat_kJpeg
        sendimagedata.width = width
        sendimagedata.height = height
        sendimagedata.size = size
        sendimagedata.data = data
	sendimagedata.detection_results.clear()
	print 'y'
        for i in range (len(detection_results)):
            plt=Point()
            prb=Point()
            plt.x = detection_results[i].lt.x
            plt.y = detection_results[i].lt.y
            prb.x = detection_results[i].rb.x
            prb.y = detection_results[i].rb.y
            DR = DetectionResult()
            DR.rb = prb
            DR.rb = plt
            DR.result_text = detection_results[i].result_text
        sendimagedata.detection_results.push_back(DR)
        ret = PresentImage(self.channel,sendimagedata)
        if ret == -1:
            status = HIAI_ERROR
        return status

    #
    def HandleOriginalImage(self, inference_res):
        status = HIAI_OK
        print("[POST ENGINE]inference_res.b_info.batch_size ", inference_res.b_info.batch_size)
        for ind in range(0, inference_res.b_info.batch_size):
            img_vec = inference_res.imgs
            width = img_vec[ind].width
            height = img_vec[ind].height
            size = img_vec[ind].size
            print("[POST ENGINE]Send image, width ", width, ", height ", height, ", size ", size)
            ret = self.SendImage(height, width, size, img_vec[ind].data, DetectionResult())
            if ret == kFdFunFailed:
                status = HIAI_ERROR
                break
        return status

    ''' 
    def HandResults(self, inference_res):
        pass
  
        status = HIAI_OK
        img_vec = inference_res.img
        output_data_vec = inference_res.output_datas
        detection_results = 
        for ind in range(0, inference_res.b_info.batch_size):
            out_index = ind * kDealResultIndex
            out = output_data_vec[out_index]
            result_tensor = out
            width = img_vec[ind].img.width
            height = img_vec[ind].img.height
            img_size = img_vec[ind].img.size
            size = int(out.size / 4)
            data = out.data
            # get float data from binary data
            frame_str = str(size) + 'f'
            result = struct.unpack(frame_str, data)
            k = 0
            while k < size - kEachResultSize:
                attr = result[k + kAttributeIndex]
                score = result[k + kScoreIndex]
                one_result = DetectionResult_p()
                one_result.lt.x = result[kAnchorLeftTopAxisIndexX] * width
                one_result.lt.y = result[kAnchorLeftTopAxisIndexY] * height
                one_result.rb.x = result[kAnchorRightBottomAxisIndexX] * width
                one_result.rb.y = result[kAnchorRightBottomAxisIndexY] * height
                if self.isInvalidResults(attr, score, one_result.lt, one_result.rb):
                    continue
                print("score=%f, lt.x=%d, lt.y=%d, rb.x=%d rb.y=%d", score, one_result.lt.x, one_result.lt.y,
                      one_result.rb.x, one_result.rb.y)
                score_percent = score * kScorePercent
                one_result.result_text = kFaceLabelTextPrefix + str(score_percent) + kFaceLabelTextSuffix
                detection_results.append(one_result)
                k = k + kEachResultSize
            ret = self.SendImage(height, width, img_size, img_vec[ind].img.data, detection_results)
            if ret == kFdFunFailed:
                status = HIAI_ERROR
    '''
        #return True

    def Process(self, data):
        if data.status == False:
            print("post engine handle original image.")
            return self.HandleOriginalImage(data)
        #else:
        #    return self.HandleResults(data)
