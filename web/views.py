#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import redirect,HttpResponse,render_to_response
from django.views.decorators.csrf import csrf_exempt
from models import UserInfo,HostInfo
from decorators import is_login_auth
from django.template.context import RequestContext
from django.template.context_processors import csrf
from mongoengine.queryset.visitor import Q
from common  import  Page,page_div,query_page_div,split_form_str
import datetime

# Create your views here.

#登陆
@csrf_exempt
def login(request):
# Create your views here.
    ret = {'status':''}
    if request.method == 'POST':
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        is_not_empty=all([username,password])
        if is_not_empty:
            count = UserInfo.objects.filter(username=username,password=password).count()
            #判断输入用户名密码OK，则跳转到主页面
            if count == 1:
                request.session['username'] = username
                request.session['login_auth'] = True
                return redirect('/web/index/')
            else:
                ret['status']='password error'
        else:
            ret['status']='can not empty'
    return render_to_response('login.html',ret)

#登出
@is_login_auth
def logout(request):
    del request.session['login_auth']
    del request.session['username']
    return redirect("/web/login/")

#主页显示
@is_login_auth
def index(request,page=1):
    ret = {'allServerObj':None,'UserInfoObj':None,'PageInfo':None,'AllCount':None}
    try:
        page = int(page)
    except Exception:
        page = 1
    if request.method == 'GET':
        #查询页面的分页显示
        if request.GET.get('issearch',None):
            searchos = request.GET.get('searchos',None)
            searchhostname = request.GET.get('searchhostname',None)
            searchsn = request.GET.get('searchsn',None)
            searchpublish = request.GET.get('searchpublish',None)
            searchip = request.GET.get('searchip',None)
            tmpstarttime = request.GET.get('searchstarttime',None)
            tmpendtime = request.GET.get('searchendtime',None)
            Qset = {}
            Qset['searchos'] = searchos
            Qset['searchhostname'] = searchhostname
            Qset['searchsn'] = searchsn
            Qset['searchpublish'] = searchpublish
            Qset['searchip'] = searchip
            Qset['tmpstarttime'] = tmpstarttime
            Qset['tmpendtime'] = tmpendtime

            #判断是否输入了开始时间，没输入或输入非法则默认为1970.01.01
            try:
                searchstarttime = datetime.datetime.strptime(tmpstarttime,'%Y-%m-%d')
            except:
                searchstarttime = datetime.datetime(1970, 1, 1)
            #判断是否输入了结束时间或输入非法，没输入或输入非法则默认为现在
            try:
                searchendtime = datetime.datetime.strptime(tmpendtime,'%Y-%m-%d')
            except:
                searchendtime = datetime.datetime.now()
            allServer = HostInfo.objects(Q(os__contains=searchos)
                                         &Q(networkinfo__addrlst__contains=searchip)
                                         &Q(hostname__contains=searchhostname)
                                         &Q(ispublish__contains=searchpublish)
                                         &Q(hardwareinfo__SN__contains=searchsn)
                                         &Q(timestamp__gte=searchstarttime)
                                         &Q(timestamp__lte=searchendtime))
            AllCount = allServer.count()
            ret['AllCount'] = AllCount
            PageObj = Page(AllCount,page,6)
            allServerObj = allServer[PageObj.begin:PageObj.end]
            pageurl = 'index'
            querycondition = request.META.get("QUERY_STRING",None)
            pageinfo = query_page_div(page, PageObj.all_page_count,pageurl,querycondition)
            ret['PageInfo'] = pageinfo
            ret['allServerObj'] = allServerObj
            UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
            ret['UserInfoObj'] = UserInfoObj
            ret['Qset'] = Qset
            return render_to_response('index.html',ret,context_instance=RequestContext(request))
        #正常主页的分页显示
        else:
            allServer = HostInfo.objects.all()
            AllCount = allServer.count()
            ret['AllCount'] = AllCount
            PageObj = Page(AllCount,page,6)
            allServerObj = allServer[PageObj.begin:PageObj.end]
            pageurl = 'index'
            pageinfo = page_div(page, PageObj.all_page_count,pageurl)
            ret['PageInfo'] = pageinfo
            ret['allServerObj'] = allServerObj
            UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
            ret['UserInfoObj'] = UserInfoObj
            return render_to_response('index.html',ret,context_instance=RequestContext(request))
    else:
        return HttpResponse("this is a web page , please use metod GET")

