import sqlite3

conn = sqlite3.connect('node.db')
c = conn.cursor()

tables = ['users', 'projects', 'tasks', 'meetings', 'vault', 'announcements', 'goals', 'news']
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

    ('Collins Odwar', 'Family Secretary', 'user', '@Collins', 
     'Kisii University (Agricultural Education and Extension)', 
     'Administration, Communications & Educational Initiatives', 
     'Administration, documentation, communication, education initiatives.', 
     'Serves as Family Secretary managing documentation and educational programs.', 
     'from-orange-500 to-amber-600'),

    ('Felix Ochieng Obuogi', 'Family Chairman', 'admin', '@Felix', 
     'Public-Sector & Administrative Governance', 
     'Public Sector Lead & Family Administration', 
     'Leadership, coordination, public-sector experience, accountability.', 
     'Serves as Family Chairman leading overall governance and strategic decision-making.', 
     'from-pink-600 to-rose-600'),

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

# Projects
c.execute('CREATE TABLE projects (id INTEGER PRIMARY KEY, title TEXT, leader TEXT, progress INTEGER, status TEXT, icon TEXT, color TEXT)')
projects = [
    ('Agri-Tech Solution', 'Gabriel Aloka Obuogi', 75, 'In Progress', 'sprout', 'bg-emerald-600'),
    ('EduCare Support Platform', 'Esther Joan', 45, 'In Progress', 'graduation-cap', 'bg-blue-600'),
    ('Food Processing Venture', 'Joan Atieno', 20, 'Planning', 'utensils', 'bg-rose-600')
]
c.executemany('INSERT INTO projects (title, leader, progress, status, icon, color) VALUES (?,?,?,?,?,?)', projects)

# Tasks
c.execute('CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT, assignee TEXT, category TEXT, priority TEXT, due_date TEXT, status TEXT)')
tasks = [
    ('Research AI tools for family', 'Gabriel Aloka Obuogi', 'Tech', 'High', 'Oct 12, 2026', 'Pending'),
    ('Prepare project report', 'Collins Odwar', 'Admin', 'Medium', 'Oct 18, 2026', 'Pending'),
    ('Attend family meeting', 'All Members', 'Affairs', 'Low', 'Oct 15, 2026', 'Pending'),
    ('Review welfare constitution', 'Felix Ochieng Obuogi', 'Governance', 'High', 'Oct 05, 2026', 'Completed')
]
c.executemany('INSERT INTO tasks (title, assignee, category, priority, due_date, status) VALUES (?,?,?,?,?,?)', tasks)

# Meetings
c.execute('CREATE TABLE meetings (id INTEGER PRIMARY KEY, title TEXT, date_badge TEXT, time TEXT, location TEXT)')
meetings = [
    ('Family Development Meeting', 'OCT 15', '10:00 AM - 12:00 PM', 'Family Centre'),
    ('Project Progress Review', 'OCT 28', '2:00 PM - 4:00 PM', 'Online / Zoom')
]
c.executemany('INSERT INTO meetings (title, date_badge, time, location) VALUES (?,?,?,?)', meetings)

# Vault
c.execute('CREATE TABLE vault (id INTEGER PRIMARY KEY, title TEXT, uploader TEXT, date TEXT)')
vault = [
    ('NODE_System_Proposal.pdf', 'Gabriel Aloka Obuogi', 'Oct 8, 2026'),
    ('Family_Constitution.pdf', 'Felix Ochieng Obuogi', 'Oct 5, 2026'),
    ('Meeting_Minutes.docx', 'Collins Odwar', 'Sep 28, 2026')
]
c.executemany('INSERT INTO vault (title, uploader, date) VALUES (?,?,?)', vault)

# Announcements / Member Feed
c.execute('CREATE TABLE announcements (id INTEGER PRIMARY KEY, title TEXT, author TEXT, category TEXT, date TEXT)')
announcements = [
    ('Family meeting next week', 'Felix Ochieng Obuogi', 'General', 'Oct 10, 2026'),
    ('Scholarship opportunities available', 'Collins Odwar', 'Education', 'Oct 8, 2026'),
    ('Agri-Tech Platform proposal ready', 'Gabriel Aloka Obuogi', 'Project', 'Oct 5, 2026')
]
c.executemany('INSERT INTO announcements (title, author, category, date) VALUES (?,?,?,?)', announcements)

# Goals
c.execute('CREATE TABLE goals (id INTEGER PRIMARY KEY, title TEXT, status TEXT)')
goals = [
    ('Complete degree program with honors', 'In Progress'),
    ('Deploy Mancer AI & NODE web system', 'In Progress'),
    ('Apply for graduate tech / education roles', 'Pending')
]
c.executemany('INSERT INTO goals (title, status) VALUES (?,?)', goals)

# News
c.execute('CREATE TABLE news (id INTEGER PRIMARY KEY, title TEXT, date TEXT)')
news = [
    ('Esther Joan completed teaching practicum', 'Oct 1, 2026'),
    ('New opportunity: Tech Internship in CS', 'Sep 28, 2026'),
    ('NODE System proposal officially approved', 'Sep 25, 2026')
]
c.executemany('INSERT INTO news (title, date) VALUES (?,?)', news)

conn.commit()
conn.close()
print("[✓] Database initialized with dynamic Mancer AI & Member Feed schemas!")
