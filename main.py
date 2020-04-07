import hiai
from hiai.nn_tensor_lib import DataType
from atlasutil import camera, ai, presenteragent, dvpp_process
import cv2 as cv


def main():
    camera_width = 1280
    camera_height = 720
    presenter_config = './face_detection.conf'
    cap = camera.Camera(id = 0, fps = 20, width = camera_width, height = camera_height , format = camera.CAMERA_IMAGE_FORMAT_YUV420_SP)
    if not cap.IsOpened():
        print("Open camera 0 failed")
        return

    dvpp_handle = dvpp_process.DvppProcess(camera_width, camera_height)

    graph = ai.Graph('./model/face_detection_rgb.om')

    chan = presenteragent.OpenChannel(presenter_config)
    if chan == None:
        print("Open presenter channel failed")
        return

    while True:
        yuv_img = cap.Read()
        orig_image = dvpp_handle.Yuv2Jpeg(yuv_img)
        yuv_img = yuv_img.reshape((1080, 1280))
        img = cv.cvtColor(yuv_img, cv.COLOR_YUV2RGB_I420)
        img = cv.resize(img, (300, 300))
   
        result = graph.Inference(img)
 
        detection_list = ai.SSDPostProcess(result, (camera_height, camera_width), 0.9, ['background', 'face'])
        chan.SendDetectionData(camera_width, camera_height, orig_image.tobytes(), detection_list)

  
if __name__ == "__main__":
    main()