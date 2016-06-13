# -*- coding: utf-8 -*-
"""
这个脚本用于显示图像文件的轮廓
@author: volader
"""
import cv2
import numpy as np
import sys

if len(sys.argv) != 2:
    print "usage: python show_img_contour.py img-file"
    exit()

orgimg = cv2.imread(sys.argv[1],0)
edges = cv2.Canny(orgimg,50,200)
cv2.imshow('origimg',orgimg)
cv2.imshow('canny',edges)
cv2.waitKey(0)
