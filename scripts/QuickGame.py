# -*- coding: utf-8 -*-
"""
这个对象封装了德扑圈quick-game界面的识别与操作
@author: volader
"""
import Template_define
import cv2
import numpy as np
from ScreenOperator import ScreenOperator

class QuickGame(ScreenBase):
    __title_loc=None

    def __init__(self,confobj):
        self.title = confobj['title']
        self.__title_loc = Location(confobj['location'])
        self.__gray_img = imread(confobj['imgfile'],0)
        optrs = confobj['operates']
        for i in xrange(len(optrs)):
            self.operates.append(Operate(optrs[i]))

    #操作我要组局功能--这里是指组建快速局
    def doMakeQuickGame(self,img):
