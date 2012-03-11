import urllib
import webapp2
import mimetypes
import os
import sys
from datetime import datetime
from tic import loader2
from tic.development import closure

from tic.web import cdp
from protorpc.webapp import service_handlers
import simplejson
from tic.utils.importlib import import_module
from google.appengine.ext import blobstore
import logging
import cgi
from google.appengine.ext.webapp import blobstore_handlers

class StaticClientFilesHandler(webapp2.RequestHandler):
    def get(self):
        paths = set([''.join([path, self.request.path]) for path in sys.path if path.startswith('/Users/')])
        files = [file for file in paths if os.path.exists(file)]
        if len(files) > 1:
            raise webapp2.exc.HTTPServerError('Found more than one static file for '
                                              '%(path)s in %(paths)s' % {
                    'path' : self.request.path,
                    'paths' : files
                    })

        if len(files) == 0:
            raise webapp2.exc.HTTPNotFound('%(path)s' % {
                    'path' : self.request.path,
                    })

            
        self.send_file(files[0])

    def send_file(self, path):
        """Send a local file to the browser.
        this is not effcient. NEVER USE IN PRODUCTION
        """
        stat = os.stat(path)
        mimetype = mimetypes.guess_type(path)[0] or \
            'application/octet-stream'

        self.response.status = 200
        self.response.headers['Content-Type'] =  mimetype
        self.response.headers['Content-Length'] = stat.st_size

        if self.request.method != 'HEAD':
            self.response.write(open(path).read())

class DefaultHandler(webapp2.RequestHandler):
    closure_template = os.path.join(os.path.dirname(__file__), 'templates', "closure.html")
    def get(self):

        files = loader2.locate("entrypoint.js")
        if len(files) > 1:
            raise webapp2.exc.HTTPServerError('More than one entry point defined\n%s' % '\n'.join(files))

        if not len(files):
            raise webapp2.exc.HTTPServerError('No entry point defined\n')

        js_entrypoint = closure.get_namespace(files[0])

        css_deps, js_deps = closure.calculate_deps(files[0])
        return self._render_template(self.closure_template, {
                'entrypoint': js_entrypoint,
                'js_deps': js_deps,
                'css_deps': css_deps
                })

    def _render_template(self, file, data=None):
        from google.appengine.ext.webapp import template
        mimetype = "text/html;charset=utf-8"
        self.response.headers['Content-Type'] = mimetype
        self.response.write(template.render(file, data))

class TestsHanlder(DefaultHandler):
    def get(self):
        request_path = self.request.path[:-1] if self.request.path.endswith('/') \
            else self.request.path

        request_path = request_path[1:] + '.js'
        
        paths = loader2.application_paths()

        files = [ os.path.join(path, request_path) \
                    for path in paths \
                    if os.path.exists(os.path.join(path, request_path))]

        if len(files) > 1:
            raise webapp2.exc.HTTPServerError('More than one entry point defined\n%s'
                                              % '\n'.join(files))

        if not len(files):
            raise webapp2.exc.HTTPServerError('Cannot find test file %s' % request_path)

        css_deps, js_deps = closure.calculate_deps(files[0])
        
        #replace script with instrumented one
        #from tic.development.labs import coverage
        original_filename = files[0].replace('_test', '')
        original_script_path = ''.join([
                '/', 
                loader2.get_relative_path(original_filename)])
        instrumented_script_path = ''.join([
                '/instrumented', #TODO: should be loaded from config .. or some other way
                original_script_path])
        js_deps[js_deps.index(original_script_path)] = instrumented_script_path

        template = os.path.join(os.path.dirname(__file__), 'templates', "closure_test.html")
        self._render_template(
            template,
            {
                'title': request_path[:-1].replace('/','.').replace('_test',''),
                'js_deps': js_deps,
                'js_test': '/' + request_path,
                'css_deps': css_deps
                })
        
class EntryPointHanlder(DefaultHandler):
    def get(self):
        request_path = self.request.path[:-1] if self.request.path.endswith('/') \
            else self.request.path

        request_path = request_path[1:] + '.js'

        files = [ os.path.join(path, request_path) \
                    for path in loader2.application_paths() \
                    if os.path.exists(os.path.join(path, request_path))]


        if len(files) > 1:
            raise webapp2.exc.HTTPServerError('More than one entry point defined\n%s'
                                              % '\n'.join(files))

        if not len(files):
            raise webapp2.exc.HTTPServerError('No entry point defined\n')
        
        ep = closure.get_namespace(files[0])
        css_deps, js_deps = closure.calculate_deps(files[0])
        self._render_template(self.closure_template, {
                'entrypoint': ep,
                'js_deps': js_deps,
                'css_deps': css_deps
                })
        

class CommandHanlder(webapp2.RequestHandler):
    def post(self):
        json_command = simplejson.loads(self.request.body)
        class_name = json_command['_cc_']
        command = self._new_instance(self._get_class(class_name))
        command.from_js(json_command)
        result = None

        command_handler = command.handler(self)
        result = command_handler.execute(command)
        result = result if isinstance(result, basestring) else result.to_json()
        logging.debug("Result:")
        logging.debug(result)

        mimetype = "application/json"
        self.response.headers['Content-Type'] = mimetype
        self.response.write(result)
        
    def _get_class(self, command_class_name):
        """
        """
        module, attr = command_class_name.rsplit('.', 1)
        mod = import_module(module)
        cls = getattr(mod, attr)
        logging.debug(cls)

        #sanity check
        if cdp.Command not in cls.mro():
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


class BlobstoreUploadHandler(webapp2.RequestHandler):
    """Handles blob store upload
    """
    def __init__(self, *args, **kwargs):
        super(BlobstoreUploadHandler, self).__init__(*args, **kwargs)
        self.__uploads = None

    def get_uploads(self, field_name=None):
        """Get uploads sent to this handler.

        Args:
        field_name: Only select uploads that were sent as a specific field.

        Returns:
        A list of BlobInfo records corresponding to each upload.
        Empty list if there are no blob-info records for field_name.
        """
        if self.__uploads is None:
            self.__uploads = {}
            for key, value in self.request.params.items():
                if isinstance(value, cgi.FieldStorage):
                    if 'blob-key' in value.type_options:
                        self.__uploads.setdefault(key, []).append(
                            blobstore.parse_blob_info(value))

        if field_name:
            try:
                return list(self.__uploads[field_name])
            except KeyError:
                return []
        else:
            results = []
            for uploads in self.__uploads.itervalues():
                results += uploads
        return results
    
    def post(self):
        """
        """
        logging.info(self.get_uploads('file'))
        result = FileUploadResult()
        result.key = str(self.get_uploads()[0].key()) #TODO: return a good key string
        mimetype = "application/json"
        self.response.headers['Content-Type'] = mimetype
        self.response.write(result.to_json())

class FileUploadResult(cdp.Result):
    key = cdp.StringProperty()

class BlobstoreDownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):

    """Handles blob store download
    """
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

        
app = webapp2.WSGIApplication(
    [(r'/.*/client/.*_ep/?', EntryPointHanlder),
     (r'/.*/client/.*_test/?', TestsHanlder),
     (r'/.*/client/.*', StaticClientFilesHandler),
     (r'/upload', BlobstoreUploadHandler),
     (r'/file/([^/]+)?', BlobstoreDownloadHandler),
     (r'/rcdc', CommandHanlder),
     (r'/.*', DefaultHandler),
     ],
    debug=True)

