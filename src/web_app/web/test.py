import multiprocessing

from src.main.main import start_scraper_process
from src import logger, progress_queue, NONE_PROGRESS
from flask import Blueprint, render_template, redirect, url_for
from flask import jsonify


test = Blueprint('test', __name__)


@test.route('/api/test')
def home():
    return jsonify("""
    {
        id: 5
    }
    """)