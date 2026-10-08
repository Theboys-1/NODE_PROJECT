import os, sqlite3, json

os.makedirs('templates', exist_ok=True)
os.makedirs('uploads', exist_ok=True)

# 1. INITIALIZE DATABASE
conn = sqlite3.connect('node.db')
c = conn.cursor()

tables = ['users', 'projects', 'tasks', 'meetings', 'vault', 'announcements']
for t in tables:
    c.execute(f'DROP TABLE IF EXISTS {t}')

c.execute('''CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    title TEXT,
    role TEXT,
    password TEXT,
    education TEXT,
    career TEXT,
    responsibilities TEXT,
    bio TEXT,
    avatar_color TEXT
)''')

members = [
    ('Gabriel Aloka Obuogi', 'Digital Architect & Developer of Mancer AI', 'admin', '@Gabriel', 
     'Kisii University (BSc Computer Science)', 
     'Software Developer, AI, Cybersecurity & System Architect', 
     'Software development, Mancer AI engine, Cybersecurity, System architecture.', 
     '"THE TECHNOLOGY IS MINE TO DEVELOP, BUT THE FAMILY VISION BELONGS TO THE FAMILY."', 
     'from-cyan-500 to-blue-600'),

    ('Felix Ochieng Obuogi', 'Family Chairman', 'admin', '@Felix', 
     'Public-Sector & Administrative Governance', 
     'Public Sector Lead & Family Administration', 
     'Leadership, coordination, public-sector experience, accountability.', 
     'Serves as Family Chairman leading overall governance and strategic decision-making.', 
     'from-pink-600 to-rose-600'),

    ('Collins Odwar', 'Family Secretary', 'user', '@Collins', 
     'Kisii University (Agricultural Education and Extension)', 
     'Administration, Communications & Educational Initiatives', 
     'Administration, documentation, communication, education initiatives.', 
     'Serves as Family Secretary managing documentation and educational programs.', 
     'from-orange-500 to-amber-600'),

    ('Elisha Ouma', 'Vice Chairman', 'user', '@Elisha', 
     'Economic Development & Opportunity Networking', 
     'Operations, Networking & Economic Opportunities', 
     'Opportunity identification, economic development, networking.', 
     'Focuses on opportunity identification and economic growth.', 
     'from-amber-500 to-yellow-600'),

    ('Judith Katiba', 'Family Member', 'user', '@Judith', 
     'Family Relations & Community Support', 
     'Community Support & Relationship Building', 
     'Family support, experience, relationship building, guidance.', 
     'Provides guidance and relationship building across the family.', 
     'from-purple-500 to-indigo-600'),

    ('Esther Joan', 'Family Member', 'user', '@Esther', 
     'Maasai Mara University (Education Science)', 
     'Educator & Youth Development Specialist', 
     'Education, teaching, mentorship, youth development.', 
     'Drives education, teaching, mentorship, and youth programs.', 
     'from-sky-500 to-blue-500'),

    ('Joan Atieno', 'Family Member', 'user', '@Joan', 
     'Homa Bay Polytechnic (Diploma in Food Technology)', 
     'Food Technologist & Agricultural Entrepreneur', 
     'Food technology, agricultural processing, entrepreneurship.', 
     'Focuses on food technology and entrepreneurial ventures.', 
     'from-rose-500 to-pink-500'),

    ('Meshack Obuogi', 'Family Member', 'user', '@Meshack', 
     'Catholic Church Seminary (Theology Student)', 
     'Theological Scholar, Values & Community Service', 
     'Values, faith, spiritual development, community service.', 
     'Drives spiritual development, values, faith, and service.', 
     'from-emerald-500 to-teal-600'),

    ('Obuogi Parents', 'Advisory Council', 'user', '@Parents', 
     'Elders Council & Ancestral Wisdom', 
     'Family Foundation & Mentorship Custodians', 
     'Foundation of experience, wisdom, guidance, family history.', 
     'Our parents spent years building and guiding the family.', 
     'from-indigo-600 to-purple-800')
]
c.executemany('INSERT INTO users (name, title, role, password, education, career, responsibilities, bio, avatar_color) VALUES (?,?,?,?,?,?,?,?,?)', members)

c.execute('CREATE TABLE projects (id INTEGER PRIMARY KEY, title TEXT, leader TEXT, progress INTEGER, status TEXT)')
projects = [
    ('Agri-Tech Solution', 'Gabriel Aloka Obuogi', 75, 'In Progress'),
    ('EduCare Support Platform', 'Esther Joan', 45, 'In Progress'),
    ('Family Business Initiative', 'Elisha Ouma', 20, 'Planning')
]
c.executemany('INSERT INTO projects (title, leader, progress, status) VALUES (?,?,?,?)', projects)

c.execute('CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT, assignee TEXT, category TEXT, priority TEXT, due_date TEXT, status TEXT)')
tasks = [
    ('Research AI tools for family', 'Gabriel Aloka Obuogi', 'Tech', 'High', 'Oct 12, 2026', 'Pending'),
    ('Prepare project report', 'Collins Odwar', 'Admin', 'Medium', 'Oct 18, 2026', 'Pending'),
    ('Attend family meeting', 'All Members', 'Affairs', 'Low', 'Oct 15, 2026', 'Pending'),
    ('Review welfare constitution', 'Felix Ochieng Obuogi', 'Governance', 'High', 'Oct 05, 2026', 'Completed')
]
c.executemany('INSERT INTO tasks (title, assignee, category, priority, due_date, status) VALUES (?,?,?,?,?,?)', tasks)

