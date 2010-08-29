import os.path

import fnmatch
import logging
import os
from tic.conf import settings
from tic.core import Component, ExtensionPoint, TracError, implements
from tic.env import Environment
from tic.exceptions import ImproperlyConfigured
from tic.utils.importlib import import_module
from tic.web.api import HTTPNotFound, IAuthenticator, IRequestHandler, Request, RequestDone


os.environ['TRAC_SETTINGS_MODULE'] = 'tic.conf.global_settings'

def dispatch_request(environ, start_response):
    """Main entry point for the Trac web interface.

    @param environ: the WSGI environment dict
    @param start_response: the WSGI callback for starting the response
    """

    env = Environment()
    req = Request(environ, start_response)

    try:
        dispatcher = RequestDispatcher(env)
        dispatcher.dispatch(req)
    except RequestDone:
        pass
    resp = req._response or []
    return resp

class DefaultHandler(Component):
    '''
    This is the default handler. It basically handles the entry, index.html
    and converting any dojo files to cross domain,xd, files if needed
    '''
    implements(IRequestHandler)

    def match_request(self, req):
        #TODO: 
        return "/client/" in req.path_info

    def process_request(self, req):
        template = "tic/templates/index.html"
        file = req.path_info[1:] #removes the first '/'
        logging.debug(template + "   [" + file + "]")
        if self.match_request(req):
            if file.endswith('.js'):
                return self._render_dojo_file(file, req)
            elif file.endswith('.html'):
                return self._render_template(file, req)

        if not file:
            return self._render_template(template, req)

        req.send_file(os.path.abspath(file))

    def _render_template(self, file, req):
        from google.appengine.ext.webapp import template
        mimetype = "text/html;charset=utf-8"
        req.send_header('Content-Type', mimetype)
        vars = {
            'modules': self._get_dojo_modules(),
            'base': os.path.join(os.path.abspath(os.curdir), 'tic/templates/base.html')
            }
        req.write(template.render(file, vars))

    def _render_dojo_file(self, file, req):
        if file.endswith(".xd.js"): # Dojo Cross domain. we need to genereate the file
            #get the basic file
            file = file.replace(".xd.", ".")
            from tic.web.dojo import render_xd_classes
            return render_xd_classes(file, req)
        
        req.send_file(os.path.abspath(file))

    def _get_dojo_modules(self):
        from tic.loader import locate
        modules = []
        for file in locate('*.js'):
            if '/client/' in file:
                logging.debug(file)
                logging.debug(file.replace(os.path.abspath(os.curdir), '').split('/'))
                m = file.replace(os.path.abspath(os.curdir), '').split('/')[1]

                modules.append(m)
        return set(modules)
        
class RequestDispatcher(Component):
    """Web request dispatcher.

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
                logging.debug(handler.__class__.__name__)
                if handler.match_request(req):
                    chosen_handler = handler
                    break

            # choose the default one if no handler found
            if not chosen_handler:
                if not req.path_info or req.path_info == '/':
                    chosen_handler = self._load_default_handler()
        except TracError, e:
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





    
