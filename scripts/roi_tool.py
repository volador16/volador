# -*- coding: utf-8 -*-
"""
这个工具方便定义配置文件时检查截取的区域是否合适
@author: volader
@usage
   python roi_tool.py imgfile h1 h2 w1 w2
"""

import cv2
import sys

if len(sys.argv) != 6:
    print "usage python roi_tool.py imgfile h1 h2 w1 w2"
    print "check input!"
    exit()
print sys.argv
imgfile = sys.argv[1]
img = cv2.imread(imgfile,0)
roi = img[int(sys.argv[2]):int(sys.argv[3]),int(sys.argv[4]):int(sys.argv[5])]

cv2.imshow('ori-img', img)
cv2.imshow('roi', roi)
cv2.waitKey(0)

