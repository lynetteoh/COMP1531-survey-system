from flask import Flask, request
import os

def save_response(course, semester, form):
	try:
		file = open('responses/'+course+'__'+semester+'.txt', 'a+')
	except FileNotFoundError:
		file = open('responses/'+course+'__'+semester+'.txt', 'w+')
		file.close()
		file = open('responses/'+course+'__'+semester+'.txt', 'a+')
	file.write('New Response\n')
	question = 1
	response = ' '.join(form.getlist('Q'+str(question)))
	while response != '':
		print("Writing", response)
		file.write('Q' + str(question) + '    ' + response + '\n')
		response = ' '.join(form.getlist('Q'+str(question)))
		question += 1
	file.close()

	return "Thankyou for trying the survey system, responses are currently not being processed, but your response was recorded.";