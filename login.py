from flask import Flask, request, render_template, redirect
from security import login_success


def login_page(request, page):
	if request.method == "GET":
		return render_template("login.html", page = page)
	if request.method == "POST":
		success = login_success(request.form["username"], request.form["password"], request.remote_addr)
		if success == "Success":
			if page:
				return redirect(page.replace("@2F", "/"))
			return redirect("/home")
		else:
			if page:
				return redirect("/login/"+page)
			return redirect("/login")