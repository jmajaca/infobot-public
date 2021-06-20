import requests
from flask import Blueprint, request
from src import config
from src.models.base import DataBase
from src.models.model_list import Channel

from src.web_app.api.slack_command_utils import SlackCommandUtils

api_course = Blueprint('api_course', __name__)
default_protocol = 'http'


@api_course.route('/api/course/archive', methods=['GET', 'POST'])
def archive_course():
    database = DataBase()
    data, data_ok = SlackCommandUtils.read_data(request=request, text_tokens_length=1)
    if not data_ok:
        return 'Invalid request format', 400
    print('> TEXT:', data['text'])
    channel = database.select(Channel, id=data['text'][2:-1])
    response = requests.post(default_protocol + '://' + config.get('flask_address') + ':' + config.get('flask_port') +
                             '/ui/channel/archive?tag=' + channel.tag[1:])
    success_flag = response.status_code == 200
    slack_command_log = SlackCommandUtils.create_slack_command_log(data, success_flag)
    database.insert(slack_command_log)
    if success_flag:
        return '', 200
    else:
        return 'Error has occurred while archiving the channel', 500
