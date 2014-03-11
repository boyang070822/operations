#!/usr/bin/python
from fabric.api import *
from fabric.contrib.files import exists
import os

def rsync():
    local("rsync -avz --progress /home/hadoop/git_project_home/operations/ %s@%s:/home/hadoop/git_project_home/operations/" % (env.user,env.host))
