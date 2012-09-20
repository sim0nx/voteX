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

<form method="post" action="${url(controller='poll', action='doEditAnswer')}" name="recordform">

<div id="content" class="span-18 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${_('Add answer')}</header>
<article>
<a href="${url(controller='poll', action='editQuestion', poll_id=c.poll.id, question_id=c.question.id)}">Back to question</a>

<table class="table_content">
  ${parent.all_messages()}
  <tr>
    <td class="table_title">
      ${_('Answer')}
   </td>
    <td>
      <textarea rows='10' cols='60' name="answer">${getFormVar(session, c, 'name')}</textarea>
    </td>
  </tr>
</table>

<input type="hidden" name="mode" value="${c.mode}">
<input type="hidden" name="poll_id" value="${c.poll.id}">
<input type="hidden" name="question_id" value="${c.question.id}">
% if c.mode is 'edit':
<input type="hidden" name="answer_id" value="${c.answer.id}">
% endif
<input type="submit" name="" value="${_('Submit')}" class="input button right"> 
</form>


</article>
<div id="make-space" class="prepend-top">&nbsp;</div>
</div>

<%
if 'reqparams' in session:
  del session['reqparams']
  session.save()
%>
