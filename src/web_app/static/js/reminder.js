
// classes disappear after applying filters and then sorting
// so reset them after table body rendering
$(document).ready(function (){
	$('#reminders-table').on('post-body.bs.table', setClasses)
})


// passes all filter fields to the back
function getFilters(){
	let course = $('#course').val()
	let author = $('#author').val()
	let from_date = $('#from').val()
	let to_date = $('#to').val()
	let posted = $('#check').is(':checked')
	$.post('/ui/reminder/filter?name=' + course + '&author=' + author + '&from=' + from_date + '&to=' + to_date + '&posted=' + posted,
		updateTable, 'json')
}

/*
updates data in the table
params: data : json { result : number of reminders
					  rows : reminder data }
 */
function updateTable(data){
	let optionsHTML = "&hellip;<div class=\"dropdown-menu menu\">\n" +
						"<a class=\"ml-3 mr-2\" href=\"#\" onclick=\"editReminder(this)\">Edit</a>\n" +
						"<a class=\"mx-1\">or</a>\n" +
						"<a class=\"mr-3 ml-2\" href=\"#\" onclick=\"deleteReminder(this)\">Delete</a>\n" +
						"</div>"
	for(let i=0; i<data.result; i++){
		data.rows[i].posted = data.rows[i].posted ? 'True' : 'False'	// just for the capital letter
		data.rows[i].options = optionsHTML	// add dropdown menu with edit and delete options
	}
	$('#reminders-table').bootstrapTable('load', data)
	setClasses()	// method 'load' removes all class attributes
}

/*
resets classes on all rows after data update
make 5th column a dropdown button
 */
function setClasses(){
	$("table#reminders-table tr").each(function() {
		$("td", this).each(function(j) {
			switch(j){
				case 0:
					this.setAttribute('class', 'reminder-id')
					break;
				case 1:
					this.setAttribute('class', 'end_date')
					break;
				case 2:
					this.setAttribute('class', 'timer')
					break;
				case 3:
					this.setAttribute('class', 'text')
					break;
				case 4:
					this.setAttribute('class', 'posted')
					break;
				case 5:
					this.setAttribute('class', 'btn w-100')
					this.setAttribute('data-toggle', 'dropdown')
					break;
			}
		});
	});
}

// get all reminders
function resetFilters(){
	$.post('/ui/reminder/filter', updateTable, 'json')
}

let rowDataBeforeEdit = { end_date:'', timer:'', text:'', posted:''}	// needed for saving row state in case of canceling
function editReminder(eventObject){
	// get index of row on which event was called
	// path: a -> dropdown-menu -> td -> tr
	let index = eventObject.parentElement.parentElement.parentElement.attributes[0].value
	// make cells editable and remember their content
	for(const name of ['end_date', 'timer', 'text', 'posted']){
		let elem = $('.'+name)[index]
		elem.setAttribute('contentEditable', 'true')
		rowDataBeforeEdit[name] = elem.textContent
	}
	// change dropdown menu to save and cancel
	$('.menu')[index].innerHTML = "<a class=\"ml-3 mr-2\" href=\"#\" onclick=\"save(this)\">Save</a> " +
									"<a class=\"mx-1\">or</a> " +
									"<a class=\"mr-3 ml-2\" href=\"#\" onclick=\"cancel(this)\">Cancel</a>"
	let row = $('table#reminders-table tr')[parseInt(index)+1]
	row.classList.add('table-danger')	// change the color of the row
	// show the truncated part of row
	$(row.cells).each(function(){
		this.style.overflow = 'visible'
		this.style.whiteSpace = 'unset'
	})
}

// give cells their original text
function cancel(eventObject) {
	let index = eventObject.parentElement.parentElement.parentElement.attributes[0].value
	for(const name of ['end_date', 'timer', 'text', 'posted']){
		$('.'+name)[index].textContent = rowDataBeforeEdit[name]
	}
	finishEditing(index)
}

