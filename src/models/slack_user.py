from sqlalchemy import Column, Integer, String, Sequence
from src.models.base import Base
from sqlalchemy.orm import relationship


class SlackUser(Base):
    __tablename__ = 'slack_user'
    id = Column(String, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    channels = relationship('Channel')
    reactions_sent = relationship('Reaction', foreign_keys="[Reaction.sender]")
    reactions_received = relationship('Reaction', foreign_keys="[Reaction.receiver]")

    def __init__(self, id, name):
        self.id, self.name = id, name

    def __repr__(self):
        return "<SlackUser(id='%s', name='%s')>" % (self.id, self.name)



