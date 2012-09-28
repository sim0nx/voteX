import logging
log = logging.getLogger(__name__)





class Authentication:

  def __init__(self, session, config):
    self.session = session
    self.config = config

    auth_module = config.get('auth.module')
    auth_class = config.get('auth.class')

    AuthMod = __import__('votex.lib.auth.' + auth_module, fromlist=[auth_class])
    AuthClass = getattr(AuthMod, auth_class)

    self.__authenticator = AuthClass()
    

    
  def auth(self, username, password):
    """Authenticate the user

    Backend modules should implement __auth__.
    """

    # sanity checks before calling backend
    if not (len(username) > 0 and len(username) < 64 and len(password) > 0 and len(password) < 64):
      log.debug("Username or password doesn't pass minimum requirements for user: {}".format(username))
      return False


    # Catch errors of third party authentication backends
    # if something goes wrong we refuse to authenticate
    is_authenticated = False

    try:
      is_authenticated = self.__authenticator(username, password)
    except Exception as e:
      log.debug("Authentication backend raised an exception: {}".format(str(e)))

    if is_authenticated:
      self.initSession(username)
      log.debug("User authenticated: {}".format(username))
      return True

    else:
      log.debug("Couldn't authenticate user: {}".format(username))
      return False
    

  def deauth(self):
    if 'uid' in self.session:
      self.session['uid'] = None
      del(self.session['uid'])
      self.session.invalidate()
      self.session.save()
      self.session.delete()

  def initSession(self, username):        
    self.deauth()

    self.session['uid'] = username
    self.session.save()
