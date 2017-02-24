#!/usr/bin/env python
# -*- coding:utf-8 -*-
from web.models import HostInfo
import datetime

#处理数据
def solve_request(data):
    try:
        hostname = data['hostinfo']['hostname']
    except Exception,e:
        print e
        return "data is invaild"
        
    if HostInfo.objects(hostname=hostname):
        return _data_update(data)
    else:
        return _data_insert(data)
        
        
#新数据插入
def _data_insert(data):
    try:
        hostInfo = data['hostinfo']
        hardwareInfo = data['hardwareinfo']
        cpuInfo = data['cpuinfo']
        memInfo = data['meminfo']
        networkInfo = data['networkinfo']
        diskInfo = data['diskinfo']
        #print hostInfo
        #插入主机信息
        newhost = HostInfo(
                          hostname = hostInfo['hostname'],
                          machineType = hostInfo['machineType'],
                          os = hostInfo['os'],
                          kernal = hostInfo['systemKernal'],
                          ispublish = hostInfo['ispublish'],
                          networkinfo = networkInfo,
                          memoryinfo = memInfo,
                          hardwareinfo = hardwareInfo,
                          cpuinfo = cpuInfo,
                          diskinfo = diskInfo
                          )
        newhost.save()
        return "insert data ok"
    except Exception,e:
        print e,111
        return "insert error"



#已存在更新
def _data_update(data):
    try:
        hostInfo = data['hostinfo']
        hardwareInfo = data['hardwareinfo']
        cpuInfo = data['cpuinfo']
        memInfo = data['meminfo']
        networkInfo = data['networkinfo']
        diskInfo = data['diskinfo']
        updatehost = HostInfo.objects(hostname=hostInfo['hostname'])

        updatehost.update(
                            os = hostInfo['os'],
                            machineType = hostInfo['machineType'],
                            kernal = hostInfo['systemKernal'],
                            ispublish = hostInfo['ispublish'],
                            networkinfo = networkInfo,
                            memoryinfo = memInfo,
                            hardwareinfo = hardwareInfo,
                            cpuinfo = cpuInfo,
                            diskinfo = diskInfo,
                            changetime = datetime.datetime.now
                          )
        return "update data ok"
    except Exception,e:
        print e,222
        return "update error"
