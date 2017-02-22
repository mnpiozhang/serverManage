服务器信息采集系统
====
抽空基于django写了一个服务器信息采集管理系统，后台数据库用了SQLite和MongoDB。（还在完善中。。。）

说明
===========
* SQLite保存用户信息密码等数据，默认django admin登陆用户名密码为admin/admin，系统登陆有两个不同的用户，用户名密码分别为aaa/aaa和bbb/bbb，分别对应两个不同的权限前者为admin后者为test，这些都可以再django admin中定义。MongoDB保存具体的服务器信息数据。
* 使用了mongoengine模块驱动MongoDB，故需要先安装pip install mongoengine
* 支持webshell功能，前提是需要首先提交该服务器的登陆用户名密码等信息，这些信息不在采集范围内。主要是使用了tornado的websocket功能，具体实现参照了[xsank/webssh](https://github.com/xsank/webssh)。使用改功能的用户必须是admin权限。同时也需要先安装tornado和paramiko，pip install tornado;pip install paramiko
* MongoDB连接的配置在项目的settings.py文件中配置，默认具体项为connect('smproject', host='192.168.188.129', port=27017)。可根据实际情况做配置。
* 启动脚本为run.py，使用python run.py命令启动
* 默认登陆地址为http://127.0.0.1:8000/，具体配置可以在run.py启动脚本中修改。
* 采集数据可以使用项目最上层目录下的collectScript.py脚本。修改脚本中的url变量为具体的服务地址，然后通过saltstack或其他工具分发至节点服务器上执行，就能将节点服务器的基本信息采集到并调用本服务的接口导入数据。
* 也支持手工输入提交服务器的基本信息，但暂时操作系统类型只提供centos和unbantu两种类型。
* 通过MongoDB的MapReduce聚合计算数据来做图表展示，但目前只有基于发布状态、操作系统版本、生产厂商三类（以后再完善。。）
* 可以使用Dockerfile快速构建运行环境，举例：在项目的最上层目录执行 docker build -t smimage . 构建docker镜像smimage，然后启动容器docker run --name smproj -v "$PWD":/usr/src/app -p 8001:8000 -d smimage创建容器名为smproj的该应用容器，然后直接访问http://XXX.XXX.XXX.XXX:8001/即可。


大致的样子
===========

![index](https://github.com/mnpiozhang/serverManage/blob/master/example/index.jpg)
![index](https://github.com/mnpiozhang/serverManage/blob/master/example/accordingos.jpg)
![index](https://github.com/mnpiozhang/serverManage/blob/master/example/webssh.jpg)