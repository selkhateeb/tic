
import os

class InitCommand(object):
    """Handles init command
    """
    
    def __init__(self, **kwargs):
        """
        """
        subparsers = kwargs.get('subparsers')
        self.parser = subparsers.add_parser('init',
                                            help='Initializes the tic project')
        self.parser.set_defaults(func=self.init)
        self.parser.add_argument('dir',
                                 nargs='?',
                                 default='.')

    @staticmethod
    def init(args, config):
        """
        """
        try:
            path = os.path.dirname(config.get_config_file())
            print 'tic project already initialized in %s' % path
            
        except Exception, ex:

            config_file = os.path.join(args.dir, config.config_file)
            path, filename = os.path.abspath(config_file).rsplit(os.sep, 1)
        
            os.makedirs(path)
            project_dir = os.path.abspath(args.dir)
            InitCommand.mkdir_if_not_exist(os.path.join(project_dir, 'src'))
            InitCommand.mkdir_if_not_exist(os.path.join(project_dir, 'docs'))
            InitCommand.mkdir_if_not_exist(os.path.join(project_dir, 'tests'))
            open(config_file, 'w').close()
            print 'Initialized new tic project in %s' % path
        
    @staticmethod    
    def mkdir_if_not_exist(dir):
        """
        """
        if not os.path.exists(dir):
            os.mkdir(dir)
        
        
