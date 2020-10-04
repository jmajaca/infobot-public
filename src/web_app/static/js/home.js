window.setInterval(function(){
    processNewData();
}, 500);

function processNewData() {
    let reload = localStorage.getItem('reload');
    const data = localStorage.getItem('data').split(',');
    $('#progress-bar').css('width', data[0]+'%').attr('aria-valuenow', data[0]);
    $('#progress-bar-label').text(data[0]+'%');
    $('#progress-bar-action').text(data[1])

    if(data[2] === 'error' && localStorage.getItem('error') === '0') {
        console.log(reload)
        localStorage.setItem('error', '1')
        location.reload();
    } else if (data[2] === 'normal') {
        localStorage.setItem('error', '0')
        $('#progress-bar').show()
        $('#progress-bar-error').hide()
    }
}

$(document).on("click", ".error-trace", function () {
    var trace = $(this).data('id');
    var uuid = $(this).data('uuid')
    $("#showTrace").val( trace );
    $("#exampleModalLabel").text('Trace log ' + uuid)
});

// F5
$(document).ready(function(){
    setTimeout(function () {
        $('#progress-placeholder').remove()
        $('#progress').removeClass('hidden-bar')
    }, 0);
    var data = localStorage.getItem('data').split(',');
    if(localStorage.getItem("error")==="1") {
        // localStorage.removeItem("error");
        $('#progress-bar').hide()
        $('#progress-bar-error').show()
        $('#progress-bar-action').text(data[1])
    } else if (localStorage.getItem("error")==="0") {
        // localStorage.removeItem("error");
        $('#progress-bar').css('width', data[0]+'%').attr('aria-valuenow', data[0]);
        $('#progress-bar-label').text(data[0]+'%');
        $('#progress-bar-action').text(data[1])

        $('#progress-bar').show()
        $('#progress-bar-error').hide()
    }
});

// start stop buttons
function start() {
    localStorage.setItem('error', '0');
    $.get("/ui/home/scraper/start", function(data){},"json");
}

function stop() {
    let response = confirm("Are you sure you want to forcefully stop the Scraper?");
    if(response) {
        $.get("/ui/home/scraper/stop", function(data){},"json");
    }
}