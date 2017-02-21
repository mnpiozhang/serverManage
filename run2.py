#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
WSGI config for serverManage project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import paramiko
import functools
import logging
import os
from django.core.wsgi import get_wsgi_application
import re

import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.gen
import tornado.httpclient
from tornado.options import define, options
import tornado.wsgi


def set_log(level, filename='servermanage.log'):
    """
    return a log file object
    根据提示设置log打印
    """
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    '''
    if not os.path.isfile(log_file):
        os.mknod(log_file)
        os.chmod(log_file, 0777)
    '''
    log_level_total = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARN, 'error': logging.ERROR,
                       'critical': logging.CRITICAL}
    logger_f = logging.getLogger()
    logger_f.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level_total.get(level, logging.DEBUG))
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger_f.addHandler(fh)
    return logger_f

logger = set_log('debug')


def django_request_support(func):
    @functools.wraps(func)
    def _deco(*args, **kwargs):
        request_started.send_robust(func)
        response = func(*args, **kwargs)
        request_finished.send_robust(func)
        return response

    return _deco

class Tty(object):
    """
    A virtual tty class
    一个虚拟终端类，实现连接ssh和记录日志，基类
    """
    def __init__(self, user, asset, role, login_type='ssh'):
        #self.username = user.username
        self.username = "hu"
        self.asset_name = "192.168.188.129"
        self.ip = None
        self.port = 22
        self.ssh = None
        self.channel = None
        self.asset = asset
        self.user = user
        self.role = role
        self.remote_ip = ''
        self.login_type = login_type
        self.vim_flag = False
        self.vim_end_pattern = re.compile(r'\x1b\[\?1049', re.X)
        self.vim_data = ''
        self.stream = None
        self.screen = None
        self.__init_screen_stream()

    def __init_screen_stream(self):
        """
        初始化虚拟屏幕和字符流
        """
        self.stream = pyte.ByteStream()
        self.screen = pyte.Screen(80, 24)
        self.stream.attach(self.screen)

    @staticmethod
    def is_output(strings):
        newline_char = ['\n', '\r', '\r\n']
        for char in newline_char:
            if char in strings:
                return True
        return False

    @staticmethod
    def command_parser(command):
        """
        处理命令中如果有ps1或者mysql的特殊情况,极端情况下会有ps1和mysql
        :param command:要处理的字符传
        :return:返回去除PS1或者mysql字符串的结果
        """
        result = None
        match = re.compile('\[?.*@.*\]?[\$#]\s').split(command)
        if match:
            # 只需要最后的一个PS1后面的字符串
            result = match[-1].strip()
        else:
            # PS1没找到,查找mysql
            match = re.split('mysql>\s', command)
            if match:
                # 只需要最后一个mysql后面的字符串
                result = match[-1].strip()
        return result

    def deal_command(self, data):
        """
        处理截获的命令
        :param data: 要处理的命令
        :return:返回最后的处理结果
        """
        command = ''
        try:
            self.stream.feed(data)
            # 从虚拟屏幕中获取处理后的数据
            for line in reversed(self.screen.buffer):
                line_data = "".join(map(operator.attrgetter("data"), line)).strip()
                if len(line_data) > 0:
                    parser_result = self.command_parser(line_data)
                    if parser_result is not None:
                        # 2个条件写一起会有错误的数据
                        if len(parser_result) > 0:
                            command = parser_result
                    else:
                        command = line_data
                    break
        except Exception:
            pass
        # 虚拟屏幕清空
        self.screen.reset()
        return command

    def get_connect_info(self):
        """
        获取需要登陆的主机的信息和映射用户的账号密码
        """
        #asset_info = get_asset_info(self.asset)
        role_key = '1234567'  # 获取角色的key，因为ansible需要权限是600，所以统一生成用户_角色key
        #role_pass = CRYPTOR.decrypt(self.role.password)
        connect_info = {'user': self.user, 'asset': self.asset, 'ip': '192.168.188.129',
                        'port': 22, 'role_name': 'hu',
                        'role_pass': 'mnpiozhang', 'role_key': role_key}
        logger.debug(connect_info)
        return connect_info

    def get_connection(self):
        """
        获取连接成功后的ssh
        """
        connect_info = self.get_connect_info()

        # 发起ssh连接请求 Make a ssh connection
        ssh = paramiko.SSHClient()
        # ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            role_key = connect_info.get('role_key')
            try:
                ssh.connect(connect_info.get('ip'),
                            port=connect_info.get('port'),
                            username=connect_info.get('role_name'),
                            password=connect_info.get('role_pass'),
                            key_filename=role_key,
                            look_for_keys=False)
                return ssh
            except (paramiko.ssh_exception.AuthenticationException, paramiko.ssh_exception.SSHException):
                logger.warning(u'使用ssh key %s 失败, 尝试只使用密码' % role_key)
                pass

            ssh.connect(connect_info.get('ip'),
                        port=connect_info.get('port'),
                        username=connect_info.get('role_name'),
                        password=connect_info.get('role_pass'),
                        allow_agent=False,
                        look_for_keys=False)

        except (paramiko.ssh_exception.AuthenticationException, paramiko.ssh_exception.SSHException):
            raise ServerError('认证失败 Authentication Error.')
        except socket.error:
            raise ServerError('端口可能不对 Connect SSH Socket Port Error, Please Correct it.')
        else:
            self.ssh = ssh
            return ssh

class WebTty(Tty):
    def __init__(self, *args, **kwargs):
        super(WebTty, self).__init__(*args, **kwargs)
        self.ws = None
        self.data = ''
        self.input_mode = False

