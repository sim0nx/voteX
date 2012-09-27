from votex.lib.auth.baseauth import AbstractAuthBackend
from votex.lib.ldapConnector import LdapConnector


class LDAPAuthBackend(AbstractAuthBackend):
  def __init__(self, session):
    super(LDAPAuthBackend, self).__init__(session)

  def auth(self, username, password):
    if not super(LDAPAuthBackend, self).auth(username, password):
      return False

    ret = False

    try:
      ldapcon = LdapConnector(uid=username, password=password)
      ret = True
      self.initSession(username)
    except:
      pass

    return ret
