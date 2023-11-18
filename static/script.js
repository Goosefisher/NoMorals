document.addEventListener('DOMContentLoaded', function() {
    
    if (document.getElementById('test')) {
        document.querySelector('#test').addEventListener('click', function() {
            let form = document.createElement('form');
            form.setAttribute('method', 'post');
            form.setAttribute('action', 'submit');
        
            document.getElementsByTagName("body")[0].appendChild(form);
        
            let nameTag = document.createElement('label');
            let name = document.createElement("input");
            name.setAttribute("placeholder", "Enter Your Name");
            nameTag.innerHTML = "Name";
            
        
            let buttTag = document.createElement('label');
            let submitButt = document.createElement('button');
            buttTag.innerHTML = "Submit";

            name.appendChild(nameTag);
            submitButt.appendChild(buttTag);
        
            form.appendChild(name);
            form.appendChild(submitButt);
        })
    }

    if (document.getElementById('start')) {
        const startButt = document.getElementById('start');
        const stopButt = document.getElementById('stop');

        startButt.addEventListener('click', async() => {

        })

        
    }
})