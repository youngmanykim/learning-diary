from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json

app = Flask(__name__)

# Fake GPT response and news articles for demonstration
def fake_gpt_response(questions, keywords, tomorrow_tasks):
    responses = {
        "answers": [f"Answer to {question}" for question in questions],
        "news": [f"News article related to {keyword}" for keyword in keywords],
        "advice": [f"Advice for {task}" for task in tomorrow_tasks]
    }
    return responses

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

@app.route('/smart_summary', methods=['POST'])
def smart_summary():
    questions = request.form.getlist('questions')
    keywords = request.form.getlist('keywords')
    tomorrow_tasks = request.form.getlist('tomorrow')

    responses = fake_gpt_response(questions, keywords, tomorrow_tasks)

    return render_template('smart_summary.html', questions=questions, keywords=keywords, tomorrow_tasks=tomorrow_tasks, responses=responses)

@app.route('/save_summary', methods=['POST'])
def save_summary():
    data = {
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'tasks': request.form.getlist('tasks'),
        'learned': request.form.getlist('learned'),
        'questions': request.form.getlist('questions'),
        'questions_responses': request.form.getlist('questions_responses'),
        'keywords': request.form.getlist('keywords'),
        'news_responses': request.form.getlist('news_responses'),
        'tomorrow': request.form.getlist('tomorrow'),
        'advice_responses': request.form.getlist('advice_responses')
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

if __name__ == '__main__':
    app.run(debug=True)
