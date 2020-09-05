from slack import WebClient

from models.base import DataBase
from models.reaction import Reaction
from models.slack_user import SlackUser
from src import Logger


class ReactionManager:

    def __init__(self, client: WebClient, database: DataBase, logger: Logger):
        self.client, self.database, self.logger = client, database, logger

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

    def generate_slack_message(self, target_reaction):
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
