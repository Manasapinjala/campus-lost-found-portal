import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    location TEXT,
    status TEXT NOT NULL,
    image TEXT,
    user_id INTEGER
)
""")

conn.commit()
conn.close()

print("Database and Users table created successfully!")