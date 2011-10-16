<%inherit file="/base.mako" />

<div id="content" class="span-19 push-1 last ">
	<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
		<article>
			<li><table class="table_content"> 
				${parent.flash()}
			        <tr> 
			                <th class="table_title">
			                        #
			                </th>
			                <th class="table_title">
			                        ${_('Name')}
			                </th>
			                <th class="table_title">
			                        ${_('Expiration Date')}
			                </th>
			                <th class="table_title">
			                        ${_('Type')}
			                </th>
			                <th class="table_title">
			                        ${_('Public')}
			                </th>
					<th colspan="3" class="table_title">
						${_('Tools')}
					</th>
				</tr>
<% i = 0 %>
% for s in c.polls:
	<%
		public = h.literal('<img src="/images/icons/notok.png">') if not s.public  else h.literal('<img src="/images/icons/ok.png">')
		i += 1
	%>
	<tr class="table_row"> 
		<td>${i}</td>
		<td>${s.name}</td>
	        <td>${s.expiration_date}</td>
	        <td>${s.type}</td>
		<td>${public}</td>
		<td><a href="${url(controller='poll', action='editPoll', poll_id=s.id)}"><img src="/images/icons/pencil.png"></a></td>
		<td><a href="${url(controller='poll', action='deletePoll', poll_id=s.id)}"><img src="/images/icons/notok.png"></a></td>
        </tr>
% endfor

</table>


<div class="clear">&nbsp;</div>
</article>
</div>
</script>
