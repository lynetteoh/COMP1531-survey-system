#Security file
#Implements security checks
#Exports only function login_success

import time

passwords = {"admin" : "adminPass"}
logged_in = {}

def login_success(username, password, ip_addr):
	if (username not in passwords):
		return "User not found"
	if passwords[username] == password:
		logged_in[ip_addr] = time.time()
		return "Success"
	return "Password incorrect"

def has_access(ip_addr, overrideTime = False):
	if ip_addr in logged_in:
		if overrideTime or logged_in[ip_addr] >= time.time() - 1800: #30 mins after last action
			return True
	return False

def update_time(ip_addr):
	if ip_addr in logged_in:
		logged_in[ip_addr] = time.time();

def logout(ip_addr):
	if ip_addr not in logged_in:
		return "<h3><center>Already logged out</center></h3> <center><a href = '/'> Front Page </a> </center>"
	else:
		logged_in.pop(ip_addr)
		return "<h3><center>Logged out</center></h3> <center><a href = '/'> Front Page </a> </center>"