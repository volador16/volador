# -*- coding: utf-8 -*-
"""
这个脚本用于测试屏幕图片识别是否正确
@author: volader
"""
from Tesseract import Tesseract
from Configures import UIDefinition
from Screen import ScreenMatcher
import sys
import os

#全局单键实例
tesseract = Tesseract()
#load 配置文件
UIDef = UIDefinition('/home/admin/volador/conf')

def match_screen(imgfile):
    matcher = ScreenMatcher(imgfile)
    ret = matcher.match(UIDef,tesseract,'ipad_mini_retina')
    print "[%s] == <%s>" %(imgfile,ret)

#is sing file
if os.path.isfile(sys.argv[1]):
    match_screen(sys.argv[1])
else:
    for f in os.listdir(sys.argv[1]):
        tmp = os.path.join(sys.argv[1],f)
        if os.path.isfile(tmp):
            match_screen(tmp)
