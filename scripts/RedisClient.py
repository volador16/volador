# -*- coding: utf-8 -*-
#@brief 这个模块封装了redis客户端的操作

import redis
import time

class RedisClient:
    __redis = None

    def __init__(self,rhost='localhost',rport=6379,rdb=0):
        self.__redis = redis.StrictRedis(host=rhost, port=rport, db=rdb)

    #@brief 添加一个新的window
    def add_window(self,winid,dev):
        keys = self.__redis.hkeys(winid)
        if len(keys) > 0:
            self.__redis.delete(winid)
        self.__redis.hset(winid,'dev-name',dev)
        self.__redis.hset(winid,'up-time',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    #@brief 更新window状态
    def update(self,winid,app,state):
        self.__redis.hset(winid,'cur-app',app)
        self.__redis.hset(winid,'cur-state',state)
        self.__redis.hset(winid,'up-time',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    #@brief 取得一个window的状态,返回是dict
    def get_window_status(self,winid):
        val = self.__redis.hgetall(winid)
        return val

    def get_status(self,winId):
        val = self.__redis.hgetall(winId)
        return (val['dev-name'],val['cur-app'],unicode(val['cur-state'],'utf-8'))
