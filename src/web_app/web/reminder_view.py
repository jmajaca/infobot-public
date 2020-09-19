from flask import Blueprint, render_template

from src import Logger, log_path
from src.main import client
from src.main.objects.reminder_manager import ReminderManager
from src.models.base import DataBase

app_reminder = Blueprint('app_reminder', __name__, template_folder='templates')
logger = Logger(log_path)
reminder_manager = ReminderManager(client, DataBase(), logger)

@app_reminder.route('/ui/reminder', methods=['GET'])
def get_reminders():
	reminders = reminder_manager.get_all_reminders()
	authors, courses = reminder_manager.get_filter_options()
	return render_template('reminder.html', courses=courses, authors=authors, reminders=reminders), 200