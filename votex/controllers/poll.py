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

# -*- coding: utf-8 -*-"



from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import redirect
from pylons import config
from webob.exc import HTTPFound

from votex.lib.base import BaseController, render, Session, flash, require_login, require
from votex.model.main import Poll, Question, Answer, Participant, Submission

import logging
log = logging.getLogger(__name__)

from votex.lib.helpers import *
from sqlalchemy.orm.exc import NoResultFound
import re

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
      if self.uid or self.authenticate():
          redirect(url(controller='poll', action='showAll'))

      return render('/login.mako')

  def logout(self):
    self.auth.deauth()
    redirect(url(controller='poll', action='login'))

  @require_login
  def showAll(self):
    c.heading = _('All polls')
    c.polls = []

    polls = Session.query(Poll).filter(Poll.owner == self.uid).all()
    for s in polls:
      try:
        s.name = s.name.encode('ascii','ignore')
      except:
        s.name ='poo...frickin P000000'
      c.polls.append(s)

    return render('/poll/showAll.mako')

  @require_login
  def addPoll(self):
    c.mode = 'add'
    return render('/poll/edit.mako')

  @require('Login', 'PollID', 'RunningPoll')
  def addQuestion(self):
    poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == request.params['poll_id']).one()

    c.heading = _('Add question')
    c.mode = 'add'
    c.poll = poll

    return render('/poll/editQuestion.mako')

  @require('Login', 'QuestionID', 'RunningPoll')
  def addAnswer(self):
    question = Session.query(Question).filter(Question.id == request.params['question_id']).one()
    poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == question.poll_id).one()

    c.heading = _('Add answer')
    c.mode = 'add'
    c.poll = poll
    c.question = question

    return render('/poll/editAnswer.mako')

  @require('Login', 'PollID', 'RunningPoll')
  def editPoll(self):
    poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == request.params['poll_id']).one()

    c.heading = _('Edit poll')
    c.mode = 'edit'
    c.poll = poll

    return render('/poll/edit.mako')

  @require('Login', 'PollID', 'RunningPoll')
  def editParticipant(self):
    poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == request.params['poll_id']).one()

    c.heading = _('Edit participant')
    c.mode = 'edit'
    c.poll = poll

    return render('/poll/editParticipant.mako')

  @require('Login', 'QuestionID', 'RunningPoll')
  def editQuestion(self):
    question = Session.query(Question).filter(Question.id == request.params['question_id']).one()
    poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == question.poll_id).one()
    
    c.heading = _('Edit question')
    c.mode = 'edit'
    c.poll = poll
    c.question = question

    return render('/poll/editQuestion.mako')

  @require('Login', 'AnswerID', 'RunningPoll')
  def editAnswer(self):
    answer = Session.query(Answer).filter(Answer.id == request.params['answer_id']).one()
    question = Session.query(Question).filter(Question.id == answer.question_id).one()
    poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == question.poll_id).one()

    poll_id = poll.id
    question_id = question.id

    if question.type == 1:
      flash('error', _('Free text type is not editable'))
      redirect(url(controller='poll', action='editQuestion', poll_id=poll.id, question_id=question.id))

    c.heading = _('Edit answer')
    c.mode = 'edit'
    c.poll = poll
    c.question = question
    c.answer = answer

    return render('/poll/editAnswer.mako')

  @require('POST', 'Login', 'PollParams')
  def doEditPoll(self):
    if request.params['mode'] == 'edit':
      poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == request.params['poll_id']).one()
    else:
      poll = Poll()

    poll.public = (request.params['public'] == 'yes')
    poll.owner = self.uid
    poll.name = request.params['name'].encode('utf8')
    poll.running = 0
    poll.instructions = str(request.params['instructions'].encode('utf-8'))
    poll.expiration_date = request.params['expiration_date']
      
    if request.params['mode'] == 'add':
      Session.add(poll)
      Session.flush()

    mailtext = '''\
        Hey,

        Your vote is requested for "%s".
        You can vote here:
          https://votex.hackerspace.lu:8443/vote/vote?vote_key=%s

        Your voting key is: %s

        The poll expires on %s
        '''

    for v in list(set(request.params['voters'].split('\n'))):
      p = Participant()
      p.poll_id = poll.id
      p.key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))

      msg = MIMEText(mailtext % (poll.name, p.key, p.key, poll.expiration_date), 'plain')
      msg['Subject'] = 'syn2cat - We need you to vote'
      msg['From'] = 'noreply@hackerspace.lu'
      msg['To'] = v

      '''
      s = smtplib.SMTP('localhost')
      s.sendmail(msg['From'], v, msg.as_string())
      s.quit()
      '''

      Session.add(p)

    Session.commit()
    flash('success', _('Poll successfully edited'))
    redirect(url(controller='poll', action='showAll'))
  
  @require('POST', 'Login', 'PollID', 'ParticipantParams')
  def doEditParticipant(self):
    poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == request.params['poll_id']).one()
    Session.query(Participant).filter(Participant.poll_id == poll.id).delete()
    Session.flush()

    voters = request.params['participants'].split('\n')
    for v in voters:
      p = Participant()
      p.poll_id = poll.id
      p.participant = v
      p.key = ''
      Session.add(p)

    Session.commit()
    flash('success', _('Participants successfully edited'))
    redirect(url(controller='poll', action='editPoll', poll_id=poll.id))

  @require('POST', 'Login', 'PollID', 'QuestionParams')
  def doEditQuestion(self):
    if request.params['mode'] == 'edit':
      question = Session.query(Question).filter(Question.id == request.params['question_id']).one()
      poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == question.poll_id).one()
    else:
      poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == request.params['poll_id']).one()
      question = Question()
      question.poll_id = poll.id
      question.mandatory = 1

    question.question = request.params['question'].encode('utf8')

    if request.params['mode'] == 'add':
      if request.params['type'] == 'text':
        question.type = 1
      elif request.params['type'] == 'radio':
        question.type = 2
      elif request.params['type'] == 'check':
        question.type = 3

      Session.add(question)

      if request.params['type'] == 'text':
        Session.flush()
        a = Answer()
        a.question_id = question.id
        a.name = 'freetext'
        Session.add(a)

    Session.commit()
    flash('success', _('Question successfully edited'))
    redirect(url(controller='poll', action='editQuestion', poll_id=poll.id, question_id=question.id))

  @require('POST', 'Login', 'QuestionID', 'PollID', 'AnswerParams')
  def doEditAnswer(self):
    question = Session.query(Question).filter(Question.id == request.params['question_id']).one()
    poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == request.params['poll_id']).one()

    if question.type == 1:
      flash('error', _('Free text type is not editable'))
      redirect(url(controller='poll', action='editQuestion', 
                   poll_id=request.params['poll_id'], question_id=request.params['question_id']))

    if request.params['mode'] == 'edit':
      answer = Session.query(Answer).filter(Answer.id == request.params['answer_id']).one()
    else:
      answer = Answer()
      answer.question_id = question.id

    answer.name = request.params['answer'].encode('utf8')

    if request.params['mode'] == 'add':
      Session.add(answer)

    Session.commit()

    flash('success', _('Answer successfully edited'))
    redirect(url(controller='poll', action='editQuestion', poll_id=request.params['poll_id'], question_id=request.params['question_id']))

  @require_login
  def showResults(self):
    if (not 'poll_id' in request.params):
      redirect(url(controller='poll', action='showAll'))

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

  @require('Login', 'PollID', 'RunningPoll')
  def deletePoll(self):
    poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == request.params['poll_id']).one()
    Session.query(Vote).filter(Vote.poll_id == poll.id).delete()

    Session.delete(poll)
    Session.commit()

    flash('success', _('Poll successfully deleted'))
    redirect(url(controller='poll', action='showAll'))

  @require('Login', 'QuestionID', 'PollID', 'RunningPoll')
  def deleteQuestion(self):
    question = Session.query(Question).filter(Question.id == request.params['question_id']).one()
    poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == question.poll_id).one()

    Session.delete(question)
    Session.commit()

    flash('success', _('Question successfully deleted'))
    redirect(url(controller='poll', action='editPoll', poll_id=request.params['poll_id']))

  @require('Login', 'QuestionID', 'AnwserID', 'RunningPoll')
  def deleteAnswer(self):
    answer = Session.query(Answer).filter(Answer.id == request.params['answer_id']).one()
    question = Session.query(Question).filter(Question.id == answer.question_id).one()
    poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == question.poll_id).one()
    poll_id = poll.id

    if question.type == 1:
      flash('error', _('Free text type is not editable'))
      redirect(url(controller='poll', action='editQuestion', poll_id=poll.id, question_id=question.id))

    Session.delete(answer)
    Session.commit()
    flash('success', _('Answer successfully deleted'))
    redirect(url(controller='poll', action='editQuestion', poll_id=poll_id, question_id=request.params['question_id']))


