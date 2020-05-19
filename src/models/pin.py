from sqlalchemy import Column, Integer, String, Sequence, TIMESTAMP, Interval, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from src.models.base import Base


class Pin(Base):
    __tablename__ = 'pin'
    id = Column(Integer, Sequence('pin_id_seq'), primary_key=True)
    creation_date = Column(TIMESTAMP, nullable=False)
    timer = Column(Interval, nullable=False)
    channel = Column(String, ForeignKey('channel.id'), nullable=False)
    timestamp = Column(Float, nullable=False)
    done = Column(Boolean, default=False)

    def __init__(self, creation_date, timer, channel, timestamp):
        self.creation_date, self.timer, self.channel, self.timestamp = creation_date, timer, channel, timestamp

    def __repr__(self):
        return "<Pin(id='%d', creation_date='%s', timer='%s', channel='%s', timestamp='%f', done='%s')>" % \
               (self.id, self.creation_date, self.timer, self.channel, self.timestamp, self.done)
