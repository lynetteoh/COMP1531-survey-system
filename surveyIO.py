from questionClass import Question, Option

SURVEY_FILENAME = "surveys.txt"

def save_survey(course, semester, survey_data):
	if (get_survey(course, semester) != []):
		return 'Survey for that semester already exists'
	file = open(SURVEY_FILENAME, 'a+')
	file.write('BEGIN ' + course + ' ' + semester + '\n')
	for data in survey_data:
		question = Question()
		question.load_from_dict(data)
		file.write(str(question))
	file.write('END ' + course + ' ' + semester + '\n')
	file.close()

	return ('Success')


def get_survey(course, semester):
	survey_data = []
	being_read = False
	current_question = None
	for line in open(SURVEY_FILENAME, 'r'):
		line = line.strip()
		if line == 'BEGIN ' + course + ' ' + semester:
			being_read = True
		elif line == 'END ' + course + ' ' + semester:
			being_read = False
			if current_question != None:
				survey_data.append(current_question)
			return survey_data
		elif being_read:
			if line.startswith('Question'):
				if current_question != None:
					survey_data.append(current_question)
				line = line.strip().split(' ')
				current_question = Question(id = int(line[0][8:]), text = ' '.join(line[2:]), multi = (line[1] == 'multi=True'))
			elif (line.strip() != ''):
				option = Option(id = int(line.split(' ')[0].split('O')[-1]), text = ' '.join(line.strip().split(' ')[1:]))
				current_question.add_option(option)
	return survey_data

def get_active_surveys():
	surveys = []
	for line in open(SURVEY_FILENAME, 'r'):
		line = line.strip()
		if line.startswith('BEGIN'):
			course = line.split(' ')[1]
			semester = line.split(' ')[2]
			surveys.append((course, semester))
	return surveys