from tic.core import Component, ExtensionPoint, implements
from tic.web.rpc.api import IJsonRpcService
from tic.utils.importlib import import_module
from tic.web.api import IRequestHandler
from tic.web.cdp import Command
from tic.web.cdp.api import ICommandHandler
from tic.web.dojo import render_xd_classes
from tic.conf import settings
from tic.utils import simplejson
import logging
class DojoClassDispatcher(Component):
    '''
    this acts as a python => javascript convertor
    '''
    implements(IRequestHandler)

    def match_request(self, req):
        """Return whether the handler wants to process the given request."""
        return "/shared/" in req.path_info

    def process_request(self, req):
        """
        this class maps "serializable" python classes to a dojo class to be
        able to use it in the Rpc request
        """
        cls = self._get_class(self._get_class_name(req.path_info))

        #dojo = to_dojo(cls())
        c = cls(settings.JAVASCRIPT_TOOLKIT)
        dojo = c.to_js()
        render_xd_classes(c.to_js(), req) if self._is_xd(req.path_info) else req.send(dojo, "application/json")
        

    def _get_class_name(self, request_path):
        """returns the fully qualified name of the python class"""
        xd_ext = ".xd.js"
        if xd_ext in request_path:
            return request_path[1:].replace("/", ".").replace(xd_ext, "")
        else:
            return request_path[1:].replace("/", ".").replace(".js", "")

    def _is_xd(self, request_path):
        return ".xd.js" in request_path

    def _get_class(self, class_name):
        """loads and returns the Command class object.
        Note: this does not return an instance, it only returns the class
        """
        module, attr = class_name.rsplit('.', 1)
        mod = import_module(module)
        cls = getattr(mod, attr)

        if Command not in cls.mro():
            raise Exception("%s.%s does not inherit from %s.%s" %
                            (cls.__class__.__module__, cls.__class__.__name__,
                            Command.__class__.__module__, Command.__class__.__name__))

        return cls



class CommandDispatcher(Component):
    """
    Handles the execution of an incoming command and returns the Command Result
    """
    implements(IJsonRpcService)

    command_handlers = ExtensionPoint(ICommandHandler)

    def execute(self, command):
        """Documentation"""

        obj = self._load_python_command_instance(command)

        for command_handler in self.command_handlers:
            if(isinstance(obj, command_handler.command)):
                command_handler.request = self.request

                result = command_handler.execute(obj)
                result = result if isinstance(result, basestring) else result.to_json()
                logging.debug("Result:")
                logging.debug(result)
                return result

        return "found na'n"

    def _load_python_command_instance(self, command):
        """Documentation"""

        try:
            class_name = command['declaredClass']
            logging.debug(class_name)
            cls = self._load_command_class(class_name)
            instance = cls()
            instance.from_js(command)
            logging.debug("instance conversion completed sucesssss")
            return instance
        except Exception, e:
            logging.error(e)
            raise e #Exception('This is not a command class')

    def _load_command_class(self, class_name):
        """Documentation"""
        module, attr = class_name.rsplit('.', 1)
        mod = import_module(module)
        cls = getattr(mod, attr)
        logging.debug(cls)
        if Command not in cls.mro():
            raise Exception("%s.%s does not inherit from %s.%s" %
                            (cls.__class__.__module__, cls.__class__.__name__,
                            Command.__class__.__module__, Command.__class__.__name__))

        return cls

class Rcdc(Component):
    implements(IRequestHandler)

    command_handlers = ExtensionPoint(ICommandHandler)
    def match_request(self, req):
        """Return whether the handler wants to process the given request."""
        return "/rcdc" in req.path_info

    def process_request(self, req):
        """

        """
        json_command = simplejson.loads(req.read())
        class_name = json_command['_cc_']
        command = self._new_instance(self._get_class(class_name))
        command.from_js(json_command)
        result = None
        for command_handler in self.command_handlers:
            if(isinstance(command, command_handler.command)):
                command_handler.request = req

                result = command_handler.execute(command)
                result = result if isinstance(result, basestring) else result.to_json()
                logging.debug("Result:")
                logging.debug(result)
#                return result
        req.send(result, "application/json")

    def _get_class(self, command_class_name):
        """

        """
        module, attr = command_class_name.rsplit('.', 1)
        mod = import_module(module)
        cls = getattr(mod, attr)
        logging.debug(cls)
        if Command not in cls.mro():
            raise Exception("%s.%s does not inherit from %s.%s" %
                            (cls.__class__.__module__, cls.__class__.__name__,
                            Command.__class__.__module__, Command.__class__.__name__))

        return cls
    
    def _new_instance(self, cls):
        """

        """
        try:
            instance = cls()
            logging.debug("instance conversion completed sucesssss")
            return instance
        except Exception, e:
            logging.error(e)
            raise e #Exception('This is not a command class')

