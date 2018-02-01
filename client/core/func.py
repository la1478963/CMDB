#!/usr/bin/python
# -*- coding:utf-8 -*-
#make in LA
from core.cpu import CpuMain
from core.disk import DiskMain
from core.memory import MemMain
from core.network import NetMain
from core.motherboard import MotherboardMain
from core.ssh_port import SshMain
from core.other import OtherMain
import requests


class GetHostInfo(object):
    '''
    程序统一入口：
    通过self._dic 执行各个分支
    '''
    def __init__(self):
        self._dic={
            'cpu':CpuMain,
            'disk':DiskMain,
            'mem':MemMain,
            'network':NetMain,
            'motherboard':MotherboardMain,
            'ssh':SshMain,
            'other':OtherMain
        }
        #此方法由服务端调用
    def _begin(self,no_all_in=False):
        ret_li=[]
        if not no_all_in:
            for key,val in self._dic.items():
                #对象实例化
                Obj=val()
                #执行各自_run方法
                JG = Obj._run()
                ret_li.append(JG)
        else:
            for key,val in self._dic.items():
                #对象实例化
                Obj=val()
                #执行各自_run方法
                JG = Obj._run(no_all_in)
                ret_li.append(JG)
        return self.format(ret_li)

    #数据格式化第二部
    def format(self,ret_li):
        JG_dic = {}
        for item in ret_li:
            for host,value in item.items():
                if host not in JG_dic.keys():
                    JG_dic[host]={}
                JG_dic[host].update(value)
        #向服务端api发送数据
        return self.send_data(JG_dic)

    def send_data(self,send_dic):
        url='http://127.0.0.1:8000/arya/client_api.html/'
        r1=requests.post(url,json=send_dic)
        return r1.text


# AA=GetHostInfo()
# AA._begin()
#cpu
#{'test3': {'num_cpus': 1, 'cpu_model': 'Intel(R) Xeon(R) CPU E5-2650 v2 @ 2.60GHz', 'cpuarch': 'x86_64'}, 'test2': {'num_cpus': 1, 'cpu_model': 'Intel(R) Xeon(R) CPU E5-2650 v2 @ 2.60GHz', 'cpuarch': 'x86_64'}, 'test1': {'num_cpus': 1, 'cpu_model': 'Intel(R) Xeon(R) CPU E5-2650 v2 @ 2.60GHz', 'cpuarch': 'x86_64'}, 'test4': {'num_cpus': 1, 'cpu_model': 'Intel(R) Xeon(R) CPU E5-2650 v2 @ 2.60GHz', 'cpuarch': 'x86_64'}, 'test5': {'num_cpus': 1, 'cpu_model': 'Intel(R) Xeon(R) CPU E5-2650 v2 @ 2.60GHz', 'cpuarch': 'x86_64'}}


#disk
#{'test3': {'/': '39.25G', '/dev/shm': '0.92G'}, 'test1': {'/': '39.25G', '/dev/shm': '0.49G'}, 'test2': {'/': '39.25G', '/dev/shm': '0.49G'}, 'test5': {'/': '39.25G', '/dev/shm': '0.49G'}, 'test4': {'/': '39.25G', '/dev/shm': '0.92G'}}



#内存
#{'test2': {'Set': ' None', 'Bank Locator': ' Not Specified', 'Total Width': ' 64 bits', 'Type Detail': ' None', 'Size': ' 1024 MB', 'Form Factor': ' DIMM', 'Data Width': ' 64 bits', 'Type': ' RAM', 'Locator': ' DIMM 0'}, 'test1': {'Set': ' None', 'Bank Locator': ' Not Specified', 'Total Width': ' 64 bits', 'Type Detail': ' None', 'Size': ' 1024 MB', 'Form Factor': ' DIMM', 'Data Width': ' 64 bits', 'Type': ' RAM', 'Locator': ' DIMM 0'}, 'test4': {'Set': ' None', 'Bank Locator': ' Not Specified', 'Total Width': ' 64 bits', 'Type Detail': ' None', 'Size': ' 2048 MB', 'Form Factor': ' DIMM', 'Data Width': ' 64 bits', 'Type': ' RAM', 'Locator': ' DIMM 0'}, 'test5': {'Set': ' None', 'Bank Locator': ' Not Specified', 'Total Width': ' 64 bits', 'Type Detail': ' None', 'Size': ' 1024 MB', 'Form Factor': ' DIMM', 'Data Width': ' 64 bits', 'Type': ' RAM', 'Locator': ' DIMM 0'}, 'test3': {'Set': ' None', 'Bank Locator': ' Not Specified', 'Total Width': ' 64 bits', 'Type Detail': ' None', 'Size': ' 2048 MB', 'Form Factor': ' DIMM', 'Data Width': ' 64 bits', 'Type': ' RAM', 'Locator': ' DIMM 0'}}


