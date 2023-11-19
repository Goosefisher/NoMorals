document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('home')) {
            document.addEventListener('click', function () {
                console.log('event');
                window.location.href = '/recording';
            });
            // Redirect to the /redirect route when the document is clicked
        }


    if (document.getElementById('restart')) {
        document.getElementById('restart').addEventListener('click', function () {
            window.location.replace("/level.html");
        })
    }

})