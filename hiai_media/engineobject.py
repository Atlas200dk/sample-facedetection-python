#! /usr/bin/env python
# coding=utf-8
import threading
from multiprocessing import Queue, Lock
import queue as dataqueue
import time
from abc import ABCMeta, abstractmethod


class MsgQueueUnit():
    def __init__(self, msgTypeNameList):
        self.mutex = Lock()
        self.msgTypeList = msgTypeNameList
        self.msgQueue = Queue()
        self.dataQueue = dataqueue.Queue()

class MsgServer():
    def __init__(self):
        self.msgQueueList = []
	self.mutex = Lock()

    def SubscribMsg(self, engine):
        msgQUnit = MsgQueueUnit(engine.subscribMsgList)
        self.msgQueueList.append(msgQUnit)
        return msgQUnit

    def SendMsg(self, msgTypeName, msgData):
        sendRes = 1
        for unit in self.msgQueueList:
            for type in unit.msgTypeList:
                if type == msgTypeName:
                    print("find the queue")
                    unit.msgQueue.put(msgTypeName)

                    self.mutex.acquire()
                    unit.dataQueue.put(msgData)
                    self.mutex.release()

                    sendRes = 0
                    print("put end")
        if sendRes == 1:
            print("Send msg %s failed", msgTypeName)
        return sendRes

class MyThread(threading.Thread):
    def __init__(self, engineObj, msgQueue, name):
        threading.Thread.__init__(self)
        self.engine = engineObj
        self.msgQueue = msgQueue
        self.name = name

    def run(self):
        print("Starting",self.name,"at:",time.time())
        while True:
            print(self.name, " monitor msg recv")
            dataType = self.msgQueue.msgQueue.get()
            print(self.name, "Recv msg ", dataType)
            msgData = self.msgQueue.dataQueue.get()
            self.engine.Process(msgData)
            print(self.name, "process msg end")
        print(self.name, "finish at:", time.time())

class EngineObject():
    def __init__(self):
        print("Engine init start")
        self.SendData = None

    def SetupMsgCenter(self, sendCenter):
        self.sendCenter = sendCenter

    def SendData(self, dataTypeName, data):
        self.sendCenter.SendMsg(dataTypeName, data)

    @abstractmethod
    def Process(self, data):
        pass
