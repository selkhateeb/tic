import os.path

import fnmatch
import logging
import os
from google.appengine.api.mail import InboundEmailMessage
from tic import loader
from tic.conf import settings
from tic.core import Component, ExtensionPoint, TicError, implements
from tic.exceptions import FileNotFoundException, ImproperlyConfigured
from tic.utils.importlib import import_module
from tic.web.api import HTTPNotFound, IAuthenticator, IEmailHandler, IRequestHandler, \
    Request, RequestDone
from tic.web.rpc.json import dumps


os.environ['TRAC_SETTINGS_MODULE'] = 'tic.conf.global_settings'

def dispatch_request(environ, start_response):
    """
    Main entry point for the TIC web interface.
    
    Args:
        environ: the WSGI environment dict
        start_response: the WSGI callback for starting the response
    """
    try:
        from boot import ENVIRONMENT
        req = Request(environ, start_response)
        try:
            dispatcher = RequestDispatcher(ENVIRONMENT)
            dispatcher.dispatch(req)
        except RequestDone:
            pass
        resp = req._response or []
        return resp
    except Exception, ex:
        req = Request(environ, start_response)
        from google.appengine.ext.webapp import template
        from tic.web import browser
        req.send_response(500)
        mimetype = "text/html;charset=utf-8"
        req.send_header('Content-Type', mimetype)
        import traceback, sys
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb = traceback.format_exception(exc_type, exc_value, exc_tb)
        err = ''.join(tb)

        logging.error('\n' + err)

        if 'Development' in os.environ['SERVER_SOFTWARE']:
            error = "function(){console.warn(%s);}()" % dumps("Python Error:\n%s" % err)
            vars = {
                'data': {
                    'js': error,
                    'text': '<br />'.join(tb)
                    }
                }
            
            req.write(template.render("%stic/web/templates/error.html" % loader.root_path(), vars))
        else:
            raise


class FavIconHanlder(Component):
    """
    Default handler for the favicon to return nothing..
    this is just to escape erroring out which cost alot in appengine
    
    This can be overridden by configuring it in the app.yaml file. see
    appengine docs for more details
    """
    implements(IRequestHandler)
    def match_request(self, req):
        return req.path_info == '/favicon.ico'

    def process_request(self, req):
        pass

class MailHandler(Component):
    '''
    Router for all incomming mail
    '''
    implements(IRequestHandler)
    
    handlers = ExtensionPoint(IEmailHandler)
    
    def match_request(self, req):
        return req.path_info.startswith('/_ah/mail/')

    def process_request(self, req):
        #TODO: construct EmailMessage object
        emailMessate = InboundEmailMessage(req.read())
        
        for handler in self.handlers:
            if handler.match_email(emailMessate):
                handler.process_email(emailMessate)

class DefaultHandler(Component):
    '''
    This is the default handler. It basically handles the entry, index.html
    and converting any dojo files to cross domain,xd, files if needed
    '''
    implements(IRequestHandler)

    templates_dir = "templates"

    def match_request(self, req):
        return "/client/" in req.path_info

    def process_request(self, req):
        
        self.templates_dir = "%stic/web/templates/" % loader.root_path()

        template = os.path.join(self.templates_dir, "index.html")
        
        request_path = req.path_info[1:]
        file = os.path.join(loader.root_path(), request_path) #removes the first '/'
        if self.match_request(req): # /client/
            if file.endswith('.js'):
                return self._render_dojo_file(file, req)
            # TODO: Not sure whats the best way to make a default renderer for django templates
            elif file.endswith('.django.html'):
                return self._render_template(file, req)
            elif file.endswith('/'):
                file = file[:-1]
                path, filename = file.rsplit('/', 1)
                css_file = os.path.join(
                                        "%s%s" % (os.sep, path), "resources%(fs)scss%(fs)s%(filename)s" % {"fs": os.sep, "filename": "%s.css" % filename})
                return self._render_template(
                                             os.path.join(self.templates_dir, "index_js.html"),
                                             req,
                                             {"js": file.replace(loader.root_path(), '').replace('/', '.'),
                                             "css": css_file
                                             })

        if not request_path:
            from tic.loader import locate, _get_module_name
            count = 0
            files = []
            for file in locate("entrypoint.js"):
                files.append(file)
                count += 1
                js_entrypoint = _get_module_name(file)
            
            if count > 1:
                raise Exception('More than one entry point defined\n%s' % '\n'.join(files))
            
            return self._render_template(template, req, {
                                            'entrypoint': js_entrypoint
                                         })

        req.send_file(os.path.abspath(file))

    def _render_template(self, file, req, data=None):
        from google.appengine.ext.webapp import template
        mimetype = "text/html;charset=utf-8"
        req.send_header('Content-Type', mimetype)
        logging.debug(self._get_dojo_modules())
        vars = {
            'modules': self._get_dojo_modules(),
            'base': os.path.join(os.path.abspath(os.curdir), os.path.join(self.templates_dir, "base.html")),
            'data': data,
            }
        req.write(template.render(file, vars))

    def _render_dojo_file(self, file, req):
        if file.endswith(".xd.js"): # Dojo Cross domain. we need to genereate the file
            #get the basic file
            file = file.replace(".xd.", ".")
            self._assert_file_exists(file)
            from tic.web.dojo import render_xd_classes
            return render_xd_classes(file, req)

        self._assert_file_exists(file)
        req.send_file(os.path.abspath(file))

    def _assert_file_exists(self, file):
        if not os.path.isfile(file):
            raise FileNotFoundException(file)

    def _get_dojo_modules(self):
        modules = []
        for file in loader.locate('*.js'):
            logging.debug(file)
            if '/client/' in file:
                m = file.replace(loader.root_path(), '').split('/')[0]
                modules.append(m)
        return set(modules)
    
        
