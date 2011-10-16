import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import redirect
from pylons import config

from votex.lib.base import BaseController, render, Session
#from votex.model import Member, TmpMember

log = logging.getLogger(__name__)

from votex.lib.helpers import *
from sqlalchemy.orm.exc import NoResultFound
import re
from pylons.decorators.rest import restrict

import gettext
_ = gettext.gettext



class IndexController(BaseController):

	def __init__(self):
		super(IndexController, self).__init__()

	def index(self):
		#return render('/members/editMember.mako')
		return 'ok'

