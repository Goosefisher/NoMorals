from flask import Flask, render_template, request, redirect, url_for, session
import speech_recognition as sr
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from pydub import AudioSegment
import ffmpeg

OPENAI_API_KEY = "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"

# Prompts
BEGIN_PROMPT = "Write a speech practice text, consisting of two\
    sentences, with themes related to jams, fruits, or breakfasts. "
EASY_TEMPLATE = "Create 2 sentences with straightforward words and\
    clear pronunciation. "
MEDIUM_TEMPLATE = "Introduce sentences with slightly more complex words or\
    phrases that require careful articulation. "
HARD_TEMPLATE = "Include sentences with challenging sounds or tongue-twisters\
    to test fluency. "
END_PROMPT = "Your writing should be able to be read aloud in 20 seconds or less,\
    and maintain a casual and creative style. Your writing: "

# Levels
EASY = 'easy'
MEDIUM = 'medium'
HARD = 'hard'

app = Flask(__name__)
app.secret_key = "JellyJabber"

@app.route('/', methods=['GET', 'POST'])
@app.route('/level', methods=['GET', 'POST'])
def level():
    input_level = ""
    # Received data
    if request.method == "POST":
        # Render buttons
        if request.form.get(EASY) == 'Easy':
            input_level = EASY
        elif request.form.get(MEDIUM) == "Medium":
            input_level = MEDIUM
        elif request.form.get(HARD) == "Hard":
            input_level = HARD

        # Store value in variable
        print(input_level)
        session['input_level'] = input_level
        print("Session level:", session['input_level'])

        return redirect(url_for('read'))
    else:
        return render_template('index.html')

@app.route('/read', methods=['GET', 'POST'])
def read():
    generated_text = ""
    transcript = ""
    input_level = session['input_level']
    print(input_level)

    # Query model
    generated_text = generate_speech_text(input_level)
    print(generated_text)

    # Received data
    if request.method == "POST":

        # Failsafes in case files not found
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        
        # Initialize recognizer if file exists; create audio file object
        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)
    
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

    return render_template('read.html', transcript=transcript, 
                           generated_text=generated_text)

def generate_speech_text(input_level):
    prompt_level = ""

    # Generate text
    print("I am going to generate text with ", input_level)
    chat_model = OpenAI(openai_api_key=OPENAI_API_KEY)

    if input_level == HARD:
        prompt_level = HARD_TEMPLATE
    elif input_level == MEDIUM:
        prompt_level = MEDIUM_TEMPLATE
    else:
        prompt_level = EASY

    prompt = str(PromptTemplate.from_template(BEGIN_PROMPT + prompt_level + 
                                              END_PROMPT))
    print(prompt)
    result = chat_model.predict(prompt)

def convert_to_pcm_wav(input_path, output_path):
    ffmpeg.input(input_path).output(output_path, acodec='pcm_s16le', ar=16000).run()

if __name__ == '__main__':
    app.run(debug=True)