#显示主机咨询详情并可编辑
@is_login_auth
def details(request,id):
    ret = {'HostObj':None,'status':'','id':None,'UserInfoObj':None}
    HostObj = HostInfo.objects.get(id=id)
    if request.method == 'POST':
        try:
            formhostname = request.POST.get('formhostname',None)
            formos = request.POST.get('formos',None)
            formmachinetype = request.POST.get('formmachinetype',None)
            formkernal = request.POST.get('formkernal',None)
            fompublish = request.POST.get('fompublish',None)
            formip = request.POST.getlist('formip[]',None)
            #print formip
            #print type(formip)
            #ssh登陆信息
            formaddressssh = request.POST.get('formaddressssh',None)
            formportssh = request.POST.get('formportssh',None)
            formusernamessh = request.POST.get('formusernamessh',None)
            formpasswordssh = request.POST.get('formpasswordssh',None)
            #处理传进来的内存信息
            formmemlstname = split_form_str(request.body)
            #print formmemlstname
            formmem = {}
            for i in formmemlstname:
                #有了数组名获取post来的数组
                tmpmeminfo = request.POST.getlist(i+"[]",None)
                print tmpmeminfo
                formmem[formmemlstname[i]] = {
                                              "msn":tmpmeminfo[0],
                                              "type":tmpmeminfo[1],
                                              "speed":tmpmeminfo[2],
                                              "size":tmpmeminfo[3]
                                              }
            #print formmem
            formhwsn = request.POST.get('formhwsn',None)
            formhwproduct = request.POST.get('formhwproduct',None)
            formhwuuid = request.POST.get('formhwuuid',None)
            formhwmanu = request.POST.get('formhwmanu',None)
            formcpucore = request.POST.get('formcpucore',None)
            formcpumodel = request.POST.get('formcpumodel',None)
            formcpupyhsical = request.POST.get('formcpupyhsical',None)
            formcpuprocess = request.POST.get('formcpuprocess',None)
            networkInfo = {"addrlst":formip}
            hardwareInfo = {"SN":formhwsn,"Product":formhwproduct,"UUID":formhwuuid,"Manufacturer":formhwmanu}
            cpuInfo = {"cpuCore":formcpucore,"cpuModel":formcpumodel,"cpuPhysical":formcpupyhsical,"cpuProcess":formcpuprocess}
            HostObj.update(
                           hostname = formhostname,
                           os = formos,
                           ispublish = fompublish,
                           machineType = formmachinetype,
                           kernal = formkernal,
                           networkinfo = networkInfo,
                           hardwareinfo = hardwareInfo,
                           cpuinfo = cpuInfo,
                           changetime = datetime.datetime.now,
                           memoryinfo = formmem,
                           usernamessh = formusernamessh,
                           passwordssh = formpasswordssh,
                           addressssh = formaddressssh,
                           portssh = formportssh
                           )
            ret['status'] = '修改成功'
            HostObj = HostInfo.objects.get(id=id)
        except Exception,e:
            ret['status'] = '修改失败'
            print e
            #添加跨站请求伪造的认证
            ret.update(csrf(request))
            return render_to_response(request,'details.html',ret)

    ret['HostObj'] = HostObj
    UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
    ret['UserInfoObj'] = UserInfoObj
    ret['id'] = id
    #添加跨站请求伪造的认证
    ret.update(csrf(request))
    return render_to_response('details.html',ret)


#提交新主机信息
@is_login_auth
def submit(request):
    ret = {'status':'','UserInfoObj':None}
    UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
    ret['UserInfoObj'] = UserInfoObj
    if request.method == 'POST':
        try:
            formhostname = request.POST.get('formhostname',None)
            formos = request.POST.get('formos',None)
            formmachinetype = request.POST.get('formmachinetype',None)
            formkernal = request.POST.get('formkernal',None)
            fompublish = request.POST.get('fompublish',None)
            formip = request.POST.getlist('formip[]',["127.0.0.1"])
            #print formip
            #print type(formip)
            
            #处理传进来的内存信息
            formmemlstname = split_form_str(request.body)
            #print formmemlstname
            formmem = {}
            for i in formmemlstname:
                #有了数组名获取post来的数组
                tmpmeminfo = request.POST.getlist(i+"[]",None)
                print tmpmeminfo
                formmem[formmemlstname[i]] = {
                                              "msn":tmpmeminfo[0],
                                              "type":tmpmeminfo[1],
                                              "speed":tmpmeminfo[2],
                                              "size":tmpmeminfo[3]
                                              }
            #print formmem
            formhwsn = request.POST.get('formhwsn',None)
            formhwproduct = request.POST.get('formhwproduct',None)
            formhwuuid = request.POST.get('formhwuuid',None)
            formhwmanu = request.POST.get('formhwmanu',None)
            formcpucore = request.POST.get('formcpucore',None)
            formcpumodel = request.POST.get('formcpumodel',None)
            formcpupyhsical = request.POST.get('formcpupyhsical',None)
            formcpuprocess = request.POST.get('formcpuprocess',None)
            networkInfo = {"addrlst":formip}
            hardwareInfo = {"SN":formhwsn,"Product":formhwproduct,"UUID":formhwuuid,"Manufacturer":formhwmanu}
            cpuInfo = {"cpuCore":formcpucore,"cpuModel":formcpumodel,"cpuPhysical":formcpupyhsical,"cpuProcess":formcpuprocess}
            newhostsubmit = HostInfo(
                                     hostname = formhostname,
                                     os = formos,
                                     ispublish = fompublish,
                                     machineType = formmachinetype,
                                     kernal = formkernal,
                                     networkinfo = networkInfo,
                                     hardwareinfo = hardwareInfo,
                                     cpuinfo = cpuInfo,
                                     changetime = datetime.datetime.now,
                                     memoryinfo = formmem
                                     )
            newhostsubmit.save()
            #print newhostsubmit.id
            ret['status'] = '提交成功'
            ret['popover'] = { "id":newhostsubmit.id,"info":"已经添加主机" }
        except Exception,e:
            ret['status'] = '提交失败'
            print e
            #添加跨站请求伪造的认证
        ret.update(csrf(request))
        return render_to_response('submit.html',ret,context_instance=RequestContext(request))
    else:
        ret.update(csrf(request))
        #ret['status'] = '提交成功'
        return render_to_response('submit.html',ret,context_instance=RequestContext(request))

