import os, sqlite3, json
from bottle import route, run, request, response, redirect, template

def json_dumps(d):
    return json.dumps(d)

def get_db():
    conn = sqlite3.connect('node.db')
    conn.row_factory = sqlite3.Row
    return conn

@route('/')
def login_page():
    conn = get_db()
    users = [dict(u) for u in conn.execute("SELECT * FROM users").fetchall()]
    conn.close()
    return template('templates/login.html', users=users)

@route('/login', method='POST')
def login():
    name = request.forms.get('name')
    password = request.forms.get('password')
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE name = ? AND password = ?", (name, password)).fetchone()
    conn.close()
    if user:
        response.set_cookie('user_name', user['name'], path='/')
        if user['role'] == 'admin':
            redirect('/admin')
        else:
            redirect('/dash')
    else:
        redirect('/')

@route('/dash')
def dashboard():
    user_name = request.cookies.get('user_name')
    if not user_name: redirect('/')
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE name = ?", (user_name,)).fetchone()
    if not user:
        conn.close()
        redirect('/')
    users = [dict(u) for u in conn.execute("SELECT * FROM users").fetchall()]
    projects = [dict(p) for p in conn.execute("SELECT * FROM projects").fetchall()]
    tasks = [dict(t) for t in conn.execute("SELECT * FROM tasks").fetchall()]
    meetings = [dict(m) for m in conn.execute("SELECT * FROM meetings").fetchall()]
    vault = [dict(v) for v in conn.execute("SELECT * FROM vault").fetchall()]
    announcements = [dict(a) for a in conn.execute("SELECT * FROM announcements").fetchall()]
    conn.close()
    return template('templates/dashboard.html', user=dict(user), users=users, projects=projects, tasks=tasks, meetings=meetings, vault=vault, announcements=announcements, json_dumps=json_dumps)

@route('/admin')
def admin_portal():
    user_name = request.cookies.get('user_name')
    if not user_name: redirect('/')
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE name = ?", (user_name,)).fetchone()
    if not user or user['role'] != 'admin':
        conn.close()
        redirect('/dash')
    
    users = [dict(u) for u in conn.execute("SELECT * FROM users").fetchall()]
    projects = [dict(p) for p in conn.execute("SELECT * FROM projects").fetchall()]
    tasks = [dict(t) for t in conn.execute("SELECT * FROM tasks").fetchall()]
    meetings = [dict(m) for m in conn.execute("SELECT * FROM meetings").fetchall()]
    vault = [dict(v) for v in conn.execute("SELECT * FROM vault").fetchall()]
    announcements = [dict(a) for a in conn.execute("SELECT * FROM announcements").fetchall()]
    conn.close()
    return template('templates/admin.html', user=dict(user), users=users, projects=projects, tasks=tasks, meetings=meetings, vault=vault, announcements=announcements, json_dumps=json_dumps)

@route('/upload', method='POST')
def upload_file():
    user_name = request.cookies.get('user_name', 'System Member')
    doc = request.files.get('document')
    if doc:
        filename = doc.filename
        save_path = os.path.join('uploads', filename)
        doc.save(save_path, overwrite=True)
        conn = get_db()
        conn.execute("INSERT INTO vault (title, uploader, date) VALUES (?,?,?)", (filename, user_name, "Oct 08, 2026"))
        conn.commit()
        conn.close()
    redirect(request.headers.get('Referer', '/dash'))

@route('/update_profile', method='POST')
def update_profile():
    user_name = request.cookies.get('user_name')
    if not user_name: redirect('/')
    conn = get_db()
    conn.execute("UPDATE users SET education=?, career=?, responsibilities=?, bio=? WHERE name=?",
                 (request.forms.get('education'), request.forms.get('career'), request.forms.get('responsibilities'), request.forms.get('bio'), user_name))
    conn.commit()
    conn.close()
    redirect('/dash')

@route('/add_concern', method='POST')
def add_concern():
    user_name = request.cookies.get('user_name')
    if not user_name: redirect('/')
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE name = ?", (user_name,)).fetchone()
    conn.execute("INSERT INTO announcements (title, author, category, date) VALUES (?,?,?,?)",
                 (request.forms.get('title'), user_name, request.forms.get('category'), "Oct 08, 2026"))
    conn.commit()
    conn.close()
    if user and user['role'] == 'admin':
        redirect('/admin')
    else:
        redirect('/dash')

