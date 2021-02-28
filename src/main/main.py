import gc
import time

from src import logger, progress_queue, INIT_PROGRESS, SCRAPE_PROGRESS, SAVE_PROGRESS, NONE_PROGRESS, DONE_PROGRESS
from src.main import client, scraper
from src.main import refresh_active_courses
from src.main.helper import *
from src.main.reactions import count_reactions
from src.models.base import DataBase
from src.models.model_list import Notification, Course, Channel


def start_scraper_process():
    progress_queue.put((NONE_PROGRESS, 'Starting scraper'))
    database = DataBase()
    logger.info_log('Program started.')
    # refresh_active_courses.start()
    # count_reactions(client)
    timeout = 600
    try:
        loop_count = 0
        courses = database.select_many(Course, watch=True)
        while True:
            check_pins(client, logger)
            check_reminders(client, logger)
            notifications = scraper.start(courses)
            print('Scraping phase done.')
            # TODO catch exception do in main
            if notifications is None:
                progress_queue.put((INIT_PROGRESS + SCRAPE_PROGRESS), None, 'warning')
                timeout *= 2
                time.sleep(min(timeout, 2400))
                notifications = []
            else:
                timeout = 600
            for i in range(len(notifications)):
                notification = notifications[i]
                result = database.select(Notification, title=notification.title, site=notification.site,
                                         author=notification.author, publish_date=notification.publish_date,
                                         text=notification.text, link=notification.link)
                if result is None:
                    fresh_notification = notification.publish_date + timedelta(hours=24) >= datetime.now()
                    course = database.select(Course, id=notification.site)
                    if check_filters(notification) and fresh_notification:
                        channel = database.select(Channel, tag=course.channel_tag)
                        # check if course.channel_tag is enough (in place of channel.id)
                        response = client.chat_postMessage(channel=channel.id,
                                                           text=structure_message(notification))
                    database.insert(notification)
                    if check_filters(notification) and fresh_notification:
                        for reminder in generate_reminders(notification):
                            database.insert(reminder)
                        # https://api.slack.com/methods/pins.add
                        client.pins_add(channel=response['channel'], timestamp=response['ts'])
                        database.insert(Pin(datetime.now(), timedelta(hours=24), response['channel'], response['ts']))
                progress_queue.put((INIT_PROGRESS + SCRAPE_PROGRESS + int(SAVE_PROGRESS/(len(notifications))) * (i+1), None))
            gc.collect()
            if loop_count == 10:
                count_reactions(client)
                courses = database.select_many(Course, watch=True)
                loop_count = 0
            progress_queue.put((DONE_PROGRESS, 'Scraping done', 'sleep'))
            time.sleep(60)
            progress_queue.put((NONE_PROGRESS, 'Starting scraper'))
    except Exception as e:
        logger.error_log(e)
    finally:
        error_channel = '#random'
        client.chat_postMessage(channel=error_channel, text='I am dead.')
        logger.info_log('Program finished with exit code 1.')
        progress_queue.put((NONE_PROGRESS, 'Program finished with exit code 1', 'error'))
        exit(1)
