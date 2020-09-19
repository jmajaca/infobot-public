from slack import WebClient
from src.models.base import DataBase
from src.models.model_list import Reminder, Author, Course
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
    get_all_reminders()
        returns all reminders from database
    get_filter_options()
        returns courses and authors to be used in filter option
	"""

	def __init__(self, client: WebClient, database: DataBase, logger: Logger):
		self.client, self.database, self.logger = client, database, logger

	def get_all_reminders(self):
		self.logger.info_log('Pulled all reminders')
		return self.database.select_many(Reminder)

	def get_filter_options(self):
		self.logger.info_log('Pulling all courses and authors')
		return self.database.select_many(Author), self.database.select_many(Course)