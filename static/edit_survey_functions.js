//Javascript functions

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

	document.getElementsByTagName("center")[0].appendChild(enclosingDiv);
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
		console.log(divId.value);
		questionDiv.setAttributeNode(divId);

		var NUM_COLUMNS = 5;

		questionDiv.innerHTML = "\n" +
		"<table>\n" +
		"<tr>\n" +
		"	<th colspan = \"" + NUM_COLUMNS + "\">\n" +
		"		<h3>Q." + qNum + ": " + questionText + "</h3>\n" +
		"		<button onclick=\"toggleRadio(" + qNum + ")\">Choose one option</button>    \n" +
		"		<button onclick=\"saveQuestion(" + qNum + ")\">Save Question</button></th>\n" +
		"	</th>\n" +
		"</tr>\n" +
		"<tr>\n" +
		"	<td colspan = \"" + NUM_COLUMNS + "\"> <center> <button onclick=\"addOption(" + qNum + ")\">Add an option... </button> </center> </td>\n" +
		"</tr>\n" +
		"</table>\n"+
		"<br> <br> <br>\n";

		document.getElementById("qSpace").appendChild(questionDiv);
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
	var optionList = [];
	for (var i = 1; i < table.rows.length - 1; i++){
		if (table.rows[i].cells[0].getElementsByTagName("input").length == 0) {
			optionList.push(table.rows[i].cells[0].innerHTML);
		} else {
			if (!confirm("Would you like to discard options currently being edited?")){
				return;
			}
		}
	}

	var multi = true;
	if (table.rows[0].getElementsByTagName("button")[0].innerHTML == "Choose one option"){
		multi = false;
	}

	var questionText = table.rows[0].cells[0].getElementsByTagName("h3")[0].innerHTML;
	questionText = questionText.substring(("Q." + question + ": ").length, questionText.length);

	console.log("TEXT:", questionText);
	console.log("OPTIONS:", JSON.stringify(optionList));
	console.log("MULTI?", multi);

	$.ajax({
		type: "POST",
		dataType: "text",
		url: "/save_question",
		data: {questionNum: question,
			   question: questionText,
			   options: JSON.stringify(optionList),
			   multi: multi},
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

	newRow.innerHTML = "\n" +
	"	<td><input id = \"Q" + question + "O" + (numOptions + 1) + "input\"> </td>" +
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