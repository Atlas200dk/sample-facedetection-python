/**
 * ============================================================================
 *
 * Copyright (C) 2018, Hisilicon Technologies Co., Ltd. All Rights Reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *   1 Redistributions of source code must retain the above copyright notice,
 *     this list of conditions and the following disclaimer.
 *
 *   2 Redistributions in binary form must reproduce the above copyright notice,
 *     this list of conditions and the following disclaimer in the documentation
 *     and/or other materials provided with the distribution.
 *
 *   3 Neither the names of the copyright holders nor the names of the
 *   contributors may be used to endorse or promote products derived from this
 *   software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 * ============================================================================
 */

#include "ascenddk/ascend_ezdvpp/dvpp_utils.h"
#include "ascenddk/ascend_ezdvpp/dvpp_data_type.h"
#include "ascenddk/ascend_ezdvpp/dvpp_process.h"
#include "image_pool.h"
#include "hiai_app_status.h"
#include "hiai_app_log.h"

//#include "face_detection_params.h"
#include <memory>
#include <sys/time.h>
#include <unistd.h>

using ascend::utils::DvppBasicVpcPara;
using ascend::utils::DvppProcess;
using ascend::utils::DvppVpcOutput;


extern "C" {
namespace {

// level for call DVPP
const int32_t kDvppToJpegLevel = 100;

// vpc input image offset
const uint32_t kImagePixelOffsetEven = 1;
const uint32_t kImagePixelOffsetOdd = 2;
}

int ConvertImageToJpeg(ImageData& destImg, ImageData& srcImg)
{  
	ascend::utils::DvppToJpgPara dvppToJpegPara;
	dvppToJpegPara.format = JPGENC_FORMAT_NV12;
	dvppToJpegPara.level = kDvppToJpegLevel;
	dvppToJpegPara.resolution.height = srcImg.height;
	dvppToJpegPara.resolution.width = srcImg.width;
	ascend::utils::DvppProcess dvppToJpeg(dvppToJpegPara);

	// call DVPP
	ascend::utils::DvppOutput dvppOut;
	int32_t ret = dvppToJpeg.DvppOperationProc(reinterpret_cast<char*>(srcImg.data), srcImg.size, &dvppOut);
	if (ret != HIAI_APP_OK) 
	{
		APP_LOG_ERROR("Failed to convert YUV420SP to JPEG, return %d.", ret);
		return ret;
	}
 
	destImg.id = srcImg.id;
	destImg.data = dvppOut.buffer;
	destImg.size = dvppOut.size;

	CacheImageData(JPEG_IMAGE_POOL, destImg);

	return HIAI_APP_OK;
}

int ResizeImage(ImageData& destImg, Resolution& resolution, const ImageData& srcImg, int isAlign)
{
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
	dvppResizeParam.is_input_align = isAlign;

	DvppProcess dvpp_process(dvppResizeParam);
	DvppVpcOutput dvppOut;
	int ret = dvpp_process.DvppBasicVpcProc(srcImg.data, srcImg.size, &dvppOut);
	if (ret != HIAI_APP_OK) 
	{
		APP_LOG_ERROR("Failed to resize image, return %d.", ret);
		return ret;
	}

	destImg.id = srcImg.id;
	destImg.data = dvppOut.buffer;
	destImg.size = dvppOut.size;
	CacheImageData(RESIZED_IMAGE_POOL, destImg);

	return HIAI_APP_OK;
}

}
