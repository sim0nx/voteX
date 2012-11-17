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

# -*- coding: utf-8 -*-


import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import redirect
from pylons import config

from votex.lib.base import BaseController, render, Session, flash, require
from votex.model.main import Poll, Question, Answer, Participant, Submission

log = logging.getLogger(__name__)

from votex.lib.helpers import *
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_
import re
from pylons.decorators.rest import restrict

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
    if not request.params.get('vote_key', '') == '':
      try:
        participant = Session.query(Participant).filter(Participant.key == request.params['vote_key']).one()
        poll = Session.query(Poll).filter(Poll.id == participant.poll_id).one()

        if datetime.now() > poll.expiration_date:
          flash('error', _('Sorry, poll has expired'))
          redirect(url(controller='vote', action='vote'))

        if participant.update_date is None:
          c.poll = poll
          c.vote_key = request.params['vote_key']

          return render('/vote/dovote.mako')
      except Exception as e:
        import sys, traceback
        traceback.print_exc(file=sys.stdout)
        pass

    return render('/vote/vote.mako')

  @require('VoteKey')
  def doVote(self):
    participant = Session.query(Participant).filter(Participant.key == request.params['vote_key']).one()
    poll = Session.query(Poll).filter(Poll.id == participant.poll_id).one()

    if not participant.update_date is None:
      flash('error', _('Sorry, your vote has already been submitted'))
      redirect(url(controller='vote', action='vote'))

    if datetime.now() > poll.expiration_date:
      flash('error', _('Sorry, poll has expired'))
      redirect(url(controller='vote', action='vote'))

    for k in request.params:
      if 'question' in k:
        m = re.match(r'question_(t|r|c)_(\d+)(?:_(\d+))?', k)
        if m and len(m.groups()) == 3:
          if m.group(1) == 't':
            q = Session.query(Question).filter(and_(Question.id == m.group(2), Question.poll_id == poll.id)).one()
            a = Session.query(Answer).filter(and_(Answer.id == m.group(3), Answer.question_id == q.id)).one()

            s = Submission()
            s.poll_id = poll.id
            s.question_id = q.id
            s.answer_id = a.id
            s.participant_id = participant.id
            s.update_date = datetime.now()
            s.answer_text = request.params[k]

            Session.add(s)
          elif m.group(1) == 'r':
            q = Session.query(Question).filter(and_(Question.id == m.group(2), Question.poll_id == poll.id)).one()
            a = Session.query(Answer).filter(and_(Answer.id == m.group(3), Answer.question_id == q.id)).one()

            s = Submission()
            s.poll_id = poll.id
            s.question_id = q.id
            s.answer_id = a.id
            s.participant_id = participant.id
            s.update_date = datetime.now()
            s.answer_bool = 1

            Session.add(s)
          elif m.group(1) == 'c':
            q = Session.query(Question).filter(and_(Question.id == m.group(2), Question.poll_id == poll.id)).one()
            a = Session.query(Answer).filter(and_(Answer.id == m.group(3), Answer.question_id == q.id)).one()

            s = Submission()
            s.poll_id = poll.id
            s.question_id = q.id
            s.answer_id = a.id
            s.participant_id = participant.id
            s.update_date = datetime.now()
            s.answer_bool = 1

            Session.add(s)

    #participant.update_date = datetime.now()
    Session.commit()

    flash('success', _('Vote successfully saved'))
    redirect(url(controller='vote', action='vote'))

  def results(self):
    return render('/vote/results.mako')

  @require('VoteKey')
  def showResults(self):
    participant = Session.query(Participant).filter(Participant.key == request.params['vote_key']).one()
    poll = Session.query(Poll).filter(Poll.id == participant.poll_id).one()

    if participant.update_date is None:
      flash('error', _('Vote first'))
      #redirect(url(controller='vote', action='vote'))

    c.poll = poll
    submissions = {}

    for q in poll.questions:
      if not q.type == 1:
        for a in q.answers:
          i = Session.query(Submission).filter(Submission.answer_id == a.id).count()
          submissions[a.id] = i
      else:
        for a in q.answers:
          all_a = Session.query(Submission).filter(Submission.answer_id == a.id).all()
          for s_a in all_a:
            if a.id in submissions:
              submissions[a.id].append(s_a.answer_text)
            else:
              submissions[a.id] = []
              submissions[a.id].append(s_a.answer_text)

    c.submissions = submissions

    return render('/vote/showResults.mako')


#---- Validator(s) --------------------------------------------------------------------------------


  def _validateVoteKey(self):
    if not 'vote_key' in request.params or request.params['vote_key'] == '':
      raise Exception("Vote key is required but not found in request")

    if not re.match(r'^[\w\d]+$', request.params.get('vote_key', '')):
      raise Exception('Invalid vote key')

