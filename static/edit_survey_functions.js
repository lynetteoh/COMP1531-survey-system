//Javascript functions

//Toggles visibility of existing questions
function toggle_view_questions(){
	questionsDiv = document.getElementById('saved_questions')
	if (questionsDiv.style.visibility == 'visible'){
		questionsDiv.style.visibility = 'hidden'
	} else {
		questionsDiv.style.visibility = 'visible'
	}
}

//Initialises the input box for adding a new question
function init_new_question(){
	var enclosingDiv = document.createElement("div");
	var divId = document.createAttribute("id");
	divId.value = "newQuestionDiv";
	enclosingDiv.setAttributeNode(divId);

	enclosingDiv.innerHTML = "\n" +
	"<br>\n" +
	"<input id = \"inputBox\">\n" +
	"<button onclick = \"finish_new_question(true)\">Add question</button>\n" +
	"<button onclick = \"finish_new_question(false)\">Cancel</button>\n";

	document.getElementById("newQuestionZone").appendChild(enclosingDiv);
}

//Deletes the input box for adding a new question
//adds the new question if saving is true 
function finish_new_question(saving){
	console.log("done");
	console.log("Saving?", saving);
	console.log(document.getElementById("inputBox").value)

	var questionText = document.getElementById("inputBox").value;
	var enclosingDiv = document.getElementById("newQuestionDiv");
	enclosingDiv.parentNode.removeChild(enclosingDiv);

	var qNum = 1; //Count all questions previously saved.
	var allDivs = document.getElementsByTagName("div");
	for (var i = 0; i < allDivs.length; i++){
		console.log(allDivs[i].id);
		if (allDivs[i].id.startsWith("Question")){
			qNum++;
		}
	}


	if (saving){
		var questionDiv = document.createElement("div");
		var divId = document.createAttribute("id");
		divId.value = "Question".concat(qNum.toString());
		var savedID = document.createAttribute("savedID");
		savedID.value = -1;
		console.log(divId.value);
		questionDiv.setAttributeNode(divId);
		questionDiv.setAttributeNode(savedID);

		var NUM_COLUMNS = 5;

		questionDiv.innerHTML = "\n" +
		"<table>\n" +
		"<tr>\n" +
		"	<th colspan = \"" + NUM_COLUMNS + "\">\n" +
		"		<h3>Q." + qNum + ": " + questionText + "</h3>\n" +
		"		<button onclick=\"toggleRadio(" + qNum + ")\">Choose one option</button>    \n" +
		"		<button onclick=\"toggleMandatory(" + qNum + ")\" style = 'color: #FF0000'>Mandatory</button>    \n" +
		"		<button onclick=\"saveQuestion(" + qNum + ")\">Save Question</button></th>\n" +
		"	</th>\n" +
		"</tr>\n" +
		"<tr>\n" +
		"	<td colspan = \"" + NUM_COLUMNS + "\"> <center> <button onclick=\"addOption(" + qNum + ")\">Add an option... </button>    \n" +
		"   <button onclick = \"toggleText(" + qNum + ")\">Multiple Choice</button> </center> </td>\n" +
		"</tr>\n" +
		"</table>\n"+
		"<br> <br> <br>\n";

		document.getElementById("qSpace").appendChild(questionDiv);
	}
}

