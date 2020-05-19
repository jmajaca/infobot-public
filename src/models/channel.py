from src.models.base import Base
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(String, primary_key=True)
    tag = Column(String, ForeignKey('course.channel_tag'))
    course = relationship("Course", back_populates="channel", uselist=False)
    creator_id = Column(String, ForeignKey('slack_user.id'), nullable=False)
    created = Column(TIMESTAMP, nullable=False)
    pins = relationship("Pin")
    reactions = relationship("Reaction")

    def __init__(self, id, tag, creator_id, created):
        self.id, self.tag, self.creator_id, self.created = id, tag, creator_id, created

    def __repr__(self):
        return "<Channel(id='%s', tag='%s', creator_id='%s', created='%s')>" % (self.id, self.tag, self.creator_id, self.created)
