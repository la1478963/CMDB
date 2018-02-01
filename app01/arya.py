from arya.service import v1
from db import models
from django.utils.safestring import mark_safe
# from django.urls import reverse
from django.core.urlresolvers import reverse
from django.conf.urls import url,include
from django.shortcuts import HttpResponse,render,redirect
import json


class CpuConfig(v1.AryaConfig):
    list_display = ['cpuarch','num_cpus','cpu_model']
    # show_add = True
v1.site.register(models.Cpu,CpuConfig)

class MotherboardConfig(v1.AryaConfig):
    list_display = ['sn','manufacturer','pn']
    # show_add = True
v1.site.register(models.Motherboard,MotherboardConfig)

class MemoryConfig(v1.AryaConfig):
    list_display = ['size','width','locator','type']
    # show_add = True
v1.site.register(models.Memory,MemoryConfig)


class DiskConfig(v1.AryaConfig):
    list_display = ['path','size',]
    # show_add = True
v1.site.register(models.Disk,DiskConfig)


class OsarchConfig(v1.AryaConfig):
    list_display = ['sarch',]
    # show_add = True
v1.site.register(models.Osarch,OsarchConfig)


class OsConfig(v1.AryaConfig):
    list_display = ['name',]
    # show_add = True
v1.site.register(models.Os,OsConfig)

class NetworkConfig(v1.AryaConfig):
    list_display = ['ip_address','mac_address']
    # show_add = True
v1.site.register(models.Network,NetworkConfig)


class HostConfig(v1.AryaConfig):
    def detail_view(self,row=None,is_title=None):
        if is_title:
            return '详情'
        app=self.model_class._meta.app_label
        mod=self.model_class._meta.model_name
        _str='arya:%s_%s_detail' %(app,mod)
        url=reverse(viewname=_str,args=(row.id,))
        result='<a href="{0}" class="btn btn-info">查看详情</a>'.format(url)
        return mark_safe(result)

    def gouzi(self):
        #通过 钩子函数 增加可以解析的URL
        return [url('^(\d+)/detail.html/', self.detail, name='%s_%s_detail' % (self.app, self.mod)),]

    def detail(self,req,nid):
        if req.method=='GET':
            obj = models.Host.objects.filter(pk=nid).first()
            # return render(req,'detail.html',locals())
        else:
            hostname=req.POST.get('hostname').strip().lstrip('主机名:')
            from client.bin.run import JG_info
            JG_func = JG_info._begin(no_all_in=hostname)
            print(JG_func)
            return HttpResponse(JG_func)
        return render(req, 'detail.html', locals())

    def cpu(self,row=None,is_title=None):
        if is_title:
            return 'cpu'
        obj=models.Host.objects.filter(pk=row.id).first()
        return obj.cpu.num_cpus
    def mem(self,row=None,is_title=None):
        if is_title:
            return '内存'
        obj=models.Host.objects.filter(pk=row.id).first()
        return obj.mem.size
    def eth1ip(self,row=None,is_title=None):
        if is_title:
            return 'eth1_ip'
        obj=models.Host.objects.filter(pk=row.id).first()
        return obj.eth1_network.ip_address

    def eth0ip(self,row=None,is_title=None):
        if is_title:
            return 'eth0_ip'
        obj=models.Host.objects.filter(pk=row.id).first()
        return obj.eth0_network.ip_address

    def disk(self,row=None,is_title=None):
        if is_title:
            return '磁盘'
        value_list=models.Host.objects.filter(pk=row.id).values('disk__size')
        ret_li=[]
        for value in value_list:
            # print(value)
            ret_li.append(value['disk__size'])
        ret='+'.join(ret_li)
        return ret



    list_display = ['hostname',cpu,mem,disk,eth1ip,eth0ip]

    # search_list = ['hostname__contains',]
    search_list = ['hostname__contains','eth1_network__ip_address__contains','eth0_network__ip_address__contains']

    # show_add=True
v1.site.register(models.Host,HostConfig)




class UserConfig(v1.AryaConfig):
    list_display = ['username','name','job']
    # show_add = True
    search_list = ['username__contains','name__contains','job__contains']
v1.site.register(models.UserInfo,UserConfig)



class BusineConfig(v1.AryaConfig):
    list_display = ['name']
    # show_add = True
v1.site.register(models.Business,BusineConfig)


v1.site.register(models.Purpose,BusineConfig)

v1.site.register(models.Source,BusineConfig)



