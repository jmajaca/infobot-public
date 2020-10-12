
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
	// set ids for each column
	// make 4th column a dropdown button
	$("table#reminders-table tr").each(function() {
		$("td", this).each(function(j) {
			switch(j){
				case 0:
					this.setAttribute('id', 'end_date')
					break;
				case 1:
					this.setAttribute('id', 'timer')
					break;
				case 2:
					this.setAttribute('id', 'text')
					break;
				case 3:
					this.setAttribute('id', 'posted')
					break;
				case 4:
					this.setAttribute('id', 'options')
					this.setAttribute('class', 'btn w-100')
					this.setAttribute('data-toggle', 'dropdown')
					break;
			}
		});
	});
}

function resetFilters(){
	$.post('/ui/reminder/filter', updateTable, 'json')
}

function editReminder(eventObject){
	let index = eventObject.parentElement.parentElement.parentElement.attributes[0].value
	$('#end_date')[index].setAttribute('contentEditable', 'true')
	$('#timer')[index].setAttribute('contentEditable', 'true')
	$('#text')[index].setAttribute('contentEditable', 'true')
	$('#posted')[index].setAttribute('contentEditable', 'true')
	$('#menu')[index].innerHTML = "<a class=\"ml-3 mr-2\" href=\"#\" onclick=\"save(this)\">Save</a> " +
									"<a class=\"mx-1\">or</a> " +
									"<a class=\"mr-3 ml-2\" href=\"#\" onclick=\"cancel(this)\">Cancel</a>"
	$('table#reminders-table tr')[parseInt(index)+1].classList.add('table-primary')
}

function cancel(eventObject) {
	let index = eventObject.parentElement.parentElement.parentElement.attributes[0].value
	$('#menu')[index].innerHTML = "<a class=\"ml-3 mr-2\" href=\"#\" onclick=\"editReminder(this)\">Edit</a> " +
									"<a class=\"mx-1\">or</a> " +
									"<a class=\"mr-3 ml-2\" href=\"#\" onclick=\"deleteReminder(this)\">Delete</a>"
	$('table#reminders-table tr')[parseInt(index)+1].classList.remove('table-primary')
}

function save(eventObject){
	let index = eventObject.parentElement.parentElement.parentElement.attributes[0].value
	$('#menu')[index].innerHTML = "<a class=\"ml-3 mr-2\" href=\"#\" onclick=\"editReminder(this)\">Edit</a> " +
								"<a class=\"mx-1\">or</a> " +
								"<a class=\"mr-3 ml-2\" href=\"#\" onclick=\"deleteReminder(this)\">Delete</a>"
	$('table#reminders-table tr')[parseInt(index)+1].classList.remove('table-primary')
}

function deleteReminder(){

}