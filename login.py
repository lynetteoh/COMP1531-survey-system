from flask import Flask, request, render_template, redirect
from security import login_user, has_access
from securityClasses import Admin, Staff, Student, Guest


def login_page(request, role, page):
	if request.method == "GET":
		logged_in_as = None
		if (has_access(request.remote_addr, Student)):
			logged_in_as = 'Student'
		if (has_access(request.remote_addr, Staff)):
			logged_in_as = 'Staff'
		return render_template("login.html", page = page, role = role, logged_in_as =  logged_in_as, attempt = request.args.get('attempt'))
	if request.method == "POST":
		user = login_user(request.form["username"], request.form["password"], request.remote_addr)
		if user == None:
			attempt = 1
			if request.args.get('attempt'):
				attempt = int(request.args.get('attempt')) + 1
			if page:
				return redirect("/login/"+page + "?attempt=" + str(attempt))
			return redirect("/login"+ "?attempt=" + str(attempt))

		if type(user) is Admin:
			if page:
				return redirect(page.replace("@2F", "/"))
			return redirect("/adminHome") #Admin Homepage
		elif type(user) is Staff:
			if page:
				return redirect(page.replace("@2F", "/"))
			return redirect("/staffHome") #Staff Homepage
		elif type(user) is Student or type(user) is Guest:
			if page:
				return redirect(page.replace("@2F", "/"))
			return redirect("/studentHome") #Student Homepage
		else:
			return "Something went wrong"