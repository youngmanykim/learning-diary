from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/diary')
def diary():
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template('diary.html', today=today)

if __name__ == '__main__':
    app.run(debug=True)
