from flask import Blueprint, request, jsonify

from src import Logger
from src.main.objects.reaction_manager import ReactionManager
from src.models.base import DataBase
from src.models.model_list import SlackUser
from src.web_app.api.slack_command_utils import SlackCommandUtils

api_reaction = Blueprint('api_reaction', __name__)
reaction_manager = ReactionManager(Logger())


@api_reaction.route('/api/reaction/top', methods=['GET', 'POST'])
def get_reaction_table():
    database = DataBase()
    data, data_ok = SlackCommandUtils.read_data(request=request, text_tokens_length=2)
    try:
        reaction_name = data['text'][1]
        if not data_ok:
            return 'Invalid request format', 400
        if data['text'][0] == 'r':
            result = reaction_manager.get_top_receivers(reaction_name=reaction_name)
        elif data['text'][0] == 's':
            result = reaction_manager.get_top_senders(reaction_name=reaction_name)
        else:
            return 'Invalid request format', 400
        response = {'response_type': 'in_channel'}
        response_text = 'Here is top chart for :' + reaction_name + ':\n\n'
        for i, info in enumerate(result):
            response_text += str(i + 1) + '. <@' + database.select(SlackUser, name=info[0]).id + '> with ' + str(info[1]) + ' total '
            if data['text'][0] == 'r':
                response_text += 'received'
            elif data['text'][0] == 's':
                response_text += 'sent'
            response_text += ' reactions\n'
        response['text'] = response_text
        slack_command_log = SlackCommandUtils.create_slack_command_log(data, True)
        database.insert(slack_command_log)
        return jsonify(response), 200
    except Exception as e:
        slack_command_log = SlackCommandUtils.create_slack_command_log(data, False)
        database.insert(slack_command_log)
        return '', 500
