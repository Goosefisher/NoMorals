document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('home')) {
        document.addEventListener('click', function() {
            window.location.href = '/level';
        });
    }

    if (document.getElementById('restart')) {
        document.getElementById('restart').addEventListener('click', function() {
            window.location.href = "/level";
        })
    }

    if (document.getElementById('analyse')) {
        document.getElementById('analyse').addEventListener('click', function() {
            window.location.href = "/scoring";
        })
    }
})