function add_existing_question(questionID){
	var qNum = 1; //Count all questions previously saved.
	var allDivs = document.getElementsByTagName("div");
	for (var i = 0; i < allDivs.length; i++){
		if (allDivs[i].id.startsWith("Question")){
			qNum++;
		}
	}

	var questionDiv = document.createElement("div");
	var divId = document.createAttribute("id");
	divId.value = "Question".concat(qNum.toString());
	var savedID = document.createAttribute("savedID");
	savedID.value = questionID;
	console.log(divId.value);
	questionDiv.setAttributeNode(divId);
	questionDiv.setAttributeNode(savedID);

	var NUM_COLUMNS = 5;

	var questionRow = document.getElementById('existingQuestion'+questionID);
	var questionText = questionRow.cells[0].innerHTML;
	var questionOptions = document.getElementById('Q'+questionID+'Options').getElementsByTagName('li')

	questionDiv.innerHTML = "\n" +
	"<table>\n" +
	"<tr>\n" +
	"	<th colspan = \"" + NUM_COLUMNS + "\">\n" +
	"		<h3>Q." + qNum + ": " + questionText + "</h3>\n" +
	"		<button onclick=\"toggleRadio(" + qNum + ")\">Choose one option</button>    \n" +
	"		<button onclick=\"toggleMandatory(" + qNum + ")\" style=\"color:#FF0000\">Mandatory</button>    \n" +
	"		<button onclick=\"saveQuestion(" + qNum + ")\">Update Question</button></th>\n" +
	"	</th>\n" +
	"</tr>\n" +
	"</table>\n";

	for (var i = 0; i < questionOptions.length; i++){
		var optionRow = questionDiv.getElementsByTagName("table")[0].insertRow(questionDiv.getElementsByTagName("table")[0].rows.length);
		var rowCode  = "	<td>" + questionOptions[i].innerHTML + "</td>\n" +
		"	<td><button onclick = \"editOption(" + qNum + ", " + (i + 1) + ")\">Edit</button> </td> \n" +
		"	<td><button onclick = \"deleteOption(" + qNum + ", " + (i + 1) + ")\">Delete</button> </td>\n";
		if (i == 0){
			rowCode += "	<td></td>";
		} else {
			rowCode += "	<td><button onclick = \"moveUp(" + qNum + ", " + (i + 1) + ")\">Up</button></td>\n";
		}
		if (i == questionOptions.length - 1){
			rowCode += "	<td></td>";
		} else {
			rowCode += "	<td><button onclick = \"moveDown(" + qNum + ", " + (i + 1) + ")\">Down</button></td>\n";
		}
		var rowId = document.createAttribute("id");
		rowId.value = "Q"+qNum+"O"+(i+1);
		var rowClass = document.createAttribute("class");
		rowClass.value = "collapse in";
		optionRow.setAttributeNode(rowClass);
		optionRow.innerHTML = rowCode;
		optionRow.setAttributeNode(rowId);
	}

	var finalRow = questionDiv.getElementsByTagName("table")[0].insertRow(questionDiv.getElementsByTagName("table")[0].rows.length);
	finalRow.innerHTML = "	<td colspan = \"" + NUM_COLUMNS + "\"> <center> <button onclick=\"addOption(" + qNum + ")\">Add an option... </button>    \n" +
						 " 		<button onclick = \"toggleText(" + qNum + ")\">Multiple Choice</button> </center> </td>\n"
	questionDiv.innerHTML += "<br><br><br>"

	console.log(questionDiv);

	document.getElementById("qSpace").appendChild(questionDiv);

	if (questionRow.cells[1].getElementsByTagName('p')[0].innerHTML == "Choose Many:"){
		toggleRadio(qNum);
	}

	toggle_view_questions();
}

//Toggles whether a question is mandatory
function toggleMandatory(question){
	console.log("toggleMan", question);
	var table = document.getElementById("Question"+question).getElementsByTagName("table")[0];

	button = table.rows[0].getElementsByTagName("button")[1];
	if (button.innerHTML == "Mandatory"){
		button.innerHTML = "Optional";
		button.style.color = "#000000";
	} else {
		button.innerHTML = "Mandatory";
		button.style.color = "#FF0000";
	}
}

//Toggles whether question n uses radio buttons or check boxes
function toggleRadio(question){
	console.log("toggle", question);

	button = document.getElementById("Question"+question).getElementsByTagName("table")[0].rows[0].getElementsByTagName("button")[0];
	if (button.innerHTML == "Choose one option"){
		button.innerHTML = "Choose many options";
	} else {
		button.innerHTML = "Choose one option";
	}
}

//Saves a question to the csv file
function saveQuestion(question){
	console.log("saving question", question);
	var table = document.getElementById("Question"+question).getElementsByTagName("table")[0];
	var text = false;
	if (table.rows[table.rows.length-1].getElementsByTagName("button")[1].innerHTML == 'Text Input'){
		text = true;
	}
	var optionList = [];
	if (!text) {
		if (table.getElementsByTagName("input").length != 0) {
			if (!confirm("Saving will ignore options currently being edited.")){
				return;
			}
		}

		for (var i = 1; i < table.rows.length - 1; i++){
			if (table.rows[i].cells[0].getElementsByTagName("input").length == 0) {
				optionList.push(table.rows[i].cells[0].innerHTML);
			}
		}
	}

	var multi = true;
	if (table.rows[0].getElementsByTagName("button")[0].innerHTML == "Choose one option"){
		multi = false;
	}

	var mandatory = false;
	if (table.rows[0].getElementsByTagName("button")[1].innerHTML == "Mandatory"){
		mandatory = true;
	}

	if (!text && optionList.length == 0){
		alert("A multiple choice question must have options!");
		return;
	}

	var questionText = table.rows[0].cells[0].getElementsByTagName("h3")[0].innerHTML;
	questionText = questionText.substring(("Q." + question + ": ").length, questionText.length);

	var saved_id = table.parentNode.savedID

	console.log("QTEXT:", questionText);
	console.log("OPTIONS:", JSON.stringify(optionList));
	console.log("MULTI?", multi);
	console.log("TEXT?", text);
	console.log("Mandatory?", mandatory);
	console.log("Saved ID:", saved_id)

	$.ajax({
		type: "POST",
		dataType: "text",
		url: "/save_question",
		data: {
			questionNum: question,
			questionText: questionText,
			options: JSON.stringify(optionList),
			multi: multi,
			text: text,
			mandatory: mandatory,
			saved_id: saved_id
		},
		success: function callback(response){
			alert(response);
		}
	});
}

