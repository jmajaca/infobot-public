import csv
import os

from src.models.course import Course
from src.models.base import DataBase

current_path = os.path.dirname(os.path.realpath(__file__))


def start():
    database = DataBase()
    with open(current_path + '/course_list.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            course = Course(row['name'], row['tag'], row['url'], True)
            # database.insert(course)
    with open('course_list.csv', 'w') as file:
        file.write('')
