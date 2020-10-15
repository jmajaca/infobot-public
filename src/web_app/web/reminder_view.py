import re

from flask import Blueprint, render_template, request, make_response, Response

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
		reminders_json.append({'id': reminder.id,
		                       'end_date': str(reminder.end_date),
		                       'timer': str(reminder.timer),
		                       'text': reminder.text,
		                       'posted': reminder.posted})
	return {'result': len(reminders_json), 'rows': reminders_json}


@app_reminder.route('/ui/reminder/save', methods=['POST'])
def save_reminder():
	reminder_data = dict()
	for elem in ['id' ,'end_date', 'timer', 'text', 'posted']:
		if elem == 'timer':
			# default format includes string "days"
			reminder_data[elem] = re.sub( r'[a-zA-Z\s]', r'', request.args.get(elem))
			reminder_data[elem] = reminder_data[elem].replace(',',':')
			continue
		reminder_data[elem] = request.args.get(elem)

	# validation timer=positive integer01,
	error_response = Response(status=400, mimetype='application/json')
	timer_in_seconds = 0
	try:
		# can't be empty string
		if not reminder_data['timer']:
			return error_response
		# days:hour:minutes:seconds, all > 0
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
