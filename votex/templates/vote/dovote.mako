# -*- coding: utf-8 -*-
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

<h3>${c.heading}</h3>

<form method="post" action="${url(controller='vote', action='doVote')}" name="recordform">

<table class="table">
	${parent.all_messages()}
  <tr>
    <td>
      ${_('Name')}
    </td>
		<td>
			${c.poll.name}
		</td>
	</tr>
	<tr>
    <td>
      ${_('Instructions')}
    </td>
		<td>
      % for l in c.poll.instructions.split('\n'):
			${l}<br/>
			% endfor
		</td>
  </tr>
</table>

% for q in c.poll.questions:
<table class="table table-striped">
  <thead>
    <tr>
      <th>
        ${q.question}
      </th>
      <th>&nbsp;</th>
    </tr>
  </thead>
  <tbody>
    % for a in q.answers:
    <tr>
      <td>
        % if q.type == 1:
        <textarea rows='10' cols='60' name="question_t_${q.id}_${a.id}"></textarea>
        % elif q.type == 2:
        <input type="radio" name="question_r_${q.id}" value="${a.id}">${a.name}<br/>
        % elif q.type == 3:
        <input type="checkbox" name="question_c_${q.id}_${a.id}" value="${a.id}">${a.name}<br/>
        % endif
      </td>
    </tr>
    % endfor
  </tbody>
</table>
% endfor

  <input type="hidden" name="vote_key" value="${c.vote_key}">

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
