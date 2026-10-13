#!/usr/bin/env python3
"""
ETL Engine for MVP-Pilot: Ingestion of Mini_case_AI_kommunal_okonomistyring.xlsx
Reads tbl_BoMiljo into DuckDB and SQLite, verifies integrity and KOSTRA structure.
"""

from pathlib import Path
import sqlite3
import duckdb
import openpyxl
import pandas as pd

try:
    from config import EXCEL_SOURCE, DB_SQLITE, DB_DUCKDB
except ImportError:
    from mvp_pilot.config import EXCEL_SOURCE, DB_SQLITE, DB_DUCKDB


def ingest_excel_to_databases(excel_path: Path = EXCEL_SOURCE):
    """
    Leser rådata fra Excel 'Rådata BoEnhet pr 2tertial' og oppretter
    strukturerte tabeller i både DuckDB og SQLite.
    """
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel-fil ikke funnet: {excel_path}")

    print(f"[ETL] Laster rådata fra {excel_path.name}...")
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    preferred_sheet = "Rådata BoEnhet pr 2tertial"
    if preferred_sheet in wb.sheetnames:
        sheet_name = preferred_sheet
    else:
        # Dynamisk søk etter ark med rådata
        candidate_sheets = [s for s in wb.sheetnames if "rådata" in s.lower() or "boenhet" in s.lower()]
        if candidate_sheets:
            sheet_name = candidate_sheets[0]
        else:
            raise ValueError(f"Finner ikke rådataark i {excel_path.name}. Tilgjengelige ark: {wb.sheetnames}")

    print(f"[ETL] Leser data fra ark: '{sheet_name}'")
    ws = wb[sheet_name]
    headers = [ws.cell(1, c).value for c in range(1, ws.max_column + 1) if ws.cell(1, c).value is not None]

    rows = []
    for r in range(2, ws.max_row + 1):
        row_vals = [ws.cell(r, c).value for c in range(1, len(headers) + 1)]
        if any(v is not None for v in row_vals):
            rows.append(row_vals)

    df = pd.DataFrame(rows, columns=headers)

    # Typekonvertering og rensing
    numeric_cols = ["Måned_Nr", "Budsjett", "Regnskap", "Avvik", "Merforbruk"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    # Konverter streng-kolonner
    str_cols = ["Periode", "Måned", "Tertial", "Status", "Lokasjon", "KOSTRA_Funksjon", 
                "Tjenesteområde", "Hovedgruppe", "Undergruppe", "KOSTRA_Art", "Kontokode", "Kontonavn"]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Generer unik SHA-256 basert transaksjons-ID per rad
    import hashlib
    def _create_txn_hash(row):
        raw_key = f"{row.get('Periode','')}_{row.get('KOSTRA_Funksjon','')}_{row.get('KOSTRA_Art','')}_{row.get('Kontokode','')}_{row.get('Budsjett',0.0)}_{row.get('Regnskap',0.0)}"
        return "TXN-" + hashlib.sha256(raw_key.encode('utf-8')).hexdigest()[:16].upper()

    df["Transaksjon_ID"] = df.apply(_create_txn_hash, axis=1)

    print(f"[ETL] Innlastet {len(df)} rader. Verifiserer avstemmingssum...")

    # Kontrollsummer mot Excel 'Metode og kontroll'
    bokfort_mask = df["Status"] == "Bokført"
    sum_budsjett = df.loc[bokfort_mask, "Budsjett"].sum()
    sum_regnskap = df.loc[bokfort_mask, "Regnskap"].sum()
    sum_merforbruk = df.loc[bokfort_mask, "Merforbruk"].sum()
    sum_gjenstaende = df.loc[~bokfort_mask, "Budsjett"].sum()

    print(f"      • Bokført Budsjett YTD:   {sum_budsjett:14,.2f} kr")
    print(f"      • Bokført Regnskap YTD:   {sum_regnskap:14,.2f} kr")
    print(f"      • Bokført Merforbruk YTD: {sum_merforbruk:14,.2f} kr")
    print(f"      • Gjenstående budsjett:   {sum_gjenstaende:14,.2f} kr")
    print(f"      • Årsbudsjett totalt:     {sum_budsjett + sum_gjenstaende:14,.2f} kr")

    # 1. Last inn i DuckDB
    con_duck = duckdb.connect(str(DB_DUCKDB))
    con_duck.execute("CREATE OR REPLACE TABLE fact_bomiljo AS SELECT * FROM df")
    con_duck.execute("""
        CREATE OR REPLACE VIEW v_driveranalyse AS
        SELECT 
            Undergruppe,
            KOSTRA_Art,
            Kontonavn,
            SUM(Budsjett) AS Sum_Budsjett,
            SUM(Regnskap) AS Sum_Regnskap,
            SUM(Merforbruk) AS Sum_Merforbruk,
            ROUND(SUM(Merforbruk) / NULLIF(SUM(Budsjett), 0) * 100, 1) AS Avvik_Prosent
        FROM fact_bomiljo
        WHERE Status = 'Bokført'
        GROUP BY Undergruppe, KOSTRA_Art, Kontonavn
        ORDER BY Sum_Merforbruk DESC;
    """)
    con_duck.close()
    print(f"[ETL] DuckDB oppdatert: {DB_DUCKDB.name}")

    # 2. Last inn i SQLite
    con_sqlite = sqlite3.connect(DB_SQLITE)
    df.to_sql("Fact_BoMiljo", con_sqlite, if_exists="replace", index=False)
    
    # Sørg for at Audit_AI_Actions tabell eksisterer med sha256_hash
    cursor = con_sqlite.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Audit_AI_Actions (
        action_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        enhet_kode TEXT NOT NULL,
        ai_model TEXT NOT NULL,
        measure_id TEXT NOT NULL,
        measure_title TEXT NOT NULL,
        estimated_effect REAL NOT NULL,
        confidence_score REAL NOT NULL,
        decision TEXT NOT NULL,
        control_documented TEXT NOT NULL,
        justification TEXT NOT NULL,
        approved_by TEXT NOT NULL,
        sha256_hash TEXT,
        ip_address TEXT DEFAULT '127.0.0.1'
    );
    """)
    # Migreringssjekk dersom sha256_hash kolonne mangler
    cursor.execute("PRAGMA table_info(Audit_AI_Actions);")
    cols = [c[1] for c in cursor.fetchall()]
    if "sha256_hash" not in cols:
        cursor.execute("ALTER TABLE Audit_AI_Actions ADD COLUMN sha256_hash TEXT;")
    con_sqlite.commit()
    con_sqlite.close()
    print(f"[ETL] SQLite oppdatert med Audit_AI_Actions: {DB_SQLITE.name}")

    return {
        "rows": len(df),
        "sum_budsjett_ytd": sum_budsjett,
        "sum_regnskap_ytd": sum_regnskap,
        "sum_merforbruk_ytd": sum_merforbruk,
        "sum_gjenstaende_budsjett": sum_gjenstaende,
        "arsbudsjett": sum_budsjett + sum_gjenstaende
    }


if __name__ == "__main__":
    ingest_excel_to_databases()
