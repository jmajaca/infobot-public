
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
	$('#reminders-table').bootstrapTable('load', data)
}

function resetFilters(){
	$.post('/ui/reminder/filter', updateTable, 'json')
}