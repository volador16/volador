# -*- coding: utf-8 -*-
"""
这个脚本根据配置load界面特征模版文件，并在内存中保存
@author: volader
"""
import os
import json

class Location:
    left_x=-1
    left_y=-1
    right_x=-1
    right_y=-1

    def __init__(self,json_node):
        self.left_x = json_node[0]
        self.left_y = json_node[1]
        self.right_x = json_node[2]
        self.right_y = json_node[3]

    def __str__(self):
       return "left_x=%d, left_y=%d, right_x=%d, right_y=%d" %(self.left_x,self.left_y,self.right_x,self.right_y)

class OperatePosition:
    opt_type=""
    name=""
    location=None

    def __init__(self,json_node):
        self.opt_type=json_node['type']
        self.name=json_node['name']
        self.location=Location(json_node['location'])

    def __str__(self):
        return "type=%s, key=%s, location=[%r]" %(self.optype,self.key,self.location)

class ScreenBase:
    title=""
    imgfile=""
    operates=[]
    __gray_img=None

class FeatureConfs:
    json_conf = None

    def __init__(self, conf):
        fl = file(conf)
        self.json_conf = json.load(fl)

    def getConfigure(self,key):
        return self.json_conf[key]
