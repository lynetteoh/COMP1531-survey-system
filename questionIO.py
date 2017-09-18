from questionClass import Question, Option

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
			current_question = Question(id = int(line[0][8:]), text = ' '.join(line[2:]), multi = (line[1] == 'multi=True'))
		elif (line.strip() != ''):
			option = Option(id = int(line.split(' ')[0].split('O')[-1]), text = ' '.join(line.strip().split(' ')[1:]))
			current_question.options.append(option)
	if current_question != None:
				question_list.append(current_question)
	return question_list

#removes a question with that id
def remove_question(id):
	file = open(QUESTIONS_FILENAME, 'r')
	lines = file.readlines()
	file.close()

	file = open(QUESTIONS_FILENAME, 'w')

	for line in lines:
		if not (line.startswith('Question'+str(id)) or line.startswith('Q' + str(id) + 'O')):
			file.write(line)

	file.close()


#return largest available id.
def get_largest_question_id():
	largest_id = 1 #Yes, I know, I'm starting my indexing from 1. Deal with it.
	id_list = []
	for line in open(QUESTIONS_FILENAME, 'r'):
		if line.startswith('Question'):
			id_list.append(int(line.split(' ')[0][8:]))
	while largest_id in id_list:
		largest_id += 1;
	return largest_id

#writes question from a form to the questions file
def write_question(form):
	question = Question()
	question.load_from_dict(form)
	write_id = get_largest_question_id()
	return question.save_to_end_of_file(QUESTIONS_FILENAME, write_id)