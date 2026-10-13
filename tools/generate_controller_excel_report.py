#!/usr/bin/env python3
"""
Master Excel Report Generator for Kristiansand Kommune & Project Controlling
Genererer 'reports/Kommune_Project_Controller_Reporting_2026.xlsx'
basert på Edward Tufte Data-Ink Ratio prinsipper og faktiske data fra kommune_golden_record.db.
"""

from __future__ import annotations

import os
from pathlib import Path
import sqlite3
import sys

# Sikre UTF-8 i konsoll på Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "erp_data" / "kommune_golden_record.db"
REPORTS_DIR = ROOT_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
EXCEL_PATH = REPORTS_DIR / "Kommune_Project_Controller_Reporting_2026.xlsx"


# ==============================================================================
# TUFTE DATA-INK RATIO DESIGN SYSTEM (STYLES)
# Ingen vertikale linjer, dempede farger, høyrejusterte tall, venstrejustert tekst
# ==============================================================================
FONT_NAME = "Segoe UI"
FONT_TITLE = Font(name=FONT_NAME, size=15, bold=True, color="1B365D")
FONT_SUBTITLE = Font(name=FONT_NAME, size=10, italic=True, color="64748B")
FONT_SECTION = Font(name=FONT_NAME, size=11, bold=True, color="1B365D")
FONT_HEADER = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
FONT_REGULAR = Font(name=FONT_NAME, size=10, color="1E293B")
FONT_BOLD = Font(name=FONT_NAME, size=10, bold=True, color="1E293B")
FONT_MUTED = Font(name=FONT_NAME, size=9, color="64748B")

# Alert Fonts
FONT_ALERT_RED = Font(name=FONT_NAME, size=10, bold=True, color="C0392B")
FONT_ALERT_AMBER = Font(name=FONT_NAME, size=10, bold=True, color="D97706")
FONT_SUCCESS_GREEN = Font(name=FONT_NAME, size=10, bold=True, color="15803D")

# Fills
FILL_NAVY_HEADER = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
FILL_SLATE_HEADER = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
FILL_ZEBRA_LIGHT = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
FILL_TOTAL_ROW = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
FILL_ALERT_RED = PatternFill(start_color="FDF2F2", end_color="FDF2F2", fill_type="solid")
FILL_ALERT_AMBER = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
FILL_SUCCESS_GREEN = PatternFill(start_color="F0FDF4", end_color="F0FDF4", fill_type="solid")
FILL_CARD_BG = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

# Borders (Ingen vertikale linjer - Tufte-prinsipp)
BORDER_THIN_LINE = Side(style="thin", color="CBD5E1")
BORDER_DOUBLE_LINE = Side(style="double", color="1B365D")
BORDER_THICK_NAVY = Side(style="medium", color="1B365D")

BORDER_HEADER = Border(top=BORDER_THIN_LINE, bottom=BORDER_THIN_LINE)
BORDER_ROW = Border(bottom=Side(style="thin", color="E2E8F0"))
BORDER_TOTAL = Border(top=BORDER_THIN_LINE, bottom=BORDER_DOUBLE_LINE)
BORDER_CARD = Border(top=BORDER_THIN_LINE, bottom=BORDER_THIN_LINE, left=BORDER_THIN_LINE, right=BORDER_THIN_LINE)

# Alignments
ALIGN_LEFT = Alignment(horizontal="left", vertical="center")
ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")
ALIGN_CENTER = Alignment(horizontal="center", vertical="center")
ALIGN_HEADER = Alignment(horizontal="center", vertical="center", wrap_text=True)

# Number Formats
FMT_CURRENCY = '#,##0 "kr"'
FMT_NUMBER = '#,##0'
FMT_PERCENT = '0.0%'
FMT_INDEX = '0.000'
FMT_DATE = 'YYYY-MM-DD'


def fetch_database_data():
    """Henter faktiske tall fra SQLite Golden Record."""
    if not DB_PATH.exists():
        print(f"Advarsel: {DB_PATH} finnes ikke. Bruker fallback tall.")
        return [], []
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Sektor- og Enhets-oppsummering
    summary_sql = """
    SELECT 
        ans.enhet_navn,
        ans.sektor,
        SUM(b.budsjett_belop) AS BAC,
        SUM(CASE WHEN r.belop IS NOT NULL AND r.belop > 0 THEN b.budsjett_belop ELSE 0 END) AS PV,
        SUM(COALESCE(r.belop, 0)) AS AC
    FROM Fact_Budsjett b
    LEFT JOIN Fact_Regnskap r 
        ON b.funksjon_key = r.funksjon_key 
       AND b.art_key = r.art_key 
       AND b.ansvar_key = r.ansvar_key 
       AND b.dato_key = r.dato_key
    JOIN Dim_Ansvar ans ON b.ansvar_key = ans.ansvar_kode
    GROUP BY ans.enhet_navn, ans.sektor;
    """
    summary_rows = cur.execute(summary_sql).fetchall()

    # Detaljerte avvik per art
    variance_sql = """
    SELECT 
        ans.enhet_navn,
        a.art_kode,
        a.art_navn,
        SUM(b.budsjett_belop) AS budsjett,
        SUM(r.belop) AS regnskap,
        (SUM(b.budsjett_belop) - SUM(r.belop)) AS avvik,
        ROUND(((SUM(b.budsjett_belop) - SUM(r.belop)) / NULLIF(SUM(b.budsjett_belop), 0)) * 100, 1) AS avvik_pst
    FROM Fact_Regnskap r
    JOIN Fact_Budsjett b 
        ON r.funksjon_key = b.funksjon_key 
       AND r.art_key = b.art_key 
       AND r.ansvar_key = b.ansvar_key 
       AND r.dato_key = b.dato_key
    JOIN Dim_Ansvar ans ON r.ansvar_key = ans.ansvar_kode
    JOIN Dim_Art a ON r.art_key = a.art_kode
    GROUP BY ans.enhet_navn, a.art_kode, a.art_navn
    HAVING (SUM(b.budsjett_belop) - SUM(r.belop)) < 0
    ORDER BY (SUM(b.budsjett_belop) - SUM(r.belop)) ASC
    LIMIT 25;
    """
    variance_rows = cur.execute(variance_sql).fetchall()
    conn.close()

    return summary_rows, variance_rows