c.execute('CREATE TABLE meetings (id INTEGER PRIMARY KEY, title TEXT, date_badge TEXT, time TEXT, location TEXT)')
meetings = [
    ('Family Development Meeting', 'OCT 15', '10:00 AM - 12:00 PM', 'Family Centre'),
    ('Project Progress Review', 'OCT 28', '2:00 PM - 4:00 PM', 'Online / Zoom')
]
c.executemany('INSERT INTO meetings (title, date_badge, time, location) VALUES (?,?,?,?)', meetings)

c.execute('CREATE TABLE vault (id INTEGER PRIMARY KEY, title TEXT, uploader TEXT, date TEXT)')
vault = [
    ('NODE_System_Proposal.pdf', 'Gabriel Aloka Obuogi', 'Oct 8, 2026'),
    ('Family_Constitution.pdf', 'Felix Ochieng Obuogi', 'Oct 5, 2026'),
    ('Meeting_Minutes.docx', 'Collins Odwar', 'Sep 28, 2026')
]
c.executemany('INSERT INTO vault (title, uploader, date) VALUES (?,?,?)', vault)

c.execute('CREATE TABLE announcements (id INTEGER PRIMARY KEY, title TEXT, author TEXT, category TEXT, date TEXT)')
announcements = [
    ('Family meeting next week', 'Felix Ochieng Obuogi', 'General', 'Oct 10, 2026'),
    ('Scholarship opportunities available', 'Collins Odwar', 'Education', 'Oct 8, 2026'),
    ('Agri-Tech Platform proposal ready', 'Gabriel Aloka Obuogi', 'Project', 'Oct 5, 2026')
]
c.executemany('INSERT INTO announcements (title, author, category, date) VALUES (?,?,?,?)', announcements)

conn.commit()
conn.close()

# 2. LOGIN TEMPLATE
login_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NODE // System Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#050914] text-slate-100 font-sans min-h-screen flex items-center justify-center p-4">
    <div class="bg-[#0b1222] border border-slate-800 rounded-2xl w-full max-w-md p-6 space-y-6 shadow-2xl">
        <div class="text-center space-y-2">
            <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-cyan-500 via-blue-600 to-indigo-600 flex items-center justify-center font-black text-white text-xl mx-auto shadow-lg shadow-cyan-500/20">N</div>
            <h1 class="text-xl font-black text-white tracking-wide">NODE System</h1>
            <p class="text-xs text-slate-400">Select profile to access Admin or Member Portal</p>
        </div>
        <form action="/login" method="POST" class="space-y-4">
            <div>
                <label class="block text-xs font-bold text-slate-400 uppercase mb-2">Family Member / Admin</label>
                <select name="name" class="w-full bg-[#050914] border border-slate-700 rounded-xl px-3 py-2.5 text-xs text-white focus:outline-none focus:border-cyan-500">
                    % for u in users:
                    <option value="{{ u['name'] }}">{{ u['name'] }} ({{ u['title'] }})</option>
                    % end
                </select>
            </div>
            <div>
                <label class="block text-xs font-bold text-slate-400 uppercase mb-2">Password</label>
                <input type="password" name="password" required placeholder="Enter profile password..." class="w-full bg-[#050914] border border-slate-700 rounded-xl px-3 py-2.5 text-xs text-white focus:outline-none focus:border-cyan-500">
            </div>
            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-500 font-bold text-white text-xs py-3 rounded-xl transition shadow-lg shadow-blue-600/30">
                Authenticate & Launch Portal
            </button>
        </form>
    </div>
