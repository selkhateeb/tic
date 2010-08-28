"""
Shared stuff to satisfy dojo unit tests
"""
from tic.core import Component, implements
from tic.web.cdp import Command, StringProperty
from tic.web.cdp.api import ICommandHandler

class TestSelfReturnedCommand(Command):
    string = StringProperty()

class TestSelfReturnedCommandHanlder(Component):
    """
    the returned result is the the same command
    this is to help in unit testing the round trip of all properties
    """
    implements(ICommandHandler)
    command = TestSelfReturnedCommand
    def execute(self, command):
        return command