# -*- coding: utf-8 -*
#
#usage: python test_redis.py command{add|update|get} winid params
#   test_redis.py add winid dev
#   test_redis.py update winid app state
#   test_redis.py get winid
#

import sys
from RedisClient import RedisClient
import json

def usage():
    print "usage: python test_redis.py command{add|update|get} winid params"
    print "\ttest_redis.py add winid dev"
    print "\ttest_redis.py update winid app state"
    print "\ttest_redis.py get winid"
    exit(-1)

if len(sys.argv) < 3:
    usage()

winid = int(sys.argv[2])
rcli = RedisClient()

if sys.argv[1] == 'add':
    dev = sys.argv[3]
    rcli.add_window(winid,dev)
    print "add window [%x | %s] succeed!" %(winid,dev)
elif sys.argv[1] == 'update':
    app = sys.argv[3]
    state = sys.argv[4]
    rcli.update(winid,app,state)
    print "update window [%x] app=[%s]; state=[%s] succeed!" %(winid,app,state)
elif sys.argv[1] == 'get':
    val = rcli.get_window_status(winid)
    txt =  json.dumps(val).decode('unicode-escape')
    print "window id=%x; %s" %(winid,txt)
else:
    usage()
