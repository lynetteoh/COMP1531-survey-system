QUESTIONS_FILENAME = "questions.txt"

#Significantly faster than looping over all ID's.
def read_all_questions():
	question_list = []
	current_question = None
	for line in open(QUESTIONS_FILENAME, 'r'):
		if line.startswith('Question'):
			if current_question != None:
				question_list.append(current_question)
			line = line.strip().split(' ')
			current_question = {'id': int(line[0][8:]), 'questionText': ' '.join(line[2:]), 'options': [], 'multi': line[1] == "multi=True"}
		elif (line.strip() != ''):
			current_question['options'].append(' '.join(line.strip().split(' ')[1:]))
	if current_question != None:
				question_list.append(current_question)
	return question_list


def read_question_by_id(id):
	return {}

#return largest available id.
def get_largest_id():
	largest_id = 1 #Yes, I know, I'm starting my indexing from 1. Deal with it.
	for line in open(QUESTIONS_FILENAME, 'r'):
		if line.startswith('Question'):
			cur_id = int(line.split(' ')[0][8:])
			if (largest_id == cur_id):
				largest_id += 1
	return largest_id

def write_question(questionText, options, multi):
	id = get_largest_id()

	f = open(QUESTIONS_FILENAME, 'a+')
	f.write('\n')
	f.write('Question' + str(id) + ' multi=' + str(multi) + ' ' + questionText + '\n')
	for i, option in enumerate(options):
		f.write('Q' + str(id) + 'O' + str(i+1) + ' ' + option + '\n')
	f.close()
	return id