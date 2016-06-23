# -*- coding: utf-8 -*
#@brief 这个模块封装了redis客户端的操作

import redis
import time
import json

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
        self.__redis.hset(windi,'cur-state',state)
        self.__redis.hset(winid,'up-time',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    #@brief 取得一个window的状态
    def get_dev_status(self,winid):
        sjn = self.__redis.hgetall(winid)
        obj = json.loads(sjn)
        if obj.has_key('cur-app') and obj.has_key('cur-state') and obj.has_key('dev-name'):
            return obj['dev-name'], obj['cur-app'], obj['cur-state']
        print "Can't find window status! id=%s" %winid
        return ()
