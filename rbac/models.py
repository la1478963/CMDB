from django.db import models
# from db import models as db_models
# from db.models import UserInfo
class Menu(models.Model):
    """
    菜单组
    """
    title = models.CharField(max_length=32)
    class Meta:
        verbose_name_plural = "菜单表"
    def __str__(self):
        return self.title

class Group(models.Model):
    """
    权限组
    """
    caption = models.CharField(verbose_name='组名称',max_length=16)
    menu = models.ForeignKey(verbose_name='所属菜单',to='Menu',default=1)
    class Meta:
        verbose_name_plural = "权限组"
    def __str__(self):
        return self.caption
class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题',max_length=32)
    url = models.CharField(verbose_name="含正则URL",max_length=64)
    menu_gp = models.ForeignKey(verbose_name='默认选中的组内权限ID',to='Permission',null=True,blank=True,related_name='x1')
    code = models.CharField(verbose_name="代码",max_length=16)
    group = models.ForeignKey(verbose_name='所属组',to="Group")
    class Meta:
        verbose_name_plural = "权限表"
    def __str__(self):
        return self.title

class User(models.Model):
    """
    用户表
    """
    # userinfo=models.OneToOneField(to=UserInfo,verbose_name='用户登录',null=True,blank=True)
    name = models.CharField(max_length=32,verbose_name='真实名称')
    roles = models.ManyToManyField(verbose_name='具有的所有角色',to="Role",blank=True)
    class Meta:
        verbose_name_plural = "用户表"
    def __str__(self):
        return self.name

class Role(models.Model):
    """
    角色表
    """
    title = models.CharField(max_length=32)
    permissions = models.ManyToManyField(verbose_name='具有的所有权限',to='Permission',blank=True)
    class Meta:
        verbose_name_plural = "角色表"
    def __str__(self):
        return self.title



