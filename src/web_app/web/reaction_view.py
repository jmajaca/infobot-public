from flask import Blueprint, render_template, Response, request

from main import client
from main.objects.reaction_manager import ReactionManager
from models.base import DataBase
from src import Logger, log_path

import re

app_reaction = Blueprint('app_reaction', __name__, template_folder='templates')
logger = Logger(log_path)
reaction_manager = ReactionManager(client, DataBase(), logger)


@app_reaction.route('/ui/reaction', methods=['GET'])
def get_reactions():
    return render_template('reaction.html'), 200


@app_reaction.route('/ui/reaction/scan', methods=['GET'])
def scan_reactions():
    try:
        reaction_manager.count()
        return Response(status=200)
    except Exception as e:
        logger.error_log(e)
        return Response(status=500)


@app_reaction.route('/ui/reaction/time', methods=['POST'])
def new_reaction_scan_time():
    match = re.search('time=([0-9]{2})%3A([0-9]{2})', request.data.decode("utf-8"))
    print(match.group(2))
    return Response(status=200)
