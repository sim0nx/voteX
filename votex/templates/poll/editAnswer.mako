<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
  if 'reqparams' in s:
    if var in s['reqparams']:
      return s['reqparams'][var]

  if hasattr(c, 'answer'):
    if var in vars(c.answer):
      return vars(c.answer)[var]

  return ''
%>

<h3>${c.heading}</h3>
${parent.flash()}
<a href="${url(controller='poll', action='editQuestion', poll_id=c.poll.id, question_id=c.question.id)}">Back to question</a>

<form method="post" action="${url(controller='poll', action='doEditAnswer')}" name="recordform" class="form-horizontal">
  <div class="control-group">
    <label class="control-label">${_('Answer')}</label>
    <div class="controls">
      <textarea rows='10' cols='60' name="answer">${getFormVar(session, c, 'name')}</textarea>
    </div>
  </div>

  <input type="hidden" name="mode" value="${c.mode}">
  <input type="hidden" name="poll_id" value="${c.poll.id}">
  <input type="hidden" name="question_id" value="${c.question.id}">
  % if c.mode is 'edit':
  <input type="hidden" name="answer_id" value="${c.answer.id}">
  % endif

  <div class="control-group">
    <div class="controls">
      <button type="submit" class="btn">${_('Submit')}</button>
    </div>
  </div>
</form>

<div id="make-space" class="prepend-top">&nbsp;</div>

<%
if 'reqparams' in session:
  del session['reqparams']
  session.save()
%>
