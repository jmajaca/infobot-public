from flask import Blueprint, render_template

from src.models.base import DataBase
from src.models.channel import Channel
from src.models.course import Course

app_ui = Blueprint('simple_page', __name__, template_folder='templates')


@app_ui.route('/ui/', methods=['GET'])
def show():
    database = DataBase()
    courses = database.select_many(Course)
    for course in courses:
        course.url = course.url.split('/')[-1]
    channels = database.select_many(Channel)
    channel_tags = [channel.tag for channel in channels]
    return render_template('course_watch_list.html', courses=courses, tags=channel_tags), 200
