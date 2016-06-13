# -*- coding: utf-8 -*-
"""
这个脚本用于接收kafka screen topic消息，并对捕获的屏幕进行分析
@author: volader
"""
import cv2
import numpy as np
import os
import json
from kafka import KafkaConsumer
from Tesseract import Tesseract
from Configures import UIDefinition
from Screen import ScreenMatcher

#全局单键实例
tesseract = Tesseract()
#load 配置文件
UIDef = UIDefinition('/home/admin/volador/conf')

#2. 开始接收kafka的消息，对每个文件进行对比处理
consumer = KafkaConsumer('screen')
for msg in consumer:
    print msg
    try:
        json_obj = json.loads(msg.value)
    except BaseException:
        print "json decoding failed! [%s] " % msg.value
    else:
        window_id = json_obj['window_id']
        imgfile = json_obj['file_name']
        matcher = ScreenMatcher(imgfile)
        screen_name = matcher.match(UIDef,tesseract)
