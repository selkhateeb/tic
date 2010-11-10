import doctest
from tic.admin.api import IAdminCommandProvider
from tic.core import Component, implements

class TestCommand(Component):
    implements(IAdminCommandProvider)
    
    def get_admin_commands(self):
        """
        
        """
	#(command, args, help, complete, execute)
        command = "test"
        args = "module.testsuite.test"
        help = """testing API."""
        
        complete = self._complete
        execute = self._execute
        
        return ((command, args, help, complete, execute),)

    def _complete(self, typed_args_list):
        c = []
        from _runner import get_unit_tests
        suites = get_unit_tests()
        for suite in suites:
            for test in suite._tests:
                if isinstance(test, doctest.DocTestCase):
                    #ignore them for now .. should we care?
                    continue
                for t in test._tests:
                    for name in t._testMethodName.split('\n'):
                        c.append("%s.%s.%s" % (t.__module__, t.__class__.__name__, name))
        return c
    
    def _execute(self, args=None):
        from _runner import run
        run(args)
        
    def mmm(self):
        """
        >>> a = 2
        >>> a + 2
        4
        """
