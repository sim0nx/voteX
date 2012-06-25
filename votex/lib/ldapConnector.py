#
# Copyright (c) 2012 Georges Toth <georges _at_ trypill _dot_ org>
#
# This file is part of voteX.
#
# voteX is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# voteX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with voteX.  If not, see <http://www.gnu.org/licenses/>.


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
