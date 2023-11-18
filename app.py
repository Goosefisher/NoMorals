from flask import Flask, render_template, request
from pydub import AudioSegment
import ffmpeg

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    audio_data = request.files['audio_data']

    # Process the audio file as needed
    # For example, save it to disk
    input_path = 'uploaded_audio.wav'
    output_path = 'processed_audio.wav'

    audio_data.save(input_path)

    # Convert the audio to PCM WAV format using ffmpeg
    convert_to_pcm_wav(input_path, output_path)

    # Redirect the user to a new page or display a message
    return "Audio received and processed."

def convert_to_pcm_wav(input_path, output_path):
    ffmpeg.input(input_path).output(output_path, acodec='pcm_s16le', ar=16000).run()

if __name__ == '__main__':
    app.run(debug=True)
