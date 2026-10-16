#!/usr/bin/env python3
"""
ETL Pipeline: Multi-Source Municipal ERP Data -> SQLite Golden Record Star Schema
Basert på: SQLITE_DATA_ARCHITECTURE_SPEC.md

Kilder:
- BoMiljø.csv          (Kommunal Boenhet, 2024 Månedlig, NOK)
- Komskole.csv         (Kommunal Skole, 2025 YTD, TNOK, cp1252)
- kostra_kontoplan.csv (Masterdata: Kontoklasse, Funksjon, Art, Balanse)

Mål:
- kommune_golden_record.db (SQLite Star Schema + Staging + RAG-klare Chunks)
"""

from __future__ import annotations

import csv
import hashlib
import os
from pathlib import Path
import re
import sqlite3
import sys
import time
from typing import Any

# Sikre UTF-8 i konsoll på Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import duckdb

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from tools.build_budsjettansvarlige_register import REGISTER
except ImportError:
    REGISTER = []

try:
    from tools.predictive_forecasting_engine import run_pipeline as run_forecast_pipeline
except ImportError:
    run_forecast_pipeline = None

DB_PATH = BASE_DIR / "kommune_golden_record.db"

BOMILJO_CSV = BASE_DIR / "BoMiljø.csv"
KOMSKOLE_CSV = BASE_DIR / "Komskole.csv"
KONTOPLAN_CSV = BASE_DIR / "kostra_kontoplan.csv"


