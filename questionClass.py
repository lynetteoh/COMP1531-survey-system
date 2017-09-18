from questionIO import *
from flask import Flask, redirect, render_template, request, url_for
from databasing import db_execute, db_select

class Question:
	def __init__(self, id = -1, question_text = "", multi = False, initial_options = None, mandatory = False, text = False):
		self._id = id
		self._question_text = question_text
		self._multi = multi
		if initial_options == None:
			self._options = []
		else:
			self._options = initial_options
		self._mandatory = mandatory
		self._text = text

	def add_option(self, option):
		self._options.append(option)

	def get_options(self):
		return [i.text for i in self._options]

	def get_type(self):
		if self._text:
			return 'text'
		elif self._multi:
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

	def load_from_db(self, filename, id):
		result = db_select(filename, """SELECT ID, QUESTION_TEXT, TEXT, OPTIONS, OPTIONSTART, MULTI, MANDATORY
							   FROM QUESTIONS
							   WHERE ID = """ + str(id))[0]
		self._id = result[0]
		self._question_text = result[1]
		self._text = True if result[2] == 1 else False
		self._multi = True if result[5] == 1 else False
		self._mandatory = True if result[6] == 1 else False
		options = []
		if (type(result[4]) == int):
			options = db_select(filename, """SELECT OPTION
											 FROM OPTIONS
											 WHERE ID >= """ + str(result[4]) + " AND ID < " + str(result[4] + result[3]))
		for option in range(len(options)):
			self._options.append(Option(option, options[option][0]))

	def load_from_dict(self, data):
		print(data)
		if 'questionNum' in data:
			self._id = data['questionNum']
		self._question_text = data['questionText']
		self._question_text = self._question_text.replace('&lt;', '<')
		self._question_text = self._question_text.replace('&gt;', '>')
		self._question_text = self._question_text.replace('&amp;', '&')

		self._multi = data['multi']
		for i, text in enumerate(data['options']):
			text = text.replace('&lt;', '<')
			text = text.replace('&gt;', '>')
			text = text.replace('&amp;', '&')
			option = Option(i, text)
			self._options.append(option)
		self._text = data['text']
		self._mandatory = data['mandatory']

	def write_to_db(self, filename):
		max_option_id = max([i[0] for i in db_select(filename, "SELECT ID FROM OPTIONS")])
		for i, option in enumerate(self._options):
			print(i, option, max_option_id)
			db_execute(filename, "INSERT INTO OPTIONS (ID, OPTION) VALUES ('{0}', '{1}')".format(str(i+max_option_id+1), option))
		max_question_id = max([i[0] for i in db_select(filename, "SELECT ID FROM QUESTIONS")])
		db_execute(filename, """INSERT INTO QUESTIONS (ID, QUESTION_TEXT, TEXT, OPTIONS, OPTIONSTART, MULTI, MANDATORY) 
								VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')
								""".format(str(max_question_id + 1), self._question_text, 1 if self._text else 0,
										   str(len(self._options)), str(max_option_id + 1), 1 if self._multi else 0, 1 if self._mandatory else 0))
		return max_question_id + 1

	def __str__(self):
		string = 'Question' + str(self._id) + ' multi=' + str(self._multi) + ' ' + self._question_text + '\n'
		string += 'mandatory=' + str(self._mandatory) + ' text=' + str(self._text) + '\n'
		for i, option in enumerate(self._options):
			print(option.text)
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