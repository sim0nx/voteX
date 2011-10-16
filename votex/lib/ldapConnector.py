#
#	VoteX (c) 2011 Georges Toth <georges _at_ trypill _dot_ org>
#

# -*- coding: utf-8 -*-

import ldap
from pylons import config, session

class InvalidCredentials(Exception):
	pass

class ServerError(Exception):
	pass

class LdapConnector(object):
	def __init__(self, con=None, uid=None, password=None):
		if con is not None:
			self.con = con
		else:
			""" Bind to server """
			self.con = ldap.initialize(config.get('ldap.server'))
			try:
				self.con.start_tls_s()
				try:
					if not uid is None and not password is None:
						binddn = 'uid=' + uid + ',' + config.get('ldap.basedn_users')
						self.con.simple_bind_s(binddn, password)
				except ldap.INVALID_CREDENTIALS:
					print "Your username or password is incorrect."
					raise InvalidCredentials()
			except ldap.LDAPError, e:
				''' @TODO better handle errors and don't use "sys.exit" ;-) '''
				print e.message['info']
				if type(e.message) == dict and e.message.has_key('desc'):
					print e.message['desc']
				else:   
					print e

				raise ServerError()

	def getLdapConnection(self):
		return self.con

	def setLdapConnection(self, con):
		self.con = con
