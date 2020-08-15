import gc
import time

from src import logger
from src.main import client, scraper
from src.main import refresh_active_courses
from src.main.helper import *
from src.main.reactions import count_reactions
from src.models.base import DataBase
from src.models.model_list import Notification, Course
from src.web_app.flask_app import start_app_windows


def start():
    database = DataBase()
    start_app_windows()
    logger.info_log('Program started.')
    refresh_active_courses.start()
    courses = database.select_many(Course, watch=True)
    # count_reactions(client)
    timeout = 600
    try:
        loop_count = 0
        while True:
            check_pins(client)
            check_reminders(client)
            notifications = scraper.scrape_notifications(courses)
            print('Scraping phase done.')
            # TODO catch exception do in main
            if notifications is None:
                timeout *= 2
                time.sleep(min(timeout, 2400))
                notifications = []
            else:
                timeout = 600
            for notification in notifications:
                result = database.select(Notification, title=notification.title, site=notification.site,
                                         author=notification.author, publish_date=notification.publish_date,
                                         text=notification.text, link=notification.link)
                if result is None:
                    fresh_notification = notification.publish_date + timedelta(hours=24) >= datetime.now()
                    course = database.select(Course, id=notification.site)
                    if check_filters(notification) and fresh_notification:
                        response = client.chat_postMessage(channel=course.channel_tag,
                                                           text=structure_message(notification))
                    database.insert(notification)
                    if check_filters(notification) and fresh_notification:
                        for reminder in generate_reminders(notification):
                            database.insert(reminder)
                        # https://api.slack.com/methods/pins.add
                        client.pins_add(channel=response['channel'], timestamp=response['ts'])
                        # database.insert(Pin(datetime.now(), timedelta(hours=24), response['channel'], response['ts']))
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
        logger.info_log('Program finished with exit code 1.')
        exit(1)
