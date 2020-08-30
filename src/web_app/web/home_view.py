import multiprocessing
import re

from main.main import start_scraper_process
from src import logger, progress_queue, none_progress
from flask import Blueprint, render_template, Response, redirect, url_for

app_home = Blueprint('app_home', __name__, template_folder='templates')
scraper_process: multiprocessing.Process = None

@app_home.route('/ui/home')
def home():
    logs = logger.read_application_log()
    trace_logs = logger.read_application_trace()
    logs.reverse()
    return render_template('home.html', logs=parse_logs(logs), trace_logs=parse_trace_logs(trace_logs))


@app_home.route('/ui/home/progress')
def progress():
    def generate():
        progress_num = 0
        action = ''
        state = 'normal'
        while progress_num <= 100:
            data = progress_queue.get()
            if data[0] is not None:
                progress_num = data[0]
            if data[1] is not None:
                action = data[1]
            if len(data) >= 3 and data[2] is not None:
                state = data[2]
            yield "data:" + str(progress_num) + ',' + action + ',' + state + "\n\n"
    return Response(generate(), mimetype='text/event-stream')


@app_home.route('/ui/home/scraper/start')
def start_scraper():
    global scraper_process
    if scraper_process is None or not scraper_process.is_alive():
        scraper_process = multiprocessing.Process(target=start_scraper_process)
        scraper_process.start()
    return redirect(url_for('app_home.home'))


@app_home.route('/ui/home/scraper/stop')
def stop_scraper():
    global scraper_process
    if scraper_process is not None and scraper_process.is_alive():
        scraper_process.kill()
        progress_queue.put((none_progress, 'Program finished with exit code 130', 'error'))
    return redirect(url_for('app_home.home'))


def parse_logs(logs):
    result = []
    for log in logs:
        groups = re.search(r'^\[(.*)\] ([A-Z]+): (.*)$', log)
        if groups is not None:
            if groups[2] == 'ERROR':
                # legacy problem
                # trace_uuid = re.search(r'^.* uuid (.+).$', groups[3])[1]
                # result.append({'timestamp': groups[1], 'type': groups[2], 'message': groups[3], 'trace_uuid': trace_uuid})
                trace_uuid = re.search(r'uuid ([A-Za-z0-9]+)', groups[3])
                if trace_uuid is not None:
                    result.append(
                        {'timestamp': groups[1], 'type': groups[2], 'message': groups[3], 'trace_uuid': trace_uuid[1]})
            else:
                result.append({'timestamp': groups[1], 'type': groups[2], 'message': groups[3]})
        else:
            result.append({'timestamp': 'unknown', 'type': 'unknown', 'message': log})
    return result


def parse_trace_logs(trace_log_lines):
    first = True
    result = ''
    uuid = ''
    trace_log = dict()
    for line in trace_log_lines + [None]:
        if line is None:
            trace_log[uuid] = result
            break
        uuid_match = re.search(r'uuid=([A-Za-z0-9]+)', line)
        if uuid_match is not None:
            if first:
                uuid = uuid_match[1]
                first = False
            else:
                trace_log[uuid] = result
                uuid = uuid_match[1]
                result = ''
        result += line + '\n'
    return trace_log
