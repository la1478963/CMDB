#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from core import main
class MemMain(main.MainClass):
    def _run(self,host='*'):
        self.host=host
        self.method = 'cmd.run'
        self.params = ['dmidecode  -q -t 17 2>/dev/null']
        result=self._main(self.method,self.params,self.host)
        JG=self.play_data(result)
        return JG

    def play_data(self,result_data):
        JG_dic={}
        for host,value in result_data.items():
            if not value:
                print(host,'内存信息获取失败，请检查dmidecode工具')
                continue
            if host not  in JG_dic.keys():
                JG_dic[host]={}
            if 'mem' not in JG_dic[host].keys():
                JG_dic[host]['mem']={}

            li=value.split('\n\t')
            for item in li[1:]:
                k,v=item.split(':')
                JG_dic[host]['mem'][k]=v
        return JG_dic