</body>
</html>"""

with open('templates/login.html', 'w') as f:
    f.write(login_html)

# 3. MEMBER DASHBOARD TEMPLATE
dash_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NODE // Member Portal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-[#050914] text-slate-100 font-sans min-h-screen flex flex-col">

    <form id="globalUploadForm" action="/upload" method="POST" enctype="multipart/form-data" class="hidden">
        <input type="file" id="globalFileInput" name="document" onchange="document.getElementById('globalUploadForm').submit()">
    </form>

    <header class="bg-[#0a1020]/95 backdrop-blur border-b border-slate-800 sticky top-0 z-40 px-4 py-2.5 flex items-center justify-between">
        <div class="flex items-center gap-3">
            <button onclick="toggleSidebar()" class="md:hidden p-1.5 text-slate-300 hover:text-white bg-slate-800 rounded-lg"><i data-lucide="menu" class="w-5 h-5"></i></button>
            <div class="flex items-center gap-2">
                <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-cyan-500 via-blue-600 to-indigo-600 flex items-center justify-center font-black text-white text-base">N</div>
                <span class="font-extrabold text-sm text-white">NODE</span>
            </div>
        </div>

        <div class="hidden md:block text-xs text-slate-400 italic">"Rooted in Faith. Built on Family. Driven by Development."</div>

        <div class="flex items-center gap-3">
            % if user['role'] == 'admin':
            <a href="/admin" class="px-2.5 py-1 bg-purple-900/60 hover:bg-purple-800 border border-purple-600 text-purple-200 text-[10px] font-bold rounded-full transition">← Admin Portal</a>
            % end
            <span class="px-2.5 py-0.5 bg-blue-950 text-blue-300 border border-blue-800/60 text-[10px] font-mono font-bold rounded-full uppercase">Member Access</span>
            <div onclick="openEditProfileModal()" class="flex items-center gap-2 bg-slate-800/60 border border-slate-700 rounded-full pl-1.5 pr-3 py-1 cursor-pointer">
                <div class="w-6 h-6 rounded-full bg-cyan-600 flex items-center justify-center font-bold text-xs text-white">{{ user['name'][0] }}</div>
                <span class="text-xs font-bold text-white hidden sm:inline">{{ user['name'] }}</span>
            </div>
        </div>
    </header>

    <div class="flex-1 flex overflow-hidden">
        <aside id="sidebar" class="fixed inset-y-0 left-0 transform -translate-x-full md:relative md:translate-x-0 transition-transform w-56 bg-[#080d1a] border-r border-slate-800 p-4 flex flex-col justify-between z-30 shrink-0 h-[calc(100vh-53px)] overflow-y-auto">
            <div class="space-y-4">
                <p class="text-[10px] font-bold text-slate-500 uppercase px-2">Navigation</p>
                <nav class="space-y-1">
                    <button onclick="switchTab('dashboard')" class="nav-btn w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-blue-600/20 active-tab bg-blue-600 text-white" id="btn-dashboard"><i data-lucide="layout-dashboard" class="w-4 h-4 text-cyan-400"></i> Dashboard</button>
                    <button onclick="openEditProfileModal()" class="nav-btn w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-blue-600/20"><i data-lucide="user-cog" class="w-4 h-4 text-emerald-400"></i> Edit Profile</button>
                    <button onclick="triggerFileUpload()" class="nav-btn w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium text-amber-300 border border-amber-800/50 hover:bg-amber-950/40"><i data-lucide="upload-cloud" class="w-4 h-4 text-amber-400"></i> Upload Document</button>
                    <button onclick="switchTab('mancer')" class="nav-btn w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-bold text-cyan-300 border border-cyan-800/50 mt-1 hover:bg-cyan-950/40" id="btn-mancer"><i data-lucide="sparkles" class="w-4 h-4 text-cyan-400"></i> Mancer AI Engine</button>
                    <button onclick="switchTab('roster')" class="nav-btn w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-blue-600/20" id="btn-roster"><i data-lucide="users" class="w-4 h-4 text-blue-400"></i> Family Directory</button>
                    <button onclick="switchTab('meetings')" class="nav-btn w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-blue-600/20" id="btn-meetings"><i data-lucide="calendar" class="w-4 h-4 text-emerald-400"></i> Meetings</button>
                    <button onclick="switchTab('projects')" class="nav-btn w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-blue-600/20" id="btn-projects"><i data-lucide="bar-chart-2" class="w-4 h-4 text-indigo-400"></i> Projects</button>
                    <button onclick="switchTab('tasks')" class="nav-btn w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-blue-600/20" id="btn-tasks"><i data-lucide="check-circle" class="w-4 h-4 text-cyan-400"></i> My Tasks</button>
                    <button onclick="switchTab('vault')" class="nav-btn w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-blue-600/20" id="btn-vault"><i data-lucide="folder" class="w-4 h-4 text-amber-400"></i> Documents Vault</button>
                </nav>
            </div>
            <div class="pt-4 border-t border-slate-800 space-y-2">
                <a href="/logout" class="flex items-center gap-2 px-3 py-1.5 text-xs text-rose-400 hover:bg-rose-950/30 rounded-lg"><i data-lucide="log-out" class="w-4 h-4"></i> Logout</a>
                <p class="text-[10px] text-slate-500 font-mono">NODE System // Obuogi Development</p>
            </div>
        </aside>

        <main class="flex-1 p-4 md:p-6 overflow-y-auto max-w-7xl mx-auto w-full space-y-6">

            <section id="tab-dashboard" class="tab-content space-y-6">
                <div class="rounded-2xl border border-blue-500/20 bg-gradient-to-r from-blue-950 via-[#0a1630] to-[#070d1d] p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div>
                        <h1 class="text-2xl font-extrabold text-white">Welcome back, {{ user['name'] }}!</h1>
                        <p class="text-xs text-cyan-300 font-medium mt-1">Learn • Grow • Contribute • Build Our Future</p>
                    </div>
                    <div class="flex flex-wrap gap-2">
                        <button onclick="openEditProfileModal()" class="px-3.5 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold transition">Update Profile</button>
                        <button onclick="triggerFileUpload()" class="px-3.5 py-2 bg-amber-600 hover:bg-amber-500 text-white rounded-xl text-xs font-bold transition">📎 Upload File</button>
                        <button onclick="openPostModal()" class="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold transition">+ Post Concern / Notice</button>
                    </div>
                </div>

                <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
                    <div onclick="switchTab('tasks')" class="bg-[#0b1222] border border-slate-800 p-4 rounded-xl cursor-pointer hover:border-blue-500/50">
                        <span class="text-xs text-slate-400">My Tasks</span>
                        <p class="text-2xl font-black text-white mt-2">{{ len(tasks) }}</p>
                    </div>
                    <div onclick="switchTab('meetings')" class="bg-[#0b1222] border border-slate-800 p-4 rounded-xl cursor-pointer hover:border-emerald-500/50">
                        <span class="text-xs text-slate-400">My Meetings</span>
                        <p class="text-2xl font-black text-white mt-2">{{ len(meetings) }}</p>
                    </div>
                    <div onclick="switchTab('projects')" class="bg-[#0b1222] border border-slate-800 p-4 rounded-xl cursor-pointer hover:border-purple-500/50">
                        <span class="text-xs text-slate-400">My Projects</span>
                        <p class="text-2xl font-black text-white mt-2">{{ len(projects) }}</p>
                    </div>
                    <div onclick="switchTab('vault')" class="bg-[#0b1222] border border-slate-800 p-4 rounded-xl cursor-pointer hover:border-amber-500/50">
                        <span class="text-xs text-slate-400">Vault Files</span>
                        <p class="text-2xl font-black text-white mt-2">{{ len(vault) }}</p>
                    </div>
                </div>

                <div class="bg-[#0b1222] border border-slate-800 rounded-2xl p-5 space-y-4">
                    <div class="flex items-center justify-between">
                        <h2 class="font-bold text-white text-sm">Family Feeds & Member Concerns</h2>
                        <button onclick="openPostModal()" class="text-xs bg-emerald-600/20 text-emerald-400 border border-emerald-800 px-3 py-1 rounded-lg font-bold">+ Post Concern</button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        % for a in announcements:
                        <div class="p-3 bg-[#080d1a] border border-slate-800 rounded-xl space-y-1">
                            <div class="flex justify-between text-[9px] font-mono text-cyan-400 uppercase"><span>{{ a['category'] }}</span><span>{{ a['date'] }}</span></div>
                            <p class="text-xs font-bold text-white">{{ a['title'] }}</p>
                            <p class="text-[10px] text-slate-400">By: {{ a['author'] }}</p>
                        </div>
                        % end
                    </div>
                </div>
            </section>

            <section id="tab-mancer" class="tab-content hidden space-y-4">
                <div class="bg-gradient-to-r from-cyan-950 via-slate-900 to-blue-950 border border-cyan-800/60 p-5 rounded-2xl space-y-2">
                    <h2 class="text-lg font-bold text-white">Mancer AI // Intelligence Assistant</h2>
                    <p class="text-xs text-slate-300">Smart AI Assistant equipped with database intelligence, general world knowledge, and instant file text analysis.</p>
                </div>
                <div class="bg-[#0b1222] border border-slate-800 rounded-2xl p-4 h-96 flex flex-col justify-between">
                    <div id="mancerChat" class="overflow-y-auto space-y-3 text-xs p-2 flex-1">
                        <div class="p-3 bg-cyan-950/40 border border-cyan-800/50 rounded-xl text-cyan-200">
                            <strong>Mancer AI:</strong> Hello {{ user['name'] }}! I am Mancer AI. Ask me anything about NODE family records, project progress, tasks, OR any general science, programming, or world knowledge questions. You can also upload a document to analyze!
                        </div>
                    </div>

                    <div class="pt-3 border-t border-slate-800 space-y-2">
                        <div id="aiFilePreview" class="hidden text-[11px] text-amber-300 bg-amber-950/40 border border-amber-800 p-1.5 rounded-lg flex justify-between items-center">
                            <span id="aiFileName">File Attached</span>
                            <button onclick="clearAiFile()" class="text-rose-400 font-bold">✕ Remove</button>
                        </div>
                        <div class="flex gap-2">
                            <input type="file" id="mancerFileInput" class="hidden" onchange="handleAiFileSelect(event)">
                            <button onclick="document.getElementById('mancerFileInput').click()" class="px-3 py-2 bg-slate-800 border border-slate-700 text-amber-400 rounded-lg text-xs font-bold flex items-center gap-1 hover:bg-slate-700">
                                📎 <span class="hidden sm:inline">Attach</span>
                            </button>
                            <input id="mancerInput" type="text" placeholder="Ask Mancer AI anything or request file analysis..." class="flex-1 bg-[#050914] border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500" onkeydown="if(event.key==='Enter') sendMancerQuery()">
                            <button onclick="sendMancerQuery()" class="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 font-bold text-white text-xs rounded-lg">Ask AI</button>
                        </div>
                    </div>
                </div>
            </section>

            <section id="tab-roster" class="tab-content hidden space-y-4">
                <h2 class="text-lg font-bold text-white">Family Directory</h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    % for u in users:
                    <div onclick="showMember({{ u['id'] }})" class="bg-[#0b1222] border border-slate-800 p-4 rounded-xl cursor-pointer hover:border-blue-500/60 transition space-y-2">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr {{ u['avatar_color'] }} flex items-center justify-center font-bold text-white">{{ u['name'][0] }}</div>
                            <div>
                                <h3 class="font-bold text-white text-xs">{{ u['name'] }}</h3>
                                <p class="text-[10px] text-cyan-400 font-mono">{{ u['title'] }}</p>
                            </div>
                        </div>
                        <p class="text-xs text-slate-300 pt-2 border-t border-slate-800"><strong>Education:</strong> {{ u['education'] }}</p>
                    </div>
                    % end
                </div>
            </section>

            <section id="tab-vault" class="tab-content hidden space-y-4">
                <div class="flex justify-between items-center">
                    <h2 class="text-lg font-bold text-white">Documents Vault Repository</h2>
                    <button onclick="triggerFileUpload()" class="px-3.5 py-1.5 bg-amber-600 hover:bg-amber-500 text-white rounded-lg text-xs font-bold transition">📎 Upload Document</button>
                </div>
                <div class="bg-[#0b1222] border border-slate-800 rounded-xl overflow-hidden text-xs">
                    % for v in vault:
                    <div class="p-3 border-b border-slate-800 flex justify-between items-center text-white">
                        <span class="font-bold">{{ v['title'] }}</span>
                        <span class="text-slate-400">{{ v['uploader'] }} • {{ v['date'] }}</span>
                    </div>
                    % end
                </div>
            </section>

            <section id="tab-meetings" class="tab-content hidden space-y-4">
                <h2 class="text-lg font-bold text-white">Meetings & Assemblies</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    % for m in meetings:
                    <div class="bg-[#0b1222] border border-slate-800 p-4 rounded-xl flex items-center gap-4">
                        <div class="bg-blue-950 border border-blue-800 rounded-lg p-2 text-center shrink-0"><p class="text-xs font-bold text-blue-400">{{ m['date_badge'] }}</p></div>
                        <div>
                            <h3 class="font-bold text-white text-xs">{{ m['title'] }}</h3>
                            <p class="text-[11px] text-slate-400">{{ m['time'] }} • {{ m['location'] }}</p>
                        </div>
                    </div>
                    % end
                </div>
            </section>

            <section id="tab-projects" class="tab-content hidden space-y-4">
                <h2 class="text-lg font-bold text-white">Projects</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    % for p in projects:
                    <div class="bg-[#0b1222] border border-slate-800 p-4 rounded-xl space-y-2">
                        <div class="flex justify-between items-center"><h3 class="font-bold text-white text-xs">{{ p['title'] }}</h3><span class="text-xs font-mono text-cyan-400 font-bold">{{ p['progress'] }}%</span></div>
                        <p class="text-xs text-slate-400">Leader: {{ p['leader'] }}</p>
                    </div>
                    % end
                </div>
            </section>

            <section id="tab-tasks" class="tab-content hidden space-y-4">
                <h2 class="text-lg font-bold text-white">My Assigned Tasks</h2>
                <div class="bg-[#0b1222] border border-slate-800 rounded-2xl p-4 space-y-3">
                    % for t in tasks:
                    <div class="p-3 bg-[#080d1a] border border-slate-800 rounded-xl flex items-center justify-between">
                        <div>
                            <p class="text-xs font-bold text-white">{{ t['title'] }}</p>
                            <p class="text-[10px] text-slate-400 mt-0.5">Assignee: {{ t['assignee'] }}</p>
                        </div>
                        <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-950 text-amber-400 border border-amber-800">{{ t['priority'] }}</span>
                    </div>
                    % end
                </div>
            </section>

        </main>
    </div>

    <!-- MODALS -->
    <div id="memberModal" class="fixed inset-0 bg-black/80 z-50 hidden flex items-center justify-center p-4">
        <div class="bg-[#0b1222] border border-slate-700 rounded-2xl w-full max-w-lg p-5 space-y-3 relative">
            <button onclick="closeModal('memberModal')" class="absolute top-3 right-3 text-slate-400">✕</button>
            <h3 id="modalName" class="text-base font-bold text-white"></h3>
            <p id="modalTitle" class="text-xs text-cyan-400 font-mono"></p>
            <p id="modalEdu" class="text-xs text-slate-200 bg-[#050914] p-2 rounded border border-slate-800"></p>
            <p id="modalCareer" class="text-xs text-slate-200 bg-[#050914] p-2 rounded border border-slate-800"></p>
            <p id="modalResp" class="text-xs text-slate-200 bg-[#050914] p-2 rounded border border-slate-800"></p>
            <p id="modalBio" class="text-xs text-slate-300"></p>
        </div>
    </div>

    <div id="editProfileModal" class="fixed inset-0 bg-black/80 z-50 hidden flex items-center justify-center p-4">
        <div class="bg-[#0b1222] border border-slate-700 rounded-2xl w-full max-w-lg p-5 space-y-4 relative">
            <button onclick="closeModal('editProfileModal')" class="absolute top-3 right-3 text-slate-400">✕</button>
            <h3 class="text-base font-bold text-white border-b border-slate-800 pb-2">Update My Profile</h3>
            <form action="/update_profile" method="POST" class="space-y-3 text-xs">
                <div><label class="block text-slate-400 font-bold mb-1">Education</label><input type="text" name="education" value="{{ user['education'] }}" required class="w-full bg-[#050914] border border-slate-700 rounded-lg p-2 text-white"></div>
                <div><label class="block text-slate-400 font-bold mb-1">Career</label><input type="text" name="career" value="{{ user['career'] }}" required class="w-full bg-[#050914] border border-slate-700 rounded-lg p-2 text-white"></div>
                <div><label class="block text-slate-400 font-bold mb-1">Responsibilities</label><input type="text" name="responsibilities" value="{{ user['responsibilities'] }}" required class="w-full bg-[#050914] border border-slate-700 rounded-lg p-2 text-white"></div>
                <div><label class="block text-slate-400 font-bold mb-1">Bio</label><textarea name="bio" rows="2" required class="w-full bg-[#050914] border border-slate-700 rounded-lg p-2 text-white">{{ user['bio'] }}</textarea></div>
                <button type="submit" class="w-full bg-blue-600 font-bold text-white py-2 rounded-lg">Save Profile</button>
            </form>
        </div>
    </div>

    <div id="postModal" class="fixed inset-0 bg-black/80 z-50 hidden flex items-center justify-center p-4">
        <div class="bg-[#0b1222] border border-slate-700 rounded-2xl w-full max-w-md p-5 space-y-4 relative">
            <button onclick="closeModal('postModal')" class="absolute top-3 right-3 text-slate-400">✕</button>
            <h3 class="text-base font-bold text-white border-b border-slate-800 pb-2">Post Announcement or Notice</h3>
            <form action="/add_concern" method="POST" class="space-y-3 text-xs">
                <div>
                    <label class="block text-slate-400 font-bold mb-1">Category</label>
                    <select name="category" class="w-full bg-[#050914] border border-slate-700 rounded-lg p-2 text-white">
                        <option value="General Notice">General Notice</option>
                        <option value="Family Concern">Family Concern</option>
                        <option value="Project Idea">Project Idea</option>
                    </select>
                </div>
                <div>
                    <label class="block text-slate-400 font-bold mb-1">Subject</label>
                    <input type="text" name="title" required class="w-full bg-[#050914] border border-slate-700 rounded-lg p-2 text-white">
                </div>
                <button type="submit" class="w-full bg-emerald-600 font-bold text-white py-2 rounded-lg">Submit Post</button>
            </form>
        </div>
    </div>

    <script>
        lucide.createIcons();
        const usersList = {{! json_dumps(users) }};
        let attachedFileText = "";

        function triggerFileUpload() {
            document.getElementById('globalFileInput').click();
        }

        function toggleSidebar() { document.getElementById('sidebar').classList.toggle('-translate-x-full'); }
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            const targetTab = document.getElementById('tab-' + tabId);
            if (targetTab) targetTab.classList.remove('hidden');
            if (window.innerWidth < 768) document.getElementById('sidebar').classList.add('-translate-x-full');
        }

        function closeModal(id) { document.getElementById(id).classList.add('hidden'); }
        function openEditProfileModal() { document.getElementById('editProfileModal').classList.remove('hidden'); }
        function openPostModal() { document.getElementById('postModal').classList.remove('hidden'); }

        function showMember(id) {
            const m = usersList.find(u => u.id === id);
            if (!m) return;
            document.getElementById('modalName').innerText = m.name;
            document.getElementById('modalTitle').innerText = m.title;
            document.getElementById('modalEdu').innerText = m.education;
            document.getElementById('modalCareer').innerText = m.career;
            document.getElementById('modalResp').innerText = m.responsibilities;
            document.getElementById('modalBio').innerText = m.bio;
            document.getElementById('memberModal').classList.remove('hidden');
        }

        function handleAiFileSelect(event) {
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {
                attachedFileText = e.target.result;
                document.getElementById('aiFileName').innerText = "Attached: " + file.name;
                document.getElementById('aiFilePreview').classList.remove('hidden');
            };
            reader.readAsText(file);
        }

        function clearAiFile() {
            attachedFileText = "";
            document.getElementById('mancerFileInput').value = "";
            document.getElementById('aiFilePreview').classList.add('hidden');
        }

        async function sendMancerQuery() {
            const input = document.getElementById('mancerInput');
            const chat = document.getElementById('mancerChat');
            const text = input.value.trim();
            if (!text && !attachedFileText) return;

            const userMsg = document.createElement('div');
            userMsg.className = "p-2.5 bg-slate-800 border border-slate-700 rounded-xl text-white text-right";
            userMsg.innerText = text + (attachedFileText ? " [Attached File Analysis]" : "");
            chat.appendChild(userMsg);
            
            const payload = { query: text, file_text: attachedFileText };
            input.value = "";
            clearAiFile();
            chat.scrollTop = chat.scrollHeight;

            try {
                const res = await fetch('/api/mancer', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();

                const aiMsg = document.createElement('div');
                aiMsg.className = "p-3 bg-cyan-950/40 border border-cyan-800/50 rounded-xl text-cyan-200 leading-relaxed";
                aiMsg.innerHTML = "<strong>Mancer AI:</strong> " + data.reply;
                chat.appendChild(aiMsg);
            } catch (err) {
                const aiMsg = document.createElement('div');
                aiMsg.className = "p-3 bg-rose-950/40 border border-rose-800/50 rounded-xl text-rose-200";
                aiMsg.innerText = "Mancer AI: Connection lost. Re-run python app.py.";
                chat.appendChild(aiMsg);
            }
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>"""

