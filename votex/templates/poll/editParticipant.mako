<%inherit file="/base.mako" />

<%

if 'reqparams' in session and 'participants' in session['reqparams']:
  participants = session['reqparams']['participants']
else:
  participants = ''

  if len(c.poll.participants) > 0:
    for k in c.poll.participants:
      if not k.participant:
        continue

      if not participants == '':
        participants += '\n'

      participants += k.participant
%>

<form method="post" action="${url(controller='poll', action='doEditParticipant')}" name="recordform">

<div id="content" class="span-18 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${_('Edit participants')}</header>
<article>
<a href="${url(controller='poll', action='editPoll', poll_id=c.poll.id)}">Back to poll</a>

<table class="table_content">
  ${parent.all_messages()}
  <tr>
    <td class="table_title">
      ${_('Participants (separate by new-line)')}
   </td>
    <td>
      <textarea rows='10' cols='60' name="participants">${participants}</textarea>
    </td>
  </tr>
</table>

<input type="hidden" name="mode" value="${c.mode}">
<input type="hidden" name="poll_id" value="${c.poll.id}">
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
