<%inherit file="/base.mako" />

<h3>${_('Enter your vote key')}</h3>

${h.form(url(controller='vote', action='vote'), method='post')}
<div><input type="text" class="text" name="vote_key" tabindex=1 required /></div> 
<div><button type="submit" class="btn" tabindex='3'>${_('Go')}</button></div>
</form> 

<%
if 'reqparams' in session:
	del session['reqparams']
	session.save()
%>
