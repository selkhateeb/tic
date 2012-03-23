===============
 Build Command
===============

I think the best approach is to implement a chain of resposibilty
design pattern.

So basically we have a bunch of execution steps and run them in a
specific order.

Execution Steps For a Typical Tic Build
=======================================

#. Compile Soy Files

#. Generate Shared JS files

#. Copy src files to build dir

#. Copy deps src files to build dir

#. Generate the new app.yaml file to specify static files

#. I think thats it!!


