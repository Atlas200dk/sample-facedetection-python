#! /usr/bin/env python
# coding=utf-8

import time
import FaceDetectionInference as inferenceengine
import MindCameraDatasets as datasetengine
import hiai_media.config as configparser
import hiai_media.engineobject as engineobject

msgCenter = engineobject.MsgServer()

class FaceDetectGraph():
    def __init__(self, graphConfigFile):
        print("Start face detect App")
        engineConfigList = configparser.parse_graph_config("Graph.config")
        self.threadList = []
        for engineCfg in engineConfigList:
            if engineCfg[0].engine_name == "Mind_camera_datasets":
                engine = datasetengine.MindCameraDatasets(engineCfg[1])
            elif engineCfg[0].engine_name == "face_detection_inference":
                engine = inferenceengine.FaceDetectInference(engineCfg[1])
            elif engineCfg[0].engine_name == "face_detection_post_process":
                continue
                #engine = postengine.FaceDetectPost(engineCfg[1])
            else:
                return

            msgQueue = msgCenter.SubscribMsg(engine)
            engine.SetupMsgCenter(msgCenter)
            thread = engineobject.MyThread(engine, msgQueue, engineCfg.engine_name)
            self.threadList.append(thread)

    def start(self):
        for thread in self.threadList:
            thread.start()
        data = "start work"
        msgCenter.SendMsg("start", data)


if __name__ == "__main__":
    graph = FaceDetectGraph()
    graph.start()
    while True:
        time.sleep(20)
        break
