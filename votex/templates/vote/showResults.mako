<%inherit file="/base.mako" />

<div id="content" class="span-18 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${_('Results')}</header>
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
			${c.poll.instructions}
		</td>
       	</tr>
        <tr>
                <td class="table_title">
                        ${_('Expiration Date')} (YYYY-MM-DD HH:MM)
                </td>
                <td>
			${c.poll.expiration_date}
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Type')}
                </td>
                <td>
			${c.poll.type}
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Public')}
                </td>
                <td>
			${c.poll.public}
                </td>
        </tr>
</table>

Results:
<table class="table_content">
	% for k, v in c.votes.items():
	<tr>
		<td class="table_title">${k}</td>
		<td>${v}</td>
	</tr>
	% endfor
</table>

</article>
<div id="make-space" class="prepend-top">&nbsp;</div>
</div>

<%
if 'reqparams' in session:
	del session['reqparams']
	session.save()
%>
