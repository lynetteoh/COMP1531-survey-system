SURVEY_FILENAME = "surveys.txt"

def save_survey(course, semester, survey_data):
	if (get_survey(course, semester) != []):
		return 'Survey for that semester already exists'
	file = open(SURVEY_FILENAME, 'a')
	file.write('BEGIN ' + course + ' ' + semester + '\n')
	for question in survey_data:
		file.write('Question' + str(question['questionNum']) + ' multi=' + str(question['multi']) + ' ' + question['question'] + '\n')
		for i, option in enumerate(question['options']):
			file.write('Q' + str(question['questionNum']) + 'O' + str(i+1) + ' ' + option + '\n')
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
				current_question = {'id': int(line[0][8:]), 'questionText': ' '.join(line[2:]), 'options': [], 'multi': line[1] == 'multi=True'}
			elif (line.strip() != ''):
				optionNum = int(line.split(' ')[0].split('O')[-1])
				current_question['options'].append((optionNum, ' '.join(line.strip().split(' ')[1:])))
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