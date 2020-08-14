from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship
from src.models.base import Base


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, Sequence('author_id_seq'), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    notifications = relationship('Notification')

    def __init__(self, first_name, last_name):
        self.first_name, self.last_name = first_name, last_name

    def __repr__(self):
        return "<Author(id='%d', first_name='%s', last_name='%s')>" % (self.id, self.first_name, self.last_name)
