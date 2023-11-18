document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('test').addEventListener('click', function() {
        let form = document.createElement('form');
        form.setAttribute('method', 'post');
        form.setAttribution('action', 'submit');

        document.getElementsByTagName("body").appendChild(form);
    })
})