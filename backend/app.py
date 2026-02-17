from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# PostgreSQL connection
def get_db_connection():
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in environment variables")

    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Create table if not exists
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_items (
            id SERIAL PRIMARY KEY,
            item_name VARCHAR(255) NOT NULL,
            quantity INTEGER NOT NULL,
            expiry_date VARCHAR(50) NOT NULL,
            price REAL NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
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
        VALUES (%s, %s, %s, %s)
    """, (item_name, quantity, expiry_date, price))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Food added successfully"}), 201


@app.route("/")
def home():
    return "Backend is running successfully with PostgreSQL"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)