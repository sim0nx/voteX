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
poll_type_yesno = ''
poll_type_yesnonull = ''
poll_type_complex = ''

public_yes = ''
public_no = ''

if c.mode == 'edit':
	if c.poll.type == 'yesno':
		poll_type_yesno = 'checked'
	elif c.poll.type == 'yesnonull':
		poll_type_yesnonull = 'checked'
	elif c.poll.type == 'complex':
		poll_type_complex = 'checked'

	if c.poll.public:
		public_yes = 'checked'
	else:
		public_no = 'checked'
%>

<form method="post" action="${url(controller='poll', action='doEditPoll')}" name="recordform">

<div id="content" class="span-18 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${_('Add poll')}</header>
<article>
<table class="table_content">
	${parent.all_messages()}
        <tr>
                <td class="table_title">
                        ${_('Name')}
                </td>
		<td>
			% if c.mode is 'add':
			<input type="text" name="name" value="${getFormVar(session, c, 'name')}" class="input text">
			% else:
			${c.poll.name}
			% endif
		</td>
	</tr>
	<tr>
                <td class="table_title">
                        ${_('Instructions')}
                </td>
		<td>
			% if c.mode is 'add':
			<textarea rows='10' cols='60' name="instructions">${getFormVar(session, c, 'instructions')}</textarea>
			% else:
			<textarea rows='10' cols='60' name="instructions" disabled>${getFormVar(session, c, 'instructions')}</textarea>
			% endif
		</td>
       	</tr>
	<tr>
                <td class="table_title">
                        ${_('Voters (separate by new-line)')}
                </td>
		<td>
			% if c.mode is 'add':
			<textarea rows='10' cols='60' name="voters">${getFormVar(session, c, 'voters')}</textarea>
			% else:
			<textarea rows='10' cols='60' name="voters" disabled>${getFormVar(session, c, 'voters')}</textarea>
			% endif
		</td>
       	</tr>
        <tr>
                <td class="table_title">
                        ${_('Expiration Date')} (YYYY-MM-DD HH:MM)
                </td>
                <td>
                        <input type="text" name="expiration_date" value="${getFormVar(session, c, 'expiration_date')}" class="input text">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Type')}
                </td>
                <td>
			<input type="radio" name="type" value="yesno" ${poll_type_yesno}>Yes/No<br/>
       			<input type="radio" name="type" value="yesnonull" ${poll_type_yesnonull}>Yes/No/Null<br/>
			<input type="radio" name="type" value="complex" ${poll_type_complex}>Complex<br/>
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Public')}
                </td>
                <td>
			<input type="radio" name="public" value="yes" ${public_yes}>Yes<br/>
       			<input type="radio" name="public" value="no" ${public_no}>No<br/>
                </td>
        </tr>
</table>

<input type="hidden" name="mode" value="${c.mode}">
% if c.mode is 'edit':
<input type="hidden" name="poll_id" value="${c.poll.id}">
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
