==============================
tictac Commad-Line Application
==============================

tictac is a command line application for manageing tic projects.

The idea is to install the tic toolkit using python package manager
applications (easy_install or pip) and use tictac command to manage
your tic projects.


tic.development.tictac.argparsers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section describes the design decisions taken on an on going
baises as I write the tictac module.

* As a rule for designing an API .. always use keyword args. This
makes it simple to read the code and in the future if we need to
change the argument order or add more arguments, we can do that with
ease.

* '.tic/' directory must exist in the root of the project directory.

* '.tic/config' is the main configuration file in 'ini' format.

* We can use tictac command in any child directory. If we cannot find
the '.tic' directory, we only need to allow the 'init' command. This
is enforced in the CommandLineApplication Class



CommandLineApplication Class
----------------------------

**Terminoligy**:
:command: the commands that come after the main application name
e.g. git add .. 'add' is what we mean by command



This class is the main entry point for this application. This class
takes an optional argparse.ArgumentParser instance as an argument.

The responsibility of this class is to manage the commands by
providing a specific api that can be easily used to add commands and
run the application.

Usage::

    app = CommandLineApplication()
    app.add_command(command_class)
    app.run()

The command_class is described in details in the next section

command_class
'''''''''''''

The command_class is a simple class that accepts an instance of
argparse.ArgumentParser._SubParsersAction which is the value returned
when invoking argparse.ArgumentParser().add_subparsers()

Here is a simple command::

  class TestCommand(object):
    # constructor accepts the subparsers
    def __init__(self, subparsers=None):

      # here we are using the subparsers as we'd expect from python
      self.parser = subparsers.add_parser('test',
                                          help='this is awesome!!')
      self.parser.set_defaults(func=self.run)

    @staticmethod
    def run(args):
      print 'awesome!!!'


CONFIGURATION
~~~~~~~~~~~~~

We need to configure the application. The way its configured should be
similar to git configuration.  So we need a system wide configuration
file which resides in the user's home directory called .tic.  In
addition, we have a .tic/ directory in the project directory.

The configuration file should be also familiar to the developers so
that they can add or remove to it. Thats why we are using the standard
python configparser to do it

So where does it all start? .. look into subcommands/config.py

Pluggable
~~~~~~~~~
Users can add command line options/arguments in the same way
python does it.

Tictac leverages the existing functionality used in argparse.

The following steps describes how to make a custom command available to tictac

1. Define a module <project>.tic.development.subcommands (that means a python
file in src/<project>/tic/development/subcommands/__init__.py)

2. Define a class in that module whos constructor accepts one argument
of type argparse.ArgumentParser._SubParsersAction which returns when
invoking argparse.ArgumentParser().add_subparsers()

3. Do what ever you wish as you would if using the standard lib
http://docs.python.org/library/argparse.html

4. Add this class in __all__ to make it available in tictac
(registration)

.. todo::
   
   Provide Example.


   
Available Commands
~~~~~~~~~~~~~~~~~~

:init: Initialzes the tic project
:runserver:  Runs the AppEngine server
:test:  Runs the tests

init
''''
Creates the initial project directory to be recognized as a tic project.

What Goes Inside a Project Directory
------------------------------------
Consider a new project created called foo, here is how the directory
structure looks like::

  foo/
    .tic/
    src/
      foo/
        __init__.py
    docs/


Project Settings Directory
--------------------------
Project settings will be places in a directory called '.tic/' which resides
in the root of the project directory, similar to git concept.


Sources Directory
-----------------
The 'src' directory contains the source code for the new
project. Inside this directory goes the another directory named after
the project name. Inside that directory goes the __init__.py file to
indicate the project name as a package.

Here is a quick example for a project called foo::

  foo/
    src/
      foo/
        __init__.py
      ...

Documentations Directory
------------------------
The 'docs' directory contains the documentations for the new
project. It is basically created using the sphinx-quickstart with some
default options or can be interactive.

.. todo::

   should this depends on sphinx?


