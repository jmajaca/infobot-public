from slack import WebClient
from src.main.objects.reaction_manager import ReactionManager
from src.models.base import DataBase
from src.models.model_list import Channel, SlackUser
from src import Logger
from datetime import datetime


class Scanner:
    """
    A class that scans Slack Workspace and saves data to database

    Attributes
    ----------
    client : WebClient
        a Slack WebClient via getting data from Slack Workspace is done
    database : DataBase
        a objects that is responsible for communicating with database
    logger : Logger
        a object that is saving scanner logs to a predefined file
    reaction_manager : ReactionManager
        a object that is responsible for managing reactions from Slack Workspace

    Methods
    -------
    scan_users()
        Saves new Slack users that are not in the database to the database
    scan_channels()
        Saves new Slack channels that are not in the database to the database
    scan_reactions()
        Saves new Slack reactions that are not in the database to the database via ReactionManager
    scan_complete()
        Saves new Slack users, channels and reactions that are not in the database to the database
    """

    def __init__(self, client: WebClient, database: DataBase):
        self.client, self.database = client, database
        self.logger = Logger()
        self.reaction_manager = ReactionManager(self.client, self.database, self.logger)

    def scan_users(self):
        self.logger.info_log('Started scanning for user.')
        response = self.client.users_list()
        for user in response['members']:
            if self.database.select(SlackUser, id=user['id']) is None:
                slack_user = SlackUser(user['id'], user['name'])
                self.database.insert(slack_user)
                self.logger.info_log('Database insert {}.'.format(slack_user))
        self.logger.info_log('Finished scanning for user.')

    def scan_channels(self):
        response = self.client.conversations_list()
        for channel in response['channels']:
            date_created = datetime.fromtimestamp(channel['created'])
            author_id = channel['creator']
            slack_channel = Channel(channel['id'], '#' + channel['name'], author_id, date_created)
            if self.database.select(Channel, id=channel['id']) is None:
                self.database.insert(slack_channel)
                self.logger.info_log('Database insert {}.'.format(slack_channel))
        self.logger.info_log('Finished scanning for channels.')

    def scan_reactions(self):
        self.reaction_manager.count()

    def scan_complete(self):
        self.logger.info_log('Started complete scan.')
        self.scan_users()
        self.scan_channels()
        self.scan_reactions()
        self.logger.info_log('Finished complete scan.')
