#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright (C) 2003-2010 Edgewall Software
#


import os.path
import sys
import logging
import cmd
import locale
import shlex
import  platform
from tic.admin.api import AdminCommandError, AdminCommandManager,IAdminCommandProvider
from tic.admin.util import console_print, exception_to_unicode, printerr, printout, \
    to_unicode
from tic.core import TicError, Component, implements
from tic.env import Environment

rl_completion_suppress_append = None

TIC_VERSION = "0.1"        

def _(str, **kwargs):
    """
    HACK I18N
    """
    if kwargs:
        try:
            return str % kwargs
        except KeyError:
            pass
    return str

def find_readline_lib():
    """Return the name (and possibly the full path) of the readline library
    linked to the readline module.
    """
    import readline
    f = open(readline.__file__, "rb")
    try:
        data = f.read()
    finally:
        f.close()
    import re
    m = re.search('\0([^\0]*libreadline[^\0]*)\0', data)
    if m:
        return m.group(1)
    return None
    

class TicAdmin(cmd.Cmd):
    intro = ''
    doc_header = 'Tic Admin Console %(version)s\n' \
                 'Available Commands:\n' \
                 % {'version': TIC_VERSION}
    ruler = ''
    prompt = "tic> "
    envname = None
    __env = None

    def __init__(self):
        cmd.Cmd.__init__(self)
        try:
            import readline
            import rlcompleter
            readline.parse_and_bind("tab: complete")
            delims = readline.get_completer_delims()
            for c in '-/:()':
                delims = delims.replace(c, '')
            readline.set_completer_delims(delims)
            
            # Work around trailing space automatically inserted by libreadline
            # until Python gets fixed, see http://bugs.python.org/issue5833
            import ctypes
            lib_name = find_readline_lib()
            if lib_name is not None:
                lib = ctypes.cdll.LoadLibrary(lib_name)
                global rl_completion_suppress_append
                rl_completion_suppress_append = ctypes.c_int.in_dll(lib,
                                            "rl_completion_suppress_append")
        except Exception:
            pass
        self.interactive = False
        self.env_set()

    def emptyline(self):
        pass

    def onecmd(self, line):
        """`line` may be a `str` or an `unicode` object"""
        try:
            if isinstance(line, str):
                if self.interactive:
                    encoding = sys.stdin.encoding
                else:
                    encoding = locale.getpreferredencoding() # sys.argv
                line = to_unicode(line, encoding)
            if self.interactive:
                line = line.replace('\\', '\\\\')
            
            rv = cmd.Cmd.onecmd(self, line) or 0
            
        except SystemExit:
            raise
        except AdminCommandError, e:
            printerr(_("Error:"), to_unicode(e))
            if e.show_usage:
                print
                self.do_help(e.cmd or self.arg_tokenize(line)[0])
            rv = 2
        except TicError, e:
            printerr(exception_to_unicode(e))
            rv = 2
        except Exception, e:
            raise
            printerr(exception_to_unicode(e))
            rv = 2
#            if self.env_check():
#                self.env.log.error("Exception in tic command: %s",
#                                   exception_to_unicode(e, traceback=True))
        if not self.interactive:
            return rv

    def run(self):
        self.interactive = True
        printout(_("""Welcome to tic %(version)s
Interactive Tic administration console.
Python Version: %(pyVersion)s
Type:  '?' or 'help' for help on commands.
        """, version=TIC_VERSION, pyVersion= platform.python_version()))
        self.cmdloop()

    ##
    ## Environment methods
    ##

    def env_set(self):
        self.prompt = "tic> "
        self.init_appengine_path()
        self.__env = self.env

    def env_check(self):
        if not self.__env:
            try:
                self.__env = Environment()
            except:
                return False
        return True
    
    def init_appengine_path(self):
        """
        TODOC
        """
        #TODO: use AppEngine Dev Server stuff for this
        root = '/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine/'
        sys.path.append(root)
        sys.path.append(root + "lib/antlr3/")
        sys.path.append(root + "lib/fancy_urllib/")
        sys.path.append(root + "lib/ipaddr/")
        sys.path.append(root + "lib/webob/")
        sys.path.append(root + "lib/yaml/lib/")
        sys.path.append(root + "lib/simplejson/")
        from google.appengine.dist import use_library
        use_library('django', '1.2')


    @property
    def env(self):
        try:
            if not self.__env:
                self.__env = Environment()
            return self.__env
        except Exception, e:
            printerr(_("Failed to open environment: %(err)s",
                       err=exception_to_unicode(e, traceback=True)))
            sys.exit(1)

    ##
    ## Utility methods
    ##

    def arg_tokenize(self, argstr):
        """`argstr` is an `unicode` string

        ... but shlex is not unicode friendly.
        """
        return [unicode(token, 'utf-8')
                for token in shlex.split(argstr.encode('utf-8'))] or ['']

    def word_complete(self, text, words):
        words = list(set(a for a in words if a.startswith(text)))
        if len(words) == 1:
            words[0] += ' '     # Only one choice, skip to next arg
        return words

    @staticmethod
    def split_help_text(text):
        import re
        paragraphs = re.split(r'(?m)(?:^[ \t]*\n){1,}', text)
        return [re.sub(r'(?m)\s+', ' ', each.strip())
                for each in paragraphs]
    
    @classmethod
    def print_doc(cls, docs, stream=None, short=False, long=False):
        if stream is None:
            stream = sys.stdout
        docs = [doc for doc in docs if doc[2]]
        if not docs:
            return
        if short:
            max_len = max(len(doc[0]) for doc in docs)
            for (cmd, args, doc) in docs:
                paragraphs = cls.split_help_text(doc)
                console_print(stream, '%s  %s' % (cmd.ljust(max_len), 
                                                  paragraphs[0]))
        else:
            import textwrap
            for (cmd, args, doc) in docs:
                paragraphs = cls.split_help_text(doc)
                console_print(stream, '%s %s\n' % (cmd, args))
                console_print(stream, '    %s\n' % paragraphs[0])
                if (long or len(docs) == 1) and len(paragraphs) > 1:
                    for paragraph in paragraphs[1:]:                        
                        console_print(stream, textwrap.fill(paragraph, 79, 
                            initial_indent='    ', subsequent_indent='    ')
                            + '\n')

    ##
    ## Command dispatcher
    ##
    
    def complete_line(self, text, line, cmd_only=False):
        if rl_completion_suppress_append is not None:
            rl_completion_suppress_append.value = 1
        args = self.arg_tokenize(line)
        if line and line[-1] == ' ':    # Space starts new argument
            args.append('')
        if self.env_check():
            cmd_mgr = AdminCommandManager(self.env)
            try:
                comp = cmd_mgr.complete_command(args, cmd_only)
            except Exception, e:
            
                printerr()
                printerr(_('Completion error: %(err)s',
                           err=exception_to_unicode(e)))
