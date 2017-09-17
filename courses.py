from courseClass import Course
import csv

COURSE_LISTING = 'courses.csv'

COURSES = []
#Read in courses
with open(COURSE_LISTING,'r') as csv_in:
	reader = csv.reader(csv_in)
	for name, semester in reader:
		course = Course(name, semester)
		COURSES.append(course)

def find_course(name, semester):
	for course in COURSES:
		if course.matches(name, semester):
			return course
	return None