import os.path
#! /usr/bin/env python

import logging
import os
import unittest

import sys
sys.path.append(os.path.join(os.path.abspath(os.curdir),'../src/'))

import tic.utils.importlib

MODULE_EXTENSIONS = set('.py'.split())

def relpath(path, start=os.curdir):
    """Return a relative version of a path"""
    
    if not path:
        raise ValueError("no path specified")
    start_list = os.path.abspath(start).split(os.sep)
    path_list = os.path.abspath(path).split(os.sep)
    if start_list[0].lower() != path_list[0].lower():
        unc_path, rest = splitunc(path)
        unc_start, rest = splitunc(start)
        if bool(unc_path) ^ bool(unc_start):
            raise ValueError("Cannot mix UNC and non-UNC paths (%s and%s)"
                                                                % (path, start))
        else:
            raise ValueError("path is on drive %s, start on drive %s"
                                                % (path_list[0], start_list[0]))
    # Work out how much of the filepath is shared by start and path.
    for i in range(min(len(start_list), len(path_list))):
        if start_list[i].lower() != path_list[i].lower():
            break
    else:
        i += 1

    rel_list = [os.pardir] * (len(start_list)-i) + path_list[i:]
    if not rel_list:
        return os.curdir
    return os.path.join(*rel_list)

def unit_test_extractor(tup, path, filenames):
    """Pull ``unittest.TestSuite``s from modules in path
    if the path represents a valid Python package. Accumulate
    results in `tup[1]`.
    """
    package_path, suites = tup
    logging.debug('Path: %s', path)
    logging.debug('Filenames: %s', filenames)
    rel_path = relpath(path, package_path)
    relpath_pieces = rel_path.split(os.sep)

    if relpath_pieces[0] == '.': # Base directory.
        relpath_pieces.pop(0) # Otherwise, screws up module name.
    elif not any(os.path.exists(os.path.join(path, '__init__' + ext))
            for ext in MODULE_EXTENSIONS):
        return # Not a package directory and not the base directory, reject.

    logging.info('Base: %s', '.'.join(relpath_pieces))
    for filename in filenames:
        base, ext = os.path.splitext(filename)
        if ext not in MODULE_EXTENSIONS: # Not a Python module.
            continue
        logging.info('Module: %s', base)
        module_name = '.'.join(relpath_pieces + [base])
        logging.info('Importing from %s', module_name)
        module = tic.utils.importlib.import_module(module_name)
        module_suites = unittest.defaultTestLoader.loadTestsFromModule(module)
        logging.info('Got suites: %s', module_suites)
        if not module_suites.countTestCases():
            continue
        suites.append((module_name, module_suites))
        
def init_appengine_path():
    """
    TODOC
    """
    root = '/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine/'
    sys.path.append(root)
    sys.path.append(root + "lib/antlr3/")
    sys.path.append(root + "lib/django/django/")
    sys.path.append(root + "lib/fancy_urllib/")
    sys.path.append(root + "lib/ipaddr/ipaddr/")
    sys.path.append(root + "lib/webob/webob/")
    sys.path.append(root + "lib/yaml/lib/")
    

def get_test_suites(path):
    """:return: Iterable of suites for the packages/modules
    present under :param:`path`.
    """
    init_appengine_path()
    logging.info('Base path: %s', package_path)
    suites = []
    os.path.walk(package_path, unit_test_extractor, (package_path, suites))
    logging.info('Got suites: %s', suites)
    return suites


if __name__ == '__main__':
    os.environ['APPLICATION_ID'] = "tic-testing-framework"
    os.environ['AUTH_DOMAIN'] = 'localhost'
    os.environ['SERVER_SOFTWARE'] = 'Development/1.0 (AppEngineTest)'
    logging.basicConfig(level=logging.WARN)
    package_path = os.path.dirname(os.path.abspath(__file__))
    suites = get_test_suites(package_path)
    for module_name, suite in suites:
        unittest.TextTestRunner(verbosity=2).run(suite)