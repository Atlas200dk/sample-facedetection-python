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
from multiprocessing import Queue, Lock
from message import *
from abc import ABCMeta, abstractmethod
from hiai import *
import graphconfig as configparser

class EngineThread(threading.Thread):
    def __init__(self, engineObj):
        threading.Thread.__init__(self)
        self.engine = engineObj
        self.msgQueue = engineObj.msgQueue

    def run(self):
        print(self.name,"start...")
        while True:
            dataType = self.msgQueue.msgQueue.get()
            msgData = self.msgQueue.dataQueue.get()
            if msgData == None:
                print("Message ", dataType, " data is None!")
                continue
            self.engine.Process(msgData)
        print(self.name, "finished")

class AppGraph():
    def __init__(self, graphConfigFile):
        print("Start face detect App")
        self.__engineConfigList = configparser.parse_graph_config(graphConfigFile)

    def GetAIConfig(self, name):
        for engine in self.__engineConfigList:
            if engine.engine_name == name:
                return engine
        return None

    def StartupEngines(self, engineList):
        for engine in engineList:
            EngineThread(engine).start()

class AppEngine():
    def __init__(self):
        print("Engine init start")

    def SubscribleMsg(self, msgTypeNameList):
        self.msgQueue = msgCenter.SubscribMsg(msgTypeNameList)

    @abstractmethod
    def Process(self, data):
        pass
