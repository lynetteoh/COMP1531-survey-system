#Page for creating surveys

from flask import Flask, request, render_template
from courses import get_all_courses
import csv

COURSE_LISTING = 'courses.csv'

def view_courses(request, existing_surveys, semester):
	surveyed_courses = [x.course for x in existing_surveys]
	unsurveyed_courses = []
	for course in get_all_courses():
		if course not in surveyed_courses and course.semester == semester:
			unsurveyed_courses.append(course)
	return render_template("select_course.html", courses = unsurveyed_courses)

def view_semesters(request, existing_surveys):
	surveyed_courses = [x.course for x in existing_surveys]
	unsurveyed_semesters = []
	for course in get_all_courses():
		if course not in surveyed_courses and course.semester not in unsurveyed_semesters:
			unsurveyed_semesters.append(course.semester)
	return render_template("select_semester.html", semesters = unsurveyed_semesters)
