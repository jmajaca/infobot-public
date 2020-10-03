from flask import Blueprint, render_template, request, jsonify

from src import Logger, log_path
from src.main import client
from src.main.objects.reminder_manager import ReminderManager
from src.models.base import DataBase

app_reminder = Blueprint('app_reminder', __name__, template_folder='templates')
logger = Logger(log_path)
reminder_manager = ReminderManager(client, DataBase(), logger)

@app_reminder.route('/ui/reminder', methods=['GET'])
def get_reminders():
	reminders = reminder_manager.get_reminders()
	courses, authors = reminder_manager.get_filter_options()
	return render_template('reminder.html', courses=courses, authors=authors, reminders=reminders), 200

@app_reminder.route('/ui/reminder/filter', methods=['POST'])
def filter_reminders():
	filters = dict()
	if len(request.args) != 0:
		for elem in ['name', 'author', 'from', 'to', 'posted']:
			filters[elem] = request.args.get(elem)

		# getting rid of not selected filters
		filters.pop('name') if filters['name'] == "Nothing selected" else None
		filters.pop('author') if filters['author'] == "Nothing selected" else None
		filters.pop('from') if not filters['from'] else None    # default is empty string
		filters.pop('to') if not filters['to'] else None

		reminders = reminder_manager.get_reminders(**filters)

	# canceling filters and returning all reminders
	else:
		reminders = reminder_manager.get_reminders()

	reminders_json = list()
	# turn a list of reminders into a list of reminder attributes in dict form
	# end_date and timer are parsed to string because timestamp and interval are not json serializable
	for i,reminder in enumerate(reminders):
		reminders_json.append({'end_date': str(reminder.end_date), 'timer': str(reminder.timer), 'text': reminder.text, 'posted': reminder.posted})
	return {'result': len(reminders_json), 'rows': reminders_json}