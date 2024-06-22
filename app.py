import os
from dotenv import load_dotenv
import openai
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json

app = Flask(__name__)

# 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# OpenAI API 호출 함수
def get_gpt_response(questions, keywords, tomorrow_tasks):
    responses = {
        "answers": [],
        "news": [],
        "advice": []
    }

    # 질문에 대한 답변
    for question in questions:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Q: {question}\nA:"}
            ]
        )
        responses["answers"].append(response.choices[0].message['content'].strip())

    # 키워드에 관련된 뉴스기사 (모의 데이터)
    for keyword in keywords:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Find three recent news articles related to {keyword}."}
            ]
        )
        responses["news"].append(response.choices[0].message['content'].strip())

    # 내일 할 일에 대한 조언
    for task in tomorrow_tasks:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Give me some advice for the task: {task}"}
            ]
        )
        responses["advice"].append(response.choices[0].message['content'].strip())

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
    tasks = request.form.getlist('task')
    learned = request.form.getlist('learned')
    questions = request.form.getlist('questions')
    keywords = request.form.getlist('keywords')
    tomorrow_tasks = request.form.getlist('tomorrow')

    responses = get_gpt_response(questions, keywords, tomorrow_tasks)

    return render_template('smart_summary.html', tasks=tasks, learned=learned, questions=questions, keywords=keywords, tomorrow_tasks=tomorrow_tasks, responses=responses)

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
