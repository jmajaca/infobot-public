from flask import Blueprint, render_template

from src.models.base import DataBase
from src.models.channel import Channel
from src.models.course import Course
from src.web_app.web.forms import WatchlistForm

app_ui = Blueprint('app_ui', __name__, template_folder='templates')


@app_ui.route('/ui/', methods=['GET', 'POST'])
def show():
    database = DataBase()
    form = WatchlistForm()
    courses = database.select_many(Course)
    for course in courses:
        course.url = course.url.split('/')[-1]
    channels = database.select_many(Channel)
    channel_tags = [channel.tag for channel in channels]
    form.init_tags(channel_tags)
    if form.validate_on_submit():
        new_course = Course(form.name.data, form.tag.data, form.url.data, form.watch.data)
        database.insert(new_course)
        courses = database.select_many(Course)
        form.name.data = ''
        form.tag.data = ''
        form.url.data = ''
        form.watch.data = True
    return render_template('course_watch_list.html', courses=courses, tags=channel_tags, form=form), 200
