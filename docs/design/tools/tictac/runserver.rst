===================
 runserver Command
===================

Usage
-----

::

  tictac runserver


Design
------

This command is responsible for running the Google AppEngine
server. Since the server blocks the imports, we need to add some hooks
so that we can make our libs available within the AppEngine sandbox.

Here is a list of paths that needs to be added to the appengine sandbox:

* our tic library

* the project sources

* the project dependancies (which are added using 'tictac deps add ...' command


