from votex.lib.auth.baseauth import AbstractAuthBackend
from votex.lib.ldapConnector import LdapConnector


class LDAPAuthBackend(AbstractAuthBackend):
  """Authenticate the user against LDAP.


  Settings:

  auth.module = ldap
  auth.class = LDAPAuthBackend
  ldap.server = ldap://localhost
  ldap.basedn_users = ou=People,dc=local,dc=org
  """


  def __init__(self, session):
    super(LDAPAuthBackend, self).__init__(session)

  def __auth__(self, username, password):
    LdapConnector(uid=username, password=password)
    return True
