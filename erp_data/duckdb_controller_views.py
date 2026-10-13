"""
DuckDB Analytical Controller Layer for Kommune Golden Record
Gir Project Controller-innsikt (EAC, ETC, CPI, S-kurve, Avvik) i tråd med Tufte data-ink ratio.
"""

from pathlib import Path
import sqlite3
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import duckdb
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "kommune_golden_record.db"
PARQUET_DIR = BASE_DIR / "parquet_exports"


def run_controller_analytics():
    if not DB_PATH.exists():
        print(f"Feil: Fant ikke databasen {DB_PATH}")
        return

    # Koble til SQLite via Python og last inn i DuckDB for in-memory analytics
    con_sqlite = sqlite3.connect(DB_PATH)
    con = duckdb.connect()

    # Registrer SQLite-tabeller som DuckDB relasjoner
    tables = ["Dim_Funksjon", "Dim_Art", "Dim_Ansvar", "Dim_Dato", "Dim_Kontoklasse", 
              "Fact_Regnskap", "Fact_Budsjett", "stg_erp_transactions"]
    for tbl in tables:
        df = pd.read_sql_query(f"SELECT * FROM {tbl}", con_sqlite)
        con.register(tbl, df)
    con_sqlite.close()

    print("\n" + "=" * 90)
    print("🏛️ DUCKDB PROJECT CONTROLLER ANALYSE — KOMMUNE GOLDEN RECORD")
    print("=" * 90)

    # 1. Hovedoversikt: Budsjett, Regnskap, Avvik, CPI og EAC per Enhet
    controller_summary_sql = """
    WITH ytd_data AS (
        SELECT 
            ans.enhet_navn,
            ans.sektor,
            SUM(b.budsjett_belop) AS BAC, -- Budget at Completion (hele året)
            SUM(CASE WHEN r.belop IS NOT NULL AND r.belop > 0 THEN b.budsjett_belop ELSE 0 END) AS PV, -- Planned Value YTD
            SUM(COALESCE(r.belop, 0)) AS AC -- Actual Cost YTD
        FROM Fact_Budsjett b
        LEFT JOIN Fact_Regnskap r 
            ON b.funksjon_key = r.funksjon_key 
           AND b.art_key = r.art_key 
           AND b.ansvar_key = r.ansvar_key 
           AND b.dato_key = r.dato_key
        JOIN Dim_Ansvar ans ON b.ansvar_key = ans.ansvar_kode
        GROUP BY ans.enhet_navn, ans.sektor
    )
    SELECT 
        enhet_navn AS Enhet,
        sektor AS Sektor,
        ROUND(PV, 0) AS "PV YTD (NOK)",
        ROUND(AC, 0) AS "AC YTD (NOK)",
        ROUND(PV - AC, 0) AS "CV Avvik (NOK)",
        ROUND(CASE WHEN AC > 0 THEN (PV / AC) ELSE 1.0 END, 3) AS CPI,
        ROUND(BAC, 0) AS "BAC Total (NOK)",
        ROUND(CASE WHEN AC > 0 THEN (BAC / (PV / AC)) ELSE BAC END, 0) AS "EAC Prognose (NOK)",
        ROUND((CASE WHEN AC > 0 THEN (BAC / (PV / AC)) ELSE BAC END) - BAC, 0) AS "Est. Sluttoverskridelse"
    FROM ytd_data;
    """
    df_summary = con.execute(controller_summary_sql).df()
    print("\n📌 1. Project Controller EAC / CPI Sammendrag:")
    print("-" * 90)
    for idx, row in df_summary.iterrows():
        print(f"Enhet: {row['Enhet']} ({row['Sektor']})")
        print(f"  • Planlagt verdi (PV YTD)     : {row['PV YTD (NOK)']:>15,.0f} kr".replace(",", " "))
        print(f"  • Påløpte kostnader (AC YTD)  : {row['AC YTD (NOK)']:>15,.0f} kr".replace(",", " "))
        print(f"  • Kostnadsavvik (CV = PV - AC): {row['CV Avvik (NOK)']:>15,.0f} kr".replace(",", " "))
        print(f"  • Kostnadsindeks (CPI = PV/AC): {row['CPI']:>15.3f} {'(Under budsjett-takt / merforbruk)' if row['CPI'] < 1 else '(Effektiv)'}")
        print(f"  • Opprinnelig årsbudsjett(BAC): {row['BAC Total (NOK)']:>15,.0f} kr".replace(",", " "))
        print(f"  • Sluttprognose (EAC = BAC/CPI):{row['EAC Prognose (NOK)']:>15,.0f} kr".replace(",", " "))
        print(f"  • Estimert sluttoverskridelse : {row['Est. Sluttoverskridelse']:>15,.0f} kr".replace(",", " "))
        print("-" * 90)

    # 2. Topp 5 Kritiske Kostnadsarter med Størst Merforbruk (Tufte Tabell)
    top_variances_sql = """
    SELECT 
        a.art_kode || ' ' || a.art_navn AS "KOSTRA Art",
        ans.enhet_navn AS Enhet,
        ROUND(SUM(b.budsjett_belop), 0) AS Budsjett,
        ROUND(SUM(r.belop), 0) AS Regnskap,
        ROUND(SUM(b.budsjett_belop) - SUM(r.belop), 0) AS Avvik_NOK,
        ROUND(((SUM(b.budsjett_belop) - SUM(r.belop)) / NULLIF(SUM(b.budsjett_belop), 0)) * 100, 1) AS "Avvik_Pst"
    FROM Fact_Regnskap r
    JOIN Fact_Budsjett b 
        ON r.funksjon_key = b.funksjon_key 
       AND r.art_key = b.art_key 
       AND r.ansvar_key = b.ansvar_key 
       AND r.dato_key = b.dato_key
    JOIN Dim_Art a ON r.art_key = a.art_kode
    JOIN Dim_Ansvar ans ON r.ansvar_key = ans.ansvar_kode
    GROUP BY a.art_kode, a.art_navn, ans.enhet_navn
    HAVING Avvik_NOK < 0
    ORDER BY Avvik_NOK ASC
    LIMIT 5;
    """
    df_var = con.execute(top_variances_sql).df()
    print("\n🚨 2. Topp 5 KOSTRA-arter med Størst Merforbruk (Negativt Avvik):")
    print(f"{'KOSTRA Art':<35} {'Enhet':<18} {'Budsjett':>14} {'Regnskap':>14} {'Avvik (NOK)':>14} {'Avvik %':>9}")
    print("-" * 110)
    for idx, r in df_var.iterrows():
        art = r['KOSTRA Art'][:34]
        enh = r['Enhet'][:17]
        print(f"{art:<35} {enh:<18} {r['Budsjett']:>14,.0f} {r['Regnskap']:>14,.0f} {r['Avvik_NOK']:>14,.0f} {r['Avvik_Pst']:>8.1f}%".replace(",", " "))
    print("-" * 110)

    # 3. Eksporter til Parquet for Power BI og DuckDB direkteanalyse
    PARQUET_DIR.mkdir(parents=True, exist_ok=True)
    con.execute(f"COPY (SELECT * FROM Fact_Regnskap) TO '{PARQUET_DIR / 'Fact_Regnskap.parquet'}' (FORMAT PARQUET);")
    con.execute(f"COPY (SELECT * FROM Fact_Budsjett) TO '{PARQUET_DIR / 'Fact_Budsjett.parquet'}' (FORMAT PARQUET);")
    con.execute(f"COPY (SELECT * FROM Dim_Funksjon) TO '{PARQUET_DIR / 'Dim_Funksjon.parquet'}' (FORMAT PARQUET);")
    con.execute(f"COPY (SELECT * FROM Dim_Art) TO '{PARQUET_DIR / 'Dim_Art.parquet'}' (FORMAT PARQUET);")
    print(f"\n📦 Parquet-filer generert for lynrask Power BI / DuckDB-import i:\n   {PARQUET_DIR.resolve()}")


if __name__ == "__main__":
    run_controller_analytics()
