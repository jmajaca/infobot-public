from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src import config
from src import logger

engine = create_engine(config['database_url'], echo=True, client_encoding='utf8')
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class DataBase:

    def __init__(self):
        self.session = Session()

    def insert(self, element):
        self.session.add(element)
        self.session.commit()
        logger.info_log('Database insert ' + str(element))

    def select(self, table, **kwargs):
        result = self.session.query(table)
        for key in kwargs.keys():
            result = result.filter(getattr(table, key) == kwargs[key])
        return result.first()

    def select_many(self, table, **kwargs):
        result = self.session.query(table)
        for key in kwargs.keys():
            result = result.filter(getattr(table, key) == kwargs[key])
        return result.all()

# getattr(object, attrname)
# setattr(object, attrname, value)
