#
# experimenting with argparse
# http://docs.python.org/library/argparse.html

import argparse
import os
import ConfigParser
import StringIO

CONFIG_DEFAULTS = """

[project]
generated = generated/client/
tests = tests
instrumented = instrumented

"""

class NoProjectFuondException(Exception):
    pass

class ApplicationConfigurationException(Exception):
    pass

class CommandLineApplication(object):
    def __init__(self, parser=None, config=None):
        """Initilazes the CommandLineApplication
        """
        if not parser:
            parser = argparse.ArgumentParser()

        self.parser = parser
        self.config = config
        self.subparsers = None
        
    def add_command(self, command_class=None):
        """creates an instance of the command_class.

        Creates an instance of the command_class and passes
        it the subparsers object
        """
        if not self.subparsers:
            self._init_subparsers()

        command_class(subparsers=self.subparsers,
                      config=self.config)

    def run(self):
        """Runs the application by parsing the args
        
        """
        args = self.parser.parse_args()
        args.func(args, self.config)


    def _init_subparsers(self):
        """Initilazes the parsers object
        """

        self.subparsers = self.parser.add_subparsers(
            title='Available Commands',
            #description='All available commands',
            #help='alot more help'
            )



class Configuration(ConfigParser.ConfigParser, object):
    """
    """
    
    def __init__(self, config_file=None):
        """
        """
        self.config_file = config_file
        self._reading = False
        self._initialized = False

    def __getattribute__(self, name):
        """Lazy loading of configuration
        
        """
        attr = object.__getattribute__(self, name)


        if not hasattr(attr, '__call__'):
            return attr
        
        if not self._initialized and \
                not self._reading and \
                name in dir(ConfigParser.ConfigParser):
            
            self._load_configurations()
            return attr
        else:
            return attr

    def get_config_file(self):
        """Returns the config file
        """
        return os.path.join(self._get_project_directory(), self.config_file)


    def get_project_deps(self):
        deps = [
            self.get_project_sources_path(),
            os.path.join(self.get_project_path(), self.get('project', 'tests'))
            ]
        if self.has_section('deps'):
            deps += [self.get('deps', option) for option in self.options('deps')]

        return deps


    def get_project_path(self):
        return self._get_project_directory()
    
    def get_project_sources_path(self):
        """Returns the project sources path
        """
        return os.path.join(self._get_project_directory(), 'src')
        

    def _load_configurations(self):
        """Loads the configurations from config files
        """
        self._reading = True

        super(Configuration, self).__init__()
        self.readfp(StringIO.StringIO(CONFIG_DEFAULTS))
        self.read(self.get_config_file())

        self._initialized = True
        self._reading = False
        
    def _get_project_directory(self, path=os.getcwd()):
        """Finds where configuration directory is.
        
        Returns the root project directory
        """

        if self._is_project_dir(path):
            return path

        path = os.path.dirname(path)
        if path != os.sep:
            #recursive call
            return self._get_project_directory(path=path)

        else: #we can't find our project directory
            raise ApplicationConfigurationException(
                'Not a tic project (or any of the parent directories): .tic')

    def _is_project_dir(self, path):
        """Determines wheather this is a project dir or not
        Arguments:
        - `path`: The project path
        """
        if not self.config_file:
            raise ApplicationConfigurationException('Configuration file not specified')
        
        return os.path.exists(os.path.join(path, self.config_file))

    def write(self):
        return super(Configuration, self).write(
            open(self.get_config_file(), 'wb'))
