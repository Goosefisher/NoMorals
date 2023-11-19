from flask import Flask, render_template, request, redirect
from fuzzywuzzy import fuzz 
import string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/scoring', methods=['POST'])
def score():
    generated_text = request.form.get('generated_text').translate(str.maketrans('', '', string.punctuation)).lower()
    transcript = request.form.get('transcript').translate(str.maketrans('', '', string.punctuation)).lower() 
    gamemode = request.form.get('gamemode')

    score = fuzz.partial_ratio(transcript, generated_text)
    message = ""

    if 0 <= score and score < 50:
        message = "Better luck next time, Jelly Warrior!"
    elif score <= 80:
        message = "Not too shabby, Jelly Warrior!"
    else:
        message = "You're out of this world, Jelly Warrior!"

    return render_template('results.html', gamemode = gamemode, score = score, message = message)




@app.route('/recording')
def recording():
    return render_template('recording.html')

if __name__ == '__main__':
    app.run(debug=True)