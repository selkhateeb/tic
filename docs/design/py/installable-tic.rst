=================
 Installable tic
=================

The basic idea is to make tic installable via easy_install or pip.

What I Want
-----------

* I want to create sub projects in a completly different folders.

* I want to include them using only absolute path. Tic figures out the rest

* I want AppEngine to pick up all dependencies and run the application

How To Accomplish This
----------------------

Not sure yet!! but here are some ideas:

* Ideally by just playing with the sys.path of the server.

* It might require some dirty hacks using monkey patching ..

* Has to work .. do what ever it takes to get you there!!!

Where To Start
--------------

* Create 2 sub projects and make one of them depends on the other

* Try to make it work!

Steps Taken So Far
------------------

.. todo:: 
   
   What ??!!

Take 1
~~~~~~

* Lets see if we can make the example project to work:

  * Create new directory called example.

  * Inside it; create the src directory

  * Copy the stuff from example into it

  * Take a clone of tic in a completely seperate directory

  * delete the example project from tic clone

  * Copy the app.yaml from tic to the example and delete it from tic

  * Copy the runserver command code into the parent directory of the example project

  * Hack the sys.path to include everything

  * Add the main method

  * Run the script !! python runserver.py 


* **RESULTS**

  * For some reason appengine did not register any of the tic libs

Take 2
~~~~~~
* Continuing where we left from Take 1

  * Diving into google.appengine.tools.dev_appserver_main and
    dev_appserver_import_hook

  * The main function that creates the server is
    google.appengine.tools.dev_appserver.CreateServer

  * Now looking at dev_appserver_import_hook.FakeFile.SetAllowdPaths:

    * Add the absolute path to the application_paths::

          application_paths +=
                          ['/Users/selkhateeb/Development/Projects/tic-experiment/tic/src/',
                          '/Users/selkhateeb/Development/Projects/tic-experiment/example/src/']

* **RESULTS**

  * Yay.. this seems to fool AppEngine to consider it as in my path..
    Awesome!!!

Take 3
~~~~~~

* From Take 2 results .. lets see if we can generalize it .. monkey patch it .. anything :)

  * Monkey patch dev_appserver_import_hook.FakeFile.SetAllowdPaths so that:

    * we take the 'application_paths' argument and add to it our custom paths

    * call the original dev_appserver_import_hook.FakeFile.SetAllowdPaths method

* **RESULTS**

  * Success!! works like a charm .. here is the monkey patch code::

  # Monkey patching Google AppEngine
  from google.appengine.tools.dev_appserver_import_hook import FakeFile

  FakeFile.oldSetAllowedPaths = staticmethod(FakeFile.SetAllowedPaths)

  #Our patching function
  def patchedSetAllowedPaths(root_path,
    application_paths): application_paths +=
      ['/Users/selkhateeb/Development/Projects/tic-experiment/tic/src/',
       '/Users/selkhateeb/Development/Projects/tic-experiment/example/src/']
      
      #this import statement is required. looks like we are in
      different scope from
      google.appengine.tools.dev_appserver_import_hook import FakeFile
      FakeFile.oldSetAllowedPaths(root_path, application_paths)
      
  FakeFile.SetAllowedPaths = staticmethod(patchedSetAllowedPaths)

  
