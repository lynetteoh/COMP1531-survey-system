from flask import Flask, request, render_template, redirect
from security import login_success


def login_page(request, page):
	if request.method == "GET":
		print(request.args.get('attempt'))
		return render_template("login.html", page = page, attempt = request.args.get('attempt'))
	if request.method == "POST":
		success = login_success(request.form["username"], request.form["password"], request.remote_addr)
		if success == "Success":
			if page:
				return redirect(page.replace("@2F", "/"))
			return redirect("/home")
		else:
			attempt = 1
			if request.args.get('attempt'):
				attempt = int(request.args.get('attempt')) + 1
			if page:
				return redirect("/login/"+page + "?attempt=" + str(attempt))
			return redirect("/login"+ "?attempt=" + str(attempt))