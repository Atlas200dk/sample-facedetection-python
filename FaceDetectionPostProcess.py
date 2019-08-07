import re
from NNTensor import *
import struct
import DataType as datatype
from ctypes import *
from ConstManager import  *
from multiprocessing import Process,Lock
import DataType as datatype



class FaceDetectPostConfig:
    def __init__(self):
        self.confidene = None
        self.presenter_ip = None
        self.present_port = None
        self.channel_name = None


class Point:
    def __init__(self):
        x = None;
        y = None;


class DetectionResult:
    def __init__(self):
        self.lt = Point();
        # The coordinate of left top point
        self.rb = Point();
        # The coordinate of the right bottom point
        self.result_text = None;  # Face:xx%


class FaceDetectionPostConfig:
    def __init__(self):
        self.confidence = None
        self.presenter_ip = None
        self.presenter_port = None
        self.channel_name = None


class FaceDetectionPostProcess:
    def __init__(self, aiConfig):
        print("I am PostProcess")
        self.mutex = Lock()
        self.subscritMsgType = ['start', ]
        self.fd_post_process_conifg_ = FaceDetectionPostConfig()
        self.libc = cdll.LoadLibrary("libface_detection_post_process.so")
        self.fd_post_process = {}
        # read config
        for item in aiConfig._ai_config_item:
            if item._AIConfigItem__name == "Confidence":
                if self.IsInvalidConfidence(float(item._AIConfigItem__value)):
                    print("Confidence=%s which configured is invalid.".item.__value)
                    return HIAI_ERROR
                self.fd_post_process_config_.confidence = float(item._AIConfigItem__value)
            if item._AIConfigItem__name == "PresenterIp":
                if self.IsInvalidIp(float(item._AIConfigItem__value)):
                    print("Presenter=%s which configured is invalid.", item._AIConfigItem__value)
                    return HIAI_ERROR
                self.fd_post_process_config_.presenter_ip = item._AIConfigItem__value
            if item._AIConfigItem__name == "PresenterPort":
                if self.IsInvalidPPort(float(item.__value)):
                    print("PresentPort=%s which configured is invalid.", item._AIConfigItem__value)
                    return HIAI_ERROR
                self.fd_port_process_config_.presenter_port = int(item._AIConfigItem__value)
            if item._AIConfigItem__name == "ChannelName":
                if self.IsInvalidChannelName(float(item._AIConfigItem__value)):
                    print("ChannelName=%s which configured is invalid.", item._AIConfigItem__value)
                    return HIAI_ERROR
                self.fd_port_process_config_.channel_name = item._AIConfigItem__value
        # read config end
        # read .so please set the .so in correct path
        # if you think the transform may is bug, please add the printf in .cpp, make the .so and test it
        self.libc.openchannel_c.argtypes = [c_char_p, c_int, c_char_p]
        self.libc.openchannel_c.restype = c_void_p
        self.ch_ptr = self.libc.openchannel_c(
            self.fd_post_process_config_.presenter_ip,
            self.fd_post_process_config_.port,
            self.fd.post.process_config_.channel_name)
        # if you think the void ptr is bug, please change .cpp return nullptr to 0 or change in here
        if self.ch_ptr == 0:
            return HIAI_ERROR
        print("End initialize")
        return HIAI_OK

    def IsinvalidIp(self, ip):
        # if you think the comparison is bug, please amend the Regular expression or verify in manual
        return not re.match(kIpRegularExpression, ip)

    def IsinvalidPort(self, port):
        return (port <= kPortMinNumber) or (port > kPortMaxNumber)

    def IsinvalidChannelName(self, channel_name):
        # if you think the comparison is bug, please amend the Regular expression or verify in manual
        return not re.match(kChannelNameRegularExpression, channel_name)

    def IsinvalidConfidence(self, confidence):
        return (confidence <= kConfidenceMin) or (confidence > kConfidenceMax)

    def IsInvalidResults(self, attr, score, point_lt, point_rb):
        if abs(attr - kAttributeFaceLabelValue) > kAttributeFaceDeviation:
            return True
        if score < self.fd_post_process_config_.confidence or self.IsInvalidConfidence(score):
            return True
        if (point_lt.x == point_rb.x) and (point_lt.y == point_rb.y):
            return True
        return False

    def SendImage(self, height, width, size, data, detection_results):
        status = kFdFunSuccess
        # if you think the transform may is bug, please add the printf in .cpp, make the .so and test it
        self.libc.SendImage_c.argtypes = [c_int, c_int, c_int, c_ubyte_p, c_int_p, c_int_p, c_int_p, c_int_p, c_char_p,
                                     c_int, c_void_p]
        self.libc.SendImage_c.restypes = c_int
        lens = len(detection_results)
        str_lens = 0;
        lx_ = (c_int * lens)()
        ly_ = (c_int * lens)()
        rx_ = (c_int * lens)()
        ry_ = (c_int * lens)()
        for i in range(0, lens):
            lx_[i] = detection_results[i].lt.x
            ly_[i] = detection_results[i].lt.y
            rx_[i] = detection_results[i].rb.x
            ry_[i] = detection_results[i].rb.y
            str_lens += len(detection_results[i].result_text) + 1
        str_ = (c_char * str_lens)()
        k = 0
        # link the str in one str,the '$' is the separation sign
        for i in range(0, lens):
            for j in range(0, len(detection_results[i])):
                str_[k] = detection_results[i][j]
                k += 1
            str_[k] = '$'
            k += 1
        ret = self.libc.SendImage_c(height, width, size, data, lx_, ly_, rx_, ry_, str_, str_lens, ch_ptr)
        if ret == -1:
            status = HIAI_ERROR
        return status

    #
    def HandleOriginalImage(self, inference_res):
        status = HIAI_OK
        for ind in range(0, inference_res.b_info.batch_size):
            img_vec = inference_res.img
            width = img_vec[ind].img.width
            height = img_vec[ind].img.height
            size = img_vec[ind].img.size
            detection_results = []
            ret = self.SendImage(height, width, size, img_vec[ind].img.data, detection_results)
            if ret == kFdFunFailed:
                status = HIAI_ERROR
                break
        return status

    def HandResults(self, inference_res):
        status = HIAI_OK
        img_vec = inference_res.img
        output_data_vec = inference_res.output_datas
        detection_results = []
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
                one_result = DetectionResult()
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
        return status

    def process(self, data):
        if data.status == False:
            print("will handle original image.")
            return self.HandleOriginalImage(data)
        else:
            return self.HandleResults(data)