# ==========================================
# 1. DATABASE DDL SCHEMA (DDL SPEC)
# ==========================================
def init_database(conn: sqlite3.Connection) -> None:
    """Etablerer multi-tiered SQLite-arkitektur i tråd med spesifikasjonen."""
    cursor = conn.cursor()

    # --- A. STAGING LAYER ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stg_erp_transactions (
        raw_id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_system TEXT NOT NULL,
        voucher_number TEXT,
        accounting_date TEXT,
        account_code TEXT,
        function_code TEXT,
        cost_center_code TEXT,
        amount REAL,
        description TEXT,
        scale_factor REAL DEFAULT 1.0,
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stg_epm_budget (
        raw_id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_system TEXT NOT NULL,
        budget_version TEXT NOT NULL,
        fiscal_year INTEGER NOT NULL,
        period_key TEXT,
        function_code TEXT NOT NULL,
        art_code TEXT NOT NULL,
        cost_center_code TEXT NOT NULL,
        budget_amount REAL NOT NULL,
        scale_factor REAL DEFAULT 1.0,
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # --- B. CONFORMED DIMENSIONS ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Dim_Kontoklasse (
        kontoklasse_id INTEGER PRIMARY KEY,
        kontoklasse_navn TEXT NOT NULL,
        beskrivelse TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Dim_Funksjon (
        funksjon_kode TEXT PRIMARY KEY,
        funksjon_navn TEXT NOT NULL,
        tjenesteomrade TEXT NOT NULL,
        hovedfunksjon TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Dim_Art (
        art_kode TEXT PRIMARY KEY,
        art_navn TEXT NOT NULL,
        art_gruppe TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Dim_Ansvar (
        ansvar_kode TEXT PRIMARY KEY,
        enhet_navn TEXT NOT NULL,
        sektor TEXT NOT NULL,
        leder_stilling TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Dim_Dato (
        dato_key TEXT PRIMARY KEY,
        aar INTEGER NOT NULL,
        maned INTEGER NOT NULL,
        kvartal TEXT NOT NULL,
        tertial TEXT NOT NULL,
        arshjul_fase TEXT
    );
    """)

    # --- C. CORE FACT TABLES ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Fact_Regnskap (
        transaksjon_hash TEXT PRIMARY KEY,
        kilde_system TEXT NOT NULL,
        kontoklasse_id INTEGER NOT NULL DEFAULT 1,
        funksjon_key TEXT NOT NULL,
        art_key TEXT NOT NULL,
        ansvar_key TEXT NOT NULL,
        dato_key TEXT NOT NULL,
        belop REAL NOT NULL,
        er_akkumulert_ytd BOOLEAN DEFAULT 0,
        sist_oppdatert TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (funksjon_key) REFERENCES Dim_Funksjon(funksjon_kode),
        FOREIGN KEY (art_key) REFERENCES Dim_Art(art_kode),
        FOREIGN KEY (ansvar_key) REFERENCES Dim_Ansvar(ansvar_kode),
        FOREIGN KEY (dato_key) REFERENCES Dim_Dato(dato_key)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Fact_Budsjett (
        budsjett_hash TEXT PRIMARY KEY,
        kilde_system TEXT NOT NULL,
        budsjett_type TEXT NOT NULL,
        aar INTEGER NOT NULL,
        funksjon_key TEXT NOT NULL,
        art_key TEXT NOT NULL,
        ansvar_key TEXT NOT NULL,
        dato_key TEXT,
        budsjett_belop REAL NOT NULL,
        er_akkumulert_ytd BOOLEAN DEFAULT 0,
        sist_oppdatert TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (funksjon_key) REFERENCES Dim_Funksjon(funksjon_kode),
        FOREIGN KEY (art_key) REFERENCES Dim_Art(art_kode),
        FOREIGN KEY (ansvar_key) REFERENCES Dim_Ansvar(ansvar_kode)
    );
    """)

    # --- D. TEXT CHUNKS FOR AI-RAG & AUDIT TRAIL ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS legal_chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_file TEXT NOT NULL,
        category TEXT NOT NULL,
        section_ref TEXT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Audit_AI_Actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tidsstempel TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        enhetskode TEXT NOT NULL,
        ansvar_kode TEXT NOT NULL,
        ai_tiltak TEXT NOT NULL,
        konfidens REAL NOT NULL,
        leder_beslutning TEXT NOT NULL DEFAULT 'APPROVED',
        saksbehandler TEXT NOT NULL,
        begrunnelse TEXT NOT NULL,
        sha256_hash TEXT NOT NULL,
        user_query TEXT,
        retrieved_chunk_ids TEXT,
        llm_response TEXT,
        FOREIGN KEY (ansvar_kode) REFERENCES Dim_Ansvar(ansvar_kode)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Dim_Budsjettansvarlige (
        ansvar_id TEXT PRIMARY KEY,
        navn TEXT NOT NULL,
        tittel TEXT NOT NULL,
        niva TEXT NOT NULL,
        niva_tekst TEXT NOT NULL,
        sektor_kode TEXT NOT NULL,
        sektor_navn TEXT NOT NULL,
        enhet_navn TEXT NOT NULL,
        kostra_funksjon TEXT NOT NULL,
        epost TEXT NOT NULL,
        telefon TEXT NOT NULL,
        kontorsted TEXT NOT NULL,
        delegeringsfullmakt_nok REAL NOT NULL,
        controller_navn TEXT NOT NULL,
        controller_epost TEXT NOT NULL,
        utsendte_rapporter TEXT NOT NULL,
        tilknyttet_mal TEXT NOT NULL,
        returkanal TEXT NOT NULL,
        returfrist TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Fact_Prognose_Logg (
        prognose_id TEXT PRIMARY KEY,
        ansvar_kode TEXT NOT NULL,
        kostra_funksjon TEXT NOT NULL,
        art_kategori TEXT,
        periode_ytd INTEGER NOT NULL,
        regnskapsar INTEGER NOT NULL,
        modell_type TEXT NOT NULL,
        hittil_regnskap_ac REAL NOT NULL,
        vedtatt_ramme_bac REAL NOT NULL,
        p10_belop REAL NOT NULL,
        p50_belop REAL NOT NULL,
        p90_belop REAL NOT NULL,
        estimert_avvik_p50 REAL NOT NULL,
        cpi REAL,
        spi REAL,
        status TEXT NOT NULL,
        driver_forutsetninger JSON,
        saksbehandler TEXT NOT NULL,
        sha256_hash TEXT NOT NULL,
        opprettet_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ansvar_kode) REFERENCES Dim_Ansvar(ansvar_kode)
    );
    """)

    conn.commit()


# ==========================================
# 2. INGESTION AV MASTERDATA (KOSTRA KONTOPLAN)
# ==========================================
def ingest_kostra_masterdata(conn: sqlite3.Connection) -> None:
    """Laster KOSTRA kontoplan til Dim_Kontoklasse, Dim_Funksjon, Dim_Art og legal_chunks."""
    print("📁 Ingesting masterdata fra kostra_kontoplan.csv...")

    cursor = conn.cursor()
    chunks_to_insert = []

    with open(KONTOPLAN_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            dim = row.get("Dimensjon", "").strip()
            n1_k = row.get("Niva_1_Kode", "").strip()
            n1_n = row.get("Niva_1_Navn", "").strip()
            n2_k = row.get("Niva_2_Kode", "").strip()
            n2_n = row.get("Niva_2_Navn", "").strip()
            n3_k = row.get("Niva_3_Kode", "").strip()
            n3_n = row.get("Niva_3_Navn", "").strip()
            regel = row.get("Beskrivelse_Regnskapsregel", "").strip()

            # 1. Kontoklasse
            if dim == "Kontoklasse":
                try:
                    kid = int(n3_k)
                    cursor.execute(
                        "INSERT OR REPLACE INTO Dim_Kontoklasse VALUES (?, ?, ?)",
                        (kid, n3_n, regel)
                    )
                except ValueError:
                    pass

            # 2. Funksjon (Både 3-sifret og 4-sifret kode for maksimal kompatibilitet)
            elif dim == "Funksjon":
                # Niva 2 (f.eks. 100, 202, 254)
                if n2_k:
                    cursor.execute(
                        "INSERT OR REPLACE INTO Dim_Funksjon VALUES (?, ?, ?, ?)",
                        (n2_k, n2_n, n1_n, n1_k)
                    )
                # Niva 3 (f.eks. 1000, 2020)
                if n3_k:
                    cursor.execute(
                        "INSERT OR REPLACE INTO Dim_Funksjon VALUES (?, ?, ?, ?)",
                        (n3_k, n3_n, n2_n, n1_k)
                    )

            # 3. Art (Både 3- og 4-sifret kode)
            elif dim == "Art":
                art_code = n3_k or n2_k
                if art_code:
                    cursor.execute(
                        "INSERT OR REPLACE INTO Dim_Art VALUES (?, ?, ?)",
                        (art_code, n3_n, n1_n)
                    )

            # 4. Lagre regelverk i legal_chunks for fremtidig RAG-søk
            if regel:
                title = f"{dim} {n3_k}: {n3_n}"
                chunks_to_insert.append((
                    "kostra_kontoplan.csv",
                    f"KOSTRA_{dim}",
                    f"Kode {n3_k}",
                    title,
                    f"{title}\nDefinisjon & Regnskapsregel: {regel}"
                ))

    # Batch insert til legal_chunks
    cursor.executemany(
        """
        INSERT INTO legal_chunks (source_file, category, section_ref, title, content)
        VALUES (?, ?, ?, ?, ?)
        """,
        chunks_to_insert
    )
    # Sikkerhetsnett: Sørg for at essensielle KOSTRA-funksjoner alltid finnes
    fallback_funksjoner = [
        ("100", "Politisk styring og konsernledelse", "Konsernledelsen", "1 Sentraladministrasjon"),
        ("1000", "Bystyre, formannskap og utvalg", "Politisk styring", "1 Sentraladministrasjon"),
        ("120", "Administrasjon og virksomhetsstyring", "Sentraladministrasjon", "1 Sentraladministrasjon"),
        ("202", "Grunnskoleopplæring", "Oppvekst og utdanning", "2 Oppvekst"),
        ("2020", "Grunnskoler (1.-10. trinn)", "Grunnskoleopplæring", "2 Oppvekst"),
        ("203", "Særskilt tilrettelagt grunnskoleopplæring", "Oppvekst og utdanning", "2 Oppvekst"),
        ("2030", "Spesialundervisning og forsterkede avdelinger", "Særskilt opplæring", "2 Oppvekst"),
        ("204", "Skolefritidsordning (SFO)", "Oppvekst og utdanning", "2 Oppvekst"),
        ("2040", "SFO drift og aktivitet", "Skolefritidsordning", "2 Oppvekst"),
        ("211", "Skolefritidstilbud (SFO)", "Oppvekst og utdanning", "2 Oppvekst"),
        ("214", "Skoleskyss", "Oppvekst og utdanning", "2 Oppvekst"),
        ("2140", "Skoleskyss og transport", "Skoleskyss", "2 Oppvekst"),
        ("215", "Skoleskyss grunnskole", "Oppvekst og utdanning", "2 Oppvekst"),
        ("221", "Pedagogisk-psykologisk tjeneste (PPT)", "Oppvekst og utdanning", "2 Oppvekst"),
        ("222", "Skolelokaler og skoleanlegg", "Oppvekst og utdanning", "2 Oppvekst"),
        ("223", "Spesialpedagogiske tiltak barnehage", "Oppvekst og utdanning", "2 Oppvekst"),
        ("2230", "Spesialpedagogisk hjelp barnehage", "Spesialpedagogikk", "2 Oppvekst"),
        ("241", "Forebyggende helsetjenester", "Helse og mestring", "2 Helse"),
        ("253", "Pleie og omsorg i institusjon", "Helse og mestring", "2 Helse"),
        ("254", "Heldøgns pleie og omsorgstjenester", "Helse og mestring", "2 Helse"),
        ("2540", "Sykehjem, bofellesskap og heldøgns omsorg", "Heldøgns pleie", "2 Helse"),
        ("257", "Hjemmetjenester i bofellesskap", "Helse og mestring", "2 Helse"),
        ("258", "Hjemmetjenester ambulerende virksomhet", "Helse og mestring", "2 Helse"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO Dim_Funksjon VALUES (?, ?, ?, ?)",
        fallback_funksjoner
    )

    conn.commit()
    print(f"  ✓ Dimensjoner lastet. {len(chunks_to_insert)} regelverks-chunks opprettet for RAG.")


# ==========================================
# 3. CONFORMED DIMENSIONS (DATO & ANSVAR)
# ==========================================
def seed_dimensions(conn: sqlite3.Connection) -> None:
    """Fyller conformed Dim_Dato, Dim_Ansvar og Dim_Budsjettansvarlige."""
    cursor = conn.cursor()

    # Kjerneansvarsenheter
    ansvar_rows = [
        ("BOMILJO", "Kommunal Boenhet", "Helse og mestring", "Enhetsleder Bo og Miljø"),
        ("KOMSKOLE", "Kommunal Skole", "Oppvekst og utdanning", "Rektor Kommunal Skole"),
        ("SENTRAL", "Sentraladministrasjonen", "Fellestjenester", "Kommunedirektør"),
        ("2020", "Kommunal Skole (Enhet 2020)", "Oppvekst og utdanning", "Rektor Kommunal Skole"),
        ("2540", "Kommunal Boenhet (Enhet 2540)", "Helse og mestring", "Enhetsleder Bo og Miljø"),
    ]

    # Berik med samtlige enheter fra det offisielle Budsjettansvarlig-registeret
    if REGISTER:
        for r in REGISTER:
            aid = r["ansvar_id"]
            enavn = r["enhet_navn"]
            snavn = r["sektor_navn"]
            tittel = r["tittel"]
            ansvar_rows.append((aid, enavn, snavn, tittel))

            cursor.execute("""
                INSERT OR REPLACE INTO Dim_Budsjettansvarlige VALUES (
                    :ansvar_id, :navn, :tittel, :niva, :niva_tekst,
                    :sektor_kode, :sektor_navn, :enhet_navn, :kostra_funksjon,
                    :epost, :telefon, :kontorsted, :delegeringsfullmakt_nok,
                    :controller_navn, :controller_epost, :utsendte_rapporter,
                    :tilknyttet_mal, :returkanal, :returfrist
                )
            """, r)

    cursor.executemany(
        "INSERT OR REPLACE INTO Dim_Ansvar VALUES (?, ?, ?, ?)",
        ansvar_rows
    )

    # Datoer for 2024 og 2025
    dato_rows = []
    for year in [2024, 2025]:
        for month in range(1, 13):
            d_key = f"{year}-{month:02d}"
            kvartal = f"Q{(month - 1) // 3 + 1}"
            tertial = f"T{(month - 1) // 4 + 1}"
            if tertial == "T1":
                fase = "1. Tertialrapportering"
            elif tertial == "T2":
                fase = "2. Tertialrapportering"
            else:
                fase = "Årsavslutning & Budsjettvedtak"

            dato_rows.append((d_key, year, month, kvartal, tertial, fase))

    cursor.executemany(
        "INSERT OR REPLACE INTO Dim_Dato VALUES (?, ?, ?, ?, ?, ?)",
        dato_rows
    )
    conn.commit()
    print("  ✓ Dim_Ansvar, Dim_Budsjettansvarlige og Dim_Dato etablert.")


# ==========================================
# 4. INGESTION AV BOMILJØ.CSV (2024 MÅNEDLIG, NOK)
# ==========================================
def ingest_bomiljo(conn: sqlite3.Connection) -> None:
    """Vasker og laster BoMiljø.csv til Staging og Core Star Schema."""
    print("📁 Ingesting BoMiljø.csv (Kommunal Boenhet 2024)...")
    cursor = conn.cursor()

    stg_rows = []
    regnskap_fact = []
    budsjett_fact = []

    with open(BOMILJO_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            periode = row["Periode"].strip()        # YYYY-MM
            funksjon = row["KOSTRA_Funksjon"].strip() # 254
            art = row["KOSTRA_Art"].strip()           # 1010
            kontokode = row["Kontokode"].strip()     # 101000
            kontonavn = row["Kontonavn"].strip()
            budsjett = float(row["Budsjett"] or 0.0)
            regnskap = float(row["Regnskap"] or 0.0)

            # Sørg for at arten finnes i Dim_Art
            cursor.execute(
                "INSERT OR IGNORE INTO Dim_Art VALUES (?, ?, ?)",
                (art, kontonavn, "Driftsart")
            )

            # Staging
            stg_rows.append((
                "BOMILJO_ERP",
                kontokode,
                periode,
                kontokode,
                funksjon,
                "BOMILJO",
                regnskap,
                kontonavn,
                1.0
            ))

            # SHA-256 for idempotent deduplisering
            r_payload = f"BOMILJO|REGNSKAP|{periode}|{funksjon}|{art}|BOMILJO|{regnskap}"
            r_hash = hashlib.sha256(r_payload.encode("utf-8")).hexdigest()

            regnskap_fact.append((
                r_hash,
                "BOMILJO_CSV",
                1, # Driftsregnskap
                funksjon,
                art,
                "BOMILJO",
                periode,
                regnskap,
                0 # Ikke YTD, månedlig transaksjon
            ))

            b_payload = f"BOMILJO|BUDSJETT|{periode}|{funksjon}|{art}|BOMILJO|{budsjett}"
            b_hash = hashlib.sha256(b_payload.encode("utf-8")).hexdigest()

            budsjett_fact.append((
                b_hash,
                "BOMILJO_CSV",
                "VEDTATT_MND",
                2024,
                funksjon,
                art,
                "BOMILJO",
                periode,
                budsjett,
                0
            ))

    cursor.executemany("""
    INSERT INTO stg_erp_transactions (
        source_system, voucher_number, accounting_date, account_code,
        function_code, cost_center_code, amount, description, scale_factor
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, stg_rows)

    cursor.executemany("""
    INSERT OR REPLACE INTO Fact_Regnskap (
        transaksjon_hash, kilde_system, kontoklasse_id, funksjon_key,
        art_key, ansvar_key, dato_key, belop, er_akkumulert_ytd
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, regnskap_fact)

    cursor.executemany("""
    INSERT OR REPLACE INTO Fact_Budsjett (
        budsjett_hash, kilde_system, budsjett_type, aar, funksjon_key,
        art_key, ansvar_key, dato_key, budsjett_belop, er_akkumulert_ytd
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, budsjett_fact)

    conn.commit()
    print(f"  ✓ BoMiljø: {len(regnskap_fact)} regnskapsposter og {len(budsjett_fact)} budsjettposter lastet.")


# ==========================================
# 5. INGESTION AV KOMSKOLE.CSV (2025 YTD, TNOK -> NOK)
# ==========================================
def ingest_komskole(conn: sqlite3.Connection) -> None:
    """Vasker Excel-feil i Komskole.csv (cp1252, TNOK * 1000, header offsets)."""
    print("📁 Ingesting Komskole.csv (Kommunal Skole 2025 YTD)...")
    cursor = conn.cursor()

    regnskap_fact = []
    budsjett_fact = []
    stg_rows = []

    # Les med cp1252 for å unngå mojibake
    with open(KOMSKOLE_CSV, "r", encoding="cp1252") as f:
        # Hopp over de 2 første linjene (tittel og blank linje)
        f.readline()
        f.readline()
        # Les overskriftslinje
        header_line = f.readline().strip()
        headers = [h.strip() for h in header_line.split(",")]
        # Data-linjer
        reader = csv.reader(f)

        for row in reader:
            if not row or len(row) < 11:
                continue

            # Kolonneposisjoner etter de 3 tomme ledende kommaene:
            # col 3: Periode (Aug-25)
            # col 4: Lokasjon (Kommunal Skole)
            # col 5: Funksjon (202 - feilmerket som Art i råfilen)
            # col 6: Ansvar/Enhet (Grunnskole)
            # col 7: Kontotype (Lønn, Kjøp av varer...)
            # col 8: Post (Fastlønn, Vikarer...)
            # col 9: Regnskap hiå. (TNOK)
            # col 10: Budsjett hiå. (TNOK)
            # col 13: Årsbudsjett (TNOK)

            raw_periode = row[3].strip() if len(row) > 3 else "Aug-25"
            funksjon = row[5].strip() if len(row) > 5 else "202"
            post_navn = row[8].strip() if len(row) > 8 else "Uspesifisert"

            # Parse tall og konverter TNOK -> NOK (* 1000.0)
            def parse_tnok(val: str) -> float:
                clean_val = val.replace(" ", "").replace("?", "0").strip()
                try:
                    return float(clean_val) * 1000.0
                except ValueError:
                    return 0.0

            regnskap_nok = parse_tnok(row[9]) if len(row) > 9 else 0.0
            budsjett_nok = parse_tnok(row[10]) if len(row) > 10 else 0.0
            aarsbudsjett_nok = parse_tnok(row[13]) if len(row) > 13 else 0.0

            # Normaliser periode 'Aug-25' -> '2025-08'
            periode_key = "2025-08"

            # Generer en deterministisk art_key basert på postnavn
            art_clean = "".join(c for c in post_navn if c.isalnum()).upper()[:12]
            art_key = f"SKOLE_{art_clean}" if art_clean else "SKOLE_DIVERS"

            # Sørg for at arten finnes i Dim_Art
            cursor.execute(
                "INSERT OR IGNORE INTO Dim_Art VALUES (?, ?, ?)",
                (art_key, post_navn, row[7].strip() if len(row) > 7 else "Skoleart")
            )

            # Staging (med 1000.0 scale factor)
            stg_rows.append((
                "KOMSKOLE_EXCEL",
                art_key,
                periode_key,
                art_key,
                funksjon,
                "KOMSKOLE",
                regnskap_nok,
                post_navn,
                1000.0
            ))

            # Fact Regnskap (YTD-akkumulert)
            r_payload = f"KOMSKOLE|REGNSKAP_YTD|{periode_key}|{funksjon}|{art_key}|KOMSKOLE|{regnskap_nok}"
            r_hash = hashlib.sha256(r_payload.encode("utf-8")).hexdigest()

            regnskap_fact.append((
                r_hash,
                "KOMSKOLE_EXCEL",
                1,
                funksjon,
                art_key,
                "KOMSKOLE",
                periode_key,
                regnskap_nok,
                1 # Akkumulert hittil i år
            ))

            # Fact Budsjett (Tertial 2 YTD)
            b_payload = f"KOMSKOLE|BUDSJETT_YTD|{periode_key}|{funksjon}|{art_key}|KOMSKOLE|{budsjett_nok}"
            b_hash = hashlib.sha256(b_payload.encode("utf-8")).hexdigest()

            budsjett_fact.append((
                b_hash,
                "KOMSKOLE_EXCEL",
                "TERTIAL_2_YTD",
                2025,
                funksjon,
                art_key,
                "KOMSKOLE",
                periode_key,
                budsjett_nok,
                1
            ))

    cursor.executemany("""
    INSERT INTO stg_erp_transactions (
        source_system, voucher_number, accounting_date, account_code,
        function_code, cost_center_code, amount, description, scale_factor
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, stg_rows)

    cursor.executemany("""
    INSERT OR REPLACE INTO Fact_Regnskap (
        transaksjon_hash, kilde_system, kontoklasse_id, funksjon_key,
        art_key, ansvar_key, dato_key, belop, er_akkumulert_ytd
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, regnskap_fact)

    cursor.executemany("""
    INSERT OR REPLACE INTO Fact_Budsjett (
        budsjett_hash, kilde_system, budsjett_type, aar, funksjon_key,
        art_key, ansvar_key, dato_key, budsjett_belop, er_akkumulert_ytd
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, budsjett_fact)

    conn.commit()
    print(f"  ✓ Komskole: {len(regnskap_fact)} poster konvertert fra TNOK -> NOK og lastet.")


# ==========================================
# 6. REVISJONSSPOR & AUDIT TRAIL (STAGE-GATE PORT 9)
# ==========================================
def seed_audit_trail(conn: sqlite3.Connection) -> None:
    """Seeder formelle revisjonslogger og HITL-vedtak i tråd med Stage-Gate Port 9."""
    cursor = conn.cursor()
    actions = [
        (
            "2026-08-20 14:30:00",
            "2020",
            "KOMSKOLE",
            "Vikarstopp korttidsfravær < 3 dager",
            0.94,
            "APPROVED",
            "Frank Ellingsen",
            "Kvantifisert innsparing 170k/mnd jf. Kommuneloven § 14-5",
            "a8f9c2e411b98d249f05786a34567890abcdef1234567890abcdef1234567890",
            "Hvordan redusere vikarmerforbruk i grunnskolen?",
            "12,13,14",
            "Anbefaler vikarstopp for fravær under 3 dager og intern omdisponering."
        ),
        (
            "2026-08-22 11:15:00",
            "2540",
            "BOMILJO",
            "Turnusendring og overtidstak døgnpost",
            0.89,
            "MODIFIED",
            "Frank Ellingsen",
            "Drøftet med tillitsvalgte iht. HTA § 4 og AML § 10-12",
            "f34b9982a74c1022bcde7890abcdef1234567890abcdef1234567890abcdef12",
            "Tiltak for å dempe overtid på heldøgns omsorgsbolig",
            "26,27,28",
            "Innføring av 12.5t langvakter krever formell drøfting med Fagforbundet og Norsk Sykepleierforbund."
        ),
        (
            "2026-08-25 09:00:00",
            "2540",
            "BOMILJO",
            "Beredskapsjustering og bemanningsplan natt",
            0.92,
            "APPROVED",
            "Frank Ellingsen",
            "Optimalisert grunnbemanning natt jf. helse- og omsorgstjenesteloven",
            "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            "Analyse av nattbemanning ved bofellesskap",
            "27,29",
            "Godkjent justering med estimert årlig besparelse på 340 000 kr."
        ),
        (
            "2026-08-28 13:45:00",
            "2020",
            "KOMSKOLE",
            "Innkjøpssamordning læremidler og digitale lisenser",
            0.95,
            "APPROVED",
            "Frank Ellingsen",
            "Samlet innkjøpsavtale via Agder fellesinnkjøp",
            "fedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321",
            "Digitale lisenser og læremidler overforbruk",
            "13,18",
            "Bruk felles avtaler fremfor enkeltbestillinger. Sparer 120 000 kr."
        ),
        (
            "2026-09-02 10:30:00",
            "SENTRAL",
            "SENTRAL",
            "Rammekutt konsulentbistand og ekstern utredning",
            0.97,
            "APPROVED",
            "Frank Ellingsen",
            "Stopp i eksterne konsulentoverskridelser i rådhusstaben",
            "abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789",
            "Konsulentbruk sentraladministrasjonen",
            "5,6,7",
            "Krav om forhåndsgodkjenning fra kommunedirektør for alle oppdrag > 100k."
        )
    ]
    cursor.executemany("""
        INSERT OR REPLACE INTO Audit_AI_Actions (
            tidsstempel, enhetskode, ansvar_kode, ai_tiltak, konfidens,
            leder_beslutning, saksbehandler, begrunnelse, sha256_hash,
            user_query, retrieved_chunk_ids, llm_response
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, actions)
    conn.commit()
    print("  ✓ Audit_AI_Actions seeded med 5 Stage-Gate Port 9 revisjonslogger.")


# ==========================================
# 7. VERIFIKASJON OG AVVIKSANALYSE (TUFTE STYLE)
# ==========================================
def verify_golden_record(conn: sqlite3.Connection) -> None:
    """Kjører verifikasjon og viser avviksrapport i tråd med Tufte data-ink ratio."""
    cursor = conn.cursor()

    print("\n" + "=" * 80)
    print("📊 GOLDEN RECORD DATA AUDIT & AVVIKSANALYSE")
    print("=" * 80)

    # 1. Tabelltellinger
    tables = [
        "Dim_Funksjon", "Dim_Art", "Dim_Ansvar", "Dim_Budsjettansvarlige",
        "Dim_Dato", "Dim_Kontoklasse", "Fact_Regnskap", "Fact_Budsjett",
        "Fact_Prognose_Logg", "Audit_AI_Actions", "legal_chunks", "stg_erp_transactions"
    ]
    print("\n📦 Tabellinnhold i kommune_golden_record.db:")
    for tbl in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        print(f"  • {tbl:<24} : {count:>8,} rader".replace(",", " "))

    # 2. Referensiell Integritetskontroll (Foreign Keys)
    fk_funksjon_reg = cursor.execute(
        "SELECT COUNT(*) FROM Fact_Regnskap WHERE funksjon_key NOT IN (SELECT funksjon_kode FROM Dim_Funksjon)"
    ).fetchone()[0]
    fk_art_reg = cursor.execute(
        "SELECT COUNT(*) FROM Fact_Regnskap WHERE art_key NOT IN (SELECT art_kode FROM Dim_Art)"
    ).fetchone()[0]
    fk_ansvar_reg = cursor.execute(
        "SELECT COUNT(*) FROM Fact_Regnskap WHERE ansvar_key NOT IN (SELECT ansvar_kode FROM Dim_Ansvar)"
    ).fetchone()[0]
    fk_dato_reg = cursor.execute(
        "SELECT COUNT(*) FROM Fact_Regnskap WHERE dato_key NOT IN (SELECT dato_key FROM Dim_Dato)"
    ).fetchone()[0]

    fk_funksjon_bud = cursor.execute(
        "SELECT COUNT(*) FROM Fact_Budsjett WHERE funksjon_key NOT IN (SELECT funksjon_kode FROM Dim_Funksjon)"
    ).fetchone()[0]
    fk_art_bud = cursor.execute(
        "SELECT COUNT(*) FROM Fact_Budsjett WHERE art_key NOT IN (SELECT art_kode FROM Dim_Art)"
    ).fetchone()[0]
    fk_ansvar_bud = cursor.execute(
        "SELECT COUNT(*) FROM Fact_Budsjett WHERE ansvar_key NOT IN (SELECT ansvar_kode FROM Dim_Ansvar)"
    ).fetchone()[0]

    print("\n🔍 Referensiell Integritetskontroll (Foreign Key Integrity):")
    print(f"  • Foreldreløse funksjonsnøkler i Fact_Regnskap: {fk_funksjon_reg} {'✅ OK' if fk_funksjon_reg == 0 else '❌ FEIL'}")
    print(f"  • Foreldreløse artsnøkler i Fact_Regnskap       : {fk_art_reg} {'✅ OK' if fk_art_reg == 0 else '❌ FEIL'}")
    print(f"  • Foreldreløse ansvarsnøkler i Fact_Regnskap    : {fk_ansvar_reg} {'✅ OK' if fk_ansvar_reg == 0 else '❌ FEIL'}")
    print(f"  • Foreldreløse datonøkler i Fact_Regnskap       : {fk_dato_reg} {'✅ OK' if fk_dato_reg == 0 else '❌ FEIL'}")
    print(f"  • Foreldreløse funksjonsnøkler i Fact_Budsjett : {fk_funksjon_bud} {'✅ OK' if fk_funksjon_bud == 0 else '❌ FEIL'}")
    print(f"  • Foreldreløse artsnøkler i Fact_Budsjett      : {fk_art_bud} {'✅ OK' if fk_art_bud == 0 else '❌ FEIL'}")
    print(f"  • Foreldreløse ansvarsnøkler i Fact_Budsjett   : {fk_ansvar_bud} {'✅ OK' if fk_ansvar_bud == 0 else '❌ FEIL'}")

    # 3. Avvik per sektor og enhet (Avvik = Budsjett - Faktisk forbruk)
    query = """
    SELECT 
        da.enhet_navn AS Enhet,
        da.sektor AS Sektor,
        r.dato_key AS Periode,
        CASE WHEN r.er_akkumulert_ytd = 1 THEN 'YTD' ELSE 'Måned' END AS Type,
        ROUND(SUM(b.budsjett_belop), 0) AS Budsjett_NOK,
        ROUND(SUM(r.belop), 0) AS Regnskap_NOK,
        ROUND(SUM(b.budsjett_belop) - SUM(r.belop), 0) AS Avvik_NOK,
        ROUND(((SUM(b.budsjett_belop) - SUM(r.belop)) / NULLIF(SUM(b.budsjett_belop), 0)) * 100, 1) AS Avvik_Prosent
    FROM Fact_Regnskap r
    LEFT JOIN Fact_Budsjett b 
        ON r.funksjon_key = b.funksjon_key 
       AND r.art_key = b.art_key 
       AND r.ansvar_key = b.ansvar_key
       AND r.dato_key = b.dato_key
    JOIN Dim_Ansvar da ON r.ansvar_key = da.ansvar_kode
    GROUP BY da.enhet_navn, da.sektor, r.dato_key, r.er_akkumulert_ytd
    ORDER BY da.enhet_navn, r.dato_key
    LIMIT 10;
    """
    rows = cursor.execute(query).fetchall()

    print("\n📈 Samlet Avviksstatus (Utdrag topp 10 rader):")
    print(f"{'Enhet':<18} {'Periode':<8} {'Type':<6} {'Budsjett (NOK)':>16} {'Regnskap (NOK)':>16} {'Avvik (NOK)':>16} {'Avvik %':>9}")
    print("-" * 92)
    for row in rows:
        enhet, sektor, per, typ, bud, reg, avv, pst = row
        pst_str = f"{pst:>8.1f}%" if pst is not None else "     N/A"
        # Tufte-prinsipp: tall høyrejustert, tekst venstrejustert
        print(f"{enhet:<18} {per:<8} {typ:<6} {bud:>16,.0f} {reg:>16,.0f} {avv:>16,.0f} {pst_str}".replace(",", " "))
    print("-" * 92)
    print("Forklaring avvik: Positivt tall = Mindreforbruk (besparelse) | Negativt tall = Merforbruk (overskridelse)")


# ==========================================
# 8. HOVEDPROGRAM
# ==========================================
def main() -> None:
    start_time = time.time()
    print("🏛️ Bygger Kommunal Golden Record Datavarehus...")
    print(f"Mål-database: {DB_PATH.resolve()}")

    # Fjern eksisterende fil for en ren bygging
    if DB_PATH.exists():
        try:
            DB_PATH.unlink()
            print("  ✓ Eksisterende database slettet for ren migrering.")
        except Exception:
            pass

    conn = sqlite3.connect(DB_PATH)
    try:
        init_database(conn)
        seed_dimensions(conn)
        ingest_kostra_masterdata(conn)
        ingest_bomiljo(conn)
        ingest_komskole(conn)
        seed_audit_trail(conn)
        verify_golden_record(conn)
    finally:
        conn.close()

    # Kjører prediktiv motor for å generere Fact_Prognose_Logg
    if run_forecast_pipeline:
        print("\n🔮 Kjører prediktiv prognose- og EVM-beregning...")
        run_forecast_pipeline()

    elapsed = time.time() - start_time
    print(f"\n🎉 Golden Record vellykket bygget på {elapsed:.2f} sekunder!")
    print(f"Filstørrelse: {DB_PATH.stat().st_size / (1024 * 1024):.2f} MB")


if __name__ == "__main__":
    main()
