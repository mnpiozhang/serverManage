#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
WSGI config for serverManage project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

from web.logger import log
import functools
import os
from django.core.wsgi import get_wsgi_application
from django.core.signals import request_started, request_finished

import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import define, options
import tornado.wsgi
from webssh.wth import WebTerminalHandler
from webssh.ioloop import IOLoop


def django_request_support(func):
    @functools.wraps(func)
    def _deco(*args, **kwargs):
        request_started.send_robust(func)
        response = func(*args, **kwargs)
        request_finished.send_robust(func)
        return response

    return _deco

##############################





define('port', type=int, default=8000)
def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serverManage.settings")
    wsgi_app  = get_wsgi_application()
    #即使直接的docker镜像已经配置了时区的环境变量,但是在调用django的get_wsgi_application()方法后,就又变回UTC时区了.所以在下面重新定义时区环境变量
    os.environ["TZ"] = "Asia/Shanghai"
    container = tornado.wsgi.WSGIContainer(wsgi_app)
    tornado_app = tornado.web.Application(
        [
            (r'/ws/terminal', WebTerminalHandler),
            (r"/static/(.*)", tornado.web.StaticFileHandler,dict(path=os.path.join(os.path.dirname(__file__),'web',"static"))),
            ('.*', tornado.web.FallbackHandler, dict(fallback=container)),
        ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port, address='0.0.0.0')
    log.info("service start")
    #log.info(os.getenv("TZ"))
    IOLoop.instance().start()
    tornado.ioloop.IOLoop.instance().start()
    

if __name__ == '__main__':
    #print "service start"
    main()
    

'''
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workordersys.settings")

application = get_wsgi_application()
'''