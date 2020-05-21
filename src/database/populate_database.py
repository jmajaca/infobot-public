import slack
import sys
from src.models.base import DataBase, Session
from src.models.model_list import Course, Channel, SlackUser, Reaction
from datetime import datetime
from src import logger
import pickle
from src.main.reactions import count_reactions
from sqlalchemy import and_


def main():
    logger.info_log('Started populating database.')
    database = DataBase()
    client = slack.WebClient(token=sys.argv[1])
    response = client.users_list()
    # insert users
    for user in response['members']:
        if database.select(SlackUser, id=user['id']) is None:
            database.insert(SlackUser(user['id'], user['name']))
    # insert channels
    response = client.conversations_list()
    for channel in response['channels']:
        date_created = datetime.fromtimestamp(channel['created'])
        author_id = channel['creator']
        if database.select(Channel, id=channel['id']) is None:
            database.insert(Channel(channel['id'], '#'+channel['name'], author_id, date_created))
    # insert courses
    courses = [('Skriptni jezici', '#skriptni'), ('Umjetna inteligencija', '#ai'), ('Statistička analiza podataka', '#sap'),
               ('Trgovačko pravo', '#pravo'), ('Interaktivna računalna grafika', '#irg'), ('Završni rad', '#završni'),
               ('Napredno korištenje operacijskog sustava Linuxi', '#linux')]
    for course in courses:
        if database.select(Course, name=course[0], channel_tag=course[1]) is None:
            database.insert(Course(*course))
    # insert reactions
    response = client.users_list()
    count_reactions(client)
    # if there is legacy file with reactions insert legacy reactions (w/o channel and timestamp attribute)
    if len(sys.argv) == 3:
        count_legacy_reactions(response, database, sys.argv[2])
    logger.info_log('Ended populating database.')


def count_legacy_reactions(response, database, file_path):
    reactions_legacy = dict()
    session = Session()
    with open(file_path, "rb") as fp:
        reactions_legacy.update(pickle.load(fp))
    # timestamp of the last reaction recorded in the legacy file
    last_ts = max([float(reactions_legacy[slack_user['id']]) if slack_user['id'] in reactions_legacy else 0 for
                   slack_user in response['members']])
    for key in reactions_legacy:
        if len(key) == 3:
            sender, receiver, reaction = key
            # legacy file reaction count - overlap with reactions already stored in database
            num = reactions_legacy[key] - len(session.query(Reaction).filter(and_(Reaction.sender == sender,
                                                                                  Reaction.receiver == receiver,
                                                                                  Reaction.name == reaction,
                                                                                  Reaction.timestamp < last_ts)).all())
            # this allows script to run N times without putting duplicates into database
            num -= len(session.query(Reaction).filter(and_(Reaction.sender == sender, Reaction.receiver == receiver,
                                                           Reaction.name == reaction, Reaction.channel == None,
                                                           Reaction.timestamp == None)).all())
            for i in range(num):
                database.insert(Reaction(None, None, reaction, sender, receiver))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error_log(e, text='Error has occurred while initializing database ')
