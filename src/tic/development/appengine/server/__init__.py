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
]

import sys
sys.path[1:1] = APPENGINE_LIBS
from google.appengine.dist import use_library
use_library('django', '1.2')

from time import sleep
import os
from threading import Thread
from tic.development.admin.api import IAdminCommandProvider
from tic.core import Component, implements, ExtensionPoint
from tic.development.tools.directory_watcher import DirectoryWatcher
from tic.development.tools.api import IRunServerTask
from tic import loader
from symbol import except_clause
import logging



class ServerCommand(Component):
    implements(IAdminCommandProvider)

    pre_tasks = ExtensionPoint(IRunServerTask)

    def get_admin_commands(self):
        """
        Returns a list of commands to execute
        @see tic.admin.api.IAdminCommandProvider
        """

        #(command, args, help, complete, execute)
        return (
                ("runserver", None, "runs the server", None, self._runserver),
                )

    def _runserver(self):
        import sys
        from google.appengine.tools import dev_appserver_main
        from google.appengine.tools import dev_appserver_import_hook
        print dev_appserver_import_hook.FakeFile.NOT_ALLOWED_DIRS
        root = '/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine/'
        sys.path.append(root)
        sys.path.append(root + "lib/antlr3/")
        sys.path.append(root + "lib/cacerts/")
        sys.path.append(root + "lib/ipaddr/")
        sys.path.append(root + "lib/graphy/")
        sys.path.append(root + "lib/ipaddr/")
        sys.path.append(root + "lib/protorpc/")
        sys.path.append(root + "lib/simplejson/")
        sys.path.append(root + "lib/webapp2/")
        sys.path.append(root + "lib/webob/")
        sys.path.append(root + "lib/yaml/lib/")
#        sys.path.append(root + "lib/whoosh/")
        from google.appengine.dist import use_library
        use_library('django', '1.2')
        
        try:
            for task in self.pre_tasks:
                task.run()
        except Exception, e:
            logging.error(e)
            sys.exit(1)
        
        progname = sys.argv[0]
        args = ['--enable_sendmail']
        # hack __main__ so --help in dev_appserver_main works.
        sys.modules['__main__'] = dev_appserver_main
        sys.exit(dev_appserver_main.main([progname] + args + [os.getcwdu()]))

class StartWatchingForDirectoryChangesTask(Component):
    implements(IRunServerTask)

    def run(self):
      '''run '''
      directory_watcher = DirectoryWatcher(self.compmgr)
      directory_watcher.watch(loader.root_path())
