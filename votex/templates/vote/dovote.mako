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


<form method="post" action="${url(controller='vote', action='doVote')}" name="recordform">

<div id="content" class="span-18 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${_('Cast your vote')}</header>
<article>
<table class="table_content">
	${parent.all_messages()}
        <tr>
                <td class="table_title">
                        ${_('Name')}
                </td>
		<td>
			${c.poll.name}
		</td>
	</tr>
	<tr>
    <td class="table_title">
      ${_('Instructions')}
    </td>
		<td>
      % for l in c.poll.instructions.split('\n'):
			${l}<br/>
			% endfor
		</td>
       	</tr>
	<tr>
                <td class="table_title">
                        ${_('Vote')}
                </td>
		% if c.poll.type == 'complex':
		<td>
			<textarea rows='10' cols='60' name="vote">${getFormVar(session, c, 'vote')}</textarea>
		</td>
		% else:
		<td>
			<input type="radio" name="vote" value="yes">Yes<br/>
			<input type="radio" name="vote" value="no">No<br/>
			% if c.poll.type == 'yesnonull':
			<input type="radio" name="vote" value="null">Null<br/>
			% endif
		</td>
		% endif
       	</tr>
</table>

<input type="hidden" name="vote_key" value="${c.vote_key}">
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
