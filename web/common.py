#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from django.utils.safestring import mark_safe
import re
import urllib

class Page:
    def __init__(self,AllCount,current_page,datanum=3):
        '''
        AllCount 所有数据条数  int
        current_page 当前页  int 
        datanum 每个页面展示多少条数据 ，默认3条  int
        '''
        self.DataNum=datanum
        self.AllCount=AllCount
        self.CurrentPage=current_page
        
    #装饰器property将方法装饰为属性
    @property
    def begin(self):
        return (self.CurrentPage-1)*self.DataNum
    @property
    def end(self):
        return self.CurrentPage*self.DataNum
    @property
    def all_page_count(self):
        #计算分页页面数量，一共有几页，divmod方法返回商和余数的元祖
        all_page = divmod(self.AllCount,self.DataNum)
        if all_page[1] == 0 and all_page[0] != 0:
            all_page_count = all_page[0]
        else:
            all_page_count = all_page[0]+1
        return all_page_count
        
#正常页面的分页方法        
def page_div(page,all_page_count,pageurl):
    '''
    page 总页面分页
    page 当前页面   int
    all_page_count 总页数 int
    pageurl 分页的页面信息 str
    '''
    #初始化页面分页为列表类型
    pagelist = []
    #分页逻辑判断，html标签的列表
    pagelist.append("<a class='pure-button' href='/web/%s/1'>首页</a>" %pageurl)
    if page == 1:
        pagelist.append("<a class='pure-button prev' href=''>上一页</a>")
    else:
        pagelist.append("<a  class='pure-button prev' href='/web/%s/%d'>上一页</a>" %(pageurl,(page-1)))
    
    
    #一次展示9个分页
    if all_page_count < 9:
        begin =0
        end =all_page_count
    elif page <5:
        begin =0
        end =9
        #end = page+4 
    elif page > all_page_count-4:
        #begin = page-5
        begin = all_page_count-9
        end = all_page_count    
    else:
        begin = page-5
        end = page+4
    for i in range(begin,end):
        if page == i+1:
            pagelist.append("<a class='pure-button' style='color:red;' href='/web/%s/%d'>%d</a>" %(pageurl,i+1,i+1))
        else:
            pagelist.append("<a class='pure-button' href='/web/%s/%d'>%d</a>" %(pageurl,i+1,i+1))
            

    if page == all_page_count:
        pagelist.append("<a class='pure-button next' href=''>下一页</a>")
    else:
        pagelist.append("<a class='pure-button next' href='/web/%s/%d'>下一页</a>" %(pageurl,(page+1)))
    pagelist.append("<a class='pure-button' href='/web/%s/%d'>尾页</a>" %(pageurl,all_page_count))
    #将列表类型的页面转换成字符串并且转义html标签能在前台显示
    return mark_safe(' '.join(pagelist))

#查询页面的分页方法        
def query_page_div(page,all_page_count,pageurl,querycondition):
    '''
    page 总页面分页
    page 当前页面   int
    all_page_count 总页数 int
    pageurl 分页的页面信息 str
    '''
    #初始化页面分页为列表类型
    pagelist = []
    #分页逻辑判断，html标签的列表
    pagelist.append("<a class='pure-button' href='/web/%s/1?%s'>首页</a>" %(pageurl,querycondition))
    if page == 1:
        pagelist.append("<a class='pure-button prev' href=''>上一页</a>")
    else:
        pagelist.append("<a  class='pure-button prev' href='/web/%s/%d?%s'>上一页</a>" %(pageurl,(page-1),querycondition))
    
    
    #一次展示9个分页
    if all_page_count < 9:
        begin =0
        end =all_page_count
    elif page <5:
        begin =0
        end =9
        #end = page+4 
    elif page > all_page_count-4:
        #begin = page-5
        begin = all_page_count-9
        end = all_page_count    
    else:
        begin = page-5
        end = page+4
    for i in range(begin,end):
        if page == i+1:
            pagelist.append("<a class='pure-button' style='color:red;' href='/web/%s/%d?%s'>%d</a>" %(pageurl,i+1,querycondition,i+1))
        else:
            pagelist.append("<a class='pure-button' href='/web/%s/%d?%s'>%d</a>" %(pageurl,i+1,querycondition,i+1))
            

    if page == all_page_count:
        pagelist.append("<a class='pure-button next' href=''>下一页</a>")
    else:
        pagelist.append("<a class='pure-button next' href='/web/%s/%d?%s'>下一页</a>" %(pageurl,(page+1),querycondition))
    pagelist.append("<a class='pure-button' href='/web/%s/%d?%s'>尾页</a>" %(pageurl,all_page_count,querycondition))
    #将列表类型的页面转换成字符串并且转义html标签能在前台显示
    return mark_safe(' '.join(pagelist))


#将传来的post信息做解析，分割过滤后就剩插槽名和js数组名
def split_form_str(str):
    tmpdic = {}
    #transtr = urllib.unquote(str.encode("utf8"))
    transtr = str.encode("utf8")
    for i in transtr.split("&"):
        kv = i.split("=")
        #print kv
        #对url字符串解码
        k = urllib.unquote_plus(kv[0].encode("utf-8"))
        v = urllib.unquote_plus(kv[1].encode("utf-8"))
        if re.match('formmem\d+$',k):
            tmpdic[k] = v
    return tmpdic