#---- Validator(s) --------------------------------------------------------------------------------


  def _validatePollID(self):
    if not 'poll_id' in request.params:
      raise Exception("Poll id required but not found in request")

    if not re.match(r'^\d+$', request.params.get('poll_id', '')):
      raise Exception("Poll id should be numeric")

  def _validateQuestionID(self):
    if not 'question_id' in request.params:
      raise Exception("Question id required but not found in request")

    if not re.match(r'^\d+$', request.params.get('question_id', '')):
      raise Exception("Question id should be numeric")

  def _validateRunningPoll(self):
    poll_id = request.params.get('poll_id', '')

    try:        
      poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == poll_id).one()
    except:
      # re-raise exception with custom message.
      # exception will be catched by BaseController,
      # see BaseController.onError for default behavior
      raise Exception(_('Poll does not exist')) 

    if poll.running > 0 and not config['debug']:
      raise Exception(_('Connot edit a running poll'))

  def _validatePollParams(self):
    # @TODO request.params may contain multiple values per key... test & fix
    modeEdit = (request.params.get('mode', '') == 'edit')
    errors = []

    if not re.match(r'^(add|edit)$', request.params.get('mode', '')):
      errors.append(_('Invalid form data'))

    if modeEdit and not re.match(r'^\d+$', request.params.get('poll_id', '')):
      errors.append(_('Invalid form data'))

    name_len = len(request.params.get('name', ''))
    if not modeEdit and not (name_len > 0 and name_len < 255):
      errors.append(_('Invalid name'))

    instructions_len = len(request.params.get('instructions', ''))
    if not (instructions_len > 0 and instructions_len < 1000):
      errors.append(_('Invalid instructions'))

    if not config['debug']:
      if request.params.get('voters', '') == '':
        errors.append(_('Invalid voters'))
      else:
        # @TODO this is not enough ... need more checks
        voters = request.params['voters'].split('\n')
        for v in voters:
          if not re.match(r'\b[A-Z0-9._%+-]+@(?:[A-Z0-9-]+\.)+[A-Z]{2,4}\b', v, re.I):
            errors.append(_('Invalid voters'))
            break

    if not 'expiration_date' in request.params or not re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', request.params['expiration_date']):
      errors.append(_('Invalid expiration date'))

    if not re.match(r'^(yes|no)$', request.params.get('public', '')):
      errors.append(_('Invalid public'))

    if len(errors) > 0:
      session['errors'] = errors
      session['reqparams'] = {}
      
      # @TODO request.params may contain multiple values per key... test & fix
      for k in request.params.iterkeys():
        session['reqparams'][k] = request.params[k]          
      session.save()
      
      if request.params['mode'] == 'add':
        redirect(url(controller='poll', action='addPoll'))
      else:
        redirect(url(controller='poll', action='editPoll', poll_id=request.params['poll_id']))

  def _validateParticipantParams(self):
    errors = []

    if request.params.get('participants', '') == '':
      errors.append(_('Invalid participants'))
    else:
      # @TODO this is not enough ... need more checks
      voters = request.params['participants'].split('\n')
      for v in voters:
        if not re.match(r'\b[A-Z0-9._%+-]+@(?:[A-Z0-9-]+\.)+[A-Z]{2,4}\b', v, re.I):
          errors.append(_('Invalid participants'))
          break

    if len(errors) > 0:
      session['errors'] = errors
      session['reqparams'] = {}
      
      # @TODO request.params may contain multiple values per key... test & fix
      for k in request.params.iterkeys():
        session['reqparams'][k] = request.params[k]          
      session.save()
      
      redirect(url(controller='poll', action='editParticipant', poll_id=request.params['poll_id']))

  def _validateQuestionParams(self):
    # @TODO request.params may contain multiple values per key... test & fix
    errors = []
    modeEdit = (request.params.get('mode', '') == 'edit')

    if not re.match(r'^\d+$', request.params.get('poll_id', '')):
      errors.append(_('Invalid form data'))

    if not re.match(r'^(add|edit)$', request.params.get('mode', '')):
      errors.append(_('Invalid form data'))

    if modeEdit and not re.match(r'^\d+$', request.params.get('question_id', '')):
      errors.append(_('Invalid form data'))
      # @TODO what do we do if no question id has been submitted but a form ?... add checks

    question_len = len(request.params.get('question', ''))
    if not (question_len > 0 and question_len < 255):
      errors.append(_('Invalid question text'))

    if not modeEdit and not re.match(r'(^text|radio|check)$', request.params.get('type', '')):
      errors.append(_('Invalid type'))

    if len(errors) > 0:
      session['errors'] = errors
      session['reqparams'] = {}

      # @TODO request.params may contain multiple values per key... test & fix
      for k in request.params.iterkeys():
        session['reqparams'][k] = request.params[k]
          
      session.save()
      if request.params.get('mode', '') == 'edit':
         redirect(url(controller='poll', action='editQuestion', poll_id=request.params['poll_id'], 
                   question_id=request.params['question_id']))
      else:
         redirect(url(controller='poll', action='addQuestion', poll_id=request.params['poll_id']))
    
  def _validateAnswerParams(self):
    # @TODO request.params may contain multiple values per key... test & fix
    errors = []
    modeEdit = (request.params.get('mode', '') == 'edit')

    if not re.match(r'^\d+$', request.params.get('poll_id', '')):
      errors.append(_('Invalid form data'))

    if not re.match(r'^\d+$', request.params.get('question_id', '')):      
      errors.append(_('Invalid form data'))

    if not re.match(r'^(add|edit)$', request.params.get('mode', '')):
      errors.append(_('Invalid form data'))

    if modeEdit and not re.match(r'^\d+$', request.params.get('answer_id', '')):
      errors.append(_('Invalid form data'))
      # @TODO what do we do if no question id has been submitted but a form ?... add checks

    answer_len = len(request.params.get('answer', ''))
    if not (answer_len > 0 and answer_len < 255):
      errors.append(_('Invalid answer text'))

    if len(errors) > 0:
      session['errors'] = errors
      session['reqparams'] = {}

      # @TODO request.params may contain multiple values per key... test & fix
      for k in request.params.iterkeys():
        session['reqparams'][k] = request.params[k]          
      
      session.save()

      if request.params['mode'] == 'add':
        redirect(url(controller='poll', action='addAnswer', poll_id=request.params['poll_id'], 
                     question_id=request.params['question_id']))
      else:
        redirect(url(controller='poll', action='editAnswer', poll_id=request.params['poll_id'], 
                     question_id=request.params['question_id'], answer_id=request.params['answer_id']))
      
