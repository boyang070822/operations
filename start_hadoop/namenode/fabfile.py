#!/usr/bin/python
from fabric.api import *
import os
from fabric.contrib.files import exists
NAME_DIR="/data/hadoop/cache/hadoop/dfs/name"
def start_namenode():
    sudo("service hadoop-hdfs-namenode start")
def stop_namenode():
    sudo("service hadoop-hdfs-namenode stop")
def make_name_dir():
    sudo("mkdir -p %s " % NAME_DIR )
    sudo("chown -R hadoop:hadoop /data/hadoop")
    sudo("chmod 775 %s " % NAME_DIR)
