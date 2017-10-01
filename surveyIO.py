from questionClass import Question, Option
from surveyClass import Survey
from databasing import db_select
from flask import request

SURVEY_FILENAME = "data.db"

def save_survey(survey_data):
	print("!!!")
	if (get_survey(survey_data['course'], survey_data['semester']) != None):
		return 'Survey for that semester already exists'

	survey = Survey()
	survey.load_from_dict(survey_data)
	survey.write_to_db(SURVEY_FILENAME)

	return 'Success'

def get_survey(course, semester):
	survey = Survey()
	survey = survey.load_course_from_db(SURVEY_FILENAME, course, semester)
	return survey

def get_surveys(state = None):
	if state != None:
		ids = [i[0] for i in db_select(SURVEY_FILENAME, "SELECT ID FROM SURVEYS WHERE STATE = " + str(state))]
	else:
		ids = [i[0] for i in db_select(SURVEY_FILENAME, "SELECT ID FROM SURVEYS")]
	surveys = []
	for id in ids:
		survey = Survey()
		survey.load_from_db(SURVEY_FILENAME, id)
		surveys.append(survey)
	return surveys