from courseClass import Course
from databasing import db_select, db_execute
import sqlite3
import csv

COURSE_LISTING = 'courses.csv'
DATABASE_FILENAME = 'data.db'

#Read in courses
print("Loading courses...")
with open(COURSE_LISTING,'r') as csv_in:
	reader = csv.reader(csv_in)
	for name, semester in reader:
		db_execute(DATABASE_FILENAME, 'INSERT INTO COURSES (NAME, SEMESTER) VALUES ("{0}", "{1}")'.format(name, semester), silent = True)
print("Courses loaded.")

def find_course(name, semester):
	result = db_select(DATABASE_FILENAME, 'SELECT NAME, SEMESTER FROM COURSES WHERE NAME = {0} AND SEMESTER = {1}'.format(
							name, semester
						))
	if len(result) == []:
		return None

	course = Course(name, semester, survey = get_survey(name, semester))
	return course

def get_all_courses():
	courses = []
	for name, semester in db_select(DATABASE_FILENAME, 'SELECT NAME, SEMESTER FROM COURSES'):
		courses.append(find_course(name, semester))
	return courses