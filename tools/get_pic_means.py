# -*- coding: utf-8 -*-
"""
这个脚本用于打印某个目录下所有图片或指定某个图片的平均灰度值
    也就是这个图片背景色是深是浅，值越小图片颜色越深
@author: volader
"""
import cv2
import os
import sys

def get_img_mean(imgfile):
    img = cv2.imread(imgfile,0)
    m = img.mean()
    print "[%s] mean=%f" %(imgfile,m)

#is sing file
if os.path.isfile(sys.argv[1]):
    get_img_mean(sys.argv[1])
else:
    for f in os.listdir(sys.argv[1]):
        tmp = os.path.join(sys.argv[1],f)
        if os.path.isfile(tmp):
            get_img_mean(tmp)
