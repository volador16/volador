# -*- coding: utf-8 -*
#@brief 该模块封装了执行器，用于执行各种配置中的任务操作

from Configures import TaskDefinition
from RedisClient import RedisClient

#@brief executor 为每一个设备操控窗口开一个thread
class Executor:
    _redis = None
    _task_config = None
    _ui_config = None
    _operator = None

    def __init__(self,taskdef,uidef,redis):
        self._task_config = taskdef
        self._ui_config = uidef
        self._redis = redis
        self._operator = ScreenOperator()

    #@brief 执行task任务, return True,False
    #task dqp:{login|register|get_award|make_game|accept_seat}
    #     wechat:{login|register|add_friend|send_msg|recv_money|transfer-accounts}
    #     alipay:{see wechat}
    # params 也是key－value形式，与配置文件保持一致
    def execute(self,winId,app,task,params={}):
        dev, cur_app, cur_state = self._redis.get_dev_status(winId)
        if cur_app == "":
            print "can't found window by [%x]" %winId
            return "Failed"
        flows = self._findShrtestFlow(app,task,cur_app,cur_state)
        for t in flows:
            k,v = t
            if k == "try-agine":
                return "TryAgine"
            self._exce_task(winId,dev,app,cur_state,t,params)
        return "Succeed"

    #@brief 找到task flow的最优路径
    def _findShortestFlow(self,app,task,cur_app,cur_state):
        flows=[]
        if app != cur_app:
            flows.append(("goto-root","")
            flows.append(("wati-next-screen","root"))
            flows.append("goto-"+app,"")
            flows.append(("wait-app-screen",app))
            flows.append(("try-agine",""))
            return flows
        #如果在同一个app中，寻找到达操作界面的最短路径
        if app == 'dpq':
            flows = self._find_dqp_task_flow(task,cur_state)
        elif app == 'wechat':
            flows = self._find_wechat_task_flow(task,cur_state)
        elif app = 'alipay':
            flows = self._find_alipay_task_flow(task,cur_state)
        else:
            print "Unknowed app task! [%s]" %app
            return None
        return flows

    #dqp:{login|register|get_award|make_game|accept_seat}
    def _find_dqp_task_flow(task,cur_state):
        flows = []
        if task == 'login':
            

    #@brief 执行一个单一的任务
    def _exec_task(self,winId,dev_name,app,cur_state,flow,params):
        key,val = flow
        if key == 'goto-root':
            w,h = self._operator.get_window_size(winId)
            self._operator.click(winId,w/2,h/2,button=2)
            return "Succeed"
        elif key == 'wait-next-screen':
            #尝试3次等待
            for i in range(3):
                cur_app, cur_state = self._redis.get_dev_status(winId)
                if cur_app == app and cur_state == val:
                    return "Succeed"
                sleep(0.2)
            return "Failed"
        elif key == 'wait-app-screen':
            for i in range(3):
                cur_app, cur_state = self._redis.get_dev_status(winId)
                if cur_app == app:
                    return "Succeed"
                sleep(0.2)
            return "Failed"

        opt = self._ui_config[app][dev_name][cur_state]['operates'][key]
        optype = opt['type']
        if optype == 'str_text':
            content = params[val]
            self._operator.inputText(winId,opt['location'][0],opt['location'][1],content)
            return "Succeed"
        elif optype == 'button' or optype == 'menu':
            self._operator.click(winId,opt['location'][0],opt['location'][1])
            return "Succeed"
        elif optype == 'drag':
            self._operator.drag()
            return "Succeed"
        elif optype == 'slider':
        
        elif optype == 'slider-button':
        
        else:
            print "Unknowed operate type! [%s]" %optype
            return "Failed"


