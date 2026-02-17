import sqlite3

conn = sqlite3.connect("food.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS food_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    category TEXT,
    quantity INTEGER,
    expiry_date TEXT,
    price REAL
)
""")

conn.commit()
conn.close()

print("Database and table created successfully")