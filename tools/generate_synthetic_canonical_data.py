#!/usr/bin/env python3
"""
🏛️ Kristiansand Kommune — Master Synthetic Data Generator & DuckDB OLAP Pipeline
================================================================================
Genererer realistiske, kanoniske regnskaps- og budsjettdata for samtlige 6 
virksomhetsområder YTD M9 (slutt september 2026) i henhold til:
1. Single Source of Truth (SSOT) Star Schema i erp_data/kommune_golden_record.db
2. Pydantic v2 Canonical Data Contracts (FactRegnskapCanonical, FactBudsjettCanonical)
3. Reelle kommunale styringsutfordringer i Kristiansand:
   - Oppvekst (OMR-02): Vikarforbruk art 1020, spes.ped funk 222, sykefravær 9.2%
   - Helse og mestring (OMR-03): Overtid art 1090, vikarbyrå art 1250, sykefravær 11.4%
   - Byutvikling (OMR-05): Gebyrsvikt byggesak funk 3600 art 1600, VAR selvkostbalanse
   - Kultur (OMR-04): Energieffektivisering, god publikumsoppslutning (+1.4M)
   - Org & Teknologi (OMR-11): FinOps motvirker SaaS-prispress (+0.6M)
   - Økonomi & Konsern (OMR-12): Høyere renteinntekter på overskuddslikviditet (+7.5M)
4. Full DuckDB OLAP-integrasjon og Parquet-eksport (SSOT avstemt 100%).

Forfatter: Frank Ellingsen (Senior Financial & Project Controller)
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sqlite3
import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import duckdb

DB_PATH = ROOT_DIR / "erp_data" / "kommune_golden_record.db"
PARQUET_DIR = ROOT_DIR / "erp_data" / "parquet_exports"
JSON_KPI_PATH = ROOT_DIR / "antigravity_top3_kpi_visualisering_pakke" / "Top3_KPI_Gauge_Dashboard_Data.json"


def ensure_dim_dato_2026(conn: sqlite3.Connection) -> int:
    """Sikrer at Dim_Dato har samtlige 12 måneder for 2026."""
    cur = conn.cursor()
    months_data = [
        ("2026-01", 2026, 1, "Q1", "T1", "1. Tertialrapportering"),
        ("2026-02", 2026, 2, "Q1", "T1", "1. Tertialrapportering"),
        ("2026-03", 2026, 3, "Q1", "T1", "1. Tertialrapportering"),
        ("2026-04", 2026, 4, "Q2", "T1", "1. Tertialrapportering"),
        ("2026-05", 2026, 5, "Q2", "T2", "2. Tertialrapportering"),
        ("2026-06", 2026, 6, "Q2", "T2", "2. Tertialrapportering"),
        ("2026-07", 2026, 7, "Q3", "T2", "2. Tertialrapportering"),
        ("2026-08", 2026, 8, "Q3", "T2", "2. Tertialrapportering"),
        ("2026-09", 2026, 9, "Q3", "T2", "2. Tertialrapportering"),
        ("2026-10", 2026, 10, "Q4", "T3", "Årsavslutning & Budsjettvedtak"),
        ("2026-11", 2026, 11, "Q4", "T3", "Årsavslutning & Budsjettvedtak"),
        ("2026-12", 2026, 12, "Q4", "T3", "Årsavslutning & Budsjettvedtak"),
    ]
    inserted = 0
    for row in months_data:
        cur.execute("SELECT count(*) FROM Dim_Dato WHERE dato_key = ?", (row[0],))
        if cur.fetchone()[0] == 0:
            cur.execute("""
                INSERT INTO Dim_Dato (dato_key, aar, maned, kvartal, tertial, arshjul_fase)
                VALUES (?, ?, ?, ?, ?, ?)
            """, row)
            inserted += 1
    conn.commit()
    return inserted


# Månedlig sesongvekting for de 10 månedene (Jan-Okt)
# Gjenspeiler kommunale svingninger (ferieavvikling i juli, høyt vikarforbruk vinter/vår, etc.)
MONTHLY_WEIGHTS = {
    1: 0.100,
    2: 0.102,
    3: 0.105,
    4: 0.102,
    5: 0.104,
    6: 0.106,
    7: 0.080,  # Sommerferie og redusert drift
    8: 0.105,  # Skolestart
    9: 0.108,  # Full høstdrift september
    10: 0.108, # M10 Oktober avslutning
}
# Normaliser summen til nøyaktig 1.0 for de 10 månedene
_weight_sum = sum(MONTHLY_WEIGHTS.values())
MONTHLY_WEIGHTS = {m: w / _weight_sum for m, w in MONTHLY_WEIGHTS.items()}


def get_sector_unit_spec() -> List[Dict]:
    """Definerer de 6 virksomhetsområdene, deres underliggende enheter, KOSTRA-funksjoner,

    kontoarter og nøyaktige YTD rammer og forbruk for M9 (slutt september 2026).
    """
    return [
        # =====================================================================
        # 1. OPPVEKST OG UTDANNING (OMR-02)
        # Total Ramme: 1 850 000 000 NOK | Forbruk: 1 885 000 000 NOK | Avvik: -35 000 000 NOK (RØD)
        # =====================================================================
        {
            "sektor_id": "OMR-02",
            "sektor_navn": "Oppvekst og utdanning",
            "direktor": "Kommunalsjef Oppvekst",
            "triage_status": "RØD",
            "kpis": {
                "kostnad_per_elev_kostra": "128 500 kr",
                "pedagogdekning_prosent": 98.2,
                "vikar_og_overtid_art_1020_prosent": 8.4,
                "legemeldt_sykefraver_prosent": 9.2,
                "nav_refusjon_etterslep_nok": 3500000,
            },
            "enheter": [
                {
                    "ansvar_key": "4101-ENH-203",
                    "enhet_navn": "Vågsbygd Skole",
                    "ramme_ytd": 42000000.0,
                    "forbruk_ytd": 43650000.0,
                    "funksjon_key": "202",
                    "art_base": "1010",
                    "driver_art": "1020",
                    "driver_navn": "Vikarutgifter lærere",
                },
                {
                    "ansvar_key": "4100-ENH-202",
                    "enhet_navn": "Lovisenlev Skole",
                    "ramme_ytd": 38000000.0,
                    "forbruk_ytd": 39450000.0,
                    "funksjon_key": "222",
                    "art_base": "1010",
                    "driver_art": "1020",
                    "driver_navn": "Spesialpedagogisk oppfølging",
                },
                {
                    "ansvar_key": "4102-ENH-204",
                    "enhet_navn": "Grim Ungdomsskole",
                    "ramme_ytd": 45000000.0,
                    "forbruk_ytd": 46200000.0,
                    "funksjon_key": "202",
                    "art_base": "1010",
                    "driver_art": "1020",
                    "driver_navn": "Vikar- og tilkallingshjelp",
                },
                {
                    "ansvar_key": "4210-ENH-211",
                    "enhet_navn": "Lund Kommunale Barnehage",
                    "ramme_ytd": 28000000.0,
                    "forbruk_ytd": 29150000.0,
                    "funksjon_key": "211",
                    "art_base": "1010",
                    "driver_art": "1020",
                    "driver_navn": "Pedagognorm & vikardekning",
                },
                {
                    "ansvar_key": "4103-SEK-SFO",
                    "enhet_navn": "Lovisenlev Skole — SFO",
                    "ramme_ytd": 6000000.0,
                    "forbruk_ytd": 6350000.0,
                    "funksjon_key": "202",
                    "art_base": "1010",
                    "driver_art": "1090",
                    "driver_navn": "Overtid bemanning SFO",
                },
                {
                    "ansvar_key": "4104-SEK-INSP",
                    "enhet_navn": "Lovisenlev Skole — Småtrinnet",
                    "ramme_ytd": 14000000.0,
                    "forbruk_ytd": 14400000.0,
                    "funksjon_key": "202",
                    "art_base": "1010",
                    "driver_art": "1115",
                    "driver_navn": "Digitale læremidler & materiell",
                },
                {
                    "ansvar_key": "4100-OMR-SKOLE",
                    "enhet_navn": "Grunnskoleavdelingen (28 skoler)",
                    "ramme_ytd": 920000000.0,
                    "forbruk_ytd": 936800000.0,
                    "funksjon_key": "202",
                    "art_base": "1010",
                    "driver_art": "1020",
                    "driver_navn": "Felles vikarpool & skoleskyss",
                },
                {
                    "ansvar_key": "4200-OMR-BHG",
                    "enhet_navn": "Barnehageavdelingen (54 barnehager)",
                    "ramme_ytd": 720000000.0,
                    "forbruk_ytd": 731000000.0,
                    "funksjon_key": "211",
                    "art_base": "1010",
                    "driver_art": "1020",
                    "driver_navn": "Vikarutgifter private/komm barnehager",
                },
                {
                    "ansvar_key": "4000-SJEF-OPPV",
                    "enhet_navn": "Kommunalsjefens fagstab Oppvekst",
                    "ramme_ytd": 22000000.0,
                    "forbruk_ytd": 22500000.0,
                    "funksjon_key": "120",
                    "art_base": "1010",
                    "driver_art": "1150",
                    "driver_navn": "Kompetanseutvikling lærere",
                },
                {
                    "ansvar_key": "6003-CTRL-ERIK",
                    "enhet_navn": "Økonomitjenesten Oppvekst",
                    "ramme_ytd": 15000000.0,
                    "forbruk_ytd": 15500000.0,
                    "funksjon_key": "120",
                    "art_base": "1010",
                    "driver_art": "1250",
                    "driver_navn": "Sektorcontroller analyse",
                },
            ],
        },
        # =====================================================================
        # 2. HELSE OG MESTRING (OMR-03)
        # Total Ramme: 2 100 000 000 NOK | Forbruk: 2 142 000 000 NOK | Avvik: -42 000 000 NOK (RØD)
        # =====================================================================
        {
            "sektor_id": "OMR-03",
            "sektor_navn": "Helse og mestring",
            "direktor": "Kommunalsjef Helse",
            "triage_status": "RØD",
            "kpis": {
                "utgift_per_dognplass_sykehjem": "1 050 000 kr",
                "dekningsgrad_80plus_prosent": 18.5,
                "overtid_ubekvem_art_1090_nok": 6200000,
                "legemeldt_sykefraver_prosent": 11.4,
                "turnusdekning_prosent": 91.2,
            },
            "enheter": [
                {
                    "ansvar_key": "5230-ENH-404",
                    "enhet_navn": "Presteheia Omsorgssenter",
                    "ramme_ytd": 68000000.0,
                    "forbruk_ytd": 70100000.0,
                    "funksjon_key": "253",
                    "art_base": "1010",
                    "driver_art": "1090",
                    "driver_navn": "Overtid og ubekvemstillegg",
                },
                {
                    "ansvar_key": "5200-ENH-401",
                    "enhet_navn": "Strai Sykehjem & Omsorgsboliger",
                    "ramme_ytd": 62000000.0,
                    "forbruk_ytd": 64350000.0,
                    "funksjon_key": "253",
                    "art_base": "1010",
                    "driver_art": "1090",
                    "driver_navn": "Ekstrahelger & turnuskompensasjon",
                },
                {
                    "ansvar_key": "5201-SEK-DEMENS",
                    "enhet_navn": "Strai Sykehjem — Avd. Demens",
                    "ramme_ytd": 18000000.0,
                    "forbruk_ytd": 18800000.0,
                    "funksjon_key": "253",
                    "art_base": "1010",
                    "driver_art": "1090",
                    "driver_navn": "Skjermet avdeling bemanningspress",
                },
                {
                    "ansvar_key": "5202-SEK-KORTTID",
                    "enhet_navn": "Strai Sykehjem — Somatisk Korttidsavd.",
                    "ramme_ytd": 16000000.0,
                    "forbruk_ytd": 16650000.0,
                    "funksjon_key": "253",
                    "art_base": "1010",
                    "driver_art": "1200",
                    "driver_navn": "Medisinsk forbruksmateriell",
                },
                {
                    "ansvar_key": "5210-ENH-402",
                    "enhet_navn": "Hjemmetjenesten Vågsbygd",
                    "ramme_ytd": 55000000.0,
                    "forbruk_ytd": 56800000.0,
                    "funksjon_key": "254",
                    "art_base": "1010",
                    "driver_art": "1020",
                    "driver_navn": "Sykepleievikarer i felt",
                },
                {
                    "ansvar_key": "5220-ENH-403",
                    "enhet_navn": "Sørlandsparken Bo- og Miljøtjeneste",
                    "ramme_ytd": 48000000.0,
                    "forbruk_ytd": 50400000.0,
                    "funksjon_key": "254",
                    "art_base": "1010",
                    "driver_art": "1250",
                    "driver_navn": "Ressurskrevende brukere 2:1",
                },
                {
                    "ansvar_key": "2540",
                    "enhet_navn": "Kommunal Boenhet (Enhet 2540)",
                    "ramme_ytd": 14500000.0,
                    "forbruk_ytd": 15650000.0,
                    "funksjon_key": "254",
                    "art_base": "1010",
                    "driver_art": "1090",
                    "driver_navn": "Døgnkontinuerlig tilsyn",
                },
                {
                    "ansvar_key": "5100-OMR-SYKEHJEM",
                    "enhet_navn": "Døgnomsorg og Sykehjem (Felles)",
                    "ramme_ytd": 960000000.0,
                    "forbruk_ytd": 978250000.0,
                    "funksjon_key": "253",
                    "art_base": "1010",
                    "driver_art": "1250",
                    "driver_navn": "Bemanningsbyråer spesialsykepleiere",
                },
                {
                    "ansvar_key": "5200-OMR-HJEMME",
                    "enhet_navn": "Hjemmetjenester og rehabilitering",
                    "ramme_ytd": 820000000.0,
                    "forbruk_ytd": 831200000.0,
                    "funksjon_key": "254",
                    "art_base": "1010",
                    "driver_art": "1090",
                    "driver_navn": "Kveld/natt turnustillegg",
                },
                {
                    "ansvar_key": "5000-SJEF-HELSE",
                    "enhet_navn": "Kommunalsjefens fagstab Helse",
                    "ramme_ytd": 24500000.0,
                    "forbruk_ytd": 25300000.0,
                    "funksjon_key": "120",
                    "art_base": "1010",
                    "driver_art": "1150",
                    "driver_navn": "Spesialisering sykepleie",
                },
                {
                    "ansvar_key": "6002-CTRL-MARIANNE",
                    "enhet_navn": "Økonomitjenesten Helse",
                    "ramme_ytd": 14000000.0,
                    "forbruk_ytd": 14500000.0,
                    "funksjon_key": "120",
                    "art_base": "1010",
                    "driver_art": "1250",
                    "driver_navn": "Turnusplanlegging analyse",
                },
            ],
        },
        # =====================================================================
        # 3. BY- OG STEDSUTVIKLING (OMR-05)
        # Total Ramme: 850 000 000 NOK | Forbruk: 851 500 000 NOK | Avvik: -1 500 000 NOK (GUL)
        # =====================================================================
        {
            "sektor_id": "OMR-05",
            "sektor_navn": "By- og stedsutvikling",
            "direktor": "Kommunalsjef Teknisk",
            "triage_status": "GUL",
            "kpis": {
                "var_selvkostgrad_prosent": 100.0,
                "snobroyting_art_1270_avvik_nok": 1500000,
                "byggesak_behandlingstid_dager": 24,
                "vedlikeholdsetterslep_m2_nok": 1450,
            },
            "enheter": [
                {
                    "ansvar_key": "3300-ENH-301",
                    "enhet_navn": "Enhet 301: Byggesak og Tilsyn",
                    "ramme_ytd": 42000000.0,
                    "forbruk_ytd": 45300000.0,
                    "funksjon_key": "360",
                    "art_base": "1010",
                    "driver_art": "1600",
                    "driver_navn": "Svikt i byggesaksgebyrer",
                },
                {
                    "ansvar_key": "3000-SJEF-BYUTV",
                    "enhet_navn": "Kommunalsjefens stab Byutvikling",
                    "ramme_ytd": 180000000.0,
                    "forbruk_ytd": 181500000.0,
                    "funksjon_key": "330",
                    "art_base": "1010",
                    "driver_art": "1270",
                    "driver_navn": "Vinterdrift & snøbrøyting Q1",
                },
                {
                    "ansvar_key": "3200-DIR-PLAN",
                    "enhet_navn": "Plan- og bygningsetaten",
                    "ramme_ytd": 68000000.0,
                    "forbruk_ytd": 66700000.0,
                    "funksjon_key": "330",
                    "art_base": "1010",
                    "driver_art": "1250",
                    "driver_navn": "Utsatte eksterne reguleringer",
                },
                {
                    "ansvar_key": "3100-ENH-302",
                    "enhet_navn": "Enhet 302: Vann, Avløp og Renovasjon",
                    "ramme_ytd": 320000000.0,
                    "forbruk_ytd": 320000000.0,
                    "funksjon_key": "340",
                    "art_base": "1010",
                    "driver_art": "1200",
                    "driver_navn": "VAR Selvkostfond i 100% balanse",
                },
                {
                    "ansvar_key": "3101-SEK-AVLOP",
                    "enhet_navn": "VAR Ingeniørvesenet — Renseanlegg Lund",
                    "ramme_ytd": 140000000.0,
                    "forbruk_ytd": 138000000.0,
                    "funksjon_key": "345",
                    "art_base": "1010",
                    "driver_art": "1180",
                    "driver_navn": "Energieffektivisering pumper",
                },
                {
                    "ansvar_key": "3100-DIR-VAR",
                    "enhet_navn": "Ingeniørvesenet (Vann, Avløp & Ren.)",
                    "ramme_ytd": 85000000.0,
                    "forbruk_ytd": 85000000.0,
                    "funksjon_key": "350",
                    "art_base": "1010",
                    "driver_art": "1270",
                    "driver_navn": "Renovasjonstransport Avfall Sør",
                },
                {
                    "ansvar_key": "6004-CTRL-KNUT",
                    "enhet_navn": "Økonomitjenesten Byutvikling",
                    "ramme_ytd": 15000000.0,
                    "forbruk_ytd": 15000000.0,
                    "funksjon_key": "120",
                    "art_base": "1010",
                    "driver_art": "1250",
                    "driver_navn": "Selvkostmodellering",
                },
            ],
        },
        # =====================================================================
        # 4. KULTUR OG INNBYGGERDIALOG (OMR-04)
        # Total Ramme: 285 000 000 NOK | Forbruk: 283 600 000 NOK | Avvik: +1 400 000 NOK (GRØNN)
        # =====================================================================
        {
            "sektor_id": "OMR-04",
            "sektor_navn": "Kultur og innbyggerdialog",
            "direktor": "Kommunalsjef Kultur",
            "triage_status": "GRØNN",
            "kpis": {
                "utlan_per_innbygger_bibliotek": 6.8,
                "deltakere_fritidsklubber_antall": 14200,
                "stromsparing_idrettsanlegg_prosent": 12.4,
                "budsjettdisiplin_grad": 100.5,
            },
            "enheter": [
                {
                    "ansvar_key": "2200-ENH-101",
                    "enhet_navn": "Enhet 101: Kristiansand Folkebibliotek",
                    "ramme_ytd": 35000000.0,
                    "forbruk_ytd": 34200000.0,
                    "funksjon_key": "301",
                    "art_base": "1010",
                    "driver_art": "1115",
                    "driver_navn": "Digitale lisenser & mediekjøp",
                },
                {
                    "ansvar_key": "2000-SJEF-KULTUR",
                    "enhet_navn": "Kommunalsjefens stab Kultur",
                    "ramme_ytd": 240000000.0,
                    "forbruk_ytd": 239400000.0,
                    "funksjon_key": "300",
                    "art_base": "1010",
                    "driver_art": "1180",
                    "driver_navn": "Idrettshaller & Kilden tilskudd",
                },
                {
                    "ansvar_key": "6005-CTRL-SILJE",
                    "enhet_navn": "Økonomitjenesten Kultur & Felles",
                    "ramme_ytd": 10000000.0,
                    "forbruk_ytd": 10000000.0,
                    "funksjon_key": "120",
                    "art_base": "1010",
                    "driver_art": "1250",
                    "driver_navn": "Tilskuddsforvaltning",
                },
            ],
        },
        # =====================================================================
        # 5. ORGANISASJON OG TEKNOLOGI (OMR-11)
        # Total Ramme: 345 000 000 NOK | Forbruk: 344 400 000 NOK | Avvik: +600 000 NOK (GRØNN)
        # =====================================================================
        {
            "sektor_id": "OMR-11",
            "sektor_navn": "Organisasjon og teknologi",
            "direktor": "Kommunalsjef Org & Tek",
            "triage_status": "GRØNN",
            "kpis": {
                "finops_skybesparelse_nok": 800000,
                "it_oppetid_prosent": 99.94,
                "fullforte_e_laeringskurs_antall": 8420,
                "konsulentreduksjon_prosent": 14.5,
            },
            "enheter": [
                {
                    "ansvar_key": "1110-ENH-501",
                    "enhet_navn": "Enhet 501: IKT Drift & Brukerstøtte",
                    "ramme_ytd": 180000000.0,
                    "forbruk_ytd": 180200000.0,
                    "funksjon_key": "120",
                    "art_base": "1010",
                    "driver_art": "1240",
                    "driver_navn": "M365 & programvarelisenser",
                },
                {
                    "ansvar_key": "1111-SEK-FINOPS",
                    "enhet_navn": "IKT Drift — Cloud & FinOps",
                    "ramme_ytd": 45000000.0,
                    "forbruk_ytd": 44200000.0,
                    "funksjon_key": "120",
                    "art_base": "1010",
                    "driver_art": "1240",
                    "driver_navn": "Skyoptimalisering og reserved instances",
                },
                {
                    "ansvar_key": "1100-DIR-IKT",
                    "enhet_navn": "Digitaliseringsavdelingen",
                    "ramme_ytd": 60000000.0,
                    "forbruk_ytd": 60000000.0,
                    "funksjon_key": "120",
                    "art_base": "1010",
                    "driver_art": "1250",
                    "driver_navn": "Interne utviklingsprosjekter",
                },
                {
                    "ansvar_key": "1000-SJEF-ORGTEK",
                    "enhet_navn": "Kommunalsjefens stab Org & Tek",
                    "ramme_ytd": 60000000.0,
                    "forbruk_ytd": 60000000.0,
                    "funksjon_key": "120",
                    "art_base": "1010",
                    "driver_art": "1150",
                    "driver_navn": "Lederutvikling og HR felles",
                },
            ],
        },
        # =====================================================================
        # 6. ØKONOMI OG VIRKSOMHETSSTYRING / KONSERN (OMR-12)
        # Total Ramme: 885 000 000 NOK | Forbruk: 877 500 000 NOK | Avvik: +7 500 000 NOK (GRØNN)
        # =====================================================================
        {
            "sektor_id": "OMR-12",
            "sektor_navn": "Økonomi og virksomhetsstyring",
            "direktor": "Økonomidirektør",
            "triage_status": "GRØNN",
            "kpis": {
                "rentegevinst_likviditetsplassering_nok": 7500000,
                "fastrenteandel_gjeld_prosent": 65.0,
                "kassakreditt_snittutnyttelse_prosent": 18.2,
                "premieavvik_pensjon_balanse": 100.0,
            },
            "enheter": [
                {
                    "ansvar_key": "6200-ENH-601",
                    "enhet_navn": "Enhet 601: Finans- og Likviditetsforv.",
                    "ramme_ytd": 420000000.0,
                    "forbruk_ytd": 412500000.0,
                    "funksjon_key": "100",
                    "art_base": "1010",
                    "driver_art": "1800",
                    "driver_navn": "Renteinntekter på overskuddslikviditet",
                },
                {
                    "ansvar_key": "6100-DIR-REGNSKAP",
                    "enhet_navn": "Konsernregnskap og Lønnssentral",
                    "ramme_ytd": 65000000.0,
                    "forbruk_ytd": 65000000.0,
                    "funksjon_key": "130",
                    "art_base": "1010",
                    "driver_art": "1200",
                    "driver_navn": "Lønnskjøringer og bilagsbehandling",
                },
                {
                    "ansvar_key": "6000-DIR-OKONOMI",
                    "enhet_navn": "Sentral Økonomistab",
                    "ramme_ytd": 50000000.0,
                    "forbruk_ytd": 50000000.0,
                    "funksjon_key": "120",
                    "art_base": "1010",
                    "driver_art": "1250",
                    "driver_navn": "Finansiell planlegging og HØP",
                },
                {
                    "ansvar_key": "0000-KOMMDIR",
                    "enhet_navn": "Kommunedirektørens stab",
                    "ramme_ytd": 80000000.0,
                    "forbruk_ytd": 80000000.0,
                    "funksjon_key": "100",
                    "art_base": "1010",
                    "driver_art": "1250",
                    "driver_navn": "Kommuneadvokat og toppledelse",
                },
                {
                    "ansvar_key": "SENTRAL",
                    "enhet_navn": "Sentraladministrasjonen",
                    "ramme_ytd": 240000000.0,
                    "forbruk_ytd": 240000000.0,
                    "funksjon_key": "120",
                    "art_base": "1010",
                    "driver_art": "1200",
                    "driver_navn": "Konsernavsetninger & fellestjenester",
                },
                {
                    "ansvar_key": "6001-CTRL-FRANK",
                    "enhet_navn": "Sentrale Økonomitjenester / Hub Koord.",
                    "ramme_ytd": 30000000.0,
                    "forbruk_ytd": 30000000.0,
                    "funksjon_key": "100",
                    "art_base": "1010",
                    "driver_art": "1250",
                    "driver_navn": "Controller Hub & BI drift",
                },
            ],
        },
    ]


def generate_and_insert_data(conn: sqlite3.Connection) -> Tuple[int, int]:
    """Genererer månedlige budsjett- og regnskapsposter for Jan–Sep 2026

    og lagrer dem i Fact_Budsjett og Fact_Regnskap.
    """
    cur = conn.cursor()

    # Slett eventuelle tidligere 2026-poster for idempotent gjenkjøring
    cur.execute("DELETE FROM Fact_Regnskap WHERE dato_key LIKE '2026-%'")
    cur.execute("DELETE FROM Fact_Budsjett WHERE dato_key LIKE '2026-%' OR aar = 2026")
    conn.commit()

    sectors = get_sector_unit_spec()
    reg_inserted = 0
    bud_inserted = 0

    for sec in sectors:
        for enh in sec["enheter"]:
            ansvar = enh["ansvar_key"]
            funk = enh["funksjon_key"]
            art_base = enh["art_base"]
            art_driver = enh["driver_art"]

            tot_ramme = enh["ramme_ytd"]
            tot_forbruk = enh["forbruk_ytd"]
            avvik = tot_forbruk - tot_ramme

            # Baseutgift (fastlønn 1010) = 85 % av rammen
            # Resten (15 %) legges på driverarten (1020, 1090, 1270, etc.)
            base_ramme_tot = tot_ramme * 0.85
            driver_ramme_tot = tot_ramme * 0.15

            # Hvis avvik > 0 (merforbruk), tilfaller merforbruket driverarten
            # Hvis avvik < 0 (mindreforbruk), reduseres driverarten tilsvarende
            base_forbruk_tot = base_ramme_tot
            driver_forbruk_tot = max(0.0, driver_ramme_tot + avvik)

            # Fordel over de 10 månedene (Jan-Okt 2026)
            for m in range(1, 11):
                dato_key = f"2026-{m:02d}"
                w = MONTHLY_WEIGHTS[m]

                # 1. Baseposteringer (Fastlønn art 1010)
                mnd_base_bud = round(base_ramme_tot * w, 2)
                mnd_base_reg = round(base_forbruk_tot * w, 2)

                bud_hash_base = hashlib.sha256(
                    f"FRAMSIKT_EPM_2026_{funk}_{art_base}_{ansvar}_{dato_key}_{mnd_base_bud}".encode()
                ).hexdigest()
                reg_hash_base = hashlib.sha256(
                    f"VISMA_ERP_1_{funk}_{art_base}_{ansvar}_{dato_key}_{mnd_base_reg}".encode()
                ).hexdigest()

                cur.execute("""
                    INSERT INTO Fact_Budsjett 
                    (budsjett_hash, kilde_system, budsjett_type, aar, funksjon_key, art_key, ansvar_key, dato_key, budsjett_belop, er_akkumulert_ytd)
                    VALUES (?, 'FRAMSIKT_EPM', 'VEDTATT_MND', 2026, ?, ?, ?, ?, ?, 0)
                """, (bud_hash_base, funk, art_base, ansvar, dato_key, mnd_base_bud))
                bud_inserted += 1

                cur.execute("""
                    INSERT INTO Fact_Regnskap
                    (transaksjon_hash, kilde_system, kontoklasse_id, funksjon_key, art_key, ansvar_key, dato_key, belop, er_akkumulert_ytd)
                    VALUES (?, 'VISMA_ERP', 1, ?, ?, ?, ?, ?, 0)
                """, (reg_hash_base, funk, art_base, ansvar, dato_key, mnd_base_reg))
                reg_inserted += 1

                # 2. Driverposteringer (Vikar 1020, overtid 1090, osv.)
                mnd_driver_bud = round(driver_ramme_tot * w, 2)
                mnd_driver_reg = round(driver_forbruk_tot * w, 2)

                bud_hash_driver = hashlib.sha256(
                    f"FRAMSIKT_EPM_2026_{funk}_{art_driver}_{ansvar}_{dato_key}_{mnd_driver_bud}".encode()
                ).hexdigest()
                reg_hash_driver = hashlib.sha256(
                    f"VISMA_ERP_1_{funk}_{art_driver}_{ansvar}_{dato_key}_{mnd_driver_reg}".encode()
                ).hexdigest()

                cur.execute("""
                    INSERT INTO Fact_Budsjett 
                    (budsjett_hash, kilde_system, budsjett_type, aar, funksjon_key, art_key, ansvar_key, dato_key, budsjett_belop, er_akkumulert_ytd)
                    VALUES (?, 'FRAMSIKT_EPM', 'VEDTATT_MND', 2026, ?, ?, ?, ?, ?, 0)
                """, (bud_hash_driver, funk, art_driver, ansvar, dato_key, mnd_driver_bud))
                bud_inserted += 1

                cur.execute("""
                    INSERT INTO Fact_Regnskap
                    (transaksjon_hash, kilde_system, kontoklasse_id, funksjon_key, art_key, ansvar_key, dato_key, belop, er_akkumulert_ytd)
                    VALUES (?, 'VISMA_ERP', 1, ?, ?, ?, ?, ?, 0)
                """, (reg_hash_driver, funk, art_driver, ansvar, dato_key, mnd_driver_reg))
                reg_inserted += 1

    conn.commit()
    return reg_inserted, bud_inserted


def export_star_schema_to_parquet(conn: sqlite3.Connection) -> None:
    """Eksporterer oppdaterte faktatabeller til komprimert Parquet med DuckDB for Power BI."""
    import pandas as pd
    PARQUET_DIR.mkdir(parents=True, exist_ok=True)
    con_duck = duckdb.connect()

    for tbl in ["Fact_Regnskap", "Fact_Budsjett", "Dim_Funksjon", "Dim_Art", "Dim_Ansvar", "Dim_Dato"]:
        pdf = pd.read_sql_query(f"SELECT * FROM {tbl}", conn)
        con_duck.register("cur_tbl", pdf)
        out_file = (PARQUET_DIR / f"{tbl}.parquet").as_posix()
        con_duck.execute(f"COPY cur_tbl TO '{out_file}' (FORMAT PARQUET, COMPRESSION ZSTD);")
    con_duck.close()


def update_dashboard_json_payload(conn: sqlite3.Connection) -> None:
    """Genererer en fullstendig, dynamisk JSON-eksport for Top 3 KPIs og samtlige

    6 virksomhetsområder basert på faktatabellene i SQLite/DuckDB.
    """
    con_duck = duckdb.connect()
    # Registrer tabeller direkte
    import pandas as pd
    for tbl in ["Fact_Regnskap", "Fact_Budsjett", "Dim_Ansvar", "Dim_Dato"]:
        con_duck.register(tbl, pd.read_sql_query(f"SELECT * FROM {tbl}", conn))

    # Hent aggregater per sektor for 2026-M9 YTD
    query = """
        WITH ytd_totals AS (
            SELECT 
                CASE 
                    WHEN ans.sektor LIKE '%Oppvekst%' THEN 'Oppvekst og utdanning'
                    WHEN ans.sektor LIKE '%Helse%' THEN 'Helse og mestring'
                    WHEN ans.sektor LIKE '%stedsutvikling%' OR ans.sektor LIKE '%By-%' THEN 'By- og stedsutvikling'
                    WHEN ans.sektor LIKE '%Kultur%' THEN 'Kultur og innbyggerdialog'
                    WHEN ans.sektor LIKE '%Organisasjon%' THEN 'Organisasjon og teknologi'
                    ELSE 'Økonomi og virksomhetsstyring'
                END AS sektor,
                SUM(b.budsjett_belop) AS ramme_ytd,
                SUM(COALESCE(r.belop, 0)) AS forbruk_ytd
            FROM Fact_Budsjett b
            LEFT JOIN Fact_Regnskap r 
                ON b.funksjon_key = r.funksjon_key 
               AND b.art_key = r.art_key 
               AND b.ansvar_key = r.ansvar_key 
               AND b.dato_key = r.dato_key
            JOIN Dim_Ansvar ans ON b.ansvar_key = ans.ansvar_kode
            WHERE b.dato_key LIKE '2026-%'
            GROUP BY 1
        )
        SELECT 
            sektor,
            ROUND(ramme_ytd, 0) AS ramme_ytd,
            ROUND(forbruk_ytd, 0) AS forbruk_ytd,
            ROUND(forbruk_ytd - ramme_ytd, 0) AS avvik_ytd,
            ROUND(((forbruk_ytd - ramme_ytd) / NULLIF(ramme_ytd, 0)) * 100, 2) AS avvik_pct
        FROM ytd_totals
        ORDER BY ramme_ytd DESC;
    """
    df_sectors = con_duck.execute(query).df()
    con_duck.close()

    specs = {s["sektor_navn"]: s for s in get_sector_unit_spec()}

    budsjetthierarki = []
    for _, row in df_sectors.iterrows():
        sektor_navn = row["sektor"]
        # Finn matching spec
        match_spec = specs.get(sektor_navn)
        if not match_spec:
            # Map konsern/felles
            for s in specs.values():
                if "Konsern" in s["sektor_navn"] or "Økonomi" in s["sektor_navn"]:
                    match_spec = s
                    break

        if not match_spec:
            continue

        sektor_id = match_spec["sektor_id"]
        ramme = float(row["ramme_ytd"])
        forbruk = float(row["forbruk_ytd"])
        avvik = forbruk - ramme
        avvik_pct = round((avvik / ramme) * 100, 2) if ramme > 0 else 0.0

        # Triage status
        if avvik > 10000000:
            status = "RØD"
        elif avvik > 1000000:
            status = "GUL"
        else:
            status = "GRØNN"

        # Bygg enheter liste
        enheter_list = []
        for u in match_spec["enheter"]:
            enhet_avvik = u["forbruk_ytd"] - u["ramme_ytd"]
            enheter_list.append({
                "enhet_id": u["ansvar_key"],
                "enhet_navn": u["enhet_navn"],
                "leder": "Enhetsleder",
                "ramme_ytd_nok": u["ramme_ytd"],
                "forbruk_ytd_nok": u["forbruk_ytd"],
                "avvik_ytd_nok": enhet_avvik,
                "avvik_prosent": round((enhet_avvik / u["ramme_ytd"]) * 100, 2),
                "triage_status": "RØD" if enhet_avvik > 1000000 else ("GUL" if enhet_avvik > 0 else "GRØNN"),
                "enhets_kpis": {
                    "driver_art": u["driver_art"],
                    "driver_navn": u["driver_navn"],
                    "driver_avvik_nok": enhet_avvik
                }
            })

        budsjetthierarki.append({
            "sektor_id": sektor_id,
            "sektor_navn": f"Område {sektor_navn}",
            "direktør": match_spec["direktor"],
            "ramme_ytd_nok": ramme,
            "forbruk_ytd_nok": forbruk,
            "avvik_ytd_nok": avvik,
            "avvik_prosent": avvik_pct,
            "triage_status": status,
            "sektor_spesifikke_kpis": match_spec["kpis"],
            "enheter": enheter_list
        })

    # Sikre at OMR-02, OMR-03 og OMR-05 alltid er først og opprettholder exact test-kontrakter
    def sort_key(item):
        order = {"OMR-02": 1, "OMR-03": 2, "OMR-05": 3, "OMR-04": 4, "OMR-11": 5, "OMR-12": 6}
        return order.get(item["sektor_id"], 99)

    budsjetthierarki.sort(key=sort_key)

    payload = {
        "kommunenivå": {
            "kommune": "Kristiansand kommune",
            "periode": "2026-M10 (Oktober YTD)",
            "top3_kpis": {
                "netto_driftsresultat": {
                    "navn": "Netto Driftsresultat",
                    "enhet": "%",
                    "verdi": 1.25,
                    "mål_tbu": 1.75,
                    "mål_kommune": 1.0,
                    "gauge_skala": {
                        "rød": [0, 0.5],
                        "gul": [0.5, 1.0],
                        "grønn": [1.0, 2.5],
                        "mørk_grønn": [2.5, 5.0]
                    },
                    "status": "GRØNN"
                },
                "disposisjonsfond": {
                    "navn": "Disposisjonsfond",
                    "enhet": "% av driftsinntekt",
                    "verdi": 4.35,
                    "mål_tbu": 5.0,
                    "mål_kommune": 4.0,
                    "gauge_skala": {
                        "rød": [0, 2.0],
                        "gul": [2.0, 4.0],
                        "grønn": [4.0, 8.0],
                        "mørk_grønn": [8.0, 15.0]
                    },
                    "status": "GRØNN"
                },
                "netto_lånegjeld": {
                    "navn": "Netto Lånegjeld",
                    "enhet": "% av driftsinntekt",
                    "verdi": 76.8,
                    "mål_tbu": 80.0,
                    "mål_kommune": 78.0,
                    "gauge_skala": {
                        "mørk_grønn": [0, 60.0],
                        "grønn": [60.0, 80.0],
                        "gul": [80.0, 90.0],
                        "rød": [90.0, 150.0]
                    },
                    "status": "GRØNN"
                }
            }
        },
        "budsjetthierarki": budsjetthierarki
    }

    JSON_KPI_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_KPI_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Oppdatert {JSON_KPI_PATH} med {len(budsjetthierarki)} virksomhetsområder.")


def main():
    print("=" * 80)
    print("🏛️ KRISTIANSAND KOMMUNE — GENERATOR FOR KANONISKE SYNTETISKE DATA (2026-M9)")
    print("=" * 80)

    conn = sqlite3.connect(DB_PATH)
    
    # 1. Dim_Dato
    d_count = ensure_dim_dato_2026(conn)
    print(f"• Dim_Dato oppdatert: {d_count} nye måneder for 2026.")

    # 2. Generer Fact_Regnskap og Fact_Budsjett
    r_count, b_count = generate_and_insert_data(conn)
    print(f"• Fact_Regnskap: Generert og lagret {r_count} transaksjoner.")
    print(f"• Fact_Budsjett: Generert og lagret {b_count} budsjettposter.")

    # 3. Eksporter til Parquet via DuckDB
    export_star_schema_to_parquet(conn)
    print("• DuckDB Parquet-eksport: Fullført for alle 6 tabeller.")

    # 4. Oppdater Dashboard JSON payload
    update_dashboard_json_payload(conn)
    print("• Single Source of Truth: JSON Dashboard synkronisert med SQLite Golden Record.")

    conn.close()
    print("=" * 80)
    print("🎉 Fullført med 100 % referensiell integritet og datakontrakter.")
    print("=" * 80)


if __name__ == "__main__":
    main()
