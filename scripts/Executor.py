# -*- coding: utf-8 -*-
#@brief 该模块封装了执行器，用于执行各种配置中的任务操作

from Configures import TaskDefinition
from Configures import ScreenPath
from RedisClient import RedisClient
#from ScreenOperator import ScreenOperator
import time
from priodict import shortestPath

#@brief executor 为每一个设备操控窗口开一个thread
class Executor:
    _redis = None
    _task_config = None
    _ui_config = None
    _operator = None
    _path_conf = None
    _is_debug = False

    def __init__(self,path_def,taskdef,uidef,redis):
        self._task_config = taskdef
        self._ui_config = uidef
        self._redis = redis
        #self._operator = ScreenOperator()
        self._path_conf = path_def
        self._is_debug = False

    def debug(self,flag):
        self._is_debug = flag

    def _print_flows(self,flows):
        for a,s,o,v in flows:
            print "app=[%s]; screen=[%s]; operator=[%s]; value=[%s]" %(a,s,o,v)

    #@brief 执行task任务, return Failed, Succeed, TryAgine
    #task dqp:see work_flow.json
    # params 也是key－value形式，与配置文件保持一致
    def execute(self,winId,app,task,params={}):
        if not self._task_config.get_flow_map(app).has_key(task):
            print "app [%s] work flow config not find task=[%s]" %(app,task)
            return "Failed"
        dev, cur_app, cur_state = self._redis.get_status(winId)
        if cur_app == "":
            print "can't found window by [%x]" %winId
            return "Failed"
        flows = self._make_work_flows(app,task,cur_app,cur_state)
        if self._is_debug:
            self._print_flows(flows)

        for a,s,o,v in flows:
            if o == "try-agine":
                return "TryAgine"
            self._exec_task(winId,dev,a,s,o,v,params)
        return "Succeed"

    #return flows[], 其中每一项是touple(app,screen,operator,value)
    def _make_work_flows(self,app,task,cur_app,cur_state):
        flows=[]
        if app != cur_app:
            flows.append((cur_app,cur_state,"goto-root",""))
            flows.append((cur_app,cur_state,"wati-next-screen","root"))
            flows.append(("root","root","goto-"+app,""))
            flows.append(("root","root","wait-app-screen",app))
            flows.append(("","","try-agine",""))
            return flows

        #如果在同一个app中，寻找到达操作界面的最短路径
        work_defs = self._task_config.get_flow_map(app)

        # 找到这个任务最开始的界面是哪一个
        at_scr_name = self._find_final_screen4task(work_defs[task])
        if at_scr_name == '':
            print "不能找到任务所对应的界面,请检查work-flow配置文件! task=[%s] app=[%s]" % (task, app)
            return None
        # 匹配当前的界面与最终界面是否一致,如果不一致则先添加跳转任务
        path_screen = []
        if at_scr_name != cur_state:
            path_screen = shortestPath(self._path_conf.get_map(app),cur_state,at_scr_name)

        for i in range(len(path_screen)-1):
            if not self._task_config.get_flow_map(app).has_key(path_screen[i]):
                print "work flow config has not screen [%s]" %path_screen[i]
                return None
            opts = self._task_config.get_flow_map(app)[path_screen[i]]
            if opts.has_key('goto-'+path_screen[i+1]):
                for it in opts['goto-'+path_screen[i+1]]:
                    flows.append((app,path_screen[i],it['key'],it['value']))
            else:
                print "Screen [%s] has not goto-%s task! please checked!" %(path_screen[i],path_screen[i+1])
                return None

        # 从任务开始界面,添加任务的系列操作
        for it in work_defs[task]:
            screen_name = it['screen']
            dic_opts = it['operates']
            for op in dic_opts:
                flows.append((app,screen_name,op['key'],op['value']))

        return flows

    #找到任务的匹配界面
    def _find_final_screen4task(self,task_conf):
        import json
        #print json.dumps(task_conf).decode('unicode-escape')
        return task_conf[0]['screen']

    #@brief 执行一个单一的任务
    # @winId 对那个窗口
    # @dev 窗口的设备型号, 对应不同的配置文件
    # @app 对那个app进行操作
    # @screen app所在的界面
    # @operator 进行什么操作
    # @aprams txt,slider 控件操作需要的参数, key,value的形式
    def _exec_task(self,winId,dev,app,screen,operator,value,params):
        if self._is_debug:
            if value == '' or (operator == 'wait-next-screen' or operator == 'wait-app-screen'):
                print "{win-id=%x; dev=%s; app=%s; screen=%s; operator=%s; value=%s}" %(winId,dev,app,screen,operator,value)
            else:
                print "{win-id=%x; dev=%s; app=%s; screen=%s; operator=%s; value=%s}" %(winId,dev,app,screen,operator,params[value])
            return True

        if operator == 'goto-root':
            w,h = self._operator.get_window_size(winId)
            self._operator.click(winId,w/2,h/2,button=2)
            return True
        elif operator == 'wait-next-screen':
            #尝试3次等待
            for i in range(3):
                d,cur_app, cur_state = self._redis.get_dev_status(winId)
                if cur_app == app and cur_state == value:
                    return True
                time.sleep(1)
            return False
        elif operator == 'wait-app-screen':
            for i in range(3):
                d,cur_app, cur_state = self._redis.get_dev_status(winId)
                if cur_app == value:
                    return True
                time.sleep(1)
            return False

        #d, cur_app, cur_state = self._redis.get_dev_status(winId)
        #if cur_app != app or cur_state != operator:
        #    print "Error: _exec_task state not match! app=%s; cur_app=%s; screen=%s; cur_screen=%s" %(app,cur_app,screen,cur_state)
        #    return False

        optlist = operator.split('.')
        at_screen = self._ui_config[app][dev][screen]
        for i in range(1,len(optlist)-1):
            at_screen = at_screen[optlist[i]]
        opt = at_screen['operates'][optlist[-1]]
        #这个操作是需要拖动屏幕的
        if opt.has_key('out-screen'):
            dopt = self._ui_config[app][dev][screen][opt['out-screen']]
            #如果已经拖动过屏幕了
            if params.has_key('already-out-screen') and params['already-out-screen'] == dopt:
                return self._widget_opt(winId,operator,opt,params)
            self._widget_opt(winId,operator,dopt,params)
            time.sleep(0.2)
            params['already-out-screen'] = dopt

        return self._widget_opt(winId,operator,opt,value,params)

    def _widget_opt(self,winId,operator,opt,value,params):
        optype = opt['type']
        if optype == 'str_text':
            content = params[value]
            self._operator.inputText(winId,opt['location'][0],opt['location'][1],content)
            return True
        elif optype == 'button' or optype == 'menu':
            self._operator.click(winId,opt['location'][0],opt['location'][1])
            return True
        elif optype == 'drag':
            loc=opt['location']
            self._operator.drag(winId,loc[0],loc[1],loc[2],loc[3])
            return True
        elif optype == 'slider':
            level = params[value]
            distance = opt['distance']
            loc = opt['location']
            self._operator.drag(winId,loc[0],loc[1],loc[0]+level*distance,loc[1])
            return True
        elif optype == 'slider-button':
            level = params[value]
            distance = opt['distance']
            loc = opt['location']
            self._operator.click(winId,loc[0]+level*distance,loc[1])
            return True
        else:
            print "Unknowed operate type! [%s]" %optype
            return False

        return False


