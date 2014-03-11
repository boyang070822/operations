# coding=utf8

"""
datanode environment setup

1. 检查cpu个数和核心个数、内存大小、磁盘个数和容量、操作系统版本
2. 创建hadoop用户，配置免密码ssh（从本机、从远程机器）和免密码sudo
3. 修改open files和nproc限制，修改timezone，配置ntp
4. 安装和配置mysql, jdk6, jdk7, datanode, tasktracker, hbase, maven
5. 修改hdfs和mapred用户的限制
6. 更新hosts
"""

import os
from fabric.api import *
from fabric.contrib.files import exists


DOWNLOAD_DIR = "/home/hadoop/download/"
RELEASE_DIR = "/home/hadoop/release/"
BACKUP_DIR = "/home/hadoop/backup/"
GIT_DIR= "/home/hadoop/git_project_home/"
RUN_DIR = "/home/hadoop/run/"
LIMIT_FILE= "/etc/security/limits.conf"
PROFILE="/etc/profile"

def make_dir():
    for directory in (DOWNLOAD_DIR, RELEASE_DIR, BACKUP_DIR, RUN_DIR,GIT_DIR):
        run("mkdir -p %s" % directory)
def make_special_dir(dir):
    run("mkdir -p %s" % dir)

def rsync_dir():
    # download目录里面应该有如下文件：jdk6 jdk7
    # release目录里面应该有如下文件：hbase drill
    for directory in (DOWNLOAD_DIR, RELEASE_DIR,GIT_DIR):
        local("rsync -avz --progress %s %s@%s:%s" % (directory, env.user, env.host, directory))
def rsync_special_dir(dir):
	local("rsync -avz --progress %s %s@%s:%s" % (dir, env.user, env.host, dir))

def install_mysql():
    sudo("yum -y install mysql mysql-server")

def install_jdk6():
    jdk6_bin = "jdk-6u45-linux-x64.bin"
    jdk6_dir = "jdk1.6.0_45"
    target_dir = "/usr/java"

    with cd(DOWNLOAD_DIR):
        assert exists(os.path.join(DOWNLOAD_DIR, jdk6_bin))
        run("chmod +x %s" % jdk6_bin)
        run("./%s" % jdk6_bin)
        if not exists(target_dir):
            sudo("mkdir %s" % target_dir)
        sudo("mv %s %s" % (jdk6_dir, os.path.join(target_dir, jdk6_dir)))
    sudo("mkdir -p %s" % target_dir)
    with cd(target_dir):
        assert exists(os.path.join(target_dir, jdk6_dir))
        for link in ("jdk", "latest"):
            if exists(os.path.join(target_dir, link)):
                sudo("rm %s" % link)
            sudo("ln -s %s %s" % (os.path.join(target_dir, jdk6_dir), link))


def install_jdk7():
    jdk7_tarball = os.path.join(DOWNLOAD_DIR, "jdk-7u45-linux-x64.tar.gz")
    assert exists(jdk7_tarball)

    target_dir = "/usr/java"
    with cd(target_dir):
        sudo("tar -zxf %s" % jdk7_tarball)

def install_maven():
    maven_tarball= os.path.join(DOWNLOAD_DIR,"apache-maven-3.0.5-bin.tar.gz")
    assert exists(maven_tarball)
    
    target_dir= "/usr/local"
    with cd(target_dir):
	sudo("tar -zxf %s" % maven_tarball)
def install_git():
    sudo("yum -y install git")

def enable_epel():
    epel_url = "http://ftp.cuhk.edu.hk/pub/linux/fedora-epel/6/i386/epel-release-6-8.noarch.rpm"
    epel_pkg = "epel-release-6-8.noarch.rpm"

    with cd(DOWNLOAD_DIR):
        run("wget %s" % epel_url)
        if "epel-release-6-8" not in run("rpm -qa"):
            sudo("rpm -ivh %s" % epel_pkg)


