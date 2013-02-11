<%inherit file="/base.mako" />

<h3>${c.heading}</h3>
<table class="table table-striped"> 
  ${parent.flash()}
  <thead>
    <tr> 
      <th>#</th>
      <th>${_('Name')}</th>
      <th>${_('Expiration Date')}</th>
      <th>${_('Public')}</th>
      <th>${_('Tools')}</th>
    </tr>
  </thead>
  <tbody>
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
      <td>${public}</td>
      <td>
        <a href="${url(controller='poll', action='editPoll', poll_id=s.id)}" alt="${_('edit poll')}">
          <img src="/images/icons/pencil.png">
        </a>
        <a href="${url(controller='poll', action='deletePoll', poll_id=s.id)}" onclick="return confirm('${_('Are you sure you want to delete this poll ?')}')" alt="${_('delete poll')}">
          <img src="/images/icons/notok.png">
        </a>
        <a href="${url(controller='poll', action='showResults', poll_id=s.id)}">
          <img src="/images/icons/pencil.png" alt="${_('Show results')}">
        </a>
      </td>
    </tr>
  % endfor
  </tbody>
</table>
