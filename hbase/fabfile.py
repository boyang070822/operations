from fabric.api import *
from fabric.contrib.files import exists
import os

def install_hbase():
    sudo("yum -y install hbase")
    sudo("yum -y install hbase-master")
    sudo("yum -y install hbase-regionserver")
    sudo("yum -y install zookeeper-server")
def install_thrift():
    sudo("yum -y install hbase-thrift")
def install_rest():
    sudo("yum -y install hbase-rest")
def start_thrift():
    sudo("service hbase-thrift start")
def start_rest():
    sudo("service hbase-rest start")

def start_master():
   sudo("service hbase-master start")

def stop_master():
   sudo("service hbase-master stop")

def start_regionserver():
   sudo("service hbase-regionserver start")

def stop_regionserver():
   sudo("service hbase-regionserver stop")

def init_zookeeper():
   sudo("service zookeeper-server init")

def start_zookeeper():
   sudo("service zookeeper-server start")

def stop_zookeeper():
   sudo("service zookeeper-server stop")

def rsync_zoo_config():
   local("rsync -avz --progress /etc/zookeeper/conf/ %s@%s:/etc/zookeeper/conf/ " % (env.user,env.host))

def rsync_hbase_config():
   local("rsync -avz --progress /etc/hbase/conf/ %s@%s:/etc/hbase/conf/ " % (env.user,env.host))

def get_status():
    with warn_only():
   	sudo("service hbase-master status")
   	sudo("service hbase-regionserver status")
   	sudo("service zookeeper-server status")
