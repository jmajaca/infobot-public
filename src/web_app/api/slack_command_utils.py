from src.models.slack_command_log import SlackCommandLog
from datetime import datetime


class SlackCommandUtils:

    @staticmethod
    def read_data(request, text_tokens_length=None):
        data = {}
        for key in request.form.keys():
            data[key] = request.form[key]
        data['text'] = data['text'].strip()
        if text_tokens_length is None:
            return data, True
        elif len(data['text'].split()) != text_tokens_length:
            return data, False
        else:
            data['text'] = data['text'].split()
            return data, True

    @staticmethod
    def create_slack_command_log(data, success):
        if len(data['text']) == 1:
            text = data['text']
        else:
            text = ' '.join(data['text'])
        return SlackCommandLog(text=text, command=data['command'], user_id=data['user_id'],
                               channel_id=data['channel_id'], creation_time=datetime.now(),
                               success=success)
