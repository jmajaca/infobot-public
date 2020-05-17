from sqlalchemy import Column, Integer, Sequence, TIMESTAMP, Interval, ForeignKey, String, Boolean
from src.models.base import Base


class Reminder(Base):
    __tablename__ = 'reminder'
    id = Column(Integer, Sequence('reminder_id_seq'), primary_key=True)
    text = Column(String, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)
    timer = Column(Interval, nullable=False)
    notification = Column(Integer, ForeignKey('notification.id'), nullable=False)
    posted = Column(Boolean, default=False)

    def __init__(self, text, end_date, timer, notification):
        self.text, self.end_date, self.timer, self.notification = text, end_date, timer, notification

    def __repr__(self):
        return 'todo'
