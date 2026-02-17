from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2

app = Flask(__name__)
CORS(app)


# ==============================
# Database Connection
# ==============================

def get_db_connection():
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if DATABASE_URL:
        # Running on Render (PostgreSQL)
        conn = psycopg2.connect(DATABASE_URL)
        return conn, "postgres"
    else:
        # Running locally (SQLite)
        import sqlite3
        conn = sqlite3.connect("food.db")
        conn.row_factory = sqlite3.Row
        return conn, "sqlite"


# ==============================
# Create Table Automatically
# ==============================

def create_table():
    conn, db_type = get_db_connection()
    cursor = conn.cursor()

    if db_type == "postgres":
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_items (
                id SERIAL PRIMARY KEY,
                item_name VARCHAR(255) NOT NULL,
                quantity INTEGER NOT NULL,
                expiry_date VARCHAR(50) NOT NULL,
                price REAL NOT NULL
            );
        """)
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                expiry_date TEXT NOT NULL,
                price REAL NOT NULL
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

    item_name = data["item_name"]
    quantity = data["quantity"]
    expiry_date = data["expiry_date"]
    price = data["price"]

    conn, db_type = get_db_connection()
    cursor = conn.cursor()

    if db_type == "postgres":
        cursor.execute("""
            INSERT INTO food_items (item_name, quantity, expiry_date, price)
            VALUES (%s, %s, %s, %s)
        """, (item_name, quantity, expiry_date, price))
    else:
        cursor.execute("""
            INSERT INTO food_items (item_name, quantity, expiry_date, price)
            VALUES (?, ?, ?, ?)
        """, (item_name, quantity, expiry_date, price))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Food added successfully"}), 201


# ==============================
# Home Route
# ==============================

@app.route("/")
def home():
    return "Backend is running successfully"


# ==============================
# Run App
# ==============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)