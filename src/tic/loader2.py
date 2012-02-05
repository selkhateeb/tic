import sys
import os
import fnmatch
import logging

def application_paths(sys_path=sys.path):
    return set([path for path in sys_path if path.startswith('/Users/')])

def locate(pattern, paths=application_paths()):
    
    files = []
    for path in paths:
        files += _locate(pattern, path)
    return files


def _locate(pattern, path, walk=os.walk):
    """Locate all files matching supplied filename pattern in and below
    supplied root directory."""
    filelist = []
    for root, dirs, files in walk(path, followlinks=True):
        filelist += [os.path.join(root, filename) for filename in fnmatch.filter(files, pattern)]
    return filelist


def get_relative_path(full_path):
    paths = application_paths()
#    files = [full_path.replace(path, '') for path in paths if path in full_path]
    files = [os.path.relpath(full_path, path) for path in paths if path in full_path]
    if len(files) != 1:
        raise Exception('Cannot find relative path for %s' % full_path)
    return files[0]


def application_path(sys_path=sys.path):
    return sys_path[0]
