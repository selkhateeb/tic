
import commands
import os
import logging
from tic import loader2
from tic.core import Component, implements
from tic.development.admin.api import IAdminCommandProvider
from tic.development.tools.api import IRunServerTask

#TODO: Move to settings
NODE_EXECUTABLE = 'node'
NODE_SCRIPT = os.path.join(os.path.dirname(__file__),__name__.replace('.', '/'), 'main.js')
INSTRUMENTED_CODE_PATH = os.path.join(loader2.application_path().replace('/src', '/tests'), 'instrumented')

def generate_instrumented_file(js_file,
                               node_executable=NODE_EXECUTABLE,
                               node_script=NODE_SCRIPT,
                               instrumented_code_path=INSTRUMENTED_CODE_PATH,
                               get_relative_path=loader2.get_relative_path):
    
    logging.info('Generating instrumentation code for [%s]' % js_file)
    command = ' '.join([node_executable, node_script, js_file])
    instrumented = commands.getoutput(command)
    
    destination, filename = os.path.join(instrumented_code_path, 
                                         get_relative_path(js_file)).rsplit('/',1)
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
