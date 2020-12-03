from flask import Blueprint, render_template, request, Response

from src import Logger, log_path
from src.main import client
from src.main.objects.reminder_manager import ReminderManager
from src.models.base import DataBase
from src.web_app.services import reminder_service


app_reminder = Blueprint('app_reminder', __name__, template_folder='templates')
logger = Logger(log_path)
reminder_manager = ReminderManager(client, DataBase(), logger)  # used for all interactions with database

@app_reminder.route('/ui/reminder', methods=['GET'])
def get_reminders():
	"""
	default mapping with all reminders
	"""
	reminders = reminder_manager.get_reminders()
	courses, authors = reminder_manager.get_filter_options()
	return render_template('reminder.html', courses=courses, authors=authors, reminders=reminders), 200


@app_reminder.route('/ui/reminder/filter', methods=['POST'])
def filter_reminders():
	"""
	mapping for returning only filtered reminders
	params: name : name of the course
			author : first and last name of the author
			from : all dates after it
			to : all dates after it
			posted : true or false, reminder posted in workspace or not
	returns: dict that has form for loading bootstrap table
			result : number of reminders
			rows : all data for reminders, must be JSON serializable
	"""
	filters = dict()
	if len(request.args) != 0:
		for elem in ['name', 'author', 'from', 'to', 'posted']:
			filters[elem] = request.args.get(elem)
		filters = reminder_service.remove_unused_filters(filters)
		reminders = reminder_manager.get_reminders(**filters)

	else:
		# canceling filters and returning all reminders
		reminders = reminder_manager.get_reminders()

	return reminder_service.parse_reminders(reminders)


@app_reminder.route('/ui/reminder/save', methods=['POST'])
def save_reminder():
	"""
	mapping for saving edited reminder data to database
	params: id : id of reminder
			end_date : that of the event
			timer : time left until end_date
			text : description of the reminder
			posted : reminder posted in workspace or not
	returns: 400 if new data doesn't pass validation
			 500 in case of database error
			 200 otherwise
	"""
	reminder_data = dict()
	for elem in ['id', 'end_date', 'timer', 'text', 'posted']:
		reminder_data[elem] = request.args.get(elem)

	# parse timer to large integer representing seconds
	try:
		reminder_data['timer'] = reminder_service.parse_timer(reminder_data['timer'])
	except ValueError:
		return Response(status=400, mimetype='application/json')

	if reminder_manager.save(**reminder_data):
		return Response(status=200, mimetype='application/json')
	else:
		return Response(status=500, mimetype='application/json')


@app_reminder.route('/ui/reminder/delete', methods=['POST'])
def delete():
	reminder_id = request.args.get('id')
	if reminder_manager.delete(reminder_id):
		return Response(status=200, mimetype='application/json')
	else:
		return Response(status=500, mimetype='application/json')
