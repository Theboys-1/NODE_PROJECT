import sqlite3
import hashlib
import os

def hash_pw(password):
    salt = os.urandom(16).hex()
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    return f"{salt}:{hashed}"

# 1. Initialize SQLite Database
print("Initializing database...")
if os.path.exists("node_phase1.db"):
    os.remove("node_phase1.db")

conn = sqlite3.connect("node_phase1.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    position TEXT NOT NULL,
    details TEXT NOT NULL
)""")

cursor.execute("""
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    assigned_to TEXT NOT NULL,
    status TEXT DEFAULT 'pending'
)""")

cursor.execute("""
CREATE TABLE vault (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    filepath TEXT NOT NULL,
    uploaded_by TEXT NOT NULL
)""")

cursor.execute("""
CREATE TABLE meetings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    meeting_date TEXT NOT NULL,
    agenda TEXT NOT NULL,
    minutes TEXT
)""")

cursor.execute("""
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    leader TEXT NOT NULL,
    budget TEXT NOT NULL,
    progress INTEGER DEFAULT 0
)""")

roster = [
    ("Felix Ochieng", "@Felix", "admin", "Family Chairman", "Leadership, coordination, public-sector experience, accountability, family decision-making."),
    ("Gabriel Aloka", "@Gabriel", "admin", "NODE Digital Architect", "BSc Computer Science (Kisii Univ). System architecture, software, AI, cybersecurity, data management."),
    ("Elisha Ouma", "@Elisha", "user", "Vice Chairman", "Opportunity identification, economic development, networking, external opportunities."),
    ("Collins Odwar", "@Collins", "user", "Family Secretary", "Student at Kisii Univ (AGED). Administration, documentation, communication, education initiatives."),
    ("Judith Katiba", "@Judith", "user", "Family Member", "Family support, experience, relationship building, guidance, community connection."),
    ("Esther Joan", "@Esther", "user", "Family Member", "Maasai Mara Univ (Education Science). Education, teaching, mentorship, youth development."),
    ("Joan Atieno", "@Joan", "user", "Family Member", "Diploma in Food Tech (Homabay Poly). Food technology, agricultural opportunities, processing, entrepreneurship."),
    ("Meshack Obuogi", "@Meshack", "user", "Family Member", "Theology student (Catholic Church). Values, faith, spiritual development, service, community connection."),
    ("Obuogi Parents", "@Obuogi", "user", "Family Advisory", "Foundation of experience, wisdom, guidance, family history, values, and mentorship.")
]

for username, password, role, position, details in roster:
    cursor.execute("INSERT INTO users (username, password_hash, role, position, details) VALUES (?, ?, ?, ?, ?)",
                   (username, hash_pw(password), role, position, details))

conn.commit()
conn.close()
print("✓ Database built successfully with official Obuogi roster.")

# 2. Write Login HTML
with open("login.html", "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NODE — Family Login</title>
    <style>
        body { background: #0b0f19; color: #f8fafc; font-family: 'Segoe UI', system-ui, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 15px; }
        .login-card { background: #151c2c; padding: 30px; border-radius: 14px; border: 1px solid rgba(139, 92, 246, 0.3); width: 100%; max-width: 380px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
        .brand { font-size: 1.6em; font-weight: 800; background: linear-gradient(to right, #38bdf8, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 5px; }
        .sub { text-align: center; font-size: 0.8em; color: #94a3b8; margin-bottom: 25px; }
        input, select { width: 100%; padding: 12px; margin: 8px 0 18px; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: white; box-sizing: border-box; }
        button { width: 100%; background: linear-gradient(to right, #0284c7, #8b5cf6); color: white; border: none; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .hint { font-size: 0.75em; color: #64748b; text-align: center; margin-top: 15px; line-height: 1.4; }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="brand">NODE</div>
        <div class="sub">New Obuogi Development System</div>

        <form id="login-form">
            <label style="font-size:0.85em;">Select Family Member</label>
            <select id="user-select" required>
                <option value="">-- Choose Account --</option>
                <option value="Felix Ochieng">Felix Ochieng (Chairman - Admin)</option>
                <option value="Gabriel Aloka">Gabriel Aloka (Digital Architect - Admin)</option>
                <option value="Elisha Ouma">Elisha Ouma (Vice Chairman)</option>
                <option value="Collins Odwar">Collins Odwar (Secretary)</option>
                <option value="Judith Katiba">Judith Katiba (Family Member)</option>
                <option value="Esther Joan">Esther Joan (Family Member)</option>
                <option value="Joan Atieno">Joan Atieno (Family Member)</option>
                <option value="Meshack Obuogi">Meshack Obuogi (Family Member)</option>
                <option value="Obuogi Parents">Obuogi Parents (Family Advisory)</option>
            </select>

            <label style="font-size:0.85em;">Password</label>
            <input type="password" id="password" placeholder="Default: @FirstName" required>

            <button type="submit">Sign In</button>
        </form>

        <div class="hint">
            🔒 Private Obuogi Family System<br>
            Default passwords: <strong>@FirstName</strong> (e.g. <code>@Felix</code>, <code>@Gabriel</code>)
        </div>
    </div>

    <script>
        document.getElementById('user-select').addEventListener('change', (e) => {
            const val = e.target.value;
            if (val) {
                const firstName = val.split(' ')[0];
                document.getElementById('password').value = `@${firstName}`;
            }
        });

        document.getElementById('login-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('user-select').value;
            const password = document.getElementById('password').value;

            const res = await fetch('/api/v1/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
            });

            if (res.ok) {
                const data = await res.json();
                sessionStorage.setItem('node_token', data.access_token);
                sessionStorage.setItem('node_user', data.username);
                sessionStorage.setItem('node_role', data.role);
                sessionStorage.setItem('node_pos', data.position);
                location.href = '/dashboard';
            } else {
                alert('Invalid credentials');
            }
        });
    </script>
</body>
</html>""")

