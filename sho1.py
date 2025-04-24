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