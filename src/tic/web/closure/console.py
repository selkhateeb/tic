from tic.admin.api import IAdminCommandProvider
from tic.core import Component, implements

class ClosureCommand(Component):
    implements(IAdminCommandProvider)

    def get_admin_commands(self):
        """
        Returns a list of commands to execute
        @see tic.admin.api.IAdminCommandProvider
        """
        
        #(command, args, help, complete, execute)
        command = "kijiji"
        args = None
        help = """test`ing API."""

        complete = None
#        execute = self._execute

        return (
                ("compile_closure_templates", None, "Compiles all closure template files (.soy)", complete, self._compile_closure_templates),
                )

    def _compile_closure_templates(self):
        """
        Runs the closure templates compiler
        """
        from tic.web import closure
        closure.prepare_generated_directory()
        if closure.compile_soy_templates(): #if we have templates copy the required js files
            closure.copy_required_js_files()
