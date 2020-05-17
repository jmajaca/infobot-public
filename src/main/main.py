from src.main.helper import *
from datetime import timedelta
from src.main.reactions import count_reactions
from src.main.constants import log_file
import slack
import sys
import gc
import time
from src.models.base import DataBase
from src.models.model_list import Notification, Course, Pin
from src.main.html_scraper import Scraper
from src.main.logger import Logger
from .. import config


if __name__ == '__main__':
    client = slack.WebClient(token=sys.argv[1])
    scraper = Scraper(link=config['fer_url'], payload={'username': sys.argv[2], 'password': sys.argv[3]})
    database = DataBase()
    logger = Logger(log_file)
    sys.argv[1:] = []
    # start_app(client)
    logger.info_log('Program started.')
    count_reactions(client)
    try:
        loop_count = 0
        while True:
            check_pins(client)
            check_reminders(client)
            notifications = scraper.scrape_data()
            print('Scraping phase done.')
            for notification in notifications:
                result = database.select(Notification, title=notification.title, site=notification.site,
                                         author=notification.author, publish_date=notification.publish_date,
                                         text=notification.text, link=notification.link)
                if result is None:
                    course = database.select(Course, id=notification.site)
                    if check_filters(notification):
                        response = client.chat_postMessage(channel=course.channel_tag, text=structure_message(notification))
                    database.insert(notification)
                    if check_filters(notification):
                        # https://api.slack.com/methods/pins.add
                        client.pins_add(channel=response['channel'], timestamp=response['ts'])
                        database.insert(Pin(datetime.now(), timedelta(hours=24), response['channel'], response['ts']))
                        for reminder in generate_reminders(notification):
                            database.insert(reminder)
            gc.collect()
            if loop_count == 10:
                count_reactions(client)
                loop_count = 0
            time.sleep(60)
    except Exception as e:
        logger.error_log(e)
    finally:
        error_channel = '#random'
        client.chat_postMessage(channel=error_channel, text='I am dead.')
        logger.info_log('Program ended.')
