from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'nonjunmo-secret'

@app.route('/')
def index():
    return '<h1>논문 초안 완성 코스 - 논준모연구소</h1>'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == 'miso0404^^':
            session['admin'] = True
            return redirect(url_for('admin_panel'))
        return '비밀번호가 틀렸습니다.'
    return '''
    <form method="post">
        <input type="password" name="password" placeholder="비밀번호 입력"/>
        <button type="submit">로그인</button>
    </form>
    '''

@app.route('/admin-panel')
def admin_panel():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    return '<h1>관리자 페이지</h1>'

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
