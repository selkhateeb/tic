import os.path
from tic.utils.simplejson import dumps
import logging
import os
import sys
from datetime import datetime, time
MESSAGES = []

# next bit filched from 1.5.2's inspect.py
def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        return sys.exc_traceback.tb_frame.f_back
if hasattr(sys, '_getframe'): currentframe = lambda: sys._getframe(2)

def find_caller():
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """
    f = currentframe().f_back
    rv = "(unknown file)", 0, "(unknown function)"
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        rv = (filename, f.f_lineno, co.co_name)
        break
    return rv

def log(message, type="INFO"):
    """
    TODO: do something with the type
    """
    global MESSAGES
    filename, lineno, func = find_caller()
    filename = filename.replace(os.path.abspath(os.curdir), '')
    now = datetime.now()
    t = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    s = "%s,%03d" % (t, now.microsecond/1000)
    MESSAGES.append("[SERVER] %s  %s %s:%s] %s" % ('INFO', s, filename,lineno, message))

def error(message):
    log(message, "ERROR")
    
def get_js(result):
    global MESSAGES
    if not MESSAGES: return
    m = '\n'.join(MESSAGES)
    MESSAGES = []
    return "function(){console.log(%s);return %s;}()" % (dumps(m), result)

