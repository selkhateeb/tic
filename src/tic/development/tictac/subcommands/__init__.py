# __init__.py

from runserver import ServerCommand

__all__ = ('TestCommand', 'ServerCommand')

class TestCommand(object):
    def __init__(self, subparsers=None):
        """TestCommand
        
        Arguments:
        - `self`:
        - `subparsers`:
        """
        self.parser = subparsers.add_parser('test',
                                            help='this is awesome!!',
                                            )
        self.parser.set_defaults(func=self.run)


    @staticmethod
    def run(args):
        """Runs the test command
        
        """
        print args
        print 'awesome!!!'

