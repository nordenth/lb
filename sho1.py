import sqlite3

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

def main():
    init_db()
    
    print("SQL Injection Test")
    print("-----------------")
    username = input("Username: ")
    password = input("Password: ")
    method = input("Method (safe/unsafe): ").lower()
    
    if method == 'safe':
        result = safe_login(username, password)
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
    else:
        result = unsafe_login(username, password)
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    print("\nExecuted query:")
    print(query)
    print("\nResult:")
    print(result)

if __name__ == '__main__':
    main()

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SQL Injection Demo (No Flask)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 600px; margin: 0 auto; }
        .form-group { margin-bottom: 15px; }
        input, select, button { padding: 8px; width: 100%; }
        pre { background: #f4f4f4; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>SQL Injection Demo (No Flask)</h1>
        <p>Используйте <code>' OR '1'='1</code> в поле пароля для обхода аутентификации.</p>
        
        <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" id="username" placeholder="admin">
        </div>
        
        <div class="form-group">
            <label for="password">Password
