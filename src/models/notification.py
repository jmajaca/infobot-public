from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, TIMESTAMP
from src.models.base import Base
from sqlalchemy.orm import relationship


class Notification(Base):
    __tablename__ = 'notification'
    id = Column(Integer, Sequence('notification_id_seq'), primary_key=True)
    title = Column(String, nullable=False)
    site = Column(Integer, ForeignKey('course.id'), nullable=False)
    author = Column(Integer, ForeignKey('author.id'), nullable=False)
    publish_date = Column(TIMESTAMP, nullable=False)
    text = Column(String, nullable=False)
    link = Column(String, nullable=False)
    reminders = relationship('Reminder')

    def __init__(self, title, site, author, publish_date, text, link):
        self.title, self.site, self.author, self.publish_date, self.text, self.link = \
            title, site, author, publish_date, text, link

    def __repr__(self):
        return "<Notification(id='%d', title='%s', link='%s', site='%d', author='%s', publish_date='%s')>" % \
               (self.id, self.title, self.link, self.site, self.author, self.publish_date)
