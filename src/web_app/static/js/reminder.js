
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

let rowDataBeforeEdit = { end_date:'', timer:'', text:'', posted:''}	// needed for saving row state in case of canceling
function editReminder(eventObject){
	// get index of row on which event was called
	// path: a -> dropdown-menu -> td -> tr
	let index = eventObject.parentElement.parentElement.parentElement.attributes[0].value
	for(const name of ['end_date', 'timer', 'text', 'posted']){
		let elem = $('#'+name)[index]
		elem.setAttribute('contentEditable', 'true')
		rowDataBeforeEdit[name] = elem.textContent
	}
	$('#menu')[index].innerHTML = "<a class=\"ml-3 mr-2\" href=\"#\" onclick=\"save(this)\">Save</a> " +
									"<a class=\"mx-1\">or</a> " +
									"<a class=\"mr-3 ml-2\" href=\"#\" onclick=\"cancel(this)\">Cancel</a>"
	$('table#reminders-table tr')[parseInt(index)+1].classList.add('table-danger')
}

function cancel(eventObject) {
	let index = eventObject.parentElement.parentElement.parentElement.attributes[0].value
	for(const name of ['end_date', 'timer', 'text', 'posted']){
		$('#'+name)[index].textContent = rowDataBeforeEdit[name]
	}
	finishEditing(index)
}

function save(eventObject){
	let index = eventObject.parentElement.parentElement.parentElement.attributes[0].value
	finishEditing(index)
}

function finishEditing(index){
	for(const n of ['end_date', 'timer', 'text', 'posted']){
		$('#'+n)[index].setAttribute('contentEditable', 'false')
	}
	$('#menu')[index].innerHTML = "<a class=\"ml-3 mr-2\" href=\"#\" onclick=\"editReminder(this)\">Edit</a> " +
								"<a class=\"mx-1\">or</a> " +
								"<a class=\"mr-3 ml-2\" href=\"#\" onclick=\"deleteReminder(this)\">Delete</a>"
	$('table#reminders-table tr')[parseInt(index)+1].classList.remove('table-danger')
}

function deleteReminder(){

}