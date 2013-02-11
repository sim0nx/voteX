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

<h3>${c.heading}</h3>
${parent.flash()}
<a href="${url(controller='poll', action='editPoll', poll_id=c.poll.id)}">Back to poll</a>

<form method="post" action="${url(controller='poll', action='doEditParticipant')}" name="recordform" class="form-horizontal">

  <div class="control-group">
    <label class="control-label">${_('Participants (separate by new-line)')}</label>
    <div class="controls">
      <textarea rows='10' cols='60' name="participants">${participants}</textarea>
    </div>
  </div>

  <input type="hidden" name="mode" value="${c.mode}">
  <input type="hidden" name="poll_id" value="${c.poll.id}">

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
