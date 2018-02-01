from django.shortcuts import HttpResponse,render,redirect
from django.utils.safestring import mark_safe
# from django.urls import reverse
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from db import models
from django.conf.urls import url,include
from django.db.models import Q
from ..utils.page import Pagination
import copy
from rbac.views import init
from django.conf import settings
from svn.views import svn_mian_func
from clientapi.views import ret_salt_api
from clientapi.views import client_func
from keras.models import load_model

class ChangeList(object):
    def __init__(self,site,queryset):
        self.model_class=site.model_class
        self.get_list_display=site.get_list_display(site.request)
        self.site=site
        self.get_show_add=site.get_show_add(site.request)
        self.get_show_dels=site.get_show_dels(site.request)
        self.add_url=site.add_url
        self.get_search_list=site.get_search_list
        self.get_q=site.request.GET.get('q','')


        par_page=site.par_page
        page_count=site.page_count
        request=site.request
        query_get=copy.deepcopy(request.GET)
        request_page=site.request.GET.get('page','1')
        all_count=queryset.count()
        page_url=site.list_url
        pag_obj=Pagination(request_page,all_count,page_url,query_get,par_page,page_count)
        self.queryset=queryset[pag_obj.start:pag_obj.end]
        self.page_html=pag_obj.page_html()


    def table_head(self):
        result = []
        for item in self.get_list_display:
            if isinstance(item,str):
                temp=self.model_class._meta.get_field(item).verbose_name
            else:
                temp=item(self.site,is_title=True)
            result.append(temp)
        return result


    def table_body(self):
        result=[]
        for obj in self.queryset:
            ret=[]
            for item in self.get_list_display:
                if isinstance(item,str):
                    temp=getattr(obj,item)
                else:
                    try:
                        temp=item(self.site,row=obj)
                    except TypeError:
                        temp=item(row=obj)
                ret.append(temp)
            result.append(ret)
        return result


