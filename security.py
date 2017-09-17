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

for account in ACCOUNTS:
	print(type(account), account.zID, account.password)

logged_in = {}

###DEPRICATED FUNCTION
def login_success(username, password, ip_addr):
	if (username not in passwords):
		return "User not found"
	if passwords[username] == password:
		logged_in[ip_addr] = time.time()
		return "Success"
	return "Password incorrect"

def login_user(zID, password, ip_addr):
	user = find_user(zID)
	if user.login(zID, password):
		logged_in[ip_addr] = time.time()
		return user
	return None

def has_access(ip_addr, overrideTime = False):
	if ip_addr in logged_in:
		if overrideTime or logged_in[ip_addr] >= time.time() - 1800: #30 mins after last action
			return True
	return False

def update_time(ip_addr):
	if ip_addr in logged_in:
		logged_in[ip_addr] = time.time();

def logout(ip_addr):
	if ip_addr in logged_in:
		logged_in.pop(ip_addr)
	return redirect('/')