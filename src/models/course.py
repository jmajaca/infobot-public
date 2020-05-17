from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship
from src.models.base import Base


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, Sequence('course_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    channel_tag = Column(String, nullable=False)
    channel = relationship("Channel", uselist=False, back_populates="course")
    notifications = relationship('Notification')

    def __init__(self, name, channel_tag):
        self.name, self.channel_tag = name, channel_tag

    def __repr__(self):
        return "<Course(id='%d', name='%s', channel_tag='%s')>" % (self.id, self.name, self.channel_tag)

    def get_notifications(self):
        return self.notifications



