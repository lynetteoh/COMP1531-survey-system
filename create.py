#Page for creating surveys

from flask import Flask, request, render_template
from courses import get_all_courses
import csv

COURSE_LISTING = 'courses.csv'

def view_courses(request, existing_surveys):
	surveyed_courses = [x.course for x in existing_surveys]
	unsurveyed_courses = []
	for course in get_all_courses():
		if course not in surveyed_courses:
			unsurveyed_courses.append(course)
	return render_template("select_course.html", courses = unsurveyed_courses)