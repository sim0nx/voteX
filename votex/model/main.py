#
#    VoteX (c) 2011 Georges Toth <georges _at_ trypill _dot_ org>
#


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
