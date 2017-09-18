from questionClass import Question, Option
from databasing import db_execute, db_select

QUESTIONS_FILENAME = "questions.db"

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
	file = open(QUESTIONS_FILENAME, 'r')
	lines = file.readlines()
	file.close()

	file = open(QUESTIONS_FILENAME, 'w')

	for line in lines:
		if not (line.startswith('Question'+str(id)) or line.startswith('Q' + str(id) + 'O')):
			file.write(line)

	file.close()

#writes question from a form to the questions file
def write_question(form):
	question = Question()
	question.load_from_dict(form)
	return question.write_to_db(QUESTIONS_FILENAME)