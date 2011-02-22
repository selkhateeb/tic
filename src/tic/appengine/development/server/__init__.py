from time import sleep

import os
from threading import Thread
from tic.admin.api import IAdminCommandProvider
from tic.core import Component, implements
from tic.tools.directory_watcher import DirectoryWatcher
from tic import loader

class ServerCommand(Component):
    implements(IAdminCommandProvider)

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
        root = '/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine/'
        sys.path.append(root)
        sys.path.append(root + "lib/antlr3/")
        sys.path.append(root + "lib/fancy_urllib/")
        sys.path.append(root + "lib/ipaddr/")
        sys.path.append(root + "lib/webob/")
        sys.path.append(root + "lib/yaml/lib/")
        from google.appengine.dist import use_library
        use_library('django', '1.2')

        directory_watcher = DirectoryWatcher(self.compmgr)
        directory_watcher.watch(loader.root_path())
        progname = sys.argv[0]
        args = ['--enable_sendmail']
        # hack __main__ so --help in dev_appserver_main works.
        sys.modules['__main__'] = dev_appserver_main
        sys.exit(dev_appserver_main.main([progname] + args + [os.getcwdu()]))