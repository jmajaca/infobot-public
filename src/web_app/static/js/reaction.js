function hideReactionProcessElements() {
    $('#reaction-scan-spinner').toggle();
    $('#reaction-scan-error').hide();
    $('#reaction-scan-success').hide();
}

$(document).ready(function(){
    hideReactionProcessElements();
});

function startReactionScan() {
    hideReactionProcessElements();
    $.ajax({
        url: '/ui/reaction/scan',
        type: 'get',
        statusCode: {
            200: function () {
                $('#reaction-scan-spinner').toggle();
                $('#reaction-scan-success').show();
            },
            500: function () {
                $('#reaction-scan-spinner').toggle();
                $('#reaction-scan-error').show();
            }
        }
    })
}

function saveNewTime() {
    $.ajax({
        url: '/ui/reaction/time',
        type: 'post',
        data: { time: $('#time_picker').val()},
        contentType: 'application/json;charset=UTF-8'
    });
}

$(document).ready(function() {
    setInterval(function(){
        $.getJSON('/ui/reaction/automatic', function (data) {
            if (data.status === '1') {

            } else if (data.status === '0' && $('#scan-toggle').is(':checked')) {
                location.reload();
            }
        });
    },10000)
});

function toggleAutomaticReactionScan() {
    $.ajax({
        url: '/ui/reaction/automatic/flip',
        type: 'get'
    });
}