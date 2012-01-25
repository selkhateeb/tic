==============================
tictac Commad-Line Application
==============================

tictac is a command line application for manageing tic projects.

The idea is to install the tic toolkit using python package manager
applications (easy_install or pip) and use tictac command to manage
your tic projects.

Pluggable
~~~~~~~~~
Users can add command line options/arguments in the same way
it's done in python.

Tictac laverages the existing functionality used in argparse.

The following steps describes how to make your command line
option/argument available to tictac

1. Define a module <project>.development.argparse (that means a pythpn
file in src/development/argparse.py)

2. Define a class in that module whos constructor accepts one argument
of type argparse.ArgumentParser

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


