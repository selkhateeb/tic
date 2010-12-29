import sys

def console_print(out, *args, **kwargs):
    cons_charset = getattr(out, 'encoding', None)
    # Windows returns 'cp0' to indicate no encoding
    if cons_charset in (None, 'cp0'):
        cons_charset = 'utf-8'
    out.write(' '.join([to_unicode(a).encode(cons_charset, 'replace') 
                        for a in args]))
    if kwargs.get('newline', True):
        out.write('\n')

def printout(*args, **kwargs):
    console_print(sys.stdout, *args, **kwargs)

def printerr(*args, **kwargs):
    console_print(sys.stderr, *args, **kwargs)
    
def to_unicode(text, charset=None):
    """Convert input to an `unicode` object.

    For a `str` object, we'll first try to decode the bytes using the given
    `charset` encoding (or UTF-8 if none is specified), then we fall back to
    the latin1 encoding which might be correct or not, but at least preserves
    the original byte sequence by mapping each byte to the corresponding
    unicode code point in the range U+0000 to U+00FF.

    Otherwise, a simple `unicode()` conversion is attempted, with some special
    care taken for `Exception` objects.
    """
    if isinstance(text, str):
        try:
            return unicode(text, charset or 'utf-8')
        except UnicodeDecodeError:
            return unicode(text, 'latin1')
    elif isinstance(text, Exception):
        # two possibilities for storing unicode strings in exception data:
        try:
            # custom __str__ method on the exception (e.g. PermissionError)
            return unicode(text)
        except UnicodeError:
            # unicode arguments given to the exception (e.g. parse_date)
            return ' '.join([to_unicode(arg) for arg in text.args])
    return unicode(text)

def get_last_traceback():
    import traceback
    from StringIO import StringIO
    tb = StringIO()
    traceback.print_exc(file=tb)
    return to_unicode(tb.getvalue())

def exception_to_unicode(e, traceback=False):
    message = '%s: %s' % (e.__class__.__name__, to_unicode(e))
    if traceback:
        traceback_only = get_last_traceback().split('\n')[:-2]
        message = '\n%s\n%s' % (to_unicode('\n'.join(traceback_only)), message)
    return message
