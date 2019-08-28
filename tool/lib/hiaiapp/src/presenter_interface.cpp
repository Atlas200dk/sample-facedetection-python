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
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

#include <vector>
#include <sstream>
#include <cmath>
#include <regex>
#include <mutex>
#include <sys/time.h>
#include "presenter_interface.h"
#include "image_pool.h"
#include "hiai_app_log.h"
#include "msg_queue.h"

using namespace ascend::presenter;
using namespace std::__cxx11;

// constants
namespace {

// port number range
const int32_t kPortMinNumber = 0;
const int32_t kPortMaxNumber = 65535;

// IP regular expression
const std::string kIpRegularExpression =
    "^((25[0-5]|2[0-4]\\d|[1]{1}\\d{1}\\d{1}|[1-9]{1}\\d{1}|\\d{1})($|(?!\\.$)\\.)){4}$";

// channel name regular expression
const std::string kChannelNameRegularExpression = "[a-zA-Z0-9/]+";
}

std::vector<ascend::presenter::Channel*> g_ChannelTable;
std::mutex g_OpenChannelMutex;

extern "C" {

class CMsgQueue msgQueue;

int SendFrameMsg(ImageFrameMsg* data)
{
	return msgQueue.SendMsg(data);
}

void* ThreadFunction(void* arg)
{
	ImageFrameMsg* msg = NULL;
	for (;;)
	{
		while (!msgQueue.RecvMsg(&msg))
		{
			SendImageToServer(msg);
			delete msg;
			msg = NULL;
		}
		usleep(1000);
	}

	return NULL;
}


int GetCpuCount()
{
	return (int)sysconf(_SC_NPROCESSORS_ONLN);
}


void CreateSendThread()
{
	int cpu_num = 0;
	static int isInited = 0;

	if (isInited) return;

	cpu_num = GetCpuCount();
	printf("The number of cpu is %d\n", cpu_num);

	pthread_t t1;

	pthread_attr_t attr1;


	pthread_attr_init(&attr1);


	if (0 != pthread_create(&t1, &attr1, ThreadFunction, NULL))
	{
		printf("create thread 1 error\n");
		return;
	}

	cpu_set_t cpu_info;
	CPU_ZERO(&cpu_info);
	CPU_SET(2, &cpu_info);
	if (0 != pthread_setaffinity_np(t1, sizeof(cpu_set_t), &cpu_info))
	{
		printf("set affinity failed");
	}

	isInited = 1;
	printf("create thread ok");
	pthread_detach(t1);
}

int OpenChannelEx(const struct OpenChannelParamC& param)
{
	int channelId = 0;
        
	APP_LOG_INFO("Begin open channel..., port %d, ip %s", param.port, param.host_ip);

	if (IsInValidIp(param.host_ip))
	{
		APP_LOG_ERROR("Open presenter channel failed for ip %s is invalid", param.host_ip);
		return PRESENTER_ERROR(ERROR_CODE_INVALID_IP);
	}

	if (IsInValidPort(param.port))
	{
		APP_LOG_ERROR("Open presenter channel failed for port %s is invalid", param.port);
		return PRESENTER_ERROR(ERROR_CODE_INVALID_PORT);
	}

	if (IsInValidChannelName(param.channel_name))
	{
		APP_LOG_ERROR("Open presenter channel failed for channel %s is invalid", param.channel_name);
		return PRESENTER_ERROR(ERROR_CODE_INVALID_PORT);
	}

	ascend::presenter::OpenChannelParam presenterPara;
	presenterPara.host_ip = param.host_ip;
	presenterPara.port = param.port;
	presenterPara.channel_name = param.channel_name;
	presenterPara.content_type = (ascend::presenter::ContentType)(param.content_type);
        
        APP_LOG_INFO("content type, origin %d, new %d", param.content_type, int(presenterPara.content_type));
	
        Channel* chan = nullptr;
	int err_code = (int)OpenChannel(chan, presenterPara);
	// open channel failed
	if (err_code != (int)PresenterErrorCode::kNone)
	{
		APP_LOG_ERROR("Open presenter channel failed, error code=%d", err_code);
		return PRESENTER_ERROR(err_code);
	}
	g_OpenChannelMutex.lock();
		g_ChannelTable.push_back(chan);
	channelId = g_ChannelTable.size();
	g_OpenChannelMutex.unlock();

	CreateSendThread();

	return channelId;
}

int SendImage(int channel, ImageData& image, struct DetectionResultC* detectionResults, uint32_t size)
{
	APP_LOG_INFO("Send image %d", image.id);

	// parameter
	ImageFrame image_frame_para;
	image_frame_para.format = ImageFormat::kJpeg;
	image_frame_para.width = image.width;
	image_frame_para.height = image.height;
	image_frame_para.size = image.size;
	image_frame_para.data = image.data;

	for (uint32_t i = 0; i < size; i++)
	{
		ascend::presenter::DetectionResult one_result;
		one_result.lt = detectionResults[i].lt;
		one_result.rb = detectionResults[i].rb;
		one_result.result_text = detectionResults[i].result_text;
		image_frame_para.detection_results.emplace_back(one_result);
	}
	
	ImageFrameMsg* msg = new ImageFrameMsg();
	msg->channel = channel;
	msg->frame = image_frame_para;
	msg->srcImage.data = image.data;
	msg->srcImage.id = image.id;
	return SendFrameMsg(msg);
}

int ExhoustTime(struct timeval& start, struct timeval& end)
{
	int sec = end.tv_sec - start.tv_sec;
	int usec = 0;
	int msec = 0;

	if (sec > 0)
		usec = 1000000 - start.tv_usec + end.tv_usec;
	else
		usec = end.tv_usec - start.tv_usec;

	return sec * 1000 + usec / 1000;
}

int SendImageToServer(ImageFrameMsg* msg)
{
	int32_t status = 0;
	struct timeval start, end;

	gettimeofday(&start, NULL);

	ascend::presenter::Channel* chan = GetChannel(msg->channel);
	if (chan == NULL)
	{
		ReleaseImageDataCache(msg->srcImage);
		return PRESENTER_ERROR(ERROR_CODE_CHANNEL_NOEXIST);
	}

	int ret = (int)PresentImage(chan, msg->frame);
	if (ret != int(PresenterErrorCode::kNone))
	{
		APP_LOG_ERROR("Send JPEG image to presenter failed, error code=%d", ret);
		status = PRESENTER_ERROR(ret);
	}

	ReleaseImageDataCache(msg->srcImage);

	gettimeofday(&end, NULL);
	APP_LOG_INFO("send exhoust %d ms\n", ExhoustTime(start, end));

	return status;
}


ascend::presenter::Channel* GetChannel(int channelIdx)
{
        int      idx = channelIdx - 1;
	Channel* chan = NULL;
        
        APP_LOG_INFO("channel num %d, chanid %d, chan table entry 0x%x", g_ChannelTable.size(), channelIdx, g_ChannelTable);

	if (idx < 0 || idx >= g_ChannelTable.size())
	{
		APP_LOG_ERROR("channnel id %d is invalid", channelIdx);
		return NULL;
	}

	chan = g_ChannelTable[idx];
	if (chan == NULL)
	{
		APP_LOG_ERROR("channnel %d is not exist", channelIdx);
		return NULL;
	}

	return chan;
}

bool IsInValidIp(const std::string &ip) 
{
  regex re(kIpRegularExpression);
  smatch sm;
  return !regex_match(ip, sm, re);
}

bool IsInValidPort(int32_t port) 
{
  return (port <= kPortMinNumber) || (port > kPortMaxNumber);
}

bool IsInValidChannelName(const std::string &channel_name) 
{
  regex re(kChannelNameRegularExpression);
  smatch sm;
  return !regex_match(channel_name, sm, re);
}



}
