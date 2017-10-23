#Security file
#Implements security checks
#Exports only function login_success

import time
from datetime import datetime
from flask import redirect
from courses import find_course
from securityClasses import Student, Staff, Admin, Guest
from databasing import db_select, db_execute
import sqlite3
import csv

DATABASE_FILENAME = "data.db"

ENROLMENTS_FILE = "enrolments.csv"
PASSWORD_FILE = "passwords.csv"

print("Checking accounts data matches database...")
#Loading users - done on startup.
if not db_select(DATABASE_FILENAME, 'SELECT * FROM PASSWORDS WHERE ZID = "1"'):
	db_execute(DATABASE_FILENAME, 'INSERT INTO PASSWORDS (ZID, PASSWORD, ROLE) VALUES ("1", "adminPass", "admin")')
with open(PASSWORD_FILE,'r') as csv_in:
	existing_values = db_select(DATABASE_FILENAME, 'SELECT ZID, PASSWORD, ROLE FROM PASSWORDS')
	reader = csv.reader(csv_in)
	for zID, password, user_type in reader:
		if (int(zID), password, user_type) not in existing_values:
			db_execute(DATABASE_FILENAME, 'INSERT INTO PASSWORDS (ZID, PASSWORD, ROLE) VALUES ("{0}", "{1}", "{2}")'.format(
							zID, password, user_type
					   ))
#Enrolling students - done on startup.
with open(ENROLMENTS_FILE,'r') as csv_in:
	existing_values = db_select(DATABASE_FILENAME, 'SELECT ZID, COURSE, SEMESTER FROM ENROLMENTS')
	reader = csv.reader(csv_in)
	for zID, name, semester in reader:
		if (int(zID), name, semester) not in existing_values:
			db_execute(DATABASE_FILENAME, 'INSERT INTO ENROLMENTS (ZID, COURSE, SEMESTER) VALUES ("{0}", "{1}", "{2}")'.format(
							zID, name, semester
					   ))
print("Loading complete.")

logged_in = {}

def guest_register(zID, password, course):
	db_execute(DATABASE_FILENAME, 'INSERT INTO PASSWORDS (ZID, PASSWORD, ROLE) VALUES ("{0}", "{1}", "{2}")'.format(
							zID, password, 'pending:'+course.name+':'+course.semester))

def get_pending_guests():
	users = db_select(DATABASE_FILENAME, 'SELECT ZID, ROLE FROM PASSWORDS')
	guests = []
	for user in users:
		if user[1].startswith('pending'):
			guests.append([int(user[0]), find_course(user[1].split(':')[1], user[1].split(':')[2])])

	return guests


def approve_guest(zID):
	role = db_select(DATABASE_FILENAME, 'SELECT ROLE FROM PASSWORDS WHERE ZID = '+str(zID))[0][0]
	db_execute(DATABASE_FILENAME, 'UPDATE PASSWORDS SET ROLE = "guest" WHERE ZID = ' + str(zID))
	db_execute(DATABASE_FILENAME, 'INSERT INTO ENROLMENTS (ZID, COURSE, SEMESTER) VALUES ("{0}", "{1}", "{2}")'.format(
						zID, role.split(':')[1], role.split(':')[2]
					))

def deny_guest(zID):
	db_execute(DATABASE_FILENAME, 'DELETE FROM PASSWORDS WHERE ZID = ' + str(zID))


def login_user(zID, password, ip_addr):
	zID = zID.replace('z', '')
	try:
		int(zID)
	except:
		return None
	results = db_select(DATABASE_FILENAME, 'SELECT PASSWORD, ROLE FROM PASSWORDS WHERE ZID = ' + str(zID))
	if len(results) == 0:
		print('No user found with that zID')
		return None
	actual_password, role = results[0]

	if role == 'admin':
		user = Admin(zID, actual_password)
	elif role == 'staff':
		user = Staff(zID, actual_password)
		enrolled_courses = db_select(DATABASE_FILENAME, 'SELECT COURSE, SEMESTER FROM ENROLMENTS WHERE ZID = '+str(zID))
		for course, semester in enrolled_courses:
			user.enrol(find_course(course, semester))
	elif role == 'student':
		user = Student(zID, actual_password)
		enrolled_courses = db_select(DATABASE_FILENAME, 'SELECT COURSE, SEMESTER FROM ENROLMENTS WHERE ZID = '+str(zID))
		for course, semester in enrolled_courses:
			user.enrol(find_course(course, semester))
	elif role == 'guest':
		user = Guest(zID, actual_password)
		enrolled_courses = db_select(DATABASE_FILENAME, 'SELECT COURSE, SEMESTER FROM ENROLMENTS WHERE ZID = '+str(zID))
		for course, semester in enrolled_courses:
			user.enrol(find_course(course, semester))

	if user.login(zID, password):
		logged_in[ip_addr] = user
		print(zID, "logged in", "["+str(datetime.now())+"]",
			  {Admin: 'Admin', Student: 'Student', Staff: 'Staff', Guest: 'Guest'}[type(user)])
		return user
	return None

def has_access(ip_addr, level, overrideTime = False):
	if ip_addr in logged_in:
		if level == type(logged_in[ip_addr]) or type(logged_in[ip_addr]) == Admin:
			if overrideTime or logged_in[ip_addr].last_activity >= time.time() - 1800: #30 mins after last action
				return True
		if level == Student and type(logged_in[ip_addr]) == Guest: #Special case as Guests have same priveleges as Student
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
		user = logged_in[ip_addr]
		print(user.zID, "logged out", "["+str(datetime.now())+"]",
			  {Admin: 'Admin', Student: 'Student', Staff: 'Staff', Guest: 'Guest'}[type(user)])
		logged_in.pop(ip_addr)
	return redirect('/login')