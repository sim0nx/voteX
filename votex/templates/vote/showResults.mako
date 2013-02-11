<%inherit file="/base.mako" />

<h3>${c.heading}</h3>
<h4>${_('Poll:')}</h4>

<table class="table">
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

<h4>${_('Results:')}</h4>
% for q in c.poll.questions:
<%
  total_answers = 0
  answers = {}
  factor = 0
  for a in q.answers:
    if not q.type == 1:
      if a.id in c.submissions:
        total_answers += c.submissions[a.id]

  if total_answers > 0:
    factor = 100.0 / total_answers

  for a in q.answers:
    if not q.type == 1:
      if a.id in c.submissions:
        answers[a.id] = c.submissions[a.id] * factor
      else:
        answers[a.id] = 0
%>
<table class="table table-striped">
  <thead>
    <tr>
      <th>${_('Question')}</th>
      <th>${q.question}</th>
    </tr>
  </thead>
  <tbody>
    % for a in q.answers:
    <tr>
      <td>${a.name}</td>
      % if not q.type == 1:
      <td>${c.submissions.get(a.id, 0)} / ${total_answers}
        <div class="progress progress-striped">
          <div class="bar" style="width: ${answers[a.id]}%;"></div>
        </div>
      </td>
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
  </tbody>
</table>
% endfor

<div id="make-space" class="prepend-top">&nbsp;</div>

<%
if 'reqparams' in session:
  del session['reqparams']
  session.save()
%>
