from google.appengine.ext import db

from tic.admin.shell.shell import INITIAL_UNPICKLABLES, Session
from tic.core import Component, implements
from tic.web.cdp import Command, StringProperty
from tic.web.cdp.api import ICommandHandler

class ExecuteCommand(Command):
    """
    Documentation
    """
    statement = StringProperty()

class ExecuteCommandResult(Command):
    """
    Documentation
    """
    result = StringProperty()


class ExecuteCommandHanlder(Component):
    """
    
    """
    implements(ICommandHandler)

    command = ExecuteCommand

    def execute(self, command):
        """

        """
#        # set up the session. TODO: garbage collect old shell sessions
#        session_key = self.req.session
#        if session_key:
#            session = Session.get(session_key)
#        else:
#            # create a new session
#            session = Session()
#            session.unpicklables = [db.Text(line) for line in INITIAL_UNPICKLABLES]
#            session_key = session.put()
#

        result = ExecuteCommandResult()
        result.result = "sweet"
        return result