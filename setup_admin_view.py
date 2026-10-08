import os

os.makedirs('templates', exist_ok=True)

# 1. HTML/CSS Template for Full Admin View
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NODE // Admin Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #0a0f1d; color: #e2e8f0; font-family: system-ui, -apple-system, sans-serif; }
        .card { background-color: #121a2d; border: 1px solid #1e293b; border-radius: 0.75rem; }
    </style>
</head>
<body class="flex h-screen overflow-hidden">

    <!-- 16-Item Navigation Sidebar -->
    <aside class="w-64 bg-[#0d1424] border-r border-[#1e293b] flex flex-col justify-between p-4 overflow-y-auto">
        <div>
            <div class="flex items-center gap-3 mb-6 px-2">
                <div class="w-10 h-10 rounded-lg bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center font-bold text-xl text-white">N</div>
                <div>
                    <h1 class="font-bold text-lg leading-none text-white">NODE</h1>
                    <p class="text-[10px] text-cyan-400 mt-1 tracking-wider">NEW OBUOGI DEVELOPMENT</p>
                </div>
            </div>

            <nav class="space-y-1 text-sm">
                <a href="/dashboard" class="flex items-center gap-3 px-3 py-2 rounded-lg bg-blue-600 text-white font-medium"><i class="fa-solid fa-chart-pie w-5"></i> Dashboard</a>
                <a href="#members" class="flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-[#121a2d] hover:text-white rounded-lg"><i class="fa-solid fa-users w-5"></i> Family Members</a>
                <a href="#leadership" class="flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-[#121a2d] hover:text-white rounded-lg"><i class="fa-solid fa-crown w-5"></i> Leadership</a>
                <a href="#meetings" class="flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-[#121a2d] hover:text-white rounded-lg"><i class="fa-solid fa-calendar w-5"></i> Meetings</a>
                <a href="#projects" class="flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-[#121a2d] hover:text-white rounded-lg"><i class="fa-solid fa-diagram-project w-5"></i> Projects</a>
                <a href="#education" class="flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-[#121a2d] hover:text-white rounded-lg"><i class="fa-solid fa-graduation-cap w-5"></i> Education</a>
                <a href="#careers" class="flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-[#121a2d] hover:text-white rounded-lg"><i class="fa-solid fa-briefcase w-5"></i> Careers</a>
                <a href="#opportunities" class="flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-[#121a2d] hover:text-white rounded-lg"><i class="fa-solid fa-lightbulb w-5"></i> Opportunities</a>
                <a href="#finance" class="flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-[#121a2d] hover:text-white rounded-lg"><i class="fa-solid fa-wallet w-5"></i> Finance</a>
                <a href="#documents" class="flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-[#121a2d] hover:text-white rounded-lg"><i class="fa-solid fa-folder-open w-5"></i> Documents</a>
                <a href="#history" class="flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-[#121a2d] hover:text-white rounded-lg"><i class="fa-solid fa-book-bookmark w-5"></i> Family History</a>
                <a href="#decisions" class="flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-[#121a2d] hover:text-white rounded-lg"><i class="fa-solid fa-gavel w-5"></i> Decisions</a>
                <a href="#tasks" class="flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-[#121a2d] hover:text-white rounded-lg"><i class="fa-solid fa-list-check w-5"></i> Tasks</a>
                <a href="#reports" class="flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-[#121a2d] hover:text-white rounded-lg"><i class="fa-solid fa-chart-line w-5"></i> Reports</a>
                <a href="#ai" class="flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-[#121a2d] hover:text-white rounded-lg"><i class="fa-solid fa-robot w-5"></i> AI Assistant</a>
                <a href="#settings" class="flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-[#121a2d] hover:text-white rounded-lg"><i class="fa-solid fa-gear w-5"></i> Settings</a>
            </nav>
        </div>

        <a href="/logout" class="flex items-center gap-3 px-3 py-2 text-red-400 hover:bg-red-500/10 rounded-lg text-sm mt-4">
            <i class="fa-solid fa-right-from-bracket w-5"></i> Logout
        </a>
    </aside>

    <!-- Main Content Area -->
    <main class="flex-1 overflow-y-auto p-6 space-y-6">
        
        <!-- Top Header Banner -->
        <header class="card p-4 flex items-center justify-between border-l-4 border-l-cyan-400">
            <div>
                <div class="flex items-center gap-2">
                    <span class="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-400">ADMIN VIEW</span>
                    <span class="text-xs text-slate-400">Full Access • Manage • Coordinate • Lead</span>
                </div>
                <h2 class="text-xl font-bold text-white mt-1">Welcome back, {{ user.name }}!</h2>
                <p class="text-xs text-slate-400 italic">"Better decisions. Stronger family. Greater impact."</p>
            </div>
            <div class="flex items-center gap-4">
                <div class="text-right">
                    <p class="text-sm font-semibold text-white">{{ user.name }}</p>
                    <p class="text-xs text-cyan-400">{{ user.title }}</p>
                </div>
                <div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center font-bold text-white">
                    {{ user.name[0] }}
                </div>
            </div>
        </header>

        <!-- 5 Metric Cards -->
        <div class="grid grid-cols-5 gap-4">
            <div class="card p-4 border-l-4 border-l-blue-500">
                <p class="text-xs text-slate-400">Family Members</p>
                <h3 class="text-2xl font-bold text-white mt-1">9</h3>
            </div>
            <div class="card p-4 border-l-4 border-l-emerald-500">
                <p class="text-xs text-slate-400">Upcoming Meetings</p>
                <h3 class="text-2xl font-bold text-white mt-1">5</h3>
            </div>
            <div class="card p-4 border-l-4 border-l-purple-500">
                <p class="text-xs text-slate-400">Active Projects</p>
                <h3 class="text-2xl font-bold text-white mt-1">12</h3>
            </div>
            <div class="card p-4 border-l-4 border-l-amber-500">
                <p class="text-xs text-slate-400">Pending Tasks</p>
                <h3 class="text-2xl font-bold text-white mt-1">8</h3>
            </div>
            <div class="card p-4 border-l-4 border-l-cyan-500">
                <p class="text-xs text-slate-400">Vault Files</p>
                <h3 class="text-2xl font-bold text-white mt-1">24</h3>
            </div>
        </div>

        <!-- Middle Row: Demographics Chart, Recent Activity, Quick Actions -->
        <div class="grid grid-cols-3 gap-6">
            
            <!-- Family Overview Donut Chart -->
            <div class="card p-5">
                <h3 class="font-bold text-white mb-4">Family Overview</h3>
                <div class="relative w-48 h-48 mx-auto">
                    <canvas id="familyChart"></canvas>
                </div>
                <div class="grid grid-cols-2 gap-2 mt-4 text-xs text-slate-300">
                    <div><span class="inline-block w-3 h-3 rounded-full bg-purple-500 mr-1"></span> Parents: 2</div>
                    <div><span class="inline-block w-3 h-3 rounded-full bg-emerald-500 mr-1"></span> Leadership: 3</div>
                    <div><span class="inline-block w-3 h-3 rounded-full bg-amber-500 mr-1"></span> Students: 3</div>
                    <div><span class="inline-block w-3 h-3 rounded-full bg-blue-500 mr-1"></span> Other: 1</div>
                </div>
            </div>

            <!-- Recent Activity Feed -->
            <div class="card p-5">
                <h3 class="font-bold text-white mb-4">Recent Activity</h3>
                <div class="space-y-3 text-xs">
                    <div class="p-2.5 bg-[#0d1424] rounded-lg border border-[#1e293b]">
                        <p class="font-semibold text-cyan-400">New member added</p>
                        <p class="text-slate-300">Collins Odwar (Secretary)</p>
                        <span class="text-[10px] text-slate-500">2 days ago</span>
                    </div>
                    <div class="p-2.5 bg-[#0d1424] rounded-lg border border-[#1e293b]">
                        <p class="font-semibold text-emerald-400">Project updated</p>
                        <p class="text-slate-300">Agritech Solution</p>
                        <span class="text-[10px] text-slate-500">3 days ago</span>
                    </div>
                    <div class="p-2.5 bg-[#0d1424] rounded-lg border border-[#1e293b]">
                        <p class="font-semibold text-purple-400">Document uploaded</p>
                        <p class="text-slate-300">Family Constitution.pdf</p>
                        <span class="text-[10px] text-slate-500">4 days ago</span>
                    </div>
                </div>
            </div>

            <!-- Quick Actions Panel -->
            <div class="card p-5">
                <h3 class="font-bold text-white mb-4">Quick Actions</h3>
                <div class="space-y-3">
                    <button class="w-full py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-medium flex items-center justify-center gap-2"><i class="fa-solid fa-user-plus"></i> Add Member</button>
                    <button class="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-medium flex items-center justify-center gap-2"><i class="fa-solid fa-folder-plus"></i> Create Project</button>
                    <button class="w-full py-2.5 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-sm font-medium flex items-center justify-center gap-2"><i class="fa-solid fa-calendar-plus"></i> Schedule Meeting</button>
                    <button class="w-full py-2.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-sm font-medium flex items-center justify-center gap-2"><i class="fa-solid fa-file-arrow-up"></i> Upload Document</button>
                </div>
            </div>

        </div>

        <!-- Family Roster Table & System Status -->
        <div class="grid grid-cols-3 gap-6">
            <div class="card p-5 col-span-2">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="font-bold text-white">Family Roster (Quick View)</h3>
                    <a href="#members" class="text-xs text-cyan-400 hover:underline">View All →</a>
                </div>
                <div class="space-y-2 text-xs">
                    <div class="flex justify-between items-center p-2 bg-[#0d1424] rounded border border-[#1e293b]">
                        <div><p class="font-semibold text-white">Felix Ochieng</p><p class="text-slate-400">Family Chairman (Admin)</p></div>
                        <span class="px-2 py-0.5 bg-purple-500/20 text-purple-400 rounded font-bold">Admin</span>
                    </div>
                    <div class="flex justify-between items-center p-2 bg-[#0d1424] rounded border border-[#1e293b]">
                        <div><p class="font-semibold text-white">Gabriel Aloka</p><p class="text-slate-400">Digital Architect (Admin)</p></div>
                        <span class="px-2 py-0.5 bg-purple-500/20 text-purple-400 rounded font-bold">Admin</span>
                    </div>
                    <div class="flex justify-between items-center p-2 bg-[#0d1424] rounded border border-[#1e293b]">
                        <div><p class="font-semibold text-white">Elisha Ouma</p><p class="text-slate-400">Vice Chairman</p></div>
                        <span class="px-2 py-0.5 bg-blue-500/20 text-blue-400 rounded font-bold">Member</span>
                    </div>
                    <div class="flex justify-between items-center p-2 bg-[#0d1424] rounded border border-[#1e293b]">
                        <div><p class="font-semibold text-white">Collins Odwar</p><p class="text-slate-400">Family Secretary</p></div>
                        <span class="px-2 py-0.5 bg-blue-500/20 text-blue-400 rounded font-bold">Member</span>
                    </div>
                </div>
            </div>

            <!-- System Status Grid -->
            <div class="card p-5">
                <h3 class="font-bold text-white mb-4">System Status</h3>
                <div class="grid grid-cols-2 gap-2 text-xs">
                    <div class="p-2 bg-emerald-500/10 border border-emerald-500/30 rounded text-center">
                        <i class="fa-solid fa-check text-emerald-400 mb-1"></i>
                        <p class="text-slate-300">Database Connected</p>
                    </div>
                    <div class="p-2 bg-emerald-500/10 border border-emerald-500/30 rounded text-center">
                        <i class="fa-solid fa-check text-emerald-400 mb-1"></i>
                        <p class="text-slate-300">File Storage Connected</p>
                    </div>
                    <div class="p-2 bg-emerald-500/10 border border-emerald-500/30 rounded text-center">
                        <i class="fa-solid fa-check text-emerald-400 mb-1"></i>
                        <p class="text-slate-300">Security Active</p>
                    </div>
                    <div class="p-2 bg-emerald-500/10 border border-emerald-500/30 rounded text-center">
                        <i class="fa-solid fa-check text-emerald-400 mb-1"></i>
                        <p class="text-slate-300">AI Assistant Ready</p>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <script>
        const ctx = document.getElementById('familyChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Parents', 'Leadership', 'Students', 'Other'],
                datasets: [{
                    data: [2, 3, 3, 1],
                    backgroundColor: ['#a855f7', '#10b981', '#f59e0b', '#3b82f6'],
                    borderWidth: 0
                }]
            },
            options: { plugins: { legend: { display: false } }, cutout: '70%' }
        });
    </script>
</body>
</html>
'''

with open('templates/dashboard.html', 'w') as f:
    f.write(html_content)

print("[✓] Admin View setup file generated successfully!")