def install_cloudera_repo():
    # 请参考CDH文档中Downloading and Installing an Earlier Release部分
    repo_url = "http://archive.cloudera.com/cdh4/one-click-install/redhat/6/x86_64/cloudera-cdh-4-0.x86_64.rpm"
    with cd(DOWNLOAD_DIR):
        run("wget %s" % repo_url)
	sudo("yum --nogpgcheck localinstall cloudera-cdh-4-0.x86_64.rpm")
    sudo("sudo rpm --import http://archive.cloudera.com/cdh4/redhat/6/x86_64/cdh/RPM-GPG-KEY-cloudera")
    sudo("yum clean all")
def uninstall_cloudera_repo():
   if exists("/etc/yum.repos.d/cloudera-cdh4.repo"):
	  sudo("rm /etc/yum.repos.d/cloudera-cdh4.repo")


def install_datanode():
    sudo("yum -y install hadoop-hdfs-datanode")
def install_namenode():
    sudo("yum -y install hadoop-hdfs-namenode")
def install_jobtracker():
    sudo("yum -y install hadoop-0.20-mapreduce-jobtracker")
def install_client():
    sudo("yum -y install hadoop-client")
def install_secondarynamenode(): 
    sudo("yum -y install hadoop-hdfs-secondarynamenode")
def install_resourcemanager():
    sudo("yum -y install hadoop-yarn-resourcemanager")
def install_nodemanager():
    sudo("yum -y install hadoop-yarn-nodemanager")
def install_yarn_mapreduce():
    sudo("yum -y install hadoop-mapreduce")

def install_tasktracker():
    sudo("yum -y install hadoop-0.20-mapreduce-tasktracker")


def install_lzo():
    lzo_cdh4_repo = "http://archive.cloudera.com/gplextras/redhat/6/x86_64/gplextras/cloudera-gplextras4.repo"

    with cd(DOWNLOAD_DIR):
        run("wget %s" % lzo_cdh4_repo)
        sudo("cp cloudera-gplextras4.repo /etc/yum.repos.d/")
        sudo("yum -y install hadoop-lzo-cdh4")


def install_hbase_region():
    sudo("yum -y install hbase")
    sudo("yum -y install hbase-regionserver")
def install_hbase_master():
    sudo("yum -y install hbase")
    sudo("yum -y install hbase-master")

def install_drill():
    pass


def install_ntp():
    sudo("yum -y install ntp")
    sudo("chkconfig ntpd on")
    sudo("cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime")
    sudo("/sbin/service ntpd start")
    sudo("ntpdate -u  pool.ntp.org")

def install_fabric():
   sudo("yum install gcc gcc-c++ autoconf automake")
   sudo("yum install python-devel")
   sudo("easy_install fabric")

def modify_limits():
    # 修改hdfs和mapred用户的限制
    src_dir = "/etc/security/limits.d/"
    local("rsync -avz --progress %s %s@%s:%s" % (src_dir, env.user, env.host, BACKUP_DIR))
    for conf_file in ("hdfs.conf", "mapred.conf"):
        conf_path = os.path.join(BACKUP_DIR, conf_file)
        if not exists(conf_path):
            print conf_path, "not exists"
            continue

        sudo("cp %s %s" % (conf_path, src_dir))


def setup_worker():
    make_dir()
    rsync_dir()

    enable_epel()
    enable_cloudera_repo()

    install_fabric()

    install_datanode()
    install_tasktracker()
    install_client()
    install_lzo()
    install_hbase_regionserver()
    install_mysql()

    install_jdk6()
    install_jdk7()
    install_maven()
    install_git()

    install_ntp()
    modify_limits()

def setup_master():
    make_dir()
    rsync_dir()

    enable_epel()
    enable_cloudera_repo()

    install_fabric()

    install_namenode()
    install_jobtracker()
    install_client()
    install_lzo()
    install_hbase_master()
    install_mysql()

    install_jdk6()
    install_jdk7()
    install_maven()
    install_git()

    install_ntp()
    modify_limits()
