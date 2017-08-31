#Routing program
#Used to route websites.

from flask import Flask, redirect, render_template, request, url_for
from server import app
from login import login_page
from security import has_access, logout
from common import update
from create import view_courses
import json
from questionIO import *
from surveyIO import *

@app.route("/")
def index():
	update(request.remote_addr)
	return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
@app.route("/login/<page>", methods=["GET", "POST"])
def login(page = None):
	if (has_access(request.remote_addr)):
		return redirect("/home")
	update(request.remote_addr)
	
	return login_page(request, page)

@app.route("/home")
def home():
	if (not has_access(request.remote_addr)):
		return redirect("/login/@2Fhome")
	update(request.remote_addr)

	active_surveys = get_active_surveys()
	print(request.url_root)
	root = request.url_root
	return render_template("home.html", active_surveys = active_surveys, root = root)

@app.route("/create")
def create():
	if (not has_access(request.remote_addr)):
		return redirect("/login/@2Fcreate")
	update(request.remote_addr)

	return view_courses(request, get_active_surveys())

@app.route("/create/<course>/<semester>")
def edit_survey(course, semester):
	if (not has_access(request.remote_addr)):
		return redirect("/login/@2Fcreate@2F" + course + "@2F" + semester)
	update(request.remote_addr)

	saved_questions = read_all_questions()
	return render_template("edit_survey.html", course = course, semester = semester, saved_questions = saved_questions)

@app.route("/save_question", methods=["POST"])
def save_question():
	if (not has_access(request.remote_addr, overrideTime = True)):
		return redirect("/login/@2Fcreate@2F" + course + "@2F" + semester)
	update(request.remote_addr)

	write_question({'questionText': request.form.get('questionText'),
					'options': json.loads(request.form.get('options')),
					'multi': True if request.form.get('multi') == 'true' else False})
	return "Question saved successfully!"

@app.route("/delete_question", methods = ["POST"])
def delete_question():
	if (not has_access(request.remote_addr, overrideTime = True)):
		return redirect("/login/@2Fcreate@2F" + course + "@2F" + semester)
	update(request.remote_addr)

	remove_question(request.form.get('id'))
	return "Question deleted."

@app.route("/publish_survey", methods = ["POST"])
def publish_survey():
	if (not has_access(request.remote_addr, overrideTime = True)):
		return redirect("/login/@2Fcreate@2F" + course + "@2F" + semester)
	update(request.remote_addr)

	surveyData = json.loads(request.form.get('surveyData'))
	semester = request.form.get('semester')
	course = request.form.get('course')
	print(surveyData, semester, course)
	response = save_survey(course, semester, surveyData)
	return response

@app.route("/survey/<course>/<semester>", methods = ["POST", "GET"])
def view_survey(course, semester):
	update(request.remote_addr)

	if request.method == "POST":
		print(request.form)
		return "Thankyou for trying the survey system, responses are currently not being recorded."
	survey_data = get_survey(course, semester)
	if survey_data == []:
		return render_template("surveyFail.html")
	print(survey_data)
	return render_template("survey.html", survey_data = survey_data, course = course, semester = semester)

@app.route("/logout")
def logout_page():
	return logout(request.remote_addr)