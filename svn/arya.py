from arya.service import v1
from db import models
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

class SvnFuncConfig(v1.AryaConfig):
    def func(self,row=None,is_title=None):
        if is_title:
            return '操作'
        _str='arya:_svn'
        url=reverse(viewname=_str,args=(row.id,))
        result='<a href="{0}" class="btn btn-info">操作</a>'.format(url)
        return mark_safe(result)

    list_display = ['name',func]
v1.site.register(models.SvnFunc,SvnFuncConfig)

class SvnUrlConfig(v1.AryaConfig):
    list_display = ['name']

v1.site.register(models.SvnUrl,SvnUrlConfig)
