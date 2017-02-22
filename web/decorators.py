#!/usr/bin/env python
# -*- coding:utf-8 -*-
from functools import wraps
from django.shortcuts import redirect,HttpResponse
from models import UserInfo
# Create decorators
#登录验证装饰器，失败则跳转至登录页面
def is_login_auth(view_func):
    @wraps(view_func)
    def wrapper(request,*args, **kwargs):
        if  request.session.get('login_auth',False):
            return view_func(request,*args, **kwargs)
        else:
            return redirect('/web/login/')
    return wrapper

#webshell终端连接验证装饰器，非admin用户无法执行
def is_admin_auth(view_func):
    @wraps(view_func)
    def wrapper(request,*args,**kwargs):
        userauth = UserInfo.objects.get(username=request.session.get('username',None)).type.typename
        #print userauth
        #print type(userauth)
        if userauth == "admin":
            return view_func(request,*args, **kwargs)
        else:
            return HttpResponse("usertype is not admin , you have no permission to link remote host")
    return wrapper