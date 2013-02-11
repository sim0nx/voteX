<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
  if 'reqparams' in s:
    if var in s['reqparams']:
      return s['reqparams'][var]

  if hasattr(c, 'question'):
    if var in vars(c.question):
      return vars(c.question)[var]

  return ''
%>

<%
type_text = ''
type_radio = ''
type_check = ''
type_disabled = ''

if c.mode == 'edit':
  type_disabled = 'disabled'

  if c.question.type == 1:
    type_text = 'checked'
  elif c.question.type == 2:
    type_radio = 'checked'
  elif c.question.type == 3:
    type_check = 'checked'
  else:
    type_text = 'checked'
else:
  m_type = getFormVar(session, c, 'type')
  if m_type == 'text':
    type_text = 'checked'
  elif m_type == 'radio':
    type_radio = 'checked'
  elif m_type == 'check':
    type_check = 'checked'
  else:
    type_text = 'checked'

%>

<h3>${c.heading}</h3>
${parent.flash()}
<a href="${url(controller='poll', action='editPoll', poll_id=c.poll.id)}">Back to poll</a>

<form method="post" action="${url(controller='poll', action='doEditQuestion')}" name="recordform" class="form-horizontal">

  <div class="control-group">
    <label class="control-label">${_('Question')}</label>
    <div class="controls">
      <textarea rows='10' cols='60' name="question">${getFormVar(session, c, 'question')}</textarea>
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Type')}</label>
    <div class="controls">
      <input type="radio" name="type" value="text" ${type_text} ${type_disabled}>${_('free text')}<br/>
      <input type="radio" name="type" value="radio" ${type_radio} ${type_disabled}>${_('single choice')}<br/>
      <input type="radio" name="type" value="check" ${type_check} ${type_disabled}>${_('multiple choice')}<br/>
    </div>
  </div>

  <input type="hidden" name="mode" value="${c.mode}">
  <input type="hidden" name="poll_id" value="${c.poll.id}">
  % if c.mode is 'edit':
  <input type="hidden" name="question_id" value="${c.question.id}">
  % endif

  <div class="control-group">
    <div class="controls">
      <button type="submit" class="btn">${_('Submit')}</button>
    </div>
  </div>
</form>

% if c.mode is 'edit':
<a href="${url(controller='poll', action='addAnswer', poll_id=c.poll.id, question_id=c.question.id)}">Add answer</a>

<table class="table table-striped">
  <thead>
    <tr>
      <th>${_('Answer')}</th>
      <th>${_('Options')}</th>
    </tr>
  </thead>
  <tbody>
    % for a in c.question.answers:
    <tr>
      <td>
        ${a.name}
      </td>
      <td>
        <a href="${url(controller='poll', action='editAnswer', poll_id=c.poll.id, answer_id=a.id)}">edit</a>
        <a href="${url(controller='poll', action='deleteAnswer', poll_id=c.poll.id, question_id=a.question_id, answer_id=a.id)}">delete</a>
      </td>
    </tr>
    % endfor
  </tbody>
</table>
% endif

<div id="make-space" class="prepend-top">&nbsp;</div>

<%
if 'reqparams' in session:
  del session['reqparams']
  session.save()
%>
