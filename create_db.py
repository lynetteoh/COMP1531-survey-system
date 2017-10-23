from databasing import db_execute

def create_db(filename):
	db_execute(filename, """
	CREATE TABLE IF NOT EXISTS SURVEYS
	(ID INT PRIMARY KEY    NOT NULL,
	 START DATE            NOT NULL,
	 END DATE              NOT NULL,
	 COURSE CHAR(8)        NOT NULL,
	 SEMESTER CHAR(4)      NOT NULL,
	 STATE INT             NOT NULL
	);
	""", silent = True)

	db_execute(filename, """
	CREATE TABLE IF NOT EXISTS QUESTIONS
	(ID INT PRIMARY KEY    NOT NULL,
	 QUESTION_TEXT TEXT    NOT NULL,
	 TEXT BOOLEAN          NOT NULL,
	 MULTI BOOLEAN,
	 MANDATORY BOOLEAN     NOT NULL,
	 VISIBLE BOOLEAN       NOT NULL
	);
	""", silent = True)

	db_execute(filename, """
	CREATE TABLE IF NOT EXISTS OPTIONS
	(ID INT PRIMARY KEY    NOT NULL,
	 OPTION TEXT           NOT NULL,
	 QUESTIONID INT        NOT NULL,
	 FOREIGN KEY (QUESTIONID) REFERENCES QUESTIONS(ID)
	);
	""", silent = True)

	db_execute(filename, """
	CREATE TABLE IF NOT EXISTS INCLUDE
	(SURVEYID INT          NOT NULL,
	 QUESTIONID INT        NOT NULL, POSITION INT NOT NULL DEFAULT -1,
	 PRIMARY KEY (SURVEYID, QUESTIONID),
	 FOREIGN KEY (SURVEYID) REFERENCES SURVEYS(ID),
	 FOREIGN KEY (QUESTIONID) REFERENCES QUESTIONS(ID)
	);
	""", silent = True)

	db_execute(filename, """
	CREATE TABLE IF NOT EXISTS RESPONSES
	(ID INT PRIMARY KEY    NOT NULL,
	 ZID INT               NOT NULL,
	 RESPONSE TEXT         NOT NULL,
	 QUESTIONID INT        NOT NULL,
	 SURVEYID INT          NOT NULL,
	 FOREIGN KEY (QUESTIONID) REFERENCES QUESTIONS(ID),
	 FOREIGN KEY (SURVEYID) REFERENCES SURVEYS(ID)
	);
	""", silent = True)

	db_execute(filename, """
	CREATE TABLE IF NOT EXISTS PASSWORDS
	(ZID INT PRIMARY KEY    NOT NULL,
	 PASSWORD TEXT          NOT NULL,
	 ROLE TEXT              NOT NULL
	);
	""", silent = True)

	db_execute(filename, """
	CREATE TABLE IF NOT EXISTS COURSES
	(NAME TEXT              NOT NULL,
	 SEMESTER TEXT          NOT NULL,
	 PRIMARY KEY (NAME, SEMESTER)
	);
	""", silent = True)

	db_execute(filename, """
	CREATE TABLE IF NOT EXISTS ENROLMENTS
	(ZID INT                NOT NULL,
	 COURSE TEXT            NOT NULL,
	 SEMESTER TEXT          NOT NULL,
	 PRIMARY KEY (ZID, COURSE, SEMESTER),
	 FOREIGN KEY (ZID) REFERENCES PASSWORDS(ZID)
	);
	""", silent = True)