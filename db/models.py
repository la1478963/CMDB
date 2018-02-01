from django.db import models
from rbac.models import User



#主机相关的表
class Cpu(models.Model):
    cpuarch=models.CharField(max_length=8, blank=True, null=True, verbose_name='CPU位数')
    num_cpus=models.CharField(max_length=4, blank=True, null=True, verbose_name='CPU核心数')
    cpu_model=models.CharField(max_length=64, blank=True, null=True, verbose_name='CPU型号')
    def __str__(self):
        return self.num_cpus
#主板
class Motherboard(models.Model):
    sn = models.CharField(max_length=64, blank=True, null=True, verbose_name='主板sn')
    manufacturer = models.CharField(max_length=16, blank=True, null=True, verbose_name='发行商')
    pn = models.CharField(max_length=64, blank=True, null=True, verbose_name='厂商')
    def __str__(self):
        return self.sn

class Memory(models.Model):
    size=models.CharField(max_length=32, blank=True, null=True, verbose_name='内存/G')
    width=models.CharField(max_length=8, blank=True, null=True, verbose_name='位数')
    locator=models.CharField(max_length=16, blank=True, null=True, verbose_name='插槽')
    type=models.CharField(max_length=16, blank=True, null=True, verbose_name='内存类型')
    def __str__(self):
        return self.size

class Disk(models.Model):
    path = models.CharField(max_length=64, blank=True, null=True, verbose_name='挂载路径')
    size = models.CharField(max_length=16, blank=True, null=True, verbose_name='磁盘大小/G')
    def __str__(self):
        return self.size

class Os(models.Model):
    name=models.CharField(max_length=8, blank=True, null=True, verbose_name='系统名称')
    def __str__(self):
        return self.name

class Osarch(models.Model):
    sarch=models.CharField(max_length=8, blank=True, null=True, verbose_name='位数')
    def __str__(self):
        return self.sarch

class Network(models.Model):
    ip_address=models.CharField(max_length=16, blank=True, null=True, verbose_name='IP地址')
    mac_address=models.CharField(max_length=32, blank=True, null=True, verbose_name='MAC地址')
    def __str__(self):
        return self.ip_address

class UserInfo(models.Model):
    '''用户'''
    auth=models.OneToOneField(to=User,verbose_name='关联',null=True,blank=True)
    username=models.CharField(max_length=16, blank=True, null=True, verbose_name='用户名')
    password=models.CharField(max_length=32, blank=True, null=True, verbose_name='密码')
    name=models.CharField(max_length=8, blank=True, null=True, verbose_name='人名')
    job=models.CharField(max_length=8, blank=True, null=True, verbose_name='职位')
    def __str__(self):
        return self.name

class Host(models.Model):
    '''主机'''
    hostname= models.CharField(max_length=32, blank=True, null=True, verbose_name='服务器主机名')
    login_port= models.CharField(max_length=16, blank=True, null=True, verbose_name='ssh登录端口')
    login_name= models.CharField(max_length=16, default='root', verbose_name='登录用户名')
    login_pwd= models.CharField(max_length=32, blank=True, null=True, verbose_name='登录密码')
    cpu= models.ForeignKey(to='Cpu',blank=True, null=True, verbose_name='CPU')
    motherboard= models.ForeignKey(to='Motherboard',blank=True, null=True, verbose_name='主板')
    mem= models.ForeignKey(to='Memory',blank=True, null=True, verbose_name='MEM/M')
    speed = models.IntegerField(blank=True, null=True, verbose_name='带宽/M')
    disk= models.ManyToManyField(to='Disk', blank=True, null=True, verbose_name='磁盘')
    eth1_network= models.ForeignKey(to='Network', blank=True, null=True, verbose_name='eth1IP',related_name='eth1',)
    eth0_network= models.ForeignKey(to='Network', blank=True, null=True, verbose_name='eth0IP',related_name='eth0')
    uuid= models.CharField(max_length=64, blank=True, null=True, verbose_name='uuid')
    os= models.ForeignKey(to='Os', blank=True, null=True, verbose_name='操作系统') #os+版本号
    osarch= models.ForeignKey(to='Osarch', blank=True, null=True, verbose_name='系统位数')
    kernel= models.CharField(max_length=32, blank=True, null=True, verbose_name='系统内核') #内核+版本号
    busnesses=models.ForeignKey(to='Business',verbose_name='业务线',blank=True, null=True)
    purposes=models.ManyToManyField(to='Purpose',verbose_name='机器用途',blank=True, null=True)
    the_fater=models.ForeignKey(to='Host',blank=True,null=True,verbose_name='宿主机',related_name='fater')
    source=models.ForeignKey(to='Source',blank=True,null=True,verbose_name='来源')
    def __str__(self):
        return self.hostname


class Business(models.Model):
    '''业务线'''
    name = models.CharField(max_length=16, blank=True, null=True, verbose_name='业务线名称')
    def __str__(self):
        return self.name

class Purpose(models.Model):
    '''用途'''
    name=models.CharField(max_length=16,blank=True,null=True,verbose_name='用途名称')
    def __str__(self):
        return self.name


class Source(models.Model):
    '''来源：阿里云、物理机（某机房等）'''
    name=models.CharField(max_length=16,blank=True,null=True,verbose_name='来源')
    def __str__(self):
        return self.name


###2017-12-06  svn
class SvnFunc(models.Model):
    name=models.CharField(max_length=16,blank=True,null=True,verbose_name='动作')

class SvnUrl(models.Model):
    name=models.CharField(max_length=32,blank=True,null=True,verbose_name='Svn地址')
