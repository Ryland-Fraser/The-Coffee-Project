"""
This module contains functions for interacting with the database to be used by the application.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "instance" / "users.db"

def get_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    """Verifies that the database exists and creates it if it doesn't."""
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
    """Adds a new user to the database."""
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
    """Retrieves a user from the database by username."""
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
    """Retrieves a user from the database by email."""
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
    """Retrieves a user from the database by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users WHERE id = ?
    """, (user_id,))
    user = cursor.fetchone()

    conn.close()
    return user
