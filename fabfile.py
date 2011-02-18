from __future__ import with_statement
import os
import sys

from fabric.api import *

def runserver():
    """ runs local server to default port 8080
    """
    local('dev_appserver.py src --enable_sendmail', capture=False)

def deploy():
    """ Deploys to app engine
    """
    local('appcfg.py update src', capture=False)

def install_closure():
    """ Configures and installs closure libs

    PRE:
        Used Commads:
            - mkdir
            - unzip
            - rm
            - wget
            - svn
    """

    #
    # clean up
    #
    local('rm -rf tools')

    _install_closure_templates()
    _install_closure_compiler()
    _install_closure_library()

def _install_closure_templates(root="tools", dir_name="closure-templates"):
    """Downloads Closure templates js compiler to specified root path

    @Pre: root and dir_name exist
    """
    #
    # Gets closure templates using latest Zip
    path = '%s/%s' % (root, dir_name)
    local('mkdir -p %s' % path)
    with cd(path):
        local('wget http://closure-templates.googlecode.com/files/closure-templates-for-javascript-latest.zip', capture=False)
        local('unzip closure-templates-for-javascript-latest.zip', capture=False)
        local('rm closure-templates-for-javascript-latest.zip', capture=False)

    
def _install_closure_library(root="tools", dir_name="closure-library"):
    """Downloads Closure js library to specified root path

    @Pre: root and dir_name exist
    """

    #TODO: should we use git instead of svn?
    #
    # Gets closure templates using latest Zip
    path = '%s/%s' % (root, dir_name)
    abs_path = '%s/%s' % (os.getcwd(), path)
    dest_path = 'src/tic/web/client/frameworks/closure'
    closure_dest_path = '%s/closure' % dest_path
    third_party_dest_path = '%s/third-party' % dest_path
    local('rm -rf %s' % dest_path, capture=False)
    local('mkdir -p %s' % path, capture=False)
    
    with cd(path):
        local('svn checkout http://closure-library.googlecode.com/svn/trunk/ .', capture=False)
        local('mkdir -p ../../%s' % closure_dest_path, capture=False)
        local('mkdir -p ../../%s' % third_party_dest_path, capture=False)
        local('ln -s %s/closure/goog/ ../../%s/goog' % (abs_path, closure_dest_path))
        local('ln -s %s/closure/css/ ../../%s/css' % (abs_path, closure_dest_path))
        local('ln -s %s/third_party/closure/goog/ ../../%s/goog' % (abs_path, third_party_dest_path))
        

def _install_closure_compiler(root="tools", dir_name="closure-compiler"):
    """Downloads Closure js compiler to specified root path

    @Pre: root and dir_name exist
    """
    #
    # Gets closure templates using latest Zip
    path = '%s/%s' % (root, dir_name)
    local('mkdir -p %s' % path)
    with cd(path):
        local('wget http://closure-compiler.googlecode.com/files/compiler-latest.zip', capture=False)
        local('unzip compiler-latest.zip', capture=False)
        local('rm compiler-latest.zip', capture=False)

