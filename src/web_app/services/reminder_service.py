
def remove_unused_filters(filters):
	# getting rid of not selected filters
	filters.pop('name') if filters['name'] == "Nothing selected" else None
	filters.pop('author') if filters['author'] == "Nothing selected" else None
	filters.pop('from') if not filters['from'] else None  # default is empty string
	filters.pop('to') if not filters['to'] else None
	return filters


def parse_reminders(reminders):
	# turn a list of reminders into a list of reminder attributes in dict form
	# end_date and timer are parsed to string because timestamp and interval are not json serializable
	reminders_json = list()
	for reminder in reminders:
		reminders_json.append({'id': reminder.id,
		                       'end_date': str(reminder.end_date),
		                       'timer': str(reminder.timer),
		                       'text': reminder.text,
		                       'posted': reminder.posted})
	return {'result': len(reminders_json), 'rows': reminders_json}


def parse_timer(timer):
	# validation timer=positive integer
	timer_in_seconds = 0
	# can't be empty string
	if not timer:
		raise ValueError
	# days:hours:minutes:seconds
	elif ':' in timer:
		values = timer.split(':')
		for i, value in enumerate(values):
			if int(value) < 0 or int(value) > 999999999:
				raise ValueError
			else:
				# hours:minutes:seconds
				if len(values) == 3:
					i += 1
				# minutes:seconds
				elif len(values) == 2:
					i += 2
				if i == 0:  # days -> seconds
					timer_in_seconds += int(value) * 24 * 60 * 60
				elif i == 1:  # hours -> seconds
					timer_in_seconds += int(value) * 60 * 60
				elif i == 2:  # minutes -> seconds
					timer_in_seconds += int(value) * 60
				elif i == 3:  # seconds -> seconds
					timer_in_seconds += int(value)
				else:
					raise ValueError
	# must be a number where 0 < number <= 999999999
	elif int(timer) < 0 or int(timer) > 999999999:
		raise ValueError