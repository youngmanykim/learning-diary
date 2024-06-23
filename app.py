from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_entries():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_entries(entries):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)

entries = load_entries()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summary', methods=['GET', 'POST'])
def summary():
    if request.method == 'POST':
        entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'main_task': request.json.get('main-task', []),
            'learning': request.json.get('learning', []),
            'special_notes': request.json.get('special-notes', []),
            'tomorrow_task': request.json.get('tomorrow-task', [])
        }
        entries.append(entry)
        save_entries(entries)
        return redirect(url_for('history'))
    return render_template('summary.html', entries=entries)

@app.route('/history')
def history():
    return render_template('history.html', entries=entries)

@app.route('/entry/<int:index>')
def entry_detail(index):
    entry = entries[index]
    return render_template('entry_detail.html', entry=entry, index=index)

@app.route('/edit_entry/<int:index>', methods=['GET', 'POST'])
def edit_entry(index):
    entry = entries[index]
    if request.method == 'POST':
        entry['main_task'] = request.form.getlist('main-task')
        entry['learning'] = request.form.getlist('learning')
        entry['special_notes'] = request.form.getlist('special-notes')
        entry['tomorrow_task'] = request.form.getlist('tomorrow-task')
        entries[index] = entry
        save_entries(entries)
        return redirect(url_for('entry_detail', index=index))
    return render_template('edit_entry.html', entry=entry, index=index)

if __name__ == '__main__':
    app.run(debug=True)
