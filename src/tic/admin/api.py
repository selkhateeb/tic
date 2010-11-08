# -*- coding: utf-8 -*-
# 
# Copyright (C)2006-2009 Edgewall Software
#

import os.path
import sys
import traceback

from tic.core import *

console_date_format = '%Y-%m-%d'
console_datetime_format = '%Y-%m-%d %H:%M:%S'
console_date_format_hint = 'YYYY-MM-DD'

def _(str):
    """
    hack tell we implement multilanguage
    """
    return str

class AdminCommandError(TicError):
    """Exception raised when an admin command cannot be executed."""
    def __init__(self, msg, show_usage=False, cmd=None):
        TicError.__init__(self, msg)
        self.show_usage = show_usage
        self.cmd = cmd


class IAdminCommandProvider(Interface):
    """Extension point interface for adding commands to the console
    administration interface.
    """
    
    def get_admin_commands():
        """Return a list of available admin commands.
        
        The items returned by this function must be tuples of the form
        `(command, args, help, complete, execute)`, where `command` contains
        the space-separated command and sub-command names, `args` is a string
        describing the command arguments and `help` is the help text. The
        first paragraph of the help text is taken as a short help, shown in the
        list of commands.
        
        `complete` is called to auto-complete the command arguments, with the
        current list of arguments as its only argument. It should return a list
        of relevant values for the last argument in the list.
        
        `execute` is called to execute the command, with the command arguments
        passed as positional arguments.
        """


class AdminCommandManager(Component):
    """tic command manager."""
    
    providers = ExtensionPoint(IAdminCommandProvider)
    
    def get_command_help(self, args=[]):
        """Return help information for a set of commands."""
        commands = []
        for provider in self.providers:
            for cmd in provider.get_admin_commands() or []:
                parts = cmd[0].split()
                if parts[:len(args)] == args:
                    commands.append(cmd[:3])
        commands.sort()
        return commands
        
    def complete_command(self, args, cmd_only=False):
        """Perform auto-completion on the given arguments."""
        comp = []
        for provider in self.providers:
            for cmd in provider.get_admin_commands() or []:
                parts = cmd[0].split()
                plen = min(len(parts), len(args) - 1)
                if args[:plen] != parts[:plen]:         # Prefix doesn't match
                    continue
                elif len(args) <= len(parts):           # Command name
                    comp.append(parts[len(args) - 1])
                elif not cmd_only:                      # Arguments
                    if cmd[3] is None:
                        return []
                    return cmd[3](args[len(parts):]) or []
        return comp
        
    def execute_command(self, *args):
        """Execute a command given by a list of arguments."""
        args = list(args)
        for provider in self.providers:
            for cmd in provider.get_admin_commands() or []:
                parts = cmd[0].split()
                if args[:len(parts)] == parts:
                    f = cmd[4]
                    fargs = args[len(parts):]
                    try:
                        return f(*fargs)
                    except AdminCommandError, e:
                        e.cmd = ' '.join(parts)
                        raise
                    except TypeError, e:
                        tb = traceback.extract_tb(sys.exc_info()[2])
                        if len(tb) == 1:
                            raise AdminCommandError(_("Invalid arguments"),
                                                    show_usage=True,
                                                    cmd=' '.join(parts))
                        raise
        raise AdminCommandError(_("Command not found"), show_usage=True)


class PrefixList(list):
    """A list of prefixes for command argument auto-completion."""
    def complete(self, text):
        return list(set(a for a in self if a.startswith(text)))

        
class PathList(list):
    """A list of paths for command argument auto-completion."""
    def complete(self, text):
        """Return the items in the list matching text."""
        matches = list(set(a for a in self if a.startswith(text)))
        if len(matches) == 1 and not os.path.isdir(matches[0]):
            matches[0] += ' '
        return matches


def get_dir_list(path, dirs_only=False):
    """Return a list of paths to filesystem entries in the same directory
    as the given path."""
    dname = os.path.dirname(path)
    d = os.path.join(os.getcwd(), dname)
    result = PathList()
    try:
        dlist = os.listdir(d)
    except OSError:
        return result
    for entry in dlist:
        path = os.path.join(dname, entry)
        try:
            if os.path.isdir(path):
                result.append(os.path.join(path, ''))
            elif not dirs_only:
                result.append(path)
        except OSError:
            pass
    return result