#                self.env.log.error("tic completion error: %s",
#                                   exception_to_unicode(e, traceback=True))
                comp = []
        if len(args) == 1:
            comp.extend(name[3:] for name in self.get_names()
                        if name.startswith('do_'))
        try:
            return comp.complete(text)
        except AttributeError:
            return self.word_complete(text, comp)
        
    def completenames(self, text, line, begidx, endidx):
        return self.complete_line(text, line, True)
        
    def completedefault(self, text, line, begidx, endidx):
        return self.complete_line(text, line)
        
    def default(self, line):
        if not self.env_check():
            raise AdminCommandError(_("Command not found"))
        args = self.arg_tokenize(line)
        cmd_mgr = AdminCommandManager(self.env)
        return cmd_mgr.execute_command(*args)

    ##
    ## Available Commands
    ##

    @classmethod
    def all_docs(cls, env=None):
        ## Help
        docs = [('help', '', 'Show documentation')]
        if env is not None:
            docs.extend(AdminCommandManager(env).get_command_help())
        return docs

    def complete_help(self, text, line, begidx, endidx):
        return self.complete_line(text, line[5:], True)
        
    def do_help(self, line=None):
        arg = self.arg_tokenize(line)
        if arg[0]:
            doc = getattr(self, "_help_" + arg[0], None)
            if doc is None and self.env_check():
                cmd_mgr = AdminCommandManager(self.env)
                doc = cmd_mgr.get_command_help(arg)
            if doc:
                self.print_doc(doc)
            else:
                printerr(_("No documentation found for '%(cmd)s'",
                           cmd=' '.join(arg)))
        else:
            printout(_("tic - The Tic Administration Console "
                       "%(version)s", version=TIC_VERSION))
            if not self.interactive:
                printout(_("Usage: cm.py "
                           "[command [subcommand] [option ...]]\n")
                    )
                printout(_("Invoking tic without command starts "
                           "interactive mode.\n"))
            env = self.env_check() and self.env or None
            self.print_doc(self.all_docs(env), short=True)
            


    ## Quit / EOF
    _help_quit = [('quit', '', 'Exit the program')]
    _help_exit = _help_quit
    _help_EOF = _help_quit

    def do_quit(self, line):
        print
        sys.exit()

    do_exit = do_quit # Alias
    do_EOF = do_quit # Alias


    def _resync_feedback(self, rev):
        sys.stdout.write(' [%s]\r' % rev)
        sys.stdout.flush()
        
def run(args=None):
    """Main entry point."""
    if len(sys.argv) > 1:
        logging.basicConfig(format=(sys.argv[0] + ': %(message)s'),
                      level=logging.INFO)
    else:
        logging.basicConfig(format=('%(message)s'), level=logging.INFO)

    os.environ['APPLICATION_ID'] = "tic-cm-utility"
    os.environ['AUTH_DOMAIN'] = 'localhost'
    os.environ['SERVER_SOFTWARE'] = 'Development/1.0 (CM Utility)'
    
    if args is None:
        args = sys.argv[1:]
    locale = None
    try:
        import babel
        try:
            locale = babel.Locale.default()
        except babel.UnknownLocaleError:
            pass
    except ImportError:
        pass
    admin = TicAdmin()
    if len(args) > 0:
        if args[0] in ('-h', '--help', 'help'):
            return admin.onecmd(' '.join(['help'] + args[1:]))
        elif args[0] in ('-v','--version'):
            printout(os.path.basename(sys.argv[0]), TIC_VERSION)
        elif args[0] in ('--shortlist'):
            cmd_mgr = AdminCommandManager(admin.env)
            printout('\n'.join(cmd_mgr.complete_command([])))
        else:            
            command = ' '.join(["'%s'" % c for c in args[0:]])
            return admin.onecmd(command)
    else:
        while True:
            try:
                admin.run()
            except KeyboardInterrupt:
                admin.do_quit('')

if __name__ == '__main__':
    sys.exit(run())
