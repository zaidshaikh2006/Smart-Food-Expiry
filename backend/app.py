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
        return conn
    else:
        raise Exception("DATABASE_URL not found")

# ==============================
# Create Table (Safe)
# ==============================

def create_table():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_items (
                id SERIAL PRIMARY KEY,
                item_name VARCHAR(255) NOT NULL,
                category VARCHAR(100) NOT NULL,
                quantity INTEGER NOT NULL,
                expiry_date VARCHAR(50) NOT NULL,
                price REAL NOT NULL
            );
        """)

        cursor.execute("""
            ALTER TABLE food_items
            ADD COLUMN IF NOT EXISTS purchase_date 
            TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        """)

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print("Database error:", e)

create_table()

# ==============================
# Add Food
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
        return jsonify({"message": "Invalid item name"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO food_items
        (item_name, category, quantity, expiry_date, price)
        VALUES (%s, %s, %s, %s, %s)
    """, (item_name, category, quantity, expiry_date, price))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Food added successfully"}), 201

# ==============================
# Get Foods
# ==============================

@app.route("/getFoods", methods=["GET"])
def get_foods():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM food_items;")
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    result = []
    for row in rows:
        row_dict = {}
        for i in range(len(columns)):
            row_dict[columns[i]] = row[i]
        result.append(row_dict)

    cursor.close()
    conn.close()

    return jsonify(result)

# ==============================
# Home
# ==============================

@app.route("/")
def home():
    return "Backend is running successfully"

# ==============================
# Run
# ==============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)