# -*- coding: utf-8 -*-
"""
这个工具方便定义配置文件时检查截取的区域是否合适
还能够打印出ocr的结果
@author: volader
@usage
   python roi_tool.py imgfile h1 h2 w1 w2 {-ocr}
"""

import cv2
import sys
sys.path.append('/home/admin/volador/scripts')
from Tesseract import Tesseract

if len(sys.argv) != 6 and len(sys.argv) != 7:
    print "usage python roi_tool.py imgfile h1 h2 w1 w2 {-ocr}"
    print "check input!"
    exit()
#print sys.argv
imgfile = sys.argv[1]
img = cv2.imread(imgfile,0)
roi = img[int(sys.argv[2]):int(sys.argv[3]),int(sys.argv[4]):int(sys.argv[5])]
#需要识别区域图片文字
if len(sys.argv) == 7:
    tes = Tesseract()
    txt = tes.image2String(roi)
    print("ocr result:",txt)
    print txt
cv2.imshow('ori-img', img)
cv2.imshow('roi', roi)
cv2.waitKey(0)

