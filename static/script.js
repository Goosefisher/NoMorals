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

    if (document.getElementById('easy')) {
        document.getElementById('easy').addEventListener('click', function() {
            document.getElementById('easyForm').submit();
        })
        document.getElementById('medium').addEventListener('click', function () {
            document.getElementById('mediumForm').submit();
        });
        document.getElementById('hard').addEventListener('click', function () {
            document.getElementById('hardForm').submit();
        });
    }

    if (document.getElementById('start-recording')) {
        let startRecordingButton = document.getElementById('start-recording');
        let stopRecordingButton = document.getElementById('stop-recording');
        let uploadButton = document.getElementById('analyse');
        // let audioPlayer = document.getElementById('audio-player');

        let mediaRecorder;
        let audioChunks = [];

        startRecordingButton.addEventListener('click', () => {
            startRecordingButton.disabled = true;
            stopRecordingButton.disabled = false;

            navigator.mediaDevices.getUserMedia({ audio: true })
                .then((stream) => {
                    mediaRecorder = new MediaRecorder(stream);

                    mediaRecorder.ondataavailable = (event) => {
                        if (event.data.size > 0) {
                            audioChunks.push(event.data);
                        }
                    };

                    mediaRecorder.onstop = () => {
                        let blob = new Blob(audioChunks, { type: 'audio/wav' });
                        let audioUrl = URL.createObjectURL(blob);
                        // audioPlayer.src = audioUrl;
                        // audioPlayer.play();
                        uploadButton.disabled = false;
                    };

                    mediaRecorder.start();
                })
                .catch((err) => console.error('Error accessing microphone', err));
        });

        stopRecordingButton.addEventListener('click', () => {
            startRecordingButton.disabled = false;
            stopRecordingButton.disabled = true;

            mediaRecorder.stop();
        });

        uploadButton.addEventListener('click', () => {
            let formData = new FormData();
            formData.append('audio_data', new Blob(audioChunks, { type: 'audio/wav' }), 'recording.wav');

            fetch('/recording', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(message => console.log(message))
            .then(response => {
                window.location.href = '/scoring'; // Redirect to the scoring route
            })
            .catch(error => console.error('Error uploading audio', error));
        })
    }
});
