from flask import Flask
import multiprocessing
from src import config
from src.web_app.web.views import app_ui

# https://stackoverflow.com/questions/11994325/how-to-divide-flask-app-into-multiple-py-files

app = Flask(__name__, template_folder='application/templates')
app.register_blueprint(app_ui)

def start_app():
    global config
    app.secret_key = 'info bot'
    app.config['SESSION_TYPE'] = 'filesystem'
    multiprocessing.Process(target=app.run, args=(config['flask_address'], config['flask_port'], False,)).start()
    del config


def start_app_windows():
    app.run(config['flask_address'], config['flask_port'], False)
