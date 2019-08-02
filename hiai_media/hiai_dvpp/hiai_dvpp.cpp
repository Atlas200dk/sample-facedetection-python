#include "hiaiengine/status.h"
#include "hiaiengine/data_type.h"
#include "hiaiengine/log.h"
#include "hiaiengine/ai_types.h"
#include "hiaiengine/ai_model_parser.h"
#include "hiaiengine/data_type_reg.h"
#include "hiaiengine/engine.h"
#include "hiaiengine/api.h"
#include "hiaiengine/ai_model_manager.h"
#include "hiaiengine/ai_tensor.h"

#include "ascenddk/ascend_ezdvpp/dvpp_data_type.h"
#include "ascenddk/ascend_ezdvpp/dvpp_process.h"

//#include "face_detection_params.h"
#include <memory>

using ascend::utils::DvppBasicVpcPara;
using ascend::utils::DvppProcess;
using ascend::utils::DvppVpcOutput;
using hiai::Engine;
using hiai::IMAGEFORMAT;

namespace {
// output port (engine port begin with 0)
const uint32_t kSendDataPort = 0;

// call dvpp success
const uint32_t kDvppProcSuccess = 0;
// level for call DVPP
const int32_t kDvppToJpegLevel = 100;

// vpc input image offset
const uint32_t kImagePixelOffsetEven = 1;
const uint32_t kImagePixelOffsetOdd = 2;
}


struct ImageData {
	uint32_t format = hiai::YUV420SP; // 图像格式
	uint32_t width  = 0;       // 图像宽
	uint32_t height = 0;      // 图像高
	uint32_t channel = 0;     // 图像通道数
	uint32_t depth = 0;       // 位深
	uint32_t height_step = 0;  // 对齐高度
	uint32_t width_step = 0;  // 对齐宽度
	uint32_t size = 0;        // 数据大小（Byte
	uint8_t*  data;   // 数据指针
};

struct Resolution {
    uint32_t width = 0;
    uint32_t height = 0;
};
    



HIAI_StatusT ConvertImageToJpeg(ImageData& destImg, ImageData& srcImg) 
{  
  // parameter
  ascend::utils::DvppToJpgPara dvpp_to_jpeg_para;
  dvpp_to_jpeg_para.format = JPGENC_FORMAT_NV12;
  dvpp_to_jpeg_para.level = kDvppToJpegLevel;
  dvpp_to_jpeg_para.resolution.height = srcImg.height;
  dvpp_to_jpeg_para.resolution.width = srcImg.width;
  ascend::utils::DvppProcess dvpp_to_jpeg(dvpp_to_jpeg_para);

  // call DVPP
  ascend::utils::DvppOutput dvpp_output;
  int32_t ret = dvpp_to_jpeg.DvppOperationProc(reinterpret_cast<char*>(srcImg.data), srcImg.size, &dvpp_output);

  // failed, no need to send to presenter
  if (ret != kDvppProcSuccess) {
    HIAI_ENGINE_LOG(HIAI_ENGINE_RUN_ARGS_NOT_RIGHT,
                    "Failed to convert YUV420SP to JPEG, skip it.");
    return HIAI_ERROR;
  }

  //reset the data in img_vec
  destImg.data = dvpp_output.buffer;
  destImg.size = dvpp_output.size;

  return HIAI_OK;
}



HIAI_StatusT ResizeImage(ImageData& resizedImg, const ImageData& srcImg, Resolution& resolution) 
{
  if (srcImg.format != IMAGEFORMAT::YUV420SP) {
    // input image must be yuv420sp nv12.
    HIAI_ENGINE_LOG(HIAI_ENGINE_RUN_ARGS_NOT_RIGHT,
                    "[ODInferenceEngine] input image type does not match");
    return HIAI_ERROR;
  }

  // assemble resize param struct
  DvppBasicVpcPara dvppResizeParam;
  dvppResizeParam.input_image_type = INPUT_YUV420_SEMI_PLANNER_UV;
  dvppResizeParam.src_resolution.height = srcImg.height;
  dvppResizeParam.src_resolution.width = srcImg.width;

  // the value of crop_right and crop_left must be odd.
  dvppResizeParam.crop_right =
      srcImg.width % 2 == 0 ? srcImg.width - kImagePixelOffsetEven :
      srcImg.width-kImagePixelOffsetOdd;
  dvppResizeParam.crop_down =
      srcImg.height % 2 == 0 ? srcImg.height - kImagePixelOffsetEven :
      srcImg.height-kImagePixelOffsetOdd;

  dvppResizeParam.dest_resolution.width = resolution.width;
  dvppResizeParam.dest_resolution.height = resolution.height;

  // the input image is aligned in memory.
  dvppResizeParam.is_input_align = true;

  DvppProcess dvpp_process(dvppResizeParam);

  DvppVpcOutput dvppOut;
  int ret = dvpp_process.DvppBasicVpcProc(srcImg.data, srcImg.size, &dvppOut);
  if (ret != kDvppProcSuccess) {
    HIAI_ENGINE_LOG(HIAI_ENGINE_RUN_ARGS_NOT_RIGHT,
                    "call dvpp resize failed with code %d!",ret);
    return HIAI_ERROR;
  }

  // dvpp_out->pbuf
  resizedImg.data = dvppOut.buffer;
  resizedImg.size = dvppOut.size;

  return HIAI_OK;
}

 
