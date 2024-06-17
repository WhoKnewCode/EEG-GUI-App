import sqlite3
from hashlib import sha256


def setup_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def hash_password(password):
    return sha256(password.encode()).hexdigest()


def register_user(username, password):
    print(f"Attempting to register user: {username}")
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hash_password(password)))
        conn.commit()
        print("User registered successfully")
        return True
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")
        return False
    finally:
        conn.close()


def login_user(username, password):
    print(f"Attempting to login user: {username}")
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    if user:
        print("Login successful")
        return user
    else:
        print("Login failed")
        return None
