from flask import Flask, request, render_template, redirect
from security import login_success
from securityClasses import Admin, Staff, Student


def login_page(request, page):
	if request.method == "GET":
		print(request.args.get('attempt'))
		return render_template("login.html", page = page, attempt = request.args.get('attempt'))
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
			return redirect("/home") #Admin Homepage
		elif type(user) is Staff:
			return redirect("/home") #Staff Homepage
		elif type(user) is Student:
			return redirect("/home") #Student Homepage
		else:
			return "Something went wrong"