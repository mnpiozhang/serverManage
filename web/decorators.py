#!/usr/bin/env python
# -*- coding:utf-8 -*-
from functools import wraps
from django.shortcuts import redirect
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