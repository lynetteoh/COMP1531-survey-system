---------
Section 1
---------

The only non-standard python library is flask. It is a framework to run a web server, and includes templating services based off jinja2.

The standard libraries being used are:

- sqlite3  (For databasing)
- csv      (Reading CSV files)
- json     (Decoding json web data)
- time     (Recording time, for security timeout services)
- datetime (Saving a date, for start/end of survey)
- unittest (For testing)
- re       (For formatting database debugging)


---------
Section 2
---------

To run the server, navigate inside the application folder, and then run:
python3 run.py
The first line of output should be "Checking courses match database..."

Once the server has started, the site can be found at either of the following:
http://localhost:5555/
http://127.0.0.1:5555/

*IMPORTANT* If the data.db file does not exist or is empty, passwords, courses and enrolments will have to be loaded from the csv files. This should take at most 5 minutes, but after this has been done once the server will start rapidly (around 2 seconds).
If the statement "Database execution failed, uniqueness..." appears, this is because of duplicate data in the csv files, which is ignored.

A note for date constraints: A survey cannot be opened/closed until the open/close date.


---------
Section 3
---------

To run the tests, move tests.py into the application folder. Then run the command:
python3 tests.py

There are 5 classes of tests which will be run on the system. These are:
1. test_question        (Creation and saving of questions)
2. test_login           (Login of admin, staff and students)
3. test_survey          (Creation and saving of surveys)
4. enrol_student        (Enrolling students in courses)
5. test_update_question (Changing a question, assumes that question is created correctly i.e. Test class 1 passed)

Note: These tests only test the python code. To test the javascript code, which includes various data collection and verification, manual tests were conducted based on the acceptance criteria of user stories.
Also Note: The tests will save to a seperate database, so as not to clutter the actual database - this is test_data.db, which has an identical schema to data.db.


---------
Section 4
---------
Debugging information (if you are interested)

If you change silent = True to silent = False in databasing.py then you will see all SQL statements interacting with the database. Otherwise a "." is printed every 50 SQL statements, and a newline every 500.
In the python console, a log is printed when a user logs in or out.
