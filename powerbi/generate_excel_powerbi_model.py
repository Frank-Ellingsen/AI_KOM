#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
KRISTIANSAND KOMMUNE - GENERER EXCEL / POWER BI DATAMODELL-ARBEIDSBOK
===============================================================================
Dette skriptet leser SQLite Golden Record databasen og genererer en komplett,
strukturert Excel-arbeidsbok: 'powerbi/Kristiansand_EPM_PowerBI_Model.xlsx'
- Inneholder Excel-tabeller med riktig navngivning og datatyper for Power BI
- Inkluderer sammendragstabeller formatert etter Edward Tuftes prinsipper
===============================================================================
"""

import sys
import sqlite3
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Sikre UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent if BASE_DIR.name == "powerbi" else BASE_DIR
DB_PATH = PROJECT_ROOT / "kristiansand_golden_record.db"
OUTPUT_XLSX = BASE_DIR / "Kristiansand_EPM_PowerBI_Model.xlsx"

def apply_tufte_header(sheet, start_row, headers):
    """Påfører Tufte-header: Mørk/grå tekst, tynn bunnlinje, ingen tunge fyllinger."""
    thin_bottom = Border(bottom=Side(style='medium', color='1A202C'))
    for col_idx, header_text in enumerate(headers, 1):
        cell = sheet.cell(row=start_row, column=col_idx, value=header_text)
        cell.font = Font(name='Segoe UI', size=10, bold=True, color='1A202C')
        cell.fill = PatternFill(start_color='F7FAFC', end_color='F7FAFC', fill_type='solid')
        cell.border = thin_bottom
        cell.alignment = Alignment(horizontal='center' if 'Dato' in header_text or 'Key' in header_text else 'left', vertical='center')

def create_excel_model():
    print(f"Kobler til Golden Record: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    wb = openpyxl.Workbook()
    # Fjern standard ark
    wb.remove(wb.active)

    thin_border = Border(bottom=Side(style='thin', color='E2E8F0'))
    
    # -------------------------------------------------------------------------
    # TABELL 1: Fact_Regnskap
    # -------------------------------------------------------------------------
    ws_fact = wb.create_sheet(title="Fact_Regnskap")
    headers_fact = ["transaksjon_id", "kilde_system", "funksjon_key", "art_key", "ansvar_key", "dato_key", "belop", "korrigert_belop", "budsjett_belop", "avvik_belop"]
    apply_tufte_header(ws_fact, 1, headers_fact)

    cur.execute("SELECT transaksjon_id, kilde_system, funksjon_key, art_key, ansvar_key, dato_key, belop, korrigert_belop, budsjett_belop, avvik_belop FROM Fact_Regnskap")
    rows = cur.fetchall()
    for r_idx, row in enumerate(rows, 2):
        for c_idx, val in enumerate(row, 1):
            cell = ws_fact.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name='Segoe UI', size=9)
            cell.border = thin_border
            if c_idx in [7, 8, 9, 10]:
                cell.number_format = '#,##0'
                cell.alignment = Alignment(horizontal='right')
            else:
                cell.alignment = Alignment(horizontal='left')
    print(f"✓ Fact_Regnskap eksportert: {len(rows)} rader.")

    # -------------------------------------------------------------------------
    # TABELL 2: Dim_Funksjon
    # -------------------------------------------------------------------------
    ws_funk = wb.create_sheet(title="Dim_Funksjon")
    headers_funk = ["funksjon_key", "funksjon_kode", "funksjon_navn", "hovedfunksjon_kode", "tjenesteomrade_navn"]
    apply_tufte_header(ws_funk, 1, headers_funk)

    cur.execute("SELECT funksjon_key, funksjon_kode, funksjon_navn, hovedfunksjon_kode, tjenesteomrade_navn FROM Dim_Funksjon")
    for r_idx, row in enumerate(cur.fetchall(), 2):
        for c_idx, val in enumerate(row, 1):
            cell = ws_funk.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name='Segoe UI', size=9)
            cell.border = thin_border

    # -------------------------------------------------------------------------
    # TABELL 3: Dim_Art
    # -------------------------------------------------------------------------
    ws_art = wb.create_sheet(title="Dim_Art")
    headers_art = ["art_key", "art_kode", "art_navn", "art_gruppe", "sign_multiplier"]
    apply_tufte_header(ws_art, 1, headers_art)

    cur.execute("SELECT art_key, art_kode, art_navn, art_gruppe, sign_multiplier FROM Dim_Art")
    for r_idx, row in enumerate(cur.fetchall(), 2):
        for c_idx, val in enumerate(row, 1):
            cell = ws_art.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name='Segoe UI', size=9)
            cell.border = thin_border

    # -------------------------------------------------------------------------
    # TABELL 4: Dim_Ansvar
    # -------------------------------------------------------------------------
    ws_ans = wb.create_sheet(title="Dim_Ansvar")
    headers_ans = ["ansvar_key", "ansvar_kode", "ansvar_navn", "kommunalsjefomrade"]
    apply_tufte_header(ws_ans, 1, headers_ans)

    cur.execute("SELECT ansvar_key, ansvar_kode, ansvar_navn, kommunalsjefomrade FROM Dim_Ansvar")
    for r_idx, row in enumerate(cur.fetchall(), 2):
        for c_idx, val in enumerate(row, 1):
            cell = ws_ans.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name='Segoe UI', size=9)
            cell.border = thin_border

    # -------------------------------------------------------------------------
    # TABELL 5: Dim_Dato
    # -------------------------------------------------------------------------
    ws_dato = wb.create_sheet(title="Dim_Dato")
    headers_dato = ["dato_key", "full_dato", "ar", "tertial", "maned"]
    apply_tufte_header(ws_dato, 1, headers_dato)

    cur.execute("SELECT dato_key, full_dato, ar, tertial, maned FROM Dim_Dato")
    for r_idx, row in enumerate(cur.fetchall(), 2):
        for c_idx, val in enumerate(row, 1):
            cell = ws_dato.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name='Segoe UI', size=9)
            cell.border = thin_border

    # -------------------------------------------------------------------------
    # TABELL 6: Audit_AI_Actions
    # -------------------------------------------------------------------------
    ws_audit = wb.create_sheet(title="Audit_AI_Actions")
    headers_audit = ["log_id", "tidsstempel", "enhet_kode", "ai_modell_versjon", "prognostisert_avvik", "foreslatt_tiltak", "konfidens_score", "leder_beslutning", "begrunnelse_tekst", "godkjent_av_saksbehandler", "IP_adresse"]
    apply_tufte_header(ws_audit, 1, headers_audit)

    cur.execute("SELECT log_id, tidsstempel, enhet_kode, ai_modell_versjon, prognostisert_avvik, foreslatt_tiltak, konfidens_score, leder_beslutning, begrunnelse_tekst, godkjent_av_saksbehandler, IP_adresse FROM Audit_AI_Actions")
    for r_idx, row in enumerate(cur.fetchall(), 2):
        for c_idx, val in enumerate(row, 1):
            cell = ws_audit.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name='Segoe UI', size=9)
            cell.border = thin_border
            if c_idx == 5:
                cell.number_format = '#,##0'
                cell.alignment = Alignment(horizontal='right')
            elif c_idx == 7:
                cell.number_format = '0.0%'
                cell.alignment = Alignment(horizontal='right')

    # -------------------------------------------------------------------------
    # TABELL 7: Dashboard_Sektor (Edward Tufte Styringssammendrag)
    # -------------------------------------------------------------------------
    ws_dash = wb.create_sheet(title="Dashboard_Sektor")
    ws_dash.views.sheetView[0].showGridLines = True
    
    # Tittelblokk
    title_cell = ws_dash.cell(row=2, column=2, value="KRISTIANSAND KOMMUNE - VIRKSOMHETSSTYRING T2")
    title_cell.font = Font(name='Segoe UI', size=14, bold=True, color='1A202C')
    subtitle_cell = ws_dash.cell(row=3, column=2, value="Konsolidert avviksoppfølging: Kommunal Skole vs. Kommunal Boenhet")
    subtitle_cell.font = Font(name='Segoe UI', size=10, italic=True, color='718096')

    headers_dash = ["Kommunalsjefområde", "Enhet / Ansvar", "Funksjon", "Budsjett YTD (kr)", "Regnskap YTD (kr)", "Avvik YTD (kr)", "Avvik %", "Status"]
    for c_idx, h in enumerate(headers_dash, 2):
        c = ws_dash.cell(row=5, column=c_idx, value=h)
        c.font = Font(name='Segoe UI', size=10, bold=True, color='1A202C')
        c.fill = PatternFill(start_color='EDF2F7', end_color='EDF2F7', fill_type='solid')
        c.border = Border(bottom=Side(style='medium', color='2D3748'))
        c.alignment = Alignment(horizontal='right' if 'kr' in h or '%' in h else 'left')

    cur.execute("""
        SELECT 
            da.kommunalsjefomrade,
            da.ansvar_navn,
            df.funksjon_navn,
            ROUND(SUM(fr.budsjett_belop), 0) as bud,
            ROUND(SUM(fr.korrigert_belop), 0) as regn,
            ROUND(SUM(fr.avvik_belop), 0) as avv
        FROM Fact_Regnskap fr
        JOIN Dim_Ansvar da ON fr.ansvar_key = da.ansvar_key
        JOIN Dim_Funksjon df ON fr.funksjon_key = df.funksjon_key
        JOIN Dim_Dato dd ON fr.dato_key = dd.dato_key
        WHERE (fr.kilde_system LIKE '%BOOM%' AND dd.maned <= 8) OR (fr.kilde_system LIKE '%Skole%')
        GROUP BY da.kommunalsjefomrade, da.ansvar_navn, df.funksjon_navn
        ORDER BY da.kommunalsjefomrade, da.ansvar_navn
    """)
    summary_rows = cur.fetchall()
    for r_idx, (omrade, ansvar, funk, bud, regn, avv) in enumerate(summary_rows, 6):
        pct = (avv / bud) if bud and bud > 0 else 0.0
        status = "Merforbruk (Sprekk)" if avv > 50000 else ("Mindreforbruk" if avv < -10000 else "I Balanse")
        
        row_vals = [omrade, ansvar, funk, bud, regn, avv, pct, status]
        for c_idx, val in enumerate(row_vals, 2):
            cell = ws_dash.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name='Segoe UI', size=10)
            cell.border = thin_border
            if c_idx in [5, 6, 7]:
                cell.number_format = '#,##0'
                cell.alignment = Alignment(horizontal='right')
                if c_idx == 7: # Avvik
                    if val > 50000:
                        cell.font = Font(name='Segoe UI', size=10, bold=True, color='C53030') # Dempet rød
                    elif val < -50000:
                        cell.font = Font(name='Segoe UI', size=10, color='2B6CB0') # Dempet blå
            elif c_idx == 8: # Prosent
                cell.number_format = '0.0%'
                cell.alignment = Alignment(horizontal='right')
            else:
                cell.alignment = Alignment(horizontal='left')

    conn.close()

    # Juster kolonnebredder automatisk
    for sheet in wb.worksheets:
        for col in sheet.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            sheet.column_dimensions[col_letter].width = max(max_len + 3, 11)

    wb.save(OUTPUT_XLSX)
    print(f"\n[OK] Excel / Power BI arbeidsbok generert: {OUTPUT_XLSX}")

if __name__ == "__main__":
    create_excel_model()
