import os
os.makedirs('templates', exist_ok=True)

# 1. Create the dark-mode Login Page
login_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NODE // Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#0a0f1d] flex items-center justify-center h-screen">
    <div class="bg-[#121a2d] p-8 rounded-xl border border-[#1e293b] w-96 shadow-2xl">
        <div class="flex items-center gap-3 mb-6 justify-center">
            <div class="w-12 h-12 rounded-lg bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center font-bold text-2xl text-white">N</div>
        </div>
        <h2 class="text-2xl font-bold text-white text-center mb-2">NODE System</h2>
        <p class="text-slate-400 text-center text-sm mb-6">Select your profile to continue</p>
        
        <form action="/login" method="POST" class="space-y-4">
            <div>
                <label class="text-xs font-bold text-slate-400 uppercase">Family Member</label>
                <select name="name" class="w-full mt-1 p-2.5 bg-[#0d1424] text-white border border-[#1e293b] rounded-lg outline-none">
                    {% for u in users %}
                    <option value="{{ u.name }}">{{ u.name }} ({{ u.title }})</option>
                    {% endfor %}
                </select>
            </div>
            <div>
                <label class="text-xs font-bold text-slate-400 uppercase">Password</label>
                <input type="password" name="password" required class="w-full mt-1 p-2.5 bg-[#0d1424] text-white border border-[#1e293b] rounded-lg outline-none">
            </div>
            <button type="submit" class="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-lg mt-2">Access Node</button>
        </form>
    </div>
</body>
</html>'''
with open('templates/login.html', 'w') as f:
    f.write(login_html)

# 2. Fix the Local Server to use Jinja2
runner_code = '''
from bottle import route, run, request, response, redirect, jinja2_template
import sqlite3

def get_db():
    conn = sqlite3.connect('node.db')
    conn.row_factory = sqlite3.Row
    return conn

@route('/')
def login_page():
    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return jinja2_template('templates/login.html', users=users)

@route('/login', method='POST')
def login():
    name = request.forms.get('name')
    password = request.forms.get('password')
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE name = ? AND password = ?", (name, password)).fetchone()
    conn.close()
    if user:
        response.set_cookie('user_name', user['name'], path='/')
        redirect('/dashboard')
    else:
        redirect('/')

@route('/dashboard')
def dashboard():
    user_name = request.cookies.get('user_name')
    if not user_name:
        redirect('/')
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE name = ?", (user_name,)).fetchone()
    conn.close()
    return jinja2_template('templates/dashboard.html', user=dict(user))

@route('/logout')
def logout():
    response.delete_cookie('user_name', path='/')
    redirect('/')

print("[+] Server fixed. Starting at http://127.0.0.1:8000...")
run(host='127.0.0.1', port=8000, quiet=False)
'''
with open('local_runner.py', 'w') as f:
    f.write(runner_code.strip())
