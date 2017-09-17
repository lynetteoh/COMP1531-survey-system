class User:
	#zID, Password, Login Function

	#Private Functions
	def __init__(self, zID = -1, password = None):
		self._zID = zID
		self._password = password
	def _get_zID(self):
		return self._zID
	def _set_zID(self, zID):
		self._zID = zID
	def _get_password(self):
		return self._password
	def _set_password(self, password):
		self._password = password

	zID = property(_get_zID, _set_zID)
	password = property(_get_password, _set_password)

	#Public Functions
	def login(self, zID_attempt, password_attempt):
		if zID_attempt == self._zID and password_attempt == self._password:
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
			if self._enrolled_courses[c] == course:
				self._enrolled_courses.pop(c)

class Staff(User):
	#Private functions
	def __init__(self, zID, password):
		super().__init__(zID = zID, password = password)

class Admin(User):
	#Private functions
	def __init__(self, zID, password):
		super().__init__(zID = zID, password = password)