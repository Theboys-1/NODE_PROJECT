import os

os.makedirs('templates', exist_ok=True)

dashboard_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NODE // Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-[#070b14] text-slate-100 font-sans antialiased min-h-screen flex flex-col md:flex-row">

    <!-- Mobile Header -->
    <div class="md:hidden bg-[#0d1424] border-b border-slate-800 p-4 flex justify-between items-center sticky top-0 z-50">
        <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white">N</div>
            <span class="font-bold text-lg text-white">NODE System</span>
        </div>
        <button onclick="toggleSidebar()" class="p-2 text-slate-300 hover:text-white">
            <i data-lucide="menu" class="w-6 h-6"></i>
        </button>
    </div>

    <!-- Navigation Sidebar -->
    <aside id="sidebar" class="fixed inset-y-0 left-0 transform -translate-x-full md:relative md:translate-x-0 transition-transform duration-200 ease-in-out w-64 bg-[#0c1220] border-r border-slate-800/80 p-4 flex flex-col justify-between z-40 h-full">
        <div>
            <div class="hidden md:flex items-center gap-3 mb-8 px-2">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center font-extrabold text-xl text-white shadow-lg shadow-cyan-500/20">N</div>
                <div>
                    <h1 class="font-bold text-white tracking-wide">NODE</h1>
                    <p class="text-[10px] text-cyan-400 font-mono tracking-wider uppercase">Obuogi Family System</p>
                </div>
            </div>

            <nav class="space-y-1">
                <button onclick="switchTab('dashboard')" class="nav-btn w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-300 hover:bg-slate-800/60 hover:text-white transition bg-slate-800 text-white" id="btn-dashboard">
                    <i data-lucide="layout-dashboard" class="w-4 h-4 text-cyan-400"></i> Dashboard
                </button>
                <button onclick="switchTab('members')" class="nav-btn w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-300 hover:bg-slate-800/60 hover:text-white transition" id="btn-members">
                    <i data-lucide="users" class="w-4 h-4 text-blue-400"></i> Family Members
                </button>
                <button onclick="switchTab('projects')" class="nav-btn w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-300 hover:bg-slate-800/60 hover:text-white transition" id="btn-projects">
                    <i data-lucide="folder-kanban" class="w-4 h-4 text-emerald-400"></i> Projects
                </button>
                <button onclick="switchTab('meetings')" class="nav-btn w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-300 hover:bg-slate-800/60 hover:text-white transition" id="btn-meetings">
                    <i data-lucide="calendar" class="w-4 h-4 text-amber-400"></i> Meetings
                </button>
                <button onclick="switchTab('tasks')" class="nav-btn w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-300 hover:bg-slate-800/60 hover:text-white transition" id="btn-tasks">
                    <i data-lucide="check-square" class="w-4 h-4 text-purple-400"></i> Tasks
                </button>
                <button onclick="switchTab('finance')" class="nav-btn w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-300 hover:bg-slate-800/60 hover:text-white transition" id="btn-finance">
                    <i data-lucide="wallet" class="w-4 h-4 text-green-400"></i> Finance
                </button>
            </nav>
        </div>

        <div class="pt-4 border-t border-slate-800">
            <div class="flex items-center justify-between mb-3 px-2">
                <div>
                    <p class="text-xs font-bold text-white">{{ user.name }}</p>
                    <p class="text-[11px] text-slate-400">{{ user.title }}</p>
                </div>
                <span class="px-2 py-0.5 text-[10px] bg-cyan-950 text-cyan-300 border border-cyan-800 rounded font-mono uppercase">{{ user.role }}</span>
            </div>
            <a href="/logout" class="flex items-center gap-2 w-full px-3 py-2 rounded-lg text-xs font-medium text-rose-400 hover:bg-rose-950/30 transition">
                <i data-lucide="log-out" class="w-4 h-4"></i> Sign Out
            </a>
        </div>
    </aside>

    <main class="flex-1 p-4 md:p-8 max-w-7xl mx-auto w-full">
        <section id="tab-dashboard" class="tab-content space-y-6">
            <div class="bg-gradient-to-r from-blue-900/40 via-cyan-900/20 to-slate-900 border border-blue-800/40 p-6 rounded-2xl">
                <h2 class="text-2xl font-bold text-white mb-1">Welcome back, {{ user.name }}!</h2>
                <p class="text-slate-300 text-sm">System active. 9 official members registered on node network.</p>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-[#0d1424] p-4 rounded-xl border border-slate-800">
                    <p class="text-xs font-medium text-slate-400 uppercase">Family Members</p>
                    <p class="text-2xl font-extrabold text-white mt-1">{{ users|length }}</p>
                </div>
                <div class="bg-[#0d1424] p-4 rounded-xl border border-slate-800">
                    <p class="text-xs font-medium text-slate-400 uppercase">Active Projects</p>
                    <p class="text-2xl font-extrabold text-emerald-400 mt-1">{{ projects|length }}</p>
                </div>
                <div class="bg-[#0d1424] p-4 rounded-xl border border-slate-800">
                    <p class="text-xs font-medium text-slate-400 uppercase">Upcoming Meetings</p>
                    <p class="text-2xl font-extrabold text-amber-400 mt-1">{{ meetings|length }}</p>
                </div>
                <div class="bg-[#0d1424] p-4 rounded-xl border border-slate-800">
                    <p class="text-xs font-medium text-slate-400 uppercase">Pending Tasks</p>
                    <p class="text-2xl font-extrabold text-purple-400 mt-1">{{ tasks|length }}</p>
                </div>
            </div>
        </section>

        <section id="tab-members" class="tab-content hidden space-y-6">
            <h2 class="text-xl font-bold text-white">Obuogi Family Members</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                {% for u in users %}
                <div class="bg-[#0d1424] p-4 rounded-xl border border-slate-800 flex items-center gap-4">
                    <div class="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center font-bold text-cyan-400 border border-slate-700">
                        {{ u.name[0] }}
                    </div>
                    <div>
                        <h3 class="font-bold text-white text-sm">{{ u.name }}</h3>
                        <p class="text-xs text-slate-400">{{ u.title }}</p>
                        <span class="inline-block mt-1 text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300">{{ u.role }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <section id="tab-projects" class="tab-content hidden space-y-6">
            <h2 class="text-xl font-bold text-white">Projects Directory</h2>
            <div class="bg-[#0d1424] border border-slate-800 rounded-xl p-8 text-center">
                <i data-lucide="folder-kanban" class="w-12 h-12 text-slate-600 mx-auto mb-3"></i>
                <h3 class="font-bold text-white mb-1">No Projects Created Yet</h3>
                <p class="text-xs text-slate-400 max-w-sm mx-auto">Database state clean. Ready for family project planning.</p>
            </div>
        </section>

        <section id="tab-meetings" class="tab-content hidden space-y-6">
            <h2 class="text-xl font-bold text-white">Family Meetings</h2>
            <div class="bg-[#0d1424] border border-slate-800 rounded-xl p-8 text-center">
                <i data-lucide="calendar" class="w-12 h-12 text-slate-600 mx-auto mb-3"></i>
                <h3 class="font-bold text-white mb-1">No Meetings Scheduled</h3>
                <p class="text-xs text-slate-400 max-w-sm mx-auto">Schedule family gather-ups and discussions.</p>
            </div>
        </section>

        <section id="tab-tasks" class="tab-content hidden space-y-6">
            <h2 class="text-xl font-bold text-white">Task Management</h2>
            <div class="bg-[#0d1424] border border-slate-800 rounded-xl p-8 text-center">
                <i data-lucide="check-square" class="w-12 h-12 text-slate-600 mx-auto mb-3"></i>
                <h3 class="font-bold text-white mb-1">No Active Tasks</h3>
                <p class="text-xs text-slate-400 max-w-sm mx-auto">Assign and track actionable responsibilities.</p>
            </div>
        </section>

        <section id="tab-finance" class="tab-content hidden space-y-6">
            <h2 class="text-xl font-bold text-white">Treasury & Finance</h2>
            <div class="bg-[#0d1424] border border-slate-800 rounded-xl p-8 text-center">
                <i data-lucide="wallet" class="w-12 h-12 text-slate-600 mx-auto mb-3"></i>
                <h3 class="font-bold text-white mb-1">Financial Module</h3>
                <p class="text-xs text-slate-400 max-w-sm mx-auto">Track contributions, budgets, and investments.</p>
            </div>
        </section>
    </main>

    <script>
        lucide.createIcons();
        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('-translate-x-full');
        }
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('bg-slate-800', 'text-white'));
            const targetTab = document.getElementById('tab-' + tabId);
            const targetBtn = document.getElementById('btn-' + tabId);
            if (targetTab) targetTab.classList.remove('hidden');
            if (targetBtn) targetBtn.classList.add('bg-slate-800', 'text-white');
            if (window.innerWidth < 768) {
                document.getElementById('sidebar').classList.add('-translate-x-full');
            }
        }
    </script>
</body>
</html>"""

with open('templates/dashboard.html', 'w') as f:
    f.write(dashboard_html)

runner_py = """from bottle import route, run, request, response, redirect, jinja2_template
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
    users = conn.execute("SELECT * FROM users").fetchall()
    projects = conn.execute("SELECT * FROM projects").fetchall()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    meetings = conn.execute("SELECT * FROM meetings").fetchall()
    conn.close()
    return jinja2_template('templates/dashboard.html', user=dict(user), users=users, projects=projects, tasks=tasks, meetings=meetings)

@route('/logout')
def logout():
    response.delete_cookie('user_name', path='/')
    redirect('/')

print("[+] Server starting at http://127.0.0.1:8000...")
run(host='127.0.0.1', port=8000, quiet=False)
"""

with open('local_runner.py', 'w') as f:
    f.write(runner_py)

print("[✓] Setup script executed cleanly!")
