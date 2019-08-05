import re
from NNTensor import *
import struct
import DataType as datatype
from ctypes import *
#constants
#if you want change the .so please make it
#I put the face_detection_post_process in the sample path and run deploy.sh, and copy .co from facedetectionapp/out
face box color
kFaceBoxColorR = 255        #int8.
kFaceBoxColorG = 190   
kFaceBoxColorB = 0     

# face box border width
kFaceBoxBorderWidth = 2     #int

#face label color
kFaceLabelColorR = 255      #int8.
kFaceLabelColorG = 255
kFaceLabelColorB = 0

#face label font
kFaceLabelFontSize = 0.7    #double
kFaceLabelFontWidth = 2     #int

# face label text prefix
kFaceLabelTextPrefix = 'Face:'
kFaceLabelTextSuffix = '%'
# $$ parameters for drawing box and label end $$

# port number range
kPortMinNumber = 0          #int.
kPortMaxNumber = 65535

# confidence range
kConfidenceMin = 0.0        #doulbe.
kConfidenceMax = 1.0

#face detection function return value
kFdFunSuccess = 0           #int32.
kFdFunFailed = -1

#need to deal results when index is 2
kDealResultIndex = 2        

#each results size
kEachResultSize = 7         

#attribute index
kAttributeIndex = 1         

#score index
kScoreIndex = 2             

#anchor_lt.x index
kAnchorLeftTopAxisIndexX = 3

#anchor_lt.y index
kAnchorLeftTopAxisIndexY = 4

#anchor_rb.x index
 kAnchorRightBottomAxisIndexX = 5

#anchor_rb.y index
kAnchorRightBottomAxisIndexY = 6

#face attribute
kAttributeFaceLabelValue = 1.0#float.
kAttributeFaceDeviation = 0.00001

#percent
kScorePercent = 100         #int32

#IP regular expression
kIpRegularExpression =
    "^((25[0-5]|2[0-4]\\d|[1]{1}\\d{1}\\d{1}|[1-9]{1}\\d{1}|\\d{1})($|(?!\\.$)\\.)){4}$"

#channel name regular expression
kChannelNameRegularExpression = "[a-zA-Z0-9/]+"

HIAI_ERROR = 3 # from cpp value. if you want to it accord with control, please amend it
HIAI_OK = 0

class FaceDetectPostConfig:
    def __init__
        self.confidene = None
        self.presenter_ip = None
        self.present_port = None
        self.channel_name = None


class Point :
    def __init__(self)
        x = None;
        y = None;


class DetectionResult :
    def __init__(self):
        lt = Point();   
        #The coordinate of left top point
        rb = Point();   
        #The coordinate of the right bottom point
        result_text = None;  #Face:xx%

class FaceDetectionPostConfig:
    def __init__(self):
        confidence = None
        presenter_ip = None
        presenter_port = None
        channel_name =None    