# 3. Write Dashboard HTML
with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NODE — New Obuogi Development</title>
    <style>
        :root {
            --bg-main: #0b0f19;
            --bg-card: #151c2c;
            --bg-accent: #1e293b;
            --primary: #8b5cf6;
            --primary-light: #c084fc;
            --cyan: #06b6d4;
            --green: #10b981;
            --danger: #ef4444;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }
        body { background: var(--bg-main); color: var(--text-main); font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; padding: 15px; }
        header { background: linear-gradient(135deg, #1e1b4b, #311042); padding: 20px; border-radius: 14px; border: 1px solid rgba(139, 92, 246, 0.3); display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .brand-title { font-size: 1.4em; font-weight: 800; background: linear-gradient(to right, #38bdf8, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .brand-subtitle { font-size: 0.75em; color: var(--text-muted); margin-top: 4px; }
        .badge { padding: 6px 12px; border-radius: 20px; font-size: 0.8em; font-weight: bold; text-transform: uppercase; }
        .badge-admin { background: rgba(168, 85, 247, 0.2); color: var(--primary-light); border: 1px solid var(--primary); }
        .badge-user { background: rgba(6, 182, 212, 0.2); color: var(--cyan); border: 1px solid var(--cyan); }
        .admin-section { background: linear-gradient(135deg, #2e1065, #1e1b4b); border: 2px solid var(--primary); padding: 20px; border-radius: 14px; margin-bottom: 25px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; margin: 15px 0; }
        .stat-card { background: rgba(15, 23, 42, 0.7); padding: 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); text-align: center; }
        .stat-val { font-size: 1.5em; font-weight: bold; color: var(--cyan); }
        .stat-lbl { font-size: 0.7em; color: var(--text-muted); }
        .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 25px; }
        .card { background: var(--bg-card); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.08); }
        .card-header { font-size: 1.1em; font-weight: 700; color: #f1f5f9; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; }
        .roster-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; }
        .member-card { background: var(--bg-accent); border-radius: 10px; padding: 12px; border-left: 4px solid var(--primary); }
        .member-name { font-size: 1em; font-weight: bold; color: #fff; }
        .member-pos { font-size: 0.8em; color: var(--cyan); font-weight: 600; margin-bottom: 4px; }
        .member-desc { font-size: 0.75em; color: var(--text-muted); line-height: 1.3; }
        .btn { background: var(--primary); color: white; border: none; padding: 8px 12px; border-radius: 6px; cursor: pointer; font-weight: 600; }
        .btn-danger { background: var(--danger); }
        .btn-sm { padding: 4px 8px; font-size: 0.75em; }
        input, select, textarea { width: 100%; padding: 10px; margin: 6px 0 12px; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: white; box-sizing: border-box; }
        ul { list-style: none; padding: 0; margin: 0; }
        li { background: var(--bg-accent); padding: 10px; border-radius: 8px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
        .done { text-decoration: line-through; opacity: 0.5; }
        .values-banner { background: linear-gradient(90deg, #0f172a, #1e293b); padding: 12px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #334155; }
        .val-chip { background: rgba(139, 92, 246, 0.15); border: 1px solid var(--primary); padding: 3px 8px; border-radius: 12px; font-size: 0.75em; color: var(--primary-light); display: inline-block; margin: 2px; }
    </style>
</head>
<body>

    <header>
        <div>
            <div class="brand-title">NODE — NEW OBUOGI DEVELOPMENT</div>
            <div class="brand-subtitle">Rooted in Faith. Built on Family. Driven by Development. Created for Legacy.</div>
        </div>
        <div>
            <span id="user-badge" class="badge"></span>
            <button onclick="sessionStorage.clear();location.href='/login';" class="btn btn-danger btn-sm" style="margin-left:10px;">Logout</button>
        </div>
    </header>

    <div class="values-banner">
        <strong style="color:var(--cyan);">FAMILY VISION:</strong>
        <span style="font-size:0.85em; color:#cbd5e1;">"To build a united, educated, economically empowered Obuogi family."</span>
        <div style="margin-top:6px;">
            <span class="val-chip">1. Unity</span>
            <span class="val-chip">2. Education</span>
            <span class="val-chip">3. Responsibility</span>
            <span class="val-chip">4. Integrity</span>
            <span class="val-chip">5. Faith & Values</span>
            <span class="val-chip">6. Development</span>
        </div>
    </div>

    <div id="admin-panel" class="admin-section" style="display:none;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <h3 style="margin:0; color:#c084fc;">👑 Executive Admin Suite</h3>
            <span style="font-size:0.75em; color:var(--text-muted);">Restricted Access</span>
        </div>

        <div class="stats-grid">
            <div class="stat-card"><div id="stat-users" class="stat-val">0</div><div class="stat-lbl">Members</div></div>
            <div class="stat-card"><div id="stat-projects" class="stat-val">0</div><div class="stat-lbl">Projects</div></div>
            <div class="stat-card"><div id="stat-meetings" class="stat-val">0</div><div class="stat-lbl">Meetings</div></div>
            <div class="stat-card"><div id="stat-tasks" class="stat-val">0</div><div class="stat-lbl">Actions</div></div>
            <div class="stat-card"><div id="stat-vault" class="stat-val">0</div><div class="stat-lbl">Vault Files</div></div>
        </div>

        <h4>👥 Family Member Roster Management</h4>
        <ul id="admin-user-list"></ul>
    </div>

    <div class="card" style="margin-bottom:25px;">
        <div class="card-header">
            <span>🏛️ Family Leadership & Governance Structure</span>
        </div>
        <div id="roster-grid" class="roster-grid"></div>
    </div>

    <div class="grid-2">
        <div class="card">
            <div class="card-header">📅 Family Meetings Tracker</div>
            <form id="meeting-form">
                <input type="text" id="m-title" placeholder="Meeting Title" required>
                <input type="text" id="m-date" placeholder="Date & Time" required>
                <textarea id="m-agenda" rows="2" placeholder="Agenda or Discussion Topics" required></textarea>
                <button type="submit" class="btn" style="width:100%;">Schedule Meeting</button>
            </form>
            <ul id="meeting-list" style="margin-top:15px;"></ul>
        </div>

        <div class="card">
            <div class="card-header">🚀 Projects & Economic Development</div>
            <form id="project-form">
                <input type="text" id="p-title" placeholder="Project Name" required>
                <input type="text" id="p-leader" placeholder="Project Leader" required>
                <input type="text" id="p-budget" placeholder="Budget / Target" required>
                <button type="submit" class="btn" style="width:100%;">Initialize Project</button>
            </form>
            <ul id="project-list" style="margin-top:15px;"></ul>
        </div>
    </div>

    <div class="grid-2">
        <div class="card">
            <div class="card-header">📋 Decision Pipeline & Responsibility Tracker</div>
            <form id="task-form">
                <input type="text" id="task-title" placeholder="Action Item / Task..." required>
                <input type="text" id="task-assign" placeholder="Assigned Member" required>
                <button type="submit" class="btn" style="width:100%;">Assign Responsibility</button>
            </form>
            <ul id="task-list" style="margin-top:15px;"></ul>
        </div>

        <div class="card">
            <div class="card-header">📁 Family Heritage & Document Vault</div>
            <form id="vault-form">
                <input type="file" id="vault-file" required>
                <button type="submit" class="btn" style="width:100%;">Upload Record / Minute</button>
            </form>
            <ul id="vault-list" style="margin-top:15px;"></ul>
        </div>
    </div>

    <script>
        const role = sessionStorage.getItem('node_role');
        const username = sessionStorage.getItem('node_user');
        const position = sessionStorage.getItem('node_pos');

        if (!sessionStorage.getItem('node_token')) location.href = '/login';

        const badge = document.getElementById('user-badge');
        badge.innerText = `${username} • ${position}`;
        badge.className = `badge ${role === 'admin' ? 'badge-admin' : 'badge-user'}`;

        if (role === 'admin') {
            document.getElementById('admin-panel').style.display = 'block';
            loadAdminStats();
        }

        async function loadAdminStats() {
            const res = await fetch('/api/v1/admin/stats');
            const d = await res.json();
            document.getElementById('stat-users').innerText = d.users;
            document.getElementById('stat-tasks').innerText = d.tasks;
            document.getElementById('stat-vault').innerText = d.vault;
            document.getElementById('stat-meetings').innerText = d.meetings;
            document.getElementById('stat-projects').innerText = d.projects;
        }

        async function loadRoster() {
            const res = await fetch('/api/v1/users');
            const users = await res.json();
            
            document.getElementById('roster-grid').innerHTML = users.map(u => `
                <div class="member-card">
                    <div class="member-name">${u.username}</div>
                    <div class="member-pos">📌 ${u.position}</div>
                    <div class="member-desc">${u.details}</div>
                </div>
            `).join('');

            if (role === 'admin') {
                document.getElementById('admin-user-list').innerHTML = users.map(u => `
                    <li>
                        <span><strong>${u.username}</strong> (${u.position})</span>
                        <button onclick="resetPassword(${u.id})" class="btn btn-sm">Reset Password</button>
                    </li>
                `).join('');
            }
        }

        async function resetPassword(id) {
            const res = await fetch('/api/v1/users/reset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `id=${id}`
            });
            const data = await res.json();
            if (data.status === 'success') {
                alert(`Password reset successfully! Default password is: ${data.default_pw}`);
            }
        }

        async function loadTasks() {
            const res = await fetch('/api/v1/tasks');
            const tasks = await res.json();
            document.getElementById('task-list').innerHTML = tasks.map(t => `
                <li class="${t.status === 'completed' ? 'done' : ''}">
                    <span><strong>${t.title}</strong> → <em>${t.assigned_to}</em></span>
                    <div>
                        <button onclick="toggleTask(${t.id}, '${t.status}')" class="btn btn-sm">${t.status === 'completed' ? 'Undo' : 'Done'}</button>
                        ${role === 'admin' ? `<button onclick="deleteTask(${t.id})" class="btn btn-danger btn-sm">Delete</button>` : ''}
                    </div>
                </li>
            `).join('');
        }

        async function toggleTask(id, cur) {
            await fetch('/api/v1/tasks/toggle', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `id=${id}&status=${cur === 'completed' ? 'pending' : 'completed'}`
            });
            loadTasks();
            if (role === 'admin') loadAdminStats();
        }

        async function deleteTask(id) {
            await fetch('/api/v1/tasks/delete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `id=${id}`
            });
            loadTasks();
            if (role === 'admin') loadAdminStats();
        }

        document.getElementById('task-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            await fetch('/api/v1/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `title=${encodeURIComponent(document.getElementById('task-title').value)}&assigned_to=${encodeURIComponent(document.getElementById('task-assign').value)}`
            });
            document.getElementById('task-title').value = '';
            document.getElementById('task-assign').value = '';
            loadTasks();
            if (role === 'admin') loadAdminStats();
        });

        async function loadMeetings() {
            const res = await fetch('/api/v1/meetings');
            const meetings = await res.json();
            document.getElementById('meeting-list').innerHTML = meetings.map(m => `
                <li>
                    <div>
                        <strong>${m.title}</strong> (${m.meeting_date})
                        <div style="font-size:0.75em; color:var(--text-muted);">${m.agenda}</div>
                    </div>
                </li>
            `).join('');
        }

        document.getElementById('meeting-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            await fetch('/api/v1/meetings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `title=${encodeURIComponent(document.getElementById('m-title').value)}&meeting_date=${encodeURIComponent(document.getElementById('m-date').value)}&agenda=${encodeURIComponent(document.getElementById('m-agenda').value)}&minutes=`
            });
            document.getElementById('m-title').value = '';
            document.getElementById('m-date').value = '';
            document.getElementById('m-agenda').value = '';
            loadMeetings();
            if (role === 'admin') loadAdminStats();
        });

        async function loadProjects() {
            const res = await fetch('/api/v1/projects');
            const projects = await res.json();
            document.getElementById('project-list').innerHTML = projects.map(p => `
                <li>
                    <div>
                        <strong>${p.title}</strong> (Leader: ${p.leader})
                        <div style="font-size:0.75em; color:var(--cyan);">Budget / Target: ${p.budget}</div>
                    </div>
                </li>
            `).join('');
        }

        document.getElementById('project-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            await fetch('/api/v1/projects', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `title=${encodeURIComponent(document.getElementById('p-title').value)}&leader=${encodeURIComponent(document.getElementById('p-leader').value)}&budget=${encodeURIComponent(document.getElementById('p-budget').value)}&progress=0`
            });
            document.getElementById('p-title').value = '';
            document.getElementById('p-leader').value = '';
            document.getElementById('p-budget').value = '';
            loadProjects();
            if (role === 'admin') loadAdminStats();
        });

        async function loadVault() {
            const res = await fetch('/api/v1/vault');
            const files = await res.json();
            document.getElementById('vault-list').innerHTML = files.map(f => `
                <li>
                    <span>📄 ${f.filename} (Uploaded by ${f.uploaded_by})</span>
                    <div>
                        <a href="${f.filepath}" download class="btn btn-sm" style="text-decoration:none;">Download</a>
                        ${role === 'admin' ? `<button onclick="deleteVault(${f.id})" class="btn btn-danger btn-sm">Delete</button>` : ''}
                    </div>
                </li>
            `).join('');
        }

        async function deleteVault(id) {
            await fetch('/api/v1/vault/delete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `id=${id}`
            });
            loadVault();
            if (role === 'admin') loadAdminStats();
        }

        document.getElementById('vault-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const fileInput = document.getElementById('vault-file');
            if (!fileInput.files.length) return;
            const file = fileInput.files[0];
            const reader = new FileReader();
            reader.onload = async () => {
                await fetch('/api/v1/vault/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        filename: file.name,
                        filedata: reader.result.split(',')[1],
                        uploaded_by: username
                    })
                });
                fileInput.value = '';
                loadVault();
                if (role === 'admin') loadAdminStats();
            };
            reader.readAsDataURL(file);
        });

        loadRoster();
        loadTasks();
        loadMeetings();
        loadProjects();
        loadVault();
    </script>
