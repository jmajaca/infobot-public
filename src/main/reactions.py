import pickle
from src.models.base import DataBase, Session
from src.models.model_list import Reaction, SlackUser


def count_reactions(client):
    database = DataBase()
    for user in Session().query(SlackUser).all():
        reactions_response = client.reactions_list(user=user.id)
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
                    if database.select(Reaction, channel=channel, timestamp=ts, sender=user.id, receiver=author, name=reaction_code) is None:
                        database.insert(Reaction(channel, ts, reaction_code, user.id, author))


def generate_reactions_message(target_reaction):
    session = Session()
    reactions = []
    for user in session.query(SlackUser).all():
        sent_count = len(session.query(Reaction).filter(Reaction.sender == user.id).filter(Reaction.name == target_reaction).all())
        received_count = len(session.query(Reaction).filter(Reaction.receiver == user.id).filter(Reaction.name == target_reaction).all())
        reactions.append((user.id, received_count, sent_count))
    results = sorted(reactions, key=lambda x: x[1])
    results.reverse()
    result_string = 'Here is top chart for :' + target_reaction + ':\n\n'
    for i in range(len(results)):
        item = results[i]
        result_string += str(i+1) + '. <@' + item[0] + '> with ' + str(item[1]) + ' total reactions received (sent ' + str(item[2]) + ')\n'
    return result_string
