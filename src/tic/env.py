# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2009 Edgewall Software
# Copyright (C) 2003-2007 Jonas Borgström <jonas@edgewall.com>
# All rights reserved.
#


from tic.core import Component, ComponentManager, ExtensionPoint, Interface, implements

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


        from tic.loader import load_components
        load_components(self)
        