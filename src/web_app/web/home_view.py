import multiprocessing
import re

from src.main.main import start_scraper_process
from src import logger, progress_queue, NONE_PROGRESS
from flask import Blueprint, render_template, redirect, url_for

app_home = Blueprint('app_home', __name__, template_folder='templates')
scraper_process: multiprocessing.Process = None


@app_home.route('/ui/home')
def home():
    return render_template('home.html', logs=logger.get_application_logs(), trace_logs=logger.get_trace_logs())


@app_home.route('/ui/home/scraper/start')
def start_scraper():
    global scraper_process
    if scraper_process is None or not scraper_process.is_alive():
        scraper_process = multiprocessing.Process(target=start_scraper_process)
        scraper_process.start()
        progress_queue.put((NONE_PROGRESS, 'Starting scraper'))
    return redirect(url_for('app_home.home'))


@app_home.route('/ui/home/scraper/stop')
def stop_scraper():
    global scraper_process
    if scraper_process is not None and scraper_process.is_alive():
        scraper_process.kill()
        progress_queue.put((NONE_PROGRESS, 'Program finished with exit code 130', 'off'))
    return redirect(url_for('app_home.home'))