#删除主机信息
@is_login_auth
def delhost(request,id):
    HostObj = HostInfo.objects.get(id=id)
    HostObj.delete()
    ret = {'allServerObj':None,'UserInfoObj':None,'PageInfo':None,'AllCount':None}
    try:
        page = int(page)
    except Exception:
        page = 1
    allServer = HostInfo.objects.all()
    AllCount = allServer.count()
    ret['AllCount'] = AllCount
    PageObj = Page(AllCount,page,6)
    allServerObj = allServer[PageObj.begin:PageObj.end]
    pageurl = 'index'
    pageinfo = page_div(page, PageObj.all_page_count,pageurl)
    ret['PageInfo'] = pageinfo
    ret['allServerObj'] = allServerObj
    UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
    ret['UserInfoObj'] = UserInfoObj
    ret['popover'] = { "id":id,"info":"已经删除主机" }
    return render_to_response('index.html',ret,context_instance=RequestContext(request))

#批量删除主机信息
@is_login_auth
def batchdelhost(request):
    if request.method == 'POST':
        #根据传进来的主机id批量删除数据库对象
        ret = {'allServerObj':None,'UserInfoObj':None,'PageInfo':None,'AllCount':None}
        tmpmeminfo = request.POST.getlist("checkboxdel[]",None)
        if tmpmeminfo:
            for i in tmpmeminfo:
                HostObj = HostInfo.objects.get(id=i)
                HostObj.delete()
            ids = ",".join(tmpmeminfo)
            ret['popover'] = { "id":ids,"info":"已经删除主机" }
        else:
            ret['popover'] = { "id":"","info":"没有选中可删除的主机" }
        try:
            page = int(page)
        except Exception:
            page = 1
        allServer = HostInfo.objects.all()
        AllCount = allServer.count()
        ret['AllCount'] = AllCount
        PageObj = Page(AllCount,page,6)
        allServerObj = allServer[PageObj.begin:PageObj.end]
        pageurl = 'index'
        pageinfo = page_div(page, PageObj.all_page_count,pageurl)
        ret['PageInfo'] = pageinfo
        ret['allServerObj'] = allServerObj
        UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
        ret['UserInfoObj'] = UserInfoObj
        return render_to_response('index.html',ret,context_instance=RequestContext(request))
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

#主机信息图形展示
@is_login_auth
def infoshow(request):
    if request.method == 'GET':
        ret = {}
        UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
        ret['UserInfoObj'] = UserInfoObj
        if request.GET.get("show",None) == "1":
            #通过使用mongodb的mapreduce聚合计算数据
            #这里emit里的1为伪赋值，目的是计算this.hardwareinfo.Manufacturer不同值的数量
            mapfunc = """
function() {
     emit(this.os,1);
}
"""

            reducefunc = """
function reduce(key, values) {
    return values.length;
}
"""

            datadic = {}
            for i in HostInfo.objects.map_reduce(mapfunc,reducefunc,'inline'):
                datadic[i.key] = i.value
            ret["result"] = "1"
            ret["data"] = datadic
            return render_to_response('infoshow.html',ret,context_instance=RequestContext(request))

        elif request.GET.get("show",None) == "2":
            #通过使用mongodb的mapreduce聚合计算数据
            #这里emit里的1为伪赋值，目的是计算this.hardwareinfo.Manufacturer不同值的数量
            mapfunc = """
function() {
     emit(this.hardwareinfo.Manufacturer,1);
}
"""

            reducefunc = """
function reduce(key, values) {
    return values.length;
}
"""

            datadic = {}
            for i in HostInfo.objects.map_reduce(mapfunc,reducefunc,'inline'):
                datadic[i.key] = i.value
            ret["result"] = "2"
            ret["data"] = datadic
            return render_to_response('infoshow.html',ret,context_instance=RequestContext(request))
        elif request.GET.get("show",None) == "3":
            datadic = {}
            datadic["已发布"] = HostInfo.objects(ispublish="1").count()
            datadic["已下架"] = HostInfo.objects(ispublish="0").count()
            ret["result"] = "3"
            ret["data"] = datadic
            return render_to_response('infoshow.html',ret,context_instance=RequestContext(request))
            
        else:
            return render_to_response('infoshow.html',ret,context_instance=RequestContext(request))
        

#webssh webshell功能
@is_login_auth
def web_terminal(request):
    UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
    print locals()
    return render_to_response('ws.html', locals())