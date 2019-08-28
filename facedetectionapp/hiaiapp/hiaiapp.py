#! /usr/bin/env python
# -*- coding:utf-8 -*-
#   =======================================================================
#
# Copyright (C) 2018, Hisilicon Technologies Co., Ltd. All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   1 Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#   2 Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#   3 Neither the names of the copyright holders nor the names of the
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#   =======================================================================
#

import threading
import ctypes
from ctypes import *
import os
import sys

HIAI_APP_OK = 0
HIAI_APP_ERROR = -1

def HiaiAppSoPathAndLinkPrepare():
    fileDir = os.path.dirname(os.path.abspath(__file__))

    logDir = fileDir + '/../log'
    if os.path.exists(logDir) == False:
        os.mkdir(logDir)
        if os.path.exists(logDir) == False:
            print("Create dir %s failed, exit"%(logDir))
            sys.exit(0)

    libDir = fileDir + '/lib'
    ldPathEnv = os.environ.get('LD_LIBRARY_PATH')
    if (ldPathEnv == None) or (-1 == ldPathEnv.find(libDir)):
        print("No hiaiapp lib link path setting")
        print("please excute: export LD_LIBRARY_PATH=%s:$LD_LIBRARY_PATH"%(libDir))
        sys.exit(0)

    hiaiAppLibPath = fileDir + '/lib/libhiai_app.so'
    print("hiai app lib: ", hiaiAppLibPath)
    return hiaiAppLibPath

class HiAiApp(object):
    _instance_lock = threading.Lock()
    lib = ctypes.CDLL(HiaiAppSoPathAndLinkPrepare())

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(HiAiApp, "_instance"):
            with HiAiApp._instance_lock:
                if not hasattr(HiAiApp, "_instance"):
                    HiAiApp._instance = object.__new__(cls)
        return HiAiApp._instance

        return hiaiAppLibPath

hiaiApp = HiAiApp.lib

