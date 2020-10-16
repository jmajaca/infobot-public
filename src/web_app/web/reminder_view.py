import re

from flask import Blueprint, render_template, request, make_response, Response

from src import Logger, log_path
from src.main import client
from src.main.objects.reminder_manager import ReminderManager
from src.models.base import DataBase

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
		reminders_json.append({'id': reminder.id,
		                       'end_date': str(reminder.end_date),
		                       'timer': str(reminder.timer),
		                       'text': reminder.text,
		                       'posted': reminder.posted})
	return {'result': len(reminders_json), 'rows': reminders_json}


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
	for elem in ['id' ,'end_date', 'timer', 'text', 'posted']:
		if elem == 'timer':
			# default format includes string "days", remove it and split data by :
			reminder_data[elem] = request.args.get(elem).replace(' days, ', ':')
			continue
		reminder_data[elem] = request.args.get(elem)

	# validation timer=positive integer01,
	error_response = Response(status=400, mimetype='application/json')
	timer_in_seconds = 0
	try:
		# can't be empty string
		if not reminder_data['timer']:
			return error_response
		# days:hours:minutes:seconds
		elif ':' in reminder_data['timer']:
			values = reminder_data['timer'].split(':')
			for i,value in enumerate(values):
					if int(value) < 0 or int(value) > 999999999:
						return error_response
					else:
						# hours:minutes:seconds
						if len(values) == 3:
							i +=1
						# minutes:seconds
						elif len(values) == 2:
							i +=2
						if i==0:    # days -> seconds
							timer_in_seconds += int(value)*24*60*60
						elif i==1:  # hours -> seconds
							timer_in_seconds += int(value)*60*60
						elif i==2:  # minutes -> seconds
							timer_in_seconds += int(value)*60
						elif i==3:  # seconds -> seconds
							timer_in_seconds += int(value)
						else:
							return error_response
		# must be a number where 0 < number <= 999999999
		elif int(reminder_data['timer']) < 0 or int(reminder_data['timer']) > 999999999:
			return error_response
	except ValueError:
		return error_response

	# parse timer to large integer representing seconds
	reminder_data['timer'] = timer_in_seconds

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
