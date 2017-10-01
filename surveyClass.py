from questionClass import Question
from databasing import db_execute, db_select
from courses import find_course
import json
import datetime

class Survey:
	def __init__(self, start = '', end = '', state = 0, course = None, questions = None):
		self._id = -1
		self._start = start
		self._end = end
		self._state = state
		self._course = course
		if (questions == None):
			self._questions = []
		else:
			self._questions = questions

	#Property functions
	def _get_start(self):
		return self._start
	def _set_start(self, start):
		self._start = start
	def _get_end(self):
		return self._end
	def _set_end(self, end):
		self._end = end
	def _get_state(self):
		return self._state
	def _set_state(self, state):
		self._state = state
	def _get_course(self):
		return self._course
	def _set_course(self, course):
		self._course = course
	def _get_questions(self):
		return self._questions
	def _set_questions(self, questions):
		self._questions = questions
	def _get_id(self):
		return self._id
	def _set_id(self, id):
		self._id = id

	start = property(_get_start, _set_start)
	end = property(_get_end, _set_end)
	state = property(_get_state, _set_state)
	course = property(_get_course, _set_course)
	questions = property(_get_questions, _set_questions)
	id = property(_get_id, _set_id)

	#Public functions
	def load_from_db(self, filename, id):
		result = db_select(filename, """SELECT ID, START, END, COURSE, SEMESTER, STATE
										FROM SURVEYS
										WHERE ID = """ + str(id))[0]
		if not result:
			return None

		self._id = result[0]
		self._start = result[1]
		self._end = result[2]
		self._course = find_course(result[3], result[4])
		self._course.survey = self
		self._questions = []
		qids = [x[0] for x in db_select(filename, """SELECT QUESTIONID FROM INCLUDE WHERE SURVEYID = """ + str(id))]
		for qid in qids:
			newQuestion = Question()
			newQuestion.load_from_db(filename, qid)
			self._questions.append(newQuestion)

		return self

	def load_course_from_db(self, filename, name, semester):
		result = db_select(filename, """SELECT ID
										FROM SURVEYS
										WHERE COURSE = "{0}" AND SEMESTER = "{1}" """.format(name, semester))
		if result:
			self.load_from_db(filename, result[0][0])
			return self
		else:
			return None

	def load_from_dict(self, data):
		self._course = find_course(data['course'], data['semester'])
		self._course.survey = self

		startData = data['start'].split('-')
		self._start = datetime.date(int(startData[0]), int(startData[1]), int(startData[2]))
		endData = data['end'].split('-')
		self._end = datetime.date(int(endData[0]), int(endData[1]), int(endData[2]))

		self._questions = []
		for question in json.loads(data['surveyData']):
			newQuestion = Question()
			newQuestion.load_from_dict(question)
			self._questions.append(newQuestion)

	def write_to_db(self, filename):
		existing_questions = []
		for qid in [x[0] for x in db_select(filename, "SELECT ID FROM QUESTIONS")]:
			question = Question()
			question.load_from_db(filename, qid)
			existing_questions.append(question)

		survey_ids = [i[0] for i in db_select(filename, "SELECT ID FROM SURVEYS")]
		if survey_ids == []:
			max_survey_id = 0
		else:
			max_survey_id = max(survey_ids)
		db_execute(filename, """INSERT INTO SURVEYS (ID, START, END, COURSE, SEMESTER, STATE) 
								VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}")
								""".format(str(max_survey_id + 1), str(self._start), str(self._end), self._course.name, self._course.semester,
										   str(self._state)))

		for question in self._questions:
			exists = False
			for existing_question in existing_questions:
				if not exists and question.matches(existing_question):
					db_execute(filename, """INSERT INTO INCLUDE (SURVEYID, QUESTIONID)
											VALUES ("{0}", "{1}")""".format(str(max_survey_id + 1), str(existing_question.get_id())))
					exists = True
			if not exists:
				write_id = question.write_to_db(filename)
				db_execute(filename, """INSERT INTO INCLUDE (SURVEYID, QUESTIONID)
										VALUES ("{0}", "{1}")""".format(str(max_survey_id + 1), str(write_id)))
		
		return max_survey_id+1

	def update_db(self, filename):
		storedIds = [x[0] for x in db_select(filename, "SELECT QUESTIONID FROM INCLUDE WHERE SURVEYID = " + str(self._id))]
		for i in range(min(len(storedIds), len(self._questions))):
			if storedIds[i] != self._questions[i].get_id():
				db_execute(filename, 'UPDATE INCLUDE SET QUESTIONID = "{0}" WHERE QUESTIONID = {1} AND SURVEYID = {2}'.format(
									  self._questions[i].get_id(), storedIds[i], self._id))

		for i in range(len(storedIds), len(self._questions)):
			db_execute(filename, 'INSERT INTO INCLUDE (SURVEYID, QUESTIONID) VALUES ("{0}", "{1}")'.format(self._id, self._questions[i].get_id()))

		for i in range(len(self._questions), len(storedIds)):
			db_execute(filename, 'DELETE FROM INCLUDE WHERE SURVEYID = {0} AND QUESTIONID = {1}'.format(self._id, storedIds[i]))