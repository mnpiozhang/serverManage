#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
WSGI config for serverManage project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""


import functools
import logging
import os
from django.core.wsgi import get_wsgi_application
import re
from django.core.signals import request_started, request_finished
import pyte
import socket
import threading
import time
import select

import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.gen
import tornado.httpclient
from tornado.options import define, options
import tornado.wsgi
from tornado.websocket import WebSocketClosedError
from wth import WebTerminalHandler

def django_request_support(func):
    @functools.wraps(func)
    def _deco(*args, **kwargs):
        request_started.send_robust(func)
        response = func(*args, **kwargs)
        request_finished.send_robust(func)
        return response

    return _deco

##############################
from tornado.options import options, define
define('port', type=int, default=8000)
def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serverManage.settings")
    wsgi_app  = get_wsgi_application()
    container = tornado.wsgi.WSGIContainer(wsgi_app)
    tornado_app = tornado.web.Application(
        [
            (r'/ws/terminal', WebTerminalHandler),
            (r"/static/(.*)", tornado.web.StaticFileHandler,dict(path=os.path.join(os.path.dirname(__file__),'web',"static"))),
            ('.*', tornado.web.FallbackHandler, dict(fallback=container)),
        ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
    

if __name__ == '__main__':
    print "server start"
    main()


'''
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workordersys.settings")

application = get_wsgi_application()
'''