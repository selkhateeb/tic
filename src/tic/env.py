# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2009 Edgewall Software
# Copyright (C) 2003-2007 Jonas Borgström <jonas@edgewall.com>
# All rights reserved.
#


from tic.core import Component, ComponentManager, ExtensionPoint, Interface, implements
from tic.conf import settings
from tic.loader import load_components, locate, _get_module_name
import re

__all__ = ['Environment']

class Environment(Component, ComponentManager):
    """Tic environment manager

    loads all components available in the system
    """
    required = True

    def __init__(self):
        """Initialize the Tic environment.
        """
        ComponentManager.__init__(self)

        self.systeminfo = []

        self._href = self._abs_href = None

        load_components(self)

        self._init_settings()

    def _init_settings(self):
        JavascriptToolkitDetector()

# TODO: make this a component that implements an EnvirnmentConfiguration Interface
class JavascriptToolkitDetector(object):
    def __init__(self):
        self.auto_detect_js_toolkit()

    def auto_detect_js_toolkit(self):
        if settings.JAVASCRIPT_TOOLKIT == 'autodetect':
            files = []
            for file in locate("entrypoint.js"):
                files.append(file)

            if len(files) > 1:
                #TODO: raise EnvironmentException
                raise Exception('More than one entry point defined\n%s' % '\n'.join(files))

            if not len(files):
                #TODO: raise EnvironmentException
                raise Exception('No entry point defined\n')

            if self._is_dojo(files[0]):
                settings.JAVASCRIPT_TOOLKIT = 'dojo' # TODO: enum this

            elif self._is_closure(files[0]):
                settings.JAVASCRIPT_TOOLKIT = 'closure' # TODO: enum this

            #TODO: else:
                

    def _is_dojo(self, file):
        """
        returns true if the javascript file has dojo.provide()
        """
        provide_matcher = re.compile(r'.*\s*dojo\.provide\([\'"](.*)[\'"]\)')
        require_matcher = re.compile(r'.*\s*dojo\.require\([\'"](.*)[\'"]\)')
        return provide_matcher.match(open(file, 'r').read())

    def _is_closure(self, file):
        """
        returns true if the javascript file has goog.provide()
        """
        provide_matcher = re.compile(r'.*\s*goog\.provide\([\'"](.*)[\'"]\)')
        require_matcher = re.compile(r'.*\s*goog\.require\([\'"](.*)[\'"]\)')
        return provide_matcher.match(open(file, 'r').read())
