import unittest
from questionClass import Question, Option
from securityClasses import Admin, Staff, Student
from security import has_access, login_user, get_user, logout
import json
from surveyClass import Survey
import datetime
from databasing import db_select, db_execute
from courses import find_course

DATABASE_FILENAME = "data.db"

class test_question(unittest.TestCase):
	def set_up(self):
		pass

	def test_values_read_from_dictionary(self):
		
		question = Question()

		data = {
			'questionNum': 20,
			'questionText': 'Example text',
			'multi': 'false',
			'options': ['yes', 'no'],
			'text': 'false',
			'mandatory': 'true'
		}

		question.load_from_dict(data)

		self.assertEqual(question.get_id(), 20)
		self.assertEqual(question.get_question_text(), 'Example text')
		self.assertEqual(question.get_type(), 'single')
		self.assertEqual(question.get_mandatory(), True)
		self.assertEqual(question.get_options()[0], 'yes')

	def test_visibility_toggle(self):
		question = Question()

		data = {
			'questionNum': 20,
			'questionText': 'Example text',
			'multi': 'false',
			'options': ['yes', 'no'],
			'text': 'false',
			'mandatory': 'true'
		}

		question.load_from_dict(data)
		

		self.assertEqual(question.get_visible(), True) #Any question loaded from dictionary is visible
		question.turn_invisible()
		self.assertEqual(question.get_visible(), False)

	def test_create_question(self):
		
		question = Question()

		data = {
			'questionText': 'Example text',
			'multi': 'false',
			'options': ['yes', 'no'],
			'text': 'false',
			'mandatory': 'true'
		}

		question.load_from_dict(data)

		write_id = question.write_to_db(DATABASE_FILENAME)

		question = None

		question = Question()
		question.load_from_db(DATABASE_FILENAME, write_id)

		self.assertEqual(question.get_id(), write_id)
		self.assertEqual(question.get_question_text(), 'Example text')
		self.assertEqual(question.get_type(), 'single')
		self.assertEqual(question.get_mandatory(), True)
		self.assertEqual(question.get_options()[0], 'yes')

	def test_create_mandatory_question(self):
		question = Question()

		data = {
			'questionText': 'Example text',
			'multi': 'false',
			'options': ['yes', 'no'],
			'text': 'false',
			'mandatory': 'true'
		}

		question.load_from_dict(data)

		write_id = question.write_to_db(DATABASE_FILENAME)

		question = None

		question = Question()
		question.load_from_db(DATABASE_FILENAME, write_id)

		self.assertEqual(question.get_mandatory(), True)


	def test_create_optional_question(self):
		question = Question()

		data = {
			'questionText': 'Example text',
			'multi': 'false',
			'options': ['yes', 'no'],
			'text': 'false',
			'mandatory': 'false'
		}

		question.load_from_dict(data)

		write_id = question.write_to_db(DATABASE_FILENAME)

		question = None

		question = Question()
		question.load_from_db(DATABASE_FILENAME, write_id)

		self.assertEqual(question.get_mandatory(), False)

	

class test_login(unittest.TestCase):

	def set_up(self):
		pass

	def test_admin_login(self):
		user = login_user('z1', 'adminPass', 'localhost')
		self.assertNotEqual(user, None)
		self.assertEqual(type(user), Admin)

		self.assertEqual(user, get_user('localhost'))

		self.assertEqual(has_access('localhost', Admin), True)


	def test_admin_logout(self):

		logout('localhost')

		self.assertEqual(get_user('localhost'), None)
		self.assertEqual(has_access('localhost', Admin), False)

	def test_admin_incorrect_login(self):
		user = login_user('z10', 'adminPass', 'localhost')
		self.assertEqual(user, None)
		self.assertEqual(has_access('localhost', Admin), False)


	def test_staff_login(self):
		user = login_user('z50', 'staff670', 'localhost')
		self.assertNotEqual(user, None)
		self.assertEqual(type(user), Staff)

		self.assertEqual(user, get_user('localhost'))

		self.assertEqual(has_access('localhost', Staff), True)

	def test_staff_logout(self):
		logout('localhost')

		self.assertEqual(get_user('localhost'), None)
		self.assertEqual(has_access('localhost', Staff), False)

	def test_staff_incorrect_login(self):
		user = login_user('z10', 'adminPass', 'localhost')
		self.assertEqual(user, None)
		self.assertEqual(has_access('localhost', Admin), False)


	def test_student_login(self):
		user = login_user('z100', 'student228', 'localhost')
		self.assertNotEqual(user, None)
		self.assertEqual(type(user), Student)

		self.assertEqual(user, get_user('localhost'))

		self.assertEqual(has_access('localhost', Student), True)

	def test_student_logout(self):
		logout('localhost')

		self.assertEqual(get_user('localhost'), None)
		self.assertEqual(has_access('localhost', Student), False)
		
	def test_staff_incorrect_login(self):
		user = login_user('z10', 'adminPass', 'localhost')
		self.assertEqual(user, None)
		self.assertEqual(has_access('localhost', Admin), False)

