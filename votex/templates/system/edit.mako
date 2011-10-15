<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
	if 'reqparams' in s:
		if var in s['reqparams']:
			return s['reqparams'][var]

	if hasattr(c, 'system'):
		if var in vars(c.system):
			return vars(c.system)[var]

	return ''
%>

<%
system_type_yesno = ''
system_type_yesnonull = ''
system_type_complex = ''

public_yes = ''
public_no = ''

if c.mode == 'edit':
	if c.system.type == 'yesno':
		system_type_yesno = 'checked'
	elif c.system.type == 'yesnonull':
		system_type_yesnonull = 'checked'
	elif c.system.type == 'complex':
		system_type_complex = 'checked'

	if c.system.public:
		public_yes = 'checked'
	else:
		public_no = 'checked'
%>

<form method="post" action="${url(controller='system', action='doEditSystem')}" name="recordform">

<div id="content" class="span-18 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${_('Add system')}</header>
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
			${c.system.name}
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
			<input type="radio" name="type" value="yesno" ${system_type_yesno}>Yes/No<br/>
       			<input type="radio" name="type" value="yesnonull" ${system_type_yesnonull}>Yes/No/Null<br/>
			<input type="radio" name="type" value="complex" ${system_type_complex}>Complex<br/>
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
<input type="hidden" name="system_id" value="${c.system.id}">
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
