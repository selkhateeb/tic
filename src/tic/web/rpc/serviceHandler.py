from tic.web.browser.console import get_js
import logging
import os
from tic.core import Component, ExtensionPoint
from tic.web.rpc.api import CustomJsException, IJsonRpcService
from tic.web.rpc.json import JSONEncodeException, dumps, loads

class ServiceException(Exception):
    pass

class ServiceRequestNotTranslatable(ServiceException):
    pass

class BadServiceRequest(ServiceException):
    pass

class ServiceMethodNotFound(ServiceException):
    def __init__(self, name):
        msg = "Could not find a service that has the method '" + name + "'"
        ServiceException.__init__(self, msg)
        self.methodName = name

class ServiceHandler(Component):

    services = ExtensionPoint(IJsonRpcService)

    def handle_request(self, json, request):
        self.request = request
        err = None
        result = None
        id_ = ''
        
        try:
            req = self._translate_request(json)
        except ServiceRequestNotTranslatable, e:
            err = e
            req = {'id':id_}

        if err == None:
            try:
                id_ = req['id']
                methName = req['method']
                args = req['params']
            except:
                err = BadServiceRequest(json)
                
        if err == None:
            try:
                meth = self._find_service_endpoint(methName)
            except Exception, e:
                err = e

        if err == None:
            try:
                result = self._invoke_service_endpoint(meth, args)
            except Exception, e:
                err = e

        resultdata = self._translate_result(result, err, id_)

        return resultdata

    def _translate_request(self, data):
        try:
            req = loads(data)
        except:
            raise ServiceRequestNotTranslatable(data)
        return req
     
    def _find_service_endpoint(self, rpc_method_name):
        '''
        finds the requested method and returns it
        '''
        try:

            #get the module, class and method names
            module, class_name, method_name = rpc_method_name.rsplit('.', 2)

            service = None
            #find the called service
            for srv in self.services:
                if (srv.__class__.__name__ == class_name) and (srv.__class__.__module__ == module):
                    service = srv
                    service.request = self.request
                    break

            if not service:
                raise ServiceMethodNotFound(rpc_method_name)
            #get the method and return it
            meth = getattr(service, method_name)
            return meth

        except AttributeError:
            raise ServiceMethodNotFound(rpc_method_name)

    def _invoke_service_endpoint(self, meth, args):
        return meth(*args)

    def _translate_result(self, rslt, err, id_):
        if err != None:
            if isinstance(err, CustomJsException):
                return err.message
            log = self._log_errors()
            if log:
                return log
            
            err = {"name": err.__class__.__name__, "message":err.message}
            rslt = None

        try:
            if isinstance(rslt, basestring):
                data = '{"result":%s,"id":%i,"error":%s}' % (rslt, id_, dumps(err))
            else:
                data = dumps({"result":rslt, "id":id_, "error":err})
        except JSONEncodeException, e:
            err = {"name": "JSONEncodeException", "message":"Result Object Not Serializable"}
            data = dumps({"result":None, "id":id_, "error":err})

        browser_hook = get_js(data)
        if browser_hook: return browser_hook
        return data

    def _log_errors(self):
        """
        In development env, it will logs the error to the browser's console as well
        as the logs file.
        otherwise, it will only be logged in the log files (appengine app console)
        """
        
        import traceback, sys
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb = traceback.format_exception(exc_type, exc_value, exc_tb)
        err = ''.join(tb)
        logging.error(err)
        if 'Development' in os.environ['SERVER_SOFTWARE']:
            return "console.warn(%s)" % dumps("Python Error:\n%s" % err)