class test_survey(unittest.TestCase):
	def set_up(self):
		pass

	def test_add_question_survey(self):
		survey = Survey()

		data = {
			'course': 'COMP1531',
			'semester': '17s2',
			'start': '2017-10-25',
			'end': '2017-10-26',
			'surveyData': json.dumps([
				{
					'questionNum': -1,
					'questionText': 'Example text',
					'multi': 'false',
					'options': ['yes', 'no'],
					'text': 'false',
					'mandatory': 'true'
				},
				{
					'questionNum': -1,
					'questionText': 'Example text 2',
					'multi': 'false',
					'options': ['yes', 'no'],
					'text': 'false',
					'mandatory': 'true'
				}
			])
		}

		survey.load_from_dict(data)
		

		self.assertEqual(survey.course.name, 'COMP1531')
		self.assertEqual(survey.course.semester, '17s2')
		self.assertEqual(survey.start, datetime.date(2017,10,25))
		self.assertEqual(survey.questions[0].get_question_text(), 'Example text')

	def test_save_survey(self):
		survey = Survey()

		data = {
			'course': 'COMP1531',
			'semester': '17s2',
			'start': '2017-10-25',
			'end': '2017-10-26',
			'surveyData': json.dumps([
				{
					'questionNum': -1,
					'questionText': 'Example text',
					'multi': 'false',
					'options': ['yes', 'no'],
					'text': 'false',
					'mandatory': 'true'
				},
				{
					'questionNum': -1,
					'questionText': 'Example text 2',
					'multi': 'false',
					'options': ['yes', 'no'],
					'text': 'false',
					'mandatory': 'true'
				}
			])
		}

		survey.load_from_dict(data)
		survey_id = survey.write_to_db(DATABASE_FILENAME)

		survey = None
		survey = Survey()
		survey = survey.load_from_db(DATABASE_FILENAME, survey_id)

		self.assertEqual(survey.course.name, 'COMP1531')
		self.assertEqual(survey.course.semester, '17s2')
		self.assertEqual(survey.start, '2017-10-25')
		self.assertEqual(survey.questions[0].get_question_text(), 'Example text')


class enrol_student(unittest.TestCase):
	def set_up(self):
		pass
	
	def test_enrol_student(self):
		user = login_user('z100', 'student228', 'localhost')
		course = find_course('COMP1531', '17s2')
		user.enrol(course)

		self.assertEqual(user.is_enrolled_in(course), True)


	def test_update_enrollment(self):
		user = login_user('z100', 'student228', 'localhost')
		course = find_course('COMP1531', '17s2')
		user.unenrol(course)

		self.assertEqual(user.is_enrolled_in(course), False)

	def test_fail_enrollment(self):
		user = login_user('z100', 'student228', 'localhost')
		course = find_course('COMP15610', '17s2')
		user.enrol(course)

		self.assertEqual(course, None)
		self.assertEqual(user.is_enrolled_in(course), False)

class test_update_question(unittest.TestCase):
	def set_up():
		pass

	def test_add_option(self):

		question = Question()

		data = {
			'questionText': 'Example text',
			'multi': 'false',
			'options': ['yes', 'no'],
			'text': 'false',
			'mandatory': 'false'
		}

		question.load_from_dict(data)


		self.assertEqual(question.get_options().count('maybe'), 0)
		question.add_option(Option(id = -1, text = 'maybe'))
		self.assertEqual(question.get_options().count('maybe'), 1)
	
	def test_turn_invisible(self):

		question = Question()

		data = {
			'questionText': 'Example text',
			'multi': 'false',
			'options': ['yes', 'no'],
			'text': 'false',
			'mandatory': 'false'
		}

		question.load_from_dict(data)


		self.assertEqual(question.get_visible(), True)
		question.turn_invisible()
		self.assertEqual(question.get_visible(), False)


	def test_edit_question(self):
		question = Question()

		data = {
			'questionText': 'Example text',
			'multi': 'false',
			'options': ['yes', 'no'],
			'text': 'false',
			'mandatory': 'false'
		}

		question.load_from_dict(data)

		write_id = question.write_to_db(DATABASE_FILENAME)

		question = None

		question = Question()

		data = {
			'questionNum': write_id,
			'questionText': 'Example other text',
			'multi': 'false',
			'options': ['yes', 'no'],
			'text': 'false',
			'mandatory': 'false'
		}

		question.load_from_dict(data)
		question.update_db(DATABASE_FILENAME, write_id)

		question = None

		question = Question()

		question.load_from_db(DATABASE_FILENAME, write_id)

		self.assertNotEqual(question.get_question_text(), 'Example text')
		self.assertEqual(question.get_question_text(), 'Example other text')

	def test_edit_question_type(self):
		question = Question()

		data = {
			'questionText': 'Example text',
			'multi': 'false',
			'options': ['yes', 'no'],
			'text': 'false',
			'mandatory': 'false'
		}

		question.load_from_dict(data)


		self.assertEqual(question.get_type(), 'single')
		question.toggle_multi()
		self.assertEqual(question.get_type(), 'multi')
		question.toggle_multi()
		self.assertEqual(question.get_type(), 'single')






		
		
		




	
	



if __name__=="__main__":
    unittest.main()