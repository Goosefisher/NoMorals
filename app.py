from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('templates/index.html', message='Hello, Flask!')

if __name__ == 'main':
    app.run(debug=True)