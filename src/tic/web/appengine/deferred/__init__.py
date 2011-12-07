import logging
from google.appengine.ext.deferred.deferred import PermanentTaskFailure, run
from tic.core import Component, implements
from tic.web.api import IRequestHandler

#/_ah/queue/deferred

class DeferredHandler(Component):
    implements(IRequestHandler)

    def match_request(self, req):
        return req.path_info.endswith("/_ah/queue/deferred")

    def process_request(self, req):
        """
        Process the request
        """
        if req.method == 'POST':
            headers = ["%s:%s" % (k, v) for k, v in req._inheaders
                   if k.lower().startswith("x-appengine-")]
            logging.info(", ".join(headers))

            try:
                run(req.read())
            except PermanentTaskFailure, e:
                logging.exception("Permanent failure attempting to execute task")
        