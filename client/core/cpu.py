#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from core import main
#继承的方法是封装的salt api的内容
class CpuMain(main.MainClass):
    #被func  _begin方法调用,
    def _run(self,host='*'):
        self.host=host
        self.method = 'grains.item'
        self.params = ["num_cpus", "cpu_model", "cpuarch"]
        result=self._main(self.method,self.params,self.host)
        #基于salt api  salt-stack 拿到返回结果
        #调用格式化第一步
        JG=self.play_data(result)
        return JG
    #格式化第一步
    def play_data(self,result_data):
        JG_dic={}
        for k,v in result_data.items():
            if not v:
                print(k,'CPU信息获取失败')
                continue
            if k not in JG_dic.keys():
                JG_dic[k]={}
            JG_dic[k]['cpu']=v
        return JG_dic