class AryaConfig(object):
    def __init__(self,model_class,site):
        self.model_class=model_class
        self.app=self.model_class._meta.app_label
        self.mod=self.model_class._meta.model_name
        self.site=site
        # sf_model=load_model('model_v0.314_epoch-07-loss0.0742-valLoss0.1214.hdf5')
        # request.session['model']=sf_model
    _detail=True
    _edit=True
    _add=True
    _del=True
    _dels = True

    list_display=[]
    show_add=False
    show_dels=False
    model_f=False
    search_list=[]
    par_page=10
    page_count=7

    @property
    def urls(self):
        parttents = [
            url('^$', self.list,name='%s_%s_list' %(self.app,self.mod)),
            url('^add.html/', self.add,name='%s_%s_add' %(self.app,self.mod)),
            url('^(\d+)/delete.html/', self.delete,name='%s_%s_del' %(self.app,self.mod)),
            url('^(\d+)/change.html/', self.change,name='%s_%s_edit' %(self.app,self.mod)),
        ]
        parttents+=self.gouzi()
        return parttents,None,None

    def gouzi(self):
        return []

    def get_show_add(self,request):
        if not self._add:
            return self.show_add
        if 'add' in request.permission_code_list:
        # if True:
            self.show_add=True
        return self.show_add

    def get_show_dels(self,request):
        if not self._dels:
            return self.show_dels
        if 'del' in request.permission_code_list:
        # if True:
            self.show_dels=True
        return self.show_dels

    def get_search_list(self):
        result=[]
        result.extend(self.search_list)
        return result

    def get_list_display(self,request):
        result=[]
        result.extend(self.list_display)

        #如果有查看详情权限
        if self._detail:
            if 'det' in request.permission_code_list:
                result.append(self.detail_view)

        # 如果有编辑权限
        # if True:
        if self._edit:
            if 'edit' in request.permission_code_list:
                result.append(AryaConfig.change_view)
        # 如果有删除权限
        # if True:
        if self._del:
            if 'del' in request.permission_code_list:
                result.append(AryaConfig.delete_view)
        result.insert(0,AryaConfig.checkbox_view)
        return result

    def checkbox_view(self,row=None,is_title=None):
        if is_title:
            return ''
        result='<input type="checkbox" value={0}>'.format(row.id)
        return mark_safe(result)

    def change_view(self,row=None,is_title=None):
        if is_title:
            return '修改'
        app=self.model_class._meta.app_label
        mod=self.model_class._meta.model_name
        _str='arya:%s_%s_edit' %(app,mod)
        url=reverse(viewname=_str,args=(row.id,))
        result='<a href="{0}" class="btn btn-warning">修改</a>'.format(url)
        return mark_safe(result)

    def delete_view(self,row=None,is_title=None):
        if is_title:
            return '删除'
        app=self.model_class._meta.app_label
        mod=self.model_class._meta.model_name
        _str='arya:%s_%s_del' %(app,mod)
        url=reverse(viewname=_str,args=(row.id,))
        result='<a href="{0}" class="btn btn-danger">删除</a>'.format(url)
        return mark_safe(result)


    def get_model_form(self):
        if self.model_f:
            return self.model_f
        class Dynamic(ModelForm):
            class Meta:
                model=self.model_class
                fields='__all__'
        return Dynamic


    def list(self,req):
        # left_menu=req.session[settings.PERMISSION_MENU_KEY]
        self.request=req
        search_q=req.GET.get('q')
        candition_q=Q()
        search_list=self.get_search_list()
        if search_list and search_q:
            for search_item in search_list:
                temp_q=Q()
                temp_q.children.append((search_item,search_q))
                candition_q.add(temp_q,'OR')
        queryset=self.model_class.objects.filter(candition_q)
        data=ChangeList(self,queryset)
        return render(req,'list.html',{'data':data,'req':req})
        # return render(req,'list.html',{'data':data,'result':left_menu,'req':req})

    def add(self,req):
        dynamic_form=self.get_model_form()
        if req.method=='GET':
            form=dynamic_form()
            return render(req,'add.html',{'data':form,'req':req})
        else:
            form=dynamic_form(data=req.POST)
            if form.is_valid():
                form.save()
                return redirect(self.list_url)
            return render(req, 'add.html', {'data': form,'req':req})


    def delete(self,req,nid):
        if req.method=='GET':
            return render(req,'del.html',{'req':req})
        else:
            obj=self.model_class.objects.filter(id=nid).delete()
            return redirect(self.list_url)


    def change(self,req,nid):
        dynamic_form = self.get_model_form()
        obj=self.model_class.objects.filter(id=nid).first()
        if req.method=='GET':
            form = dynamic_form(instance=obj)
            return render(req,'edit.html',{'data':form,'req':req})
        else:
            form = dynamic_form(instance=obj,data=req.POST)
            if form.is_valid():
                form.save()
                return redirect(self.list_url)
            return render(req, 'edit.html', {'data': form,'req':req})


    @property
    def list_url(self):
        app=self.model_class._meta.app_label
        mod=self.model_class._meta.model_name
        str='arya:%s_%s_list' %(app,mod)
        result=reverse(viewname=str)
        return result

    @property
    def del_url(self):
        app=self.model_class._meta.app_label
        mod=self.model_class._meta.model_name
        str='arya:%s_%s_del' %(app,mod)
        result=reverse(viewname=str)
        return result

    @property
    def add_url(self):
        app = self.model_class._meta.app_label
        mod = self.model_class._meta.model_name
        str = 'arya:%s_%s_add' % (app, mod)
        result = reverse(viewname=str)
        return result

class AryaSite(object):
    def __init__(self):
        self._registry={}

    def register(self,model_class,model_config):
        self._registry[model_class]=model_config(model_class,self)

    @property
    def urls(self):
        parttents=[
            url('^login/', init.login),
            url('^logout/', init.logout),
            url('^home/', init.home),
            url('^v48_update/', init.v48_update),
            url('^FC/', init.FC),
            url('^QGFX/', init.QGFX),
            url('^GJCCQ/', init.GJCCQ),
            url('^CXBZ/', init.CXBZ),
            url('^(\d+)/svn.html/', svn_mian_func, name='_svn' ),
            url('^client_api.html/', ret_salt_api, name='_saltapi' ),
            url('^client_func.html/', client_func, name='_saltfunc' ),
        ]

        for model_class,model_config in self._registry.items():
            '''
            url("^db/host/" ([],None,None)),
            '''
            JG="^{0}/{1}/".format(model_class._meta.app_label,model_class._meta.model_name)
            pt=url(JG,model_config.urls)
            parttents.append(pt)
        return parttents

site=AryaSite()







