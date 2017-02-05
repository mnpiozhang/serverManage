# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CpuInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cpuModel', models.CharField(max_length=50, verbose_name='cpu\u578b\u53f7')),
                ('cpuPhysical', models.IntegerField(verbose_name='\u7269\u7406cpu\u6570\u91cf')),
                ('cpuCore', models.IntegerField(verbose_name='cpu\u5185\u6838\u6570')),
                ('cpuProcess', models.IntegerField(verbose_name='cpu\u7ebf\u7a0b\u6570')),
            ],
        ),
        migrations.CreateModel(
            name='HardwareInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product', models.CharField(max_length=50, verbose_name='\u4ea7\u54c1\u540d\u79f0')),
                ('manufacturer', models.CharField(max_length=50, verbose_name='\u5236\u9020\u5546')),
                ('uuid', models.CharField(max_length=50, verbose_name='uuid')),
                ('serialNumber', models.CharField(max_length=50, verbose_name='\u5e8f\u5217\u53f7')),
            ],
        ),
        migrations.CreateModel(
            name='HostInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(unique=True, max_length=50, verbose_name='\u670d\u52a1\u5668\u4e3b\u673a\u540d')),
                ('os', models.CharField(max_length=20, verbose_name='\u64cd\u4f5c\u7cfb\u7edf')),
                ('machineType', models.CharField(max_length=20, verbose_name='\u670d\u52a1\u5668\u4f4d\u6570')),
                ('kernal', models.CharField(max_length=50, verbose_name='\u5185\u6838\u7248\u672c')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
        ),
        migrations.CreateModel(
            name='MemoryInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('memSize', models.FloatField(verbose_name='\u5185\u5b58\u5927\u5c0f')),
                ('host', models.ForeignKey(related_name='host_memory', verbose_name='\u670d\u52a1\u5668\u5185\u5b58', to='web.HostInfo')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nic', models.CharField(max_length=50, verbose_name='\u7f51\u5361')),
                ('ipaddr', models.GenericIPAddressField(verbose_name='\u7f51\u7edc\u5730\u5740')),
                ('host', models.ForeignKey(related_name='host_network', verbose_name='\u670d\u52a1\u5668\u7f51\u5361', to='web.HostInfo')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50, verbose_name='\u7528\u6237\u540d')),
                ('password', models.CharField(max_length=50, verbose_name='\u5bc6\u7801')),
                ('realname', models.CharField(max_length=20, verbose_name='\u771f\u5b9e\u59d3\u540d')),
                ('telphone', models.CharField(max_length=12, verbose_name='\u7528\u6237\u7535\u8bdd')),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typename', models.CharField(max_length=50, verbose_name='\u7528\u6237\u7c7b\u578b\u540d\u79f0')),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='type',
            field=models.ForeignKey(verbose_name='\u7528\u6237\u7c7b\u578b', to='web.UserType'),
        ),
        migrations.AddField(
            model_name='hardwareinfo',
            name='host',
            field=models.OneToOneField(related_name='host_hardware', verbose_name='\u4e3b\u673a\u786c\u4ef6', to='web.HostInfo'),
        ),
        migrations.AddField(
            model_name='cpuinfo',
            name='host',
            field=models.OneToOneField(related_name='host_cpu', verbose_name='\u4e3b\u673aCPU', to='web.HostInfo'),
        ),
    ]
