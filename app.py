from flask import Flask, render_template, request, SQLalchemy

app = Flask(__name__)
db = SQLalchemy("sqlite:///score.db")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/name', methods=['GET', 'POST'])
def name():
    if request.method == 'POST':
        name = request.form.get('name')
        user = db.execute()
    return render_template('name.html')

@app.route('/scoring', methods=['POST'])
def score():
    text = request.form.get('text')
    transcript = request.form.get('transcript')


if __name__ == '__main__':
    app.run(debug=True)