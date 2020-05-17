import slack
import sys
from src.models.base import DataBase
from src.models.model_list import Course, Channel, Author, SlackUser
from datetime import datetime


if __name__ == '__main__':
    print('start')
    database = DataBase()
    client = slack.WebClient(token=sys.argv[1])
    response = client.users_list()
    # users
    for user in response['members']:
        if database.select(SlackUser, id=user['id']) is None:
            database.insert(SlackUser(user['id'], user['name']))
    # channels
    response = client.conversations_list()
    for channel in response['channels']:
        date_created = datetime.fromtimestamp(channel['created'])
        author_id = channel['creator']
        if database.select(Channel, id=channel['id']) is None:
            database.insert(Channel(channel['id'], '#'+channel['name'], author_id, date_created))
    # connect course to channel
    courses = [('Skriptni jezici', '#skriptni'), ('Umjetna inteligencija', '#ai'), ('Statistička analiza podataka', '#sap'),
               ('Trgovačko pravo', '#pravo'), ('Interaktivna računalna grafika', '#irg'), ('Završni rad', '#završni'),
               ('Napredno korištenje operacijskog sustava Linuxi', '#linux')]
    for course in courses:
        if database.select(Course, name=course[0], channel_tag=course[1]) is None:
            database.insert(Course(*course))
