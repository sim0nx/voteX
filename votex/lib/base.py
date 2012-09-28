"""The base Controller API

Provides the BaseController class for subclassing.
"""

from pylons import request, config, session
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from votex.model.meta import Session
from votex.lib import Authentication

import logging
log=logging.getLogger(__name__)








class BaseController(WSGIController):

    def __init__(self, *args, **kwargs):
        super(BaseController, self).__init__(*args, **kwargs)
        self.__auth = None



    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return super(BaseController, self).__call__(environ, start_response)
        except Exception as e:
            log.exception('Execution of controller stopped with errors')
            result = self.onError(e)
            start_response('200 OK', [('Content-type', 'text/html')])
            return result

        


    def onError(self, exception):
        """This callback should be overriden in sublcass, it should render an error page"""
        return render('/error.mako')








