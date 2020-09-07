import time

from slack import WebClient
from models.base import DataBase
from models.model_list import Reaction, SlackUser
from src import Logger
from multiprocessing import Process
from datetime import datetime


class ReactionManager:
    """
    A class that is responsible for handling all actions regarding Slack Workspace reactions

    Attributes
    ----------
    client : WebClient
        a Slack WebClient via getting reactions from Slack Workspace is done
    database : DataBase
        a objects that is responsible for communicating with database
    logger : Logger
        a object that is saving scanner logs to a predefined file
    scan_hour: int
        value of a hour on which to start automatic scanning for new reactions
    scan_minute: int
        value of a minute on which to start automatic scanning for new reactions
    process: Process
        process that is executing the automatic scanning for new reactions

    Methods
    -------
    start()
        Start async child process for automatic reaction scanning
    _start_process()
        Infinite loop that checks if time has come to start automatic reaction scanning
    is_alive() -> bool
        Method that returns boolean value that represent if automatic scraping process is alive
    close()
        Ends async child process for automatic reaction scanning
    count()
        Scans for new reactions in Slack Workspace and saves them in the database
    generate_slack_message(target_reaction) -> str
        Method for generating Slack message that contains top list (sender and receiver) for target reaction
    """

    process: Process = None

    def __init__(self, client: WebClient, database: DataBase, logger: Logger):
        self.client, self.database, self.logger = client, database, logger
        self.scan_hour, self.scan_minute = 0, 0

    def start(self):
        self.process = Process(target=self._start_process)
        self.logger.info_log('Started process of automatic reaction scanning.')
        self.process.start()

    def _start_process(self):
        last_date = None
        while True:
            current_time = datetime.now().time()
            if current_time.hour >= self.scan_hour and current_time.minute >= self.scan_minute and \
                    (last_date is None or datetime.now().date() > last_date):
                last_date = datetime.now().date()
                try:
                    self.count()
                except Exception as e:
                    self.logger.error_log(e)
                    raise e
            time.sleep(600)

    def is_alive(self) -> bool:
        if self.process:
            return self.process.is_alive()
        else:
            return False

    def close(self):
        self.process.kill()
        # self.process.close()
        self.logger.info_log('Killed process of automatic reaction scanning.')

    def count(self):
        self.logger.info_log('Started counting reactions.')
        for user in self.database.select_many(SlackUser):
            reactions_response = self.client.reactions_list(user=user.id)
            items = reactions_response.data['items']
            for item in items:
                channel = item['channel']
                message = item['message']
                ts = message['ts']
                author = message['user']
                reactions = message['reactions']
                for reaction in reactions:
                    if user.id in reaction['users']:
                        reaction_code = reaction['name'].split(':')[0]
                        if self.database.select(Reaction, channel=channel, timestamp=ts, sender=user.id,
                                                receiver=author, name=reaction_code) is None:
                            slack_reaction = Reaction(channel, ts, reaction_code, user.id, author)
                            self.database.insert(slack_reaction)
                            self.logger.info_log('Database insert {}'.format(slack_reaction))
        self.logger.info_log('Finished counting reactions.')

    def generate_slack_message(self, target_reaction) -> str:
        reactions = []
        for user in self.database.select_many(SlackUser):
            sent_count = len(self.database.select_many(Reaction, sender=user.id, name=target_reaction))
            received_count = len(self.database.select_many(Reaction, receiver=user.id, name=target_reaction))
            reactions.append((user.id, received_count, sent_count))
        results = sorted(reactions, key=lambda x: x[1])
        results.reverse()
        slack_message = 'Here is top chart for :{}:\n\n'.format(target_reaction)
        for i in range(len(results)):
            item = results[i]
            slack_message += '{}. <@{}> with {} total reaction received (sent {})\n'.format(i+1, item[0], item[1],
                                                                                            item[2])
        return slack_message
