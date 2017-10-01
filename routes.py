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
from save_response import save_response
from securityClasses import Admin, Staff, Student

DATABASE_FILENAME = "data.db"

@app.route("/")
def index():
	update(request.remote_addr)
	return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
@app.route("/login/<page>", methods=["GET", "POST"])
def login(page = None):
	if (has_access(request.remote_addr, Admin)):
		return redirect("/adminHome")
	if (has_access(request.remote_addr, Student)):
		return redirect("/studentHome")
	if (has_access(request.remote_addr, Staff)):
		return redirect("/staffHome")
	update(request.remote_addr)
	
	return login_page(request, page)

@app.route("/adminHome")
def home():
	if (not has_access(request.remote_addr, Admin)):
		return redirect("/login/@2FadminHome")
	update(request.remote_addr)

	review_surveys = get_surveys(state = 0)
	active_surveys = get_surveys(state = 1)
	closed_surveys = get_surveys(state = 2)
	print(request.url_root)
	root = request.url_root
	return render_template("home.html", review_surveys = review_surveys, active_surveys = active_surveys,
		                                closed_surveys = closed_surveys, root = root)

@app.route("/studentHome")
def studentHome():
	if (not has_access(request.remote_addr, Student)):
		return redirect("/login/@2FstudentHome")
	update(request.remote_addr)
	return render_template("studentHome.html")

@app.route("/create")
def create():
	if (not has_access(request.remote_addr, Admin)):
		return redirect("/login/@2Fcreate")
	update(request.remote_addr)

	return view_courses(request, get_surveys())

@app.route("/review_questions")
def review_saved_questions():
	if (not has_access(request.remote_addr, Admin)):
		return redirect("/login/@2Freview_questions")
	update(request.remote_addr)

	saved_questions = read_all_questions()
	return render_template("viewQuestions.html", saved_questions = saved_questions)


@app.route("/create/<course>/<semester>")
def edit_survey(course, semester):
	if (not has_access(request.remote_addr, Admin)):
		return redirect("/login/@2Fcreate@2F" + course + "@2F" + semester)
	update(request.remote_addr)

	saved_questions = read_all_questions()
	return render_template("edit_survey.html", course = course, semester = semester, saved_questions = saved_questions)

@app.route("/save_question", methods=["POST"])
def save_question():
	if (not has_access(request.remote_addr, Admin, overrideTime = True)):
		return redirect("/login/@2Fcreate")
	update(request.remote_addr)

	write_question({'questionText': request.form.get('questionText'),
					'options': json.loads(request.form.get('options')),
					'multi': request.form.get('multi'),
					'text': request.form.get('text'),
					'mandatory': request.form.get('mandatory'),
					'saved_id': request.form.get('saved_id')})
	return "Question saved successfully!"

@app.route("/delete_question", methods = ["POST"])
def delete_question():
	if (not has_access(request.remote_addr, Admin, overrideTime = True)):
		return redirect("/login/@2Fcreate@2F" + course + "@2F" + semester)
	update(request.remote_addr)

	remove_question(request.form.get('id'))
	return "Question deleted."

@app.route("/publish_survey", methods = ["POST"])
def publish_survey():
	if (not has_access(request.remote_addr, Admin, overrideTime = True)):
		return redirect("/login/@2Fcreate@2F" + request.form['course'] + "@2F" + request.form['semester'])
	update(request.remote_addr)
	response = save_survey(request.form)
	return response

@app.route("/staffHome")
def staffHome():
	if (not has_access(request.remote_addr, Staff)):
		return redirect("/login/@2FstaffHome")
	update(request.remote_addr)

	review_surveys = get_surveys(state = 0)
	active_surveys = get_surveys(state = 1)
	closed_surveys = get_surveys(state = 2)
	print(request.url_root)
	root = request.url_root
	return render_template("staffHome.html", review_surveys = review_surveys, active_surveys = active_surveys,
		                                	 closed_surveys = closed_surveys, root = root)

@app.route("/open_survey/<course>/<semester>")
def openSurvey(course, semester):
	if (not has_access(request.remote_addr, Staff)):
		return redirect("/login/@open_survey@2F" + course + "@2F" + semester)
	update(request.remote_addr)

	survey = Survey()
	survey.load_course_from_db(DATABASE_FILENAME, course, semester)
	db_execute(DATABASE_FILENAME, 'UPDATE SURVEYS SET STATE = "1" WHERE ID = ' + str(survey.id))
	return redirect('/staffHome')

@app.route("/review/<course>/<semester>")
def reviewSurvey(course, semester):
	if (not has_access(request.remote_addr, Staff)):
		return redirect("/login/@2Freview@2F" + course + "@2F" + semester)
	update(request.remote_addr)

	survey = get_survey(course, semester)
	num_questions = len(survey.questions)
	all_questions = read_all_questions()
	extra_questions = []
	for question in all_questions:
		matches = False
		for survey_question in survey.questions:
			if question.matches(survey_question):
				matches = True
				break
		if not matches and question.get_visible() and not question.get_mandatory():
			extra_questions.append(question)
	print(extra_questions)
	num_extra_questions = len(extra_questions)

	return render_template("reviewSurvey.html", survey = survey, num_questions = num_questions,
												extra_questions = extra_questions, num_extra_questions = num_extra_questions)

@app.route("/commit_review", methods = ["POST"])
def commit_review():
	if (not has_access(request.remote_addr, Staff, overrideTime = True)):
		return redirect("/login/@2Fcommit_review")
	update(request.remote_addr)

	print(request.form)

	survey = Survey()
	survey.load_course_from_db(DATABASE_FILENAME, request.form.get('course'), request.form.get('semester'))
	survey.questions = []

	for questionId in json.loads(request.form.get('ids')):
		question = Question()
		question.load_from_db(DATABASE_FILENAME, questionId)
		survey.questions.append(question)

	survey.update_db(DATABASE_FILENAME)

	return "Success"

@app.route("/survey/<course>/<semester>", methods = ["POST", "GET"])
def view_survey(course, semester):
	update(request.remote_addr)

	if request.method == "POST":
		print(request.form)
		return save_response(course, semester, request.form)

	survey = Survey()
	survey = survey.load_course_from_db(DATABASE_FILENAME, course, semester)
	numQuestions = len(survey.questions)

	if survey == None:
		return render_template("surveyFail.html")
	return render_template("survey.html", survey = survey, numQuestions = numQuestions)

@app.route("/logout")
def logout_page():
	return logout(request.remote_addr)