from flask import Blueprint, render_template, request

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
	for elem in ['name', 'author', 'from', 'to', 'posted']:
		filters[elem] = request.args.get(elem)

	# validation
	filters.pop('name') if filters['name'] == "Nothing selected" else None
	filters.pop('author') if filters['author'] == "Nothing selected" else None
	filters.pop('from') if not filters['from'] else None    # default is empty string
	filters.pop('to') if not filters['to'] else None

	reminders = reminder_manager.get_reminders(**filters)
	courses, authors = reminder_manager.get_filter_options()
	return render_template('reminder.html', courses=courses, authors=authors, reminders=reminders), 200