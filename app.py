from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json
import os
import pytz

app = Flask(__name__)

DATA_FILE = 'data.json'
STATS_FILE = 'stats.json'
UPDATES_FILE = 'updates.json'

def load_entries():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_entries(entries):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'visit_count': 0, 'interaction_count': 0}

def save_stats(stats):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=4)

def load_updates():
    if os.path.exists(UPDATES_FILE):
        with open(UPDATES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_updates(updates):
    with open(UPDATES_FILE, 'w', encoding='utf-8') as f:
        json.dump(updates, f, ensure_ascii=False, indent=4)

entries = load_entries()
stats = load_stats()
updates = load_updates()

@app.route('/')
def home():
    stats['visit_count'] += 1
    save_stats(stats)
    return render_template('index.html', visit_count=stats['visit_count'], interaction_count=stats['interaction_count'])

@app.route('/summary', methods=['GET', 'POST'])
def summary():
    if request.method == 'POST':
        seoul_tz = pytz.timezone('Asia/Seoul')
        entry = {
            'timestamp': datetime.now(seoul_tz).strftime('%Y-%m-%d %H:%M'),
            'main_task': request.json.get('main-task', []),
            'learning': request.json.get('learning', []),
            'special_notes': request.json.get('special-notes', []),
            'tomorrow_task': request.json.get('tomorrow-task', [])
        }
        entries.append(entry)
        save_entries(entries)
        stats['interaction_count'] += 1
        save_stats(stats)
        return redirect(url_for('history'))
    return render_template('summary.html', entries=entries)

@app.route('/history')
def history():
    return render_template('history.html', entries=entries)

@app.route('/entry/<int:index>')
def entry_detail(index):
    entry = entries[index]
    stats['interaction_count'] += 1
    save_stats(stats)
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
        stats['interaction_count'] += 1
        save_stats(stats)
        return redirect(url_for('entry_detail', index=index))
    return render_template('edit_entry.html', entry=entry, index=index)

@app.route('/lab')
def lab():
    return render_template('lab.html', updates=updates)

@app.route('/add_update', methods=['POST'])
def add_update():
    update_description = request.form['update_description']
    update_date = datetime.now().strftime('%Y-%m-%d')
    new_update = {'date': update_date, 'description': update_description}
    updates.insert(0, new_update)
    save_updates(updates)
    return jsonify(new_update)

if __name__ == '__main__':
    app.run(debug=True)
