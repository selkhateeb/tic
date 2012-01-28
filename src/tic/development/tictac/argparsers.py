#
# experimenting with argparse
# http://docs.python.org/library/argparse.html

import argparse
import subcommands

class CommandLineApplication(object):
    def __init__(self, parser=None):
        """Initilazes the CommandLineApplication
        """
        if not parser:
            parser = argparse.ArgumentParser()

        self.parser = parser
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
        
        
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        epilog="See '%(prog)s COMMAND --help' for more information on a specific command.",
        )
    
    app = CommandLineApplication(parser=parser)

    for command in subcommands.__all__:
        c = getattr(subcommands, command)
        app.add_command(c)

    app.run()
    
