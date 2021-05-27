from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src import config
from src import logger

engine = create_engine(config['database_url'], echo=True, client_encoding='utf8', pool_size=20, max_overflow=100)
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class DataBase:

    def __init__(self):
        self.session = Session()

    def insert(self, element):
        try:
            self.session.add(element)
            self.session.commit()
            logger.info_log('Database insert {}'.format(element))
        except Exception as e:
            self.session.rollback()
            logger.error_log(e, text='Database insert error occurred')

    def select(self, table, **kwargs):
        try:
            result = self.session.query(table)
            for key in kwargs.keys():
                result = result.filter(getattr(table, key) == kwargs[key])
            return result.first()
        except Exception as e:
            self.session.rollback()
            logger.error_log(e, text='Database select error occurred')

    def select_many(self, table, **kwargs):
        try:
            result = self.session.query(table)
            for key in kwargs.keys():
                result = result.filter(getattr(table, key) == kwargs[key])
            return result.all()
        except Exception as e:
            self.session.rollback()
            logger.error_log(e, text='Database select many error occurred')

# getattr(object, attrname)
# setattr(object, attrname, value)
