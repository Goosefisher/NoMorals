document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('home')) {
        document.addEventListener('click', function() {
            window.location.href = '/recording';
        });
    }

    if (document.getElementById('restart')) {
        document.getElementById('restart').addEventListener('click', function() {
            window.location.replace("/level.html");
        })
    }

    if (document.getElementById('analyse')) {
        document.getElementById('analyse').addEventListener('click', function() {
            window.location.href = "/scoring";
        })
    }
})