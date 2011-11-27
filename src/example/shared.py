from tic.core import Component, implements
from tic.web import cdp
from tic.web.cdp import Command, Result
from tic.web.cdp.api import ICommandHandler
from google.appengine.api import users

class IsLoggedInCommand(Command):
  """
  Handles fetching the data from the database
  """
  user = cdp.StringProperty()
    
class IsLoggedInResult(Result):
  """
  Documentation
  """
  result = cdp.IntegerProperty()
    
class IsLoggedInHandler(Component):
  implements(ICommandHandler)

  command = IsLoggedInCommand

  def execute(self, command):
    user = users.get_current_user()
    r = IsLoggedInResult()
    r.result = 1 if user else 0 
    return r
