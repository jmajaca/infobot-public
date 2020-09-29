from slack import WebClient
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