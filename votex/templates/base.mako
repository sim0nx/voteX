<% self.seen_css = set() %>
<!DOCTYPE HTML>
<html lang="en-US">
<head>
	<meta charset="UTF-8">
	<!-- Stylesheets !-->
  <link href="/css/bootstrap.min.css" rel="stylesheet" media="screen" type="text/css"/>
  <link href="/css/mematool_bootstrap_custom.css" rel="stylesheet" media="screen" type="text/css"/>
	<!-- Website title !-->
	<title>VoteX</title>
</head>
<body>

<div id="wrap">
  <div class="container-fluid offset3">
    <div class="row-fluid" style="margin: 0 auto;">
      <div class="span10">
        <!-- Title -->
        <div class="page-header">
          <h1><img src="/images/logo.png" width="" height="" alt="mematool logo" /></h1>

          <!-- NavBar -->
          <div class="navbar navbar-inverse">
            <div class="navbar-inner">
              <div class="container">
                <a class="btn btn-navbar" data-toggle="collapse" data-target=".navbar-inverse-collapse">
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                </a>
                <div class="nav-collapse collapse navbar-inverse-collapse">
                  <div class="nav-collapse collapse">
                    <ul class="nav">
                      <li>${h.link_to(_('Poll'),url(controller='poll', action='login'))}</li>
                      <li>${h.link_to(_('Vote'),url(controller='vote', action='index'))}</li>
                      <li>${h.link_to(_('Results'),url(controller='vote', action='results'))}</li>
                      % if session.has_key('uid'):
                      <li>${h.link_to(_('Logout'),url(controller='poll', action='logout',id=None))}</li>
                      % endif
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- NavBar -->
        </div>
        <!-- Title -->
      </div>
    </div>
    <div class="row-fluid">
      <div class="span1">
        <!-- sidebar !-->
        % if hasattr(c, 'actions') and len(c.actions) > 0:
        <ul class="nav nav-list">
          <li class="nav-header">Menu</li>
          % for k in c.actions:
            % if len(k) == 4:
              <li>${h.link_to(k[0], url(controller=k[1], action=k[2], member_id=k[3]))}</li>
            % else:
              <li>${h.link_to(k[0], url(controller=k[1], action=k[2]))}</li>
            % endif
          % endfor
        </ul>
        % endif
      </div>
      <!-- content !-->
      <div class="span8 offset1">
      ${flash()}
      ${self.header()}
      ${next.body()}
      ${self.footer()}
      <!-- content end !-->
      </div>
    </div>
  </div>
  <div id="push"></div>
</div>

  <!-- footer !-->
<div id="footer">
  <div class="container-fluid offset3">
    <div class="row-fluid" style="margin: 0 auto;">
      <div class="span10">
        VoteX (c) 2011-2013 Georges Toth
      </div>
    </div>
  </div>
</div>
  <!-- footer !-->
</body>
</html>

  <script type="text/javascript" src="/javascript/jquery.js"></script>
  <script type="text/javascript" src="/javascript/ui.jquery.js"></script>
  <script type="text/javascript" src="/javascript/mematool.js"></script>
  <script type="text/javascript" src="/javascript/jquery.qtip.js"></script>
</body>
</html>



<%def name="css_link(path, media='')">
% if path not in self.seen_css:
<link rel="stylesheet" type="text/css" href="${path|h}" media="${media}"></link>
% endif
<% self.seen_css.add(path) %>
</%def>

<%def name="css()">
${css_link('/css/main.css', 'screen')}
</%def>

<%def name="heading()"><h1>${hasattr(c, 'heading') and c.heading or 'No Title'}</h1></%def>
<%def name="header()"><a name="top"></a></%def>
<%def name="actions()"></%def>
<%def name="breadcrumbs()"></%def>
<%def name="footer()"><p><a href="#top">Top ^</a></p></%def>

<%def name="flash()">
% if 'flash' in session:
  <%
    flash_class = session.get('flash_class', '')
    flash_title = ''
    if flash_class == 'warning':
      flash_class = 'block'
      flash_title = '<h4>Warning!</h4>'
    elif flash_class == 'error':
      flash_title = '<h4>Error!</h4>'
    elif flash_class == '':
      flash_class == 'info'
  %>
  <div class="alert alert-${flash_class}">${flash_title|n}${session.get('flash', '')}</div>
  <%
    del session['flash']
    session.save()
  %>
% endif
</%def>

<%def name="error_messages()">
% if 'errors' in session:
  % if len(session['errors']) > 0:
<tr>
  <td colspan="2">
    <div class="error">
    % for k in session['errors']:
      <p>${k}</p>
    % endfor
    </div>
  </td>
</tr>
  % endif
  <%
  del session['errors']
  session.save()
  %>
% endif
</%def>

<%def name="all_messages()">
${self.flash()}
${self.error_messages()}
</%def>

<%
if session.has_key('reqparams'):
  del session['reqparams']
  session.save()
%>
