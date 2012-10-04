"""The base Controller API

Provides the BaseController class for subclassing.
"""

from pylons import request, config, session, response
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


class require(object):
    """Search and execute a validator method

    A validator method should check for a requried condition. If the condition 
    is not met it should raise an Exception. The return value of a validator is 
    ignored.
    
    Validators should not have side effects nor assume that they will be executed
    in a specific order.

    Here are default validators which are defined in BaseController, feel free to 
    to override them if needed. Note that the validator methdos are "protected" not 
    "private", single dash _ 

    Login:  check for the presence of a valid self.uid
    POST: raise an exception if http method is not POST
    """
    def __init__(self, *args):
        self.validators = args

    def __call__(self, f):
        def wrapped_f(this, *args, **kwargs):
            for k in self.validators:
                func = getattr(this, "_validate{0}".format(k))
                if func:
                    func()
                else:
                    raise Exception('Validator {0} not found.'.format(k))
            return f(this)
        return wrapped_f

                
def require_login(f):
    """Short form for require('Login')"""
    return require('Login')(f)




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
            start_response('200 OK', [('Content-type', 'text/html')])
            return self.onError(e)


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

        return True


    def onError(self, exception):
        """This callback can  be overriden in sublcass, it should render an error page"""
        flash('error', exception)

        # the default old behavior was:
        # redirect(url(controller='poll', action='showAll'))

        # show an error page? with error text
        return render('/error.mako')






#---- Default Validator(s) -----------------------------------------------------

    def _validateLogin(self):
        if not self.uid:
            raise Exception("User is not authenticated")


    def _validatePOST(self):
        if request.method != 'POST':
            raise Exception("only accepts POST method requests")

