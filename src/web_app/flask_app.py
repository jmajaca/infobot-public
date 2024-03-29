from flask import Flask
import multiprocessing
from src import config
from src.web_app.api.command_api import api_command
from src.web_app.api.course_api import api_course
from src.web_app.api.reaction_api import api_reaction
from src.web_app.web.course_view import app_course
from src.web_app.web.home_view import app_home

# https://stackoverflow.com/questions/11994325/how-to-divide-flask-app-into-multiple-py-files
from src.web_app.web.base_view import app_base
from src.web_app.web.nav_bar_view import app_nav_bar
from src.web_app.web.reaction_view import app_reaction
from src.web_app.web.reminder_view import app_reminder

app = Flask(__name__, template_folder='application/templates')
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.register_blueprint(app_course)
app.register_blueprint(app_home)
app.register_blueprint(app_base)
app.register_blueprint(app_nav_bar)
app.register_blueprint(app_reaction)
app.register_blueprint(app_reminder)
app.register_blueprint(api_course)
app.register_blueprint(api_reaction)
app.register_blueprint(api_command)


def start_app():
    global config
    app.secret_key = 'info bot'
    app.config['SESSION_TYPE'] = 'filesystem'
    multiprocessing.Process(target=app.run, args=(config['flask_address'], config['flask_port'], False,)).start()
    del config


def start_app_windows():
    app.run(config['flask_address'], config['flask_port'], False)
