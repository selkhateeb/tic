from tic.admin.api import IAdminCommandProvider
from tic.core import Component, implements
from tic.tools.api import IRunServerTask
from tic.web import closure

class ClosureCommand(Component):
    implements(IAdminCommandProvider, IRunServerTask)


    def get_admin_commands(self):
        """
        Returns a list of commands to execute
        @see tic.admin.api.IAdminCommandProvider
        """
        return (
                ("compile_closure_templates", None, "Compiles all closure template files (.soy)", complete, self._run),
                )

    #IRunServerTask
    def run(self):
        """
        Runs the closure templates compiler
        """
        self._run()
        
    def _run(self):
        closure.prepare_generated_directory()
        if closure.compile_soy_templates(): #if we have templates copy the required js files
            closure.copy_required_js_files()
