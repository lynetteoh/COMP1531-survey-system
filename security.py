#Security file
#Implements security checks
#Exports only function login_success

import time
from flask import redirect
from courses import find_course
from securityClasses import Student, Staff, Admin
from databasing import db_select, db_execute
import sqlite3
import csv

DATABASE_FILENAME = "data.db"

ENROLMENTS_FILE = "enrolments.csv"
PASSWORD_FILE = "passwords.csv"

print("Loading accounts data into database...")
#Loading users - done on startup.
db_execute(DATABASE_FILENAME, 'INSERT INTO PASSWORDS (ZID, PASSWORD, ROLE) VALUES ("admin", "adminPass", "admin")')
with open(PASSWORD_FILE,'r') as csv_in:
	reader = csv.reader(csv_in)
	for zID, password, user_type in reader:
		db_execute(DATABASE_FILENAME, 'INSERT INTO PASSWORDS (ZID, PASSWORD, ROLE) VALUES ("{0}", "{1}", "{2}")'.format(
						zID, password, user_type
				   ), silent = True)
#Enrolling students - done on startup.
with open(ENROLMENTS_FILE,'r') as csv_in:
	reader = csv.reader(csv_in)
	for zID, name, semester in reader:
		db_execute(DATABASE_FILENAME, 'INSERT INTO ENROLMENTS (ZID, COURSE, SEMESTER) VALUES ("{0}", "{1}", "{2}")'.format(
						zID, name, semester
				   ), silent = True)
print("Loading complete.")

logged_in = {}

def login_user(zID, password, ip_addr):
	results = db_select(DATABASE_FILENAME, 'SELECT PASSWORD, ROLE FROM PASSWORDS WHERE ZID = ' + str(zID))
	if len(results) == 0:
		return None
	actual_password, role = results[0]

	if role == 'admin':
		user = Admin(zID, actual_password)
	elif role == 'staff':
		user = Staff(zID, actual_password)
	else:
		user = Student(zID, actual_password)
		enrolled_courses = db_select(DATABASE_FILENAME, 'SELECT COURSE, SEMESTER FROM ENROLMENTS WHERE ZID = '+str(zID))
		for course, semester in enrolled_courses:
			user.enrol(find_course(course, semester))

	if user.login(zID, password):
		logged_in[ip_addr] = user
		print(zID, "logged in", "["+str(time.time())+"]",
			  "(Admin)" if type(user) == Admin else ("(Student)" if type(user) == Student else "(Staff)"))
		return user
	return None

def has_access(ip_addr, level, overrideTime = False):
	if ip_addr in logged_in:
		if level == type(logged_in[ip_addr]) or type(logged_in[ip_addr]) == Admin:
			if overrideTime or logged_in[ip_addr].last_activity >= time.time() - 1800: #30 mins after last action
				return True
	return False

def get_user(ip_addr):
	if ip_addr not in logged_in:
		return None
	return logged_in[ip_addr]

def update_time(ip_addr):
	if ip_addr in logged_in:
		logged_in[ip_addr].last_activity = time.time();

def logout(ip_addr):
	if ip_addr in logged_in:
		print(zID, "logged out", "["+str(time.time())+"]",
			  "(Admin)" if type(logged_in[ip_addr]) == Admin else ("(Student)" if type(logged_in[ip_addr]) == Student else "(Staff)"))
		logged_in.pop(ip_addr)
	return redirect('/login')