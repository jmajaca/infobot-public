from datetime import datetime, timedelta

from slack import WebClient
from sqlalchemy.exc import SQLAlchemyError

from src.models.base import DataBase, Session
from src.models.model_list import Reminder, Author, Course, Notification
from src import Logger


class ReminderManager:
	"""
	A class that is responsible for handling all actions regarding Slack Workspace reminders

	Attributes
    ----------
    client : WebClient
        a Slack WebClient with which reminders are pulled from Slack Workspace
    database : DataBase
        a objects that is responsible for communicating with database
    logger : Logger
        a object that is saving scanner logs to a predefined file

    Methods
    ---------
    get_reminders()
        returns reminders from database
        kwargs: course, author, from and to dates
        default is return all
    get_filter_options()
        returns all authors and courses
    save()
        saves a changed reminder
        returns result of saving
    delete()
        deletes reminder with given id from database
        return result of deletion
	"""

	def __init__(self, client: WebClient, database: DataBase, logger: Logger):
		self.client, self.database, self.logger = client, database, logger
		self.session = Session()

	def get_reminders(self, **kwargs):
		self.logger.info_log('Pulling reminders')
		if not kwargs:
			return self.database.select_many(Reminder)
		else:
			result = self.session.query(Reminder).join(Notification).join(Author).join(Course)
			for filters in kwargs.keys():
				if filters == 'name':
					result = result.filter(getattr(Course, 'name') == kwargs['name'])
				elif filters == 'author':
					result = result.filter(getattr(Author, 'first_name') == kwargs['author'].split(' ')[0])
					result = result.filter(getattr(Author, 'last_name') == kwargs['author'].split(' ')[1])
				elif filters == 'from':
					result = result.filter(getattr(Reminder, 'end_date') >= kwargs['from'])
				elif filters == 'to':
					result = result.filter(getattr(Reminder, 'end_date') < kwargs['to'])
				elif filters == 'posted':
					result = result.filter(getattr(Reminder, 'posted') == kwargs['posted'])
			return result.all()

	def get_filter_options(self):
		self.logger.info_log('Pulling all courses and authors')
		return self.database.select_many(Course), self.database.select_many(Author)

	def save(self, **kwargs):
		self.logger.info_log('Updating reminder with id: ' + kwargs['id'])
		reminder = self.session.query(Reminder).get(kwargs['id'])
		# parse string data
		year, month, day = kwargs['end_date'].split(' ')[0].split('-')
		hour, minute, second = kwargs['end_date'].split(' ')[1].split(':')
		try:
			reminder.end_date = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
			reminder.timer = timedelta(seconds=kwargs['timer'])
			reminder.text = kwargs['text']
			reminder.posted = True if kwargs['posted'] is True else False
			self.session.commit()
		except SQLAlchemyError as e:
			self.logger.info_log('Error when updating:' + str(type(e)))
			return False
		return True

	def delete(self, reminder_id):
		self.logger.info_log("Removing reminder with id: " + reminder_id)
		try:
			self.session.query(Reminder).filter_by(id=reminder_id).delete()
			self.session.commit()
		except SQLAlchemyError as e:
			self.logger.info_log('Error when deleting:' + str(type(e)))
			return False
		return True
