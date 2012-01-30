# __init__.py

from runserver import ServerCommand
from init import InitCommand
__all__ = ('TestCommand', 'ServerCommand', 'InitCommand')

class TestCommand(object):
    def __init__(self, **kwargs):
        subparsers = kwargs.get('subparsers')
        self.config = kwargs.get('config')
        
        self.parser = subparsers.add_parser('test',
                                            help='this is awesome!!',
                                            )
        self.parser.set_defaults(func=self.run)
        

    @staticmethod
    def run(args, config):
        """Runs the test command
        
        """
        print 'awesome!!!'

