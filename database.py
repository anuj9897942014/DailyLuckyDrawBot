import sqlite3

conn = sqlite3.connect("luckydraw.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS participants (
    user_id INTEGER,
    username TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS winners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    win_time TEXT
)
""")

conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS winners(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    win_time TEXT
)
""")
conn.commit()