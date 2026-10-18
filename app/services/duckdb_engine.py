"""
DuckDB Analytical OLAP Engine for Kristiansand Kommune Golden Record
Single Source of Truth (SSOT) Architecture — Project Controlling & EVM Calculations
"""

from __future__ import annotations

from pathlib import Path
import sqlite3
from typing import Any, Dict, List, Optional
import pandas as pd
import duckdb

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = ROOT_DIR / "erp_data" / "kommune_golden_record.db"
DEFAULT_PARQUET_DIR = ROOT_DIR / "erp_data" / "parquet_exports"


class DuckDbAnalyticalEngine:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH

    def get_connection(self) -> duckdb.DuckDBPyConnection:
        """Oppretter en in-memory DuckDB-tilkobling med SQLite Star Schema registrert."""
        con = duckdb.connect()
        sqlite_con = sqlite3.connect(self.db_path)

        tables = ["Fact_Regnskap", "Fact_Budsjett", "Dim_Funksjon", "Dim_Art", "Dim_Ansvar", "Dim_Dato"]
        for tbl in tables:
            try:
                df = pd.read_sql_query(f"SELECT * FROM {tbl}", sqlite_con)
                con.register(tbl, df)
            except Exception:
                pass
        sqlite_con.close()
        return con

    def run_query(self, sql_query: str) -> pd.DataFrame:
        """Kjører en analytisk SQL-spørring direkte i DuckDB over Star Schema."""
        con = self.get_connection()
        try:
            return con.execute(sql_query).df()
        finally:
            con.close()

    def get_sector_evm_summary(self, year: int = 2026, month: int = 9) -> List[Dict[str, Any]]:
        """Beregner Planned Value (PV), Actual Cost (AC), Cost Variance (CV),

        Cost Performance Index (CPI) og Estimate at Completion (EAC) per virksomhetsområde.
        """
        dato_filter = f"{year}-%"
        sql = f"""
            WITH raw_agg AS (
                SELECT 
                    CASE 
                        WHEN ans.sektor LIKE '%Oppvekst%' THEN 'Oppvekst og utdanning'
                        WHEN ans.sektor LIKE '%Helse%' THEN 'Helse og mestring'
                        WHEN ans.sektor LIKE '%stedsutvikling%' OR ans.sektor LIKE '%By-%' THEN 'By- og stedsutvikling'
                        WHEN ans.sektor LIKE '%Kultur%' THEN 'Kultur og innbyggerdialog'
                        WHEN ans.sektor LIKE '%Organisasjon%' THEN 'Organisasjon og teknologi'
                        ELSE 'Økonomi og virksomhetsstyring'
                    END AS sektor_navn,
                    SUM(b.budsjett_belop) AS BAC,
                    SUM(CASE WHEN b.dato_key <= '{year}-{month:02d}' THEN b.budsjett_belop ELSE 0 END) AS PV,
                    SUM(COALESCE(r.belop, 0)) AS AC
                FROM Fact_Budsjett b
                LEFT JOIN Fact_Regnskap r 
                    ON b.funksjon_key = r.funksjon_key 
                   AND b.art_key = r.art_key 
                   AND b.ansvar_key = r.ansvar_key 
                   AND b.dato_key = r.dato_key
                JOIN Dim_Ansvar ans ON b.ansvar_key = ans.ansvar_kode
                WHERE b.dato_key LIKE '{dato_filter}'
                GROUP BY 1
            )
            SELECT 
                sektor_navn,
                ROUND(BAC, 0) AS bac_nok,
                ROUND(PV, 0) AS pv_nok,
                ROUND(AC, 0) AS ac_nok,
                ROUND(PV - AC, 0) AS cv_nok,
                ROUND(PV / NULLIF(AC, 0), 4) AS cpi,
                ROUND(BAC / NULLIF(PV / NULLIF(AC, 0), 0), 0) AS eac_prognose,
                CASE 
                    WHEN (PV - AC) < -10000000 THEN 'RØD'
                    WHEN (PV - AC) < -1000000 THEN 'GUL'
                    ELSE 'GRØNN'
                END AS triage_status
            FROM raw_agg
            ORDER BY pv_nok DESC;
        """
        df = self.run_query(sql)
        return df.to_dict(orient="records")

    def get_unit_drilldown(self, sektor_navn: Optional[str] = None, year: int = 2026, month: int = 9) -> List[Dict[str, Any]]:
        """Henter enhetsfordeling med avvik og kostnadsdrivere."""
        sektor_clause = f"AND ans.sektor LIKE '%{sektor_navn}%'" if sektor_navn else ""
        sql = f"""
            WITH unit_agg AS (
                SELECT 
                    ans.ansvar_kode,
                    ans.enhet_navn,
                    ans.sektor,
                    SUM(b.budsjett_belop) AS pv_nok,
                    SUM(COALESCE(r.belop, 0)) AS ac_nok
                FROM Fact_Budsjett b
                LEFT JOIN Fact_Regnskap r 
                    ON b.funksjon_key = r.funksjon_key 
                   AND b.art_key = r.art_key 
                   AND b.ansvar_key = r.ansvar_key 
                   AND b.dato_key = r.dato_key
                JOIN Dim_Ansvar ans ON b.ansvar_key = ans.ansvar_kode
                WHERE b.dato_key <= '{year}-{month:02d}'
                  AND b.dato_key LIKE '{year}-%'
                  {sektor_clause}
                GROUP BY ans.ansvar_kode, ans.enhet_navn, ans.sektor
            )
            SELECT 
                ansvar_kode,
                enhet_navn,
                sektor,
                ROUND(pv_nok, 0) AS pv_nok,
                ROUND(ac_nok, 0) AS ac_nok,
                ROUND(pv_nok - ac_nok, 0) AS cv_nok,
                ROUND(pv_nok / NULLIF(ac_nok, 0), 3) AS cpi,
                CASE 
                    WHEN (pv_nok - ac_nok) < -1000000 THEN 'RØD'
                    WHEN (pv_nok - ac_nok) < 0 THEN 'GUL'
                    ELSE 'GRØNN'
                END AS status
            FROM unit_agg
            ORDER BY cv_nok ASC;
        """
        df = self.run_query(sql)
        return df.to_dict(orient="records")

    def get_art_cost_drivers(self, ansvar_kode: Optional[str] = None, year: int = 2026) -> List[Dict[str, Any]]:
        """Avdekker hvilke kontoarter som driver avviket (f.eks. Art 1020 Vikarer, Art 1090 Overtid)."""
        unit_clause = f"AND b.ansvar_key = '{ansvar_kode}'" if ansvar_kode else ""
        sql = f"""
            SELECT 
                art.art_kode,
                art.art_navn,
                art.art_gruppe,
                ROUND(SUM(b.budsjett_belop), 0) AS budsjett_ytd,
                ROUND(SUM(COALESCE(r.belop, 0)), 0) AS regnskap_ytd,
                ROUND(SUM(b.budsjett_belop) - SUM(COALESCE(r.belop, 0)), 0) AS avvik_nok,
                ROUND((SUM(COALESCE(r.belop, 0)) - SUM(b.budsjett_belop)) / NULLIF(SUM(b.budsjett_belop), 0) * 100, 2) AS avvik_pct
            FROM Fact_Budsjett b
            LEFT JOIN Fact_Regnskap r 
                ON b.funksjon_key = r.funksjon_key 
               AND b.art_key = r.art_key 
               AND b.ansvar_key = r.ansvar_key 
               AND b.dato_key = r.dato_key
            JOIN Dim_Art art ON b.art_key = art.art_kode
            WHERE b.dato_key LIKE '{year}-%'
              {unit_clause}
            GROUP BY art.art_kode, art.art_navn, art.art_gruppe
            ORDER BY avvik_nok ASC
            LIMIT 10;
        """
        df = self.run_query(sql)
        return df.to_dict(orient="records")
