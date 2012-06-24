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


from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from votex.model.meta import Base


class Poll(Base):
	__tablename__ = 'poll'

	id			= Column(Integer, primary_key=True)
	name			= Column(String(255))
	owner			= Column(String(64))
	instructions		= Column(Text)
	expiration_date		= Column(DateTime)
	type			= Column(String(64))
	public			= Column(Boolean)

	votes = relationship('Vote')

	def __str__(self):
		return "<Poll id=%s, name=%s, owner=%s, instructions=%s, expiration_date=%s, type=%s, public=%s>>" %\
			(self.id, self.name, self.owner, self.instructions, self.expiration_date, self.type, self.public)


class Vote(Base):
	__tablename__ = 'vote'

	id = Column(Integer, primary_key=True)
	poll_id = Column(Integer, ForeignKey('poll.id'), index=True)
	update_date = Column(DateTime)
	key = Column(String(255))
	simple_vote = Column(String(4))
	complex_vote = Column(Text)


	def __str(self):
		return "<Vote id=%s, poll_id=%s, update_date=%s, key=%s, simple_vote=%s, complex_vote=%s>" %\
			(self.id, self.poll_id, self.update_date, self.key, self.simple_vote, self.complex_vote)
