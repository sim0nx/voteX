<%inherit file="/base.mako" />

<!-- content !-->
<div id="content" class="span-9 push-6 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${_('Enter your vote key')}</header>
				
<article>
	<h3>VoteX</h3>
	${h.form(url(controller='vote', action='showResults'), method='post')}
     	<div><input type="text" class="text" name="vote_key" tabindex=1 required /></div> 
	<div><input type="submit" class="text" name="submit" tabindex=2 value="${_('Go')}" /></div>
	</form> 
	 <div class="clear">&nbsp;</div>
</article>


<script language="JavaScript">
	document.forms[0].username.focus()
</script>
