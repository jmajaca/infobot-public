
function getFilters(){
	let course = $('#course').val()
	let author = $('#author').val()
	let from_date = $('#from').val()
	let to_date = $('#to').val()
	let posted = $('#check').is(':checked')
	$.post('/ui/reminder/filter?name=' + course + '&author=' + author + '&from=' + from_date + '&to=' + to_date + '&posted=' + posted,
		updateTable, 'json')
}

function updateTable(data){
	for(let i=0; i<data.result; i++){
		data.rows[i].options = $('#reminders-table').bootstrapTable('getData')[0].options
	}
	$('#reminders-table').bootstrapTable('load', data)
}

function resetFilters(){
	$.post('/ui/reminder/filter', updateTable, 'json')
}

function editReminder(eventObject){
	// get index of the row
	let index = parseInt(eventObject.parentElement.parentElement.attributes[0].value)
	console.log(index)
	let row = $('#reminders-table').bootstrapTable('getRowByUniqueId', index)
	// $('#end_date')[index].setAttribute('contentEditable', 'true')
	// $('#timer')[index].setAttribute('contentEditable', 'true')
	// $('#text')[index].setAttribute('contentEditable', 'true')
	// $('#posted')[index].setAttribute('contentEditable', 'true')
	row.options.innerHTML = "<a class=\"mx-1\" href=\"#\" onclick=\"save(this)\">Save</a> " +
									"<a class=\"mx-1\">or</a> " +
									"<a class=\"mx-1\" href=\"#\" onclick=\"cancel(this)\">Cancel</a>"
}

function cancel(eventObject){
	let index = eventObject.parentElement.parentElement.attributes[0].value
	alert("canceled editing " + index + ". row")
	$('#options')[index].innerHTML = "<a class=\"mx-1\" href=\"#\" onclick=\"editReminder(this)\">Edit</a> " +
								"<a class=\"mx-1\">or</a> " +
								"<a class=\"mx-1\" href=\"#\" onclick=\"deleteReminder(this)\">Delete</a>"
}

function save(eventObject){
	let index = eventObject.parentElement.parentElement.attributes[0].value
	alert("saving " + index + ". row")
	$('#options')[index].innerHTML = "<a class=\"mx-1\" href=\"#\" onclick=\"editReminder(this)\">Edit</a> " +
								"<a class=\"mx-1\">or</a> " +
								"<a class=\"mx-1\" href=\"#\" onclick=\"deleteReminder(this)\">Delete</a>"
}

function deleteReminder(){

}