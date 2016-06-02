# -*- coding: utf-8 -*

from ScreenOperator import ScreenOperator
import os
import time

os.system('export DISPLAY=:0')

optr = ScreenOperator()
optr.click(0x3200004,310,600)
#显示主屏幕
optr.click(0x3200004,310,600,2)
time.sleep(1)
#滑动解开主屏幕锁,不知道为啥一定执行两次
optr.drag(0x3200004,75,240,75,700)
optr.drag(0x3200004,75,240,75,700)
#
