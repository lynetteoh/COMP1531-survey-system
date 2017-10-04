#Security file
#Implements security checks
#Exports only function login_success

import time
from flask import redirect
from courses import COURSES, find_course
from securityClasses import Student, Staff, Admin
import csv

ENROLMENTS_FILE = "enrolments.csv"
PASSWORD_FILE = "passwords.csv"
ACCOUNTS = [Admin("admin", "adminPass")]


def find_user(zID):
	for user in ACCOUNTS:
		if user.zID == zID:
			return user
	return None

print("Loading accounts data...")
#Loading users - done on startup.
with open(PASSWORD_FILE,'r') as csv_in:
	reader = csv.reader(csv_in)
	for zID, password, user_type in reader:
		if user_type == "staff":
			user = Staff(zID, password)
			ACCOUNTS.append(user)
		elif user_type == "student":
			user = Student(zID, password)
			ACCOUNTS.append(user)
		elif user_type == "admin":
			user = Admin(zID, password)
			ACCOUNTS.append(user)
#Enrolling students - done on startup.
with open(ENROLMENTS_FILE,'r') as csv_in:
	reader = csv.reader(csv_in)
	for zID, name, semester in reader:
		user = find_user(zID)
		course = find_course(name, semester)
		user.enrol(course)
print("Loading complete.")

logged_in = {}

def login_user(zID, password, ip_addr):
	user = find_user(zID)
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