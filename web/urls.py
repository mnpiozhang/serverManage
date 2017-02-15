#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""serverManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from views import login,index,logout,details,submit,delhost,batchdelhost,infoshow


urlpatterns = [
    url(r'^login/', login),
    url(r'^logout/', logout),
    url(r'^index/(\d*)', index),
    #url(r'^index/(?P<searchparam>\w*)/(?P<page>\d*)$',index)
    url(r'^details/(?P<id>\w+)/$',details),
    url(r'^submit/',submit),
    url(r'^del/(?P<id>\w+)/$',delhost),
    url(r'^batchdel/',batchdelhost),
    url(r'^infoshow/',infoshow)
]
