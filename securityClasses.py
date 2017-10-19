import time
from databasing import db_select, db_execute

class User:
	#zID, Password, Login Function

	#Private Functions
	def __init__(self, zID = -1, password = None):
		self._zID = zID
		self._password = password
		self._last_activity = -1
	def _get_zID(self):
		return self._zID
	def _set_zID(self, zID):
		self._zID = zID
	def _get_password(self):
		return self._password
	def _set_password(self, password):
		self._password = password
	def _get_last_activity(self):
		return self._last_activity
	def _set_last_activity(self, last_activity):
		self._last_activity = last_activity

	zID = property(_get_zID, _set_zID)
	password = property(_get_password, _set_password)
	last_activity = property(_get_last_activity, _set_last_activity)

	#Public Functions
	def login(self, zID_attempt, password_attempt):
		if zID_attempt == self._zID and password_attempt == self._password:
			self._last_activity = time.time()
			return True
		return False

class Student(User):
	#Private Functions
	def __init__(self, zID, password, enrolled_courses = []):
		super().__init__(zID = zID, password = password)
		self._enrolled_courses = enrolled_courses

	#Public Functions
	def enrol(self, course):
		self._enrolled_courses.append(course)

	def unenrol(self, course):
		for c in range(len(self._enrolled_courses)):
			if self._enrolled_courses[c].matches(course.name, course.semester):
				self._enrolled_courses.pop(c)
				break

	def is_enrolled_in(self, course):
		for enrolled_course in self._enrolled_courses:
			if enrolled_course.matches(course.name, course.semester):
				return True
		return False

	def has_responded_to(self, filename, survey):
		result = db_select(filename, """SELECT ID FROM RESPONSES WHERE ZID = {0} AND SURVEYID = {1}""".format(self._zID, survey.id))
		if len(result) > 0:
			return True
		return False

class Staff(User):
	#Private functions
	def __init__(self, zID, password, enrolled_courses = []):
		super().__init__(zID = zID, password = password)
		self._enrolled_courses = enrolled_courses

	#Public Functions
	def enrol(self, course):
		self._enrolled_courses.append(course)

	def unenrol(self, course):
		for c in range(len(self._enrolled_courses)):
			if self._enrolled_courses[c] == course:
				self._enrolled_courses.pop(c)

	def is_enrolled_in(self, course):
		for enrolled_course in self._enrolled_courses:
			if enrolled_course.matches(course.name, course.semester):
				return True
		return False


class Admin(User):
	#Private functions
	def __init__(self, zID, password):
		super().__init__(zID = zID, password = password)