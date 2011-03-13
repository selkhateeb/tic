from tic import loader
from tic.core import Component, implements
from tic.tools.api import IDirectoryWatcher, IRunServerTask, IBuildTask
from tic.utils import importlib
from tic.web import cdp
import logging
import os
import shutil
import types

class HandleSharedClasses(Component):
    implements(IRunServerTask, IDirectoryWatcher, IBuildTask)

    def __init__(self):
        self.generated_path = "%sgenerated/client/closure/" % loader.root_path()

    #---------------
    # IRunSererTask and IBuildTask implementation
    #---------------
    def run(self, build_path=None):
        
        logging.info('Generating shared js classes:')
        commands = self._get_shared_commands()
        self._prepare_generated_path()

        for command in commands:
            logging.info('\t%s.%s.js' % (command.__module__, command.__name__))
            self._generate_file_for_class(command)
            
    #----------------
    # IDirectoryWatcher implementation
    #   -changed
    #   -created
    #   -deleted
    #----------------
    def changed(self, changed_files):
        """
        changed_files: list of paths to changed files
        """
        for shared_file in changed_files:
            if '/shared.py' in shared_file:
                for command in self._get_shared_commands_for_file(shared_file):
                    self._generate_file_for_class(command)

    def created(self, created_files):
        """
        created_files: list of paths to newly created files
        """
        self.changed(created_files)

    def deleted(self, deleted_files):
        """
        deleted_files: list of paths to removed files

        TODO: This is the tricky one.. we need to delete the generated closure
        class files.

        Implementation Idea: since this is a singleton class we can keep the
        state in a variable and use it to clean up ..

        """
    

    def _get_shared_commands(self):
        shared_files = loader.locate('shared.py')
        commands = set()
        for file in shared_files:
            commands.update(self._get_shared_commands_for_file(file))

        return commands

    def _get_shared_commands_for_file(self, file):
        commands = []
        module_name = loader._get_module_name(file)
        module = importlib.import_module(module_name)
        for name in dir(module):
            obj = getattr(module, name)
            if (isinstance(obj, (type, types.ClassType)) and
                issubclass(obj, cdp.Command)):
                commands.append(obj)
        return commands

    def _generate_file_for_class(self, command_class):
        filename = '%s.%s' % (command_class.__module__, command_class.__name__)
        file = open('%s%s.js' % (self.generated_path, filename), "w")
        file.write(command_class('closure').to_js())
        file.close()

    def _prepare_generated_path(self):
        try:
            shutil.rmtree(self.generated_path)
        except OSError:
            pass #no such file or dir
        os.makedirs(self.generated_path)
