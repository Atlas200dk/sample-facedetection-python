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

#ifndef HIAI_APP_IMAGE_POOL_H_
#define HIAI_APP_IMAGE_POOL_H_
#include <memory>
#include <mutex>
#include <unistd.h>

extern "C" {

#define POOL_SIZE 30

enum POOL_TYPE
{
	FRAME_POOL = 0,
	RESIZED_IMAGE_POOL,
	JPEG_IMAGE_POOL,
	POOL_TYPE_MAX
};

typedef struct _Resolution
{
	uint32_t width = 0;
	uint32_t height = 0;
}Resolution;

typedef struct _ImageData {
	uint32_t id = 0;
	uint32_t width = 0;       // 图像宽
	uint32_t height = 0;      // 图像高
	uint32_t size = 0;        // 数据大小（Byte）
	uint8_t* data;            // 数据指针
}ImageData;

typedef struct _PoolNode
{
	uint32_t used;
	ImageData image;
}PoolNode;

typedef struct _ImagePool
{
	std::mutex poolMutex;
	uint32_t usedNum;
	PoolNode imagePool[POOL_SIZE];
}ImagePool;


void ImagePoolInit(void);
ImageData* GetIdleImageNode(POOL_TYPE poolType, uint32_t imageSize, uint32_t imageIdx);
int CheckImageData(POOL_TYPE poolType, ImageData& image);
void ReleasePoolNode(POOL_TYPE poolType, int imageId);
int CacheImageData(POOL_TYPE poolType, ImageData& image);
void ReleaseImageDataCache(ImageData& image);
uint32_t GetRemainderPoolNodeNum(POOL_TYPE poolType);
}

#endif /* HIAI_APP_IMAGE_POOL_H_ */
