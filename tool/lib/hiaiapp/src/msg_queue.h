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

#ifndef HIAI_APP_MSG_QUEUE_H_
#define HIAI_APP_MSG_QUEUE_H_

#include <mutex>
#include <unistd.h>
#include "presenter_interface.h"

extern "C" {


class CCycleQueue
{
private:
	uint32_t m_size;
	int32_t m_front;
	int32_t m_rear;
	ImageFrameMsg*  m_data[128];
public:
	CCycleQueue()
		:m_size(128),
		m_front(0),
		m_rear(0)
	{

	}

	~CCycleQueue()
	{

	}

	bool isEmpty()
	{
		return m_front == m_rear;
	}

	bool isFull()
	{
		return m_front == (m_rear + 1) % m_size;
	}

	int32_t push(ImageFrameMsg* ele)
	{
		if (isFull())
		{
			return -1;
		}
		m_data[m_rear] = ele;
		m_rear = (m_rear + 1) % m_size;
		return 0;
	}

	ImageFrameMsg* pop()
	{
		ImageFrameMsg* tmp = m_data[m_front];
		m_front = (m_front + 1) % m_size;
		return tmp;
	}
};

class CMsgQueue
{
public:
	CMsgQueue() :bound(128) {};

	int32_t RecvMsg(ImageFrameMsg** msgBuf)
	{
		if (msgQueue.isEmpty()) return -1;
		queueMutex.lock();
		*msgBuf = msgQueue.pop();
		queueMutex.unlock();

		return 0;
	}

	int32_t SendMsg(ImageFrameMsg* msg)
	{
		int32_t sendOk = 0;

		queueMutex.lock();
		sendOk = msgQueue.push(msg);
		queueMutex.unlock();

		return sendOk;
	}

private:
	int32_t bound;
	std::mutex queueMutex;
	CCycleQueue msgQueue;
};
}
#endif