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
      % for l in c.poll.instructions.split('\n'):
      ${l}<br/>
      % endfor
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Expiration Date')}
    </td>
    <td>
      ${c.poll.expiration_date}
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
% for q in c.poll.questions:
<table class="table_content">
  <tr>
    <td class="table_title">${_('Question')}</td>
    <td class="table_title">${q.question}</td>
  </tr>
  % for a in q.answers:
  <tr>
    <td>${a.name}</td>
    % if not q.type == 1:
      % if a.id in c.submissions:
    <td>${c.submissions[a.id]}</td>
      % else:
    <td>0</td>
      % endif
    % else:
    <td>
      <table>
      % if a.id in c.submissions:
        % for t in c.submissions[a.id]: 
        <tr>
          <td>Answer:</td>
          <td>
            ${t}
          </td>
        </tr>
        % endfor
      % endif
      </table>
    </td>
    % endif
  </tr>
  % endfor
</table>
% endfor

</article>
<div id="make-space" class="prepend-top">&nbsp;</div>
</div>

<%
if 'reqparams' in session:
  del session['reqparams']
  session.save()
%>
