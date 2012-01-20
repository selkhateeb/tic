.. highlight:: javascript

Dependency Injection Framework
==============================

The idea is to port google Guice over to javascript.  We need to be
able to do that in both development and compiled environment.

Usage
-----
Similar to::

   goog.inherit(class_obj, super);

we can use after class definition::

  tic.inject(class_obj, [arg_class1, arg_class2, ...]);

How It Works 
------------ 
It is important that we don't use string class names, like
'goog.ui.Component'.  In order to avoid that here is what we need to
do:
map that class object to its args in a global var::

  var INJECT = {};
  tic.inject = function(class_obj, args){
    INJECT[class_obj] = args;
  };

and later use it::
 
  tic.getArgs(class_obj){
    return INJECT[class_obj];
  };

However, we cannot just do it that way. Simply because javascript
objects are arrays whose keys are strings. Or map where the key is
only and only strings are allowed.  So in the previous code the VM
will convert the class to a string object using class.toString. Which
will result in non unique and unpredictable string.

So we have to find a way to calculate a string from the class
object. This string generating algorithm must be deterministic.

So lets generate our own unique strings, *sweet!*

Algorithm to Generate a String From Class Object
------------------------------------------------

Using the toString property::

  String s = ""
  foreach property in class_obj:
    s += property.toString();
  
  return md5(s);

There are 2 issues with this:
1. this assumes that every time you call for..in.. it loops through
them in the same order.

2. a performance issue. Because we need to generate the the unique
string every time we need to access the object.

To resolve these issues, all we need to do is just cache the result in
a special property on the same object, lets call it ___class_id___.

So, the previous code becomes::

  if(class_obj.___class_id___) return class_obj.___class_id___
  String s = ""
  for(var property in class_obj)
    s += property.toString();
  
  var md5 = md5(s);
  class_obj.___class_id___ = md5;
  return md5

So far so good.. wait a minute, why in the world are we doing this?
why are we looping and calculating the md5 of a string? all what we
really doing is generating a unique id, right? so why not just use
goog.getUid(object).

Going through the documentations of goog.getUid reveals that "calls
with the same object as a parameter returns the same value.", *awesome*,
our work is done here.


