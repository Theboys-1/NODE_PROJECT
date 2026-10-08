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
        redirect('/dash')
    else:
        redirect('/')

@route('/dash')
def dashboard():
    user_name = request.cookies.get('user_name')
    if not user_name:
        redirect('/')
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE name = ?", (user_name,)).fetchone()
    users_raw = conn.execute("SELECT * FROM users").fetchall()
    users = [dict(u) for u in users_raw]
    
    projects = [dict(p) for p in conn.execute("SELECT * FROM projects").fetchall()]
    tasks = [dict(t) for t in conn.execute("SELECT * FROM tasks").fetchall()]
    meetings = [dict(m) for m in conn.execute("SELECT * FROM meetings").fetchall()]
    vault = [dict(v) for v in conn.execute("SELECT * FROM vault").fetchall()]
    conn.close()
    
    return jinja2_template('templates/dashboard.html', user=dict(user), users=users, projects=projects, tasks=tasks, meetings=meetings, vault=vault)

@route('/logout')
def logout():
    response.delete_cookie('user_name', path='/')
    redirect('/')

print("[+] Target UI NODE System running at http://127.0.0.1:8000...")
run(host='127.0.0.1', port=8000, quiet=False)
