# 🛠️ Tool Skill: DuckDB Analytical Engine & Parquet Driver (`TOOL_SKILL_DUCKDB_ANALYTICS`)

> **Høyytelses OLAP-analysemotor for in-memory regnskapskonsolidering, Project Controlling-beregninger (CPI, EAC, ETC) og Parquet-eksport for Power BI.**

---

## 1. Oversikt og Formål

Denne verktøy-skillen gir agenten evnen til å utføre lynraske analytiske aggregasjoner over kommunale regnskaps- og budsjettdata lagret i SQLite (`kommune_golden_record.db`) eller rå CSV/Parquet-filer, uten å overbelaste minnet eller CPU-en.

---

## 2. Kjernefunksjonalitet & Bruksmønstre

### A. In-Memory Sammenstilling av SQLite Star Schema
```python
import sqlite3
import duckdb
import pandas as pd

def run_olap_query(db_path: str, sql_query: str) -> pd.DataFrame:
    """Kjører analytiske spørringer i DuckDB over SQLite Star Schema."""
    con_sqlite = sqlite3.connect(db_path)
    con = duckdb.connect()

    # Registrer SQLite-tabeller som in-memory DuckDB-relasjoner
    tables = ["Fact_Regnskap", "Fact_Budsjett", "Dim_Funksjon", "Dim_Art", "Dim_Ansvar", "Dim_Dato"]
    for tbl in tables:
        df = pd.read_sql_query(f"SELECT * FROM {tbl}", con_sqlite)
        con.register(tbl, df)
    con_sqlite.close()

    return con.execute(sql_query).df()
```

### B. Project Controlling Beregninger (EAC / ETC / CPI)
```sql
-- Beregner Cost Performance Index og Estimate at Completion
WITH evm_base AS (
    SELECT 
        ans.enhet_navn,
        SUM(b.budsjett_belop) AS BAC,
        SUM(CASE WHEN r.belop > 0 THEN b.budsjett_belop ELSE 0 END) AS PV,
        SUM(COALESCE(r.belop, 0)) AS AC
    FROM Fact_Budsjett b
    LEFT JOIN Fact_Regnskap r 
        ON b.funksjon_key = r.funksjon_key 
       AND b.art_key = r.art_key 
       AND b.dato_key = r.dato_key
    JOIN Dim_Ansvar ans ON b.ansvar_key = ans.ansvar_kode
    GROUP BY ans.enhet_navn
)
SELECT 
    enhet_navn,
    ROUND(PV, 0) AS pv_nok,
    ROUND(AC, 0) AS ac_nok,
    ROUND(PV - AC, 0) AS cv_nok,
    ROUND(PV / NULLIF(AC, 0), 3) AS cpi,
    ROUND(BAC / NULLIF(PV / NULLIF(AC, 0), 0), 0) AS eac_prognose
FROM evm_base;
```

### C. Direkte Parquet-Eksport for Power BI
```python
def export_star_schema_to_parquet(duck_con, output_dir: str):
    """Eksporterer tabeller til komprimert columnar Parquet for Power BI / Fabric."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    tables = ["Fact_Regnskap", "Fact_Budsjett", "Dim_Funksjon", "Dim_Art"]
    for tbl in tables:
        duck_con.execute(f"COPY (SELECT * FROM {tbl}) TO '{output_dir}/{tbl}.parquet' (FORMAT PARQUET);")
```
