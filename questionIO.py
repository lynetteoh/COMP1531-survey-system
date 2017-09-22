from questionClass import Question, Option
from databasing import db_execute, db_select

QUESTIONS_FILENAME = "data.db"

#Significantly faster than looping over all ID's.
def read_all_questions():
	question_list = []
	for questionID in [i[0] for i in db_select(QUESTIONS_FILENAME, "SELECT ID FROM QUESTIONS")]:
		question = Question()
		question.load_from_db(QUESTIONS_FILENAME, questionID)
		print(question)
		question_list.append(question)
	return question_list

#removes a question with that id
###DEPRECATED FUNCTION
def remove_question(id):
	question = Question()
	question.load_from_db(QUESTIONS_FILENAME)
	question.turn_invisible()
	question.update_db(QUESTIONS_FILENAME)

#writes question from a form to the questions file
def write_question(form):
	question = Question()
	question.load_from_dict(form)
	if int(form['saved_id']) != -1:
		return question.update_db(QUESTIONS_FILENAME, int(form['saved_id']))
	else:
		return question.write_to_db(QUESTIONS_FILENAME)