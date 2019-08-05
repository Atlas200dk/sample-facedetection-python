#! /usr/bin/env python
# coding=utf-8

import hiai_media.image as image

class EngineTransT:
    def __init__(self):
        self.status = 0
        self.msg = None
        self.b_info = None
        self.output_datas = []
        self.imgs = []

class ScaleInfoT:
    def __init__(self):
        self.scale_width = 1
        self.scale_height = 1

class NewImageParaT:
    def __init__(self):
        self.f_info = FrameInfo()
        self.img = image.ImageData()
        self.scale_info = ScaleInfoT()

class FrameInfo:
    def __init__(self):
        self.is_first = False  # 是否为第一个frame
        self.is_last = False  # 是否为最后一个frame
        self.channel_ID = 0  # 处理当前frame的通道ID号
        self.processor_stream_ID = 0  # 处理器计算流ID号
        self.frame_ID = 0  # 图像帧ID号
        self.source_ID = 0  # 图像源ID号
        self.timestamp = 0  # 图像的时间戳


class BatchInfo:
    def __init__(self):
        self.is_first = False
        self.is_last = False
        self.batch_size = 0
        self.max_batch_size = 0
        self.batch_ID = 0
        self.channel_ID = 0
        self.processor_stream_id = 0
        self.frame_ID = []
        self.source_id = []
        self.timestamp = []


class BatchImageParaWithScaleT:
    def __init__(self):
        self.b_info = BatchInfo()
        self.v_img = []


class OutputT:
    def __init__(self):
        self.size = 0
        self.data = None


class EngineTransT:
    def __init__(self):
        self.status = 0
        self.msg = None
        self.b_info = None
        self.output_datas = []
        self.imgs = None
