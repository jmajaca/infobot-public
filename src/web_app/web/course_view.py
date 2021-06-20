from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for

from src.main import client
from src.models.base import Session
from src.models.channel import Channel
from src.models.course import Course
from src.models.notification import Notification
from src.models.pin import Pin
from src.models.reminder import Reminder
from src.models.slack_user import SlackUser
from src.web_app.web.forms import WatchlistForm

app_course = Blueprint('app_course', __name__, template_folder='templates')


@app_course.route('/ui/course', methods=['GET', 'POST'])
def course_handler():
    session = Session()
    default_course_url = 'www.fer.unizg.hr/predmet/'
    form = WatchlistForm()
    courses = session.query(Course).all()
    archived_channel_tags = [channel.tag for channel in session.query(Channel).filter(Channel.archived == True).all()]
    if form.validate_on_submit():
        watch = False
        if request.form.get('watch_input') == 'on':
            watch = True
        if form.id.data == -1:
            new_course = Course(form.name.data, request.form.get('tag_select'), default_course_url + form.url.data, watch)
            session.add(new_course)
            session.commit()
            session.flush()
        else:
            course = session.query(Course).filter(Course.id == form.id.data).first()
            course.name = form.name.data
            course.url = default_course_url + form.url.data
            course.channel_tag = request.form.get('tag_select')
            course.watch = watch
            session.commit()
            session.flush()
        courses = session.query(Course).all()
        form.name.data = ''
        form.url.data = ''
        form.watch.data = True
    watched = [course for course in courses if course.watch and course.channel_tag not in archived_channel_tags]
    unwatched = [course for course in courses if not course.watch and course.channel_tag not in archived_channel_tags]
    archived = [course for course in courses if course.channel_tag in archived_channel_tags]
    users = session.query(SlackUser).filter(SlackUser.name != 'infobot').all()
    # channels = session.query(Channel).all()
    channels = session.query(Channel).outerjoin(Course, Channel.tag == Course.channel_tag).filter(
        Course.channel_tag == None).all()
    channel_tags = [channel.tag for channel in channels]
    if not channel_tags.__contains__('#general'):
        channel_tags.append('#general')
    return render_template('course.html', watched_courses=watched, unwatched_courses=unwatched, tags=channel_tags,
                           form=form, users=users, archived_courses=archived), 200


@app_course.route('/ui/course/delete', methods=['POST'])
def course_delete():
    # course_id = request.args.get('id')
    # session = Session()
    # course = session.query(Course).filter(Course.id == course_id).first()
    # channel = session.query(Channel).filter(Channel.tag == course.channel_tag).first()
    # client.conversations_close(channel=channel.id)
    # session.query(Channel).filter(Channel.tag == course.channel_tag).delete()
    # session.query(Course).filter(Course.id == course_id).delete()
    # session.commit()
    # session.flush()
    return redirect(url_for('app_course.course_handler'))


@app_course.route('/ui/channel', methods=['POST'])
def add_channel_tag():
    session = Session()
    channel_tag = request.form.get('tag')
    topic = request.form.get('topic')
    users = request.form.getlist('user_select')
    response = client.conversations_create(name=channel_tag, is_private=False)
    channel = response['channel']
    channel_model = Channel(channel['id'], '#' + channel['name'], channel['creator'], datetime.fromtimestamp(
        channel['created']))
    session.add(channel_model)
    client.conversations_setTopic(channel=channel['id'], topic=topic)
    client.conversations_invite(channel=channel['id'], users=users)
    session.commit()
    session.flush()
    return redirect(url_for('app_course.course_handler'))


@app_course.route('/ui/channel/archive', methods=['POST'])
def archive_channel():
    session = Session()
    channel_tag = '#' + request.args.get('tag')
    course = session.query(Course).filter(Course.channel_tag == channel_tag).first()
    course.watch = False
    session.add(course)
    pins = session.query(Pin).join(Channel, Pin.channel == Channel.id).filter(Pin.done == False).filter(Channel.tag == channel_tag).all()
    for pin in pins:
        client.pins_remove(channel=pin.channel, timestamp='%.6f' % pin.timestamp)
        pin.done = True
        session.add(pin)
    reminders = session.query(Reminder).join(Notification, Reminder.notification == Notification.id)\
        .join(Course, Course.id == Notification.site).filter(Course.channel_tag == channel_tag)\
        .filter(Reminder.posted == False).all()
    for reminder in reminders:
        reminder.posted = True
        session.add(reminder)
    channel = session.query(Channel).filter(Channel.tag == channel_tag).first()
    client.conversations_archive(channel=channel.id)
    channel.archived = True
    session.add(channel)
    session.commit()
    session.flush()
    return redirect(url_for('app_course.course_handler'))


@app_course.route('/ui/channel/unarchive', methods=['POST'])
def unarchive_channel():
    session = Session()
    channel_tag = '#' + request.args.get('tag')
    channel = session.query(Channel).filter(Channel.tag == channel_tag).first()
    try:
        client.conversations_join(channel=channel.id)
        client.conversations_unarchive(channel=channel.id)
    except Exception as e:
        print(e)
    channel.archived = False
    session.add(channel)
    session.commit()
    session.flush()
    return redirect(url_for('app_course.course_handler'))
