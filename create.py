#Page for creating surveys

from flask import Flask, request, render_template
import csv

COURSE_LISTING = 'courses.csv'

def view_courses(request, active_surveys):
	courses = []
	with open(COURSE_LISTING,'r') as csv_in:
		reader = csv.reader(csv_in)
		first_line_read = False
		for row in reader:
			if len(row) == 1:
				row = row[0].split(" ")
			if (row[0], row[1]) not in active_surveys:
				courses.append(row)
	return render_template("select_course.html", courses = courses)