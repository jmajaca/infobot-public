from flask import Blueprint, Response, get_template_attribute

from main import client
from main.objects.scanner import Scanner
from models.base import DataBase
from src import log_path, Logger

app_nav_bar = Blueprint('app_nav_bar', __name__, template_folder='templates')
scanner = Scanner(client, DataBase())
logger = Logger(log_path)


@app_nav_bar.route('/scan/reactions', methods=['GET'])
def scan_reactions():
    try:
        scanner.scan_reactions()
        return Response(status=200)
    except Exception as e:
        logger.error_log(e)
        return Response(status=500)


@app_nav_bar.route('/scan/users', methods=['GET'])
def scan_users():
    try:
        scanner.scan_users()
        return Response(status=200)
    except Exception as e:
        logger.error_log(e)
        return Response(status=500)


@app_nav_bar.route('/scan/channels', methods=['GET'])
def scan_channels():
    try:
        scanner.scan_channels()
        return Response(status=200)
    except Exception as e:
        logger.error_log(e)
        return Response(status=500)


@app_nav_bar.route('/scan/complete', methods=['GET'])
def scan_complete():
    try:
        scanner.scan_complete()
        return Response(status=200)
    except Exception as e:
        logger.error_log(e)
        return Response(status=500)


@app_nav_bar.route('/status', methods=['GET'])
def get_status(status: str):
    yield "data:" + status + "\n\n"
