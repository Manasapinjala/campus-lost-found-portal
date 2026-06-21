import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute(
    "ALTER TABLE items ADD COLUMN image TEXT"
)

conn.commit()
conn.close()

print("Image column added")