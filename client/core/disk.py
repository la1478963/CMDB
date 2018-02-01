#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from core import main
class DiskMain(main.MainClass):
    def _run(self,host='*'):
        self.host=host
        self.method = 'disk.usage'
        self.params = ["", ]
        result=self._main(self.method,self.params,self.host)
        JG=self.play_data(result)
        return JG

    def play_data(self,result_data):
        JG_dic={}
        for host,dic in result_data.items():
            if not dic:
                continue
            if host not in JG_dic.keys():
                JG_dic[host]={}
            if 'disk' not in JG_dic[host].keys():
                JG_dic[host]['disk']={}

            for disk,value in dic.items():
                font_size=round(int(value['1K-blocks']) /1024 /1024,2)
                if font_size < 10 :
                    continue
                else:
                    font_size=str(font_size)+'G'
                JG_dic[host]['disk'][disk]=font_size
        # print(JG_dic)
        return JG_dic