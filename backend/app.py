from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2
import re

app = Flask(__name__)
CORS(app)

# ==============================
# Database Connection
# ==============================

def get_db_connection():
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if DATABASE_URL:
        conn = psycopg2.connect(DATABASE_URL)
        return conn, "postgres"
    else:
        import sqlite3
        conn = sqlite3.connect("food.db")
        conn.row_factory = sqlite3.Row
        return conn, "sqlite"

# ==============================
# Create Table
# ==============================

def create_table():
    conn, db_type = get_db_connection()
    cursor = conn.cursor()

    if db_type == "postgres":
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_items (
                id SERIAL PRIMARY KEY,
                item_name VARCHAR(255) NOT NULL,
                category VARCHAR(100) NOT NULL,
                quantity INTEGER NOT NULL,
                expiry_date VARCHAR(50) NOT NULL,
                price REAL NOT NULL,
                purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                expiry_date TEXT NOT NULL,
                price REAL NOT NULL,
                purchase_date TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)

    conn.commit()
    cursor.close()
    conn.close()

create_table()

# ==============================
# Add Food API
# ==============================

@app.route("/addFood", methods=["POST"])
def add_food():
    data = request.json

    item_name = data.get("item_name")
    category = data.get("category")
    quantity = data.get("quantity")
    expiry_date = data.get("expiry_date")
    price = data.get("price")

    if not re.match(r"^[A-Za-z ]+$", item_name):
        return jsonify({"message": "Item name must contain only letters"}), 400

    conn, db_type = get_db_connection()
    cursor = conn.cursor()

    if db_type == "postgres":
        cursor.execute("""
            INSERT INTO food_items 
            (item_name, category, quantity, expiry_date, price)
            VALUES (%s, %s, %s, %s, %s)
        """, (item_name, category, quantity, expiry_date, price))
    else:
        cursor.execute("""
            INSERT INTO food_items 
            (item_name, category, quantity, expiry_date, price)
            VALUES (?, ?, ?, ?, ?)
        """, (item_name, category, quantity, expiry_date, price))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Food added successfully"}), 201

# ==============================
# Get Food API (SAFE VERSION)
# ==============================

@app.route("/getFoods", methods=["GET"])
def get_foods():
    conn, db_type = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM food_items;")
    rows = cursor.fetchall()

    result = []

    # Get column names dynamically
    columns = [desc[0] for desc in cursor.description]

    for row in rows:
        row_dict = {}
        for i in range(len(columns)):
            row_dict[columns[i]] = row[i]
        result.append(row_dict)

    cursor.close()
    conn.close()

    return jsonify(result)

# ==============================
# Fix DB Route (Safe)
# ==============================

@app.route("/fixDB")
def fix_db():
    conn, db_type = get_db_connection()
    cursor = conn.cursor()

    try:
        if db_type == "postgres":
            cursor.execute("""
                ALTER TABLE food_items
                ADD COLUMN IF NOT EXISTS purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            """)
        else:
            cursor.execute("""
                ALTER TABLE food_items
                ADD COLUMN purchase_date TEXT DEFAULT CURRENT_TIMESTAMP;
            """)

        conn.commit()
        message = "Column checked/added successfully"
    except Exception as e:
        message = str(e)

    cursor.close()
    conn.close()

    return message

# ==============================
# Debug Routes
# ==============================

@app.route("/")
def home():
    return "Backend is running successfully"

@app.route("/debugDB")
def debug_db():
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM food_items;")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return f"Total records: {count}"

# ==============================
# Run App
# ==============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)