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
from Template_define import ScreenTemplates

#全局单键实例
tesseract = Tesseract()
#load 配置文件
configures = ScreenTemplates('/home/admin/volador/conf/feature_define.json')

#@brief 这个对象封装了一个界面的原始图片，轮廓图片，以及主要轮廓的数据结构，以及主要轮廓的极值点
class Screen:
    ori_img = None
    edge_img = None
    main_contours = []
    #extreme_point = []
    #表示是什么界面，例如'快速组局'
    name = []

    def __init__(self, filename):
        self.ori_img = cv2.imread(filename,0)

    #根据配置文件读取特征区域，找出特征轮廓并保存在main_contours中
    def loadFeature(self,locs, arc_min_len=300, area_min=700):
        #
        fteImg = self.ori_img[locs[0]:locs[1],locs[2]:locs[3]]
        #edge_img = cv2.Canny(ori_img,50,200)
        contours, hierarchy = cv2.findContours(fteImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for i in xrange(len(contours)):
            arcl = cv2.arcLength(contours[i],False)
            if arcl > arc_min_len:
                self.main_contours.append(contours[i])
                continue
            area = cv2.contourArea(contours[i])
            if area > area_min:
                self.main_contours.append(contours[i])
                print "contour add by area = %d\n. %r" % (area, contours[i])

    #匹配是属于配置中的哪一个模版
    def matchTemplate(self,conf):
        edge_img = cv2.Canny(ori_img,50,200)
        contours, hierarchy = cv2.findContours(edge_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for i in xrange(len(contours)):
            arcl = cv2.arcLength(contours[i],False)
            if arcl > arc_min_len:
                main_contours.append(contours[i])
                continue
            area = cv2.contourArea(contours[i])
            if area > area_min:
                main_contours.append(contours[i])
                print "contour add by area = %d\n. %r" % (area, contours[i])


#
# @brief: 比较两组轮廓，确定是否是同一界面
#    先比较特征轮廓，区别是主界面还是游戏开局、游戏内界面
#    再根据细节特征，确定是在什么状态内
def compare_screen(main_cts):
    #leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
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
