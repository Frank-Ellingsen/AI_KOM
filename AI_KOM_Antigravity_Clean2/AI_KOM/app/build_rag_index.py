import sqlite3
import os
import shutil

def initialize_database():
    """Initialiserer SQLite-database og oppretter tabeller for AI_KOM Clean2."""
    db_dir = os.path.abspath("data/db")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "kommune_golden_record.db")

    # Hvis canonical golden record finnes i rotmappen, kopier eller synkroniser
    canonical_candidates = [
        os.path.abspath("../../erp_data/kommune_golden_record.db"),
        os.path.abspath("../../data/db/kommune_golden_record.db"),
        os.path.abspath("../erp_data/kommune_golden_record.db"),
    ]
    for candidate in canonical_candidates:
        if os.path.exists(candidate) and not os.path.exists(db_path):
            try:
                shutil.copyfile(candidate, db_path)
                print(f"Kopierte canonical golden record fra {candidate} til {db_path}")
                break
            except Exception:
                pass

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Audit Log (Uforanderlig revisjonsspor jf. Arkivlova)
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

    # 2. ERP Transactions Staging
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stg_erp_transactions (
        raw_id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_system TEXT DEFAULT 'Visma Enterprise',
        voucher_number TEXT,
        accounting_date TEXT,
        account_code TEXT,
        function_code TEXT,
        cost_center_code TEXT,
        ansvar TEXT,
        amount REAL,
        description TEXT,
        scale_factor REAL DEFAULT 1.0,
        ingested_at TEXT
    )
    """)

    # 3. Legg inn baseline demo-transaksjoner dersom tabellen er tom
    cursor.execute("SELECT COUNT(*) FROM stg_erp_transactions")
    if cursor.fetchone()[0] == 0:
        demo_rows = [
            ('Visma', 'BIL-2026-001', '2026-08-12', '1010', '253', '2530', '2530', 450000.0, 'Fast lønn august'),
            ('Visma', 'BIL-2026-002', '2026-08-15', '1020', '253', '2530', '2530', 125000.0, 'Vikarinnleie Adecco'),
            ('Visma', 'BIL-2026-003', '2026-08-18', '1040', '253', '2530', '2530', 88000.0, 'Overtid helgevakter'),
            ('Visma', 'BIL-2026-004', '2026-08-20', '1150', '253', '2530', '2530', 14500.0, 'Kurs og opplæring HMS'),
            ('Visma', 'BIL-2026-005', '2026-08-22', '1010', '254', '2540', '2540', 380000.0, 'Fast lønn hjemmetjeneste'),
            ('Visma', 'BIL-2026-006', '2026-08-25', '1020', '254', '2540', '2540', 95000.0, 'Vikarer sommerturnus')
        ]
        cursor.executemany("""
            INSERT INTO stg_erp_transactions 
            (source_system, voucher_number, accounting_date, account_code, function_code, cost_center_code, ansvar, amount, description, ingested_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, demo_rows)
        print("La til demo ERP-transaksjoner.")

    # 4. Førstegangs audit log post
    cursor.execute("""
        INSERT INTO audit_log (timestamp, user_id, role, action_type, query_or_input, execution_result_summary, status)
        VALUES (datetime('now'), 'system_init', 'system', 'DB_INIT', 'build_rag_index.py', 'Database initialisert og sjekket', 'SUCCESS')
    """)

    conn.commit()
    conn.close()
    print(f"[OK] AI_KOM database initialisert vellykket: {db_path}")

if __name__ == "__main__":
    initialize_database()
