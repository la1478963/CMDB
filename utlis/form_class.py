from django.forms import Form
from django.forms import fields
from django.forms import widgets
from db import models
from django.core.exceptions import ValidationError
class LoginForm(Form):
    username=fields.CharField(
        max_length=15,
        min_length=2,
        required=True,
        error_messages={'required':'用户名不能为空','invalid':'输入不合规'},
        # widget = widgets.TextInput(attrs={'class': 'form-control loon luser'})
        widget = widgets.TextInput(attrs={'class': 'form-control loon luser','value':'用户名'})
    )
    password = fields.CharField(
        required=True,
        max_length=32,
        min_length=2,
        error_messages={'required': '密码不能为空', 'invalid': '输入不合规'},
        widget=widgets.TextInput(attrs={'class': 'form-control loon lpass', 'value': '密码'})
    )

class RegisterForm(Form):
    # user_id=fields.IntegerField()
    username=fields.CharField(
        max_length=12,
        min_length=2,
        required=True,
        error_messages={'required':'用户名不能为空','invalid':'输入不合规'},
        widget = widgets.TextInput(attrs={'class': 'form-control loon luser','value':'用户名'})
    )
    password = fields.CharField(
        required=True,
        max_length=32,
        min_length=2,
        error_messages={'required': '密码不能为空', 'invalid': '输入不合规'},
        widget=widgets.TextInput(attrs={'class': 'form-control loon lpass', 'value': '密码'})
    )
    password_confum = fields.CharField(
        required=True,
        max_length=32,
        min_length=2,
        error_messages={'required': '密码不能为空', 'invalid': '输入不合规'},
        widget=widgets.TextInput(attrs={'class': 'form-control loon lpass', 'value': '确认密码'})
    )
    def clean(self):
        if self.cleaned_data['password'] == self.cleaned_data['password_confum']:
            return self.cleaned_data
        else:
            self.add_error('password_confum',ValidationError('密码不一致'))
            return self.cleaned_data


class NewForm(Form):
    id=fields.IntegerField()

    url=fields.URLField(
        # required==True,
        error_messages={'required': '不能为空'},
        widget=widgets.TextInput(attrs={'class': 'form-control','id':'Url'})
    )
    title=fields.CharField(
        required=True,
        error_messages={'required':'不能为空'},
        widget=widgets.TextInput(attrs={'class': 'form-controls','id':'title'})
    )
    summary=fields.CharField(
        required=True,
        max_length=2048,
        error_messages={'required': '不能为空','invalid':'输入不合规'},
        widget=widgets.TextInput(attrs={'class': 'form-control','id':'summary'})
    )

    like_count=fields.IntegerField(
        required=True,
        error_messages={'required': '不能为空','invalid':'输入不合规'},
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )

    img=fields.CharField(
        required=True,
        error_messages={'required': '不能为空', 'invalid': '输入不合规'},
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )

    news_id=fields.ChoiceField(
        choices=[],
        widget=widgets.Select(attrs={'class': 'form-control'})
    )
    user_id=fields.ChoiceField(
        choices=[],
        widget=widgets.Select(attrs={'class': 'form-control'})
    )
    def __init__(self,*args,**kwargs):
        super(NewForm,self).__init__(*args,**kwargs)
        self.fields['news_id'].choices=models.NewsType.objects.values_list('id','name')
        self.fields['user_id'].choices=models.LoginUser.objects.values_list('id','username')


