import time

from flask import Blueprint, render_template, Response

app_home = Blueprint('app_home', __name__, template_folder='templates')

progress = 25


@app_home.route('/ui/home')
def home():
    return render_template('home.html')


@app_home.route('/ui/home/progress')
def progress():
    def generate():
        x = 0

        while x <= 100:
            yield "data:" + str(x) + "\n\n"
            x = x + 10
            time.sleep(0.5)

    return Response(generate(), mimetype='text/event-stream')
