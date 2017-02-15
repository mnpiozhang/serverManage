服务器信息采集系统
====
抽空基于django写了一个服务器信息采集管理系统，后台数据库用了SQLite和MongoDB。（还在完善中。。。）

说明
===========
* SQLite保存用户信息密码等数据，默认django admin登陆用户名密码为admin/admin，系统登陆用户名密码aaa/aaa。MongoDB保存具体的服务器信息数据。
* 使用了mongoengine模块驱动MongoDB，故需要先安装pip install mongoengine
* MongoDB连接的配置在项目的settings.py文件中配置，默认具体项为connect('smproject', host='192.168.188.129', port=27017)。可根据实际情况做配置。
* 默认登陆地址为http://127.0.0.1:8000/
* 采集数据可以使用项目最上层目录下的collectScript.py脚本。修改脚本中的url变量为具体的服务地址，然后通过saltstack或其他工具分发至节点服务器上执行，就能将节点服务器的基本信息采集到并调用本服务的接口导入数据。
* 也支持手工输入提交服务器的基本信息，但暂时操作系统类型只提供centos和unbantu两种类型。
* 通过MongoDB的MapReduce聚合计算数据来做图表展示，但目前只有基于发布状态、操作系统版本、生产厂商三类（以后再完善。。）
