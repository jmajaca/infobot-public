from flask import Blueprint
from main.objects.scanner import Scanner

app_nav_bar = Blueprint('app_nav_bar', __name__, template_folder='templates')


@app_nav_bar.route('/scan/reactions', methods=['GET'])
def scan_reactions():
    print(Scanner.__doc__)
    pass


@app_nav_bar.route('/scan/users', methods=['GET'])
def scan_users():
    pass


@app_nav_bar.route('/scan/channels', methods=['GET'])
def scan_channels():
    pass


@app_nav_bar.route('/scan/complete', methods=['GET'])
def scan_complete():
    pass

