import webapp2
import mimetypes
import os
import sys
from datetime import datetime
from tic import loader2
from tic.development import closure


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


class TestsHanlder(webapp2.RequestHandler):
    def get(self):
        request_path = self.request.path[:-1] if self.request.path.endswith('/') \
            else self.request.path
        path, filename = request_path.rsplit('/', 1)
        css_deps, js_deps = closure.calculate_test_deps(request_path)
        
        #replace script with instrumented one
        #from tic.development.labs import coverage
        #original_filename = file.replace('_test', '.js')
        #original_script_path = ''.join([
        #        '/', 
        #        loader.get_relative_path(original_filename)])
        #instrumented_script_path = ''.join([
        #        '/instrumented',
        #        original_script_path])
        #js_deps[js_deps.index(original_script_path)] = instrumented_script_path

        template = os.path.join(os.path.dirname(__file__), 'templates', "closure_test.html")
        
        js_test = js_deps.pop()        
        return self._render_template(
            os.path.join(self.templates_dir, "closure_test.html"),
            req,
            {
                'title': request_path[:-1].replace('/','.').replace('_test',''),
                'js_deps': js_deps,
                'js_test': js_test,
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
        return self._render_template(self.closure_template, {
                'entrypoint': ep,
                'js_deps': js_deps,
                'css_deps': css_deps
                })
        


    
app = webapp2.WSGIApplication(
    [(r'/.*/client/.*_ep/?', EntryPointHanlder),
     (r'/.*/client/.*', StaticClientFilesHandler),
     (r'/.*', DefaultHandler)
     ],
    debug=True)
