
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecret'
DATA_FILE = 'data.json'
ADMIN_PASSWORD = 'miso0404^^'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    today = datetime.today()
    return render_template('index.html', today=today.strftime('%Y-%m-%d'))

@app.route('/apply', methods=['POST'])
def apply():
    data = load_data()
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    date = request.form['date']
    major = request.form['major']
    topic = request.form['topic']
    category = request.form['category']
    message = request.form['message']
    if date not in data:
        data[date] = []
    if len(data[date]) < 5:
        data[date].append({
            'name': name,
            'phone': phone,
            'email': email,
            'category': category,
            'major': major,
            'topic': topic,
            'message': message
        })
        save_data(data)
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('dashboard'))
    return render_template('admin_login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    data = load_data()
    return render_template('admin.html', data=data)

@app.route('/delete/<date>/<int:index>')
def delete(date, index):
    if not session.get('admin'):
        return redirect(url_for('admin'))
    data = load_data()
    if date in data and 0 <= index < len(data[date]):
        del data[date][index]
        if not data[date]:
            del data[date]
        save_data(data)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