@route('/logout')
def logout():
    response.delete_cookie('user_name', path='/')
    redirect('/')

@route('/api/mancer', method='POST')
def mancer_api():
    data = request.json or {}
    query = data.get('query', '').strip()
    file_text = data.get('file_text', '').strip()
    query_lower = query.lower()
    user_name = request.cookies.get('user_name', 'Member')
    
    conn = get_db()
    
    # 1. Document & File Content Analysis
    if file_text:
        summary_preview = file_text[:400].strip() + ("..." if len(file_text) > 400 else "")
        reply = f"<strong>Document Content Analysis Complete:</strong><br/>I have processed your uploaded file ({len(file_text)} characters).<br/><br/><strong>Extracted Summary / Preview:</strong><br/><em>'{summary_preview}'</em><br/><br/>How would you like me to process or modify this text further?"

    # 2. Explicit Developer Identity Query ONLY
    elif any(k in query_lower for k in ['who built', 'who created', 'who is your developer', 'who is developer', 'who architected', 'developer of mancer']):
        reply = "Mancer AI was architected and developed exclusively by Gabriel Aloka Obuogi, Digital Architect & Software Developer of the NODE system."

    # 3. Specific General World & Technical Knowledge Inquiries
    elif 'president' in query_lower and 'kenya' in query_lower:
        reply = "The President of the Republic of Kenya is His Excellency Dr. William Samoei Ruto, who assumed office in September 2022 as the 5th President of Kenya."

    elif 'python' in query_lower:
        reply = "Python is a high-level, interpreted programming language known for its clean, readable syntax and extensive ecosystem. In the NODE platform, Python powers the backend web server via Bottle and communicates seamlessly with SQLite."

    elif 'family' in query_lower and ('define' in query_lower or 'what is' in query_lower or 'meaning' in query_lower):
        reply = "A family is a fundamental social unit united by kinship, lineage, or shared commitments. In NODE, family represents a unified structure collaborating across education, agriculture, technology, and economic development."

    # 4. Internal Database Inquiries
    elif any(k in query_lower for k in ['meeting', 'assembly', 'assemblies']):
        m_list = conn.execute("SELECT title, date_badge, time, location FROM meetings").fetchall()
        reply = "<strong>Upcoming Assemblies:</strong><br/>" + "<br/>".join([f"• <b>{m['title']}</b> on {m['date_badge']} ({m['time']} at {m['location']})" for m in m_list])

    elif any(k in query_lower for k in ['project', 'agri', 'educare', 'venture']):
        p_list = conn.execute("SELECT title, leader, progress FROM projects").fetchall()
        reply = "<strong>Active Family Projects:</strong><br/>" + "<br/>".join([f"• <b>{p['title']}</b> (Led by {p['leader']}) - {p['progress']}% Complete" for p in p_list])

    elif any(k in query_lower for k in ['task', 'duty', 'assigned', 'todo']):
        t_list = conn.execute("SELECT title, priority, status FROM tasks WHERE assignee = ? OR assignee = 'All Members'", (user_name,)).fetchall()
        if t_list:
            reply = f"<strong>Tasks for {user_name}:</strong><br/>" + "<br/>".join([f"• {t['title']} [{t['priority']} Priority - Status: {t['status']}]" for t in t_list])
        else:
            reply = f"Hello {user_name}, you currently have no pending tasks assigned."

    elif any(k in query_lower for k in ['hello', 'hi', 'hey', 'greetings']):
        reply = f"Hello {user_name}! I am Mancer AI. How can I assist you today? You can ask me about NODE database records, general knowledge and technical topics, or upload a document for instant analysis."

    # 5. Standard AI Knowledge Fallback Engine
    else:
        reply = f"Regarding <strong>'{query}'</strong>: Mancer AI is fully operational. As a universal assistant, I can help answer technical and general knowledge questions, write code, analyze document files, or retrieve internal NODE records. Let me know what specific detail you'd like to explore!"

    conn.close()
    response.content_type = 'application/json'
    return json.dumps({'reply': reply})

print("[+] NODE Server running with responsive uploads & smart Mancer AI on http://127.0.0.1:8000")
run(host='127.0.0.1', port=8000, quiet=False)
