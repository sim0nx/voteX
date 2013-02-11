<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
	if 'reqparams' in s:
		if var in s['reqparams']:
			return s['reqparams'][var]

	if hasattr(c, 'poll'):
		if var in vars(c.poll):
			return vars(c.poll)[var]

	return ''
%>

<%
public_yes = ''
public_no = ''

if c.mode == 'edit':
	if c.poll.public:
		public_yes = 'checked'
	else:
		public_no = 'checked'
%>

<h3>${c.heading}</h3>

<form method="post" action="${url(controller='poll', action='doEditPoll')}" name="recordform" class="form-horizontal">
  <div class="control-group">
    <label class="control-label">${_('Name')}</label>
    <div class="controls">
    % if c.mode == 'add':
    <input type="text" name="name" value="${getFormVar(session, c, 'name')}" class="input text">
    % else:
    ${c.poll.name}
    % endif
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Instructions')}</label>
    <div class="controls">
      <textarea rows='10' cols='60' name="instructions">${getFormVar(session, c, 'instructions')}</textarea>
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Participants')}</label>
    <div class="controls">
 			% if c.mode == 'edit':
        <a href="${url(controller='poll', action='editParticipant', poll_id=c.poll.id)}">Edit participants</a><br/>
        % if len(c.poll.participants) > 0:
          % for k in c.poll.participants:
            % if not k.mail_sent:
              <p class="text-error">${k.participant}</p>
            % else:
              <p class="text-success">${k.participant}</p>
            % endif
          % endfor
        % endif
			% endif
   </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Expiration Date')} (YYYY-MM-DD HH:MM:SS)</label>
    <div class="controls">
      <input type="text" name="expiration_date" value="${getFormVar(session, c, 'expiration_date')}" class="input text">
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Public')}</label>
    <div class="controls">
      <input type="radio" name="public" value="yes" ${public_yes}>Yes<br/>
      <input type="radio" name="public" value="no" ${public_no}>No<br/>
    </div>
  </div>

  <input type="hidden" name="mode" value="${c.mode}">
  % if c.mode is 'edit':
  <input type="hidden" name="poll_id" value="${c.poll.id}">
  % endif

  <div class="control-group">
    <div class="controls">
      <button type="submit" class="btn">${_('Submit')}</button>
    </div>
  </div>
</form>

% if c.mode is 'edit':
Questions:
<a href="${url(controller='poll', action='addQuestion', poll_id=c.poll.id)}">Add question</a>

  % for q in c.poll.questions:
<table class="table table-striped">
  <thead>
    <tr>
      <th>${_('Question')}</th>
      <th>${q.question}</th>
      <th>
        <a href="${url(controller='poll', action='editQuestion', poll_id=c.poll.id, question_id=q.id)}">${_('edit')}</a>
        <a href="${url(controller='poll', action='deleteQuestion', poll_id=c.poll.id, question_id=q.id)}">${_('delete')}</a>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        ${_('Type')}
      </td>
      <td>
      % if q.type == 1:
        free text
      % elif q.type == 2:
        single choice
      % elif q.type == 3:
        multiple choice
      % endif
      </td>
    </tr>
      % for a in q.answers:
    <tr>
      <td>
        ${_('Name')}
      </td>
      <td>
        ${a.name}
      </td>
    </tr>
    % endfor
  </tbody>
</table>
  % endfor
% endif

<div id="make-space" class="prepend-top">&nbsp;</div>

<%
if 'reqparams' in session:
	del session['reqparams']
	session.save()
%>