with open('templates/dashboard.html', 'w') as f:
    f.write(dash_html)

# 4. ADMIN DASHBOARD TEMPLATE
admin_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NODE // Admin Portal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-[#050914] text-slate-100 font-sans min-h-screen flex flex-col">

    <form id="globalUploadFormAdmin" action="/upload" method="POST" enctype="multipart/form-data" class="hidden">
        <input type="file" id="globalFileInputAdmin" name="document" onchange="document.getElementById('globalUploadFormAdmin').submit()">
    </form>

    <header class="bg-[#0a1020]/95 backdrop-blur border-b border-purple-900/60 sticky top-0 z-40 px-4 py-2.5 flex items-center justify-between">
        <div class="flex items-center gap-3">
            <button onclick="toggleSidebar()" class="md:hidden p-1.5 text-slate-300 hover:text-white bg-slate-800 rounded-lg"><i data-lucide="menu" class="w-5 h-5"></i></button>
            <div class="flex items-center gap-2">
                <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-purple-600 via-indigo-600 to-cyan-500 flex items-center justify-center font-black text-white text-base">N</div>
                <span class="font-extrabold text-sm text-white">NODE</span>
            </div>
        </div>

        <div class="hidden md:block text-xs text-purple-300 font-mono italic">
            "ADMIN DASHBOARD // Full Governance • Portal Controller"
        </div>

        <div class="flex items-center gap-3">
            <a href="/dash" class="px-2.5 py-1 bg-cyan-950 hover:bg-cyan-900 border border-cyan-700 text-cyan-200 text-[10px] font-bold rounded-full transition">→ Member View</a>
            <span class="px-2.5 py-0.5 bg-purple-950 text-purple-300 border border-purple-700 text-[10px] font-mono font-bold rounded-full uppercase">Admin Portal</span>
            <div class="flex items-center gap-2 bg-purple-950/40 border border-purple-800 rounded-full pl-1.5 pr-3 py-1">
                <div class="w-6 h-6 rounded-full bg-purple-600 flex items-center justify-center font-bold text-xs text-white">{{ user['name'][0] }}</div>
                <span class="text-xs font-bold text-white hidden sm:inline">{{ user['name'] }}</span>
            </div>
        </div>
    </header>

    <div class="flex-1 flex overflow-hidden">
        <aside id="sidebar" class="fixed inset-y-0 left-0 transform -translate-x-full md:relative md:translate-x-0 transition-transform w-56 bg-[#080d1a] border-r border-slate-800 p-4 flex flex-col justify-between z-30 shrink-0 h-[calc(100vh-53px)] overflow-y-auto">
            <div class="space-y-4">
                <p class="text-[10px] font-bold text-purple-400 uppercase px-2 font-mono">Executive Controls</p>
                <nav class="space-y-1">
                    <button onclick="switchTab('admin-overview')" class="nav-btn w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-purple-600/20 active-tab bg-purple-600 text-white" id="btn-admin-overview"><i data-lucide="shield" class="w-4 h-4 text-purple-400"></i> Admin Overview</button>
                    <a href="/dash" class="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium text-cyan-300 bg-cyan-950/40 border border-cyan-800/50 hover:bg-cyan-900/60"><i data-lucide="layout" class="w-4 h-4 text-cyan-400"></i> Member Dashboard</a>
                    <button onclick="triggerFileUploadAdmin()" class="nav-btn w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium text-amber-300 border border-amber-800/50 hover:bg-amber-950/40"><i data-lucide="upload-cloud" class="w-4 h-4 text-amber-400"></i> Upload Document</button>
                    <button onclick="switchTab('roster')" class="nav-btn w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-purple-600/20" id="btn-roster"><i data-lucide="users" class="w-4 h-4 text-blue-400"></i> Member Directory</button>
                    <button onclick="switchTab('vault')" class="nav-btn w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-purple-600/20" id="btn-vault"><i data-lucide="folder" class="w-4 h-4 text-amber-400"></i> Vault Master</button>
                </nav>
            </div>
            <div class="pt-4 border-t border-slate-800 space-y-2">
                <a href="/logout" class="flex items-center gap-2 px-3 py-1.5 text-xs text-rose-400 hover:bg-rose-950/30 rounded-lg"><i data-lucide="log-out" class="w-4 h-4"></i> Logout Admin</a>
            </div>
        </aside>

        <main class="flex-1 p-4 md:p-6 overflow-y-auto max-w-7xl mx-auto w-full space-y-6">

            <section id="tab-admin-overview" class="tab-content space-y-6">
                <div class="rounded-2xl border border-purple-500/30 bg-gradient-to-r from-purple-950 via-[#120a2a] to-[#070d1d] p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div>
                        <h1 class="text-2xl font-extrabold text-white">Executive Control Portal</h1>
                        <p class="text-xs text-purple-300 font-medium mt-1">Full Governance Access • Database & Member Control</p>
                    </div>
                    <div class="flex gap-2">
                        <button onclick="triggerFileUploadAdmin()" class="px-3.5 py-2 bg-amber-600 hover:bg-amber-500 text-white rounded-xl text-xs font-bold transition">📎 Upload Document</button>
                        <button onclick="openPostModal()" class="px-3.5 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-xl text-xs font-bold transition">+ Broadcast Notice</button>
                    </div>
                </div>

                <div class="grid grid-cols-2 lg:grid-cols-5 gap-3">
                    <div class="bg-[#0b1222] border border-slate-800 p-4 rounded-xl"><span class="text-xs text-slate-400">Total Members</span><p class="text-2xl font-black text-white mt-1">{{ len(users) }}</p></div>
                    <div class="bg-[#0b1222] border border-slate-800 p-4 rounded-xl"><span class="text-xs text-slate-400">Active Projects</span><p class="text-2xl font-black text-cyan-400 mt-1">{{ len(projects) }}</p></div>
                    <div class="bg-[#0b1222] border border-slate-800 p-4 rounded-xl"><span class="text-xs text-slate-400">Assemblies</span><p class="text-2xl font-black text-emerald-400 mt-1">{{ len(meetings) }}</p></div>
                    <div class="bg-[#0b1222] border border-slate-800 p-4 rounded-xl"><span class="text-xs text-slate-400">Tasks</span><p class="text-2xl font-black text-amber-400 mt-1">{{ len(tasks) }}</p></div>
                    <div class="bg-[#0b1222] border border-slate-800 p-4 rounded-xl"><span class="text-xs text-slate-400">Vault Documents</span><p class="text-2xl font-black text-purple-400 mt-1">{{ len(vault) }}</p></div>
                </div>

                <div class="bg-[#0b1222] border border-slate-800 rounded-2xl p-5 space-y-4">
                    <h2 class="font-bold text-white text-sm">System Announcements & Notices</h2>
                    <div class="space-y-2">
                        % for a in announcements:
                        <div class="p-3 bg-[#080d1a] border border-slate-800 rounded-xl text-xs flex justify-between items-center">
                            <div><p class="font-bold text-white">{{ a['title'] }}</p><p class="text-[10px] text-slate-400">By: {{ a['author'] }}</p></div>
                            <span class="text-[10px] font-mono text-purple-400 font-bold uppercase">{{ a['category'] }}</span>
                        </div>
                        % end
                    </div>
                </div>
            </section>

            <section id="tab-roster" class="tab-content hidden space-y-4">
                <h2 class="text-lg font-bold text-white">Member Roster</h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    % for u in users:
                    <div class="bg-[#0b1222] border border-slate-800 p-4 rounded-xl space-y-2">
                        <div class="flex justify-between items-center"><h3 class="font-bold text-white text-xs">{{ u['name'] }}</h3><span class="text-[9px] font-mono px-2 py-0.5 rounded uppercase % if u['role']=='admin': bg-purple-950 text-purple-400 border border-purple-800 % else: bg-slate-800 text-slate-400 % end">{{ u['role'] }}</span></div>
                        <p class="text-[10px] text-cyan-400 font-mono">{{ u['title'] }}</p>
                        <p class="text-xs text-slate-300 mt-1">{{ u['education'] }}</p>
                    </div>
                    % end
                </div>
            </section>

            <section id="tab-vault" class="tab-content hidden space-y-4">
                <div class="flex justify-between items-center">
                    <h2 class="text-lg font-bold text-white">Master Vault Repository</h2>
                    <button onclick="triggerFileUploadAdmin()" class="px-3.5 py-1.5 bg-amber-600 text-white text-xs font-bold rounded-lg">📎 Upload Document</button>
                </div>
                <div class="bg-[#0b1222] border border-slate-800 rounded-xl text-xs">
                    % for v in vault:
                    <div class="p-3 border-b border-slate-800 flex justify-between text-white"><span>{{ v['title'] }}</span><span class="text-slate-400">{{ v['uploader'] }} • {{ v['date'] }}</span></div>
                    % end
                </div>
            </section>
        </main>
    </div>

    <!-- POST MODAL -->
    <div id="postModal" class="fixed inset-0 bg-black/80 z-50 hidden flex items-center justify-center p-4">
        <div class="bg-[#0b1222] border border-slate-700 rounded-2xl w-full max-w-md p-5 space-y-4 relative">
            <button onclick="closeModal('postModal')" class="absolute top-3 right-3 text-slate-400">✕</button>
            <h3 class="text-base font-bold text-white border-b border-slate-800 pb-2">Broadcast Executive Notice</h3>
            <form action="/add_concern" method="POST" class="space-y-3 text-xs">
                <div>
                    <label class="block text-slate-400 font-bold mb-1">Category</label>
                    <select name="category" class="w-full bg-[#050914] border border-slate-700 rounded-lg p-2 text-white">
                        <option value="Executive Announcement">Executive Announcement</option>
                        <option value="General Notice">General Notice</option>
                        <option value="Project Notice">Project Notice</option>
                    </select>
                </div>
                <div>
                    <label class="block text-slate-400 font-bold mb-1">Subject</label>
                    <input type="text" name="title" required class="w-full bg-[#050914] border border-slate-700 rounded-lg p-2 text-white">
                </div>
                <button type="submit" class="w-full bg-purple-600 font-bold text-white py-2 rounded-lg">Broadcast Post</button>
            </form>
        </div>
    </div>

    <script>
        lucide.createIcons();
        function triggerFileUploadAdmin() { document.getElementById('globalFileInputAdmin').click(); }
        function toggleSidebar() { document.getElementById('sidebar').classList.toggle('-translate-x-full'); }
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            const targetTab = document.getElementById('tab-' + tabId);
            if (targetTab) targetTab.classList.remove('hidden');
            if (window.innerWidth < 768) document.getElementById('sidebar').classList.add('-translate-x-full');
        }
        function closeModal(id) { document.getElementById(id).classList.add('hidden'); }
        function openPostModal() { document.getElementById('postModal').classList.remove('hidden'); }
    </script>
</body>
</html>"""

with open('templates/admin.html', 'w') as f:
    f.write(admin_html)

# 5. BACKEND APP LOGIC
app_code = """import os, sqlite3, json
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
"""

with open('app.py', 'w') as f:
    f.write(app_code)

print("[✓] All project files built successfully!")
