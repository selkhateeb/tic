import os
import urllib2
import zipfile
import logging 

class InstallCommand(object):
    """Handles Install Command
    """
    
    def __init__(self, **kwargs):
        """
        
        Arguments:
        - `**kwargs`:
        """
        subparsers = kwargs.get('subparsers')
        self.parser = subparsers.add_parser('install',
                                            help='Installs all the required libs')
        self.parser.set_defaults(func=self.install)
        #self.parser.add_argument('dir',
        #                         nargs='?',
        #                         default='.')

    @staticmethod
    def install(args, config):
        """
        
        Arguments:
        - `args`:
        - `config`:
        """
        path = make_tic_directory()

        compiler_path = os.path.join(path, 'compiler')
        os.mkdir(compiler_path)
        
        download_closure_compiler(compiler_path)

        templates_path = os.path.join(path, 'templates')
        os.mkdir(templates_path)
        download_closure_templates(templates_path)


def make_tic_directory(tic_directory='.tic'):
    """
    """
    home = os.path.expanduser('~')
    tic = os.path.join(home, tic_directory)
    logging.info('Createing tic directory... %s' % tic)
    os.mkdir(tic)
    return tic
    
def download_closure_compiler(path,
                              closure_compiler_url='http://closure-compiler.googlecode.com/files/compiler-latest.zip'):
    """
    """
    u = urllib2.urlopen(closure_compiler_url)
    filename = os.path.join(path, 'compiler.zip')
    file = open(filename, 'w')
    file.write(u.read())
    file.close()

    zip = zipfile.ZipFile(filename)
    print zip.extractall(path)
    
    
def download_closure_lib():
    """
    """
    
def download_closure_templates(path, url='http://closure-templates.googlecode.com/files/closure-templates-for-javascript-latest.zip'):
    """
    """
    u = urllib2.urlopen(url)
    filename = os.path.join(path, 'templates.zip')
    file = open(filename, 'w')
    file.write(u.read())
    file.close()

    zip = zipfile.ZipFile(filename)
    print zip.extractall(path)
    
