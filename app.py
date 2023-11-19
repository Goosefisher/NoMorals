from flask import Flask, render_template, request, redirect, url_for, session
import speech_recognition as sr
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import subprocess
import os

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

# Final generated text
final_text = ""
all_generated_texts = []

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
    input_level = session['input_level']
    print(input_level)

    # Query model
    generated_text = generate_speech_text(input_level)
    print("Generated Text: ", generated_text)
    all_generated_texts.append(generated_text)

    # Process the audio file as needed
    # For example, save it to disk
    input_path = 'uploaded.wav'
    output_path = 'converted.wav'

    audio_file_exists = False
    transcript = ""

    # Collect audio from browser and save generated_text as final_text
    if 'audio_data' in request.files:
        audio_data = request.files['audio_data']
        audio_data.save(input_path)
        audio_file_exists = True
        print("Saved audio file")
        # Convert the audio to PCM WAV format using ffmpeg
        # convert_to_pcm_wav(input_path, output_path)
    else: 
        print("No 'audio_data' file found in the request")

    # Received data
    if audio_file_exists:
        print("Audio exists! Now transcribing...")
        # sound = wave.open(output_path, 'rb')
        success = convert_to_wav(input_path, output_path)

        if success:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(output_path)
            with audioFile as source:
                data = recognizer.record(source)
                transcript = recognizer.recognize_google(data, key=None)
            # Delete file
            os.remove(output_path)

            # Print out original passage and then transcript
            print("Original passage: ", all_generated_texts[0])
            print("Transcript: ", transcript)
        else:
            print("Cannot transcribe, wrong format")
    else:
        print("Cannot transcribe, audio file doesn't exist")

    # Redirect the user to a new page or display a message
    return render_template('read.html', transcript=transcript, 
                           generated_text=generated_text)

def generate_speech_text(input_level):
    prompt_level = ""

    # Generate text
    print("I am going to generate text with ", input_level)
    chat_model = OpenAI(openai_api_key=OPENAI_API_KEY)
    print(chat_model)

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

    if result != "":
        return str(result)
    else:
        return "No text found"

def convert_to_wav(input_path, output_path):
    print("Beginning function convert_to_wav")

    try:
        print("Creating command")
        command = [
            'ffmpeg',
            '-i', input_path,
            '-acodec', 'pcm_s16le',
            '-ar', '44100',
            output_path
        ]
        print(command)
        # subprocess.run(command, check=True)
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("function converted file")
        print("Conversion completed")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while converting file: {e}")
        return False
    return True

if __name__ == '__main__':
    app.run(debug=True)