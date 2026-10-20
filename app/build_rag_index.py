import sqlite3
import os

def init_db(db_path: str):
    dir_name = os.path.dirname(db_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    conn = sqlite3.connect(db_path)
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
    print(f"Audit log initialized in {db_path}")

# Initialiser i både data/db og erp_data for full kompatibilitet
init_db("data/db/kommune_golden_record.db")
if os.path.exists("erp_data/kommune_golden_record.db"):
    init_db("erp_data/kommune_golden_record.db")

print("Database initialized successfully.")
