# -*- coding: utf-8 -*-

from Tesseract import Tesseract
import cv2
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

template_path='./test_ocr_pic/'

tes = Tesseract()
for f in os.listdir(template_path):
    tmp = os.path.join(template_path,f)
    if os.path.isfile(tmp):
        img = cv2.imread(tmp,0)
        txt = tes.line2String(img)
        print "ocr image file [%s] text='%s'" % (f,txt)
