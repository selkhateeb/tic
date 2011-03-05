import logging
import os
import shutil
import types
import uuid
from tic import loader
from tic.core import Component, implements
from tic.tools.api import IRunServerTask
from tic.utils import importlib
from tic.web import cdp

class GenerateClosureSharedClasses(Component):
    implements(IRunServerTask)

    def run(self):
        shared_files = loader.locate('shared.py')
        commands = set()
        for file in shared_files:
            module_name = loader._get_module_name(file)
            module = importlib.import_module(module_name)
            for name in dir(module):
                obj = getattr(module, name)
                if (isinstance(obj, (type, types.ClassType)) and
                    issubclass(obj, cdp.Command)):
                    commands.add(obj)

        generated_path = "%sgenerated/client/closure/" % loader.root_path()
        try:
            shutil.rmtree(generated_path)
        except OSError:
            pass #no such file or dir
        
        os.makedirs(generated_path)

        logging.info('Generating shared js classes:')
        for command in commands:
            filename = '%s.%s' % (command.__module__, command.__name__)
            logging.info('\t<%s>' % filename)
            file = open('%s%s.js' % (generated_path, filename), "w")
            file.write(command('closure').to_js())
            file.close()
            

            