from votex.lib.auth.baseauth import AbstractAuthBackend
import pam


class PAMAuthBackend(AbstractAuthBackend):
    """Authenticate the user with PAM

    PAM can be configured to use different backends like
    LDAP, mysql, passwd file, kerberos. We simply respect
    what PAM has to say. 


    Settings:
    
    auth.module = pamauth
    auth.class = PAMAuthBackend
    """

    def __init__(self, session):
        super(PAMAuthBackend, self).__init__(session)
            
    def __auth__(self, username, password):
        return pam.authenticate(username, password,service="votex")
