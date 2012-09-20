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


import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import redirect
from pylons import config

from votex.lib.base import BaseController, render, Session
from votex.model.main import Poll, Question, Answer, Participant, Submission

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
        try:
          s.name = s.name.encode('ascii','ignore')
        except:
          s.name ='poo...frickin P000000'

        c.polls.append(s)
    except NoResultFound:
      print 'No such poll'

    return render('/poll/showAll.mako')

  @needLogin
  def addPoll(self):
    c.mode = 'add'

    return render('/poll/edit.mako')

  @needLogin
  def addQuestion(self):
    if (not 'poll_id' in request.params):
      redirect(url(controller='poll', action='showAll'))

    try:
      poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == request.params['poll_id']).one()

      c.heading = _('Add question')
      c.mode = 'add'
      c.poll = poll

      return render('/poll/editQuestion.mako')
    except:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      pass

    redirect(url(controller='poll', action='showAll'))

  @needLogin
  def addAnswer(self):
    if (not 'question_id' in request.params):
      redirect(url(controller='poll', action='showAll'))

    try:
      question = Session.query(Question).filter(Question.id == request.params['question_id']).one()
      poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == question.poll_id).one()

      c.heading = _('Add answer')
      c.mode = 'add'
      c.poll = poll
      c.question = question

      return render('/poll/editAnswer.mako')
    except:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      pass

    redirect(url(controller='poll', action='showAll'))

  @needLogin
  def editPoll(self):
    if (not 'poll_id' in request.params):
      redirect(url(controller='poll', action='showAll'))

    try:
      poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == request.params['poll_id']).one()

      c.heading = _('Edit poll')
      c.mode = 'edit'

      if len(poll.submissions) > 0:
        session['flash'] = _('Cannot edit a running poll')
        session['flash_class'] = 'error'
        session.save()
        redirect(url(controller='poll', action='showAll'))

      c.poll = poll

      return render('/poll/edit.mako')
    except:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      pass

    redirect(url(controller='poll', action='showAll'))

  @needLogin
  def editQuestion(self):
    if (not 'question_id' in request.params):
      redirect(url(controller='poll', action='showAll'))

    try:
      question = Session.query(Question).filter(Question.id == request.params['question_id']).one()
      poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == question.poll_id).one()

      c.heading = _('Edit question')
      c.mode = 'edit'

      if len(poll.submissions) > 0:
        session['flash'] = _('Cannot edit a running poll')
        session['flash_class'] = 'error'
        session.save()
        redirect(url(controller='poll', action='showAll'))

      c.poll = poll
      c.question = question

      return render('/poll/editQuestion.mako')
    except:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      pass

    redirect(url(controller='poll', action='showAll'))

  @needLogin
  def editAnswer(self):
    if (not 'answer_id' in request.params):
      redirect(url(controller='poll', action='showAll'))

    try:
      answer = Session.query(Answer).filter(Answer.id == request.params['answer_id']).one()
      question = Session.query(Question).filter(Question.id == answer.question_id).one()
      poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == question.poll_id).one()

      c.heading = _('Edit answer')
      c.mode = 'edit'

      if len(poll.submissions) > 0:
        session['flash'] = _('Cannot edit a running poll')
        session['flash_class'] = 'error'
        session.save()
        redirect(url(controller='poll', action='showAll'))

      c.poll = poll
      c.question = question
      c.answer = answer

      return render('/poll/editAnswer.mako')
    except:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
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

  def _checkQuestion(f):
    def new_f(self):
      # @TODO request.params may contain multiple values per key... test & fix
      formok = True
      errors = []

      if not 'poll_id' in request.params or not re.match(r'^\d+$', request.params['poll_id']):
        formok = False
        errors.append(_('Invalid form data'))

      if not 'mode' in request.params or (request.params['mode'] != 'add' and request.params['mode'] != 'edit'):
        formok = False
        errors.append(_('Invalid form data'))

      if request.params['mode'] == 'edit' and (not 'question_id' in request.params or request.params['question_id'] == '' or not re.match(r'^\d+$', request.params['question_id'])):
        formok = False
        errors.append(_('Invalid form data'))
        # @TODO what do we do if no question id has been submitted but a form ?... add checks

      if not 'question' in request.params or request.params['question'] == '' or len(request.params['question']) > 255:
        formok = False
        errors.append(_('Invalid question text'))

      if  request.params['mode'] == 'add' and (not 'type' in request.params or (request.params['type'] != 'text' and request.params['type'] != 'radio' and request.params['type'] != 'check')):
        formok = False
        errors.append(_('Invalid type'))

      if not formok:
        session['errors'] = errors
        session['reqparams'] = {}

        # @TODO request.params may contain multiple values per key... test & fix
        for k in request.params.iterkeys():
          session['reqparams'][k] = request.params[k]
          
        session.save()

        if request.params['mode'] == 'add':
          redirect(url(controller='poll', action='addQuestion'))
        else:
          redirect(url(controller='poll', action='editQuestion'))

      return f(self)
    return new_f

  def _checkAnswer(f):
    def new_f(self):
      # @TODO request.params may contain multiple values per key... test & fix
      formok = True
      errors = []

      if not 'poll_id' in request.params or not re.match(r'^\d+$', request.params['poll_id']):
        formok = False
        errors.append(_('Invalid form data'))

      if not 'question_id' in request.params or not re.match(r'^\d+$', request.params['question_id']):
        formok = False
        errors.append(_('Invalid form data'))

      if not 'mode' in request.params or (request.params['mode'] != 'add' and request.params['mode'] != 'edit'):
        formok = False
        errors.append(_('Invalid form data'))

      if request.params['mode'] == 'edit' and (not 'answer_id' in request.params or request.params['answer_id'] == '' or not re.match(r'^\d+$', request.params['answer_id'])):
        formok = False
        errors.append(_('Invalid form data'))
        # @TODO what do we do if no question id has been submitted but a form ?... add checks

      if not 'answer' in request.params or request.params['answer'] == '' or len(request.params['answer']) > 255:
        formok = False
        errors.append(_('Invalid question text'))


      if not formok:
        session['errors'] = errors
        session['reqparams'] = {}

        # @TODO request.params may contain multiple values per key... test & fix
        for k in request.params.iterkeys():
          session['reqparams'][k] = request.params[k]
          
        session.save()

        if request.params['mode'] == 'add':
          redirect(url(controller='poll', action='addAnswer'))
        else:
          redirect(url(controller='poll', action='editAnswer'))

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
      poll.name = request.params['name'].encode('utf8')
      poll.instructions = str(request.params['instructions'].encode('utf-8'))
      poll.expiration_date = request.params['expiration_date']

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
        p = None
        p = Participant()
        p.poll_id = poll.id
        p.key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))
        mailtext = '''\
        Hey,

        Your vote is requested for "%s".
        You can vote here:
          https://votex.hackerspace.lu:8443/vote/vote?vote_key=%s

        Your voting key is: %s

        The poll expires on %s
        ''' %\
        (poll.name, p.key, p.key, poll.expiration_date)

        msg = MIMEText(mailtext, 'plain')
        msg['Subject'] = 'syn2cat - We need you to vote'
        msg['From'] = 'noreply@hackerspace.lu'
        msg['To'] = v
        s = smtplib.SMTP('localhost')
        s.sendmail(msg['From'], v, msg.as_string())
        s.quit()

        Session.add(p)

      Session.commit()

      session['flash'] = _('Poll successfully edited')
      session.save()

      redirect(url(controller='poll', action='showAll'))
    except LookupError:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      print 'No such user !'
      session['flash'] = _('Failed to add poll')
      session['flash_class'] = 'error'
      session.save()
    except:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)

    redirect(url(controller='poll', action='showAll'))

  @needLogin
  @_checkQuestion
  @restrict('POST')
  def doEditQuestion(self):
    transaction_ok = False

    try:
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

      Session.commit()

      session['flash'] = _('Question successfully edited')
      session.save()

      transaction_ok = True
    except LookupError:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      session['flash'] = _('Failed to add question')
      session['flash_class'] = 'error'
      session.save()
    except:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)

    if transaction_ok:
      redirect(url(controller='poll', action='editQuestion', poll_id=poll.id, question_id=question.id))
    else:
      redirect(url(controller='poll', action='editPoll', poll_id=poll.id))

  @needLogin
  @_checkAnswer
  @restrict('POST')
  def doEditAnswer(self):
    try:
      question = Session.query(Question).filter(Question.id == request.params['question_id']).one()
      poll = Session.query(Poll).filter(Poll.owner == self.uid).filter(Poll.id == request.params['poll_id']).one()

      if request.params['mode'] == 'edit':
        answer = Session.query(Answer).filter(Answer.id == request.params['answer_id']).one()
      else:
        answer = Answer()
        answer.question_id = question.id

      answer.name = request.params['answer'].encode('utf8')

      if request.params['mode'] == 'add':
        Session.add(answer)

      Session.commit()

      session['flash'] = _('Answer successfully edited')
      session.save()
    except LookupError:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      session['flash'] = _('Failed to add answer')
      session['flash_class'] = 'error'
      session.save()
    except:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)

    redirect(url(controller='poll', action='editQuestion', poll_id=request.params['poll_id'], question_id=request.params['question_id']))

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
