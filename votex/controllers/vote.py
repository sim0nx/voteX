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

from datetime import datetime

import gettext
_ = gettext.gettext



class VoteController(BaseController):

	def __init__(self):
		super(VoteController, self).__init__()

	def index(self):
		return self.vote()

	def vote(self):
		if 'vote_key' in request.params and not request.params['vote_key'] == '':
			try:
				vote = Session.query(Vote).filter(Vote.key == request.params['vote_key']).one()

				if vote.update_date is None:
					c.poll = Session.query(Poll).filter(Poll.id == vote.poll_id).one()
					c.vote_key = request.params['vote_key']

					return render('/vote/dovote.mako')
			except Exception as e:
				print e
				pass

		return render('/vote/vote.mako')

	def doVote(self):
		if not 'vote_key' in request.params or request.params['vote_key'] == '' or\
			not 'vote' in request.params or request.params['vote'] == '':
			redirect(url(controller='vote', action='vote'))
		else:
			try:
				vote = Session.query(Vote).filter(Vote.key == request.params['vote_key']).one()
				poll = Session.query(Poll).filter(Poll.id == vote.poll_id).one()

				if poll.type == 'yesno' and (request.params['vote'] == 'yes' or request.params['vote'] == 'no'):
					vote.simple_vote = request.params['vote']
				elif poll.type == 'yesnonull' and (request.params['vote'] == 'yes' or request.params['vote'] == 'no' or request.params['vote'] == 'null'):
					vote.simple_vote = request.params['vote']
				elif poll.type == 'complex':
					vote.complex_vote = request.params['vote']
				else:
					redirect(url(controller='vote', action='vote'))

				vote.update_date = datetime.now()

				Session.commit()

				print 'vote OK'
				redirect(url(controller='vote', action='vote'))
			except:
				pass

		redirect(url(controller='vote', action='vote'))

	def results(self):
		if not 'vote_key' in request.params or request.params['vote_key'] == '':
			return render('/vote/results.mako')
		else:
			try:
				vote = Session.query(Vote).filter(Vote.key == request.params['vote_key']).one()
				poll = Session.query(Poll).filter(Poll.id == vote.poll_id).one()
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

					c.votes = votes
				else:
					i = 0
					for v in poll.votes:
						votes[str(c)] = v.complex_vote

						i += 1

				return render('/vote/showResults.mako')
			except Exception as e:
				print e
				raise e
				pass

			return render('/vote/results.mako')
