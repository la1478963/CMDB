from django.shortcuts import render,redirect,HttpResponse
from db import models
import requests
import json
import ssl
import traceback
try:
    import cookielib
except:
    import http.cookiejar as cookielib
def svn_mian_func(req,nid):
    obj=models.SvnFunc.objects.filter(id=nid).first()
    h_li=models.Host.objects.all()
    svn_url_li=models.SvnUrl.objects.all()
    if req.method == 'POST':
        hosts = req.POST.getlist('hosts')
        hosts = ','.join(hosts)
        # print(hosts)
        svn_func = req.POST.get('svn_func')
        svn_url = req.POST.get('svn_url')
        route = req.POST.get('route')
        F1 = Func(hosts, 'svn.' + svn_func, svn_url, route)
        ret = getattr(F1, svn_func)()

    return render(req,'svn.html',locals())
##之后的思路  基于反射 执行其他 方法  checkout  add  commit  update 传递参数


class Func(object):
    def __init__(self,hosts,svn_func,svn_url,route):
        self.hosts=hosts
        #获取是哪个函数调用的自己
        # self.svn_func = 'svn.' + traceback.extract_stack()[-2][2]
        self.svn_func = svn_func
        self.svn_url=svn_url
        self.route=route
        self.salt_api = "https://101.201.141.232:8001/"
        self.params={'client': 'local', 'fun': self.svn_func, 'tgt': self.hosts,'expr_form':'list'}
        self.file_auth='root'
        self.svn_user='zhangyi'

    def update(self):
                                # ['/', '/mnt/www', 'root', 'liang', 'liang']
        self.params['arg']=['/',self.route,self.file_auth,self.svn_user,self.svn_user]
        ret=self.salt()
        return ret
        # return HttpResponse(ret)

    def checkout(self):
                        # ['/','svn://59.110.52.67/sql', '/mnt/www', 'root', 'liang', 'liang']
        self.params['arg'] = ['/', self.svn_url,self.route, self.file_auth, self.svn_user, self.svn_user]
        ret=self.salt()
        return ret
        # return HttpResponse(ret)

    def add(self):
        # ret=self.salt()
        # return ret
        return HttpResponse('add')

    def commit(self):
        # ret=self.salt()
        # return ret
        return HttpResponse('commit')


    def salt(self):
        print('同步执行命令')
                        #"https://101.201.141.232:8001/"
        salt = SaltApi(self.salt_api)
        result1 = salt.salt_command(self.params)
        ret=''
        print(result1)
        for i in result1.keys():
            ret +=i
            ret +=result1[i]
            ret += '\n'
        return ret


class SaltApi:
    """
    定义salt api接口的类
    初始化获得token
    """
    def __init__(self, url):
        self.url = url
        self.username = "saltapi"
        self.password = "123@qwe"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Content-type": "application/json"
        }
        self.params = {'client': 'local', 'fun': '', 'tgt': ''}
        self.login_url = self.url + "login"
        self.login_params = {'username': self.username, 'password': self.password, 'eauth': 'pam'}
        self.token = self.get_data(self.login_url, self.login_params)['token']
        self.headers['X-Auth-Token'] = self.token

    def get_data(self, url, params):
        send_data = json.dumps(params)
        request = requests.post(url, data=send_data, headers=self.headers, verify=False)
        response = request.json()
        result = dict(response)
        return result['return'][0]

    def salt_command(self,params):
        result = self.get_data(self.url, params)
        return result


