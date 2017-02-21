import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serverManage.settings")
import django.conf
import django.contrib.auth
import django.core.handlers.wsgi
from django.core.wsgi import get_wsgi_application
import django.db

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

from tornado.options import options, define

define('port', type=int, default=8080)

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello from tornado')


def main():
    wsgi_app = tornado.wsgi.WSGIContainer(get_wsgi_application())
    tornado_app = tornado.web.Application(
        [
            (r'/hello-tornado*', HelloHandler),
            (r'.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()