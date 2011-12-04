from tic.admin.api import IAdminCommandProvider
from tic.core import Component, implements
from tic.tools.api import IRunServerTask, IBuildTask
from tic.web import closure

class ClosureCommand(Component):
  implements(IAdminCommandProvider, IRunServerTask)

  #IAdminCommandProvider implementation
  def get_admin_commands(self):
    """
    Returns a list of commands to execute
    @see tic.admin.api.IAdminCommandProvider
    """
    return (
            ("compile_closure_templates", None, "Compiles all closure template files (.soy)", None, self._run),
                ("compile_closure_js", None, "Compiles all closure js files", None, self._compile_closure),
            
            )
  
  #IRunServerTask
  def run(self, build_path=None):
    """
    Runs the closure templates compiler
    """
    if build_path:
      self._run()
      self._compile_closure()
    else:            
      self._run()
    
  def _run(self):
    closure.prepare_generated_directory()
    if closure.compile_soy_templates(): #if we have templates copy the required js files
        closure.copy_required_js_files()
           
  def _compile_closure(self):
    closure.compile_closure_files()
