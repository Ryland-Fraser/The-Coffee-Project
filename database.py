import sqlite3
import os

BASE_DIR = os.path.dirname("/home/rylan/Python Projects/Python/Account Project/instance/users.db")
DB_PATH = os.path.join(BASE_DIR, "users.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        dob TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

def add_new_user(username, email, password, dob):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO users (username, email, password, dob)
    VALUES (?, ?, ?, ?)
    """, (
        username,
        email,
        password, 
        dob
        ))
    
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users WHERE username = ?
    """, (username,))
    user = cursor.fetchone()

    if user is None:
        user = False
    else:
        pass

    conn.close()
    return user

def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users WHERE email = ?
    """, (email,))
    user = cursor.fetchone()
    if user is None:
        user = False
    else:
        pass

    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users WHERE id = ?
    """, (user_id,))
    user = cursor.fetchone()

    conn.close()
    return user
