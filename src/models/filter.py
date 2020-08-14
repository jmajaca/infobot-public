from sqlalchemy import Column, Integer, String, Sequence
from src.models.base import Base


class Filter(Base):
    __tablename__ = 'filter'
    id = Column(Integer, Sequence('filter_id_seq'), primary_key=True)
    ban_title = Column(String, nullable=False)

    def __init__(self, ban_title, last_name):
        self.ban_title = ban_title

    def __repr__(self):
        return "<Filter(id='%d', ban_title='%s')>" % (self.id, self.ban_title)
