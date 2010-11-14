
import os

def in_development():
    """
    Returns True if we are in development
    """
    return not os.environ.get('SERVER_SOFTWARE') \
        or 'Development' in os.environ.get('SERVER_SOFTWARE')