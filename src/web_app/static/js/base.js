// redirect logic

function home() {
    window.location.href = '/ui/home';
}
function course() {
    window.location.href = '/ui/course';
}
function reaction() {
    window.location.href = '/ui/reaction';
}
function reminder() {
    window.location.href = '/ui/reminder';
}


// spinner logic

const SCAN_URL = '/scan/';
let completeScanFlag = false;
const LAST_OPTION = 'reactions';
const OPTION_CLICKS = {'users': false, 'channels': false, 'reactions': false, 'complete': false};

$(document).ready(function(){
    completeScanFlag = false;
    const OPTIONS = ['users', 'channels', 'reactions', 'complete']
    OPTIONS.forEach(element => {
        $('#scan-' + element + '-spinner').toggle();
        $('#scan-' + element + '-error').hide();
        $('#scan-' + element + '-success').hide();
    })
});

function toggleSpinners(resource) {
    $('#scan-' + resource + '-spinner').toggle();
}

function scan(resource) {
    if (OPTION_CLICKS[resource] === true) return
    else OPTION_CLICKS[resource] = true
    toggleSpinners(resource);
    $.ajax({
        url  : SCAN_URL + resource,
        type : 'get',
        statusCode: {
            500: function () {
                toggleSpinners(resource);
                $('#scan-' + resource + '-error').show();
                if(completeScanFlag && resource === LAST_OPTION) {
                    toggleSpinners('complete');
                    $('#scan-complete-error').show();
                }
            },
            200: function () {
                toggleSpinners(resource);
                $('#scan-' + resource + '-success').show();
                if(completeScanFlag && resource === LAST_OPTION) {
                    toggleSpinners('complete');
                    $('#scan-complete-success').show();
                }
            }
        }
    });
}

function completeScan() {
    if (OPTION_CLICKS['complete'] === true) return
    else OPTION_CLICKS['complete'] = true
    completeScanFlag = true;
    $('#scan-complete-spinner').toggle();
    ['users', 'channels', 'reactions'].forEach(element => {
        scan(element);
    });
}


// bot status logic

$(document).ready(function(){
    $("#status-badges").delay(1000).fadeIn(500);
    hideStatuses();
    if (localStorage.getItem('error') === null) localStorage.setItem('error', '0');
});

function hideStatuses() {
    const STATUS = ['normal', 'error', 'warning', 'sleep', 'off'];
    STATUS.forEach(element => {
        $('#status-' + element).hide();
    });
}

window.setInterval(function(){
    let data = localStorage.getItem('data').split(',');
    hideStatuses();
    $('#status-' + data[2]).show().fadeIn(500);
}, 500);

let source = new EventSource("/scraper/progress");
source.onmessage = function (event) {
    localStorage.setItem('data', event.data);
}
