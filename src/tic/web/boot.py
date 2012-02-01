import webapp2
import mimetypes
import os
import sys
from datetime import datetime
from tic.utils.datefmt import LocalTimezone, http_date

localtz = LocalTimezone()

import sys
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

      
      
app = webapp2.WSGIApplication([(r'.*/client/.*', StaticClientFilesHandler)],
                              debug=True)
