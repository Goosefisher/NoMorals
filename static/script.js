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
        });
    }

    if (document.getElementById('start')) {
        const startButt = document.getElementById('start');
        const stopButt = document.getElementById('stop');
        const audioPlayer = document.getElementById('audioPlay')
        let mediaRecorder;
        let recorded = [];

        startButt.addEventListener('click', async() => {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
            
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondatavailabe = event => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                const blob = new Blob(recordedChunks, {type: 'audio/wav'});
                const url = URL.createObjectURL(blob);
                audioPlayer.src = url;
            };

            mediaRecorder.start();
            console.log('recording!');
        });

        stopButt.addEventListener('click', () => {
            mediaRecorder.stop();
            console.log('stopped!');
        });
    }
})