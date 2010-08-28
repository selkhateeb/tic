import sys

import cStringIO
import logging
import new
import traceback
from google.appengine.ext import db
from tic.admin.shell.models import INITIAL_UNPICKLABLES, Session, UNPICKLABLE_TYPES
from tic.core import Component, implements
from tic.utils.simplejson import dumps
from tic.web.cdp import Command, StringProperty
from tic.web.cdp.api import ICommandHandler
from tic.web.rpc.api import CustomJsException

class ExecuteCommand(Command):
    """
    Contains the statement to execute
    """
    statement = StringProperty()

class ExecuteCommandResult(Command):
    """
    Contains the result of the execution
    """
    result = StringProperty()


class ExecuteCommandHanlder(Component):
    """
    Handles the execute command execution
    """
    implements(ICommandHandler)

    command = ExecuteCommand

    def _get_session(self):
        """
        gets the session instance or creates a new one if it does not exist

        Returns:
            Session: session object
        """
        # set up the session. TODO: garbage collect old shell sessions
        try:
            session_key = self.request.session['execution_session']
            session = Session.get(session_key)
        except KeyError:
            # create a new session
            session = Session()
            session.unpicklables = [db.Text(line) for line in INITIAL_UNPICKLABLES]
            session_key = session.put()
            self.request.session['execution_session'] = session_key

        return session

    def _compile(self, statement):
        """
        compiles the statement

        Args:
            statement: a string containing a python statement

        Returns:
            the compiled object

        """
        statement = statement.replace("\r\n", "\n")
        compiled = compile(statement, '<stdin>', 'single')
        return compiled

    def _prepare_execution_module(self, session):
        # create a dedicated module to be used as this statement's __main__
        statement_module = new.module('__main__')

        # use this request's __builtin__, since it changes on each request.
        # this is needed for import statements, among other things.
        import __builtin__
        statement_module.__builtins__ = __builtin__

        sys.modules['__main__'] = statement_module
        statement_module.__name__ = '__main__'

        # re-evaluate the unpicklables
        for code in session.unpicklables:
            exec code in statement_module.__dict__

        # re-initialize the globals
        for name, val in session.globals_dict().items():
            try:
                statement_module.__dict__[name] = val
            except:
                msg = 'Dropping %s since it could not be unpickled.\n' % name
                session.remove_global(name)
                raise

        # use this request's __builtin__, since it changes on each request.
        # this is needed for import statements, among other things.
        import __builtin__
        statement_module.__builtins__ = __builtin__

        sys.modules['__main__'] = statement_module
        statement_module.__name__ = '__main__'
        # re-evaluate the unpicklables
        for code in session.unpicklables:
            exec code in statement_module.__dict__

        # re-initialize the globals
        for name, val in session.globals_dict().items():
            try:
                statement_module.__dict__[name] = val
            except:
                msg = 'Dropping %s since it could not be unpickled.\n' % name
                session.remove_global(name)
                raise

        return statement_module

    def _run(self, compiled, statement_module, results_io):
        # run!
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        try:
            sys.stdout = results_io
            sys.stderr = results_io
            exec compiled in statement_module.__dict__
        except Exception, e:
            eval(compiled, statement_module.__dict__)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    def _prepare_session_after_execution(self, statement_module, old_globals, session):
        # extract the new globals that this statement added
        new_globals = {}
        for name, val in statement_module.__dict__.items():
            if name not in old_globals or val != old_globals[name]:
                new_globals[name] = val

        if True in [isinstance(val, UNPICKLABLE_TYPES)
            for val in new_globals.values()]:
        # this statement added an unpicklable global. store the statement and
            # the names of all of the globals it added in the unpicklables.
            session.add_unpicklable(statement, new_globals.keys())
            logging.debug('Storing this statement as an unpicklable.')

        else:
            # this statement didn't add any unpicklables. pickle and store the
            # new globals back into the datastore.
            for name, val in new_globals.items():
                if not name.startswith('__'):
                    session.set_global(name, val)

    def execute(self, command):
        """
        ICommandHandler API function
        """
        session = self._get_session()
        try:
            compiled = self._compile(command.statement)
        except:
            self._log_error()
        
        results_io = cStringIO.StringIO()


        # swap in our custom module for __main__. then unpickle the session
        # globals, run the statement, and re-pickle the session globals, all
        # inside it.
        old_main = sys.modules.get('__main__')
        try:
            statement_module = self._prepare_execution_module(session)
            old_globals = dict(statement_module.__dict__)
            self._run(compiled, statement_module, results_io)
            self._prepare_session_after_execution(statement_module, old_globals, session)
        except:
            self._log_error()
        finally:
            sys.modules['__main__'] = old_main
        
        session.put()
        results = results_io.getvalue()
        result = ExecuteCommandResult()
        result.result = results
        return result

    def _log_error(self):
        exc_type, value, tb = sys.exc_info()
        tblist = traceback.extract_tb(tb)
        message = traceback.format_list(tblist)
        del message[:2]
        if message:
            # we don't print the 'Traceback...' part for SyntaxError
            message.insert(0, "Traceback (most recent call last):\n")

        message.extend(traceback.format_exception_only(exc_type, value))
        raise CustomJsException("console.warn(%s)" % dumps(''.join(message)))

