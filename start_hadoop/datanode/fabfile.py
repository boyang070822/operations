#!/usr/bin/python
import os
from fabric.api import *
from fabric.contrib.files import exists

DATA_DIR0="/data0/"
DATA_DIR1="/data1/"
DATA_DIR2="/data2/"
DATA_DIR3="/data3/"
DATA_DIR4="/data4/"
DATA_DIR5="/data5/"
SAME_DIR="hadoop/cache/hadoop/dfs/data"
def make_datadir():
   for dir in (DATA_DIR0,DATA_DIR1,DATA_DIR2,DATA_DIR3,DATA_DIR4,DATA_DIR5):
	ABSOLUTEDIR=os.path.join(dir,SAME_DIR)
	sudo("mkdir -p %s" % ABSOLUTEDIR)
        sudo("chown -R hadoop:hadoop %s " % os.path.join(dir,"hadoop"))
        sudo("chmod 775 %s" % ABSOLUTEDIR)
def start_datanode():
   sudo("service hadoop-hdfs-datanode start")

def stop_datanode():
   sudo("service hadoop-hdfs-datanode stop")

