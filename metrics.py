from databasing import db_execute, db_select

DATABASE_FILENAME = "data.db"

def get_all_survey_responses(survey):
	survey_responses = {}
	for question in survey.questions:
		survey_responses[question.get_id()] = get_all_question_responses(survey, question)

	return survey_responses

def get_all_question_responses(survey, question):
	result = db_select(DATABASE_FILENAME, """SELECT RESPONSE
					   FROM RESPONSES
					   WHERE QUESTIONID = {0} AND SURVEYID = {1}""".format(
					   question.get_id(), survey.id))
	responses = []
	for item in result:
		responses.append(item[0])

	return responses
