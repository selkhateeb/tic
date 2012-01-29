#
# experimenting with argparse
# http://docs.python.org/library/argparse.html

import argparse
import os
import ConfigParser

class NoProjectFuondException(Exception):
    pass

class ApplicationConfigurationException(Exception):
    pass

class CommandLineApplication(object):
    def __init__(self, parser=None, config_file=None):
        """Initilazes the CommandLineApplication
        """
        if not parser:
            parser = argparse.ArgumentParser()

        self.parser = parser
        self.config_file = config_file
        self.subparsers = None
        
    def add_command(self, command_class=None):
        """creates an instance of the command_class.

        Creates an instance of the command_class and passes
        it the subparsers object
        """
        if not self.subparsers:
            self._init_subparsers()

        command_class(subparsers=self.subparsers)

    def run(self):
        """Runs the application by parsing the args
        
        """
        args = self.parser.parse_args()
        args.func(args)


    def _init_subparsers(self):
        """Initilazes the parsers object
        """

        self.subparsers = self.parser.add_subparsers(
            title='Available Commands',
            #description='All available commands',
            #help='alot more help'
            )
        
    def load_configurations(self):
        """Loads the configurations from config files
        """
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(self._get_config_file()))

    def _get_config_file(self):
        """Returns the config file
        """
        return os.path.join(self._get_project_directory(), self.config_file)
        
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
    


