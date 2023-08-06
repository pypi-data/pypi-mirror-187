const today = new Date();

function go_back() {
    window.history.back();
}

function go_forward() {
    window.history.forward();
}

function refresh() {
    window.location.reload();
}

function getKeyValue(val) {
    let display = document.getElementById('display');
    display.value += val
}

function addNumber(element, displayID) {
    const display = document.getElementById(displayID);
    display.classList.add('keypad-display');
    display.value = display.value + element.value;
    // document.getElementById('keypadVar').value = document.getElementById('keypadVar').value + element.value;
}

function currentDate() {
    const year = today.getFullYear();
    const month = today.toLocaleString('default', {month: "long"});
    const day = today.toLocaleString('default', {day: "2-digit"});

    document.getElementById('date').innerText = month + " " + day + " " + year;
}

function currentTime() {
    function updateTime(time) {
        if (time < 10) {
            return "0" + time;
        } else {
            return time;
        }
    }

    let hour = updateTime(today.getHours());
    let min = updateTime(today.getMinutes());

    let mid_day = (hour >= 12) ? "PM" : "AM";
    hour = (hour === 0) ? 12 : ((hour > 12) ? (hour - 12) : hour);

    document.getElementById('time').innerText = hour + ":" + min + " " + mid_day;

    const t = setTimeout(function () {
        currentTime();
    }, 1000);
}

function clearMessage() {
    // Remove the message after 5 seconds
    setTimeout(function () {
        document.getElementById('message').remove();
    }, 3000);
}

function reloadPage() {
// The last "domLoading" Time //
    var currentDocumentTimestamp =
        new Date(performance.timing.domLoading).getTime();
// Current Time //
    var now = Date.now();
// Ten Seconds //
    var tenSec = 10 * 1000;
// Plus Ten Seconds //
    var plusTenSec = currentDocumentTimestamp + tenSec;
    if (now > plusTenSec) {
        location.reload();
    } else {
    }
}

// REload all css files
function reloadCssFiles() {
    var queryString = '?reload=' + new Date().getTime();
    $('link[rel="stylesheet"]').each(function () {
        this.href = this.href.replace(/\?.*|$/, queryString);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    M.AutoInit();
    // var elems = document.querySelectorAll('.datepicker');
    // max_date = new Date();
    // max_date.setDate(max_date.getDate() + 1);
    // var instances = M.Datepicker.init(elems, {
    //     maxDate: new Date(today.getFullYear(), today.getMonth(), today.getDate()),
    //     yearRange: [today.getFullYear() - 125, today.getFullYear() - 15],
    // });
    //
    // var paymentBtn = document.getElementById('paymentBtn');
    // var paymentBtnInstance = M.FloatingActionButton.init(paymentBtn, {
    //     direction: 'left',
    //     hoverEnabled: false
    // });
    currentTime();
    currentDate();
    clearMessage();
})
