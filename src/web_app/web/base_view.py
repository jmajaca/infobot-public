from flask import Blueprint, url_for, redirect, Response

from src import progress_queue

app_base = Blueprint('app_base', __name__, template_folder='templates')


@app_base.route('/', methods=['GET'])
def base_redirect():
    return redirect(url_for('app_home.home'))


@app_base.route('/ui', methods=['GET'])
def base_redirect_ui():
    return base_redirect()


@app_base.route('/scraper/progress')
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
