

APPENGINE_PATH = '/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine/'
APPENGINE_LIB_PATH = APPENGINE_PATH + 'lib/'
APPENGINE_LIBS = [
    APPENGINE_PATH,
    APPENGINE_LIB_PATH + 'antlr3/',
    APPENGINE_LIB_PATH + 'cacerts/',
    APPENGINE_LIB_PATH + 'ipaddr/',
    APPENGINE_LIB_PATH + 'graphy/',
    APPENGINE_LIB_PATH + 'ipaddr/',
    APPENGINE_LIB_PATH + 'protorpc/',
    APPENGINE_LIB_PATH + 'simplejson/',
    APPENGINE_LIB_PATH + 'webapp2/',
    APPENGINE_LIB_PATH + 'webob/',
    APPENGINE_LIB_PATH + 'yaml/lib/',
    APPENGINE_LIB_PATH + 'fancy_urllib/',
]

import sys
sys.path[1:1] = APPENGINE_LIBS

# add tic to the path, harcoded for now
sys.path.insert(1, '/Users/selkhateeb/Development/Projects/tic-experiment/tic/src/')

# add the example
sys.path.insert(1, '/Users/selkhateeb/Development/Projects/tic-experiment/example/src/')

#from google.appengine.dist import use_library
#use_library('django', '1.2')

import os
from google.appengine.tools import dev_appserver_main
import logging

class ServerCommand:
    def __init__(self, subparsers=None):
        self.parser = subparsers.add_parser('runserver',
                                            help='Runs Google AppEngine server')
        self.parser.set_defaults(func=self.runserver)

    @staticmethod
    def runserver(args):
        monkey_patch_appengine_setAllowedPaths()
        progname = sys.argv[0]
        args = ['/Users/selkhateeb/Development/Projects/tic-experiment/example/src/']
        # hack __main__ so --help in dev_appserver_main works.
        sys.modules['__main__'] = dev_appserver_main
        sys.exit(dev_appserver_main.main([progname] + args ))

def monkey_patch_appengine_setAllowedPaths():
    # Monkey patching Google AppEngine
    from google.appengine.tools.dev_appserver_import_hook import FakeFile
    FakeFile.oldSetAllowedPaths = staticmethod(FakeFile.SetAllowedPaths)

    def patchedSetAllowedPaths(root_path, application_paths):
        application_paths += ['/Users/selkhateeb/Development/Projects/tic-experiment/tic/src/',
                              '/Users/selkhateeb/Development/Projects/tic-experiment/example/src/']
        from google.appengine.tools.dev_appserver_import_hook import FakeFile
        FakeFile.oldSetAllowedPaths(root_path, application_paths)
    
    FakeFile.SetAllowedPaths = staticmethod(patchedSetAllowedPaths)

