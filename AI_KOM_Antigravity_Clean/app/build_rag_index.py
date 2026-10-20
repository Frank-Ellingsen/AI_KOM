import sqlite3
import os

os.makedirs("data/db", exist_ok=True)
conn = sqlite3.connect("data/db/kommune_golden_record.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    user_id TEXT,
    role TEXT,
    action_type TEXT,
    query_or_input TEXT,
    execution_result_summary TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()
print("Database initialized successfully.")
