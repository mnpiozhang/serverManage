#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.db import models
from mongoengine import *  
import datetime
# Create your models here.
# server data

class HostInfo(Document):
    hostname = StringField(max_length=50,unique=True,verbose_name = u'服务器主机名')
    os = StringField(max_length=20,verbose_name = u'操作系统')
    machineType = StringField(max_length=20,verbose_name = u'服务器位数')
    kernal = StringField(max_length=50,verbose_name = u'内核版本')
    timestamp = DateTimeField(default=datetime.datetime.now,verbose_name = u'创建时间')
    changetime = DateTimeField(default=datetime.datetime.now,verbose_name = u'修改时间')
    ispublish = StringField(verbose_name = u'是否发布')
    networkinfo = DictField()
    memoryinfo = DictField()
    hardwareinfo = DictField()
    cpuinfo = DictField()
    diskinfo = DictField()
    usernamessh = StringField(max_length=50,verbose_name = u'服务器登陆名')
    passwordssh = StringField(max_length=50,verbose_name = u'服务器登陆密码')
    addressssh = StringField(max_length=20,verbose_name = u'服务器登陆地址')
    portssh = StringField(max_length=10,verbose_name = u'服务器登陆端口')
    
    
    meta = {
        'ordering': ['-timestamp']
    }
    
#manage user data
class UserInfo(models.Model):
    username = models.CharField(max_length=50,verbose_name = u'用户名')
    password = models.CharField(max_length=50,verbose_name = u'密码')
    type = models.ForeignKey('UserType',verbose_name = u'用户类型')
    realname = models.CharField(max_length=20,verbose_name = u'真实姓名')
    telphone = models.CharField(max_length=12,verbose_name = u'用户电话')
    def __unicode__(self):
        return self.realname
    
class UserType(models.Model):
    typename= models.CharField(max_length=50,verbose_name = u'用户类型名称')
    def __unicode__(self):
        return self.typename