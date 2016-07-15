# -*- coding: utf-8 -*-
"""
这个模块负责load 定义配置和执行flow
@author: volader
"""
import os
import json

def delete_comment(jsonfile,result):
    os.system('sed "/^ *\/\//d" '+jsonfile+' >'+result)

def delete_file(f):
    os.system('rm '+f)

#@brief config parse base
class ConfigParser:
    conf={}

    def __init__(self,path,key):
        for f in os.listdir(path):
            tmp = os.path.join(path,f)
            if f[-5:] != '.json':
                continue
            if os.path.isfile(tmp):
                #print "find file [%s]" %tmp
                lst = f.split('-')
                if len(lst) < 2 and key != "MP":
                    continue
                if key == 'UI':
                    if lst[1] == 'work_flow.json': continue
                elif key == 'WF':
                    if lst[1] != 'work_flow.json': continue
                elif key == 'MP':
                    if f != 'app_screen_path.json': continue
                else:
                    print "unknowed parse key %s" %key
                    continue
                jtmp = './'+f+'.tmp'
                delete_comment(tmp,jtmp)
                fl = file(jtmp)
                jsonobj = json.load(fl)
                if key == 'MP':
                    self.conf = jsonobj
                elif key=='WF':
                    self.conf[lst[0]] = jsonobj
                else:
                    self.conf[lst[0]]={}
                    self.conf[lst[0]][lst[1][0:-5]] = jsonobj
                print "load configure json file [%s]" % tmp

#用户界面定义配置
class UIDefinition(ConfigParser):
    def __init__(self,path):
        ConfigParser.__init__(self,path,'UI')

    #取得指定app指定设备的配置
    def get_definition(self,app,dev):
        return self.conf[app][dev]

#任务定义配置
class TaskDefinition(ConfigParser):
    def __init__(self,path):
        ConfigParser.__init__(self,path,'WF')

    def get_flow_map(self,app):
        return self.conf[app]

#界面跳转路径map
class ScreenPath(ConfigParser):
    def __init__(self, path):
        ConfigParser.__init__(self, path, 'MP')

    def get_map(self,app):
        return self.conf[app]