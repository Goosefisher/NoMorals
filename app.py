from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    audio_data = request.files['audio_data']
    # Process the audio file as needed
    # For example, save it to disk
    audio_data.save('uploaded_audio.wav')
    return "Audio received and processed."

if __name__ == '__main__':
    app.run(debug=True)


