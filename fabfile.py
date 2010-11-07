
from __future__ import with_statement # needed for python 2.5
from fabric.api import env, run, local

def runserver():
    local('dev_appserver.py src --enable_sendmail', capture=False)