// get new content of cells and post request to update database
function save(eventObject){
	let index = eventObject.parentElement.parentElement.parentElement.attributes[0].value
	let id = $('.reminder-id')[index].textContent
	let endDate = $('.end_date')[index].textContent
	let timer = $('.timer')[index].textContent
	let text = $('.text')[index].textContent
	let posted = $('.posted')[index].textContent
	// if there were no changes don't save
	if(rowDataBeforeEdit['end_date'] !== endDate || rowDataBeforeEdit['timer'] !== timer || rowDataBeforeEdit['text'] !== text || rowDataBeforeEdit['posted'] !== posted) {
		$.ajax({
			url: '/ui/reminder/save?id=' + id + '&end_date=' + endDate + "&timer=" + timer + "&text=" + text + "&posted=" + posted,
			method: 'POST',
			statusCode: {
				200: finishEditing(index),
				400: function () {
					alert("Timer must be a positive number representing time in seconds or in format days:hours:minutes:seconds!")
					cancel(eventObject)
				},
				500: function () {
					alert("There was a problem while updating reminder. We apologise.")
					cancel(eventObject)
				}
			}
		})
	} else {
		finishEditing(index)
	}
}


function finishEditing(index){
	// make cells not editable again
	for(const n of ['end_date', 'timer', 'text', 'posted']){
		$('.'+n)[index].setAttribute('contentEditable', 'false')
	}
	// make dropdown menu options edit or delete again
	$('.menu')[index].innerHTML = "<a class=\"ml-3 mr-2\" href=\"#\" onclick=\"editReminder(this)\">Edit</a> " +
								"<a class=\"mx-1\">or</a> " +
								"<a class=\"mr-3 ml-2\" href=\"#\" onclick=\"deleteReminder(this)\">Delete</a>"
	let row = $('table#reminders-table tr')[parseInt(index)+1]
	row.classList.remove('table-danger')	// change the color back
	// hide back the truncated part of row
	$(row.cells).each(function(){
		this.style.overflow = 'hidden'
		this.style.whiteSpace = 'nowrap'
		this.style.cssText = "tr > td:hover { overflow: visible; white-space: unset; }"
	})
}

// send a post request to delete a reminder with given id
function deleteReminder(eventObject){
	let index = eventObject.parentElement.parentElement.parentElement.attributes[0].value
	let id = $('.reminder-id')[index].textContent
	$.ajax({
			url: '/ui/reminder/delete?id=' + id,
			method: 'POST',
			statusCode: {
				200: function(){
					$('#reminders-table').bootstrapTable('remove', {field: 'id', values: id})	// remove row from table
					setClasses()
				},
				500: function () {
					alert("There was a problem while deleting reminder. We apologise.")
				}
			}
		})
}

/*
sorter for countdown column
needed because a and b are strings but need to be sorted like dates
form : (<number> days, )<number>:<number>:<number>
		part in brackets optional
*/
function countdownSorter(a,b){
	let parsedDateA = a.replace(' days, ', ':').split(':')
	// if there are 4 elements contains days
	let dateA = parsedDateA.length === 4 ?
		new Date(0,0,parseInt(parsedDateA[0]), parseInt(parsedDateA[1]), parseInt(parsedDateA[2]), parseInt(parsedDateA[3])) :
		new Date(0,0,0, parseInt(parsedDateA[0]), parseInt(parsedDateA[1]), parseInt(parsedDateA[2]))

	let parsedDateB = b.replace(' days, ', ':').split(':')
	let dateB = parsedDateB.length === 4 ?
		new Date(0,0,parseInt(parsedDateB[0]), parseInt(parsedDateB[1]), parseInt(parsedDateB[2]), parseInt(parsedDateB[3])) :
		new Date(0,0,0, parseInt(parsedDateB[0]), parseInt(parsedDateB[1]), parseInt(parsedDateB[2]))
	if(dateA < dateB) return -1
	else if(dateA > dateB) return 1
	else return 0
}