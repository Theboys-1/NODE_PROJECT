import sqlite3
import os

# 1. Database Initialization
conn = sqlite3.connect('node.db')
c = conn.cursor()

# Drop existing tables to rebuild with full schema
for table in ['users', 'projects', 'tasks', 'meetings', 'vault', 'decisions', 'history']:
    c.execute(f'DROP TABLE IF EXISTS {table}')

# Users Table (Rich Profiles)
c.execute('''CREATE TABLE users (
    id INTEGER PRIMARY KEY,
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
    ('Felix Ochieng', 'Family Chairman (Admin)', 'admin', '@Felix', 
     'MSc in Project Management & Governance', 
     'Executive Strategy Director & Senior Project Lead', 
     'Overall administration, constitutional governance, financial authorization, and long-term asset management.', 
     'Serving as head of the executive council, leading key development initiatives.', 'from-pink-600 to-rose-600'),
    
    ('Gabriel Aloka', 'Digital Architect (User)', 'user', '@Gabriel', 
     'BSc in Computer Science & Systems Engineering', 
     'Senior Software Architect & Systems Administrator', 
     'Architecture of NODE platform, system security, digital archives, and technical infrastructure.', 
     'Lead developer of the NODE system and manager of digital family records.', 'from-cyan-500 to-blue-600'),
    
    ('Elisha Ouma', 'Vice Chairman (User)', 'user', '@Elisha', 
     'BA in Public Administration & Policy', 
     'Operations Manager & Regional Coordinator', 
     'Deputizing executive duties, logistics coordination, and dispute resolution.', 
     'Coordinates operational affairs across regional family branches.', 'from-amber-500 to-yellow-600'),
    
    ('Collins Odwar', 'Family Secretary (User)', 'user', '@Collins', 
     'BSc in Information & Records Management', 
     'Corporate Communications Specialist', 
     'Official communications, meeting minutes, document vault archiving, and assembly scheduling.', 
     'Custodian of official family documentation and meeting records.', 'from-orange-500 to-amber-600'),
    
    ('Judith Katiba', 'Family Member (User)', 'user', '@Judith', 
     'Diploma in Community Development', 
     'Community Outreach Lead', 
     'Welfare program coordination, member outreach, and event management.', 
     'Manages welfare funds and family reunion logistics.', 'from-purple-500 to-indigo-600'),
    
    ('Esther Joan', 'Education Lead (User)', 'user', '@Esther', 
     'Master of Education (M.Ed)', 
     'Academic Consultant & Education Strategist', 
     'Youth education mentorship, academic progress tracking, and skill workshops.', 
     'Directs the EduCare platform and youth mentorship programs.', 'from-sky-500 to-blue-500'),
    
    ('Joan Atieno', 'Health Advisor (User)', 'user', '@Joan', 
     'BSc in Nursing & Public Health', 
     'Healthcare Practitioner', 
     'Family wellness policy, medical emergency support, and health awareness.', 
     'Leads health assistance projects and wellness initiatives.', 'from-rose-500 to-pink-500'),
    
    ('Meshack Obuogi', 'Agri-Business Lead (User)', 'user', '@Meshack', 
     'BSc in Agricultural Economics', 
     'Agribusiness Consultant & Property Manager', 
     'Land resource management, agricultural ventures, and real estate development.', 
     'Oversees farming investments and physical property assets.', 'from-emerald-500 to-teal-600'),
    
    ('Obuogi Parents', 'Advisory Council (User)', 'user', '@Parents', 
     'Elders Governance Council', 
     'Cultural Custodians & Senior Advisors', 
     'Ancestral wisdom, cultural preservation, high-level mediation, and family blessings.', 
     'Provides foundational advice and governance oversight to the executive council.', 'from-indigo-600 to-purple-800')
]

for m in members:
    c.execute('INSERT INTO users (name, title, role, password, education, career, responsibilities, bio, avatar_color) VALUES (?,?,?,?,?,?,?,?,?)', m)

# Projects Table
c.execute('''CREATE TABLE projects (
    id INTEGER PRIMARY KEY, title TEXT, leader TEXT, progress INTEGER, status TEXT, icon TEXT, color TEXT
)''')
projects_data = [
    ('Agri-Tech Solution', 'Gabriel Aloka', 75, 'Smart farming information system', 'sprout', 'bg-emerald-600'),
    ('EduCare Platform', 'Esther Joan', 45, 'Student support and learning resources', 'graduation-cap', 'bg-blue-600'),
    ('HealthAssist', 'Joan Atieno', 20, 'Basic healthcare decision support', 'heart-pulse', 'bg-rose-600'),
    ('Family Business', 'Elisha Ouma', 10, 'Investment and economic growth', 'briefcase', 'bg-purple-600')
]
c.executemany('INSERT INTO projects (title, leader, progress, status, icon, color) VALUES (?,?,?,?,?,?)', projects_data)

# Tasks Table
c.execute('''CREATE TABLE tasks (
    id INTEGER PRIMARY KEY, title TEXT, category TEXT, priority TEXT, due_date TEXT, status TEXT
)''')
tasks_data = [
    ('Prepare project report', 'Agri-Tech', 'High', 'Oct 10, 2026', 'Pending'),
    ('Research AI tools for study', 'Personal Development', 'Medium', 'Oct 12, 2026', 'Pending'),
    ('Attend family meeting', 'Family Affairs', 'Low', 'Oct 15, 2026', 'Pending'),
    ('Review annual welfare budget', 'Finance', 'Medium', 'Oct 01, 2026', 'Completed'),
    ('Update land registry documents', 'Property', 'High', 'Sep 25, 2026', 'Completed')
]
c.executemany('INSERT INTO tasks (title, category, priority, due_date, status) VALUES (?,?,?,?,?)', tasks_data)

# Meetings Table
c.execute('''CREATE TABLE meetings (
    id INTEGER PRIMARY KEY, title TEXT, date_badge TEXT, time TEXT, location TEXT
)''')
meetings_data = [
    ('Family Development Meeting', 'OCT 15', '10:00 AM - 12:00 PM', 'Family Centre'),
    ('Project Progress Review', 'OCT 28', '2:00 PM - 4:00 PM', 'Online / Zoom')
]
c.executemany('INSERT INTO meetings (title, date_badge, time, location) VALUES (?,?,?,?)', meetings_data)

# Vault Documents Table
c.execute('''CREATE TABLE vault (
    id INTEGER PRIMARY KEY, title TEXT, uploader TEXT, date TEXT, ext TEXT
)''')
vault_data = [
    ('Family_Constitution.pdf', 'Felix Ochieng', 'Oct 5, 2026', 'pdf'),
    ('Project_Plan.docx', 'Gabriel Aloka', 'Oct 3, 2026', 'doc'),
    ('Education_Resources.pdf', 'Esther Joan', 'Sep 28, 2026', 'pdf'),
    ('Meeting_Minutes.pdf', 'Collins Odwar', 'Sep 20, 2026', 'pdf'),
    ('Land_Title_Deed_Plot402.pdf', 'Meshack Obuogi', 'Sep 15, 2026', 'pdf'),
    ('Annual_Financial_Report.xlsx', 'Felix Ochieng', 'Sep 10, 2026', 'xls'),
    ('Welfare_Guidelines_2026.pdf', 'Judith Katiba', 'Aug 30, 2026', 'pdf'),
    ('Health_Insurance_Policy.pdf', 'Joan Atieno', 'Aug 22, 2026', 'pdf'),
    ('AgriTech_Architecture.png', 'Gabriel Aloka', 'Aug 18, 2026', 'img'),
    ('Youth_Mentorship_Roster.xlsx', 'Esther Joan', 'Aug 12, 2026', 'xls'),
    ('Family_Tree_Archive.pdf', 'Obuogi Parents', 'Jul 29, 2026', 'pdf'),
    ('Asset_Inventory_2026.docx', 'Elisha Ouma', 'Jul 15, 2026', 'doc')
]
c.executemany('INSERT INTO vault (title, uploader, date, ext) VALUES (?,?,?,?)', vault_data)

conn.commit()
conn.close()

# 2. Write UI Template
os.makedirs('templates', exist_ok=True)

dashboard_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NODE // New Obuogi Development</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-[#050914] text-slate-100 font-sans antialiased min-h-screen flex flex-col">

    <!-- TOP HEADER NAVBAR -->
    <header class="bg-[#0a1020]/90 backdrop-blur-md border-b border-slate-800/80 sticky top-0 z-40 px-4 py-3 flex items-center justify-between">
        <div class="flex items-center gap-3">
            <button onclick="toggleSidebar()" class="md:hidden p-1.5 text-slate-300 hover:text-white bg-slate-800/60 rounded-lg">
                <i data-lucide="menu" class="w-5 h-5"></i>
            </button>
            <div class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 via-blue-600 to-indigo-600 flex items-center justify-center font-extrabold text-white text-lg shadow-lg shadow-cyan-500/20">
                    <i data-lucide="hexagon" class="w-5 h-5 fill-cyan-400/30"></i>
                </div>
                <div>
                    <span class="font-extrabold tracking-wider text-base text-white">NODE</span>
                    <span class="hidden sm:inline text-xs text-slate-400 ml-2 font-light">New Obuogi Development</span>
                </div>
            </div>
        </div>

        <div class="hidden lg:block italic text-xs text-slate-400 font-serif">
            "Rooted in Faith. Built on Family. Driven by Development."
        </div>

        <div class="flex items-center gap-3">
            <div class="relative">
                <button class="p-2 text-slate-400 hover:text-white bg-slate-800/40 rounded-full relative">
                    <i data-lucide="bell" class="w-4 h-4"></i>
                    <span class="absolute top-1 right-1 w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
                </button>
            </div>
            
            <div onclick="openCurrentProfile()" class="flex items-center gap-2.5 bg-slate-800/50 hover:bg-slate-800 border border-slate-700/60 rounded-full pl-1.5 pr-3 py-1 cursor-pointer transition">
                <div class="w-7 h-7 rounded-full bg-cyan-600 flex items-center justify-center font-bold text-xs text-white">
                    {{ user.name[0] }}
                </div>
                <div class="text-left hidden sm:block">
                    <p class="text-xs font-bold text-white leading-none">{{ user.name }}</p>
                    <p class="text-[10px] text-slate-400 leading-tight mt-0.5">{{ user.title }}</p>
                </div>
                <i data-lucide="chevron-down" class="w-3.5 h-3.5 text-slate-400"></i>
            </div>
        </div>
    </header>

    <div class="flex-1 flex overflow-hidden">
        
        <!-- SIDEBAR NAVIGATION -->
        <aside id="sidebar" class="fixed inset-y-0 left-0 transform -translate-x-full md:relative md:translate-x-0 transition-transform duration-200 ease-in-out w-60 bg-[#080d1a] border-r border-slate-800/80 p-4 flex flex-col justify-between z-30 shrink-0 h-[calc(100vh-57px)] overflow-y-auto">
            <div class="space-y-6">
                <div>
                    <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wider px-3 mb-2">Main Menu</p>
                    <nav class="space-y-1">
                        <button onclick="switchTab('dashboard')" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-blue-600/20 hover:text-white transition active-tab bg-blue-600 text-white" id="btn-dashboard">
                            <i data-lucide="layout-dashboard" class="w-4 h-4 text-cyan-400"></i> Dashboard
                        </button>
                        <button onclick="openCurrentProfile()" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-blue-600/20 hover:text-white transition">
                            <i data-lucide="user" class="w-4 h-4 text-slate-400"></i> My Profile
                        </button>
                        <button onclick="switchTab('roster')" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-blue-600/20 hover:text-white transition" id="btn-roster">
                            <i data-lucide="users" class="w-4 h-4 text-blue-400"></i> Family Roster
                        </button>
                        <button onclick="switchTab('meetings')" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-blue-600/20 hover:text-white transition" id="btn-meetings">
                            <i data-lucide="calendar" class="w-4 h-4 text-emerald-400"></i> Meetings
                        </button>
                        <button onclick="switchTab('projects')" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-blue-600/20 hover:text-white transition" id="btn-projects">
                            <i data-lucide="bar-chart-2" class="w-4 h-4 text-indigo-400"></i> Projects
                        </button>
                        <button onclick="switchTab('tasks')" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-blue-600/20 hover:text-white transition" id="btn-tasks">
                            <i data-lucide="check-circle" class="w-4 h-4 text-cyan-400"></i> My Tasks
                        </button>
                        <button onclick="switchTab('vault')" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-blue-600/20 hover:text-white transition" id="btn-vault">
                            <i data-lucide="folder" class="w-4 h-4 text-amber-400"></i> Vault
                        </button>
                    </nav>
                </div>

                <div>
                    <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wider px-3 mb-2">System</p>
                    <nav class="space-y-1">
                        <button onclick="switchTab('settings')" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-slate-800 hover:text-white transition" id="btn-settings">
                            <i data-lucide="settings" class="w-4 h-4 text-slate-400"></i> Settings
                        </button>
                        <a href="/logout" class="flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium text-rose-400 hover:bg-rose-950/30 transition">
                            <i data-lucide="log-out" class="w-4 h-4"></i> Logout
                        </a>
                    </nav>
                </div>
            </div>

            <div class="pt-6 border-t border-slate-800/60 mt-6">
                <p class="text-[11px] text-slate-400 italic leading-snug">"Stronger together, building a better tomorrow."</p>
                <p class="text-[10px] text-slate-500 mt-2 font-mono">— Obuogi Family</p>
            </div>
        </aside>

        <!-- MAIN DASHBOARD CONTENT CONTAINER -->
        <main class="flex-1 p-4 md:p-6 overflow-y-auto max-w-7xl mx-auto w-full space-y-6">

            <!-- TAB 1: MAIN DASHBOARD -->
            <section id="tab-dashboard" class="tab-content space-y-6">

                <!-- HERO WELCOME BANNER -->
                <div class="relative rounded-2xl overflow-hidden border border-blue-500/20 bg-gradient-to-r from-blue-950 via-[#0a1630] to-[#070d1d] p-6 md:p-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-6 shadow-xl">
                    <div class="space-y-2 max-w-xl z-10">
                        <h1 class="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
                            Welcome back, {{ user.name }}! 👋
                        </h1>
                        <p class="text-sm text-cyan-300/80 font-medium">
                            Family • Knowledge • Progress • Legacy
                        </p>
                    </div>

                    <div class="bg-slate-900/80 backdrop-blur border border-slate-700/50 p-4 rounded-xl max-w-xs w-full z-10">
                        <p class="text-xs italic text-slate-300">"Small steps of progress build great things."</p>
                        <p class="text-[10px] text-cyan-400 font-mono mt-1 text-right">— NODE System</p>
                    </div>

                    <!-- Ambient Glow -->
                    <div class="absolute -right-10 -bottom-10 w-60 h-60 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>
                </div>

                <!-- TOP 5 METRIC CARDS -->
                <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5">
                    <div onclick="switchTab('roster')" class="bg-[#0b1222] border border-slate-800/80 hover:border-blue-500/50 p-4 rounded-xl cursor-pointer transition group">
                        <div class="flex items-center justify-between">
                            <div class="w-9 h-9 rounded-lg bg-blue-600/20 flex items-center justify-center text-blue-400 group-hover:bg-blue-600 group-hover:text-white transition">
                                <i data-lucide="users" class="w-5 h-5"></i>
                            </div>
                        </div>
                        <p class="text-2xl font-black text-white mt-3">{{ users|length }}</p>
                        <p class="text-xs text-slate-400 font-medium">Family Members</p>
                        <p class="text-[10px] text-blue-400 mt-1 flex items-center gap-1 group-hover:underline">View Roster →</p>
                    </div>

                    <div onclick="switchTab('meetings')" class="bg-[#0b1222] border border-slate-800/80 hover:border-emerald-500/50 p-4 rounded-xl cursor-pointer transition group">
                        <div class="flex items-center justify-between">
                            <div class="w-9 h-9 rounded-lg bg-emerald-600/20 flex items-center justify-center text-emerald-400 group-hover:bg-emerald-600 group-hover:text-white transition">
                                <i data-lucide="calendar" class="w-5 h-5"></i>
                            </div>
                        </div>
                        <p class="text-2xl font-black text-white mt-3">{{ meetings|length }}</p>
                        <p class="text-xs text-slate-400 font-medium">Upcoming Meetings</p>
                        <p class="text-[10px] text-emerald-400 mt-1 flex items-center gap-1 group-hover:underline">View Meetings →</p>
                    </div>

                    <div onclick="switchTab('projects')" class="bg-[#0b1222] border border-slate-800/80 hover:border-purple-500/50 p-4 rounded-xl cursor-pointer transition group">
                        <div class="flex items-center justify-between">
                            <div class="w-9 h-9 rounded-lg bg-purple-600/20 flex items-center justify-center text-purple-400 group-hover:bg-purple-600 group-hover:text-white transition">
                                <i data-lucide="bar-chart-2" class="w-5 h-5"></i>
                            </div>
                        </div>
                        <p class="text-2xl font-black text-white mt-3">{{ projects|length }}</p>
                        <p class="text-xs text-slate-400 font-medium">Active Projects</p>
                        <p class="text-[10px] text-purple-400 mt-1 flex items-center gap-1 group-hover:underline">View Projects →</p>
                    </div>

                    <div onclick="switchTab('tasks')" class="bg-[#0b1222] border border-slate-800/80 hover:border-amber-500/50 p-4 rounded-xl cursor-pointer transition group">
                        <div class="flex items-center justify-between">
                            <div class="w-9 h-9 rounded-lg bg-amber-600/20 flex items-center justify-center text-amber-400 group-hover:bg-amber-600 group-hover:text-white transition">
                                <i data-lucide="check-circle" class="w-5 h-5"></i>
                            </div>
                        </div>
                        <p class="text-2xl font-black text-white mt-3">{{ tasks|length }}</p>
                        <p class="text-xs text-slate-400 font-medium">Your Tasks</p>
                        <p class="text-[10px] text-amber-400 mt-1 flex items-center gap-1 group-hover:underline">View Tasks →</p>
                    </div>

                    <div onclick="switchTab('vault')" class="bg-[#0b1222] border border-slate-800/80 hover:border-cyan-500/50 p-4 rounded-xl cursor-pointer transition group">
                        <div class="flex items-center justify-between">
                            <div class="w-9 h-9 rounded-lg bg-cyan-600/20 flex items-center justify-center text-cyan-400 group-hover:bg-cyan-600 group-hover:text-white transition">
                                <i data-lucide="folder" class="w-5 h-5"></i>
                            </div>
                        </div>
                        <p class="text-2xl font-black text-white mt-3">{{ vault|length }}</p>
                        <p class="text-xs text-slate-400 font-medium">Vault Documents</p>
                        <p class="text-[10px] text-cyan-400 mt-1 flex items-center gap-1 group-hover:underline">View Vault →</p>
                    </div>
                </div>

                <!-- MIDDLE GRID: TASKS + MEETINGS + QUICK LINKS -->
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

                    <!-- MY TASKS WIDGET -->
                    <div class="lg:col-span-5 bg-[#0b1222] border border-slate-800/80 rounded-2xl p-5 space-y-4">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <i data-lucide="check-circle" class="w-5 h-5 text-blue-400"></i>
                                <h2 class="font-bold text-white text-sm">My Tasks</h2>
                            </div>
                            <button onclick="switchTab('tasks')" class="text-xs text-blue-400 hover:underline font-medium">View All →</button>
                        </div>

                        <!-- Task Category Pills -->
                        <div class="flex gap-2 border-b border-slate-800 pb-2">
                            <button class="px-3 py-1 rounded-full text-xs font-medium bg-blue-600 text-white">Pending (3)</button>
                            <button class="px-3 py-1 rounded-full text-xs font-medium bg-slate-800/80 text-slate-400 hover:text-white">Completed (2)</button>
                        </div>

                        <div class="space-y-3">
                            {% for t in tasks if t.status == 'Pending' %}
                            <div class="p-3 bg-[#080d1a] border border-slate-800 rounded-xl flex items-center justify-between gap-3">
                                <div class="flex items-center gap-3">
                                    <input type="checkbox" class="rounded border-slate-700 bg-slate-900 text-blue-600 focus:ring-0">
                                    <div>
                                        <p class="text-xs font-bold text-white">{{ t.title }}</p>
                                        <p class="text-[10px] text-slate-400 mt-0.5"><i data-lucide="tag" class="w-3 h-3 inline"></i> {{ t.category }}</p>
                                    </div>
                                </div>
                                <div class="text-right">
                                    <span class="text-[10px] font-bold px-2 py-0.5 rounded-full {% if t.priority == 'High' %}bg-rose-950 text-rose-400 border border-rose-800{% elif t.priority == 'Medium' %}bg-amber-950 text-amber-400 border border-amber-800{% else %}bg-emerald-950 text-emerald-400 border border-emerald-800{% endif %}">
                                        {{ t.priority }}
                                    </span>
                                    <p class="text-[10px] font-mono text-slate-500 mt-1">Due: {{ t.due_date }}</p>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>

                    <!-- UPCOMING MEETINGS WIDGET -->
                    <div class="lg:col-span-4 bg-[#0b1222] border border-slate-800/80 rounded-2xl p-5 space-y-4">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <i data-lucide="calendar" class="w-5 h-5 text-emerald-400"></i>
                                <h2 class="font-bold text-white text-sm">Upcoming Meetings</h2>
                            </div>
                            <button onclick="switchTab('meetings')" class="text-xs text-blue-400 hover:underline font-medium">View All →</button>
                        </div>

                        <div class="space-y-3">
                            {% for m in meetings %}
                            <div class="p-3.5 bg-[#080d1a] border border-slate-800 rounded-xl flex items-center gap-3.5 hover:border-slate-700 transition">
                                <div class="bg-blue-950 border border-blue-800/60 rounded-xl px-3 py-2 text-center shrink-0">
                                    <p class="text-[10px] font-extrabold text-blue-400 uppercase tracking-wide">{{ m.date_badge.split()[0] }}</p>
                                    <p class="text-lg font-black text-white leading-none mt-0.5">{{ m.date_badge.split()[1] }}</p>
                                </div>
                                <div>
                                    <h3 class="font-bold text-white text-xs">{{ m.title }}</h3>
                                    <p class="text-[10px] text-slate-400 mt-1"><i data-lucide="clock" class="w-3 h-3 inline"></i> {{ m.time }}</p>
                                    <p class="text-[10px] text-slate-400"><i data-lucide="map-pin" class="w-3 h-3 inline"></i> {{ m.location }}</p>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>

                    <!-- QUICK LINKS WIDGET -->
                    <div class="lg:col-span-3 bg-[#0b1222] border border-slate-800/80 rounded-2xl p-5 space-y-4">
                        <div class="flex items-center gap-2">
                            <i data-lucide="zap" class="w-5 h-5 text-amber-400"></i>
                            <h2 class="font-bold text-white text-sm">Quick Links</h2>
                        </div>

                        <div class="space-y-2">
                            <button onclick="switchTab('roster')" class="w-full p-2.5 bg-[#080d1a] hover:bg-slate-800 border border-slate-800 rounded-xl flex items-center justify-between text-xs font-medium text-slate-300 hover:text-white transition">
                                <span class="flex items-center gap-2.5"><i data-lucide="users" class="w-4 h-4 text-blue-400"></i> View Family Roster</span>
                                <i data-lucide="chevron-right" class="w-4 h-4 text-slate-500"></i>
                            </button>
                            <button onclick="switchTab('projects')" class="w-full p-2.5 bg-[#080d1a] hover:bg-slate-800 border border-slate-800 rounded-xl flex items-center justify-between text-xs font-medium text-slate-300 hover:text-white transition">
                                <span class="flex items-center gap-2.5"><i data-lucide="bar-chart-2" class="w-4 h-4 text-purple-400"></i> View All Projects</span>
                                <i data-lucide="chevron-right" class="w-4 h-4 text-slate-500"></i>
                            </button>
                            <button onclick="switchTab('vault')" class="w-full p-2.5 bg-[#080d1a] hover:bg-slate-800 border border-slate-800 rounded-xl flex items-center justify-between text-xs font-medium text-slate-300 hover:text-white transition">
                                <span class="flex items-center gap-2.5"><i data-lucide="folder" class="w-4 h-4 text-cyan-400"></i> Access Vault Docs</span>
                                <i data-lucide="chevron-right" class="w-4 h-4 text-slate-500"></i>
                            </button>
                            <button onclick="switchTab('meetings')" class="w-full p-2.5 bg-[#080d1a] hover:bg-slate-800 border border-slate-800 rounded-xl flex items-center justify-between text-xs font-medium text-slate-300 hover:text-white transition">
                                <span class="flex items-center gap-2.5"><i data-lucide="file-text" class="w-4 h-4 text-emerald-400"></i> View Meeting Minutes</span>
                                <i data-lucide="chevron-right" class="w-4 h-4 text-slate-500"></i>
                            </button>
                        </div>
                    </div>

                </div>

                <!-- BOTTOM GRID: FAMILY PROJECTS + ROSTER QUICK VIEW + RECENT VAULT -->
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

                    <!-- FAMILY PROJECTS -->
                    <div class="lg:col-span-5 bg-[#0b1222] border border-slate-800/80 rounded-2xl p-5 space-y-4">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <i data-lucide="bar-chart-2" class="w-5 h-5 text-indigo-400"></i>
                                <h2 class="font-bold text-white text-sm">Family Projects</h2>
                            </div>
                            <button onclick="switchTab('projects')" class="text-xs text-blue-400 hover:underline font-medium">View All →</button>
                        </div>

                        <div class="space-y-4">
                            {% for p in projects %}
                            <div class="p-3 bg-[#080d1a] border border-slate-800 rounded-xl space-y-2">
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center gap-2.5">
                                        <div class="w-7 h-7 rounded-lg {{ p.color }} flex items-center justify-center text-white">
                                            <i data-lucide="{{ p.icon }}" class="w-4 h-4"></i>
                                        </div>
                                        <div>
                                            <h3 class="font-bold text-white text-xs">{{ p.title }}</h3>
                                            <p class="text-[10px] text-slate-400">Leader: {{ p.leader }}</p>
                                        </div>
                                    </div>
                                    <span class="text-xs font-black font-mono text-cyan-400">{{ p.progress }}%</span>
                                </div>
                                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                                    <div class="bg-gradient-to-r from-blue-500 to-cyan-400 h-full rounded-full" style="width: {{ p.progress }}%"></div>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>

                    <!-- FAMILY ROSTER (QUICK VIEW) -->
                    <div class="lg:col-span-4 bg-[#0b1222] border border-slate-800/80 rounded-2xl p-5 space-y-4">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <i data-lucide="users" class="w-5 h-5 text-blue-400"></i>
                                <h2 class="font-bold text-white text-sm">Family Roster (Quick View)</h2>
                            </div>
                            <button onclick="switchTab('roster')" class="text-xs text-blue-400 hover:underline font-medium">View All →</button>
                        </div>

                        <div class="space-y-2.5 max-h-72 overflow-y-auto pr-1">
                            {% for u in users %}
                            <div onclick='openMemberModal({{ u|tojson|safe }})' class="p-2.5 bg-[#080d1a] hover:bg-slate-800/80 border border-slate-800/80 rounded-xl flex items-center justify-between cursor-pointer transition">
                                <div class="flex items-center gap-3">
                                    <div class="w-8 h-8 rounded-full bg-gradient-to-tr {{ u.avatar_color }} flex items-center justify-center text-xs font-bold text-white">
                                        {{ u.name[0] }}
                                    </div>
                                    <div>
                                        <h3 class="font-bold text-white text-xs">{{ u.name }}</h3>
                                        <p class="text-[10px] text-slate-400">{{ u.title }}</p>
                                    </div>
                                </div>
                                {% if u.name == user.name %}
                                <span class="px-2 py-0.5 bg-blue-600 text-white text-[9px] font-bold rounded-full">You</span>
                                {% endif %}
                            </div>
                            {% endfor %}
                        </div>
                    </div>

                    <!-- RECENT VAULT FILES -->
                    <div class="lg:col-span-3 bg-[#0b1222] border border-slate-800/80 rounded-2xl p-5 space-y-4">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <i data-lucide="folder" class="w-5 h-5 text-amber-400"></i>
                                <h2 class="font-bold text-white text-sm">Recent Vault Files</h2>
                            </div>
                            <button onclick="switchTab('vault')" class="text-xs text-blue-400 hover:underline font-medium">View All →</button>
                        </div>

                        <div class="space-y-2.5">
                            {% for v in vault[:4] %}
                            <div class="p-2.5 bg-[#080d1a] border border-slate-800 rounded-xl flex items-center justify-between">
                                <div class="flex items-center gap-2.5 truncate">
                                    <i data-lucide="file-text" class="w-4 h-4 text-rose-400 shrink-0"></i>
                                    <div class="truncate">
                                        <p class="text-xs font-bold text-white truncate">{{ v.title }}</p>
                                        <p class="text-[9px] text-slate-500">By {{ v.uploader }}</p>
                                    </div>
                                </div>
                                <button onclick="switchTab('vault')" class="px-2 py-1 bg-slate-800 hover:bg-blue-600 text-[10px] font-medium text-slate-300 hover:text-white rounded transition">View</button>
                            </div>
                            {% endfor %}
                        </div>
                    </div>

                </div>

            </section>

            <!-- TAB 2: FULL FAMILY ROSTER WITH DETAILED CARD CLICK -->
            <section id="tab-roster" class="tab-content hidden space-y-6">
                <div class="flex justify-between items-center">
                    <div>
                        <h2 class="text-xl font-extrabold text-white">Obuogi Family Directory</h2>
                        <p class="text-xs text-slate-400">Tap any profile card to view detailed career, education & role breakdown.</p>
                    </div>
                    <span class="px-3 py-1 bg-blue-950 text-blue-300 border border-blue-800 rounded-full text-xs font-mono">9 Official Members</span>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {% for u in users %}
                    <div onclick='openMemberModal({{ u|tojson|safe }})' class="bg-[#0b1222] border border-slate-800 hover:border-blue-500/60 p-5 rounded-2xl cursor-pointer transition group relative overflow-hidden">
                        <div class="flex items-start gap-4">
                            <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr {{ u.avatar_color }} flex items-center justify-center text-lg font-bold text-white shadow-lg shrink-0">
                                {{ u.name[0] }}
                            </div>
                            <div class="space-y-1">
                                <h3 class="font-bold text-white text-base group-hover:text-blue-400 transition">{{ u.name }}</h3>
                                <p class="text-xs font-medium text-cyan-400">{{ u.title }}</p>
                                <p class="text-[11px] text-slate-400 line-clamp-1 mt-1"><i data-lucide="briefcase" class="w-3 h-3 inline"></i> {{ u.career }}</p>
                            </div>
                        </div>

                        <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px]">
                            <span class="text-slate-400 font-mono">{{ u.role }}</span>
                            <span class="text-blue-400 font-medium group-hover:translate-x-1 transition flex items-center gap-1">Full Profile →</span>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </section>

            <!-- TAB 3: PROJECTS TAB -->
            <section id="tab-projects" class="tab-content hidden space-y-6">
                <h2 class="text-xl font-bold text-white">Active Family Projects</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {% for p in projects %}
                    <div class="bg-[#0b1222] border border-slate-800 p-6 rounded-2xl space-y-4">
                        <div class="flex justify-between items-start">
                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 rounded-xl {{ p.color }} flex items-center justify-center text-white">
                                    <i data-lucide="{{ p.icon }}" class="w-5 h-5"></i>
                                </div>
                                <div>
                                    <h3 class="font-bold text-white text-base">{{ p.title }}</h3>
                                    <p class="text-xs text-slate-400">Lead: {{ p.leader }}</p>
                                </div>
                            </div>
                            <span class="text-sm font-extrabold font-mono text-cyan-400">{{ p.progress }}%</span>
                        </div>
                        <p class="text-xs text-slate-300">{{ p.status }}</p>
                        <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                            <div class="bg-gradient-to-r from-blue-500 to-cyan-400 h-full rounded-full" style="width: {{ p.progress }}%"></div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </section>

            <!-- TAB 4: MEETINGS TAB -->
            <section id="tab-meetings" class="tab-content hidden space-y-6">
                <h2 class="text-xl font-bold text-white">Assembly & Meetings</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {% for m in meetings %}
                    <div class="bg-[#0b1222] border border-slate-800 p-6 rounded-2xl flex items-start gap-4">
                        <div class="bg-blue-950 border border-blue-800 rounded-xl p-3 text-center shrink-0">
                            <p class="text-xs font-black text-blue-400">{{ m.date_badge.split()[0] }}</p>
                            <p class="text-2xl font-black text-white mt-0.5">{{ m.date_badge.split()[1] }}</p>
                        </div>
                        <div class="space-y-1">
                            <h3 class="font-bold text-white text-base">{{ m.title }}</h3>
                            <p class="text-xs text-slate-300"><i data-lucide="clock" class="w-3.5 h-3.5 inline"></i> {{ m.time }}</p>
                            <p class="text-xs text-slate-400"><i data-lucide="map-pin" class="w-3.5 h-3.5 inline"></i> {{ m.location }}</p>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </section>

            <!-- TAB 5: TASKS TAB -->
            <section id="tab-tasks" class="tab-content hidden space-y-6">
                <h2 class="text-xl font-bold text-white">Task Management</h2>
                <div class="bg-[#0b1222] border border-slate-800 rounded-2xl p-6 space-y-4">
                    {% for t in tasks %}
                    <div class="p-4 bg-[#080d1a] border border-slate-800 rounded-xl flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <input type="checkbox" {% if t.status == 'Completed' %}checked{% endif %} class="rounded border-slate-700 bg-slate-900 text-blue-600">
                            <div>
                                <p class="text-sm font-bold text-white {% if t.status == 'Completed' %}line-through text-slate-500{% endif %}">{{ t.title }}</p>
                                <p class="text-xs text-slate-400 mt-0.5">{{ t.category }}</p>
                            </div>
                        </div>
                        <div class="text-right">
                            <span class="text-xs px-2.5 py-0.5 rounded-full font-bold {% if t.priority == 'High' %}bg-rose-950 text-rose-400 border border-rose-800{% else %}bg-amber-950 text-amber-400 border border-amber-800{% endif %}">{{ t.priority }}</span>
                            <p class="text-xs font-mono text-slate-500 mt-1">{{ t.due_date }}</p>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </section>

            <!-- TAB 6: VAULT TAB -->
            <section id="tab-vault" class="tab-content hidden space-y-6">
                <h2 class="text-xl font-bold text-white">Document Vault Directory</h2>
                <div class="bg-[#0b1222] border border-slate-800 rounded-2xl overflow-hidden">
                    <table class="w-full text-left text-xs text-slate-300">
                        <thead class="bg-[#080d1a] text-slate-400 border-b border-slate-800">
                            <tr>
                                <th class="p-4">Document Title</th>
                                <th class="p-4">Uploader</th>
                                <th class="p-4">Date Uploaded</th>
                                <th class="p-4 text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for v in vault %}
                            <tr class="border-b border-slate-800/60 hover:bg-slate-800/30">
                                <td class="p-4 font-bold text-white flex items-center gap-2"><i data-lucide="file-text" class="w-4 h-4 text-rose-400"></i> {{ v.title }}</td>
                                <td class="p-4">{{ v.uploader }}</td>
                                <td class="p-4 font-mono text-slate-400">{{ v.date }}</td>
                                <td class="p-4 text-right"><button class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-500">Download</button></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- TAB 7: SETTINGS TAB -->
            <section id="tab-settings" class="tab-content hidden space-y-6">
                <h2 class="text-xl font-bold text-white">System Settings</h2>
                <div class="bg-[#0b1222] border border-slate-800 rounded-2xl p-6 space-y-4">
                    <div class="flex justify-between items-center pb-4 border-b border-slate-800">
                        <div>
                            <p class="font-bold text-white text-sm">Target UI Blueprint</p>
                            <p class="text-xs text-slate-400">Match active photo design layout & mobile responsive grid</p>
                        </div>
                        <span class="px-3 py-1 bg-emerald-950 text-emerald-400 border border-emerald-800 rounded-full text-xs font-mono">Matched</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <div>
                            <p class="font-bold text-white text-sm">Database Engine</p>
                            <p class="text-xs text-slate-400">SQLite3 (`node.db` with seeded Obuogi records)</p>
                        </div>
                        <span class="px-3 py-1 bg-blue-950 text-blue-400 border border-blue-800 rounded-full text-xs font-mono">Connected</span>
                    </div>
                </div>
            </section>

        </main>
    </div>

    <!-- FOOTER TAGLINE -->
    <footer class="bg-[#080d1a] border-t border-slate-800 px-4 py-2 text-center text-[11px] text-slate-500 flex flex-col sm:flex-row justify-between items-center gap-1 font-mono">
        <span>🛡️ NODE — Secure Family Management System</span>
        <span>Connected to Local Network (Termux)</span>
    </footer>

    <!-- INTERACTIVE MEMBER DETAIL MODAL -->
    <div id="memberModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 hidden flex items-center justify-center p-4">
        <div class="bg-[#0b1222] border border-slate-700/80 rounded-2xl w-full max-w-lg p-6 space-y-5 relative shadow-2xl overflow-y-auto max-h-[90vh]">
            <button onclick="closeMemberModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white p-1 rounded-lg bg-slate-800">
                <i data-lucide="x" class="w-5 h-5"></i>
            </button>
            
            <div class="flex items-center gap-4 border-b border-slate-800 pb-4">
                <div id="modalAvatar" class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-cyan-600 to-blue-600 flex items-center justify-center text-xl font-bold text-white shadow-lg shrink-0">
                    M
                </div>
                <div>
                    <h3 id="modalName" class="text-xl font-extrabold text-white">Member Name</h3>
                    <p id="modalTitle" class="text-xs text-cyan-400 font-mono font-bold mt-0.5">Title</p>
                    <span id="modalRole" class="inline-block mt-1 text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 uppercase font-mono">Role</span>
                </div>
            </div>

            <div class="space-y-3.5 text-xs">
                <div>
                    <p class="text-slate-400 font-bold uppercase tracking-wider text-[10px] flex items-center gap-1.5"><i data-lucide="briefcase" class="w-3.5 h-3.5 text-teal-400"></i> Career & Current Occupation</p>
                    <p id="modalCareer" class="text-white mt-1 bg-[#050914] p-3 rounded-xl border border-slate-800 font-medium">...</p>
                </div>

                <div>
                    <p class="text-slate-400 font-bold uppercase tracking-wider text-[10px] flex items-center gap-1.5"><i data-lucide="graduation-cap" class="w-3.5 h-3.5 text-sky-400"></i> Academic Qualifications & Education</p>
                    <p id="modalEdu" class="text-white mt-1 bg-[#050914] p-3 rounded-xl border border-slate-800 font-medium">...</p>
                </div>

                <div>
                    <p class="text-slate-400 font-bold uppercase tracking-wider text-[10px] flex items-center gap-1.5"><i data-lucide="shield-check" class="w-3.5 h-3.5 text-amber-400"></i> Position Responsibilities</p>
                    <p id="modalResp" class="text-white mt-1 bg-[#050914] p-3 rounded-xl border border-slate-800 leading-relaxed">...</p>
                </div>

                <div>
                    <p class="text-slate-400 font-bold uppercase tracking-wider text-[10px] flex items-center gap-1.5"><i data-lucide="info" class="w-3.5 h-3.5 text-blue-400"></i> Council Bio & Notes</p>
                    <p id="modalBio" class="text-slate-300 mt-1 leading-relaxed">...</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        lucide.createIcons();

        const currentUser = {{ user|tojson|safe }};

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('-translate-x-full');
        }

        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('bg-blue-600', 'text-white'));

            const targetTab = document.getElementById('tab-' + tabId);
            const targetBtn = document.getElementById('btn-' + tabId);

            if (targetTab) targetTab.classList.remove('hidden');
            if (targetBtn) targetBtn.classList.add('bg-blue-600', 'text-white');

            if (window.innerWidth < 768) {
                document.getElementById('sidebar').classList.add('-translate-x-full');
            }
        }

        function openMemberModal(member) {
            document.getElementById('modalAvatar').innerText = member.name[0];
            document.getElementById('modalName').innerText = member.name;
            document.getElementById('modalTitle').innerText = member.title;
            document.getElementById('modalRole').innerText = member.role;
            document.getElementById('modalCareer').innerText = member.career;
            document.getElementById('modalEdu').innerText = member.education;
            document.getElementById('modalResp').innerText = member.responsibilities;
            document.getElementById('modalBio').innerText = member.bio;
            
            document.getElementById('memberModal').classList.remove('hidden');
        }

        function openCurrentProfile() {
            openMemberModal(currentUser);
        }

        function closeMemberModal() {
            document.getElementById('memberModal').classList.add('hidden');
        }
    </script>
</body>
</html>"""

with open('templates/dashboard.html', 'w') as f:
    f.write(dashboard_html)

# 3. Server Script
runner_code = """from bottle import route, run, request, response, redirect, jinja2_template
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
"""

with open('local_runner.py', 'w') as f:
    f.write(runner_code)

print("[✓] Complete target design script executed successfully!")
