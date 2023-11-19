document.addEventListener('DOMContentLoaded', function() {

    /*document.getElementById('test').addEventListener('click', function() {
        let form = document.createElement('form');
        form.setAttribute('method', 'post');
        form.setAttribution('action', 'submit');

        document.getElementsByTagName("body").appendChild(form);

        let nameTag = document.createElement('label');
        let name = document.createElement("input");
        name.setAttribute("placeholder", "Enter Your Name");
        nameTag.innerHTML = "Name";
        name.appendChild(nameTag);

        let btnTag = document.createElement('label');
        let submitButt = document.createElement('button');
        btnTag.innerHTML = "Submit";
        submitBtn.appendChild(btnTag);

        form.appendChild(name);
        form.appendChild(submitButt);
    }) */

    if (document.getElementById('home')) {
        document.addEventListener('click', function() {
            console.log('event');
            window.location.href = '/recording';
        });
            // Redirect to the /redirect route when the document is clicked
    }
})