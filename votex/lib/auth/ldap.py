from votex.lib.ldapConnector import LdapConnector




class LDAPAuthBackend:
  """Authenticate the user against LDAP.


  Settings:

  auth.module = ldap
  auth.class = LDAPAuthBackend
  ldap.server = ldap://localhost
  ldap.basedn_users = ou=People,dc=local,dc=org
  """
  
  def __call__(self, username, password):
    LdapConnector(uid=username, password=password)
    return True
