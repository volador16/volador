# -*- coding: utf-8 -*-
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
