import requests
from flask import Blueprint, request

from src import config
from src.models.base import DataBase
from src.web_app.api.slack_command_utils import SlackCommandUtils

api_command = Blueprint('api_command', __name__)
default_protocol = 'http'


@api_command.route('/api/command/scraper', methods=['GET', 'POST'])
def command_endpoint():
    database = DataBase()
    data, data_ok = SlackCommandUtils.read_data(request, text_tokens_length=1)
    if not data_ok:
        return 'Invalid request format', 400
    command = data['text']
    if command != 'start' and command != 'stop':
        return 'Invalid request format', 400
    response = requests.get(default_protocol + '://' + config.get('flask_address') + ':' + config.get('flask_port') +
                            '/ui/home/scraper/' + command)
    success_flag = response.status_code == 500
    slack_command_log = SlackCommandUtils.create_slack_command_log(data, success_flag)
    database.insert(slack_command_log)
    if response.status_code == 200:
        return '', 200
    else:
        return 'Error has occurred while commanding scraper', 500
