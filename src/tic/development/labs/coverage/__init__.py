
import commands
import os
import logging
from tic import loader
from tic.core import Component, implements
from tic.development.admin.api import IAdminCommandProvider
from tic.development.tools.api import IRunServerTask

#TODO: Move to settings
NODE_EXECUTABLE = 'node'
NODE_SCRIPT = os.path.join(loader.root_path(),__name__.replace('.', '/'), 'main.js')
INSTRUMENTED_CODE_PATH = os.path.join(loader.root_path(), 'instrumented')

def generate_instrumented_file(js_file):
    logging.info('Generating instrumentation code for [%s]' % js_file)
    command = ' '.join([NODE_EXECUTABLE, NODE_SCRIPT, js_file])
    instrumented = commands.getoutput(command)
    
    destination, filename = os.path.join(INSTRUMENTED_CODE_PATH, 
                                     loader.get_relative_path(js_file)).rsplit('/',1)
    
    if not os.path.exists(destination):
        os.makedirs(destination)
    
    file = open(os.path.join(destination, filename), 'w')
    file.write(instrumented)
    file.close()
    logging.info('done...')

class CoverageCommand(Component):
    implements(IAdminCommandProvider, IRunServerTask)

    def get_admin_commands(self):
        """
        Returns a list of commands to execute
        @see tic.admin.api.IAdminCommandProvider
        """

        #(command, args, help, complete, execute)
        return (
                ("tc", None, "have fun", None, self.run),
                )

    def run(self):
        for f in loader.locate('*_test.js'):
            #TODO: find a way not to skip entrypoint for now
            #      wich causes a more than one entrypoint defined   
            if not 'entrypoint' in f:
                generate_instrumented_file(f.replace('_test.js', '.js'))
