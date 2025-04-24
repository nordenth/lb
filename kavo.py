from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                     (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'secret123')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'user1', 'password1')")
    conn.commit()
    conn.close()


def safe_login(username, password):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

def unsafe_login(username, password):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
     
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result

HTML_FORM = """
<!doctype html>
<html>
<head><title>SQL Injection Test</title></head>
<body>
    <h2>Login Form</h2>
    <form method="post">
        <p>Username: <input type="text" name="username"></p>
        <p>Password: <input type="text" name="password"></p>
        <p>Method: 
            <select name="method">
                <option value="safe">Safe (параметризованный)</option>
                <option value="unsafe">Unsafe (конкатенация)</option>
            </select>
        </p>
        <p><input type="submit" value="Login"></p>
    </form>
    {% if result %}
        <h3>Result:</h3>
        <p>{{ result }}</p>
    {% endif %}
    {% if query %}
        <h3>Executed query:</h3>
        <p>{{ query }}</p>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    query = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        method = request.form['method']
        
        if method == 'safe':
            result = safe_login(username, password)
            query = "SELECT * FROM users WHERE username = ? AND password = ?"
        else:
            result = unsafe_login(username, password)
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    return render_template_string(HTML_FORM, result=result, query=query)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)