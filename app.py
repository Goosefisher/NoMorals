# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# import pandas as pd

from flask import Flask, render_template, request, redirect
import speech_recognition as sr
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

OPENAI_API_KEY = "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"
PROMPT_TEMPLATE = "Generate a speech practice text, consisting of two\
    sentences, with themes related to jams, fruits, or breakfasts. For an\
        'easy' level, create sentences with straightforward words and clear\
            pronunciation. For a 'medium' level, introduce sentences with\
                slightly more complex words or phrases that require careful\
                    articulation. For the 'hard' level, include sentences with\
                        challenging sounds or tongue-twisters to test fluency.\
                            Ensure that each text can be read aloud in 20\
                                seconds or less, and maintain a casual\
                                    and creative style. You will now generate\
                                        a {{level}} text"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_text = ""
    transcript = ""
    level = ""

    # Received data
    if request.method == "POST":
        # Render buttons
        if request.form.get('easy') == 'Easy':
            level = 'easy'
        elif request.form.get('medium') == "Medium":
            level = 'medium'
        elif request.form.get('hard') == "Hard":
            level = 'hard'

        print(request.form)

        # Query model
        generated_text = generate_speech_text('hard')
        print(generated_text)

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

    elif request.method == 'GET':
        return render_template('index.html', transcript=transcript, 
                           generated_text=generated_text)
    
    return render_template('index.html', transcript=transcript, 
                           generated_text=generated_text)

def generate_speech_text(input_level):
    # Generate text
    chat_model = OpenAI(openai_api_key=OPENAI_API_KEY)
    prompt = str(PromptTemplate.from_template(PROMPT_TEMPLATE.format(level=input_level)))
    result = chat_model.predict(prompt)

    if result != "":
        return str(result)
    else:
        return "No text found"

if __name__ == "__main__":
    app.run(debug=True, threaded=True)