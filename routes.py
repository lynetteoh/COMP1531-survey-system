#Routing program
#Used to route websites.

from flask import Flask, redirect, render_template, request, url_for
from server import app
from login import login_page
from security import has_access
from common import update
from create import view_courses
import json
from fileIO import *

@app.route("/")
def index():
	update(request.remote_addr)
	return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
@app.route("/login/<page>", methods=["GET", "POST"])
def login(page = None):
	update(request.remote_addr)
	return login_page(request, page)

@app.route("/home")
def home():
	if (not has_access(request.remote_addr)):
		return redirect("/login/@2Fhome")
	update(request.remote_addr)
	return render_template("home.html")

@app.route("/create")
def create():
	if (not has_access(request.remote_addr)):
		return redirect("/login/@2Fcreate")
	update(request.remote_addr)
	return view_courses(request)

@app.route("/create/<course>/<semester>", methods = ["GET", "POST"])
def edit_survey(course, semester):
	if (not has_access(request.remote_addr)):
		return redirect("/login/@2Fcreate@2F" + course + "@2F" + semester)
	update(request.remote_addr)
	saved_questions = read_all_questions()
	return render_template("edit_survey.html", course = course, semester = semester, saved_questions = saved_questions)

@app.route("/save_question", methods=["POST"])
def save_question():
	questionText = request.form.get('question')
	options = json.loads(request.form.get('options'))
	multi = True if request.form.get('multi') == 'true' else False
	write_question(questionText, options, multi)
	return "Question saved successfully!"