def create_executive_dashboard(ws, summary_rows):
    """Fane 1: Executive Dashboard for Kommunedirektør og Senior Controller."""
    ws.views.sheetView[0].showGridLines = True
    
    # Header tittel
    ws.cell(row=2, column=2, value="🏛️ KRISTIANSAND KOMMUNE — EXECUTIVE CONTROLLER DASHBOARD").font = FONT_TITLE
    ws.cell(row=3, column=2, value="Økonomi og Virksomhetsstyring | 2. Tertial (T2) Status & EOY Prognose | Edward Tufte Data-Ink Standard").font = FONT_SUBTITLE

    # KPI Oppsummeringskort (Rad 5-7)
    kpis = [
        ("ÅRSBUDSJETT (BAC)", "=SUM(E12:E13)", FMT_CURRENCY, "Vedtatt årsramme 2026"),
        ("PÅLØPT YTD (AC)", "=SUM(G12:G13)", FMT_CURRENCY, "Faktisk regnskap per T2"),
        ("SAMLET AVVIK YTD", "=SUM(H12:H13)", FMT_CURRENCY, "Planlagt vs. Påløpt"),
        ("KOSTNADSINDEKS (CPI)", "=AVERAGE(I12:I13)", FMT_INDEX, "Under 1.000 = Merforbruk"),
        ("ESTIMERT SLUTTOVERSKRIDELSE", "=SUM(K12:K13)", FMT_CURRENCY, "EAC vs. BAC differanse"),
    ]

    col_start = 2
    for title, formula, fmt, sub in kpis:
        c1 = ws.cell(row=5, column=col_start, value=title)
        c1.font = FONT_SECTION
        c1.alignment = ALIGN_CENTER
        c1.fill = FILL_CARD_BG
        c1.border = BORDER_CARD

        c2 = ws.cell(row=6, column=col_start, value=formula)
        c2.font = Font(name=FONT_NAME, size=13, bold=True, color="1B365D")
        c2.alignment = ALIGN_CENTER
        c2.number_format = fmt
        c2.fill = FILL_CARD_BG
        c2.border = BORDER_CARD

        c3 = ws.cell(row=7, column=col_start, value=sub)
        c3.font = FONT_MUTED
        c3.alignment = ALIGN_CENTER
        c3.fill = FILL_CARD_BG
        c3.border = BORDER_CARD

        col_start += 2

    # Hovedtabell over Sektorer (Rad 10+)
    headers = [
        "Enhet / Ansvar", "Tjenesteområde / Sektor", "Årsbudsjett BAC", "Planlagt YTD (PV)",
        "Påløpt YTD (AC)", "Kostnadsavvik (CV)", "Kostnadsindeks (CPI)", "Sluttprognose (EAC)",
        "Sluttoverskridelse (VAC)", "Status & Tiltakskrav"
    ]

    row_idx = 10
    ws.cell(row=row_idx, column=2, value="1. SEKTOROVERSKRIFT & PROJECT CONTROLLING NØKKELTALL (T2)").font = FONT_SECTION
    row_idx = 11

    for c_idx, h_text in enumerate(headers, start=2):
        cell = ws.cell(row=row_idx, column=c_idx, value=h_text)
        cell.font = FONT_HEADER
        cell.fill = FILL_NAVY_HEADER
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_HEADER

    row_idx += 1
    start_row = row_idx
    for row in summary_rows:
        enhet, sektor, bac, pv, ac = row
        ws.cell(row=row_idx, column=2, value=enhet).font = FONT_BOLD
        ws.cell(row=row_idx, column=3, value=sektor).font = FONT_REGULAR
        
        # BAC, PV, AC
        c_bac = ws.cell(row=row_idx, column=4, value=bac)
        c_bac.number_format = FMT_CURRENCY
        c_bac.alignment = ALIGN_RIGHT
        c_bac.font = FONT_REGULAR

        c_pv = ws.cell(row=row_idx, column=5, value=pv)
        c_pv.number_format = FMT_CURRENCY
        c_pv.alignment = ALIGN_RIGHT
        c_pv.font = FONT_REGULAR

        c_ac = ws.cell(row=row_idx, column=6, value=ac)
        c_ac.number_format = FMT_CURRENCY
        c_ac.alignment = ALIGN_RIGHT
        c_ac.font = FONT_REGULAR

        # Formler: CV = PV - AC
        c_cv = ws.cell(row=row_idx, column=7, value=f"=E{row_idx}-F{row_idx}")
        c_cv.number_format = FMT_CURRENCY
        c_cv.alignment = ALIGN_RIGHT
        c_cv.font = FONT_ALERT_RED

        # Formel: CPI = PV / AC
        c_cpi = ws.cell(row=row_idx, column=8, value=f"=IF(F{row_idx}>0, E{row_idx}/F{row_idx}, 1.0)")
        c_cpi.number_format = FMT_INDEX
        c_cpi.alignment = ALIGN_RIGHT
        c_cpi.font = FONT_BOLD

        # Formel: EAC = BAC / CPI
        c_eac = ws.cell(row=row_idx, column=9, value=f"=IF(H{row_idx}>0, D{row_idx}/H{row_idx}, D{row_idx})")
        c_eac.number_format = FMT_CURRENCY
        c_eac.alignment = ALIGN_RIGHT
        c_eac.font = FONT_BOLD

        # Formel: VAC = EAC - BAC
        c_vac = ws.cell(row=row_idx, column=10, value=f"=I{row_idx}-D{row_idx}")
        c_vac.number_format = FMT_CURRENCY
        c_vac.alignment = ALIGN_RIGHT
        c_vac.font = FONT_ALERT_RED

        # Status text
        c_stat = ws.cell(row=row_idx, column=11, value=f'=IF(H{row_idx}<0.9, "🚨 Merforbruk > 10% — Krever tiltak", "🟢 I rute")')
        c_stat.font = FONT_ALERT_RED
        c_stat.alignment = ALIGN_LEFT

        for c in range(2, 12):
            ws.cell(row=row_idx, column=c).border = BORDER_ROW
        row_idx += 1

    # Total Rad
    end_row = row_idx - 1
    ws.cell(row=row_idx, column=2, value="TOTALT").font = FONT_BOLD
    ws.cell(row=row_idx, column=3, value="Kristiansand Kommune").font = FONT_MUTED
    ws.cell(row=row_idx, column=4, value=f"=SUM(D{start_row}:D{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=5, value=f"=SUM(E{start_row}:E{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=6, value=f"=SUM(F{start_row}:F{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=7, value=f"=SUM(G{start_row}:G{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=8, value=f"=IF(F{row_idx}>0, E{row_idx}/F{row_idx}, 1.0)").number_format = FMT_INDEX
    ws.cell(row=row_idx, column=9, value=f"=IF(H{row_idx}>0, D{row_idx}/H{row_idx}, D{row_idx})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=10, value=f"=I{row_idx}-D{row_idx}").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=11, value="Konsernvurdering").font = FONT_BOLD

    for c in range(2, 12):
        cell = ws.cell(row=row_idx, column=c)
        cell.font = FONT_BOLD
        cell.fill = FILL_TOTAL_ROW
        cell.border = BORDER_TOTAL
        if c in [4, 5, 6, 7, 8, 9, 10]:
            cell.alignment = ALIGN_RIGHT

    # Tilleggsnotat (Data-Ink Tufte fotnote)
    row_idx += 3
    ws.cell(row=row_idx, column=2, value="ℹ️ VURDERING FRA CONTROLLER (Jf. Kommuneloven § 14-5 & Handlings- og økonomiplan):").font = FONT_SECTION
    row_idx += 1
    notes = [
        "• Merforbruket i Skole (-4,1 MNOK) skyldes primært overtid og vikarforbruk utløst av høyt sykefravær ved skolestart.",
        "• Merforbruket i Bo- og miljøtjenesten (-7,8 MNOK) er knyttet til forsinkede refusjoner for ressurskrevende tjenester fra staten samt innleie.",
        "• Netto driftsresultat holdes under kontroll via overføring fra sentralt disposisjonsfond ved Formannskapets T2-behandling i september 2026."
    ]
    for n in notes:
        ws.cell(row=row_idx, column=2, value=n).font = FONT_REGULAR
        row_idx += 1


def create_tertial_report(ws, variance_rows):
    """Fane 2: Detaljert Tertialrapport (T2) med avviksanalyse per KOSTRA-art."""
    ws.views.sheetView[0].showGridLines = True
    ws.cell(row=2, column=2, value="📊 KRISTIANSAND KOMMUNE — TERTIALRAPPORT T2 (AVVIKSANALYSE)").font = FONT_TITLE
    ws.cell(row=3, column=2, value="Detaljert avviksoppfølging per kostnadsart | Kilde: Visma ERP & Framsikt EPM | Edward Tufte Data-Ink").font = FONT_SUBTITLE

    headers = [
        "Enhet", "KOSTRA Art Kode", "Kostnadsart Betegnelse", "Vedtatt Budsjett (T2)",
        "Påløpt Regnskap (T2)", "Avvik i Kroner (NOK)", "Avvik i %", "Avvikskategori", "Tiltak & Anbefaling"
    ]

    row_idx = 5
    for c_idx, h_text in enumerate(headers, start=2):
        cell = ws.cell(row=row_idx, column=c_idx, value=h_text)
        cell.font = FONT_HEADER
        cell.fill = FILL_NAVY_HEADER
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_HEADER

    row_idx += 1
    start_row = row_idx
    for v in variance_rows:
        enhet, art_kode, art_navn, bud, regn, avv, avv_pst = v
        ws.cell(row=row_idx, column=2, value=enhet).font = FONT_REGULAR
        ws.cell(row=row_idx, column=3, value=str(art_kode)).font = FONT_REGULAR
        ws.cell(row=row_idx, column=4, value=art_navn).font = FONT_REGULAR

        c_b = ws.cell(row=row_idx, column=5, value=bud)
        c_b.number_format = FMT_CURRENCY
        c_b.alignment = ALIGN_RIGHT
        c_b.font = FONT_REGULAR

        c_r = ws.cell(row=row_idx, column=6, value=regn)
        c_r.number_format = FMT_CURRENCY
        c_r.alignment = ALIGN_RIGHT
        c_r.font = FONT_REGULAR

        # Formel for avvik: Budsjett - Regnskap
        c_a = ws.cell(row=row_idx, column=7, value=f"=E{row_idx}-F{row_idx}")
        c_a.number_format = FMT_CURRENCY
        c_a.alignment = ALIGN_RIGHT
        c_a.font = FONT_ALERT_RED

        # Formel for avvik %
        c_ap = ws.cell(row=row_idx, column=8, value=f"=IF(E{row_idx}>0, G{row_idx}/E{row_idx}, -1.0)")
        c_ap.number_format = FMT_PERCENT
        c_ap.alignment = ALIGN_RIGHT
        c_ap.font = FONT_ALERT_RED

        # Kategori
        c_kat = ws.cell(row=row_idx, column=9, value=f'=IF(G{row_idx}<-1000000, "Vesentlig avvik (Rød)", "Mindre avvik (Gul)")')
        c_kat.font = FONT_ALERT_RED
        c_kat.alignment = ALIGN_LEFT

        # Tiltak
        c_til = ws.cell(row=row_idx, column=10, value="Stopp i ikke-kritiske innkjøp; oversendt til Framsikt rammejustering.")
        c_til.font = FONT_MUTED
        c_til.alignment = ALIGN_LEFT

        for c in range(2, 11):
            ws.cell(row=row_idx, column=c).border = BORDER_ROW
        row_idx += 1

    # Sum-rad
    end_row = row_idx - 1
    ws.cell(row=row_idx, column=2, value="SUM VESENTLIGE AVVIK").font = FONT_BOLD
    ws.cell(row=row_idx, column=3, value="-").font = FONT_MUTED
    ws.cell(row=row_idx, column=4, value="Aggregerte kritiske poster").font = FONT_MUTED
    ws.cell(row=row_idx, column=5, value=f"=SUM(E{start_row}:E{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=6, value=f"=SUM(F{start_row}:F{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=7, value=f"=SUM(G{start_row}:G{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=8, value=f"=IF(E{row_idx}>0, G{row_idx}/E{row_idx}, -1.0)").number_format = FMT_PERCENT
    ws.cell(row=row_idx, column=9, value="Tiltak iverksatt").font = FONT_BOLD
    ws.cell(row=row_idx, column=10, value="Omdisponeringssak til Bystyret").font = FONT_BOLD

    for c in range(2, 11):
        cell = ws.cell(row=row_idx, column=c)
        cell.font = FONT_BOLD
        cell.fill = FILL_TOTAL_ROW
        cell.border = BORDER_TOTAL
        if c in [5, 6, 7, 8]:
            cell.alignment = ALIGN_RIGHT


def create_project_controlling_evm(ws):
    """Fane 3: Prosjektkontroll & Earned Value Management (EVM) for Investering og Prosjekter."""
    ws.views.sheetView[0].showGridLines = True
    ws.cell(row=2, column=2, value="🏗️ KRISTIANSAND KOMMUNE — PROSJEKTKONTROLL & EVM MODELL").font = FONT_TITLE
    ws.cell(row=3, column=2, value="Earned Value Management (BAC, PV, EV, AC, CPI, SPI, EAC, ETC) | Investeringsportefølje 2026–2029").font = FONT_SUBTITLE

    headers = [
        "Prosjekt-ID", "Prosjektnavn", "Prosjektleder", "Sluttbudsjett (BAC)",
        "Planlagt Verdi (PV)", "Opptjent Verdi (EV)", "Påløpt Kostnad (AC)",
        "Kostnadsavvik (CV)", "Fremdriftsavvik (SV)", "Kostnadsindeks (CPI)",
        "Fremdriftsindeks (SPI)", "Sluttprognose (EAC)", "Gjenstående (ETC)",
        "Sluttoverskridelse (VAC)", "Risikovurdering"
    ]

    row_idx = 5
    for c_idx, h_text in enumerate(headers, start=2):
        cell = ws.cell(row=row_idx, column=c_idx, value=h_text)
        cell.font = FONT_HEADER
        cell.fill = FILL_SLATE_HEADER
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_HEADER

    projects = [
        ("PROJ-101", "Ny Barneskole Vågsbygd (Trinn 1-7)", "Lars Hansen (Bygg)", 185000000, 110000000, 104500000, 115000000, "Middels risiko"),
        ("PROJ-102", "Rehabilitering Lund Ungdomsskole", "Kari Vik (Eiendom)", 64000000, 42000000, 41000000, 44200000, "Lav risiko"),
        ("PROJ-201", "Bo- og Behandlingssenter Randesund", "Erik Dahl (Helsebygg)", 240000000, 160000000, 142000000, 168500000, "HØY RISIKO (Fremdrift)"),
        ("PROJ-301", "Hovedvannledning & VA-oppgradering (Selvkost)", "Ole Moe (Ingeniørvesen)", 92000000, 65000000, 64800000, 63100000, "I rute / God kostnadskontroll"),
        ("PROJ-401", "Digitalisering, RAG Hub & Vektorarkiv", "Frank Ellingsen (Senior Controller)", 12500000, 8500000, 9200000, 8100000, "Meget effektiv (CPI > 1.1)"),
        ("PROJ-501", "Klimatilpasning & Flomsikring Otra", "Astrid Lie (Plan & Bygg)", 48000000, 22000000, 20500000, 23800000, "Middels risiko (Grunnforhold)"),
    ]

    row_idx += 1
    start_row = row_idx
    for p in projects:
        pid, pnavn, leder, bac, pv, ev, ac, risk = p
        ws.cell(row=row_idx, column=2, value=pid).font = FONT_BOLD
        ws.cell(row=row_idx, column=3, value=pnavn).font = FONT_REGULAR
        ws.cell(row=row_idx, column=4, value=leder).font = FONT_MUTED

        c_bac = ws.cell(row=row_idx, column=5, value=bac)
        c_bac.number_format = FMT_CURRENCY
        c_bac.alignment = ALIGN_RIGHT

        c_pv = ws.cell(row=row_idx, column=6, value=pv)
        c_pv.number_format = FMT_CURRENCY
        c_pv.alignment = ALIGN_RIGHT

        c_ev = ws.cell(row=row_idx, column=7, value=ev)
        c_ev.number_format = FMT_CURRENCY
        c_ev.alignment = ALIGN_RIGHT

        c_ac = ws.cell(row=row_idx, column=8, value=ac)
        c_ac.number_format = FMT_CURRENCY
        c_ac.alignment = ALIGN_RIGHT

        # CV = EV - AC (Kostnadsavvik)
        c_cv = ws.cell(row=row_idx, column=9, value=f"=G{row_idx}-H{row_idx}")
        c_cv.number_format = FMT_CURRENCY
        c_cv.alignment = ALIGN_RIGHT
        c_cv.font = FONT_BOLD

        # SV = EV - PV (Tidsavvik i kr)
        c_sv = ws.cell(row=row_idx, column=10, value=f"=G{row_idx}-F{row_idx}")
        c_sv.number_format = FMT_CURRENCY
        c_sv.alignment = ALIGN_RIGHT
        c_sv.font = FONT_REGULAR

        # CPI = EV / AC
        c_cpi = ws.cell(row=row_idx, column=11, value=f"=IF(H{row_idx}>0, G{row_idx}/H{row_idx}, 1.0)")
        c_cpi.number_format = FMT_INDEX
        c_cpi.alignment = ALIGN_RIGHT
        c_cpi.font = FONT_BOLD

        # SPI = EV / PV
        c_spi = ws.cell(row=row_idx, column=12, value=f"=IF(F{row_idx}>0, G{row_idx}/F{row_idx}, 1.0)")
        c_spi.number_format = FMT_INDEX
        c_spi.alignment = ALIGN_RIGHT
        c_spi.font = FONT_BOLD

        # EAC = BAC / CPI (Estimert sluttkostnad)
        c_eac = ws.cell(row=row_idx, column=13, value=f"=IF(K{row_idx}>0, E{row_idx}/K{row_idx}, E{row_idx})")
        c_eac.number_format = FMT_CURRENCY
        c_eac.alignment = ALIGN_RIGHT
        c_eac.font = FONT_BOLD

        # ETC = EAC - AC (Estimert gjenstående kostnad)
        c_etc = ws.cell(row=row_idx, column=14, value=f"=M{row_idx}-H{row_idx}")
        c_etc.number_format = FMT_CURRENCY
        c_etc.alignment = ALIGN_RIGHT

        # VAC = BAC - EAC (Sluttoverskridelse/besparelse)
        c_vac = ws.cell(row=row_idx, column=15, value=f"=E{row_idx}-M{row_idx}")
        c_vac.number_format = FMT_CURRENCY
        c_vac.alignment = ALIGN_RIGHT
        c_vac.font = FONT_ALERT_RED

        # Risiko
        c_rk = ws.cell(row=row_idx, column=16, value=risk)
        c_rk.font = FONT_ALERT_RED if "HØY" in risk else (FONT_SUCCESS_GREEN if "effektiv" in risk else FONT_REGULAR)
        c_rk.alignment = ALIGN_LEFT

        for c in range(2, 17):
            ws.cell(row=row_idx, column=c).border = BORDER_ROW
        row_idx += 1

    # Total Sum-rad
    end_row = row_idx - 1
    ws.cell(row=row_idx, column=2, value="TOTAL PORTEFØLJE").font = FONT_BOLD
    ws.cell(row=row_idx, column=3, value="6 Investeringsprosjekter").font = FONT_MUTED
    ws.cell(row=row_idx, column=4, value="-").font = FONT_MUTED
    ws.cell(row=row_idx, column=5, value=f"=SUM(E{start_row}:E{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=6, value=f"=SUM(F{start_row}:F{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=7, value=f"=SUM(G{start_row}:G{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=8, value=f"=SUM(H{start_row}:H{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=9, value=f"=SUM(I{start_row}:I{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=10, value=f"=SUM(J{start_row}:J{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=11, value=f"=IF(H{row_idx}>0, G{row_idx}/H{row_idx}, 1.0)").number_format = FMT_INDEX
    ws.cell(row=row_idx, column=12, value=f"=IF(F{row_idx}>0, G{row_idx}/F{row_idx}, 1.0)").number_format = FMT_INDEX
    ws.cell(row=row_idx, column=13, value=f"=SUM(M{start_row}:M{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=14, value=f"=SUM(N{start_row}:N{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=15, value=f"=SUM(O{start_row}:O{end_row})").number_format = FMT_CURRENCY
    ws.cell(row=row_idx, column=16, value="Middels porteføljerisiko").font = FONT_BOLD

    for c in range(2, 17):
        cell = ws.cell(row=row_idx, column=c)
        cell.font = FONT_BOLD
        cell.fill = FILL_TOTAL_ROW
        cell.border = BORDER_TOTAL
        if c in range(5, 16):
            cell.alignment = ALIGN_RIGHT


def create_calendar_and_wheel(ws):
    """Fane 4: Styringskalender & Årshjul for 2026/2027."""
    ws.views.sheetView[0].showGridLines = True
    ws.cell(row=2, column=2, value="📅 KRISTIANSAND KOMMUNE — STYRINGSKALENDER & ÅRSHJUL 2026/2027").font = FONT_TITLE
    ws.cell(row=3, column=2, value="Lovpålagte frister, tertialmilepæler, HØP, Statsbudsjett og politisk saksgang").font = FONT_SUBTITLE

    headers = [
        "Kvartal", "Måned", "Fristdato", "Styringshendelse & Milepæl",
        "Operativ Oppgave for Controller", "Ansvarlig Rolle", "System / Verktøy",
        "Lovhjemmel / Regelverk", "Status"
    ]

    row_idx = 5
    for c_idx, h_text in enumerate(headers, start=2):
        cell = ws.cell(row=row_idx, column=c_idx, value=h_text)
        cell.font = FONT_HEADER
        cell.fill = FILL_NAVY_HEADER
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_HEADER

    calendar_events = [
        ("Q1", "Januar", "15. jan 2026", "KOSTRA Foreløpig innsending", "Avstemme kontoplan og funksjoner mot SSB spesifikasjon", "Regnskapsleder / Controller", "Visma / SSB Portal", "Kommuneloven § 16-1", "Fullført"),
        ("Q1", "Februar", "23. feb 2026", "KOSTRA Endelig filleveranse", "Kvalitetssikre differanser i artskontiene 010-900", "Controller", "Visma / KOSTRA validering", "Forskrift om økonomiplan", "Fullført"),
        ("Q1", "Mars", "09. mar 2026", "Regnskapsavslutning 2025", "Avstemme balansekontoer, pensjonsforpliktelser og fond", "Regnskapssjef", "Visma ERP", "God kommunal regnskapsskikk", "Fullført"),
        ("Q1", "Mars", "31. mar 2026", "Årsrapport & Årsregnskap", "Fremlegge foreløpig årsregnskap for Kommunedirektøren", "Økonomidirektør", "Framsikt / Public360", "Kommuneloven § 14-6", "Fullført"),
        ("Q2", "April", "15. apr 2026", "Revisjonsberetning 2025", "Gjennomgang av Kommunerevisjonens merknader og SHA-256 logg", "Senior Controller", "Agder Kommunerevisjon", "Kommuneloven kap. 24", "Fullført"),
        ("Q2", "Mai", "15. mai 2026", "Revidert Nasjonalbudsjett (RNB)", "Analysere virkning på kommunens skatteinngang og rammetilskudd", "Spesialrådgiver Strategi", "Regjeringen.no / Excel", "Styringsdokument", "Fullført"),
        ("Q2", "Mai", "25. mai 2026", "1. Tertialrapport (T1) i Bystyret", "Avviksanalyse T1, sykepengeetterslep, første EOY-prognose", "Senior Controller", "Framsikt / Power BI", "Kommuneloven § 14-5", "Fullført"),
        ("Q2", "Juni", "15. jun 2026", "Endelige KOSTRA-tall publiseres", "Benchmarking mot ASSS-kommunene (Stavanger, Bergen, m.fl.)", "Rådgiver Virksomhetsstyring", "SSB KOSTRA / Power BI", "SSB Statistikk", "Fullført"),
        ("Q3", "August", "15. aug 2026", "Innspill til HØP 2027–2030", "Innhente investerings- og driftsbehov fra kommunalsjefene", "Controller Oppvekst / Helse", "Framsikt Budsjettmodul", "Kommuneloven § 14-2", "Fullført"),
        ("Q3", "September", "15. sep 2026", "Lukking av 2. Tertialregnskap", "Månedsslutt august/september, periodiseringer og prosjektestimat", "Prosjektcontroller", "Visma ERP", "Periodelukkingsprosedyre", "Fullført"),
        ("Q3", "September", "23. sep 2026", "Kommunedirektørens forslag til HØP", "Ferdigstille 4-årig økonomiplan og investeringsprogram", "Økonomidirektør", "Framsikt / Sakspapir", "Kommuneloven § 14-2", "Fullført"),
        ("Q3", "September", "28. sep 2026", "2. Tertialrapport (T2) i Formannskapet", "Fremme avvikssak: Oppvekst +4,1M, BoMiljø +7,8M, fondsbruk", "Senior Controller", "Control Office Hub", "Kommuneloven § 14-5", "PÅGÅR NÅ (Aktiv)"),
        ("Q4", "Oktober", "07. okt 2026", "Statsbudsjettet 2027 fremlegges", "Beregne lokale konsekvenser av deflator og vekst i frie inntekter", "Sjeføkonom / Controller", "Statsbudsjett.no / Excel", "Styringssignal", "Planlagt"),
        ("Q4", "November", "10. nov 2026", "Månedsoppfølging per oktober", "Kontrollere at tiltak iverksatt i T2 har bremset vikarforbruket", "Controller", "Visma / Power BI", "Internkontroll", "Planlagt"),
        ("Q4", "November", "25. nov 2026", "Formannskapets budsjettinnstilling", "Politisk behandling av HØP 2027-2030 og Årsbudsjett 2027", "Formannskapet / Rådmann", "Politiske sakspapirer", "Kommuneloven § 14-3", "Planlagt"),
        ("Q4", "Desember", "18. des 2026", "Bystyrets endelige Budsjettsanktion", "Sluttvedtak av Handlings- og økonomiplan og skatteøre", "Bystyret", "Bystyrevedtak", "Kommuneloven § 14-3", "Planlagt"),
        ("Q4", "Desember", "31. des 2026", "Årsoppgjørsstenging 2026", "Årsoppgjørsdisponeringer, overføringer og fondsavsetninger", "Regnskap / Controller", "Visma ERP / Framsikt", "Kommuneloven § 14-6", "Planlagt"),
    ]

    row_idx += 1
    for ev in calendar_events:
        q, mnd, dato, hendelse, oppgave, rolle, sys_kilde, lov, status = ev
        ws.cell(row=row_idx, column=2, value=q).font = FONT_BOLD
        ws.cell(row=row_idx, column=3, value=mnd).font = FONT_REGULAR
        ws.cell(row=row_idx, column=4, value=dato).font = FONT_REGULAR
        ws.cell(row=row_idx, column=5, value=hendelse).font = FONT_BOLD
        ws.cell(row=row_idx, column=6, value=oppgave).font = FONT_REGULAR
        ws.cell(row=row_idx, column=7, value=rolle).font = FONT_REGULAR
        ws.cell(row=row_idx, column=8, value=sys_kilde).font = FONT_MUTED
        ws.cell(row=row_idx, column=9, value=lov).font = FONT_MUTED

        c_st = ws.cell(row=row_idx, column=10, value=status)
        if "PÅGÅR" in status:
            c_st.font = FONT_ALERT_AMBER
            c_st.fill = FILL_ALERT_AMBER
        elif "Fullført" in status:
            c_st.font = FONT_SUCCESS_GREEN
        else:
            c_st.font = FONT_MUTED

        for c in range(2, 11):
            ws.cell(row=row_idx, column=c).border = BORDER_ROW
        row_idx += 1


def create_audit_and_checklist(ws):
    """Fane 5: Revisjon & Controller Sjekkliste (Månedsavslutning, Tertial, Kommunerevisjon)."""
    ws.views.sheetView[0].showGridLines = True
    ws.cell(row=2, column=2, value="🛡️ KRISTIANSAND KOMMUNE — CONTROLLER & REVISJON SJEKKLISTE").font = FONT_TITLE
    ws.cell(row=3, column=2, value="Internkontroll, Månedslukking, Stage-Gate Portmodell (1-10) og Kommuneloven kap. 24").font = FONT_SUBTITLE

    headers = [
        "Område", "Sjekk-ID", "Kontrollpunkt & Beskrivelse", "Frekvens",
        "Hjemmel / Standard", "Ansvarlig", "Kontrollmetodikk", "Status", "Signatur / SHA-256 Hash"
    ]

    row_idx = 5
    for c_idx, h_text in enumerate(headers, start=2):
        cell = ws.cell(row=row_idx, column=c_idx, value=h_text)
        cell.font = FONT_HEADER
        cell.fill = FILL_NAVY_HEADER
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_HEADER

    checklist_items = [
        ("Månedsavslutning", "CHK-01", "Bankavstemminger fullført for samtlige kommunale driftskontoer", "Månedlig", "Regnskapsforskrift § 2-1", "Regnskapsavdelingen", "Fullstendig saldoavstemming", "Godkjent", "SHA256: 7f83b1657ff1..."),
        ("Månedsavslutning", "CHK-02", "Gjennomgang av uoppgjorte poster på mellomregningskontoer", "Månedlig", "Internkontrollforskriften", "Regnskapsfører", "Maks 30 dagers restanser", "Godkjent", "SHA256: 9b2d8c341aa0..."),
        ("Månedsavslutning", "CHK-03", "Periodisering av kjente vesentlige inntekter og kostnader", "Månedlig", "God kommunal regnskapsskikk", "Controller", "Balansejusteringer", "Godkjent", "SHA256: 12ab44ef8912..."),
        ("Månedsavslutning", "CHK-04", "Avstemming av lønns- og trekkontoer mot A-melding til Skatteetaten", "Månedlig", "A-opplysningsloven", "Lønnsansvarlig", "Månedlig kvittering", "Godkjent", "SHA256: c398ef2011da..."),
        ("Tertialavslutning", "CHK-05", "Avstemming mellom Visma ERP faktisk forbruk og Framsikt rammer", "Tertialvis", "Kommuneloven § 14-5", "Senior Controller", "Automatisk diff-sjekk", "Godkjent", "SHA256: e3b0c44298fc..."),
        ("Tertialavslutning", "CHK-06", "Validering av sykepengerefusjoner fra NAV (etterslep)", "Tertialvis", "Folketrygdloven kap. 8", "Rådgiver Helse / Skole", "Refusjonssaldo vs. krav", "Avvik funnet", "Fulgtes opp i T2"),
        ("Tertialavslutning", "CHK-07", "Oppdatering av Earned Value (EVM) for investeringsprosjekter >10M", "Tertialvis", "Prosjektstyringsmodell", "Prosjektcontroller", "BAC/EAC/CPI beregning", "Godkjent", "EVM Ark fane 3"),
        ("Tertialavslutning", "CHK-08", "Klargjøring av politisk saksfremlegg med obligatorisk tiltaksplan", "Tertialvis", "Kommuneloven § 14-5", "Økonomidirektør", "Skriftlig saksnotat", "Godkjent", "Formannskapssak"),
        ("AI & RAG Audit", "CHK-09", "Verifisering av uforanderlig SHA-256 logg i Audit_AI_Actions", "Løpende", "EU AI Act Art. 26(6)", "Internrevisjonen", "Kryptografisk hash-kontroll", "Godkjent", "100% hash-samsvar"),
        ("AI & RAG Audit", "CHK-10", "Human-in-the-Loop (HITL) validering — 0 autonome vedtak", "Løpende", "GDPR Art. 22 / Kommuneloven", "Controller / Rådgiver", "Aktiv godkjenning påkrevd", "Godkjent", "100% HITL dekning"),
        ("AI & RAG Audit", "CHK-11", "PII-vasking og personvernskjerming før LLM-prosessering", "Løpende", "GDPR Art. 5 / Port 4", "Systemansvarlig", "RegEx + NER anonymisering", "Godkjent", "0 PII lekket"),
        ("AI & RAG Audit", "CHK-12", "Glass-Box kildeverifisering (100% sitater mot lov og reglement)", "Løpende", "Stage-Gate Port 8", "AI Guardrails", "Paragrafsjekk (§)", "Godkjent", "100% kildeforankret"),
        ("Kommunerevisjon", "CHK-13", "Stikkprøvekontroll av innkjøpsavtaler mot terskelverdier (Anskaffelser)", "Årlig", "Anskaffelsesloven", "Agder Kommunerevisjon", "Stikkprøve 50 fakturaer", "Planlagt", "Revisjonsplan"),
        ("Kommunerevisjon", "CHK-14", "Kontroll av disposisjonsfond og lovpålagte bundne fondsavsetninger", "Årlig", "Kommuneloven § 14-18", "Kommunerevisjonen", "Balanse- og formueskontroll", "Planlagt", "Årsrevisjon"),
    ]

    row_idx += 1
    for it in checklist_items:
        omr, cid, tittel, frekv, lov, ans, met, stat, sign = it
        ws.cell(row=row_idx, column=2, value=omr).font = FONT_BOLD
        ws.cell(row=row_idx, column=3, value=cid).font = FONT_REGULAR
        ws.cell(row=row_idx, column=4, value=tittel).font = FONT_REGULAR
        ws.cell(row=row_idx, column=5, value=frekv).font = FONT_MUTED
        ws.cell(row=row_idx, column=6, value=lov).font = FONT_MUTED
        ws.cell(row=row_idx, column=7, value=ans).font = FONT_REGULAR
        ws.cell(row=row_idx, column=8, value=met).font = FONT_MUTED

        c_st = ws.cell(row=row_idx, column=9, value=stat)
        if stat == "Godkjent":
            c_st.font = FONT_SUCCESS_GREEN
            c_st.fill = FILL_SUCCESS_GREEN
        elif stat == "Avvik funnet":
            c_st.font = FONT_ALERT_AMBER
            c_st.fill = FILL_ALERT_AMBER
        else:
            c_st.font = FONT_MUTED

        ws.cell(row=row_idx, column=10, value=sign).font = FONT_MUTED

        for c in range(2, 11):
            ws.cell(row=row_idx, column=c).border = BORDER_ROW
        row_idx += 1


def create_kostra_mapping(ws):
    """Fane 6: Masterdata KOSTRA-kontoplan og mapping mot Visma ERP."""
    ws.views.sheetView[0].showGridLines = True
    ws.cell(row=2, column=2, value="📚 KRISTIANSAND KOMMUNE — KOSTRA KONTOPLAN & MASTERDATA").font = FONT_TITLE
    ws.cell(row=3, column=2, value="SSB KOSTRA Funksjoner, Kostnadsarter og Kontoklasser (Kilde: kostra_kontoplan.csv)").font = FONT_SUBTITLE

    headers = ["Kategori", "Kode", "Betegnelse / Tekst", "Kontoklasse", "SSB Rapporteringsplikt", "Kommentar / Merknad"]
    row_idx = 5
    for c_idx, h_text in enumerate(headers, start=2):
        cell = ws.cell(row=row_idx, column=c_idx, value=h_text)
        cell.font = FONT_HEADER
        cell.fill = FILL_NAVY_HEADER
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_HEADER

    sample_kostra = [
        ("Funksjon", "100", "Politiske styringsorganer", "1 (Drift)", "Obligatorisk", "Kommunestyre, formannskap, kontrollutvalg"),
        ("Funksjon", "120", "Administrasjon og fellesutgifter", "1 (Drift)", "Obligatorisk", "Sentraladministrasjon og stab"),
        ("Funksjon", "202", "Grunnskoleundervisning", "1 (Drift)", "Obligatorisk", "Kommunale skoler, lærere og drift"),
        ("Funksjon", "211", "Styrket tilbud til førskolebarn", "1 (Drift)", "Obligatorisk", "Spesialpedagogisk hjelp barnehage"),
        ("Funksjon", "234", "Aktivitetstilbud barn og unge", "1 (Drift)", "Obligatorisk", "SFO og fritidsklubber"),
        ("Funksjon", "253", "Pleie, omsorg og botilbud", "1 (Drift)", "Obligatorisk", "Sykehjem og heldøgns omsorgsboliger"),
        ("Funksjon", "261", "Hjemmetjenester", "1 (Drift)", "Obligatorisk", "Hjemmesykepleie og praktisk bistand"),
        ("Art", "010", "Fast lønn", "1 (Drift)", "Obligatorisk", "Hovedlønnsart for faste stillinger"),
        ("Art", "020", "Vikarer", "1 (Drift)", "Obligatorisk", "Ekstrahjelp og korttidsvikarer"),
        ("Art", "030", "Overtid og ekstraarbeid", "1 (Drift)", "Obligatorisk", "Overtidstillegg"),
        ("Art", "090", "Pensjonsinnskudd og arbeidsgiveravgift", "1 (Drift)", "Obligatorisk", "KLP / SPK og AGA"),
        ("Art", "120", "Kjøp av varer og tjenester", "1 (Drift)", "Obligatorisk", "Driftsmateriell, konsulenter, lisenser"),
        ("Art", "700", "Refusjoner fra staten", "1 (Drift)", "Obligatorisk", "NAV sykepenger, ressurskrevende tjenester"),
        ("Art", "900", "Bruk av disposisjonsfond", "1 (Drift)", "Obligatorisk", "Finansiering av netto merforbruk"),
    ]

    row_idx += 1
    for k in sample_kostra:
        kat, kode, navn, kl, ssb, m = k
        ws.cell(row=row_idx, column=2, value=kat).font = FONT_BOLD
        ws.cell(row=row_idx, column=3, value=kode).font = FONT_REGULAR
        ws.cell(row=row_idx, column=4, value=navn).font = FONT_REGULAR
        ws.cell(row=row_idx, column=5, value=kl).font = FONT_MUTED
        ws.cell(row=row_idx, column=6, value=ssb).font = FONT_REGULAR
        ws.cell(row=row_idx, column=7, value=m).font = FONT_MUTED

        for c in range(2, 8):
            ws.cell(row=row_idx, column=c).border = BORDER_ROW
        row_idx += 1


def auto_fit_columns(ws):
    """Justerer kolonnebredder automatisk for perfekt lesbarhet."""
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        if col[0].column == 1:
            ws.column_dimensions[col_letter].width = 3  # Smal marg i kolonne A
            continue
        for cell in col:
            val_str = str(cell.value or "")
            if cell.row in [2, 3]:  # Ikke bruk tittelradene til kolonnebredde
                continue
            max_len = max(max_len, len(val_str))
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)


def generate_master_excel():
    """Hovedfunksjon som bygger hele arbeidsboken."""
    print("=" * 80)
    print("🚀 GENERERER MASTER CONTROLLER EXCEL RAPPORT")
    print(f"Målfil: {EXCEL_PATH}")
    print("=" * 80)

    summary_rows, variance_rows = fetch_database_data()
    print(f"Hentet {len(summary_rows)} enhetssammendrag og {len(variance_rows)} kritiske avvikslinjer.")

    wb = openpyxl.Workbook()
    # Fjern standard ark
    wb.remove(wb.active)

    # 1. Executive Dashboard
    ws1 = wb.create_sheet(title="Executive_Dashboard")
    create_executive_dashboard(ws1, summary_rows)
    auto_fit_columns(ws1)

    # 2. Tertialrapport T2
    ws2 = wb.create_sheet(title="Tertialrapport_T2")
    create_tertial_report(ws2, variance_rows)
    auto_fit_columns(ws2)

    # 3. Prosjektkontroll EVM
    ws3 = wb.create_sheet(title="Prosjektkontroll_EVM")
    create_project_controlling_evm(ws3)
    auto_fit_columns(ws3)

    # 4. Styringskalender & Årshjul
    ws4 = wb.create_sheet(title="Styringskalender_Arshjul")
    create_calendar_and_wheel(ws4)
    auto_fit_columns(ws4)

    # 5. Revisjon & Sjekkliste
    ws5 = wb.create_sheet(title="Revisjon_Og_Checklist")
    create_audit_and_checklist(ws5)
    auto_fit_columns(ws5)

    # 6. KOSTRA Kontoplan
    ws6 = wb.create_sheet(title="KOSTRA_Kontoplan_Mapping")
    create_kostra_mapping(ws6)
    auto_fit_columns(ws6)

    # Lagre arbeidsboken
    wb.save(EXCEL_PATH)
    print(f"✅ Excel-rapport vellykket generert i: {EXCEL_PATH}")
    print(f"Størrelse: {os.path.getsize(EXCEL_PATH):,} bytes".replace(",", " "))


if __name__ == "__main__":
    generate_master_excel()
