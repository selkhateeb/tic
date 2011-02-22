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