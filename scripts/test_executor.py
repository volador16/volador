# -*- coding: utf-8 -*

from RedisClient import RedisClient
from Configures import UIDefinition,TaskDefinition,ScreenPath
import sys
from Executor import Executor
import json
import pdb

redis_client = RedisClient()
cp = '/Users/JinZuo/works/volador/conf'
path_conf = ScreenPath(cp)
ui_conf = UIDefinition(cp)
task_conf = TaskDefinition(cp)

runer = Executor(path_conf,task_conf,ui_conf,redis_client)
runer.debug(True)

if len(sys.argv) != 5:
    print "usage: python test_exceutor.py winID app task params-file(format to json string)"
    exit(-1)
winId = int(sys.argv[1])
app = sys.argv[2]
task = sys.argv[3]
pfname = sys.argv[4]

fl = file(pfname)
params = json.load(fl)

print "input task name=%s" %task
runer.execute(winId,app,task,params)

