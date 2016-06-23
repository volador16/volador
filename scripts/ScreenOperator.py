# -*- coding: utf-8 -*-
"""
@brief 这个模块封装了界面操作的基本功能，如鼠标按下，发送输入，拖拽等
  他是一个全局单键实例
@author volador16
"""

from Xlib.display import Display
from Xlib import X
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import os

#@brief 这个对象以borg模式封装了键盘、鼠标、屏幕的接口
class DisplayDevice(object):
    _state = {}
    mouse = None
    keyboard = None
    display = None

    def __new__(cls,*args,**kwargs):
        self = object.__new__(cls, *args, **kwargs)
        self.__dict__ = cls._state
        return self

    def __init__(self):
        os.popen('export DISPLAY=:0')
        self.mouse = PyMouse()
        self.keyboard=PyKeyboard()
        self.display = Display()

class ScreenOperator:
    __screen_width=0
    __screen_hight=0
    __disdev=None

    #使用前export DISPLAY=:0
    def __init__(self):
        self.__disdev = DisplayDevice()
        self.__screen_width, self.__screen_hight = self.__disdev.mouse.screen_size()

    #@brief 返回窗口的位置x,y,以及窗口的width,hight; 如果窗口没有找到则抛出异常
    def __find_window(self,winId):
        window = self.__disdev.display.create_resource_object('window',winId)
        #print('find window',window.get_wm_name())
        #将window置在最前端，为后续操作做准备
        window.set_input_focus(X.RevertToParent, X.CurrentTime)
        window.configure(stack_mode=X.Above)
        #获取window的位置，size
        gp = window.query_tree().parent.query_tree().parent
        ge = gp.get_geometry()._data
        return ge['x'],ge['y'],ge['width'],ge['height']

    #对指定窗口内的x,y发送鼠标单机操作,默认是鼠标左键button=1; 鼠标右键为2; 中间键为3;
    def click(self,windowID,x,y,button=1):
        wx,wy,ww,wh = self.__find_window(windowID)
        #print "wx=%d, wy=%d, ww=%d, wh=%d" % (wx,wy,ww,wh)
        #check x,y 数据是否是界面内
        #发送点击
        self.__disdev.mouse.click(wx+x,wy+y,button)

    #鼠标的拖拉操作，模拟iOS设备的滑动从fx,fy拖拽到tx,ty
    def drag(self,windowID,fx,fy,tx,ty):
        wx,wy,ww,wh = self.__find_window(windowID)
        #print "wx=%d, wy=%d, fx=%d, fy=%d, tx=%d, ty=%d" % (wx, wy, fx,fy,tx,ty)
        #check fx,fy,tx,ty 数据是否是界面内
        #move mouse and drag
        self.__disdev.mouse.move(wx+fx,wy+fy)
        self.__disdev.mouse.drag(wx+tx,wy+ty)

    #在指定的位置输入文字内容
    def inputText(self,windowID,x,y,txt):
        self.click(windowID,x,y)
        self.__disdev.keyboard.type_string(txt)

    def get_window_size(self,winId):
        wx,wy,ww,wh = self.__find_window(winId)
        return ww,wh

