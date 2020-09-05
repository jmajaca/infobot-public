from slack import WebClient

from main.reaction_manager import ReactionManager
from models.base import DataBase
from models.channel import Channel
from models.slack_user import SlackUser
from src import Logger
from datetime import datetime


class Scanner:

    def __init__(self, client: WebClient, database: DataBase):
        self.client, self.database = client, database
        self.logger = Logger('../log')
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
