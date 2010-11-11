
import os

def in_development():
    """
    Returns True if we are in development
    """
    return 'Development' in os.environ['SERVER_SOFTWARE']