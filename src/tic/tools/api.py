from tic.core import Interface

class IDirectoryWatcher(Interface):
    '''
    Interface for watching deleted files and stuff
    '''

    def changed(self, changed_files):
        """
        changed_files: list of paths to changed files
        """

    def created(self, created_files):
        """
        created_files: list of paths to newly created files
        """

    def deleted(self, deleted_files):
        """
        deleted_files: list of paths to removed files
        """

class IRunServerTask(Interface):
    """Interface for running a task before the server starts
    """

    def run(self):
        """Executes the task
        """
        
class IBuildTask(Interface):
    """Interface for running a build task
    """
    def run(self, build_path):
        """What to do to execute the task"""