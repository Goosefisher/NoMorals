from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recording')
def recording():
    return render_template('recording.html')


if __name__ == '__main__':
    app.run(debug=True)
