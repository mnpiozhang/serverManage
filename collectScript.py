#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import os
import sys
import multiprocessing
import platform
import socket
import urllib2
import json
import re
import psutil

#collect server INFO

#hostinfo
def getHostInfo():
    operatingSystem = "-".join(platform.dist())
    machineType = platform.machine()
    systemKernal = platform.release()
    hostname = socket.gethostname()
    #ipAddr = os.popen("ifconfig | grep inet | grep -v 127|grep -v inet6|grep -v 255.255.0.0 |awk '{print $2}'|tr -d 'addr:'|head -1").read()
    baseInfo = {}
    baseInfo['os'] = operatingSystem
    baseInfo['machineType'] = machineType
    baseInfo['systemKernal'] = systemKernal
    baseInfo['hostname'] = hostname
    baseInfo['ispublish'] = "1"
    #baseInfo['ipaddress'] = ipAddr.strip("\n")
    return baseInfo

#print getBaseInfo()

dmiInfo = os.popen("dmidecode").read()

def divide_into_paragraphs(data):
    parsedlist = []
    a = ""
    tmplist = data.splitlines(True)
    for i in tmplist:
        if i.strip():
            a = a + i
        else:
            parsedlist.append(a)
            a=""
    parsedlist.append(a)
    return parsedlist


dmi = divide_into_paragraphs(dmiInfo)

#networkinfo
def getNetworkInfo():
    cmdOutput = os.popen("ip -o addr show").read()
    tmplist = cmdOutput.splitlines(True)
    pattern = re.compile(r"\d+:\s(\w+)\s+inet\s([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s?.*")
    networkinfo = {}
    niclst = []
    addrlst = []
    for line in tmplist:
        ipinfo = re.match(pattern,line.strip())
        if ipinfo:
            nic = ipinfo.groups()[0]
            addr = ipinfo.groups()[1]
            if nic.startswith("lo") or addr.startswith("127.0.0.1"):
                continue
            else:
                niclst.append(nic)
                addrlst.append(addr)
    networkinfo["addrlst"] = addrlst
    return networkinfo

#hardwareinfo
def getHardwareInfo(dmi):
    for i in dmi:
        if "System Information" in i:
            sysinfo = i.strip().split("\n")
            hostinfodic = dict([a.strip().split(": ") for a in sysinfo if ":" in a])
    hardwareinfo = {}
    hardwareinfo['SN'] = hostinfodic['Serial Number']
    hardwareinfo['Manufacturer'] = hostinfodic['Manufacturer']
    hardwareinfo['Product'] = hostinfodic['Product Name']
    hardwareinfo['UUID'] = hostinfodic['UUID']
    #print hostinfo
    return hardwareinfo

#print getHostInfo(dmi)

#cpuinfo
def getCpuInfo():
    cpuModel =  os.popen("cat /proc/cpuinfo  |grep 'model name' |sort | uniq |awk -F\: '{print $2}' |sed 's/^[ \t]*//g'").read()
    cpuPhysical = os.popen("cat /proc/cpuinfo  |grep 'physical id'|sort|uniq |wc -l").read()
    cpuCore = os.popen("cat /proc/cpuinfo  |grep 'core id'|sort |uniq|wc -l").read()
    cpuProcess = multiprocessing.cpu_count()
    cpuInfo = {}
    cpuInfo['cpuModel'] = cpuModel.strip("\n")
    cpuInfo['cpuPhysical'] = cpuPhysical.strip("\n")
    cpuInfo['cpuCore'] = cpuCore.strip("\n")
    cpuInfo['cpuProcess'] = str(cpuProcess).strip("\n")
    return cpuInfo
#print getCpuInfo()

def getMemInfo():
    dmiMemInfo = os.popen("dmidecode -t memory").read()
    memInfo = {}
    for i in divide_into_paragraphs(dmiMemInfo):
        if "Memory Device" in i and not "No Module Installed" in i:
            tmplist = i.strip().split("\n")
            memdic = dict([a.strip().split(": ") for a in tmplist if ":" in a])
            memInfo[memdic['Locator']] = {}
            memInfo[memdic['Locator']]['msn'] = memdic['Serial Number']
            memInfo[memdic['Locator']]['size'] = memdic['Size']
            memInfo[memdic['Locator']]['type'] = memdic['Type']
            memInfo[memdic['Locator']]['speed'] = memdic['Speed']
    return memInfo

#抄来的http://code.activestate.com/recipes/578019/    
#本来用于转换服务器内存等单位用的，现在用不到了    
def bytes2human(n, format='%(value).1f %(symbol)s', symbols='customary'):
    SYMBOLS = {
        'customary'     : ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'),
        'customary_ext' : ('byte', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa',
                           'zetta', 'iotta'),
        'iec'           : ('Bi', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi'),
        'iec_ext'       : ('byte', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi',
                           'zebi', 'yobi'),
    }
    n = int(n)
    if n < 0:
        raise ValueError("n < 0")
    symbols = SYMBOLS[symbols]
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i+1)*10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=symbols[0], value=n)


def getDiskInfo():
    diskInfo = {}
    for i in psutil.disk_partitions():
        mountpoint = i.mountpoint
        device = i.device
        disk_total = bytes2human(psutil.disk_usage(i.mountpoint).total)
        diskInfo[mountpoint] = {}
        diskInfo[mountpoint]['device'] = device
        diskInfo[mountpoint]['total'] = disk_total
    return diskInfo
        



postInfo = {
            'hostinfo':getHostInfo(),
            'hardwareinfo':getHardwareInfo(dmi),
            'cpuinfo':getCpuInfo(),
            'meminfo':getMemInfo(),
            'networkinfo':getNetworkInfo(),
            'diskinfo':getDiskInfo()
            }

url = 'http://192.168.15.125:8000/api/'
headers = {'Content-Type': 'application/json'}
request = urllib2.Request(url=url, headers=headers, data=json.dumps(postInfo))
response = urllib2.urlopen(request)
print  response.read()