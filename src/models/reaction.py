from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Float
from src.models.base import Base


class Reaction(Base):
    __tablename__ = 'reaction'
    id = Column(Integer, Sequence('reaction_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    sender = Column(String, ForeignKey('slack_user.id'), nullable=False)
    receiver = Column(String, ForeignKey('slack_user.id'), nullable=False)
    timestamp = Column(Float, nullable=True)
    channel = Column(String, ForeignKey('channel.id'))

    def __init__(self, channel, timestamp, name, sender, receiver):
        self.channel, self.timestamp, self.name, self.sender, self.receiver = channel, timestamp, name, sender, receiver

    def __repr__(self):
        return ("<Reaction(id='%d', name='%s', sender='%s', receiver='%s', timestamp='%s', channel='%s')>" %
                (self.id, self.name, self.sender, self.receiver, str(self.timestamp), self.channel))
