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
        self.add_parser.add_argument('option')
        self.add_parser.add_argument('value', nargs='?', default='')
        
        self.add_parser.set_defaults(func=self.add)
        

        self.remove_parser = self.subparsers.add_parser('remove',
                                                        help='Removes a configuration option')
        self.remove_parser.set_defaults(func=self.remove)
        self.remove_parser.add_argument('section')
        self.remove_parser.add_argument('option', nargs='?', default='')

        self.get_parser = self.subparsers.add_parser('get',
                                                        help='Gets a configuration option')
        self.get_parser.set_defaults(func=self.get)
        self.get_parser.add_argument('section')
        self.get_parser.add_argument('option', nargs='?', default='')

    @staticmethod
    def add(args, config):
        """
        - `args`: args passed
        - `config`: configuration object
        """

        if not config.has_section(args.section):
            config.add_section(args.section)
        config.set(args.section, args.option, args.value)
        config.write()
        

    @staticmethod
    def remove(args, config):
        """
        - `args`: args passed
        - `config`: configuration object
        """
        if args.option:
            config.remove_option(args.section, args.option)
        else:
            config.remove_section(args.section)
        config.write()


    @staticmethod
    def get(args, config):
        """
        - `args`: args passed
        - `config`: configuration object
        """
        if args.option:
            print config.get(args.section, args.option)
        else:
            print '\n'.join(config.options(args.section))
