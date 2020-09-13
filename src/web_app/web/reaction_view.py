from flask import Blueprint, render_template, Response, request

from src.main import client
from src.main.objects.reaction_manager import ReactionManager
from src.models.base import DataBase
from src import Logger

import re

app_reaction = Blueprint('app_reaction', __name__, template_folder='templates')
logger = Logger()
reaction_manager = ReactionManager(client, DataBase(), logger)


@app_reaction.route('/ui/reaction', methods=['GET'])
def get_reactions():
    return render_template('reaction.html', alive=reaction_manager.is_alive()), 200


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
    reaction_manager.scan_hour, reaction_manager.scan_minute = int(match.group(1)), int(match.group(2))
    return Response(status=200)


@app_reaction.route('/ui/reaction/automatic/flip', methods=['GET'])
def manage_automatic_reaction_scan():
    if not reaction_manager.is_alive():
        reaction_manager.start()
    elif reaction_manager.is_alive():
        reaction_manager.close()
    return Response(status=200)


@app_reaction.route('/ui/reaction/automatic', methods=['GET'])
def get_reaction_manager_process_status():
    if reaction_manager.is_alive():
        return {'status': '1'}
    else:
        return {'status': '0'}
