import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

# Инициализация БД
def init_db():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'secret123')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'user1', 'password1')")
    conn.commit()
    conn.close()

# Безопасный вход
def safe_login(username, password):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

# Небезопасный вход (уязвимость к SQL-инъекциям)
def unsafe_login(username, password):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result, query

# Обработчик HTTP-запросов
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("index.html", "rb") as f:
                self.wfile.write(f.read())
        
        elif self.path.startswith("/login"):
            query = parse_qs(urlparse(self.path).query)
            username = query.get("username", [""])[0]
            password = query.get("password", [""])[0]
            method = query.get("method", ["unsafe"])[0]
            
            if method == "safe":
                result = safe_login(username, password)
                query_sql = "SELECT * FROM users WHERE username = ? AND password = ?"
            else:
                result, query_sql = unsafe_login(username, password)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "result": result,
                "query": query_sql
            }).encode())

if __name__ == "__main__":
    init_db()
    server = HTTPServer(("localhost", 8000), SimpleHandler)
    print("Server running at http://localhost:8000")
    server.serve_forever()