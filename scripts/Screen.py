# -*- coding: utf-8 -*-
"""
#@brief 这个对象封装了一个界面的原始图片，轮廓图片，以及主要轮廓的数据结构
@author: volader
"""

import cv2
import numpy as np
from Template_define import ScreenTemplates
from Tesseract import Tesseract
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

#@brief 这个对象封装了一个界面的原始图片，轮廓图片，以及主要轮廓的数据结构，以及主要轮廓的极值点
class Screen:
    ori_img = None
    #edge_img = None
    main_contours = []
    #extreme_point = []
    #表示是什么界面，例如'快速组局'
    title = ""

    def __init__(self, filename):
        self.ori_img = cv2.imread(filename,0)

    #根据配置文件读取特征区域，找出特征轮廓并保存在main_contours中
    def loadFeature(self,locs, arc_min_len=300, area_min=700):
        #
        fteImg = self.ori_img[locs.left_x:locs.left_y,locs.right_x:locs.right_y]
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
    def matchTemplate(self,conf, templates, tessocr):
        #首先尝试用title匹配，这种最准确
        title_img = self.ori_img[30:90,0:-1]
        title = tessocr.line2String(title_img)
        title_list = title.split()
        #str = " "
        #print str.join(title_list)
        for s in title_list:
            if s in conf.templates:
                return s
        #如果界面没有title，则进行牌局界面的特征匹配
        #for k,v in templates.iteritems():
