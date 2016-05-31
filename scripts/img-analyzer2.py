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

#各个界面的轮廓map， key文件名 value轮廓数组
template_map={}
#
# @brief:该函数找出图片中的轮廓数组，并返回 
def find_screen_contours(img_file):
    orgimg = cv2.imread(img_file)
    edges = cv2.Canny(orgimg,100,200)
    contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours

#
# @brief: 比较两个轮廓，确定是否是同一界面    
def compare_screen(cts1, cts2):
    ret = cv2.matchShapes(cts1,cts2,1,0.0)
    return ret

#1. 首先，要load所有界面的基础模版，用于后续的比较
template_path='/home/admin/volador/pic-templates/iphone4-2.1.12'
for f in os.listdir(template_path):
    tmp = os.path.join(template_path,f)
    if os.path.isfile(tmp):
        try:
            template_map[f] = find_screen_contours(tmp)
        except BaseException:
            print "open image file %s failed!" % tmp

print('load templates succeed!')
#print template_map

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
        ctr = find_screen_contours(imgfile)
        for k,v in template_map.iteritems():
            ret = compare_screen(ctr[0],v[0])
            print "this screen and %s similarity=%f" % (k,ret)
