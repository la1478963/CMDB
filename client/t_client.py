#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import requests
import json
try:
    import cookielib
except:
    import http.cookiejar as cookielib
# 使用urllib2请求https出错，做的设置
import ssl
context = ssl._create_unverified_context()

# 使用requests请求https出现警告，做的设置
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
salt_api = "https://101.201.141.232:8001/"
class SaltApi:
    def __init__(self, url):
        self.url = url
        self.username = "saltapi"
        self.password = "123@qwe"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Content-type": "application/json"
        }
        self.params = {'client': 'local', 'fun': '', 'tgt': ''}
        self.login_url = salt_api + "login"
        self.login_params = {'username': self.username, 'password': self.password, 'eauth': 'pam'}
        self.token = self.get_data(self.login_url, self.login_params)['token']
        self.headers['X-Auth-Token'] = self.token

    def get_data(self, url, params):
        send_data = json.dumps(params)
        request = requests.post(url, data=send_data, headers=self.headers, verify=False)
        response = request.json()
        result = dict(response)
        return result['return'][0]

    def salt_command(self, tgt, method, arg=None):
        """远程执行命令，相当于salt 'client1' cmd.run 'free -m'"""
        if arg:
            # params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg,'expr_form':'list'}
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg,}
        else:
            params = {'client': 'local', 'fun': method, 'tgt': tgt}
        # print ('命令参数: ', params)
        result = self.get_data(self.url, params)
        return result

def main():
    # print ('==================')
    # print ('同步执行命令')
    salt = SaltApi(salt_api)
    salt_client = 'test'
    # salt_client = ['*']
    salt_test = 'grains.item'
    salt_method = 'cmd.run'
    # salt_method = 'disk.usage'
    # salt_method = 'svn.update'
    salt_params = ['ip_interfaces','hwaddr_interfaces']
    # salt_params = ['free -m',]
    # salt_params = ['/','/mnt/www','root','liang','liang']
    # print salt.salt_command(salt_client, salt_method, salt_params)
    # 下面只是为了打印结果好看点
    result1 = salt.salt_command(salt_client, salt_test)
    print(result1)
    result2 = salt.salt_command(salt_client, salt_method, salt_params)
    print(result2)

    #disk
    # for host,dic in result2.items():
    #     print (host)
    #
    #     for disk,value in dic.items():
    #         font_size=str(round(int(value['1K-blocks']) /1024 /1024,2)) +('G')
    #         print('目录',disk,'磁盘大小',font_size)
if __name__ == '__main__':
    main()