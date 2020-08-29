import re
from src import logger, progress_queue
from flask import Blueprint, render_template, Response

app_home = Blueprint('app_home', __name__, template_folder='templates')


@app_home.route('/ui/home')
def home():
    logs = logger.read_application_log()
    trace_logs = logger.read_application_trace()
    trace_logs.reverse()
    logs.reverse()
    return render_template('home.html', logs=parse_logs(logs))


@app_home.route('/ui/home/progress')
def progress():
    def generate():
        progress_num = 0
        action = ''
        while progress_num <= 100:
            data = progress_queue.get()
            if data[0] is not None:
                progress_num = data[0]
            if data[1] is not None:
                action = data[1]
            yield "data:" + str(progress_num) + ',' + action + "\n\n"
    return Response(generate(), mimetype='text/event-stream')


def parse_logs(logs):
    result = []
    for log in logs:
        groups = re.search(r'^\[(.*)\] ([A-Z]+): (.*)$', log)
        if groups is not None:
            result.append({'timestamp': groups[1], 'type': groups[2], 'message': groups[3]})
        else:
            result.append({'timestamp': 'unknown', 'type': 'unknown', 'message': log})
    return result
