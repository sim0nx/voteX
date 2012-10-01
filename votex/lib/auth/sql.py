from votex.lib.base import Session
from votex.model.main import Login
import hashlib
import datetime


class SQLAuthBackend:
  """Authenticate the user against an SQL DB.

  Settings:

  auth.module = sql
  auth.class = SQLAuthBackend
  """
  
  def __call__(self, username, password):
    m = hashlib.sha1()
    m.update(password)

    login = Session.query(Login).filter(Login.username == username).filter(Login.password == m.hexdigest()).one()
    login.last_login = datetime.datetime.now()

    Session.commit()

    return True
