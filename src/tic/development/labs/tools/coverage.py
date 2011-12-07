import logging
from tic.development.admin.api import IAdminCommandProvider
from tic.core import Component, implements
from tic import loader
from tic.utils.jsparser import parse

class CoverageCommand(Component):
    implements(IAdminCommandProvider)

    def get_admin_commands(self):
        """
        Returns a list of commands to execute
        @see tic.admin.api.IAdminCommandProvider
        """

        #(command, args, help, complete, execute)

        return (
                ("coverage", None, "Generages js coverage reports", None, self._coverage),
                )

    def _coverage(self):
        """
        TODOC
        """
        logging.info('Scanning For Js Files')
        jsfile = "/Users/selkhateeb/Development/Projects/tic/src/example/client/entrypoint.js"
        nodes = parse(file(jsfile).read())
        self._recurse(nodes)

    def _recurse(self, nodes):
        for node in nodes:
            print nodes.funDecls
            print nodes.varDecls
            source = node.getSource()
            self._recurse(node)