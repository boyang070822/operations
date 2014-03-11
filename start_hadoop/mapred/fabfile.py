#!/usr/bin/python
from fabric.api import *
from fabric.contrib.files import exists
import os

def start_jobtracker():
    sudo("service hadoop-0.20-mapreduce-jobtracker start")
def stop_jobtracker():
    sudo("service hadoop-0.20-mapreduce-jobtracker stop")
def restart_jobtracker():
    sudo("service hadoop-0.20-mapreduce-jobtracker restart")
def start_tasktracker():
    sudo("service hadoop-0.20-mapreduce-tasktracker start")
def restart_tasktracker():
    sudo("service hadoop-0.20-mapreduce-tasktracker restart")
def stop_tasktracker():
    sudo("service hadoop-0.20-mapreduce-tasktracker stop")

def mk_local_dir():
    sudo("mkdir -p /data/hadoop/cache/hadoop/mapred/local")
    sudo("chown -R mapred:mapred /data/hadoop/cache/hadoop/mapred/local")

def rsync_config():
    local("rsync -avz --progress /etc/hadoop/conf/mapred-site.xml %s@%s:/etc/hadoop/conf/mapred-site.xml " % (env.user,env.host))
