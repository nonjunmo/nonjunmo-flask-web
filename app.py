from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'nonjunmo-secret'

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)