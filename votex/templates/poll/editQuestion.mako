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
%>

<form method="post" action="${url(controller='poll', action='doEditQuestion')}" name="recordform">

<div id="content" class="span-18 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${_('Add question')}</header>
<article>
<a href="${url(controller='poll', action='editPoll', poll_id=c.poll.id)}">Back to poll</a>

<table class="table_content">
  ${parent.all_messages()}
  <tr>
    <td class="table_title">
      ${_('Question')}
   </td>
    <td>
      <textarea rows='10' cols='60' name="question">${getFormVar(session, c, 'question')}</textarea>
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Type')}
    </td>
    <td>
      <input type="radio" name="type" value="text" ${type_text} ${type_disabled}>${_('free text')}<br/>
      <input type="radio" name="type" value="radio" ${type_radio} ${type_disabled}>${_('single choice')}<br/>
      <input type="radio" name="type" value="check" ${type_check} ${type_disabled}>${_('multiple choice')}<br/>
    </td>
  </tr>
</table>

<input type="hidden" name="mode" value="${c.mode}">
<input type="hidden" name="poll_id" value="${c.poll.id}">
% if c.mode is 'edit':
<input type="hidden" name="question_id" value="${c.question.id}">
% endif
<input type="submit" name="" value="${_('Submit')}" class="input button right"> 
</form>

% if c.mode is 'edit':
<a href="${url(controller='poll', action='addAnswer', poll_id=c.poll.id, question_id=c.question.id)}">Add answer</a>

<table>
  % for a in c.question.answers:
  <tr>
    <td>
      ${_('Answer')}
    </td>
    <td>
      ${a.name}
    </td>
    <td>
      <a href="${url(controller='poll', action='editAnswer', poll_id=c.poll.id, answer_id=a.id)}">edit</a>
      <a href="${url(controller='poll', action='deleteAnswer', poll_id=c.poll.id, question_id=a.question_id, answer_id=a.id)}">delete</a>
    </td>
  </tr>
  % endfor
</table>

% endif

</article>
<div id="make-space" class="prepend-top">&nbsp;</div>
</div>

<%
if 'reqparams' in session:
  del session['reqparams']
  session.save()
%>
