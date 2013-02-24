<%inherit file="/base.mako" />

<h3>${c.heading}</h3>
<table class="table table-striped"> 
  ${parent.flash()}
  <thead>
    <tr> 
      <th>#</th>
      <th>${_('Name')}</th>
      <th>${_('Expiration Date')}</th>
      <th>${_('Tools')}</th>
    </tr>
  </thead>
  <tbody>
  <% i = 0 %>
  % for s in c.polls:
  <%
    i += 1

    status = ''
    if s.running and s.expiration_date > c.datetimenow:
      status = 'success'
    elif not s.running:
      status = 'pending'
  %>
    <tr class="table_row ${status}">
      <td>${i}</td>
      <td>${s.name}</td>
      <td>${s.expiration_date}</td>
      <td>
        <a href="${url(controller='poll', action='showPublicResults', poll_id=s.id)}">
          <i class="icon-align-left"></i>
        </a>
      </td>
    </tr>
  % endfor
  </tbody>
</table>
