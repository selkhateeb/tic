==============================
tictac Commad-Line Application
==============================

tictac is a command line application for manageing tic projects.

The idea is to install the tic toolkit using python package manager
applications (easy_install or pip) and use tictac command to manage
your tic projects.

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
==========================
Project settings will be places in a directory called '.tic/' which resides
in the root of the project directory, similar to git concept.


Sources Directory
=================
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
========================
The 'docs' directory contains the documentations for the new
project. It is basically created using the sphinx-quickstart with some
default options or can be interactive.

TODO: should this depends on sphinx?


