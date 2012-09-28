from abc import ABCMeta, abstractmethod
import logging
log = logging.getLogger(__name__)


class AbstractAuthBackend:
  __metaclass__ = ABCMeta

  def __init__(self, session):
    self.session = session




    
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
      is_authenticated = self.__auth__(username, password)
    except Exception as e:
      log.debug("Authentication backend raised an exception: {}".format(str(e)))

    if is_authenticated:
      self.initSession(username)
      log.debug("User authenticated: {}".format(username))
      return True

    else:
      log.debug("Couldn't authenticate user: {}".format(username))
      return False
    

  
  @abstractmethod
  def __auth__(self,username, password):
    """This method should be overriden

    Should return True/False or raise an Exception with an error description 
    if username exists and the passwords match. 
    """
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
