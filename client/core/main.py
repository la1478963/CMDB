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
import os,sys

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
# os.environ['SET']='conf.settings'
from CMDB import settings

# 使用requests请求https出现警告，做的设置
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
salt_api = settings.SALT_API

class SaltApi:
    def __init__(self, url):
        self.url = url
        self.username = settings.SALT_USERNAME
        self.password = settings.SALT_PASSWORD
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
        if arg:
            # params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg,'expr_form':'list'}
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg,}
        else:
            params = {'client': 'local', 'fun': method, 'tgt': tgt}
        result = self.get_data(self.url, params)
        return result


class MainClass(object):
    def __init__(self):
        self.salt_api = settings.SALT_API
        self.method = None
        self.params = []
    def _main(self,salt_method,salt_params,salt_client='*',test=False):
        salt = SaltApi(self.salt_api)
        salt_test = 'test.ping'
        if test:
            result1 = salt.salt_command(salt_client, salt_test)
            return result1
        result2 = salt.salt_command(salt_client, salt_method, salt_params)
        return result2
