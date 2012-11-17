import pam


class PAMAuthBackend:
    """Authenticate the user with PAM

    PAM can be configured to use different backends like
    LDAP, mysql, passwd file, kerberos. We simply respect
    what PAM has to say. 


    Settings:
    
    auth.module = pamauth
    auth.class = PAMAuthBackend
    """
    def __call__(self, username, password):
        return pam.authenticate(username, password, service="votex")
