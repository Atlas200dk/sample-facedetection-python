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

#include <memory>
#include <sys/time.h>
#include <unistd.h>
#include <stdlib.h>

#include "image_pool.h"
extern "C" {
#include "driver/peripheral_api.h"
#include "hiai_app_status.h"
#include "hiai_app_log.h"

unsigned int g_ImageIdx = 1;

int HiaiApp_MediaLibInit(void)
{
	ImagePoolInit();
	return MediaLibInit();
}

int HiaiApp_QueryCameraStatus(int cameraId)
{
	return (int)QueryCameraStatus(cameraId);
}

int HiaiApp_OpenCamera(int cameraId)
{
	return OpenCamera(cameraId);
}

// 设置摄像头参数.
// 设置成功返回1，否则返回0
int HiaiApp_SetCameraProperty(int cameraId, int prop, const void* pInValue)
{
	return SetCameraProperty(cameraId, (enum CameraProperties)prop, pInValue);
}

int HiaiApp_ReadFrameFromCamera(int cameralId, ImageData& image)
{
	uint8_t* data = new uint8_t[image.size];
	int32_t size = image.size;

	while (!GetRemainderPoolNodeNum(FRAME_POOL))
	{
		APP_LOG_INFO("Frame pool is full, wait 0.5s");
		usleep(500 * 1000);
	}

	int ret = ReadFrameFromCamera(cameralId, (void*)data, &size);
	if (!ret)
	{
		delete data;
		return ret;
	}
	image.data = data;
	image.id = g_ImageIdx;
	image.size = (uint32_t)size;

	CacheImageData(FRAME_POOL, image);

	g_ImageIdx++;

	return ret;
}

// 关闭摄像头
// 打开成功返回1，否则返回0.
int HiaiApp_CloseCamera(int cameraId)
{
	return CloseCamera(cameraId);
}

}