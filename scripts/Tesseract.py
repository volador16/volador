# -*- coding: utf-8 -*-
import os
import cv2

class Tesseract:
    __pid=""
    __path=""

    def __init__(self):
        self.__pid = os.getpid()
        self.__path = os.path.expanduser('~')+'/volador/TesseractTemp/'
        os.system('mkdir -p '+self.__path)

    #识别文本, psm 是指图片的文字的排版格式，默认为单行文本
    def image2String(self,img,psm = '7', lang='chi_sim+eng'):
        imgfile=self.__path+str(self.__pid)+'.png'
        retfile=self.__path+str(self.__pid)
        cv2.imwrite(imgfile,img)
        os.popen('tesseract '+imgfile+' '+retfile+' -l '+lang+' -psm '+psm+' >/dev/null 2>&1')
        txt=file(retfile+'.txt').read().strip()
        os.remove(imgfile)
        return txt.decode('utf-8')

"""
#下面这个版本有待深入研究，为赶进度换成上面的版本
import cv2
import numpy as np
from PIL import Image
import pyocr
import pyocr.builders

#@brief 这个对象封装了pyocr文字识别功能
class Tesseract:
    tool = None
    lang = None

    def __init__(self):
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("No OCR tool found")
        #默认只安装tesseract
        self.tool = tools[0]
        print("Will use tool '%s'" % (self.tool.get_name()))
        langs = self.tool.get_available_languages()
        print("Available languages: %s" % ", ".join(langs))
        self.lang = "chi_sim+eng"

    def __str__(self):
        return "tool='%s'\nlangs='%s'" % (self.tool.get_name(),self.langs)

    #@brief 识别图片中的文字,为提高识别率，最佳识别为图片只包含一行文字
    def line2String(self, opencvImg):
        pil_img = Image.fromarray(opencvImg)
        txt = self.tool.image_to_string( pil_img, lang=self.lang, builder=pyocr.builders.TextBuilder() )
        return txt
"""
