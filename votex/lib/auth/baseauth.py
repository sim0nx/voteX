from abc import ABCMeta, abstractmethod


class AbstractAuthBackend:
  __metaclass__ = ABCMeta

  def __init__(self, session):
    self.session = session

  @abstractmethod
  def auth(self, username, password):
    if len(username) > 0 and len(username) < 64 and len(password) > 0 and len(password) < 64:
      return True

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
