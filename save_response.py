from flask import Flask, request, redirect
from databasing import db_select, db_execute
from security import get_user

def save_response(filename, survey, request):
	user = get_user(request.remote_addr)
	print(":", request.form)
	print("USER:", user.zID)
	try:
		write_id = max([int(x[0]) for x in db_select(filename, "SELECT ID FROM RESPONSES")]) + 1
	except ValueError:
		write_id = 1
	for question in survey.questions:
		if question.get_type() == 'text':
			response = request.form.get('TextBox' + str(question.get_id()))
			print("Question, id =", question.get_id(), "Text,  Value:", response)
			db_execute(filename, """INSERT INTO RESPONSES (ID, ZID, RESPONSE, QUESTIONID, SURVEYID)
											 VALUES ("{0}", "{1}", "{2}", "{3}", "{4}")""".format(
											 write_id, user.zID, response, question.get_id(), survey.id)
					   )
			write_id += 1
		elif question.get_type() == 'single':
			response = request.form.get('Q' + str(question.get_id()))
			print("Question, id =", question.get_id(), "Single,  Value:", response)
			db_execute(filename, """INSERT INTO RESPONSES (ID, ZID, RESPONSE, QUESTIONID, SURVEYID)
											 VALUES ("{0}", "{1}", "{2}", "{3}", "{4}")""".format(
											 write_id, user.zID, response, question.get_id(), survey.id)
					   )
			write_id += 1
		else:
			print("Question, id =", question.get_id(), "Multi,  Value:", request.form.getlist('Q' + str(question.get_id())))
			for response in request.form.getlist('Q' + str(question.get_id())):
				db_execute(filename, """INSERT INTO RESPONSES (ID, ZID, RESPONSE, QUESTIONID, SURVEYID)
											 VALUES ("{0}", "{1}", "{2}", "{3}", "{4}")""".format(
											 write_id, user.zID, response, question.get_id(), survey.id)
					   )
				write_id += 1
	return redirect('/login')