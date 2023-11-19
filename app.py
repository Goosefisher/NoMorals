# @app.route('/scoring')
# def score():
#     generated_text = "Grapse" #request.form.get('generated_text').translate(str.maketrans('', '', string.punctuation)).lower()
#     transcript = "Grapes" #request.form.get('transcript').translate(str.maketrans('', '', string.punctuation)).lower() 
#     gamemode = "medium" #request.form.get('gamemode')

#     score = fuzz.partial_ratio(transcript, generated_text)
# =======
from flask import Flask, render_template, request, redirect, url_for, session
import speech_recognition as sr
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import subprocess
import os
from fuzzywuzzy import fuzz
import string
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

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
        return render_template('level.html')

@app.route('/read', methods=['GET', 'POST'])
def read():
    input_level = session['input_level']
    print(input_level)

    # Query model
    # generated_text = generate_speech_text(input_level)
    generated_text = "Breakfast is the most important meal of the day so why not start off with a delicious homemade spread"
    # generated_text = generated_text.strip('\"\"')
    print("Generated Text: ", generated_text)
    all_generated_texts.append(generated_text)

    # Process the audio file as needed
    # For example, save it to disk
    input_path = 'uploaded.wav'
    output_path = 'converted_file.wav'

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
                # os.remove(output_path)
                print("Deleted OS")

            # Print out original passage and then transcript
            print("Original passage: ", all_generated_texts[0])
            session['generated_text'] = all_generated_texts[0]
            print("Transcript: ", transcript)
            session['transcript'] = transcript
            print("Level: ", session['input_level'])
            return redirect(url_for('score'))
        else:
            print("Cannot transcribe, wrong format")
    else:
        print("Cannot transcribe, audio file doesn't exist")

    # Redirect the user to a new page or display a message
    return render_template('recording.html', transcript=transcript, 
                           generated_text=generated_text)

@app.route('/scoring', methods=['GET','POST'])
def score():
    generated_text = session['generated_text'].translate(str.maketrans('', '', string.punctuation)).lower()
    transcript = session['transcript'].translate(str.maketrans('', '', string.punctuation)).lower() 
    gamemode = session['input_level'].translate(str.maketrans('', '', string.punctuation)).lower() 

    score = fuzz.ratio(transcript, generated_text)
    print(score)

    message = ""

    if 0 <= score and score < 50:
        message = "Better luck next time, Jelly Warrior!"
    elif score <= 80:
        message = "Not too shabby, Jelly Warrior!"
    else:
        message = "You're out of this world, Jelly Warrior!"

#     return render_template('results.html', gamemode = gamemode, score = score, message = message)

# @app.route('/recording', methods = ['GET'])
# def recording():
#     return render_template('recording.html')
# =======
    print(message)

    # Generate diff between two strings
    strings_diff = compare_strings(transcript, generated_text)

    generic_x_list, generic_y_list = create_horizontal_function(strings_diff)
    plt.plot(generic_x_list, generic_y_list, marker='o', linestyle='', 
             color='purple')

    discontinuity_list = find_discontinuity_points(strings_diff)

    for point in discontinuity_list:
        plt.scatter(*point, color='red', marker='x', s=100)

    plt.xlabel('Words you said')
    plt.ylabel('Correct or incorrect')
    plt.title('How well did you jam in this level?')

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the plot image as base64
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    if request.method == "POST":
        if "restart" in request.form:
            # User wants to restart
            return redirect(url_for('level'))

    # return render_template('results.html', gamemode = gamemode, score = score,
    #                        message = message, strings_diff=strings_diff)
    return render_template('results.html', gamemode = gamemode, score = score,
                           message = message, strings_diff = strings_diff, 
                           plot_url=plot_url)

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

def create_horizontal_function(strings_diff):
    x_list = []
    y_list = []

    strings_list = strings_diff.split(" ")

    # x-coordinates are a counter of the number of words in generated_text
    for i in range(len(strings_list)):
        if not '*' in strings_list[i]:
            x_list.append(i + 1) 
            y_list.append(1)

    return x_list, y_list

def find_discontinuity_points(strings_diff):
    discontinuity_list = []
    strings_list = strings_diff.split(" ")

    for index, word in enumerate(strings_list):
        print("strings list", strings_list)
        if '*' in word:
            discontinuity_list.append((index + 1, 1))
    
    print("discontinuity list", discontinuity_list)
    return discontinuity_list

def compare_strings(transcript, generated_text):
    transcript_list = transcript.split(" ")
    generated_text_list = generated_text.split(" ")
    output_list = []

    for word in generated_text_list:
        if word in transcript_list:
            output_list.append(word)
        else:
            output_list.append('*' + word + '*')

    output_list_string = " ".join(output_list)
    print(output_list_string)
    return output_list_string

if __name__ == '__main__':
    app.run(debug=True)