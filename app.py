from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json

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

@app.route('/history')
def history():
    try:
        with open('history.json', 'r') as f:
            history_data = json.load(f)
    except FileNotFoundError:
        history_data = []
    return render_template('history.html', history=history_data)

@app.route('/save', methods=['POST'])
def save():
    data = {
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'tasks': request.form.getlist('task'),
        'learned': request.form.getlist('learned'),
        'questions': request.form.getlist('questions'),
        'keywords': request.form.getlist('keywords'),
        'tomorrow': request.form.getlist('tomorrow')
    }

    try:
        with open('history.json', 'r') as f:
            history_data = json.load(f)
    except FileNotFoundError:
        history_data = []

    history_data.append(data)

    with open('history.json', 'w') as f:
        json.dump(history_data, f, indent=4)

    return redirect(url_for('history'))

@app.route('/entry/<int:entry_id>')
def entry(entry_id):
    try:
        with open('history.json', 'r') as f:
            history_data = json.load(f)
    except FileNotFoundError:
        return "No entries found."

    if entry_id >= len(history_data):
        return "Entry not found."

    entry_data = history_data[entry_id]
    return render_template('entry.html', entry=entry_data)

if __name__ == '__main__':
    app.run(debug=True)
