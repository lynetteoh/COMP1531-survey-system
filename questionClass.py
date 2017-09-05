from questionIO import *
from flask import Flask, redirect, render_template, request, url_for

class Question:
	def __init__(self, id = -1, text = "", multi = False, options = None):
		self.id = id
		self.text = text
		self.multi = multi
		if options == None:
			self.options = []
		else:
			self.options = options

	def add_option(self, option):
		self.options.append(option)

	def toggle_multi(self):
		self.multi = not self.multi

	def load_from_file(self, filename, id):
		self.id = id
		for line in open(filename, 'r'):
			if line.startswith('Question' + str(id) + " "):
				line = line.strip().split(' ')
				self.text = ' '.join(line[2:])
				self.options = []
				self.multi = (line[1] == 'multi=True')
			elif line.startswith('Q' + str(id) + 'O'):
				self.options.append(' '.join(line.strip().split(' ')[1:]))

	def load_from_dict(self, data):
		print(data)
		if 'questionNum' in data:
			self.id = data['questionNum']
		self.text = data['questionText']
		self.text = self.text.replace('&lt;', '<')
		self.text = self.text.replace('&gt;', '>')
		self.text = self.text.replace('&amp;', '&')

		self.multi = data['multi']
		for i, text in enumerate(data['options']):
			text = text.replace('&lt;', '<')
			text = text.replace('&gt;', '>')
			text = text.replace('&amp;', '&')
			option = Option(i, text)
			self.options.append(option)

	def save_to_end_of_file(self, filename, write_id):
		f = open(filename, 'a+')
		f.write('\n')
		print(self.multi)
		print(self.text)
		f.write('Question' + str(write_id) + ' multi=' + str(self.multi) + ' ' + self.text + '\n')
		for i, option in enumerate(self.options):
			f.write('Q' + str(write_id) + 'O' + str(i+1) + ' ' + option.text + '\n')

		f.close()
		return write_id

	def __str__(self):
		string = 'Question' + str(self.id) + ' multi=' + str(self.multi) + ' ' + self.text + '\n'
		for i, option in enumerate(self.options):
			string += 'Q' + str(self.id) + 'O' + str(i+1) + ' ' + option.text + '\n'
		return string

class Option:
	def __init__(self, id = -1, text = ""):
		self.id = id
		self.text = text