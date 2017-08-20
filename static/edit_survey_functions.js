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
}

//Saves a question to the csv file
function saveQuestion(question){
	console.log("saving question", question);
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
}

function moveUp(question, option){
	console.log("moveUp", question, option);
}

function moveDown(question, option){
	console.log("moveDown", question, option);
}