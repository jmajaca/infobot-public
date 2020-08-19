from src.models.base import Base
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(String, primary_key=True)
    tag = Column(String, ForeignKey('course.channel_tag'))
    course = relationship("Course", back_populates="channel", uselist=False)
    creator_id = Column(String, ForeignKey('slack_user.id'), nullable=False)
    created = Column(TIMESTAMP, nullable=False)
    archived = Column(Boolean, nullable=False, default=False)
    pins = relationship("Pin")
    reactions = relationship("Reaction")

    def __init__(self, channel_id, tag, creator_id, created, archived=False):
        self.id, self.tag, self.creator_id, self.created, self.archived = channel_id, tag, creator_id, created, archived

    def __repr__(self):
        return "<Channel(id='%s', tag='%s', creator_id='%s', created='%s', archived='%s')>" % (self.id, self.tag,
                                                                                               self.creator_id,
                                                                                               self.created,
                                                                                               self.archived)
