function deleteQuestion(question) {
	var table = document.getElementById("Question"+question);
	var count = 1;
	var tables = table.parentNode.getElementsByTagName("table");
	for (var other_table = 0; other_table < tables.length; other_table++) {
		if (tables[other_table] == table) {
			break;
		} else {
			count ++;
		}
	}
	var questionText = table.rows[0].cells[0].innerHTML.split("<br>")[0].split(': ')[1];
	console.log(questionText);
	var type = table.rows[0].cells[0].getElementsByTagName("i")[0].innerHTML;
	console.log(type);
	var options = [];
	for (var i = 1; i < table.rows.length; i++) {
		options.push(table.rows[i].cells[0].innerHTML);
	}
	console.log(options);
	table.parentNode.removeChild(table);
	for (var other_table = count - 1; other_table < tables.length - 1; other_table ++) {
		tables[other_table].innerHTML.replace("Q." + (other_table + 2) + ":", "Q." + (other_table + 1) + ":");
	}

	var newRow = document.getElementById('optional_questions').insertRow(document.getElementById('optional_questions').rows.length);
	var rowId = document.createAttribute("id");
	rowId.value = "existingQuestion" + question;
	newRow.setAttributeNode(rowId);

	rowCode =   "<td style = \"width: 30%\">" + questionText + "</td> \n" +
				"<td style = \"width: 40%\">\n"
	if (type == "Text response") {
		rowCode += "<p>Text</p>\n"
	} else {
		if (type == "Choose many:") {
			rowCode += "<p>Choose Many:</p>\n"
		} else {
			rowCode += "<p>Choose One:</p>\n"
		}
		rowCode += "<button data-toggle=\"collapse\" data-target=\"#Q" + question + "Options\">Show options...</button>\n" + 
		"<div id = \"Q" + question + "Options\" class=\"collapse\">\n" +
		"<ul>\n";
		for (i = 0; i < options.length; i++) {
			rowCode += "	<li style = \"white-space: wrap\">" + options[i] + "</li>\n";
		}
		rowCode += "</ul>\n</div>\n";
	}
	rowCode += "</td>\n" +
	"<td style = \"width: 15%\"> <button onclick=\"addQuestion(" + question + ")\"> Add </button> </td> \n" +
	"</tr>\n";

	newRow.innerHTML = rowCode;
}

function addQuestion(question) {
	var qRow = document.getElementById("existingQuestion" + question);
	var questionText = qRow.cells[0].innerHTML;
	var type = qRow.cells[1].getElementsByTagName("p")[0].innerHTML;
	var options = [];
	if (type != "Text") {
		var raw_options = qRow.cells[1].getElementsByTagName("ul")[0].getElementsByTagName("li");
		for (var i = 0; i < raw_options.length; i++){
			options.push(raw_options[i].innerHTML);
		}
	}

	qRow.parentNode.removeChild(qRow);

	var table = document.createElement("table");
	var tableId = document.createAttribute("id");
	tableId.value = "Question" + question;
	table.setAttributeNode(tableId);

	var tableCode = "<tr>\n" +
	"<th>Q." + (document.getElementById('qspace').getElementsByTagName("table").length + 1) + ": " + questionText + "<br>\n" +
	"<b>Optional</b> <button onclick = \"deleteQuestion(" + question + ")\"> Delete </button>\n";

	if (type == "Text"){
		tableCode += "<i>Text response</i>\n";
	} else if (type == "Choose Many:") {
		tableCode += "<i>Choose many:</i>\n";
	} else {
		tableCode += "<i>Choose one:</i>\n";
	}

	tableCode += "</th>\n" +
	"</tr>\n";

	for (var i = 0; i < options.length; i++){
		tableCode += "<tr>\n" +
		"<td>" + options[i] + "</td>\n" +
		"</tr>\n";
	}

	table.innerHTML = tableCode;

	document.getElementById('qspace').appendChild(table);
}