#网卡
# {'test5': {'eth1': ['101.200.219.213', '00:16:3e:08:c1:11'], 'eth0': ['10.44.184.200', '00:16:3e:0a:c3:26']}, 'test1': {'eth1': ['123.57.231.22', '00:16:3e:0a:ba:57'], 'eth0': ['10.51.61.77', '00:16:3e:0a:c0:c6']}, 'test3': {'eth1': ['101.200.219.222', '00:16:3e:0a:c1:7a'], 'eth0': ['10.44.184.244', '00:16:3e:0a:b8:5b']}, 'test2': {'eth1': ['123.57.218.21', '00:16:3e:08:fc:e3'], 'eth0': ['10.44.59.146', '00:16:3e:0a:ba:43']}, 'test4': {'eth1': ['101.200.234.203', '00:16:3e:0a:6d:06'], 'eth0': ['10.44.208.235', '00:16:3e:0a:bd:a5']}}



#主板
#{'test2': {'Manufacturer': ' Xen', 'Serial Number': ' f155ef75-4ea1-454e-9b15-61f27eebf0e0', 'Product Name': ' HVM domU'}, 'test1': {'Manufacturer': ' Xen', 'Serial Number': ' 525e5284-6fa7-4405-8e7d-09b5f2ca8a5e', 'Product Name': ' HVM domU'}, 'test3': {'Manufacturer': ' Xen', 'Serial Number': ' 08dc4ec5-344f-40b3-bdac-55439981389d', 'Product Name': ' HVM domU'}, 'test4': {'Manufacturer': ' Xen', 'Serial Number': ' 87eb9daf-ab1a-4525-9465-8829a4907731', 'Product Name': ' HVM domU'}, 'test5': {'Manufacturer': ' Xen', 'Serial Number': ' 4cb94c93-d8dc-4525-bce7-d3ce421e3600', 'Product Name': ' HVM domU'}}


#ssh端口
#{'test2': '22', 'test1': '22', 'test4': '22', 'test3': '22', 'test5': '22'}



#其他
#{'test5': {'os': 'CentOS', 'kernel': 'Linux', 'osarch': 'x86_64', 'id': 'test5', 'uuid': '4cb94c93-d8dc-4525-bce7-d3ce421e3600', 'kernelrelease': '2.6.32-696.6.3.el6.x86_64', 'osrelease': '6.8'}, 'test4': {'os': 'CentOS', 'kernel': 'Linux', 'osarch': 'x86_64', 'id': 'test4', 'uuid': '87eb9daf-ab1a-4525-9465-8829a4907731', 'kernelrelease': '2.6.32-696.6.3.el6.x86_64', 'osrelease': '6.8'}, 'test1': {'os': 'CentOS', 'kernel': 'Linux', 'osarch': 'x86_64', 'id': 'test1', 'uuid': '525e5284-6fa7-4405-8e7d-09b5f2ca8a5e', 'kernelrelease': '2.6.32-696.6.3.el6.x86_64', 'osrelease': '6.9'}, 'test2': {'os': 'CentOS', 'kernel': 'Linux', 'osarch': 'x86_64', 'id': 'test2', 'uuid': 'f155ef75-4ea1-454e-9b15-61f27eebf0e0', 'kernelrelease': '2.6.32-696.6.3.el6.x86_64', 'osrelease': '6.9'}, 'test3': {'os': 'CentOS', 'kernel': 'Linux', 'osarch': 'x86_64', 'id': 'test3', 'uuid': '08dc4ec5-344f-40b3-bdac-55439981389d', 'kernelrelease': '2.6.32-696.6.3.el6.x86_64', 'osrelease': '6.8'}}
