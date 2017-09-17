class Course:
	#Private Functions
	def __init__(self, name, semester, survey = None):
		self._name = name
		self._semester = semester
		self._survey = survey

	def _get_name(self):
		return self._name
	def _set_name(self, name):
		self._name = name
	def _get_semester(self):
		return self._semester
	def _set_semester(self, semester):
		self._semester = semester
	def _get_survey(self):
		return self._survey
	def _set_survey(self, survey):
		self._survey = survey

	name = property(_get_name, _set_name)
	semester = property(_get_semester, _set_semester)
	survey = property(_get_survey, _set_survey)

	def matches(self, name, semester):
		if self._name == name and self._semester == semester:
			return True
		return False