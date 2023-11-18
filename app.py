from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record', methods=['GET', 'POST'])
def record():
    recorded = False

    if request.method == 'POST':
        recording = request.form.get('recording')
    
    return render_template('record.html', )

if __name__ == '__main__':
    app.run(debug=True)