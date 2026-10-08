import http.server
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