function delete_existing_question(id){
	console.log("deleting question", id);
	if (!confirm("Are you sure you want to delete this question?")){
		return;
	}

	row = document.getElementById("existingQuestion" + id);
	row.parentNode.removeChild(row);

	$.ajax({
		type: "POST",
		dataType: "text",
		url: "/delete_question",
		data: {id: id},
		success: function callback(response){
			alert(response);
		}
	});
}

//Adds an option to a question
function addOption(question){
	console.log("adding option to question", question);
	var questionDiv = document.getElementById("Question" + question);
	var table = questionDiv.getElementsByTagName("table")[0];
	var numOptions = table.getElementsByTagName("tr").length - 2; //Existing options


	var newRow = table.insertRow(numOptions + 1);


	var rowID = document.createAttribute("id");
	rowID.value = "Q" + question + "O" + (numOptions + 1);
	newRow.setAttributeNode(rowID);

	var rowClass = document.createAttribute("class");
	rowClass.value = "collapse in";
	newRow.setAttributeNode(rowClass);

	newRow.innerHTML = "\n" +
	"	<td><input id = \"Q" + question + "O" + (numOptions + 1) + "input\"> </td>\n" +
	"	<td><button onclick = \"finishOptionEdit(" + question + ", " + (numOptions + 1) + ")\">Add</button> </td> \n" +
	"	<td><button onclick = \"deleteOption(" + question + ", " + (numOptions + 1) + ")\">Cancel</button> </td>\n" +
	"	<td></td>\n" +
	"	<td></td>\n";

	if (numOptions != 0) {
		newRow.cells[3].innerHTML = "<button onclick = \"moveUp(" + question + ", " + (numOptions + 1) + ")\">Up</button>";
		table.rows[numOptions].cells[4].innerHTML = "<button onclick = \"moveDown(" + question + ", " + numOptions + ")\">Down</button> </td>\n";
	}
}

function finishOptionEdit(question, option){
	console.log("Finish", question, option);
	var row = document.getElementById("Q" + question + "O" + option);
	var text = document.getElementById("Q"+question+"O"+option+"input").value;
	row.cells[0].innerHTML = text;

	row.cells[1].innerHTML = "<button onclick = \"editOption(" + question + ", " + option + ")\">Edit</button>";

	row.cells[2].innerHTML = "<button onclick = \"deleteOption(" + question + ", " + option + ")\">Delete</button>";
}

function editOption(question, option){
	console.log("EDIT", question, option);
	var row = document.getElementById("Q" + question + "O" + option);
	var text = row.cells[0].innerHTML;
	row.cells[0].innerHTML = "<input id = \"Q" + question + "O" + option + "input\" value = \""+ text + "\">";
	row.cells[1].innerHTML = "<button onclick = \"finishOptionEdit(" + question + ", " + option + ")\">Done</button>";
}

function deleteOption(question, option){
	console.log("DELETE", question, option);
	var row = document.getElementById("Q" + question + "O" + option);
	var table = row.parentNode;
	if (option == 1){
		if (table.rows.length - 2 > 1){
			table.rows[2].cells[3].innerHTML = "";
		}
	}
	else if (option == table.rows.length - 2){
		table.rows[option - 1].cells[4].innerHTML = "";
	}
	row.parentNode.deleteRow(option);

	//Update all subsequent id's (what a hassle >.<)
	for (var i = option; i < table.rows.length - 1; i++){
		correct_IDs(question, i);
	}
}

