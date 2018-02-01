#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from core import main
class SshMain(main.MainClass):
    def _run(self,host='*'):
        self.host=host
        self.method = 'cmd.run'
        self.params = ["ss -tnlp |grep sshd |awk -F ':' '{print $2}'",]
        result=self._main(self.method,self.params,self.host)
        JG=self.play_data(result)
        return JG

    def play_data(self,result_data):
        JG_dic={}
        for host,value in result_data.items():
            if not value:
                # print(host,'is down')
                continue
            port=value.split()[0].strip()
            if host not in JG_dic.keys():
                JG_dic[host]={}
            if 'port' not in JG_dic[host].keys():
                JG_dic[host]['port']={}
            JG_dic[host]['port']=port
        return JG_dic
