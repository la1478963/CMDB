#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from core import main
class NetMain(main.MainClass):
    def _run(self,host='*'):
        self.host=host
        self.method = 'grains.item'
        self.params = ['ip_interfaces','hwaddr_interfaces']
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
            if 'network' not in JG_dic[host].keys():
                JG_dic[host]['network']={}

            for ip_mac,val in value.items():
                if ip_mac=='hwaddr_interfaces':
                    cache_dic=val
                else:
                    for eth,ip in val.items():
                        if eth=='lo':
                            continue
                        JG_dic[host]['network'][eth]=ip
            for eth,mac in cache_dic.items():
                if eth=='lo':
                    continue
                JG_dic[host]['network'][eth].append(mac.strip())
        return JG_dic
