from flask import Flask, redirect, render_template, request, url_for
from databasing import db_execute, db_select

class Question:
	def __init__(self, id = -1, question_text = "", multi = False, initial_options = None, mandatory = False, text = False, visible = True):
		self._id = id
		self._question_text = question_text
		self._multi = multi
		if initial_options == None:
			self._options = []
		else:
			self._options = initial_options
		self._mandatory = mandatory
		self._text = text
		self._visible = visible

	def add_option(self, option):
		self._options.append(option)

	def get_options(self):
		return [i.text for i in self._options]

	def get_visible(self):
		return self._visible

	def turn_invisible(self):
		self._visible = False

	def get_type(self):
		if self._text:
			return 'text'
		elif self._multi == True:
			return 'multi'
		else:
			return 'single'

	def get_question_text(self):
		return self._question_text

	def get_mandatory(self):
		return self._mandatory

	def get_id(self):
		return self._id

	def toggle_multi(self):
		self._multi = not self._multi

	def matches(self, other):
		if self._question_text.strip() != other._question_text.strip():
			return False
		if self._text != other._text:
			return False
		if self._multi != other._multi:
			return False
		if self._mandatory != other._mandatory:
			return False
		if len(self._options) != len(other._options):
			return False
		for i in range(len(self._options)):
			if self._options[i].text != other._options[i].text:
				return False
		return True

	def load_from_db(self, filename, id):
		result = db_select(filename, """SELECT ID, QUESTION_TEXT, TEXT, MULTI, MANDATORY, VISIBLE
							   			FROM QUESTIONS
							   			WHERE ID = """ + str(id))[0]
		self._id = int(result[0])
		self._question_text = result[1]
		self._text = True if result[2] == 1 else False
		self._multi = True if result[3] == 1 else False
		self._mandatory = True if result[4] == 1 else False
		self._visible = True if result[5] == 1 else False
		options = []
		if (not self._text):
			options = db_select(filename, """SELECT OPTION
											 FROM OPTIONS
											 WHERE QUESTIONID = """ + str(id) +
											 " ORDER BY ID")
		for option in range(len(options)):
			self._options.append(Option(option, options[option][0]))

	def load_from_dict(self, data):
		if 'questionNum' in data:
			self._id = int(data['questionNum'])
		self._question_text = data['questionText'].strip()
		self._question_text = self._question_text.replace('&lt;', '<')
		self._question_text = self._question_text.replace('&gt;', '>')
		self._question_text = self._question_text.replace('&amp;', '&')

		self._multi = data['multi']
		if self._multi == 'false':
			self._multi = False
		if self._multi == 'true':
			self._multi = True

		for i, text in enumerate(data['options']):
			text = text.replace('&lt;', '<')
			text = text.replace('&gt;', '>')
			text = text.replace('&amp;', '&')
			option = Option(i, text)
			self._options.append(option)

		self._text = data['text']
		if self._text == 'false':
			self._text = False
		if self._text == 'true':
			self._text = True

		self._mandatory = data['mandatory']
		if self._mandatory == 'false':
			self._mandatory = False
		if self._mandatory == 'true':
			self._mandatory = True

	def write_to_db(self, filename):
		question_ids = [i[0] for i in db_select(filename, "SELECT ID FROM QUESTIONS")]
		if question_ids == []:
			max_question_id = 0
		else:
			max_question_id = max(question_ids)
		db_execute(filename, """INSERT INTO QUESTIONS (ID, QUESTION_TEXT, TEXT, MULTI, MANDATORY, VISIBLE)
								VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}")
								""".format(str(max_question_id + 1), self._question_text, 1 if self._text else 0,
										   1 if self._multi else 0, 1 if self._mandatory else 0, 1 if self._visible else 0))

		option_ids = [i[0] for i in db_select(filename, "SELECT ID FROM OPTIONS")]
		if option_ids == []:
			max_option_id = 0
		else:
			max_option_id = max(option_ids)
		for i, option in enumerate(self._options):
			db_execute(filename, 'INSERT INTO OPTIONS (ID, OPTION, QUESTIONID) VALUES ("{0}", "{1}", "{2}")'.format(
								 str(i+max_option_id+1), option.text, str(max_question_id + 1))
					  )
		
		return max_question_id + 1

	def update_db(self, filename, id):
		db_execute(filename, """UPDATE QUESTIONS
								SET QUESTION_TEXT = "{0}", TEXT = "{1}", MULTI = "{2}", MANDATORY = "{3}", VISIBLE = "{4}"
								WHERE ID = {5}""".format(self._question_text, 1 if self._text else 0, 1 if self._multi else 0,
									                     1 if self._mandatory else 0, 1 if self._visible else 0, str(id)))
		current_options = db_select(filename, "SELECT ID, OPTION FROM OPTIONS WHERE QUESTIONID = " + str(id) + " ORDER BY ID")
		if len(current_options) < len(self._options):
			option_ids = [i[0] for i in db_select(filename, "SELECT ID FROM OPTIONS")]
			if option_ids == []:
				max_option_id = 0
			else:
				max_option_id = max(option_ids)

		for option in range(len(self._options)):
			if option < len(current_options):
				if current_options[option][1] != self._options[option].text:
					db_execute(filename, """UPDATE OPTIONS
											SET OPTION = "{0}"
											WHERE ID = {1}""".format(self._options[option].text, current_options[option][0]))
			else:
				db_execute(filename, 'INSERT INTO OPTIONS (ID, OPTION, QUESTIONID) VALUES ("{0}", "{1}", "{2}")'.format(
								 	  str(option - len(current_options) + max_option_id + 1), self._options[option].text, str(id)))

		for i in range(len(self._options), len(current_options)):
			db_execute(filename, """DELETE FROM OPTIONS
									WHERE ID = {0}""".format(current_options[i][0]))

		return id;

	def __str__(self):
		string = 'Question' + str(self._id) + ' multi=' + str(self._multi) + ' ' + self._question_text + '\n'
		string += 'mandatory=' + str(self._mandatory) + ' text=' + str(self._text) + '\n'
		for i, option in enumerate(self._options):
			string += 'Q' + str(self._id) + 'O' + str(i+1) + ' ' + option.text + '\n'
		return string

class Option:
	def __init__(self, id = -1, text = ""):
		self._id = id
		self._text = text
	def _get_id(self):
		return self._id
	def _set_id(self, id):
		self._id = id
	def _get_text(self):
		return self._text
	def _set_text(self, text):
		self._text = text

	id = property(_get_id, _set_id)
	text = property(_get_text, _set_text)