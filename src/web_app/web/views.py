from flask import Blueprint, render_template, request, redirect, url_for

from src.models.base import DataBase, Session
from src.models.channel import Channel
from src.models.course import Course
from src.web_app.web.forms import WatchlistForm

app_ui = Blueprint('app_ui', __name__, template_folder='templates')


@app_ui.route('/ui/course', methods=['GET', 'POST'])
def course_handler():
    session = Session()
    form = WatchlistForm()
    courses = session.query(Course).all()
    for course in courses:
        course.url = course.url.split('/')[-1]
    channels = session.query(Channel).all()
    channel_tags = [channel.tag for channel in channels]
    form.init_tags(channel_tags)
    if form.validate_on_submit():
        watch = False
        if request.form.get('watch_input') == 'on':
            watch = True
        if form.id.data == -1:
            new_course = Course(form.name.data, request.form.get('tag_select'), form.url.data, watch)
            session.add(new_course)
            session.commit()
            session.flush()
        else:
            course = session.query(Course).filter(Course.id == form.id.data).first()
            course.name = form.name.data
            course.url = form.url.data
            course.channel_tag = request.form.get('tag_select')
            course.watch = watch
            session.commit()
            session.flush()
        courses = session.query(Course).all()
        form.name.data = ''
        form.url.data = ''
        form.watch.data = True
    watched = [course for course in courses if course.watch]
    unwatched = [course for course in courses if not course.watch]
    return render_template('course.html', watched_courses=watched, unwatched_courses=unwatched, tags=channel_tags,
                           form=form), 200


@app_ui.route('/ui/course/delete', methods=['POST'])
def course_delete():
    course_id = request.args.get('id')
    session = Session()
    session.query(Course).filter(Course.id == course_id).delete()
    session.commit()
    session.flush()
    return redirect(url_for('app_ui.course_handler'))
