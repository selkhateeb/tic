import time
#from multiprocessing import Process
import logging
import threading
import os
from tic import loader
from tic.development.admin.api import IAdminCommandProvider
from tic.core import Component, ExtensionPoint, implements
from tic.development.tools.api import IDirectoryWatcher

class DirectoryWatcher(Component):

    directory_watchers = ExtensionPoint(IDirectoryWatcher)
        
    def watch(self, path, delay=1):
        """
        starts watching the provided path
        """
        p = threading.Thread(target=watch_directories, args=([loader.root_path()],self.__watcher__,delay))
        p.start()
    
    def __watcher__(self, created, changed, deleted):
        """
        
        """
        logging.info(len(self.directory_watchers))
        for directory_watcher in self.directory_watchers:
            if hasattr(directory_watcher, 'created') and created:
                directory_watcher.created(created)
            if hasattr(directory_watcher, 'changed') and changed:
                directory_watcher.changed(changed)
            if hasattr(directory_watcher, 'deleted') and deleted :
                directory_watcher.deleted(deleted)
        return True
        
def watch_directories (paths, func, delay=1):
    """(paths:[str], func:callable, delay:float)
    Continuously monitors the paths and their subdirectories
    for changes.  If any files or directories are modified,
    the callable 'func' is called with a list of the modified paths of both
    files and directories.  'func' can return a Boolean value
    for rescanning; if it returns True, the directory tree will be
    rescanned without calling func() for any found changes.
    (This is so func() can write changes into the tree and prevent itself
    from being immediately called again.)
    """
    

    # Basic principle: all_files is a dictionary mapping paths to
    # modification times.  We repeatedly crawl through the directory
    # tree rooted at 'path', doing a stat() on each file and comparing
    # the modification time.

    all_files = {}
    def f (unused, dirname, files):
        # Traversal function for directories
        for filename in files:
            path = os.path.join(dirname, filename)
            try:
                t = os.stat(path)
            except os.error:
                # If a file has been deleted between os.path.walk()
                # scanning the directory and now, we'll get an
                # os.error here.  Just ignore it -- we'll report
                # the deletion on the next pass through the main loop.
                continue

            mtime = remaining_files.get(path)
            if mtime is not None:
                # Record this file as having been seen
                del remaining_files[path]
                # File's mtime has been changed since we last looked at it.
                if t.st_mtime > mtime:
                    changed_list.append(path)
            else:
                # No recorded modification time, so it must be
                # a brand new file.
                created_list.append(path)

            # Record current mtime of file.
            all_files[path] = t.st_mtime

    # Main loop
    rescan = False
    while True:
        changed_list = []
        created_list = []
        remaining_files = all_files.copy()
        all_files = {}
        for path in paths:
            os.path.walk(path, f, None)
        removed_list = remaining_files.keys()
        if rescan:
            rescan = False
        elif changed_list or removed_list:
            rescan = func(created_list, changed_list, removed_list)

        time.sleep(delay)


class DirectoryWatcherCommand(Component):
    implements(IAdminCommandProvider)

    def get_admin_commands(self):
        """
        Returns a list of commands to execute
        @see tic.admin.api.IAdminCommandProvider
        """

        #(command, args, help, complete, execute)

        return (
                ("watch", None, "Watchs directory for changes", None, self._watch),
                )

    def _watch(self):
        """
        TODOC 
        """
        logging.info('Watching directry for changes...')
        def f(created, changed, removed):
            for f in created:
                logging.info('created:%s', f)
            for f in changed:
                logging.info('changed:%s', f)
            for f in removed:
                logging.info('removed:%s', f)
            return True
                
        watch_directories([loader.root_path()], f, 1)

class SimpleDirectoryChangeLogger(Component):
    implements(IDirectoryWatcher)

    def changed(self, list):
        logging.info(list)

    def created(self, list):
        self.changed(['created'] + list)

    def deleted(self, list):
        self.changed(['deleted'] + list)
