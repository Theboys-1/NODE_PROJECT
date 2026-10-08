import sqlite3

print("[+] Resetting dynamic database entries to clean zero/null state...")

conn = sqlite3.connect('node.db')
cursor = conn.cursor()

# 1. Clear projects, tasks, meetings, announcements, and goals
cursor.execute("DELETE FROM projects")
cursor.execute("DELETE FROM tasks")
cursor.execute("DELETE FROM meetings")
cursor.execute("DELETE FROM announcements")
cursor.execute("DELETE FROM goals")

conn.commit()
conn.close()

print("[✓] Database reset complete! Projects, tasks, meetings, and announcements are now empty (0).")
