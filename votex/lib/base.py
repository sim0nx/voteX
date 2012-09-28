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



def flash(klass, msg):
    session['flash'] = str(msg)
    session['flash_class'] = klass
    session.save()



def login_required(f):
    def new_f(self, *args, **kwargs):        
        if not self.uid:
            raise Exception("User is not authenticated")
        return f(self,*args, **kwargs)
    return new_f


class has_params:
    def __init__(self,*args ):
        self.args = args

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            for k in self.args:
                if not k in request.params:
                    raise Exception("Key {} not found in request".format(str(k)))
            return f(*args, **kwargs)
        return wrapped_f


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
            print "Session: ",  session
            return super(BaseController, self).__call__(environ, start_response)
        except Exception as e:
             log.exception('Execution of controller stopped with errors')
             result = self.onError(e)
             start_response('200 OK', [('Content-type', 'text/html')])
             return result

    @property
    def auth(self):
        if not self.__auth:
            self.__auth = Authentication(session, config)
        return self.__auth

        
    def authenticate(self):
        if not ('username' in request.params and 'password' in request.params):
            return False

        if not self.auth.auth(request.params['username'], request.params['password']):
            flash('error', "Wrong credentials or user doesn't exist")
            return False

        self.uid = request.params['username']
        session['uid'] = self.uid
        session.save()
        return True


    def onError(self, exception):
        """This callback should be overriden in sublcass, it should render an error page"""
        return render('/error.mako')