function toggleText(question){
	var table = document.getElementById("Question"+question).getElementsByTagName("table")[0];
	console.log(table);
	var button = table.rows[table.rows.length-1].getElementsByTagName("button")[1];
	var multiButton = table.rows[0].getElementsByTagName("button")[0];
	var addOptionButton = table.rows[table.rows.length-1].getElementsByTagName("button")[0];
	console.log(button);
	if (button.innerHTML == "Multiple Choice"){
		button.innerHTML = "Text Input";
		for (var i = 1; i < table.rows.length - 1; i++){
			console.log(table.rows[i])
			table.rows[i].className = "collapse"
		}
		multiButton.disabled = true;
		addOptionButton.disabled = true;
	} else {
		button.innerHTML = "Multiple Choice";
		for (var i = 1; i < table.rows.length - 1; i++){
			table.rows[i].className = "collapse in"
		}
		multiButton.disabled = false;
		addOptionButton.disabled = false;
	}
}

function correct_IDs(question, option){
	var table = document.getElementById("Question"+question).getElementsByTagName("table")[0];
	table.rows[option].id = "Q" + question + "O" + option;
	var editing = table.rows[option].cells[0].getElementsByTagName("input").length > 0;
	if (editing){
		table.rows[option].cells[0].getElementsByTagName("input")[0].id = "Q" + question + "O" + option + "input";
	}
	if (editing){
		console.log("<button onclick = \"finishOptionEdit(" + question + ", " + option + ")\">Done</button>");
		table.rows[option].cells[1].innerHTML = "<button onclick = \"finishOptionEdit(" + question + ", " + option + ")\">Done</button>";
	} else {
		table.rows[option].cells[1].innerHTML = "<button onclick = \"editOption(" + question + ", " + option + ")\">Edit</button>";
	}
	table.rows[option].cells[2].innerHTML = "<button onclick = \"deleteOption(" + question + ", " + option + ")\">Delete</button>";

	if (table.rows[option].cells[3].getElementsByTagName("button").length > 0) {
		table.rows[option].cells[3].innerHTML = "<button onclick = \"moveUp(" + question + ", " + option + ")\">Up</button>";
	}

	if (table.rows[option].cells[4].getElementsByTagName("button").length > 0) {
		table.rows[option].cells[4].innerHTML = "<button onclick = \"moveDown(" + question + ", " + option + ")\">Down</button>";
	}
}

function moveUp(question, option){
	console.log("moveUp", question, option);
	var row = document.getElementById("Q" + question + "O" + option);
	var prev_row = document.getElementById("Q" + question + "O" + (option-1));
	var row_innerHTML = row.innerHTML;
	row.parentNode.deleteRow(option);
	var new_row = prev_row.parentNode.insertRow(option-1);
	new_row.innerHTML = row_innerHTML;
	correct_IDs(question, option-1);
	correct_IDs(question, option);
	if (option-1 == 1){
		new_row.cells[3].innerHTML = "";
		prev_row.cells[3].innerHTML = "<button onclick = \"moveUp(" + question + ", " + option + ")\">Up</button>";
	}
	if (option == new_row.parentNode.rows.length - 2){
		prev_row.cells[4].innerHTML = "";
		new_row.cells[4].innerHTML = "<button onclick = \"moveDown(" + question + ", " + (option-1) + ")\">Down</button>";
	}
}

function moveDown(question, option){
	console.log("moveDown", question, option);
	var row = document.getElementById("Q" + question + "O" + option);
	var next_row = document.getElementById("Q" + question + "O" + (option+1));
	var row_innerHTML = row.innerHTML;
	row.parentNode.deleteRow(option);
	var new_row = next_row.parentNode.insertRow(option+1);
	new_row.innerHTML = row_innerHTML;
	correct_IDs(question, option);
	correct_IDs(question, option+1);
	if (option == 1){
		next_row.cells[3].innerHTML = "";
		new_row.cells[3].innerHTML = "<button onclick = \"moveUp(" + question + ", " + (option+1) + ")\">Up</button>";
	}
	if (option+1 == new_row.parentNode.rows.length - 2){
		new_row.cells[4].innerHTML = "";
		next_row.cells[4].innerHTML = "<button onclick = \"moveDown(" + question + ", " + option + ")\">Down</button>";
	}
}

function moveQuestionUp(question){
	console.log("Raise ", question)
}

function moveQuestionDown(question){
	console.log("Lower ", question)
}

function discard_survey(){
	if (confirm('Warning: This will discard the current survey')){
		window.location.href = '/adminHome';
	}
}

