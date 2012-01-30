"""Manages the configuration for a tic project
"""


class ConfigCommand(object):
    def __init__(self, **kwargs):
        """
        Arguments:
        - `**kwargs`:
        """
        subparsers = kwargs.get('subparsers')
        
        self.parser = subparsers.add_parser('config',
                                            help='Configure your tic project')

        self.subparsers = self.parser.add_subparsers()

        self.add_parser = self.subparsers.add_parser('add',
                                                     help='Adds a configuration option')

        self.add_parser.add_argument('section')
        self.add_parser.add_argument('key')
        self.add_parser.add_argument('value')
        
        self.add_parser.set_defaults(func=self.add)
        

        self.remove_parser = self.subparsers.add_parser('remove',
                                                        help='Removes a configuration option')
        self.remove_parser.set_defaults(func=self.remove)

    @staticmethod
    def add(args, config):
        """
        - `args`: args passed
        - `config`: configuration object
        """
        print 'adding'
        #todo: verify that the seciton exists 
        #config.add_section(args.section)
        config.set(args.section, args.key, args.value)
        config.write()
        print args

    @staticmethod
    def remove(args, config):
        """
        - `args`: args passed
        - `config`: configuration object
        """
        print 'removing'        
