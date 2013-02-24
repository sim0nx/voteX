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
    public = '' if not s.public else h.literal('<i class="icon-ok"></i>')
    i += 1

    status = ''
    if s.running and s.expiration_date > c.datetimenow:
      status = 'success'
    elif not s.running and s.expiration_date > c.datetimenow:
      status = 'warning'
    elif not s.running and s.expiration_date < c.datetimenow:
      status = 'error'
  %>
    <tr class="table_row ${status}">
      <td>${i}</td>
      <td>${s.name}</td>
      <td>${s.expiration_date}</td>
      <td>${public}</td>
      <td>
        <a href="${url(controller='poll', action='editPoll', poll_id=s.id)}" alt="${_('edit poll')}">
          <i class="icon-wrench"></i>
        </a>
        <a href="${url(controller='poll', action='deletePoll', poll_id=s.id)}" data-confirm="${_('Are you sure you want to delete this poll ?')}">
          <i class="icon-remove"></i>
        </a>
        <a href="${url(controller='poll', action='showResults', poll_id=s.id)}">
          <i class="icon-align-left"></i>
        </a>
        <a href="${url(controller='poll', action='doResendMails', poll_id=s.id)}" data-confirm="${_('Are you sure you want to continue ?')}">
          <i class="icon-envelope"></i>
        </a>
      </td>
    </tr>
  % endfor
  </tbody>
</table>
