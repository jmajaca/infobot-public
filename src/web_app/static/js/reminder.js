
function getFilters(){
	let course = $('#course').val()
	let author = $('#author').val()
	let from_date = $('#from').val()
	let to_date = $('#to').val()
	let posted = $('#check').is(':checked')
	$.post('/ui/reminder/filter?course=' + course + '&author=' + author + '&from=' + from_date + '&to=' + to_date + '&posted=' + posted, function(data){}, 'json')
}

function resetFilters(){
	$.get('/ui/reminder')
}