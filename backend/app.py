from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Database connection
def get_db_connection():
    conn = sqlite3.connect("food.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table automatically if not exists
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            expiry_date TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_table()

# Add food API
@app.route("/addFood", methods=["POST"])
def add_food():
    data = request.json

    item_name = data["item_name"]
    quantity = data["quantity"]
    expiry_date = data["expiry_date"]
    price = data["price"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO food_items (item_name, quantity, expiry_date, price)
        VALUES (?, ?, ?, ?)
    """, (item_name, quantity, expiry_date, price))

    conn.commit()
    conn.close()

    return jsonify({"message": "Food added successfully"}), 201


@app.route("/")
def home():
    return "Backend is running successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)