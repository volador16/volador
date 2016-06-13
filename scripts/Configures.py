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

#用户界面定义配置
class UIDefinition:
    __definition={}

    #
    def __init__(self,path):
        for f in os.listdir(path):
            tmp = os.path.join(path,f)
            if f[-5:] != '.json':
                continue
            if os.path.isfile(tmp):
                print "find file [%s]" %tmp
                lst = f.split('-')
                if len(lst) < 2 or lst[1] == 'work_flow.json':
                    print "run to here"
                    continue
                jtmp = './'+f+'.tmp'
                delete_comment(tmp,jtmp)
                fl = file(jtmp)
                jsonobj = json.load(fl)
                self.__definition[lst[0]]={}
                self.__definition[lst[0]][lst[1][0:-5]] = jsonobj
                print "load UI definition json file [%s]" % tmp

    #取得指定app指定设备的配置
    def get_definition(self,app,dev):
        return self.__definition[app][dev]

#任务定义配置
class TaskDefinition:
    __def_dict={}

