#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from common import solve_request
# Create your views here.

@csrf_exempt
def apiimport(request):
    if request.method == 'POST':
        try:
            receiveData = json.loads(request.body)
            #print receiveData
        except Exception,e:
            print e
            return HttpResponse("json is invaild")
        result = solve_request(receiveData)
        return HttpResponse(result)
        #return HttpResponse("hehe")
    else:
        return HttpResponse("this is a http interface")
    
