import os
import sys
import re
from bolacha import Bolacha
from zipfile import ZipFile
from getpass import getpass

def get_csrf_token(bolacha, url):
    '''gets the CSRF token from the form
    '''
    res, content = bolacha.get(url)
    r = re.search("input type='hidden' name='csrfmiddlewaretoken' value='(.+)'", content)    
    return r.group(1)

def login(bolacha, username, password):
    '''Login into readthedocs.org
    '''
    login_data = {
            'username': username,
            'password': password,
            'submit': 'Log in',
            'csrfmiddlewaretoken': get_csrf_token(bolacha, 'http://readthedocs.org/accounts/login/')
            
            }
    res, content = bolacha.post('http://readthedocs.org/accounts/login/', body=login_data)
    print res.status
    print content
    if res.status != 302:
        print content
        raise Exception('Login faild!!')

def upload_file(bolacha, filename):
    '''Uploads the docs file
    '''
    sys.stdout.write('Uploading file ...')
    sys.stdout.flush()
    data = {
        'title': 'Some pictures of my vacations at Rio de Janeiro',
        'overwrite': 'on',
        'version': 'latest',
        'content': open(filename),
        'submit': 'Upload',
        'csrfmiddlewaretoken': get_csrf_token(bolacha, 'http://readthedocs.org/dashboard/upload_html/tic-toolkit/')
        }
    res, content = bolacha.post('http://readthedocs.org/dashboard/upload_html/tic-toolkit/', body=data)
    print res
    print content
    sys.stdout.write('Done ...')
    
def zip(in_dir, outfile):
    '''Builds the docs zipfile
    '''
    sys.stdout.write('Writing zip file...')
    with ZipFile(outfile, 'w') as z:
        for root, subFolders, files in os.walk(in_dir):
            for f in files:
                zipname = os.path.join(root,f).replace(in_dir, '')
                sys.stdout.write('%s\n' % zipname)
                z.write(os.path.join(root, f), zipname)
        z.close()
    sys.stdout.write('\t...done\n')

if __name__ == '__main__':
    '''Main entry point of the application when run from command line
    '''
    b = Bolacha()
    login(b, raw_input('Username:'), getpass('Password:'))
    zip('_build/html/', '_build/latest.zip')
    upload_file(b, '_build/latest.zip')
    

