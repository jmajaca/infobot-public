from flask import Blueprint, url_for, redirect

app_base = Blueprint('app_base', __name__, template_folder='templates')


@app_base.route('/', methods=['GET'])
def base_redirect():
    return redirect(url_for('app_home.home'))


@app_base.route('/ui', methods=['GET'])
def base_redirect_ui():
    return base_redirect()