function publish_survey(){
	console.log("Publish...");
	var survey = [];
	var allDivs = document.getElementById("qSpace").getElementsByTagName("div");
	if (!confirm("Are you sure you want to publish?\nPublishing will ignore options currently being edited, and make the survey available to staff for review.")){
		return;
	}
	console.log(allDivs.length);
	for (var div = 0; div < allDivs.length; div++){
		console.log(div);
		if (allDivs[div].id.startsWith("Question")){
			var question = parseInt(allDivs[div].id.substring(8, allDivs[div].id.length));

			var table = document.getElementById(allDivs[div].id).getElementsByTagName("table")[0];
			var text = false;
			if (table.rows[table.rows.length-1].getElementsByTagName("button")[1].innerHTML == 'Text Input'){
				text = true;
			}
			var optionList = [];
			if (!text) {
				for (var i = 1; i < table.rows.length - 1; i++){
					if (table.rows[i].cells[0].getElementsByTagName("input").length == 0) {
						optionText = table.rows[i].cells[0].innerHTML;
						optionList.push(optionText);
					}
				}
			}

			var multi = true;
			if (table.rows[0].getElementsByTagName("button")[0].innerHTML == "Choose one option"){
				multi = false;
			}

			var mandatory = false;
			if (table.rows[0].getElementsByTagName("button")[1].innerHTML == "Mandatory"){
				mandatory = true;
			}

			if (!text && optionList.length == 0){
				alert("Question " + question + " is a multiple choice question, but it has no options!");
				return;
			}

			var questionText = table.rows[0].cells[0].getElementsByTagName("h3")[0].innerHTML;
			questionText = questionText.substring(("Q." + question + ": ").length, questionText.length);

			console.log("ID:", question);
			console.log("TEXT:", questionText);
			console.log("OPTIONS:", optionList);
			console.log("MULTI?", multi);
			console.log("TEXT?", text);
			console.log("MANTATORY:", mandatory);

			survey.push({
				questionNum: question,
				questionText: questionText,
				options: optionList,
				multi: multi,
				text: text,
				mandatory: mandatory
			});
		}
	}
	if (survey.length == 0){
		alert("Please add a question before publishing the survey");
		return;
	}

	var start = document.getElementById('start').value;
	var end = document.getElementById('end').value;
	if (start == '' || end == ''){
		alert("Please specify the start and end dates for this survey.");
		return;
	}

	if (start.includes('/') && end.includes('/')){
		start = start.split('/')[2] + '-' + start.split('/')[1] + '-' + start.split('/')[0];
		end = end.split('/')[2] + '-' + end.split('/')[1] + '-' + end.split('/')[0];
	}

	if (!date_lte(start, end)){
		alert("The closing date for the survey must be on or after the starting date.");
		return;
	}

	if (!date_in_future(start) || !date_in_future(end)){
		alert("The starting date is in the past");
		return;
	}

	var url_pathname = window.location.pathname.split("/");
	var course = url_pathname[url_pathname.length-2];
	var semester = url_pathname[url_pathname.length-1];

	$.ajax({
		type: "POST",
		dataType: "text",
		url: "/publish_survey",
		data: {surveyData: JSON.stringify(survey),
			   semester: semester,
			   course: course,
			   start: start,
			   end: end},
		success: function callback(response){
			if (response == 'Success'){
				alert('Survey successfully published!\nSurvey can be found at: ' + window.location.hostname + window.location.pathname.replace('/create/', '/survey/'));
				window.location.href = "/login";
			} else {
				alert(response);
			}
		}
	});
}

function date_in_future(a){

	//----
	//Code taken from <https://stackoverflow.com/questions/1531093/how-do-i-get-the-current-date-in-javascript>
	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth()+1; //January is 0!
	var yyyy = today.getFullYear();

	if(dd<10) {
	    dd = '0'+dd
	} 

	if(mm<10) {
	    mm = '0'+mm
	} 
	//----

	return (date_lte(yyyy+'-'+mm+'-'+dd, a))
}

//Compares two dates to see if a is less than or equal to b.
function date_lte(a, b){
	if (parseInt(a.split('-')[0]) < parseInt(b.split('-')[0])){
		return true;
	}
	if (parseInt(a.split('-')[0]) > parseInt(b.split('-')[0])){
		return false;
	}
	if (parseInt(a.split('-')[1]) < parseInt(b.split('-')[1])){
		return true;
	}
	if (parseInt(a.split('-')[1]) > parseInt(b.split('-')[1])){
		return false;
	}
	if (parseInt(a.split('-')[2]) <= parseInt(b.split('-')[2])){
		return true;
	}
	return false;
}