from tic.core import Interface

class CustomJsException(Exception):
    """
    raise this exception only if you know what your doing

    the message of this exception will be evaluated in the browser

    so if you raise CustomJsException('console.log("exception from python")')
    it will log it in the browser's console 
    """
##
## JSON RPC
##
class IJsonRpcService(Interface):
    """
    Marker interface for all json rpc services
    """
