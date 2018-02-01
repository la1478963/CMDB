#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from core import main
class MotherboardMain(main.MainClass):
    def _run(self,host='*'):
        self.host=host
        self.method = 'cmd.run'
        self.params = ['dmidecode -t1']
        result=self._main(self.method,self.params,self.host)
        JG=self.play_data(result)
        return JG

    def play_data(self,result_data):
        JG_dic={}
        for host,value in result_data.items():
            if host not in JG_dic.keys():
                JG_dic[host]={}
            if 'motherboard' not in JG_dic[host].keys():
                JG_dic[host]['motherboard']={}
            if not value:
                print(host,'主板信息获取失败，请检查dmidecode工具')
                continue
            li=value.split('\n\t')
            for item in li:
                #发行商
                if 'Manufacturer' in item or 'Product Name' in item or 'Serial Number' in item:
                    name,val=item.split(':')
                    JG_dic[host]['motherboard'][name]=val
        return JG_dic
