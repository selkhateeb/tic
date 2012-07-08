
#TODO: Refactor this to a config option or auto detect
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
    APPENGINE_LIB_PATH + 'webob_1_1_1/',
    APPENGINE_LIB_PATH + 'yaml/lib/',
    APPENGINE_LIB_PATH + 'fancy_urllib/',
    APPENGINE_LIB_PATH + 'django_1_3/',
]

import sys
import os
import tic
sys.path[1:1] = APPENGINE_LIBS

class ServerCommand:
    def __init__(self, **kwargs):
        subparsers = kwargs.get('subparsers')
        self.parser = subparsers.add_parser('runserver',
                                            add_help=False, # needed for dev_appserver_main --help
                                            prefix_chars='//', #hack so we dont capture '--'
                                            help='Runs Google AppEngine server')
        self.parser.add_argument('args', nargs='*')
        self.parser.set_defaults(func=self.runserver)

    @staticmethod
    def runserver(args, config):

        ServerCommand.pre(config)
        
        from google.appengine.tools import dev_appserver_main

        deps_section = 'deps'
        deps = [ os.path.dirname(os.path.dirname(tic.__file__))] + config.get_project_deps()

        monkey_patch_appengine_setAllowedPaths(deps)
        
        progname = sys.argv[0]
        args = [config.get_project_sources_path()] + args.args
        # hack __main__ so --help in dev_appserver_main works.
        sys.modules['__main__'] = dev_appserver_main
        sys.exit(dev_appserver_main.main([progname] + args ))


    @staticmethod
    def pre(config):
        """runs before runserver
        
        Arguments:
        - `config`:
        """
        from pprint import pprint as p
        p(sys.path)
        import pre
        for func_or_class in pre.__all__:
            fun_cls = getattr(pre, func_or_class)
            fun_cls(config)
        

def monkey_patch_appengine_setAllowedPaths(deps):
    # Monkey patching Google AppEngine
    from google.appengine.tools.dev_appserver_import_hook import FakeFile
    FakeFile.oldSetAllowedPaths = staticmethod(FakeFile.SetAllowedPaths)

    def patchedSetAllowedPaths(root_path, application_paths):
        application_paths += deps

        from google.appengine.tools.dev_appserver_import_hook import FakeFile
        FakeFile.oldSetAllowedPaths(root_path, application_paths)
    
    FakeFile.SetAllowedPaths = staticmethod(patchedSetAllowedPaths)