class RequestDispatcher(Component):
    """
    Web request dispatcher.
    This component dispatches incoming requests to registered handlers.
    """
    required = True

    authenticators = ExtensionPoint(IAuthenticator)
    handlers = ExtensionPoint(IRequestHandler)

    # Public API

    def authenticate(self, req):
        for authenticator in self.authenticators:
            authname = authenticator.authenticate(req)
            if authname:
                return authname
        else:
            return 'anonymous'

    def dispatch(self, req):

        # Setup request callbacks for lazily-evaluated properties
        req.callbacks.update({
                             'authname': self.authenticate,
                             'session': self._get_session,
                             #            'locale': self._get_locale,
                             #            'tz': self._get_timezone,
                             #            'form_token': self._get_form_token
                             })

        # select handler
        chosen_handler = None
        try:
            for handler in self.handlers:
                if handler.match_request(req):
                    chosen_handler = handler
                    break

            # choose the default one if no handler found
            if not chosen_handler:
                if not req.path_info or req.path_info == '/':
                    chosen_handler = self._load_default_handler()
        except TicError, e:
            raise HTTPInternalError(e)

        
        if not chosen_handler:
            if req.path_info.endswith('/'):
                # Strip trailing / and redirect
                target = req.path_info.rstrip('/').encode('utf-8')
                if req.query_string:
                    target += '?' + req.query_string
                req.redirect(req.href + target, permanent=True)
            raise HTTPNotFound('No handler matched request to %s',
                               req.path_info)

        # pre-process any incoming request, whether a handler
        # was found or not
        chosen_handler = self._pre_process_request(req, chosen_handler)
        

        # process request
        chosen_handler.process_request(req)

        # TODO: post-process request


    # Private methods
    def _load_default_handler(self):
        """loads the default handler"""
        module, attr = settings.DEFAULT_HANDLER.rsplit('.', 1)
        try:
            mod = import_module(module)
        except ImportError, e:
            raise ImproperlyConfigured('Error importing default handler module %s: "%s"' % (module, e))
        except ValueError, e:
            raise ImproperlyConfigured('Error importing default handler module. Is DEFAULT_HANDLER a correctly defined class')
        try:
            cls = getattr(mod, attr)
        except AttributeError:
            raise ImproperlyConfigured('Module "%s" does not define a "%s" default handler backend' % (module, attr))
        return cls(self.compmgr)

    def _pre_process_request(self, req, chosen_handler):
        for filter_ in settings.REQUEST_FILTERS:
            filter = self._load_filter(filter_)
            chosen_handler = filter.pre_process_request(req, chosen_handler)
        return chosen_handler

    def _load_filter(self, filter):
        """loads the filter"""
        module, attr = filter.rsplit('.', 1)
        try:
            mod = import_module(module)
        except ImportError, e:
            raise ImproperlyConfigured('Error importing filter module %s: "%s"' % (module, e))
        except ValueError, e:
            raise ImproperlyConfigured('Error importing filter module. Is FILTERS a correctly defined class')
        try:
            cls = getattr(mod, attr)
        except AttributeError:
            raise ImproperlyConfigured('Module "%s" does not define a "%s" filter backend' % (module, attr))
        return cls(self.compmgr)

        
    
    def _get_session(self, req):
        from tic.web.sessions import Session
        return Session()





    
