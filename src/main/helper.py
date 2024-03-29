import re
from datetime import datetime, timedelta

from src.models.base import DataBase, Session
from src.models.model_list import Notification, Course, Author, Reminder, Pin, Filter


def structure_message(notification):
    database = DataBase()
    author = database.select(Author, id=notification.author)
    output_string = '>*' + notification.title + '*\n>\n>'
    output_string += str(notification.text).replace('\n', '\n>') + '\n>\n>'
    output_string += '*' + author.first_name + ' ' + author.last_name + '*' + ' ' * 10 + parse_date(
        str(notification.publish_date)) + '\n\n'
    output_string += '[src: ' + notification.link + ']'
    return output_string


def parse_date(date):
    groups = re.search(r'(.*)-(.*)-(.*) ([0-9]+:[0-9]+)', date)
    return groups.group(3) + '.' + groups.group(2) + '.' + groups.group(1) + '. u ' + groups.group(4)


def check_reminders(client, logger):
    session = Session()
    reminders = session.query(Reminder).filter(Reminder.end_date - Reminder.timer <= datetime.now()).filter(
        Reminder.posted == False).all()
    for reminder in reminders:
        notification = session.query(Notification).filter(Notification.id == reminder.notification).first()
        course = session.query(Course).filter(notification.site == Course.id).first()
        time_left = reminder.end_date - datetime.now()
        text = '*' + str(time_left) + ('h* left until this event\n>' + notification.title + '\n>' + reminder.text +
                                       '\nSee more at ' + notification.link)
        response = client.chat_postMessage(channel=course.channel_tag, text=text)
        reminder.posted = True
        logger.info_log('Posted reminder with id ' + str(reminder.id) + ' in channel ' + course.channel_tag + '(' +
                        str(course.channel.id) + ')')
        session.commit()


def generate_reminders(notification):
    reminders = []
    input_string = notification.text
    months = 'siječ|veljač|ožuj|trav|svib|lip|srp|kolovoz|ruj|listopad|studen|prosin'
    chapters = input_string.split('\n')
    for chapter in chapters:
        matches = re.findall(r"(([0-9]{1,2}\. ?([0-9]\.|" +
                             months +
                             r"))[^0-9]*( ?[0-9]{4}[^0-9]+|[^0-9]+)([0-9]+(:[0-9]+| ?h|\.[0-9]+| ?sati?))h?[^.0-9])",
                             chapter)
        if len(matches) != 0:
            for match in matches:
                test = get_date(match[1]) + get_time(match[4])
                date_time_obj = datetime.strptime(test, '%d.%m.%Y. %H:%M')
                reminder = Reminder(chapter, date_time_obj, timedelta(hours=12), notification.id)
                reminders.append(reminder)
    return reminders


def get_date(match_group):
    match_group = match_group.replace(' ', '')
    if not re.search(r'[0-9]+\.[0-9]+\.', match_group):
        groups = re.search(r'([0-9]+)(.*)', match_group)
        day = groups.group(1)
        group_month = groups.group(2)
        if 'siječ' in group_month:
            month = 1
        elif 'veljač' in group_month:
            month = 2
        elif 'ožuj' in group_month:
            month = 3
        elif 'trav' in group_month:
            month = 4
        elif 'svib' in group_month:
            month = 5
        elif 'lip' in group_month:
            month = 6
        elif 'srp' in group_month:
            month = 7
        elif 'kolovoz' in group_month:
            month = 8
        elif 'ruj' in group_month:
            month = 9
        elif 'listopad' in group_month:
            month = 10
        elif 'studen' in group_month:
            month = 11
        else:
            month = 12
        if month > datetime.now().month:
            year = datetime.now().year + 1
        else:
            year = datetime.now().year
        return str(day) + '.' + str(month) + '.' + str(year) + '.'
    else:
        month = re.search(r'[0-9]+\.([0-9])\.', match_group).group(1)
        if int(month) < datetime.now().month:
            year = datetime.now().year + 1
        else:
            year = datetime.now().year
        return match_group + str(year) + '.'


def get_time(match_group):
    match_group = re.sub(r"[^:\d]", "", match_group.replace('.', ':').strip())
    if len(match_group) <= 2:
        return ' ' + match_group + ':00'
    return ' ' + match_group


# b -ban filter, a - accept filter
def check_filters(notification):
    session = Session()
    filters = session.query(Filter).all()
    for filter in filters:
        if re.search(filter.ban_title, notification.title):
            return False
    return True


def check_pins(client, logger):
    session = Session()
    pins = session.query(Pin).filter(Pin.done == False).all()
    for pin in pins:
        if datetime.now() >= pin.creation_date + pin.timer:
            response = client.pins_remove(channel=pin.channel, timestamp='%.6f' % pin.timestamp)
            pin.done = True
            session.commit()
            logger.info_log('Unpinned message with timestamp ' + str(pin.timestamp) + ' in channel ' + pin.channel)
