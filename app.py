from flask import Flask, render_template

app = Flask(name)

@app.route('/')
def home():
    return render_template('index.html', message='Hello, Flask!')

if name == 'main':
    app.run(debug=True)