from arya.service import v1
from . import models

class UserConfig(v1.AryaConfig):
    list_display = ['name',]
    # show_add=True
v1.site.register(models.User,UserConfig)

class RoleConfig(v1.AryaConfig):
    list_display = ['title',]
    # show_add=True
v1.site.register(models.Role,RoleConfig)

class PermissionConfig(v1.AryaConfig):
    list_display = ['title','url','menu_gp','code','group']
    # show_add=True
v1.site.register(models.Permission,PermissionConfig)

class GroupConfig(v1.AryaConfig):
    list_display = ['caption',]
    # show_add=True
v1.site.register(models.Group,GroupConfig)

class MenuConfig(v1.AryaConfig):
    list_display = ['title',]
    # show_add=True
v1.site.register(models.Menu,MenuConfig)




