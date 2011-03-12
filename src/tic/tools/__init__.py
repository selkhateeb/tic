import logging
from tic.admin.api import IAdminCommandProvider
from tic.core import Component, implements, ExtensionPoint
from tic.tools.api import IBuildTask
class BuildTaskRunner(Component):
    implements(IAdminCommandProvider)
    '''Provides a command line option to runs all defined build tasks
    '''
    
    tasks = ExtensionPoint(IBuildTask)
    
    #---------------------
    # IAdminCommandProvider implementation
    #---------------------
    def get_admin_commands(self):
        return (('build', None, "Builds the application", None, self._execute),
                )
        
    
    #--------------------
    # Private Logic
    #--------------------
    def _execute(self):
        logging.info('Running build tasks...')
        for task in self.tasks:
            task.run()
        logging.info('Done.')