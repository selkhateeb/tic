import os.path

import fnmatch
import logging
import os
from tic.utils.importlib import import_module

__all__ = ['load_components', 'locate']

def locate(pattern, root=None):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    if root:
        walker_path = os.path.abspath(root)
    else:
        walker_path = root_path()
    for path, dirs, files in os.walk(walker_path):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)

def root_path():
    mod_path = __name__.replace(".", "/")
    file_path, ext = __file__.rsplit(".", 1)
    if file_path.startswith("./"):
        #fallback to abspath
        file_path = "%s/" % os.path.abspath(os.curdir)
    return file_path.replace(mod_path, '')

def _get_module_name(path):
    """takes an absolute path of a module and returns the fully
    qualified name of the module
    """
    relative_path = path.replace(root_path(), '/')
    # remove __init__.py .. (invalid module name)
#    relative_path = relative_path.replace("__init__.py", '')
    return relative_path[1:-3].replace("/", ".")

    

def load_py_files():
    """Loader that look for Python source files in the plugins directories,
    which simply get imported, thereby registering them with the component
    manager if they define any components.
    """
    def _load_py_files(env, search_path, auto_enable=None):
        import sys
        for path in search_path:
            sys.path.append(os.path.join(path, "lib"))
            plugin_files = locate("*.py", path)
            for plugin_file in plugin_files:
                p = "%s%s" % (os.path.join(path, "lib"), os.sep)
                if plugin_file.startswith(p):
                    continue
                try:
                    plugin_name = os.path.basename(plugin_file[:-3])
                    module_name = _get_module_name(plugin_file)
                    import_module(module_name)
                    _enable_plugin(env, plugin_name)
                except NotImplementedError, e:
                    #print "Cant Implement This"
                    pass


    return _load_py_files



def get_plugins_dir(env):
    """Return the path to the `plugins` directory of the environment."""
    plugins_dir = os.path.realpath(".")
    path = root_path()
    return os.path.normcase(path)

def _enable_plugin(env, module):
    """Enable the given plugin module if it wasn't disabled explicitly."""
    if env.is_component_enabled(module) is None:
        env.enable_component(module)

def load_components(env, extra_path=None, loaders=(load_py_files(),)):
    """Load all plugin components found on the given search path."""
    plugins_dir = get_plugins_dir(env)
    search_path = [plugins_dir]
    if extra_path:
        search_path += list(extra_path)

    for loadfunc in loaders:
        loadfunc(env, search_path, auto_enable=plugins_dir)

