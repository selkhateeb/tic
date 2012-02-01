import sys
import os
import fnmatch


def application_paths(sys_path=sys.path):
    return [path for path in sys_path if path.startswith('/Users/')]

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


