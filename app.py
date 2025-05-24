from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

MAX_CAPACITY = 5
ADMIN_PASSWORD = 'miso0404^^'

# in-memory DB
applications = {}

@app.route('/')
def index():
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', today=today, applications=applications)

@app.route('/apply', methods=['POST'])
def apply():
    date = request.form['date']
    name = request.form['name']
    contact = request.form['contact']

    if date not in applications:
        applications[date] = []

    if len(applications[date]) < MAX_CAPACITY:
        applications[date].append({'name': name, 'contact': contact})

    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin'))
        return render_template('admin_login.html', error="비밀번호가 틀렸습니다.")
    if not session.get('admin'):
        return render_template('admin_login.html')
    return render_template('admin.html', applications=applications)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
