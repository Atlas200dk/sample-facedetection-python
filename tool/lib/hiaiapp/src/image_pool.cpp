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
#include <unistd.h>
#include <string.h>
#include "hiai_app_status.h"
#include "hiai_app_log.h"
#include "image_pool.h"
extern "C" {
ImagePool g_ImagePool[POOL_TYPE_MAX];

void ImagePoolInit(void)
{
	APP_LOG_INFO("Image pool init...");

	for (int i = 0; i < int(POOL_TYPE_MAX); i++)
	{
		memset(g_ImagePool[i].imagePool, 0, sizeof(PoolNode) * POOL_SIZE);
		g_ImagePool[i].usedNum = 0;
	}
}

ImageData* GetIdleImageNode(POOL_TYPE poolType, uint32_t imageSize, uint32_t imageIdx)
{
	int i = 0;
	ImageData* idleImageNode = NULL;

	if (poolType < 0 || poolType >= POOL_TYPE_MAX)
	{
		APP_LOG_ERROR("Get idle image node failed for pool type %s is invalid", poolType);
		return NULL;
	}

	PoolNode* poolList = g_ImagePool[uint32_t(poolType)].imagePool;
	g_ImagePool[poolType].poolMutex.lock();
	for (i = 0; i < POOL_SIZE; i++)
	{
		if (poolList[i].used)
			continue;
		APP_LOG_INFO("Set pool %d node % d used for image %d", poolType, i, imageIdx);
		poolList[i].image.size = imageSize;
		poolList[i].image.id = imageIdx;
		poolList[i].used = 1;
		g_ImagePool[uint32_t(poolType)].usedNum++;
		idleImageNode = &(poolList[i].image);
		break;
	}
	g_ImagePool[poolType].poolMutex.unlock();

	if (i >= POOL_SIZE)
		APP_LOG_INFO("Pool %d is full", poolType);

	return idleImageNode;
}

ImageData* GetImage(POOL_TYPE poolType, uint32_t imageSize, uint32_t imageIdx)
{
	ImageData* image = NULL;

	if (poolType < 0 || poolType >= POOL_TYPE_MAX)
	{
		APP_LOG_ERROR("Get image failed for pool type %s is invalid", poolType);
		return NULL;
	}

	PoolNode* poolList = g_ImagePool[poolType].imagePool;
	for (int i = 0; i < POOL_SIZE; i++)
	{
		if (!poolList[i].used)
			continue;

		if ((poolList[i].image.id == imageIdx) &&
			(poolList[i].image.data != NULL) &&
			(poolList[i].image.size == imageSize))
		{
			image = &(poolList[i].image);
			break;
		}
	}

	return image;
}

int CheckImageData(POOL_TYPE poolType, ImageData& image)
{
	int res = HIAI_APP_OK;
	ImageData* imageCache = GetImage(poolType, image.size, image.id);

	if ((imageCache == NULL) || (imageCache->data != image.data))
		res = HIAI_APP_ERROR;

	return res;
}

void ReleasePoolNode(POOL_TYPE poolType, int imageId)
{
	PoolNode* poolList = g_ImagePool[poolType].imagePool;

	g_ImagePool[poolType].poolMutex.lock();
	for (int i = 0; i < POOL_SIZE; i++)
	{
		if (!poolList[i].used)
		{
			continue;
		}

		if (poolList[i].image.id == imageId)
		{
			APP_LOG_INFO("Release image  pool %d, node %d for imgage %d ", poolType, i, imageId);

			poolList[i].image.id = 0;
			poolList[i].used = 0;
			if (g_ImagePool[poolType].usedNum > 0)
				g_ImagePool[poolType].usedNum--;
			if (poolList[i].image.data != NULL)
			{
				delete [] poolList[i].image.data;
				poolList[i].image.data = NULL;
			}
		}
	}
	g_ImagePool[poolType].poolMutex.unlock();
}

void ReleaseImageDataCache(ImageData& image)
{
	APP_LOG_INFO("Release image %d", image.id);
	image.data = NULL;
	ReleasePoolNode(FRAME_POOL, image.id);
	ReleasePoolNode(RESIZED_IMAGE_POOL, image.id);
	ReleasePoolNode(JPEG_IMAGE_POOL, image.id);
}

int CacheImageData(POOL_TYPE poolType, ImageData& image)
{
	ImageData* imgNode = GetIdleImageNode(poolType, image.size, image.id);

	if (imgNode == NULL)
	{
		APP_LOG_ERROR("Cache image failed, type %d", poolType);
		return HIAI_APP_ERROR;
	}

	imgNode->data = image.data;
	return HIAI_APP_OK;
}

uint32_t GetRemainderPoolNodeNum(POOL_TYPE poolType)
{
	if (poolType < 0 || poolType >= POOL_TYPE_MAX)
	{
		return 0;
	}

	return POOL_SIZE - g_ImagePool[poolType].usedNum;
}

}