class FaceDetectionPostProcess:

    def __init__(self, aiConfig)
        self.fd_post_process_conifg_ = FaceDetedtinPostConfig()
        self.libc = None
        print("Begin initialize!")
        fd_post_process = {}
		#read config
        for item in aiConfig._ai_config_item:
            if item.__name == "Confidence":
                if IsInvalidConfidence(float(item.__value))
                    print("Confidence=%s which configured is invalid.".item.__value)
                    return HIAI_ERROR
                self.fd_post_process_config_.confidence = float(item.__value)
            if item.__name == "PresenterIp":
                if IsInvalidIp(float(item.__value))
                    print("Presenter=%s which configured is invalid.",item.__value)
                    return HIAI_ERROR
                self.fd_post_process_config_.presenter_ip = item.__value      
            if item.__name == "PresenterPort":
                if IsInvalidPPort(float(item.__value))
                    print("PresentPort=%s which configured is invalid.",item.__value)
                    return HIAI_ERROR
                self.fd_port_process_config_.presenter_port = int(item.__value)
            if item.__name == "ChannelName":
                if IsInvalidChannelName(float(item.__value))
                    print("ChannelName=%s which configured is invalid.",item.__value)
                    return HIAI_ERROR
                self.fd_port_process_config_.channel_name = item.__value
	#read config end
	#read .so please set the .so in correct path
	#if you think the transform may is bug, please add the printf in .cpp, make the .so and test it   
        self.libc = LoadLibrary("libface_detection_post_process.so")
        self.libc.openchannel_c.argtypes = [c_char_p,c_int,c_char_p]
        self.libc.openchannel_c.restype = c_void_p
        self.ch_ptr = self.libc.openchannel_c(
                self.fd_post_process_config_.presenter_ip,
                self.fd_post_process_config_.port,
                self.fd.post.process_config_.channel_name)
	#if you think the void ptr is bug, please change .cpp return nullptr to 0 or change in here 
        if self.ch_ptr == 0
            return HIAI_ERROR
        print("End initialize")
        return HIAI_OK
    
    def IsinvalidIp (self, ip)
    #if you think the comparison is bug, please amend the Regular expression or verify in manual
        return !is.match(KIpRegularExpression,ip)

    def IsinvalidPort(self, port)
        return (port <= kPortMinNumber) or (port > KPortMaxNumber)

    def IsinvalidChannelName(self, channel_name)
    #if you think the comparison is bug, please amend the Regular expression or verify in manual
        return !is.match(kChannelNameRegularExpression,channel)

    def IsinvalidConfidence(self, confidence)
        return (condfidence <= KConfidenceMin) or (confidence > KConfidenceMax) 

    def IsInvalidResults(self, attr, score, point_lt, point_rb)
        if (abs(attr - kAttibuteFaceLabelValue) > kAttibuteFaceDevitation)
            return True
        if score < self.fd_post_process_config_.confidence or IsInvalidConfidence(score)
            return True
        if (point_lt.x == point_rb.x) and (point_lt.y == point_rb.y)
            return True
        return False

    def SendImage(self, height, width, size, data, detection_results)
        status = kFdFunSuccess
	#if you think the transform may is bug, please add the printf in .cpp, make the .so and test it   
        libc.SendImage_c.argtypes = [c_int, c_int, c_int, c_ubyte_p, c_int_p, c_int_p, c_int_p, c_int_p, c_char_p, c_int, c_void_p]
        libc.SendImage_c.restypes = c_int
        lens = len(detection_results)
        str_lens = 0;
        lx_ = (c_int * lens)()
        ly_ = (c_int * lens)()
        rx_ = (c_int * lens)()
        ry_ = (c_int * lens)()
        for i in range (0, lens)
            lx[i] = detection_results[i].lt.x
            ly[i] = detection_results[i].lt.y
            rx[i] = detection_results[i].rb.x
            ry[i] = detection_results[i].rb.y
            str_lens += len(detection_result[i].result_text) + 1
        str_ = (c_char * str_lens)()
        k = 0
		#link the str in one str,the '$' is the separation sign  
        for i in range(0, lens)
            for j in range (0, len(detection_results[i]))
                str_[k] = detection_results[i][j]
                k += 1
            str_[k] = '$'
            k += 1
        ret = libc.SendImage_c(height, wigth, size, data, lx, ly, rx, ry, str_, str_kens,ch_ptr)
	if ret == -1
            status = HIAI_ERROR
        return status
	#
    def HandleOriginalImage(self, inference_res)
        status = HIAI_OK
        for ind in range(0, inference_res.b_info.batch_size)
            img_vec = inference_res.img
            width = img_vec[ind].img.width
            height = img_vec[ind].img.height
            size = img_vec[ind].img.size
            detection_results = []
            ret = SendImage(height, width, size, img_vec[ind].img.data, detection_results) 
            if ret == kFdFunFailed 
                status = HIAI_ERROR
                break
        return status

    def HandResults(self,inference_res)
        status HIAI_OK
        img_vec inference_res.img
        output_data_vec = inference_res.output_datas
        detection_result = []
        for ind in range(0,inference_res.b_info.batch_size)  
            out_index = ind * kDealResultIndex
            out = output_data_vec[out_index]
            result_tensor = out
            width = img_vec[ind].img.width
            height = img_vec[ind]img.height
            img_size = img_vec[ind].img.size
            size =int(out.size/4)
            data = out.data
			#get float data from binary data
            frame_str = str(size)+'f'
            result = struct.unpack(frame_str,data)
            k = 0
            while k <size - kEachResultSize
                attr = result[k + kAttributeIndex]
                score = result[k + kScoreIndex]
                one_result = DetectionResult()
                one_result.lt.x = result[kAnchorLeftAxisIndexX] * width
                one_result.lt.y = result[kAnchorLeftAxisIndexY] * height
                one_result.rb.x = result[kAnchorRightBottomIndexX] * width
                one_result.rb.y = result[kAnchorRightBottomIndexY] * height
                if isInvalidResults(attr, score, one_result.lt, one_result.rb)
                    continue
                print ("score=%f, lt.x=%d, lt.y=%d, rb.x=%d rb.y=%d",score,one_result.lt.x, one_result.lt.y, one_result.rb.x, one_result.rb.y)
                score_percent = score * kScorePercent
                one_result.result_text = kFaceLabelTextPrefix + str(score_precent) + kFaceLabelTextSuffix
                detection_results.append(one.result)
                k = k + kEachResultSize 
            ret = SendImage(height, width, img_size, img_vec[ind].img.data, detection_results)
            if ret == kdFunFailed
                status = HIAI_ERROR
        return status
        
    def process (self, data)
        if data.status == False
            print ("will handle original image.")
            return HandleOriginalImage(data)
        else    
            return HandleResults(data)
