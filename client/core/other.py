#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from core import main
class OtherMain(main.MainClass):
    def _run(self,host='*'):
        self.host=host
        self.method = 'grains.item'
        self.params = ["os",'osarch','osrelease','kernel','kernelrelease','uuid','id',]
        result=self._main(self.method,self.params,self.host)
        JG=self.play_data(result)
        return JG

    def play_data(self,result_data):
        JG_dic={}
        for host,value in result_data.items():
            if not value:
                # print(host,'is down')
                continue
            if host not in JG_dic.keys():
                JG_dic[host]={}
            if 'other' not in JG_dic[host].keys():
                JG_dic[host]['other']={}
            JG_dic[host]['other']=value
        return JG_dic
