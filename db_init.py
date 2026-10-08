import sqlite3, os

conn = sqlite3.connect('node.db')
c = conn.cursor()

for t in ['users', 'committees', 'projects', 'tasks', 'meetings', 'vault']:
    c.execute(f'DROP TABLE IF EXISTS {t}')

c.execute('''CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, title TEXT, role TEXT, password TEXT,
    education TEXT, career TEXT, responsibilities TEXT, bio TEXT, avatar_color TEXT
)''')

members = [
    ('Parents', 'Advisory Council', 'user', '@Parents', 'Elders Council & Ancestral Wisdom', 'Family Foundation & Mentorship Custodians', 'Foundation of experience, wisdom, guidance, family history, values, and mentorship.', 'Our parents have spent years building and guiding the family.', 'from-indigo-600 to-purple-800'),
    ('Felix Ochieng Obuogi', 'Family Chairman', 'admin', '@Felix', 'Public-Sector & Administrative Governance', 'Public Sector Lead & Family Administration', 'Leadership, coordination, public-sector experience, accountability, family decision-making.', 'Serves as Family Chairman leading overall governance.', 'from-pink-600 to-rose-600'),
    ('Judith Katiba', 'Family Member', 'user', '@Judith', 'Family Relations & Community Support', 'Community Support & Relationship Building', 'Family support, experience, relationship building, guidance, community connection.', 'Provides guidance and community connections across the family.', 'from-purple-500 to-indigo-600'),
    ('Elisha Ouma', 'Vice Chairman', 'user', '@Elisha', 'Economic Development & Opportunity Networking', 'Operations, Networking & Economic Opportunities', 'Opportunity identification, economic development, networking, external opportunities.', 'Serves as Vice Chairman focusing on opportunity identification.', 'from-amber-500 to-yellow-600'),
    ('Collins Odwar', 'Family Secretary', 'user', '@Collins', 'Kisii University (Agricultural Education and Extension)', 'Administration, Communications & Educational Initiatives', 'Administration, documentation, communication, education initiatives.', 'Serves as Family Secretary managing documentation and communication.', 'from-orange-500 to-amber-600'),
    ('Esther Joan', 'Family Member', 'user', '@Esther', 'Maasai Mara University (Education Science)', 'Educator & Youth Development Specialist', 'Education, teaching, mentorship, youth development.', 'Drives education, teaching, mentorship, and youth programs.', 'from-sky-500 to-blue-500'),
    ('Gabriel Aloka Obuogi', 'NODE Digital Architect / Developer', 'admin', '@Gabriel', 'Kisii University (BSc Computer Science)', 'Software Developer, AI, Cybersecurity & System Architect', 'Software development, AI, Cybersecurity, Data management, Digital transformation.', '"THE TECHNOLOGY IS MINE TO DEVELOP, BUT THE FAMILY VISION BELONGS TO THE FAMILY."', 'from-cyan-500 to-blue-600'),
    ('Joan Atieno', 'Family Member', 'user', '@Joan', 'Homa Bay Polytechnic (Diploma in Food Technology)', 'Food Technologist & Agricultural Entrepreneur', 'Food technology, agricultural opportunities, processing, entrepreneurship.', 'Focuses on food technology and agricultural processing.', 'from-rose-500 to-pink-500'),
    ('Meshack Obuogi', 'Family Member', 'user', '@Meshack', 'Catholic Church Seminary (Theology Student)', 'Theological Scholar, Values & Community Service', 'Values, faith, spiritual development, service, community connection.', 'Drives spiritual development, values, faith, and community service.', 'from-emerald-500 to-teal-600')
]
c.executemany('INSERT INTO users (name, title, role, password, education, career, responsibilities, bio, avatar_color) VALUES (?,?,?,?,?,?,?,?,?)', members)

c.execute('CREATE TABLE committees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, mandate TEXT, lead TEXT)')
c.executemany('INSERT INTO committees (name, mandate, lead) VALUES (?,?,?)', [
    ('Education & Career', 'Scholarships, jobs, mentorship, and academic growth', 'Esther Joan'),
    ('Finance & Investment', 'Finances, investments, project budgets, and records', 'Felix Ochieng Obuogi'),
    ('Projects & Development', 'Project oversight and execution tracking', 'Elisha Ouma'),
    ('Technology & Digital', 'NODE software development, cybersecurity, and data management', 'Gabriel Aloka Obuogi'),
    ('Faith & Community Service', 'Values, spiritual development, and community impact', 'Meshack Obuogi')
])

c.execute('CREATE TABLE projects (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, leader TEXT, progress INTEGER, status TEXT, icon TEXT, color TEXT)')
c.executemany('INSERT INTO projects (title, leader, progress, status, icon, color) VALUES (?,?,?,?,?,?)', [
    ('Establish NODE Platform', 'Gabriel Aloka Obuogi', 85, 'Phase 4 MVP Development & Deployment', 'code', 'bg-cyan-600'),
    ('EduCare & Mentorship Initiative', 'Esther Joan', 40, 'Student tracking and study support', 'graduation-cap', 'bg-blue-600'),
    ('Agri-Business & Processing', 'Joan Atieno', 25, 'Food processing and agricultural opportunities', 'sprout', 'bg-emerald-600'),
    ('Family Economic Investment Plan', 'Elisha Ouma', 15, 'Economic development & networking opportunities', 'briefcase', 'bg-purple-600')
])

c.execute('CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, category TEXT, priority TEXT, due_date TEXT, status TEXT)')
c.executemany('INSERT INTO tasks (title, category, priority, due_date, status) VALUES (?,?,?,?,?)', [
    ('Finalize NODE System Proposal Approval', 'Governance', 'High', 'Oct 15, 2026', 'Pending'),
    ('Draft Family Constitution Charter', 'Legal & Policy', 'High', 'Oct 20, 2026', 'Pending'),
    ('Compile Academic Profiles for Students', 'Education', 'Medium', 'Oct 25, 2026', 'Pending'),
    ('Review First Quarter Contributions', 'Finance', 'Medium', 'Nov 01, 2026', 'Pending')
])

c.execute('CREATE TABLE meetings (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date_badge TEXT, time TEXT, location TEXT)')
c.executemany('INSERT INTO meetings (title, date_badge, time, location) VALUES (?,?,?,?)', [
    ('NODE System Adoption Assembly', 'OCT 18', '10:00 AM - 12:30 PM', 'Family Centre / Online Hybrid'),
    ('Executive Council Progress Review', 'NOV 05', '2:00 PM - 4:00 PM', 'Virtual Assembly Room')
])

c.execute('CREATE TABLE vault (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, uploader TEXT, date TEXT, ext TEXT)')
c.executemany('INSERT INTO vault (title, uploader, date, ext) VALUES (?,?,?,?)', [
    ('NODE_Family_Development_System_Proposal.pdf', 'Gabriel Aloka Obuogi', 'Oct 8, 2026', 'pdf'),
    ('Obuogi_Family_Core_Values_Charter.pdf', 'Felix Ochieng Obuogi', 'Oct 5, 2026', 'pdf'),
    ('Meeting_Minutes_Sept_2026.docx', 'Collins Odwar', 'Sep 28, 2026', 'doc')
])

conn.commit()
conn.close()
print("[✓] Database initialized cleanly!")
