from flask import Blueprint, render_template, Response, request, redirect, url_for

from src.main import client
from src.main.objects.reaction_scrapper import ReactionScrapper
from src.models.base import DataBase, Session
from src import Logger
from src.main.objects.reaction_manager import ReactionManager
import re

app_reaction = Blueprint('app_reaction', __name__, template_folder='templates')
logger = Logger()
reaction_scrapper = ReactionScrapper(client, DataBase(), logger)
reaction_manager = ReactionManager(logger)


@app_reaction.route('/ui/reaction/', methods=['GET', 'POST'])
def get_reactions():
    reaction_name = 'default'
    if request.method == 'POST':
        reaction_name = request.args.get('name')
        if reaction_name == '':
            reaction_name = 'default'
    senders, receivers, top_channels = reaction_manager.get_top_all(search_filter=reaction_name)
    return render_template('reaction.html', senders=senders, receivers=receivers, top_channels=top_channels,
                           alive=reaction_scrapper.is_alive()), 200


@app_reaction.route('/ui/reaction/scan', methods=['GET'])
def scan_reactions():
    try:
        reaction_scrapper.count()
        return Response(status=200)
    except Exception as e:
        logger.error_log(e)
        return Response(status=500)


@app_reaction.route('/ui/reaction/time', methods=['POST'])
def new_reaction_scan_time():
    match = re.search('time=([0-9]{2})%3A([0-9]{2})', request.data.decode("utf-8"))
    reaction_scrapper.scan_hour, reaction_scrapper.scan_minute = int(match.group(1)), int(match.group(2))
    return Response(status=200)


@app_reaction.route('/ui/reaction/automatic/flip', methods=['GET'])
def manage_automatic_reaction_scan():
    if not reaction_scrapper.is_alive():
        reaction_scrapper.start()
    elif reaction_scrapper.is_alive():
        reaction_scrapper.close()
    return Response(status=200)


@app_reaction.route('/ui/reaction/automatic', methods=['GET'])
def get_reaction_manager_process_status():
    if reaction_scrapper.is_alive():
        return {'status': '1'}
    else:
        return {'status': '0'}
