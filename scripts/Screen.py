# -*- coding: utf-8 -*-
"""
#@brief 这个对象封装了一个界面的比较方法，用来确定是那个app的那个界面
@author: volader
"""
import pdb
import re
import cv2
import numpy as np
from Tesseract import Tesseract
from Configures import UIDefinition

#@brief 这个对象封装了一个界面的原始图片，轮廓图片，以及主要轮廓的数据结构，以及主要轮廓的极值点
class ScreenMatcher:
    __ori_img = None
    #界面的title
    __title = ""
    #是那个app的那个界面 ex: dpq.快速普通局.温馨提示
    __name = ""
    test=""

    def __init__(self, filename):
        self.__ori_img = cv2.imread(filename,0)
        self.test = filename

    #确定图片是那个app的那个界面
    def match(self,uidef,tesseract,dev_name):
        #计算图片灰度值,德扑游戏的灰度值较低，微信支付宝的较高
        mean = self.__ori_img.mean()
        if mean > float(150.0):
            if self.wechat_match(uidef,tesseract):
                return self.__name
            if self.alipay_match(uidef,tesseract):
                return self.__name
            if self.root_match(uidef,tesseract):
                return self.__name
            if self.dpq_match(uidef,tesseract,dev_name):
                return self.__name
            if self.dyq_match(uidef,tesseract):
                return self.__name 
        else:
            if self.dpq_match(uidef,tesseract,dev_name):
                return self.__name
            if self.dyq_match(uidef,tesseract):
                return self.__name
            if self.root_match(uidef,tesseract):
                return self.__name
        return "UNKNOWN"

    def root_match(self,uidef,tesseract):
        return False

    def dpq_match(self,uidef,tesseract,dev_name):
        cur_def = uidef.get_definition('dpq_2.2.0',dev_name)
        #先获取多数界面的title区域，做OCR
        title = self.__do_area_ocr(tesseract,cur_def[u'快速牌局']['title_area'])
        #debug
        print "[%s] title=%s" %(self.test,title)
        #cv2.imshow('ori',self.__ori_img)
        #cv2.imshow('title',img)
        #cv2.waitKey(0)
        #遍历dpq所有界面，做title匹配
        for k,v in cur_def.iteritems():
            if v.has_key('title') and self.__do_ocr_res_match(title,v['title'],v['title_match']):
                self.__name = k
                return True
        #如果title没有匹配到，则只剩下login、牌局内界面
        #game UI match
        if self.__do_feature_match(cur_def,'nine-game'):
            self.__name = 'nine-game'
            return True
        if self.__do_feature_match(cur_def,'six-game'):
            self.__name = 'six-game'
            return True
        #login match
        title = self.__do_area_ocr(tesseract,cur_def['login']['title_area'])
        if title == cur_def['login']['title']:
            self.__name = 'login'
            return True

        return False

    def dyq_match(self,uidef,tesseract):
        return False

    def wechat_match(self,uidef,tesseract):
        return False

    def alipay_match(self,uidef,tesseract):
        return False

    #做区域ocr识别
    def __do_area_ocr(self,tesseract,area,ocr_psm = '7'):
        img = self.__ori_img[area[0]:area[1],area[2]:area[3]]
        return tesseract.image2String(img,ocr_psm)

    #做ocr识别结果匹配
    #    ocr_res: 识别的结果
    #    template_def: 模版定义的内容
    #    mode: 匹配的模式{complete_match|regex_match}
    #  reutrn True 匹配
    def __do_ocr_res_match(self,ocr_res,template_def,mode):
        if mode == 'complete_match':
            return ocr_res == template_def
        elif mode == 'regex_match':
            mrt = re.match(template_def,ocr_res)
            if not mrt is None:
                mspan=mrt.span()
                return mspan[0]==0 and mspan[1]==len(ocr_res)
        else:
            print "Unknowned ocr_result match mode! [%s]" %mode
        return False

    #做界面特征匹配
    def __do_feature_match(self,conf,name):
        cpm = conf[name]['recognition_method']
        templateImg = cv2.imread(conf[name]['imgfile'],0)
        area = conf[name]['features_area']
        for a in area:
            img1 = self.__ori_img[a[0]:a[1],a[2]:a[3]]
            img2 = templateImg[a[0]:a[1],a[2]:a[3]]
            if cpm == 'contour_compare':
                if not self.__contour_compare(img1,img2):
                    return False
            elif cpm == 'imgae_similar':
                if not self.__similar_compare(img1,img2):
                    return False
            else:
                print "unknowned match method [%s]" %cpm
                return False

        return len(area) > 0

    #@brief 查找图像中的轮廓，进行轮廓比较，只比较1级轮廓，子轮廓不比较
    def __contour_compare(self,img1,img2):
        #edges1 = cv2.Canny(img1,10,200)
        #edges2 = cv2.Canny(img2,10,200)
        ret1, binary1 = cv2.threshold(img1,127,255,cv2.THRESH_BINARY)
        ret2, binary2 = cv2.threshold(img2,127,255,cv2.THRESH_BINARY)
        cturs1, hier1 = cv2.findContours(binary1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cturs2, hier2 = cv2.findContours(binary2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        if len(cturs1)==0 or len(cturs2)==0:
            return False
        """
        ic1 = cv2.drawContours(img1,cturs1, 0, (255,255,255), 2)
        ic2 = cv2.drawContours(img2,cturs2, 0, (255,255,255), 2)
        cv2.imshow('img1',img1)
        cv2.imshow('img2',img2)
        cv2.waitKey(0)
        """
        ct1, area1, arcl1 = self.__find_main_contour(cturs1)
        ct2, area2, arcl2 = self.__find_main_contour(cturs2)
        ret = cv2.matchShapes(ct1,ct2,1,0.0)
        #轮廓相似
        if ret < 0.02:
            return True
        elif ret < 0.1:
            dea = abs(area1 - area2)
            min_area=0
            if area1 > area2:
                min_area = int(area2/10)
            else:
                min_area = int(area1/10)
            if dea < min_area:
                return True
        return False

    #在一组轮廓中找出面积或边长最大的轮廓
    def __find_main_contour(self,contours):
        max_arcl = 0
        max_area = 0
        idx = -1
        for i in xrange(len(contours)):
            area = cv2.contourArea(contours[i])
            if area > max_area:
                max_area = area
                max_arcl = cv2.arcLength(contours[i],False)
                idx = i
        return contours[idx],max_area,max_arcl

    #@brief 很多比较方法，todo
    def __similar_compare(self,img1,img2):
        return False
