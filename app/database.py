"""
This module contains functions for interacting with the database to be used by the application.
"""

import sqlite3
import requests
from flask import session
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "instance" / "coffee_app.db"

#-------------------------------------

API_KEY = "AIzaSyD6uC-70hb66HYk22mQa2fSboXKUozjPHc"

URL = "https://places.googleapis.com/v1/places:searchText"

HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "places.displayName,places.id,places.location,places.formattedAddress"
}

def fetch_places(query):
    body = {"textQuery": query}
    all_places = []

    while True:
        res = requests.post(URL, headers=HEADERS, json=body, timeout=15)
        data = res.json()

        all_places.extend(data.get("places", []))

        next_token = data.get("nextPageToken")
        if not next_token:
            break

        time.sleep(2)

        body = {
            "textQuery": query,
            "pageToken": next_token
        }

    return all_places

def save_to_db(cursor, places):
    for shop in places:

        location = shop.get("location", {})

        cursor.execute("""
        INSERT OR IGNORE INTO shops
        (place_id, name, address, longitude, latitude)
        VALUES (?, ?, ?, ?, ?)
        """, (
            shop.get("id"),
            shop.get("displayName", {}).get("text"),
            shop.get("formattedAddress"),
            location.get("longitude"),
            location.get("latitude")
        ))

def shop_api_pull_all():
    queries = [

    # =========================
    # EDMONTON AREA GENERIC
    # =========================

    "coffee shops in Edmonton",
    "cafe Edmonton",
    "espresso bar Edmonton",
    "specialty coffee Edmonton",
    "coffee Edmonton",
    "coffee shop Edmonton",

    "coffee shops in Sherwood Park",
    "cafe Sherwood Park",
    "espresso bar Sherwood Park",
    "specialty coffee Sherwood Park",

    "coffee shops in St. Albert",
    "cafe St. Albert",
    "espresso bar St. Albert",

    "coffee shops in Leduc",
    "cafe Leduc",
    "espresso bar Leduc",

    "coffee shops in Fort Saskatchewan",
    "cafe Fort Saskatchewan",

    "coffee shops in Spruce Grove",
    "cafe Spruce Grove",

    "coffee shops in Stony Plain",
    "cafe Stony Plain",

    "coffee shops in Beaumont Alberta",
    "cafe Beaumont Alberta",

    # =========================
    # STARBUCKS
    # =========================

    "Starbucks Edmonton",
    "Starbucks Sherwood Park",
    "Starbucks St. Albert",
    "Starbucks Leduc",
    "Starbucks Fort Saskatchewan",
    "Starbucks Spruce Grove",
    "Starbucks Stony Plain",
    "Starbucks Beaumont Alberta",

    # =========================
    # TIM HORTONS
    # =========================

    "Tim Hortons Edmonton",
    "Tim Hortons Sherwood Park",
    "Tim Hortons St. Albert",
    "Tim Hortons Leduc",
    "Tim Hortons Fort Saskatchewan",
    "Tim Hortons Spruce Grove",
    "Tim Hortons Stony Plain",
    "Tim Hortons Beaumont Alberta",

    # =========================
    # SECOND CUP
    # =========================

    "Second Cup Edmonton",
    "Second Cup Sherwood Park",
    "Second Cup St. Albert",
    "Second Cup Leduc",

    # =========================
    # REMEDY
    # =========================

    "Remedy Cafe Edmonton",
    "Remedy Cafe Sherwood Park",
    "Remedy Cafe St. Albert",

    # =========================
    # ROASTI
    # =========================

    "Roasti Coffee Edmonton",
    "Roasti Coffee Sherwood Park",
    "Roasti Coffee St. Albert",
    "Roasti Coffee Leduc",
    "Roasti Coffee Fort Saskatchewan",
    "Roasti Coffee Spruce Grove",

    # =========================
    # TRANSCEND
    # =========================

    "Transcend Coffee Edmonton",
    "Transcend Coffee Sherwood Park",
    "Transcend Coffee St. Albert",

    # =========================
    # ACE COFFEE
    # =========================

    "Ace Coffee Roasters Edmonton",
    "Ace Coffee Roasters Sherwood Park",
    "Ace Coffee Roasters St. Albert",

    # =========================
    # ROGUE WAVE
    # =========================

    "Rogue Wave Coffee Edmonton",
    "Rogue Wave Coffee Sherwood Park",
    "Rogue Wave Coffee St. Albert",

    # =========================
    # SQUARE 1
    # =========================

    "Square 1 Coffee Edmonton",
    "Square 1 Coffee Sherwood Park",
    "Square 1 Coffee St. Albert",

    # =========================
    # THE COLOMBIAN
    # =========================

    "The Colombian Edmonton",
    "The Colombian Sherwood Park",
    "The Colombian St. Albert",
    "Colombian Coffee Edmonton",

    # =========================
    # COFFEE BUREAU
    # =========================

    "Coffee Bureau Edmonton",
    "Coffee Bureau Sherwood Park",
    "Coffee Bureau St. Albert",

    # =========================
    # DISTRICT CAFE
    # =========================

    "District Cafe Edmonton",
    "District Cafe Sherwood Park",
    "District Cafe St. Albert",

    # =========================
    # WAVES
    # =========================

    "Waves Coffee Edmonton",
    "Waves Coffee Sherwood Park",
    "Waves Coffee St. Albert",

    # =========================
    # CAFE NEO
    # =========================

    "Cafe Neo Edmonton",
    "Cafe Neo Sherwood Park",
    "Cafe Neo St. Albert",

    # =========================
    # LOCK STOCK
    # =========================

    "Lock Stock Coffee Edmonton",
    "Lock Stock Coffee Sherwood Park",
    "Lock Stock Coffee St. Albert",

    # =========================
    # CAFE BICYCLETTE
    # =========================

    "Cafe Bicyclette Edmonton",

    # =========================
    # OTHER COMMON CHAINS
    # =========================

    "McCafe Edmonton",
    "McCafe Sherwood Park",
    "McCafe St. Albert",

    "Good Earth Coffeehouse Edmonton",
    "Good Earth Coffeehouse Sherwood Park",
    "Good Earth Coffeehouse St. Albert",

    "Blenz Coffee Edmonton",
    "Blenz Coffee Sherwood Park",

    "Caffiend Edmonton",
    "Caffiend Sherwood Park",

    "Dirtbag Cafe Edmonton",
    "Dirtbag Cafe Sherwood Park"
    ]

    conn = get_connection()
    cursor = conn.cursor()

    total = 0

    for q in queries:
        print(f"Searching: {q}")

        places = fetch_places(q)
        save_to_db(cursor, places)

        conn.commit()

        total += len(places)
        print(f"Found {len(places)} places")

    conn.close()

    print(f"\nDone. Total raw results fetched: {total}")

#-------------------------------------

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

def show_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, address
    FROM shops
    ORDER BY name
    """)

    rows = cursor.fetchall()

    for i, row in enumerate(rows, 1):
        print(f"{i}. {row[0]} - {row[1]}")

    conn.close()