class WebTerminalHandler(tornado.websocket.WebSocketHandler):
    clients = []
    tasks = []

    def __init__(self, *args, **kwargs):
        self.term = None
        self.log_file_f = None
        self.log_time_f = None
        self.log = None
        self.id = 0
        self.user = None
        self.ssh = None
        self.channel = None
        super(WebTerminalHandler, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    @django_request_support
    def open(self):
        logger.debug('Websocket: Open request')
        role_name = self.get_argument('role', 'sb')
        asset_id = self.get_argument('id', 9999)
        asset = get_object(Asset, id=asset_id)
        #self.termlog = TermLogRecorder(User.objects.get(id=self.user_id))
        if asset:
            roles = user_have_perm(self.user, asset)
            logger.debug(roles)
            logger.debug('系统用户: %s' % role_name)
            login_role = ''
            for role in roles:
                if role.name == role_name:
                    login_role = role
                    break
            if not login_role:
                logger.warning('Websocket: Not that Role %s for Host: %s User: %s ' % (role_name, asset.hostname,
                                                                                       self.user.username))
                self.close()
                return
        else:
            logger.warning('Websocket: No that Host: %s User: %s ' % (asset_id, self.user.username))
            self.close()
            return
        logger.debug('Websocket: request web terminal Host: %s User: %s Role: %s' % (asset.hostname, self.user.username,
                                                                                     login_role.name))
        self.term = WebTty(self.user, asset, login_role, login_type='web')
        # self.term.remote_ip = self.request.remote_ip
        self.term.remote_ip = self.request.headers.get("X-Real-IP")
        if not self.term.remote_ip:
            self.term.remote_ip = self.request.remote_ip
        self.ssh = self.term.get_connection()
        self.channel = self.ssh.invoke_shell(term='xterm')
        WebTerminalHandler.tasks.append(MyThread(target=self.forward_outbound))
        WebTerminalHandler.clients.append(self)

        for t in WebTerminalHandler.tasks:
            if t.is_alive():
                continue
            try:
                t.setDaemon(True)
                t.start()
            except RuntimeError:
                pass

    def on_message(self, message):
        jsondata = json.loads(message)
        if not jsondata:
            return

        if 'resize' in jsondata.get('data'):
            self.termlog.write(message)
            self.channel.resize_pty(
                width=int(jsondata.get('data').get('resize').get('cols', 100)),
                height=int(jsondata.get('data').get('resize').get('rows', 35))
            )
        elif jsondata.get('data'):
            self.termlog.recoder = True
            self.term.input_mode = True
            if str(jsondata['data']) in ['\r', '\n', '\r\n']:
                match = re.compile(r'\x1b\[\?1049', re.X).findall(self.term.vim_data)
                if match:
                    if self.term.vim_flag or len(match) == 2:
                        self.term.vim_flag = False
                    else:
                        self.term.vim_flag = True
                elif not self.term.vim_flag:
                    result = self.term.deal_command(self.term.data)[0:200]
                    if len(result) > 0:
                        TtyLog(log=self.log, datetime=datetime.datetime.now(), cmd=result).save()
                self.term.vim_data = ''
                self.term.data = ''
                self.term.input_mode = False
            self.channel.send(jsondata['data'])
        else:
            pass

    def on_close(self):
        logger.debug('Websocket: Close request')
        print self.termlog.CMD
        self.termlog.save()
        if self in WebTerminalHandler.clients:
            WebTerminalHandler.clients.remove(self)
        try:
            self.log_file_f.write('End time is %s' % datetime.datetime.now())
            self.log.is_finished = True
            self.log.end_time = datetime.datetime.now()
            self.log.filename = self.termlog.filename
            self.log.save()
            self.log_time_f.close()
            self.ssh.close()
            self.close()
        except AttributeError:
            pass

    def forward_outbound(self):
        self.log_file_f, self.log_time_f, self.log = self.term.get_log()
        self.id = self.log.id
        self.termlog.setid(self.id)
        try:
            data = ''
            pre_timestamp = time.time()
            while True:
                r, w, e = select.select([self.channel], [], [])
                if self.channel in r:
                    recv = self.channel.recv(1024)
                    if not len(recv):
                        return
                    data += recv
                    self.term.vim_data += recv
                    try:
                        self.write_message(data.decode('utf-8', 'replace'))
                        self.termlog.write(data)
                        self.termlog.recoder = False
                        now_timestamp = time.time()
                        self.log_time_f.write('%s %s\n' % (round(now_timestamp - pre_timestamp, 4), len(data)))
                        self.log_file_f.write(data)
                        pre_timestamp = now_timestamp
                        self.log_file_f.flush()
                        self.log_time_f.flush()
                        if self.term.input_mode:
                            self.term.data += data
                        data = ''
                    except UnicodeDecodeError:
                        pass
        except IndexError:
            pass








##############################
def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serverManage.settings")
    wsgi_app  = get_wsgi_application()
    container = tornado.wsgi.WSGIContainer(wsgi_app)
    setting = {
        'cookie_secret': 'DFksdfsasdfkasdfFKwlwfsdfsa1204mx',
        'template_path': os.path.join(os.path.dirname(__file__),'web','templates'),
        'static_path': os.path.join(os.path.dirname(__file__),'web','static'),
        'debug': False,
    }
    tornado_app = tornado.web.Application(
        [
            (r'/ws/terminal', WebTerminalHandler),
            (r"/static/(.*)", tornado.web.StaticFileHandler,dict(path=os.path.join(os.path.dirname(__file__),'web',"static"))),
            ('.*', tornado.web.FallbackHandler, dict(fallback=container)),
        ], **setting)
    server = tornado.httpserver.HTTPServer(tornado_app)
    tornado.ioloop.IOLoop.instance().start()
    server.listen(8000, address='0.0.0.0')

if __name__ == '__main__':
    main()


'''
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workordersys.settings")

application = get_wsgi_application()
'''