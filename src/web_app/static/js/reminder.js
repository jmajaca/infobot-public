
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
					this.setAttribute('class', 'end_date')
					break;
				case 1:
					this.setAttribute('class', 'timer')
					break;
				case 2:
					this.setAttribute('class', 'text')
					break;
				case 3:
					this.setAttribute('class', 'posted')
					break;
				case 4:
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
		let elem = $('.'+name)[index]
		elem.setAttribute('contentEditable', 'true')
		rowDataBeforeEdit[name] = elem.textContent
	}
	$('.menu')[index].innerHTML = "<a class=\"ml-3 mr-2\" href=\"#\" onclick=\"save(this)\">Save</a> " +
									"<a class=\"mx-1\">or</a> " +
									"<a class=\"mr-3 ml-2\" href=\"#\" onclick=\"cancel(this)\">Cancel</a>"
	let row = $('table#reminders-table tr')[parseInt(index)+1]
	row.classList.add('table-danger')
	// show the truncated part of row
	$(row.cells).each(function(){
		this.style.overflow = 'visible'
		this.style.whiteSpace = 'unset'
	})
}

function cancel(eventObject) {
	let index = eventObject.parentElement.parentElement.parentElement.attributes[0].value
	for(const name of ['end_date', 'timer', 'text', 'posted']){
		$('.'+name)[index].textContent = rowDataBeforeEdit[name]
	}
	finishEditing(index)
}

function save(eventObject){
	let index = eventObject.parentElement.parentElement.parentElement.attributes[0].value
	let endDate = $('.end_date')[index].textContent
	let timer = $('.timer')[index].textContent
	let text = $('.text')[index].textContent
	let posted = $('.posted')[index].textContent
	// if there were no changes don't save
	if(rowDataBeforeEdit['end_date'] !== endDate || rowDataBeforeEdit['timer'] !== timer || rowDataBeforeEdit['text'] !== text || rowDataBeforeEdit['posted'] !== posted){
		$.post('/ui/reminder/save?end_date=' + endDate + "timer=" + timer + "text=" + text + "posted=" + posted, function res(data){}, 'json')
	}
	finishEditing(index)
}

function finishEditing(index){
	for(const n of ['end_date', 'timer', 'text', 'posted']){
		$('.'+n)[index].setAttribute('contentEditable', 'false')
	}
	$('.menu')[index].innerHTML = "<a class=\"ml-3 mr-2\" href=\"#\" onclick=\"editReminder(this)\">Edit</a> " +
								"<a class=\"mx-1\">or</a> " +
								"<a class=\"mr-3 ml-2\" href=\"#\" onclick=\"deleteReminder(this)\">Delete</a>"
	let row = $('table#reminders-table tr')[parseInt(index)+1]
	row.classList.remove('table-danger')
	// hide back the truncated part of row
	$(row.cells).each(function(){
		this.style.overflow = 'hidden'
		this.style.whiteSpace = 'nowrap'
		this.style.cssText = "tr > td:hover { overflow: visible; white-space: unset; }"
	})
}

function deleteReminder(){

}