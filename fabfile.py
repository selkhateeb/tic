from __future__ import with_statement
from os import mkdir

from fabric.api import *

def runserver():
    local('dev_appserver.py src --enable_sendmail', capture=False)

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
    """Downloads Closure templates js compiler to specified root path

    @Pre: root and dir_name exist
    """

    #TODO: use git instead of svn
    #
    # Gets closure templates using latest Zip
    path = '%s/%s' % (root, dir_name)
    local('mkdir -p %s' % path)
    with cd(path):
        local('svn checkout http://closure-library.googlecode.com/svn/trunk/ .', capture=False)

def _install_closure_compiler(root="tools", dir_name="closure-compiler"):
    """Downloads Closure templates js compiler to specified root path

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

