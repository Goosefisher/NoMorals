document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('home')) {
        document.getElementById('home').addEventListener('click', function () {
            window.location.href = '/level';
        });
    }

    if (document.getElementById('restart')) {
        document.getElementById('restart').addEventListener('click', function () {
            window.location.href = "/level";
        });
    }

    if (document.getElementById('analyse')) {
        document.getElementById('analyse').addEventListener('click', function () {
            window.location.href = "/scoring";
        });
    }

    if (document.getElementById('easy')) {
        document.getElementById('easy').addEventListener('click', function () {
            window.location.href = "/recording";
        });
    }

    if (document.getElementById('medium')) {
        document.getElementById('medium').addEventListener('click', function () {
            window.location.href = "/recording";
        });
    }

    if (document.getElementById('hard')) {
        document.getElementById('hard').addEventListener('click', function () {
            window.location.href = "/recording";
        });
    }
});
