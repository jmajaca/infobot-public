from slack import WebClient
from src.models.base import DataBase
from src.models.model_list import Reminder
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

	"""

	def __init__(self, client: WebClient, database: DataBase, logger: Logger):
		self.client, self.database, self.logger = client, database, logger

	def get_all(self):
		self.logger.info_log('Pulled all reminders')
		return self.database.select_many(Reminder)