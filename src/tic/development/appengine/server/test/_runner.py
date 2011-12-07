import os.path

import doctest
import logging
import os
import tic
import unittest
from tic.utils import importlib
def get_unit_tests(args=None):
    
    if not args:
        files = tic.loader.locate("*.py")
        
    elif _is_args_dir(args):
        files = tic.loader.locate("*.py", 
            root=os.path.join(os.curdir, _convert_module_to_path(args)))
    elif _is_args_module(args):
        module = _is_args_module(args)
        module_suites = unittest.defaultTestLoader.loadTestsFromModule(module)
        if module_suites.countTestCases():
            return [module_suites]
    elif _is_args_TestCase(args):
        return [unittest.defaultTestLoader.loadTestsFromTestCase(_is_args_TestCase(args))]
    else:
        #maybe its a method?
        testcase = unittest.defaultTestLoader.loadTestsFromName(args)
        return [testcase]
#        raise Exception('Cant find test: %s' % args)
        
    suites = []
    for file in files:
        p = "%s%s" % (os.path.join(os.path.abspath(os.curdir), "lib"), os.sep)
        if file.startswith(p):
            continue
        module_name = tic.loader._get_module_name(file)
        module = importlib.import_module(module_name)
        module_suites = unittest.defaultTestLoader.loadTestsFromModule(module)
        try:
            module_suites.addTests(doctest.DocTestSuite(module))
        except:
            pass
        if not module_suites.countTestCases():
            continue
        suites.append(module_suites)
    
    return suites

def _is_args_TestCase(args):
    module_name, TestCase = args.rsplit('.', 1)
    module = _is_args_module(module_name)
    if module and hasattr(module, TestCase):
        return getattr(module, TestCase)
    return False

def _is_args_module(args):
    try:
        module = importlib.import_module(args)
        return module
    except:
        return None
    
    

def _is_args_dir(args):
    if args:
        dir = os.path.join(os.curdir, _convert_module_to_path(args))
        return os.path.isdir(dir)
    return False

def _convert_module_to_path(module):
    """
    converts 'a.b.c' to 'a/b/c'
    """
    return module.replace('.', os.sep)

def run(args):
    """
    Runs all the unit tests available
    """
    os.environ['APPLICATION_ID'] = "tic-testing-framework"
    os.environ['AUTH_DOMAIN'] = 'localhost'
    os.environ['SERVER_SOFTWARE'] = 'Development/1.0 (AppEngineTest)'
    logging.basicConfig(level=logging.DEBUG)
    
    t = unittest.TestSuite()
    for suite in get_unit_tests(args):
        if hasattr(suite, "_tests"):
            t.addTests(suite._tests)
        else:
            t.addTests([suite])
    unittest.TextTestRunner(verbosity=1).run(t)

if __name__ == '__main__':
    run()

