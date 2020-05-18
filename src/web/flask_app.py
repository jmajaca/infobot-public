from flask import Flask
import multiprocessing
from src import config

# https://stackoverflow.com/questions/11994325/how-to-divide-flask-app-into-multiple-py-files

app = Flask(__name__, template_folder='application/templates')


def start_app():
    global config
    app.secret_key = 'info bot'
    app.config['SESSION_TYPE'] = 'filesystem'
    multiprocessing.Process(target=app.run, args=(config['flask_address'], config['flask_port'], False,)).start()
    del config
