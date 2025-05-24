from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'nonjunmo-secret'

DATA_FILE = 'applications.json'

def load_applications():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_applications(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == 'miso0404^^':
            session['admin'] = True
            return redirect(url_for('admin_panel'))
        return '비밀번호가 틀렸습니다.'
    return render_template('admin_login.html')

@app.route('/admin-panel')
def admin_panel():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    return render_template('admin_panel.html')

@app.route('/apply', methods=['POST'])
def apply():
    data = request.form.to_dict()
    date = data.get('date')
    applications = load_applications()
    if date not in applications:
        applications[date] = []
    applications[date].append(data)
    save_applications(applications)
    return jsonify(success=True)

@app.route('/get_applications')
def get_applications():
    return jsonify(load_applications())

@app.route('/delete_application', methods=['POST'])
def delete_application():
    date = request.form.get('date')
    name = request.form.get('name')
    applications = load_applications()
    if date in applications:
        applications[date] = [app for app in applications[date] if app['name'] != name]
        if not applications[date]:
            del applications[date]
        save_applications(applications)
    return jsonify(success=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)