</body>
</html>""")

# 4. Write Python Server Script
with open("server.py", "w", encoding="utf-8") as f:
    f.write("""import http.server
import socketserver
import json
import urllib.parse
import sqlite3
import hashlib
import os
import base64

PORT = 8000

def hash_pw(password):
    salt = os.urandom(16).hex()
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    return f"{salt}:{hashed}"

def verify_pw(password, stored_hash):
    try:
        salt, hashed = stored_hash.split(":")
        check = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
        return check == hashed
    except Exception:
        return False

class NodeHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ['/', '/dashboard']:
            self.send_file('dashboard.html')
        elif self.path == '/login':
            self.send_file('login.html')
        elif self.path == '/api/v1/users':
            conn = sqlite3.connect("node_phase1.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, role, position, details FROM users")
            rows = cursor.fetchall()
            conn.close()
            self.send_json([{"id": r[0], "username": r[1], "role": r[2], "position": r[3], "details": r[4]} for r in rows])
        elif self.path == '/api/v1/admin/stats':
            conn = sqlite3.connect("node_phase1.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            u_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM tasks")
            t_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM vault")
            v_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM meetings")
            m_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM projects")
            p_count = cursor.fetchone()[0]
            conn.close()
            self.send_json({"users": u_count, "tasks": t_count, "vault": v_count, "meetings": m_count, "projects": p_count})
        elif self.path == '/api/v1/tasks':
            conn = sqlite3.connect("node_phase1.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, assigned_to, status FROM tasks")
            rows = cursor.fetchall()
            conn.close()
            self.send_json([{"id": r[0], "title": r[1], "assigned_to": r[2], "status": r[3]} for r in rows])
        elif self.path == '/api/v1/vault':
            conn = sqlite3.connect("node_phase1.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, filename, filepath, uploaded_by FROM vault")
            rows = cursor.fetchall()
            conn.close()
            self.send_json([{"id": r[0], "filename": r[1], "filepath": r[2], "uploaded_by": r[3]} for r in rows])
        elif self.path == '/api/v1/meetings':
            conn = sqlite3.connect("node_phase1.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, meeting_date, agenda, minutes FROM meetings")
            rows = cursor.fetchall()
            conn.close()
            self.send_json([{"id": r[0], "title": r[1], "meeting_date": r[2], "agenda": r[3], "minutes": r[4]} for r in rows])
        elif self.path == '/api/v1/projects':
            conn = sqlite3.connect("node_phase1.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, leader, budget, progress FROM projects")
            rows = cursor.fetchall()
            conn.close()
            self.send_json([{"id": r[0], "title": r[1], "leader": r[2], "budget": r[3], "progress": r[4]} for r in rows])
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        if self.path == '/api/v1/login':
            parsed = urllib.parse.parse_qs(post_data.decode('utf-8'))
            username = parsed.get('username', [''])[0].strip()
            password = parsed.get('password', [''])[0].strip()

            conn = sqlite3.connect("node_phase1.db")
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash, role, position, username FROM users WHERE LOWER(username) = ?", (username.lower(),))
            row = cursor.fetchone()
            conn.close()

            if row and verify_pw(password, row[0]):
                self.send_json({
                    "access_token": f"token_{row[3]}",
                    "username": row[3],
                    "role": row[1],
                    "position": row[2]
                })
            else:
                self.send_json({"detail": "Invalid username or password"}, status=401)

        elif self.path == '/api/v1/users/reset':
            parsed = urllib.parse.parse_qs(post_data.decode('utf-8'))
            user_id = parsed.get('id', [''])[0]
            conn = sqlite3.connect("node_phase1.db")
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                first_name = row[0].split()[0]
                default_pw = f"@{first_name}"
                cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hash_pw(default_pw), user_id))
                conn.commit()
                conn.close()
                self.send_json({"status": "success", "default_pw": default_pw})
            else:
                conn.close()
                self.send_json({"status": "error", "message": "User not found"})

        elif self.path == '/api/v1/tasks':
            parsed = urllib.parse.parse_qs(post_data.decode('utf-8'))
            conn = sqlite3.connect("node_phase1.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title, assigned_to) VALUES (?, ?)", 
                           (parsed.get('title', [''])[0], parsed.get('assigned_to', [''])[0]))
            conn.commit()
            conn.close()
            self.send_json({"status": "success"})

        elif self.path == '/api/v1/tasks/toggle':
            parsed = urllib.parse.parse_qs(post_data.decode('utf-8'))
            conn = sqlite3.connect("node_phase1.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (parsed.get('status', [''])[0], parsed.get('id', [''])[0]))
            conn.commit()
            conn.close()
            self.send_json({"status": "success"})

        elif self.path == '/api/v1/tasks/delete':
            parsed = urllib.parse.parse_qs(post_data.decode('utf-8'))
            conn = sqlite3.connect("node_phase1.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (parsed.get('id', [''])[0],))
            conn.commit()
            conn.close()
            self.send_json({"status": "success"})

        elif self.path == '/api/v1/meetings':
            parsed = urllib.parse.parse_qs(post_data.decode('utf-8'))
            conn = sqlite3.connect("node_phase1.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO meetings (title, meeting_date, agenda, minutes) VALUES (?, ?, ?, ?)",
                           (parsed.get('title', [''])[0], parsed.get('meeting_date', [''])[0], parsed.get('agenda', [''])[0], parsed.get('minutes', [''])[0]))
            conn.commit()
            conn.close()
            self.send_json({"status": "success"})

        elif self.path == '/api/v1/projects':
            parsed = urllib.parse.parse_qs(post_data.decode('utf-8'))
            conn = sqlite3.connect("node_phase1.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO projects (title, leader, budget, progress) VALUES (?, ?, ?, ?)",
                           (parsed.get('title', [''])[0], parsed.get('leader', [''])[0], parsed.get('budget', [''])[0], int(parsed.get('progress', [0])[0])))
            conn.commit()
            conn.close()
            self.send_json({"status": "success"})

        elif self.path == '/api/v1/vault/upload':
            data = json.loads(post_data.decode('utf-8'))
            filename = data['filename']
            filebytes = base64.b64decode(data['filedata'])
            uploaded_by = data.get('uploaded_by', 'Admin')

            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            filepath = os.path.join('uploads', filename)
            with open(filepath, 'wb') as f:
                f.write(filebytes)

            conn = sqlite3.connect("node_phase1.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO vault (filename, filepath, uploaded_by) VALUES (?, ?, ?)", (filename, f"/{filepath}", uploaded_by))
            conn.commit()
            conn.close()
            self.send_json({"status": "success"})

        elif self.path == '/api/v1/vault/delete':
            parsed = urllib.parse.parse_qs(post_data.decode('utf-8'))
            file_id = parsed.get('id', [''])[0]
            conn = sqlite3.connect("node_phase1.db")
            cursor = conn.cursor()
            cursor.execute("SELECT filepath FROM vault WHERE id = ?", (file_id,))
            row = cursor.fetchone()
            if row:
                rel_path = row[0].lstrip('/')
                if os.path.exists(rel_path):
                    try:
                        os.remove(rel_path)
                    except Exception:
                        pass
                cursor.execute("DELETE FROM vault WHERE id = ?", (file_id,))
                conn.commit()
            conn.close()
            self.send_json({"status": "success"})

    def send_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content)
        except Exception:
            self.send_error(404, f"File not found: {filename}")

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

with socketserver.TCPServer(("0.0.0.0", PORT), NodeHandler) as httpd:
    print(f"NODE Admin & Governance Server running at http://0.0.0.0:{PORT}")
    httpd.serve_forever()
""")

print("✓ All files successfully generated.")
