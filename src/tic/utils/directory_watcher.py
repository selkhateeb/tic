import time
import os

import logging
from tic.admin.api import IAdminCommandProvider
from tic.core import Component, implements
from tic import loader


def watch_directories (paths, func, delay=1.0):
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
                changed_list.append(path)

            # Record current mtime of file.
            all_files[path] = t.st_mtime

    # Main loop
    rescan = False
    while True:
        changed_list = []
        remaining_files = all_files.copy()
        all_files = {}
        for path in paths:
            os.path.walk(path, f, None)
        removed_list = remaining_files.keys()
        if rescan:
            rescan = False
        elif changed_list or removed_list:
            rescan = func(changed_list, removed_list)

        time.sleep(delay)

if __name__ == '__main__':
    def f (changed_files, removed_files):
        print changed_files
        print 'Removed', removed_files

    watch_directory('.', f, 1)

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
        def f(changed, removed):
            for f in changed:
                logging.info('changed:%s', f)
            for f in removed:
                logging.info('removed:%s', f)
            return True
                
        watch_directories([loader.root_path()], f, 1)
