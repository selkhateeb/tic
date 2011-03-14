from tic.admin.api import IAdminCommandProvider
from tic.core import Component, implements, ExtensionPoint
from tic.tools.api import IBuildTask
import logging
import shutil
import os
import yaml
from tic import loader
class BuildTaskRunner(Component):
    implements(IAdminCommandProvider, IBuildTask)
    '''Provides a command line option to runs all defined build tasks
    '''
    
    tasks = ExtensionPoint(IBuildTask)
    
    build_path = 'build'
    #---------------------
    # IAdminCommandProvider implementation
    #---------------------
    def get_admin_commands(self):
        return (('build', None, "Builds the application", None, self._execute),
                )
        
    #--------------------
    # IBuildTask implementation
    #--------------------
    def run(self, build=None):
        '''Cleans and initializes the build directory.
        '''
        try:
            shutil.rmtree(self.build_path)
        except:
            pass
        try:
            os.mkdir(self.build_path)
        except:
            pass
    
    #--------------------
    # Private Logic
    #--------------------
    
    def _execute(self):
        logging.info('Running build tasks...')
        for task in self.tasks:
            task.run(self.build_path)
        logging.info('Done.')
        

class AppYamlGeneratorBuildTask(Component):
    implements(IBuildTask)
    '''Generates the app.yaml file with the proper static files
    '''
    
    app_yaml = 'app.yaml'
    
    #-------------------
    # IBuildTask implementation
    #-------------------
        
    def run(self, build_path):
        '''Gnerates the app.yaml file
        '''
        app = self._read_original_app_yaml_file()
        handlers = app['handlers']
        
        static_dirs = self._get_static_dirs()
        
        insert_index = len(handlers) - 1
        for static_dir in static_dirs:
            handlers.insert(insert_index,
                { 'url': static_dir,
                  'static_dir':static_dir[1:]
                  })

        #add the static root handler
        handlers.insert(len(handlers) - 1,
                        { 'url': '/',
                  'static_files': 'generated/index.html',
                  'upload': 'generated/index.html'
                  })
        
        out = open('%s/app.yaml' % build_path, 'w')
        out.write(yaml.dump(app, default_flow_style=False))
        
    def _read_original_app_yaml_file(self):
        '''Reads and returns the app.yaml file as a yaml objects.
        '''
        return yaml.load(open(self.app_yaml))
    
    def _get_static_dirs(self):
        '''finds all 'client' directories and returns them as list'''
        return [x[1:] for x, dirs, files in loader.walk('.', followlinks=True) if x.endswith('/client')]
    
    
class SettingsPyGeneratorBuildTask(Component):
    implements(IBuildTask)
    '''Generates the settings.py file
    '''
    settings_file = 'settings.py'
    
    def run(self, build_path):
        '''Writes the file
        '''
        out = open('%s/%s' %(build_path, self.settings_file), 'w')
        out.write("JAVASCRIPT_TOOLKIT = 'closure'\n")
        
    
    
