#
# Copyright (c) 2012 Georges Toth <georges _at_ trypill _dot_ org>
#
# This file is part of voteX.
#
# voteX is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# voteX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with voteX.  If not, see <http://www.gnu.org/licenses/>.


import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import redirect
from pylons import config

from votex.lib.base import BaseController, render, Session
from votex.model.main import Poll, Vote

log = logging.getLogger(__name__)

from votex.lib.helpers import *
from sqlalchemy.orm.exc import NoResultFound
import re
from pylons.decorators.rest import restrict
from votex.lib.ldapConnector import LdapConnector

import smtplib
from email.mime.text import MIMEText

import random
import string

import gettext
_ = gettext.gettext



class PollController(BaseController):

	def __init__(self):
		super(PollController, self).__init__()
		self.uid = session.get('uid')

		if self.uid:
			c.actions = list()
			c.actions.append( (_('Show all polls'), 'poll', 'showAll') )
			c.actions.append( (_('Add poll'), 'poll', 'addPoll') )

	def login(self):
		if not self.uid is None:
			redirect(url(controller='poll', action='showAll'))

		return render('/login.mako')

	def doLogin(self):
		if not 'username' in request.params or request.params['username'] == '' or not 'password' in request.params or request.params['password'] == '':
			print "crap"
		else:

			ret = False
			try:   
				ldapcon = LdapConnector(uid=request.params['username'], password=request.params['password'])
				ret = True
				print 'auth ok'
			except:
				print 'auth exception'
				pass

			if ret:
				self._clearSession()

				session['uid'] = request.params['username']
				session.save()

				redirect(url(controller='poll', action='showAll'))

		redirect(url(controller='poll', action='login'))

	def _clearSession(self):
		if not self.uid is None:
			session['uid'] = None
			del(session['uid'])
			session.invalidate()
			session.save()
			session.delete()

	def logout(self):
		self._clearSession()

		redirect(url(controller='poll', action='login'))

	def needLogin(f):
		def new_f(self):
			if not self.uid is None:
				return f(self)
			else:
				redirect(url(controller='poll', action='login'))

                return new_f

	@needLogin
	def showAll(self):
		c.heading = _('All polls')
		c.polls = []

		try:
			polls = Session.query(Poll).filter(Poll.owner == self.uid).all()

			for s in polls:
				c.polls.append(s)
		except NoResultFound:
			print 'No such poll'

		return render('/poll/showAll.mako')

	@needLogin
	def addPoll(self):
		c.mode = 'add'

		return render('/poll/edit.mako')

	@needLogin
	def editPoll(self):
		if (not 'poll_id' in request.params):
			redirect(url(controller='poll', action='showAll'))

		try:
			poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == request.params['poll_id']).one()

			c.heading = _('Edit poll')
			c.mode = 'edit'

			if len(poll.votes) > 0:
				session['flash'] = _('Cannot edit a running poll')
				session['flash_class'] = 'error'
				session.save()
				redirect(url(controller='poll', action='showAll'))

			c.poll = poll

			return render('/poll/edit.mako')
		except:
			pass

		redirect(url(controller='poll', action='showAll'))

	def _checkPoll(f):
		def new_f(self):
			# @TODO request.params may contain multiple values per key... test & fix
			formok = True
			errors = []

			if not 'mode' in request.params or (request.params['mode'] != 'add' and request.params['mode'] != 'edit'):
				formok = False
				errors.append(_('Invalid form data'))

			if request.params['mode'] == 'edit' and (not 'poll_id' in request.params or request.params['poll_id'] == '' or not re.match(r'^\d+$', request.params['poll_id'])):
				formok = False
				errors.append(_('Invalid form data'))

			if not 'name' in request.params or request.params['name'] == '' or len(request.params['name']) > 255:
				formok = False
				errors.append(_('Invalid name'))

			if not 'instructions' in request.params or request.params['instructions'] == '' or len(request.params['instructions']) > 1000:
				formok = False
				errors.append(_('Invalid instructions'))

			if not 'voters' in request.params or request.params['voters'] == '':
				formok = False
				errors.append(_('Invalid voters'))
			else:
				voters = request.params['voters'].split('\n')
				for v in voters:
					if not re.match(r'\b[A-Z0-9._%+-]+@(?:[A-Z0-9-]+\.)+[A-Z]{2,4}\b', v, re.I):
						formok = False
						errors.append(_('Invalid voters'))
						break

			if not 'expiration_date' in request.params or not re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', request.params['expiration_date']):
				formok = False
				errors.append(_('Invalid expiration date'))

			if not 'type' in request.params or (request.params['type'] != 'yesno' and request.params['type'] != 'yesnonull' and request.params['type'] != 'complex'):
				formok = False
				errors.append(_('Invalid type'))

			if not 'public' in request.params or (request.params['public'] != 'yes' and request.params['public'] != 'no'):
				formok = False
				errors.append(_('Invalid public'))

			if not formok:
				session['errors'] = errors
				session['reqparams'] = {}

				# @TODO request.params may contain multiple values per key... test & fix
				for k in request.params.iterkeys():
					session['reqparams'][k] = request.params[k]
					
				session.save()

				if request.params['mode'] == 'add':
					redirect(url(controller='poll', action='addPoll'))
				else:
					redirect(url(controller='poll', action='editPoll'))

			return f(self)
		return new_f

	@needLogin
	@_checkPoll
	@restrict('POST')
	def doEditPoll(self):
		try:
			if request.params['mode'] == 'edit':
				poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == request.params['poll_id']).one()
			else:
				poll = Poll()

			poll.owner = self.uid
			poll.name = request.params['name']
			poll.instructions = request.params['instructions']
			poll.expiration_date = request.params['expiration_date']
			poll.type = request.params['type']

			if request.params['public'] == 'yes':
				poll.public = True
			else:
				poll.public = False
			
			if request.params['mode'] == 'add':
				Session.add(poll)
				Session.flush()

			voters = request.params['voters'].split('\n')
			voters = list(set(voters))
			for v in voters:
				vo = None
				vo = Vote()
				vo.poll_id = poll.id
				vo.key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))
				mailtext = '''\
				Hey,

				Your vote is requested for "%s".
				You can vote here:
					https://votex.hackerspace.lu:8443/vote/vote?vote_key=%s

				Your voting key is: %s

				The poll expires on %s
				''' %\
				(poll.name, vo.key, vo.key, poll.expiration_date)

				msg = MIMEText(mailtext, 'plain')
				msg['Subject'] = 'syn2cat - We need you to vote'
				msg['From'] = 'noreply@hackerspace.lu'
				msg['To'] = v
				s = smtplib.SMTP('localhost')
				s.sendmail(msg['From'], v, msg.as_string())
				s.quit()

				Session.add(vo)

			Session.commit()

			session['flash'] = _('Poll successfully edited')
			session.save()

			redirect(url(controller='poll', action='showAll'))

		except LookupError:
			print 'No such user !'
			session['flash'] = _('Failed to add poll')
			session['flash_class'] = 'error'
			session.save()

		redirect(url(controller='poll', action='showAll'))

	@needLogin
	def showResults(self):
		if (not 'poll_id' in request.params):
			redirect(url(controller='poll', action='showAll'))

		try:
			poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == request.params['poll_id']).one()
			c.poll = poll
			votes = {}
			votes['missing'] = 0

			if poll.type == 'yesno' or poll.type == 'yesnonull':
				for v in poll.votes:
					if v.simple_vote is None:
						votes['missing'] += 1
					elif not v.simple_vote in votes:
						votes[v.simple_vote] = 1
					else:
						votes[v.simple_vote] += 1
			else:
				for v in poll.votes:
					if v.complex_vote is None:
						votes['missing'] += 1
					else:
						votes[v.complex_vote] = 1

			c.votes = votes
			
			return render('/vote/showResults.mako')
		except Exception as e:
			print e
			pass

		redirect(url(controller='poll', action='showAll'))

	@needLogin
	def deletePoll(self):
		if (not 'poll_id' in request.params):
			redirect(url(controller='poll', action='showAll'))

		try:
			poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == request.params['poll_id']).one()
			Session.query(Vote).filter(Vote.poll_id == poll.id).delete()

			Session.delete(poll)
			Session.commit()
			session['flash'] = _('Poll successfully deleted')
			session.save()
		except Exception as e:
			print e
			session['flash'] = _('Failed to delete poll')
			session['flash_class'] = 'error'
			session.save()

		redirect(url(controller='poll', action='showAll'))
