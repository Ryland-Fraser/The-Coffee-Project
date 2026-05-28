"""
This module contains functions for interacting with the database to be used by the application.
"""

import sqlite3
import requests
from flask import session
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "instance" / "coffee_app.db"

def api_pull():
    """Pulls data from the Google Maps API."""
    API_KEY = "AIzaSyD6uC-70hb66HYk22mQa2fSboXKUozjPHc"

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    params = {
        "query": "coffee shops in Edmonton",
        "key": API_KEY
    }

    res = requests.get(url, params=params, timeout=15)
    data = res.json()

    print(data)


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
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        shop_id INTEGER NOT NULL,
        coffee_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        review TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (shop_id) REFERENCES shops (id),
        FOREIGN KEY (coffee_id) REFERENCES coffees (id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place_id TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        longitude REAL NOT NULL,
        latitude REAL NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coffees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shop_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (shop_id) REFERENCES shops (id)
    )
    """)
    
    conn.commit()
    conn.close()

def add_new_review(user_id, shop_id, rating, coffee_id=0, txt_review=0):
    """Adds new review"""
    conn = get_connection()
    cursor = conn.cursor()
    user_id = session["acct_id"]
    cursor.execute("""
    INSERT INTO reviews (user_id, shop_id, coffee_id, rating, review)
    VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        shop_id,
        coffee_id,
        rating,
        txt_review
        ))

def add_new_coffee(shop_id, name, description, price):
    """Adds new coffee to shop"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO coffees (shop_id, name, description, price)
    VALUES (?, ?, ?, ?)
    """, (
        shop_id,
        name,
        description,
        price
        ))
    
def get_coffee_id(shop_id, name):
    """Retrieves a coffee from the database by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id FROM coffees WHERE shop_id = ? AND name = ?
    """, (shop_id, name))
    coffee = cursor.fetchone()

    if coffee is None:
        coffee = False
    else:
        pass

    conn.close()
    return coffee

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
