#!/usr/bin/env python3
"""
Generator for 'Rapport Enhet Bo og Miljø.xlsx'
Fullt alligned med minicase-workflow, Human-in-the-Loop (HITL) interface,
governance sign-off, revisjonsspor og Edward Tufte Data-Ink standarder.
"""

from pathlib import Path
from datetime import datetime
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

PILOT_DIR = Path(__file__).resolve().parent
TARGET_EXCEL = PILOT_DIR / "Rapport Enhet Bo og Miljø.xlsx"
DB_SQLITE = PILOT_DIR / "mvp_pilot.db"

# --- FARGEPALETT (Edward Tufte Muted Professional Palette) ---
COLOR_NAVY = "1B365D"       # Hovedtittel & Tabelloverskrifter
COLOR_SLATE_BG = "F1F5F9"   # Nøytralt seksjonsfyll / KPI-bakgrunn
COLOR_WHITE = "FFFFFF"
COLOR_TEXT_MAIN = "0F172A"  # Mørk tekst
COLOR_TEXT_MUTED = "475569" # Sekundærtekst / veiledning
COLOR_BORDER = "CBD5E1"     # Tynn horisontal linje (1px)
COLOR_ALERT_RED = "C53030"  # Aksent: Merforbruk / Høy risiko
COLOR_ALERT_AMB = "D97706"  # Aksent: Observasjon / Moderat risiko
COLOR_ACCENT_GRN = "166534" # Aksent: Godkjent / Innsparing
COLOR_BADGE_RED_BG = "FEE2E2"
COLOR_BADGE_GRN_BG = "DCFCE7"
COLOR_BADGE_AMB_BG = "FEF3C7"

# Stiler
font_title = Font(name="Calibri", size=16, bold=True, color=COLOR_WHITE)
font_subtitle = Font(name="Calibri", size=10, italic=True, color="E2E8F0")
font_section = Font(name="Calibri", size=11, bold=True, color=COLOR_NAVY)
font_header = Font(name="Calibri", size=10, bold=True, color=COLOR_WHITE)
font_bold = Font(name="Calibri", size=10, bold=True, color=COLOR_TEXT_MAIN)
font_regular = Font(name="Calibri", size=10, color=COLOR_TEXT_MAIN)
font_muted = Font(name="Calibri", size=9, italic=True, color=COLOR_TEXT_MUTED)
font_kpi_num = Font(name="Calibri", size=13, bold=True, color=COLOR_NAVY)
font_kpi_red = Font(name="Calibri", size=13, bold=True, color=COLOR_ALERT_RED)
font_kpi_grn = Font(name="Calibri", size=13, bold=True, color=COLOR_ACCENT_GRN)

fill_navy = PatternFill("solid", fgColor=COLOR_NAVY)
fill_slate = PatternFill("solid", fgColor=COLOR_SLATE_BG)
fill_red_badge = PatternFill("solid", fgColor=COLOR_BADGE_RED_BG)
fill_grn_badge = PatternFill("solid", fgColor=COLOR_BADGE_GRN_BG)
fill_amb_badge = PatternFill("solid", fgColor=COLOR_BADGE_AMB_BG)

border_thin_bottom = Border(bottom=Side(style="thin", color=COLOR_BORDER))
border_thin_top_bottom = Border(top=Side(style="thin", color=COLOR_BORDER), bottom=Side(style="thin", color=COLOR_BORDER))
border_double_bottom = Border(top=Side(style="thin", color=COLOR_BORDER), bottom=Side(style="double", color=COLOR_BORDER))

align_left = Alignment(horizontal="left", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")
align_center = Alignment(horizontal="center", vertical="center")

# Formater
FMT_KR = '#,##0 "kr"'
FMT_PCT = '0.0%'
FMT_INT = '#,##0'


def add_banner(ws, title: str, subtitle: str, max_col: int = 12):
    ws.views.sheetView[0].showGridLines = True
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=max_col)
    ws.cell(1, 1).value = title
    ws.cell(1, 1).font = font_title
    ws.cell(1, 1).fill = fill_navy
    ws.cell(1, 1).alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 28

    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=max_col)
    ws.cell(2, 1).value = subtitle
    ws.cell(2, 1).font = font_subtitle
    ws.cell(2, 1).fill = fill_navy
    ws.cell(2, 1).alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[2].height = 18
    ws.row_dimensions[3].height = 8


def format_header_row(ws, row_idx: int, cols_count: int):
    ws.row_dimensions[row_idx].height = 24
    for c in range(1, cols_count + 1):
        cell = ws.cell(row_idx, c)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = align_center if cell.value in ["ID", "Status", "Beslutning", "Kontroll", "Horisont", "Periode", "Signal", "Revisjonsstatus"] else align_left
        cell.border = border_thin_bottom


def auto_fit_columns(ws, min_width: int = 12, max_width: int = 58):
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            if cell.row in [1, 2]:
                continue
            val_str = str(cell.value or "")
            if "\n" in val_str:
                val_str = max(val_str.split("\n"), key=len)
            max_len = max(max_len, len(val_str))
        ws.column_dimensions[col_letter].width = max(min(max_len + 3, max_width), min_width)


def build_full_workbook():
    wb = Workbook()
    default_sheet = wb.active

    # =========================================================================
    # 1. ARK: 0 Styring & Workflow
    # =========================================================================
    ws0 = wb.create_sheet(title="0 Styring & Workflow")
    add_banner(
        ws0,
        "Kristiansand kommune · Bo og Miljø (Enhet 5200 · KOSTRA 254)",
        "EPM Virksomhetsstyring · AI-Assistert Beslutningsstøtte & Human-in-the-Loop (HITL) Sløyfe | Controller: Frank Ellingsen",
        max_col=10
    )

    ws0.cell(4, 1).value = "STYRINGSRAMME & FORVALTNINGSPRINSIPPER"
    ws0.cell(4, 1).font = font_section
    ws0.cell(5, 1).value = (
        "Dette styringsdokumentet operasjonaliserer Kristiansand kommunes økonomimodell i henhold til Kommuneloven §§ 14-5 og 14-6.\n"
        "All AI-støtte fungerer etter 'Human-in-the-Loop' prinsippet (EU AI Act Art. 14): AI-modeller analyserer avvik og foreslår tiltak, "
        "men ingen tiltakseffekt godskrives i regnskapsprognosen uten eksplisitt saksbehandlergodkjenning og dokumentert fag-/tariffkontroll (HTA § 4)."
    )
    ws0.cell(5, 1).font = font_muted
    ws0.row_dimensions[5].height = 32

    # Executive KPI Cards (Tufte-standard: ingen skygger, ren typografi)
    ws0.cell(7, 1).value = "NØKKELTALL PR. 2. TERTIAL 2024 (BO OG MILJØ)"
    ws0.cell(7, 1).font = font_section

    kpi_cards = [
        ("Vedtatt Årsbudsjett (BAC)", 17233691.0, FMT_KR, font_kpi_num, "Bevilget årsramme for Enhet 5200"),
        ("Bokført Regnskap YTD", 12622851.42, FMT_KR, font_kpi_num, "Faktisk bokført Jan–Aug (73,2 % av årsramme)"),
        ("Merforbruk YTD", 1285614.42, FMT_KR, font_kpi_red, "+11,3 % over periodisert budsjett (RØDT)"),
        ("Ujustert EAC (AI Sesongmodell)", 19050222.75, FMT_KR, font_kpi_red, "+1 816 532 kr merforbruk før tiltak"),
        ("Godkjent Tiltak (HITL)", "='4 HITL Signoff & Governance'!H18", FMT_KR, font_kpi_grn, "Dokumentert og godkjent effekt fra HITL-arket"),
        ("Revidert Sluttkostnad (EAC)", "=B11-B12", FMT_KR, font_kpi_num, "EAC etter godkjente tiltak"),
        ("Gjenstående Restavvik mot BAC", "=B13-B8", FMT_KR, font_kpi_red, "Netto finansieringsgap som krever tertialoppfølging")
    ]

    row_kpi = 8
    ws0.cell(row_kpi - 1, 1).value = "Styringsparameter"
    ws0.cell(row_kpi - 1, 2).value = "Beløp / Verdi"
    ws0.cell(row_kpi - 1, 3).value = "Merknad / Status"
    for c in range(1, 4):
        ws0.cell(row_kpi - 1, c).font = font_header
        ws0.cell(row_kpi - 1, c).fill = fill_navy
        ws0.cell(row_kpi - 1, c).alignment = align_left if c != 2 else align_right

    for label, val, num_fmt, f_style, note in kpi_cards:
        ws0.cell(row_kpi, 1).value = label
        ws0.cell(row_kpi, 1).font = font_bold
        ws0.cell(row_kpi, 1).border = border_thin_bottom

        c2 = ws0.cell(row_kpi, 2)
        c2.value = val
        c2.font = f_style
        c2.number_format = num_fmt
        c2.alignment = align_right
        c2.border = border_thin_bottom

        c3 = ws0.cell(row_kpi, 3)
        c3.value = note
        c3.font = font_muted
        c3.border = border_thin_bottom
        ws0.row_dimensions[row_kpi].height = 20
        row_kpi += 1

    # Styrings-Workflow (5-Trinns Sløyfe)
    ws0.cell(row_kpi + 1, 1).value = "OPERATIV STYRINGS-WORKFLOW (5-TRINNS SLØYFE)"
    ws0.cell(row_kpi + 1, 1).font = font_section

    workflow_steps = [
        ("Trinn 1: Nåsituasjon (Ark '1 Nåsituasjon')", "Avstemmer regnskap mot budsjett. Identifiserer avviksdrivere i KOSTRA-kontoplanen.", "YTD Merforbruk: +1 285 614 kr (10 Lønn står for 1,15 mill. kr)"),
        ("Trinn 2: Prediktiv EAC (Ark '2 Prediktiv EAC')", "Earned Value & sesongjustert tidsserieprognose. Beregner usikkerhetsspenn.", "EAC Sesong: 19 050 223 kr (P10: 18,65m · P50: 19,05m · P90: 19,45m)"),
        ("Trinn 3: Preskriptiv AI (Ark '3 Preskriptiv AI')", "Lokal LLM (Ollama) analyserer avviksmatrisen og genererer 6 kandidattiltak.", "Tiltaksmeny T1..T6 med brutto potensial på 192 967 kr"),
        ("Trinn 4: Human-in-the-Loop (Ark '4 HITL Signoff')", "Controller/leder evaluerer tiltak, dokumenterer kontroll iht. HTA § 4 og signerer.", "Interaktiv Stage-Gate: Kun 'Godkjent' OG 'Ja' godskrives prognosen"),
        ("Trinn 5: Revidert EOY (Ark '5 Revidert EOY')", "Reberegner EOY med godkjent effekt, oppdaterer scenariobro og saksfremlegg.", "Sikker writeback til Excel og uutslettelig revisjonslogg i SQLite")
    ]

    r_wf_head = row_kpi + 2
    ws0.cell(r_wf_head, 1).value = "Trinn"
    ws0.cell(r_wf_head, 2).value = "Aktivitet & Formål"
    ws0.cell(r_wf_head, 3).value = "Nøkkeltall / Status i Bo og Miljø"
    for c in range(1, 4):
        ws0.cell(r_wf_head, c).font = font_header
        ws0.cell(r_wf_head, c).fill = fill_navy
        ws0.cell(r_wf_head, c).alignment = align_left
    ws0.row_dimensions[r_wf_head].height = 22

    r_wf = r_wf_head + 1
    for step, desc, status_txt in workflow_steps:
        ws0.cell(r_wf, 1).value = step
        ws0.cell(r_wf, 1).font = font_bold
        ws0.cell(r_wf, 1).border = border_thin_bottom

        ws0.cell(r_wf, 2).value = desc
        ws0.cell(r_wf, 2).font = font_regular
        ws0.cell(r_wf, 2).border = border_thin_bottom

        ws0.cell(r_wf, 3).value = status_txt
        ws0.cell(r_wf, 3).font = font_bold
        ws0.cell(r_wf, 3).border = border_thin_bottom
        ws0.row_dimensions[r_wf].height = 22
        r_wf += 1

    # Scenariobro Tabell
    r_bridge_head = r_wf + 1
    ws0.cell(r_bridge_head, 1).value = "SCENARIOBRO FRA VEDTATT RAMME TIL REVIDERT SLUTTPROGNOSE"
    ws0.cell(r_bridge_head, 1).font = font_section

    bridge_rows = [
        ("1. Vedtatt årsbudsjett (BAC)", 17233691.0, "Utgangspunkt og bevilget årsramme for Enhet 5200"),
        ("2. Påløpt YTD merforbruk (pr 2. tertial)", 1285614.42, "Bokført merforbruk hittil i år (Jan–Aug)"),
        ("3. Forventet T3 sesong- og trendmerforbruk", 530917.33, "Estimert merforbruk Sep–Des før nye tiltak"),
        ("4. Ujustert EAC Sluttprognose (AI Sesong)", "=B26+B27+B28", "AI Sesongmodell (19 050 222,75 kr) før tiltak"),
        ("5. Hypotetisk full kandidat-effekt (T1–T6)", -192966.73, "Dersom alle AI-kandidater realiseres uten barrierer"),
        ("6. Dokumentert godkjent tiltakseffekt (HITL)", "=-'4 HITL Signoff & Governance'!H18", "Faktisk godkjent effekt etter HTA § 4 og fagkontroll"),
        ("7. Revidert EAC Sluttkostnad", "=B29+B31", "Endelig prognose etter besluttede tiltak"),
        ("8. Gjenstående restavvik mot årsbudsjett", "=B32-B26", "Netto finansieringsgap som må rapporteres til kommunalsjef")
    ]

    r_b_h = r_bridge_head + 1
    ws0.cell(r_b_h, 1).value = "Scenariosteg"
    ws0.cell(r_b_h, 2).value = "Beløp (kr)"
    ws0.cell(r_b_h, 3).value = "Forklaring & Forankring"
    for c in range(1, 4):
        ws0.cell(r_b_h, c).font = font_header
        ws0.cell(r_b_h, c).fill = fill_navy
        ws0.cell(r_b_h, c).alignment = align_left if c != 2 else align_right
    ws0.row_dimensions[r_b_h].height = 22

    r_b = r_b_h + 1
    for step_title, val, exp in bridge_rows:
        ws0.cell(r_b, 1).value = step_title
        ws0.cell(r_b, 1).font = font_bold if "EAC" in step_title or "restavvik" in step_title or "Vedtatt" in step_title else font_regular
        ws0.cell(r_b, 1).border = border_thin_bottom

        c2 = ws0.cell(r_b, 2)
        c2.value = val
        c2.font = font_bold if "EAC" in step_title or "restavvik" in step_title else font_regular
        c2.number_format = FMT_KR
        c2.alignment = align_right
        c2.border = border_thin_bottom

        c3 = ws0.cell(r_b, 3)
        c3.value = exp
        c3.font = font_muted
        c3.border = border_thin_bottom
        ws0.row_dimensions[r_b].height = 20
        r_b += 1

    auto_fit_columns(ws0)

    # =========================================================================
    # 2. ARK: 1 Nåsituasjon & Drivere
    # =========================================================================
    ws1 = wb.create_sheet(title="1 Nåsituasjon & Drivere")
    add_banner(
        ws1,
        "1. Nåsituasjon & Avviksdrivere · Bo og Miljø (T2/2024)",
        "Avstemming mot Unit4 ERP og Visma Enterprise | KOSTRA Funksjon 254 | Tall i NOK",
        max_col=8
    )

    ws1.cell(4, 1).value = "AVSTEMMING REGNSKAP MOT BUDSJETT YTD (JANUAR – AUGUST 2024)"
    ws1.cell(4, 1).font = font_section

    ytd_summary = [
        ("Periodisert Budsjett YTD", 11337237.0, FMT_KR, "65,8 % av årsbudsjett"),
        ("Bokført Regnskap YTD", 12622851.42, FMT_KR, "73,2 % av årsbudsjett"),
        ("Netto Merforbruk YTD", 1285614.42, FMT_KR, "+11,3 % over budsjettert ramme (RØDT)")
    ]

    r_s = 5
    for lbl, v, fmt_str, note in ytd_summary:
        ws1.cell(r_s, 1).value = lbl
        ws1.cell(r_s, 1).font = font_bold
        ws1.cell(r_s, 2).value = v
        ws1.cell(r_s, 2).font = font_bold
        ws1.cell(r_s, 2).number_format = fmt_str
        ws1.cell(r_s, 2).alignment = align_right
        ws1.cell(r_s, 3).value = note
        ws1.cell(r_s, 3).font = font_muted
        ws1.row_dimensions[r_s].height = 20
        r_s += 1

    # Hovedgrupper
    ws1.cell(r_s + 1, 1).value = "FORSKJELLER PER KOSTRA HOVEDGRUPPE"
    ws1.cell(r_s + 1, 1).font = font_section

    hg_headers = ["Hovedgruppe", "Budsjett YTD", "Regnskap YTD", "Merforbruk YTD", "Avvik %", "Andel av Merforbruk"]
    r_hg_h = r_s + 2
    for c, h in enumerate(hg_headers, 1):
        ws1.cell(r_hg_h, c).value = h
    format_header_row(ws1, r_hg_h, len(hg_headers))

    hg_data = [
        ("1 Lønn & Sosiale Kostnader", 11025573.0, 12175245.34, 1149672.34, 0.1043, 0.8943),
        ("2 Andre Driftsutgifter", 311552.0, 455666.08, 144114.08, 0.4626, 0.1121),
        ("3 Salgs- og Leieinntekter", 112.0, -8060.0, -8172.0, -72.964, -0.0064)
    ]

    r_hg = r_hg_h + 1
    for row_vals in hg_data:
        ws1.cell(r_hg, 1).value = row_vals[0]
        ws1.cell(r_hg, 1).font = font_bold
        ws1.cell(r_hg, 1).border = border_thin_bottom

        for c_idx in range(2, 5):
            cell = ws1.cell(r_hg, c_idx)
            cell.value = row_vals[c_idx - 1]
            cell.font = font_regular
            cell.number_format = FMT_KR
            cell.alignment = align_right
            cell.border = border_thin_bottom

        c5 = ws1.cell(r_hg, 5)
        c5.value = row_vals[4]
        c5.font = font_bold if row_vals[4] > 0.05 else font_regular
        c5.number_format = FMT_PCT
        c5.alignment = align_right
        c5.border = border_thin_bottom

        c6 = ws1.cell(r_hg, 6)
        c6.value = row_vals[5]
        c6.font = font_regular
        c6.number_format = FMT_PCT
        c6.alignment = align_right
        c6.border = border_thin_bottom

        ws1.row_dimensions[r_hg].height = 20
        r_hg += 1

    # Topp Avviksdrivere
    ws1.cell(r_hg + 1, 1).value = "TOPP 8 BOKFØRTE AVVIKSDRIVERE (KOSTRA ARTSNIVÅ)"
    ws1.cell(r_hg + 1, 1).font = font_section

    drv_headers = ["Art", "Kontonavn", "Regnskap YTD", "Budsjett YTD", "Merforbruk YTD", "Månedsgj.snitt", "Estimert T3 Behov", "Driverkategori"]
    r_drv_h = r_hg + 2
    for c, h in enumerate(drv_headers, 1):
        ws1.cell(r_drv_h, c).value = h
    format_header_row(ws1, r_drv_h, len(drv_headers))

    drivers_data = [
        ("1010", "Fastlønn - ordinære", 6206768.61, 5731850.0, 474918.61, 775846.08, 3103384.30, "Grunnbemanning / vakanser"),
        ("1270", "Kjøp av vikarbyråtjenester", 382656.0, 0.0, 382656.0, 47832.0, 191328.0, "Akuttvikarer / bemanningsbyrå"),
        ("1020", "Vikar - kvelds- og nattillegg", 259304.09, 0.0, 259304.09, 32413.01, 149099.85, "Ubudsjetterte turnustillegg"),
        ("1040", "Overtidslønn", 242075.85, 56504.0, 185571.85, 30259.48, 139193.61, "Sykefraværsdekning helg"),
        ("1030", "Ekstrahjelp", 141648.70, 0.0, 141648.70, 17706.09, 70824.35, "Timevikarer ved korttidsfravær"),
        ("1020", "Vikar - lørdags- og søndagstillegg", 140747.32, 0.0, 140747.32, 17593.42, 80929.71, "Helgedekning turnus"),
        ("1099", "Arbeidsgiveravgift", 1527431.13, 1425817.0, 101614.13, 190928.89, 763715.57, "Følgekostnad av lønnsvekst"),
        ("1020", "Vikar - helligdagstillegg", 93469.77, 0.0, 93469.77, 11683.72, 53745.12, "Høytidstillegg påske/mai")
    ]

    r_drv = r_drv_h + 1
    for r_vals in drivers_data:
        ws1.cell(r_drv, 1).value = r_vals[0]
        ws1.cell(r_drv, 1).font = font_bold
        ws1.cell(r_drv, 1).alignment = align_center
        ws1.cell(r_drv, 1).border = border_thin_bottom

        ws1.cell(r_drv, 2).value = r_vals[1]
        ws1.cell(r_drv, 2).font = font_regular
        ws1.cell(r_drv, 2).border = border_thin_bottom

        for c_idx in range(3, 8):
            c_cell = ws1.cell(r_drv, c_idx)
            c_cell.value = r_vals[c_idx - 1]
            c_cell.font = font_regular
            c_cell.number_format = FMT_KR
            c_cell.alignment = align_right
            c_cell.border = border_thin_bottom

        ws1.cell(r_drv, 8).value = r_vals[7]
        ws1.cell(r_drv, 8).font = font_muted
        ws1.cell(r_drv, 8).border = border_thin_bottom

        ws1.row_dimensions[r_drv].height = 20
        r_drv += 1

    auto_fit_columns(ws1)

    # =========================================================================
    # 3. ARK: 2 Prediktiv EAC & Konfidens
    # =========================================================================
    ws2 = wb.create_sheet(title="2 Prediktiv EAC & Konfidens")
    add_banner(
        ws2,
        "2. Prediktiv EAC/ETC Prognosemodellering · Prosjektcontrolling",
        "Earned Value Management (BAC/ACWP/ETC/EAC) · Tidsserier & Konfidensintervaller (P10-P50-P90)",
        max_col=8
    )

    ws2.cell(4, 1).value = "SAMMENLIGNING AV PROGNOSEMODELLER (END OF YEAR - EAC)"
    ws2.cell(4, 1).font = font_section

    eac_headers = ["Modellnavn", "Metodikk & Forutsetning", "EAC Sluttprognose", "Årsbudsjett (BAC)", "Prognosert Avvik", "Avvik %", "Styringssignal"]
    r_eac_h = 5
    for c, h in enumerate(eac_headers, 1):
        ws2.cell(r_eac_h, c).value = h
    format_header_row(ws2, r_eac_h, len(eac_headers))

    eac_models = [
        ("1. Excel Sjablong", "YTD Regnskap + Restbudsjett + (50 % x Merforbruk)", 19162112.63, 17233691.0, 1928421.63, -0.1119, "RØD"),
        ("2. Lineær Run-rate", "Mekanisk ekstrapolering: (YTD / 8) x 12", 18934277.13, 17233691.0, 1700586.13, -0.0987, "GUL"),
        ("3. AI Sesongmodell (Anbefalt)", "Driver-basert KOSTRA-artsnivå m/ sesongvekting og NAV-lag", 19050222.75, 17233691.0, 1816531.75, -0.1054, "RØD")
    ]

    r_eac = r_eac_h + 1
    for m_vals in eac_models:
        ws2.cell(r_eac, 1).value = m_vals[0]
        ws2.cell(r_eac, 1).font = font_bold
        ws2.cell(r_eac, 1).border = border_thin_bottom

        ws2.cell(r_eac, 2).value = m_vals[1]
        ws2.cell(r_eac, 2).font = font_regular
        ws2.cell(r_eac, 2).border = border_thin_bottom

        c3 = ws2.cell(r_eac, 3)
        c3.value = m_vals[2]
        c3.font = font_bold
        c3.number_format = FMT_KR
        c3.alignment = align_right
        c3.border = border_thin_bottom

        c4 = ws2.cell(r_eac, 4)
        c4.value = m_vals[3]
        c4.font = font_regular
        c4.number_format = FMT_KR
        c4.alignment = align_right
        c4.border = border_thin_bottom

        c5 = ws2.cell(r_eac, 5)
        c5.value = m_vals[4]
        c5.font = font_bold
        c5.number_format = FMT_KR
        c5.alignment = align_right
        c5.border = border_thin_bottom

        c6 = ws2.cell(r_eac, 6)
        c6.value = m_vals[5]
        c6.font = font_bold
        c6.number_format = FMT_PCT
        c6.alignment = align_right
        c6.border = border_thin_bottom

        c7 = ws2.cell(r_eac, 7)
        c7.value = m_vals[6]
        c7.font = font_bold
        c7.alignment = align_center
        c7.fill = fill_red_badge if m_vals[6] == "RØD" else fill_amb_badge
        c7.border = border_thin_bottom

        ws2.row_dimensions[r_eac].height = 22
        r_eac += 1

    # Konfidensintervaller
    ws2.cell(r_eac + 1, 1).value = "KONFIDENSINTERVALLER & STRESSTESTING (MONTE CARLO SIMULERING)"
    ws2.cell(r_eac + 1, 1).font = font_section

    ci_headers = ["Persentil", "Scenariobeskrivelse", "EAC Sluttbeløp", "Merforbruk mot BAC", "Sannsynlighet"]
    r_ci_h = r_eac + 2
    for c, h in enumerate(ci_headers, 1):
        ws2.cell(r_ci_h, c).value = h
    format_header_row(ws2, r_ci_h, len(ci_headers))

    ci_rows = [
        ("P10 (Optimistisk)", "Rask refusjonsinngang fra NAV, lavt høstfravær, minimal overtidsbruk i turnus", 18650262.97, 1416571.97, "10 % sjanse for lavere kostnad"),
        ("P50 (Forventningsrett)", "Mest sannsynlig utfall uten nye korrigerende tiltak (Sesongnormal)", 19050222.75, 1816531.75, "Median forventet sluttresultat"),
        ("P90 (Pessimistisk)", "Stresstest: Høy influensabølge i T3, økt helgeovertid og forsinkede refusjoner", 19449544.32, 2215853.32, "90 % konfidensgrense (Worst-case)")
    ]

    r_ci = r_ci_h + 1
    for ci in ci_rows:
        ws2.cell(r_ci, 1).value = ci[0]
        ws2.cell(r_ci, 1).font = font_bold
        ws2.cell(r_ci, 1).border = border_thin_bottom

        ws2.cell(r_ci, 2).value = ci[1]
        ws2.cell(r_ci, 2).font = font_regular
        ws2.cell(r_ci, 2).border = border_thin_bottom

        c3 = ws2.cell(r_ci, 3)
        c3.value = ci[2]
        c3.font = font_bold
        c3.number_format = FMT_KR
        c3.alignment = align_right
        c3.border = border_thin_bottom

        c4 = ws2.cell(r_ci, 4)
        c4.value = ci[3]
        c4.font = font_bold
        c4.number_format = FMT_KR
        c4.alignment = align_right
        c4.border = border_thin_bottom

        ws2.cell(r_ci, 5).value = ci[4]
        ws2.cell(r_ci, 5).font = font_muted
        ws2.cell(r_ci, 5).border = border_thin_bottom

        ws2.row_dimensions[r_ci].height = 22
        r_ci += 1

    auto_fit_columns(ws2)

    # =========================================================================
    # 4. ARK: 3 Preskriptiv AI (Tiltak)
    # =========================================================================
    ws3 = wb.create_sheet(title="3 Preskriptiv AI (Tiltak)")
    add_banner(
        ws3,
        "3. Preskriptive AI-Kandidattiltak (Ollama LLM Agent)",
        "Generert tiltaksmeny · Vurdert opp mot Kommuneloven § 14-5, HTA § 4 og AML § 10-6",
        max_col=11
    )

    ws3.cell(4, 1).value = "AI-MODELLERT TILTAKSMENY (KANDIDATER T1 – T6)"
    ws3.cell(4, 1).font = font_section

    tiltak_headers = [
        "ID", "Tiltaksbeskrivelse", "Horisont", "Effektbase (kr)", "Sats %", "Sannsynlighet",
        "EOY-Effekt (kr)", "Tjenesterisiko", "HR/Tariff (HTA § 4)", "Governance Gate", "Anbefalt Neste Steg"
    ]
    r_t_h = 5
    for c, h in enumerate(tiltak_headers, 1):
        ws3.cell(r_t_h, c).value = h
    format_header_row(ws3, r_t_h, len(tiltak_headers))

    measures_catalog = [
        ("T1", "Oppfølging refusjoner og inntektskrav", "Kort", 732705.0, 0.08, 0.85, 41323.94, 0.05, 0.05, "KREVER FAGKONTROLL", "Avstem refusjonskrav mot NAV; regnskapsmessig sjekk før inndriving."),
        ("T2", "Redusere vikarbruk via intern dekning", "Kort", 612450.15, 0.10, 0.70, 28871.51, 0.15, 0.25, "KREVER HR/TARIFF", "Analyser turnus og intern ledig tid; drøft vikarstopp iht. HTA § 4."),
        ("T3", "Redusere overtid gjennom planlegging", "Kort", 1105443.81, 0.08, 0.75, 55076.63, 0.15, 0.25, "KREVER HR/TARIFF", "Gjennomgå overtidsårsaker og arbeidsplaner; sjekk AML § 10-6 og HMS."),
        ("T4", "Kontroll av ikke-kritiske kjøp", "Kort", 155776.0, 0.10, 0.90, 9519.84, 0.10, 0.05, "KREVER FAGKONTROLL", "Gjennomgå innkjøpslinjer og rammeavtaler; godkjenning av enhetsleder."),
        ("T5", "Turnus- og kapasitetsanalyse", "Lang", 4789478.56, 0.02, 0.60, 27473.74, 0.10, 0.25, "KREVER HR/TARIFF", "Omfattende bemanningsanalyse for 2025; partssamarbeid med tillitsvalgte."),
        ("T6", "Digital oppfølging og planprosess", "Lang", 17233691.0, 0.005, 0.60, 30701.07, 0.05, 0.05, "KREVER FAGKONTROLL", "Pilotere digital vaktbok og fraværsvarsling; gevinstrealiseringsplan.")
    ]

    r_t = r_t_h + 1
    for m in measures_catalog:
        ws3.cell(r_t, 1).value = m[0]
        ws3.cell(r_t, 1).font = font_bold
        ws3.cell(r_t, 1).alignment = align_center
        ws3.cell(r_t, 1).border = border_thin_bottom

        ws3.cell(r_t, 2).value = m[1]
        ws3.cell(r_t, 2).font = font_bold
        ws3.cell(r_t, 2).border = border_thin_bottom

        ws3.cell(r_t, 3).value = m[2]
        ws3.cell(r_t, 3).font = font_regular
        ws3.cell(r_t, 3).alignment = align_center
        ws3.cell(r_t, 3).border = border_thin_bottom

        c4 = ws3.cell(r_t, 4)
        c4.value = m[3]
        c4.font = font_regular
        c4.number_format = FMT_KR
        c4.alignment = align_right
        c4.border = border_thin_bottom

        c5 = ws3.cell(r_t, 5)
        c5.value = m[4]
        c5.font = font_regular
        c5.number_format = FMT_PCT
        c5.alignment = align_right
        c5.border = border_thin_bottom

        c6 = ws3.cell(r_t, 6)
        c6.value = m[5]
        c6.font = font_regular
        c6.number_format = FMT_PCT
        c6.alignment = align_right
        c6.border = border_thin_bottom

        c7 = ws3.cell(r_t, 7)
        c7.value = m[6]
        c7.font = font_bold
        c7.number_format = FMT_KR
        c7.alignment = align_right
        c7.border = border_thin_bottom

        c8 = ws3.cell(r_t, 8)
        c8.value = m[7]
        c8.font = font_regular
        c8.number_format = FMT_PCT
        c8.alignment = align_right
        c8.border = border_thin_bottom

        c9 = ws3.cell(r_t, 9)
        c9.value = m[8]
        c9.font = font_regular
        c9.number_format = FMT_PCT
        c9.alignment = align_right
        c9.border = border_thin_bottom

        c10 = ws3.cell(r_t, 10)
        c10.value = m[9]
        c10.font = font_bold
        c10.alignment = align_center
        c10.fill = fill_amb_badge if "TARIFF" in m[9] else fill_slate
        c10.border = border_thin_bottom

        c11 = ws3.cell(r_t, 11)
        c11.value = m[10]
        c11.font = font_muted
        c11.border = border_thin_bottom

        ws3.row_dimensions[r_t].height = 22
        r_t += 1

    # Total potensial
    ws3.cell(r_t, 2).value = "SAMLET TEORETISK KANDIDATPOTENSIAL (T1 – T6)"
    ws3.cell(r_t, 2).font = font_bold
    ws3.cell(r_t, 2).border = border_double_bottom

    c_sum = ws3.cell(r_t, 7)
    c_sum.value = "=SUM(G6:G11)"
    c_sum.font = font_bold
    c_sum.number_format = FMT_KR
    c_sum.alignment = align_right
    c_sum.border = border_double_bottom
    ws3.row_dimensions[r_t].height = 24

    auto_fit_columns(ws3)

    # =========================================================================
    # 5. ARK: 4 HITL Signoff & Governance (KJERNEELEMENT)
    # =========================================================================
    ws4 = wb.create_sheet(title="4 HITL Signoff & Governance")
    add_banner(
        ws4,
        "4. Human-in-the-Loop (HITL) Beslutningsgrensesnitt & Sign-off",
        "Formell Stage-Gate Kontroll iht. Kommuneloven § 14-5 & HTA § 4 · EU AI Act Art. 14 Human Oversight",
        max_col=12
    )

    ws4.cell(4, 1).value = "HITL STAGE-GATE REGELMOTOR & VEILEDNING"
    ws4.cell(4, 1).font = font_section

    ws4.cell(5, 1).value = (
        "1. Velg 'Beslutning' (Godkjent / Kandidat / Avvist) fra nedtrekkslisten i kolonne F.\n"
        "2. Bekreft 'Kontroll dokumentert' (Ja / Nei) i kolonne G. Krav: Fagkontroll, tariffdrøfting (HTA § 4) eller HMS må foreligge.\n"
        "3. Formel i kolonne H beregner godkjent effekt KUN dersom Beslutning = 'Godkjent' OG Kontroll = 'Ja': =IF(AND(F8=\"Godkjent\", G8=\"Ja\"), C8, 0)\n"
        "4. Før inn faglig begrunnelse, saksbehandlers navn og dato. Signert vedtak logges automatisk i revisjonssporet under."
    )
    ws4.cell(5, 1).font = font_muted
    ws4.row_dimensions[5].height = 50

    signoff_headers = [
        "ID", "Tiltaksbeskrivelse", "Beregnet EOY (kr)", "Konfidens %", "Governance Krav",
        "Beslutning", "Kontroll dokumentert", "Godkjent EOY-Effekt (kr)", "Faglig Begrunnelse / Kontrollnotat",
        "Godkjent Av", "Sign-off Dato", "Revisjonsstatus"
    ]

    r_s_h = 7
    for c, h in enumerate(signoff_headers, 1):
        ws4.cell(r_s_h, c).value = h
    format_header_row(ws4, r_s_h, len(signoff_headers))

    hitl_rows_data = [
        ("T1", "Oppfølging refusjoner og inntektskrav", 41323.94, 0.85, "KREVER FAGKONTROLL", "Godkjent", "Ja", "Avstemt mot NAV refusjonsportal; 41k bekreftet inngått.", "Frank Ellingsen", "2024-10-13"),
        ("T2", "Redusere vikarbruk via intern dekning", 28871.51, 0.70, "KREVER HR/TARIFF", "Godkjent", "Ja", "Drøftet med tillitsvalgt iht. HTA § 4; vikarstopp dagtid godkjent.", "Frank Ellingsen", "2024-10-13"),
        ("T3", "Redusere overtid gjennom planlegging", 55076.63, 0.75, "KREVER HR/TARIFF", "Kandidat", "Nei", "Turnusdrøfting pågår med vernetjenesten og tillitsvalgte.", "Frank Ellingsen", "2024-10-13"),
        ("T4", "Kontroll av ikke-kritiske kjøp", 9519.84, 0.90, "KREVER FAGKONTROLL", "Kandidat", "Nei", "Innkjøpsstopp krever godkjenning fra enhetsleder.", "Frank Ellingsen", "2024-10-13"),
        ("T5", "Turnus- og kapasitetsanalyse", 27473.74, 0.60, "KREVER HR/TARIFF", "Kandidat", "Nei", "Langsiktig omstilling; drøftes i partssammensatt utvalg.", "Frank Ellingsen", "2024-10-13"),
        ("T6", "Digital oppfølging og planprosess", 30701.07, 0.60, "KREVER FAGKONTROLL", "Kandidat", "Nei", "Planlagt test i 4. kvartal; avventer IKT-avklaring.", "Frank Ellingsen", "2024-10-13")
    ]

    r_hitl = r_s_h + 1
    for item in hitl_rows_data:
        # A: ID
        ws4.cell(r_hitl, 1).value = item[0]
        ws4.cell(r_hitl, 1).font = font_bold
        ws4.cell(r_hitl, 1).alignment = align_center
        ws4.cell(r_hitl, 1).border = border_thin_bottom

        # B: Tittel
        ws4.cell(r_hitl, 2).value = item[1]
        ws4.cell(r_hitl, 2).font = font_bold
        ws4.cell(r_hitl, 2).border = border_thin_bottom

        # C: Beregnet EOY
        c3 = ws4.cell(r_hitl, 3)
        c3.value = item[2]
        c3.font = font_regular
        c3.number_format = FMT_KR
        c3.alignment = align_right
        c3.border = border_thin_bottom

        # D: Konfidens
        c4 = ws4.cell(r_hitl, 4)
        c4.value = item[3]
        c4.font = font_regular
        c4.number_format = FMT_PCT
        c4.alignment = align_right
        c4.border = border_thin_bottom

        # E: Governance krav
        c5 = ws4.cell(r_hitl, 5)
        c5.value = item[4]
        c5.font = font_bold
        c5.alignment = align_center
        c5.fill = fill_amb_badge if "TARIFF" in item[4] else fill_slate
        c5.border = border_thin_bottom

        # F: Beslutning (Dropdown)
        c6 = ws4.cell(r_hitl, 6)
        c6.value = item[5]
        c6.font = font_bold
        c6.alignment = align_center
        c6.fill = fill_grn_badge if item[5] == "Godkjent" else (fill_red_badge if item[5] == "Avvist" else fill_amb_badge)
        c6.border = border_thin_bottom

        # G: Kontroll dokumentert (Dropdown)
        c7 = ws4.cell(r_hitl, 7)
        c7.value = item[6]
        c7.font = font_bold
        c7.alignment = align_center
        c7.fill = fill_grn_badge if item[6] == "Ja" else fill_red_badge
        c7.border = border_thin_bottom

        # H: Godkjent EOY-effekt (FORMEL)
        c8 = ws4.cell(r_hitl, 8)
        c8.value = f'=IF(AND(F{r_hitl}="Godkjent",G{r_hitl}="Ja"),C{r_hitl},0)'
        c8.font = font_bold
        c8.number_format = FMT_KR
        c8.alignment = align_right
        c8.fill = fill_grn_badge if (item[5] == "Godkjent" and item[6] == "Ja") else fill_slate
        c8.border = border_thin_bottom

        # I: Faglig Begrunnelse
        ws4.cell(r_hitl, 9).value = item[7]
        ws4.cell(r_hitl, 9).font = font_regular
        ws4.cell(r_hitl, 9).border = border_thin_bottom

        # J: Godkjent Av
        ws4.cell(r_hitl, 10).value = item[8]
        ws4.cell(r_hitl, 10).font = font_regular
        ws4.cell(r_hitl, 10).alignment = align_left
        ws4.cell(r_hitl, 10).border = border_thin_bottom

        # K: Sign-off Dato
        c11 = ws4.cell(r_hitl, 11)
        c11.value = item[9]
        c11.font = font_regular
        c11.alignment = align_center
        c11.border = border_thin_bottom

        # L: Revisjonsstatus (FORMEL)
        c12 = ws4.cell(r_hitl, 12)
        c12.value = f'=IF(AND(F{r_hitl}="Godkjent",G{r_hitl}="Ja"),"GYLDIG VEDTAK",IF(F{r_hitl}="Godkjent","MANGLER KONTROLL",IF(F{r_hitl}="Avvist","AVVIST","KANDIDAT")))'
        c12.font = font_bold
        c12.alignment = align_center
        c12.border = border_thin_bottom

        ws4.row_dimensions[r_hitl].height = 24
        r_hitl += 1

    # Data Validation (Dropdowns) for kolonne F og G
    dv_decision = DataValidation(type="list", formula1='"Godkjent,Kandidat,Avvist"', allow_blank=False)
    dv_decision.error = "Ugyldig valg. Velg Godkjent, Kandidat eller Avvist."
    dv_decision.errorTitle = "Feil i beslutningsstatus"
    ws4.add_data_validation(dv_decision)
    dv_decision.add(f"F8:F{r_hitl-1}")

    dv_control = DataValidation(type="list", formula1='"Ja,Nei"', allow_blank=False)
    dv_control.error = "Ugyldig valg. Velg Ja eller Nei."
    dv_control.errorTitle = "Feil i kontrollbekreftelse"
    ws4.add_data_validation(dv_control)
    dv_control.add(f"G8:G{r_hitl-1}")

    # Kontrolloppsummering
    r_sum = r_hitl + 1
    ws4.cell(r_sum, 1).value = "HITL KONTROLLOPPSUMMERING"
    ws4.cell(r_sum, 1).font = font_section

    kpi_hitl = [
        ("Totalt antall evaluerte AI-tiltak", '=COUNTA(A8:A13)', FMT_INT, "Samlet kandidatvolum"),
        ("Antall dokumenterte og godkjente tiltak", '=COUNTIFS(F8:F13,"Godkjent",G8:G13,"Ja")', FMT_INT, "Kvalifisert for regnskapsgodskriving"),
        ("Samlet godkjent EOY-effekt", '=SUM(H8:H13)', FMT_KR, "Fratrekkes i revidert prognose (Ark 5 og Ark 0)"),
        ("Gjenstående / Ikke-godkjent potensial", '=SUM(C8:C13)-H18', FMT_KR, "Krever ytterligere saksbehandling/avklaring")
    ]

    r_kpi_h = r_sum + 1
    for label, formel, fmt_str, note in kpi_hitl:
        ws4.cell(r_kpi_h, 1).value = label
        ws4.cell(r_kpi_h, 1).font = font_bold
        ws4.cell(r_kpi_h, 1).border = border_thin_bottom

        cell_v = ws4.cell(r_kpi_h, 8)
        cell_v.value = formel
        cell_v.font = font_bold
        cell_v.number_format = fmt_str
        cell_v.alignment = align_right
        cell_v.border = border_thin_bottom

        cell_n = ws4.cell(r_kpi_h, 9)
        cell_n.value = note
        cell_n.font = font_muted
        cell_n.border = border_thin_bottom

        ws4.row_dimensions[r_kpi_h].height = 20
        r_kpi_h += 1

    # Formell Signoff Erklæring (Certification Block)
    r_cert = r_kpi_h + 1
    ws4.cell(r_cert, 1).value = "FORMELL ATTESTASJON & GODKJENNINGSERKLÆRING"
    ws4.cell(r_cert, 1).font = font_section

    ws4.cell(r_cert + 1, 1).value = (
        "Undertegnede bekrefter herved at overnevnte tiltak er faglig vurdert og kvalitetssikret i henhold til "
        "Kommuneloven § 14-5, internkontrollforskriften og Hovedtariffavtalen (HTA) § 4. "
        "AI-modellens estimater er verifisert mot gjeldende turnusplaner og refusjonskrav."
    )
    ws4.cell(r_cert + 1, 1).font = font_muted
    ws4.row_dimensions[r_cert + 1].height = 28

    cert_fields = [
        ("Ansvarlig Controller / BI-spesialist:", "Frank Ellingsen", "Signert elektronisk", "2024-10-13"),
        ("Enhetsleder Bo og Miljø (Ansvar 5200):", "[Enhetsleder]", "Vurdering og drøfting gjennomført", "2024-10-13"),
        ("Kommunalsjef Helse og mestring:", "[Kommunalsjef]", "Orienteres i tertialsak T2", "2024-10-14")
    ]

    r_c_line = r_cert + 3
    for title_role, name_val, status_sign, dt_val in cert_fields:
        ws4.cell(r_c_line, 1).value = title_role
        ws4.cell(r_c_line, 1).font = font_bold

        ws4.cell(r_c_line, 3).value = name_val
        ws4.cell(r_c_line, 3).font = font_bold

        ws4.cell(r_c_line, 5).value = status_sign
        ws4.cell(r_c_line, 5).font = font_regular

        ws4.cell(r_c_line, 8).value = f"Dato: {dt_val}"
        ws4.cell(r_c_line, 8).font = font_muted

        ws4.row_dimensions[r_c_line].height = 20
        r_c_line += 1

    # Revisjonsspor (Audit Trail / EU AI Act Art. 14)
    r_audit = r_c_line + 2
    ws4.cell(r_audit, 1).value = "UUTSLETTELIG REVISJONSSPOR (AUDIT TRAIL · EU AI ACT ART. 14 / GDPR)"
    ws4.cell(r_audit, 1).font = font_section

    audit_headers = ["Action ID", "Tidsstempel (Lokal tid)", "Enhet", "AI-Modell", "Tiltak", "Effekt (kr)", "Konfidens", "Beslutning", "Kontroll", "Begrunnelse", "Saksbehandler"]
    r_aud_h = r_audit + 1
    for c, h in enumerate(audit_headers, 1):
        ws4.cell(r_aud_h, c).value = h
    format_header_row(ws4, r_aud_h, len(audit_headers))

    audit_data = [
        (101, "2024-10-13 08:30:15", "5200", "Ollama llama3.1", "T1", 41323.94, 0.85, "Godkjent", "Ja", "Avstemt mot NAV refusjonsportal; 41k bekreftet.", "Frank Ellingsen"),
        (102, "2024-10-13 08:35:42", "5200", "Ollama llama3.1", "T2", 28871.51, 0.70, "Godkjent", "Ja", "Drøftet med tillitsvalgt iht. HTA § 4; vikarstopp dagtid.", "Frank Ellingsen"),
        (103, "2024-10-13 08:38:10", "5200", "Ollama llama3.1", "T3", 55076.63, 0.75, "Kandidat", "Nei", "Turnusdrøfting pågår med vernetjenesten.", "Frank Ellingsen"),
        (104, "2024-10-13 08:40:05", "5200", "Ollama llama3.1", "T4", 9519.84, 0.90, "Kandidat", "Nei", "Innkjøpsstopp krever godkjenning fra enhetsleder.", "Frank Ellingsen"),
        (105, "2024-10-13 08:42:20", "5200", "Ollama llama3.1", "T5", 27473.74, 0.60, "Kandidat", "Nei", "Langsiktig analyse; drøftes i partssammensatt utvalg.", "Frank Ellingsen"),
        (106, "2024-10-13 08:44:55", "5200", "Ollama llama3.1", "T6", 30701.07, 0.60, "Kandidat", "Nei", "Planlagt pilotering i 4. kvartal; avventer IKT.", "Frank Ellingsen")
    ]

    r_aud = r_aud_h + 1
    for row in audit_data:
        ws4.cell(r_aud, 1).value = row[0]
        ws4.cell(r_aud, 1).alignment = align_center
        ws4.cell(r_aud, 1).font = font_regular
        ws4.cell(r_aud, 1).border = border_thin_bottom

        ws4.cell(r_aud, 2).value = row[1]
        ws4.cell(r_aud, 2).font = font_regular
        ws4.cell(r_aud, 2).border = border_thin_bottom

        ws4.cell(r_aud, 3).value = row[2]
        ws4.cell(r_aud, 3).alignment = align_center
        ws4.cell(r_aud, 3).font = font_regular
        ws4.cell(r_aud, 3).border = border_thin_bottom

        ws4.cell(r_aud, 4).value = row[3]
        ws4.cell(r_aud, 4).font = font_regular
        ws4.cell(r_aud, 4).border = border_thin_bottom

        ws4.cell(r_aud, 5).value = row[4]
        ws4.cell(r_aud, 5).alignment = align_center
        ws4.cell(r_aud, 5).font = font_bold
        ws4.cell(r_aud, 5).border = border_thin_bottom

        c6 = ws4.cell(r_aud, 6)
        c6.value = row[5]
        c6.font = font_regular
        c6.number_format = FMT_KR
        c6.alignment = align_right
        c6.border = border_thin_bottom

        c7 = ws4.cell(r_aud, 7)
        c7.value = row[6]
        c7.font = font_regular
        c7.number_format = FMT_PCT
        c7.alignment = align_right
        c7.border = border_thin_bottom

        c8 = ws4.cell(r_aud, 8)
        c8.value = row[7]
        c8.font = font_bold
        c8.alignment = align_center
        c8.fill = fill_grn_badge if row[7] == "Godkjent" else fill_amb_badge
        c8.border = border_thin_bottom

        c9 = ws4.cell(r_aud, 9)
        c9.value = row[8]
        c9.font = font_bold
        c9.alignment = align_center
        c9.fill = fill_grn_badge if row[8] == "Ja" else fill_red_badge
        c9.border = border_thin_bottom

        ws4.cell(r_aud, 10).value = row[9]
        ws4.cell(r_aud, 10).font = font_muted
        ws4.cell(r_aud, 10).border = border_thin_bottom

        ws4.cell(r_aud, 11).value = row[10]
        ws4.cell(r_aud, 11).font = font_regular
        ws4.cell(r_aud, 11).border = border_thin_bottom

        ws4.row_dimensions[r_aud].height = 20
        r_aud += 1

    auto_fit_columns(ws4)

    # =========================================================================
    # 6. ARK: 5 Revidert EOY & Ny Prognose
    # =========================================================================
    ws5 = wb.create_sheet(title="5 Revidert EOY & Ny Prognose")
    add_banner(
        ws5,
        "5. Revidert EOY-Prognose etter Dokumenterte Tiltak",
        "Dynamisk integrasjon mot HITL Sign-off · Scenarioanalyse og Tertialrapport til Kommunalsjef",
        max_col=8
    )

    ws5.cell(4, 1).value = "REVIDERT SLUTTPROGNOSE (GODKJENT SPOR)"
    ws5.cell(4, 1).font = font_section

    rev_headers = ["Styringsparameter", "Formel / Grunnlag", "Beløp (NOK)", "Avvik mot Budsjettert Ramme", "Signal / Status"]
    r_rev_h = 5
    for c, h in enumerate(rev_headers, 1):
        ws5.cell(r_rev_h, c).value = h
    format_header_row(ws5, r_rev_h, len(rev_headers))

    rev_rows = [
        ("Vedtatt Årsbudsjett (BAC)", "Bevilget årsramme for enheten", 17233691.0, 0.0, "Basis"),
        ("Ujustert EAC Sluttkostnad", "AI Sesongprognose før nye tiltak", 19050222.75, 1816531.75, "RØD (-10,5 %)"),
        ("Fratrekk: Dokumentert godkjent tiltakseffekt", "Dynamisk sum fra '4 HITL Signoff & Governance'", "='4 HITL Signoff & Governance'!H18", "=-C8/C6", "Godkjent HITL"),
        ("Revidert EAC Sluttkostnad", "Ujustert EAC (C7) minus godkjent effekt (C8)", "=C7-C8", "=C9-C6", "GUL / RØD"),
        ("Gjenstående restavvik mot årsbudsjett", "Revidert EAC (C9) minus årsbudsjett (C6)", "=C9-C6", "=C10/C6", "Rapporteringsplikt")
    ]

    r_rev = r_rev_h + 1
    for r_vals in rev_rows:
        ws5.cell(r_rev, 1).value = r_vals[0]
        ws5.cell(r_rev, 1).font = font_bold
        ws5.cell(r_rev, 1).border = border_thin_bottom

        ws5.cell(r_rev, 2).value = r_vals[1]
        ws5.cell(r_rev, 2).font = font_regular
        ws5.cell(r_rev, 2).border = border_thin_bottom

        c3 = ws5.cell(r_rev, 3)
        c3.value = r_vals[2]
        c3.font = font_bold
        c3.number_format = FMT_KR
        c3.alignment = align_right
        c3.border = border_thin_bottom

        c4 = ws5.cell(r_rev, 4)
        c4.value = r_vals[3]
        c4.font = font_bold
        c4.number_format = FMT_KR if isinstance(r_vals[3], float) else FMT_PCT
        c4.alignment = align_right
        c4.border = border_thin_bottom

        c5 = ws5.cell(r_rev, 5)
        c5.value = r_vals[4]
        c5.font = font_bold
        c5.alignment = align_center
        c5.fill = fill_grn_badge if "Godkjent" in r_vals[4] else (fill_red_badge if "RØD" in r_vals[4] else fill_slate)
        c5.border = border_thin_bottom

        ws5.row_dimensions[r_rev].height = 24
        r_rev += 1

    # Scenario-sammenligning
    ws5.cell(r_rev + 1, 1).value = "SCENARIO-SAMMENLIGNING: KANDIDAT-POTENSIAL VS. DOKUMENTERT EFFEKT"
    ws5.cell(r_rev + 1, 1).font = font_section

    scen_headers = ["Scenario", "Forutsetning", "Effekt fradrag", "Sluttkostnad (EAC)", "Restavvik", "Avvik %", "Signal"]
    r_sc_h = r_rev + 2
    for c, h in enumerate(scen_headers, 1):
        ws5.cell(r_sc_h, c).value = h
    format_header_row(ws5, r_sc_h, len(scen_headers))

    scenarios = [
        ("1. Grunnlinje (Null nye tiltak)", "Ujustert AI-sesongprognose videreføres", 0.0, 19050222.75, 1816531.75, -0.1054, "RØD"),
        ("2. Teoretisk Kandidat-scenario", "Dersom alle 6 kandidattiltak realiseres fullt ut", 192966.73, 18857256.02, 1623565.02, -0.0942, "GUL"),
        ("3. Dokumentert Godkjent Spor (Dagens vedtak)", "Kun tiltak med 'Godkjent' og 'Kontroll = Ja' godskrives", "='4 HITL Signoff & Governance'!H18", "=19050222.75-C16", "=D16-17233691", "=E16/17233691", "GUL / RØD")
    ]

    r_sc = r_sc_h + 1
    for sc in scenarios:
        ws5.cell(r_sc, 1).value = sc[0]
        ws5.cell(r_sc, 1).font = font_bold
        ws5.cell(r_sc, 1).border = border_thin_bottom

        ws5.cell(r_sc, 2).value = sc[1]
        ws5.cell(r_sc, 2).font = font_regular
        ws5.cell(r_sc, 2).border = border_thin_bottom

        c3 = ws5.cell(r_sc, 3)
        c3.value = sc[2]
        c3.font = font_regular
        c3.number_format = FMT_KR
        c3.alignment = align_right
        c3.border = border_thin_bottom

        c4 = ws5.cell(r_sc, 4)
        c4.value = sc[3]
        c4.font = font_bold
        c4.number_format = FMT_KR
        c4.alignment = align_right
        c4.border = border_thin_bottom

        c5 = ws5.cell(r_sc, 5)
        c5.value = sc[4]
        c5.font = font_bold
        c5.number_format = FMT_KR
        c5.alignment = align_right
        c5.border = border_thin_bottom

        c6 = ws5.cell(r_sc, 6)
        c6.value = sc[5]
        c6.font = font_bold
        c6.number_format = FMT_PCT
        c6.alignment = align_right
        c6.border = border_thin_bottom

        c7 = ws5.cell(r_sc, 7)
        c7.value = sc[6]
        c7.font = font_bold
        c7.alignment = align_center
        c7.fill = fill_red_badge if "RØD" in sc[6] else fill_amb_badge
        c7.border = border_thin_bottom

        ws5.row_dimensions[r_sc].height = 22
        r_sc += 1

    # Handlingsplan og Eskalering
    ws5.cell(r_sc + 1, 1).value = "ANBEFALTE STYRINGSHANDLINGER TIL KOMMUNALSJEF (TERTIALRAPPORTERING)"
    ws5.cell(r_sc + 1, 1).font = font_section

    actions_text = [
        "1. Prioritert refusjonsoppfølging (T1): Regnskapsavdelingen må forsere krav mot NAV; forventet innbetaling 41 324 kr i T3.",
        "2. Formell drøfting av vikarstopp (T2): Gjennomføre drøftingsmøte iht. HTA § 4 med tillitsvalgte for å sikre partssamarbeid.",
        "3. Turnusanalyse for overtid (T3): Avklare HMS-belastning og AML § 10-6 før overtidsreduksjon kan godkjennes.",
        "4. Varsel om restavvik: Restavviket på over 1,7 mill. kr overstiger delegert enhetsfullmakt og må tas inn i kommunens samlede tertialsak."
    ]

    r_act = r_sc + 2
    for act in actions_text:
        ws5.cell(r_act, 1).value = act
        ws5.cell(r_act, 1).font = font_regular
        ws5.row_dimensions[r_act].height = 20
        r_act += 1

    auto_fit_columns(ws5)

    # =========================================================================
    # 7. ARK: Data & Kontoplan (Grunnlagsdata)
    # =========================================================================
    ws6 = wb.create_sheet(title="Data & Kontoplan")
    add_banner(
        ws6,
        "Underliggende Transaksjons- og Periodedata · Bo og Miljø (2024)",
        "Bokførte data Jan–Aug · Periodisert budsjett Sep–Des | Enhet 5200 · KOSTRA 254",
        max_col=7
    )

    ws6.cell(4, 1).value = "MÅNEDLIG REGNSKAP, BUDSJETT OG AVVIK (TALL I KR)"
    ws6.cell(4, 1).font = font_section

    data_headers = ["Periode", "Måned", "Status", "Regnskap (kr)", "Budsjett (kr)", "Merforbruk (kr)", "Akkumulert Merforbruk (kr)"]
    r_d_h = 5
    for c, h in enumerate(data_headers, 1):
        ws6.cell(r_d_h, c).value = h
    format_header_row(ws6, r_d_h, len(data_headers))

    monthly_records = [
        ("2024-01", "Januar", "Bokført", 1014751.50, 1403337.0),
        ("2024-02", "Februar", "Bokført", 2082089.79, 1410893.0),
        ("2024-03", "Mars", "Bokført", 1541248.51, 1342381.0),
        ("2024-04", "April", "Bokført", 2256715.66, 2357359.0),
        ("2024-05", "Mai", "Bokført", 1613436.84, 1544215.0),
        ("2024-06", "Juni", "Bokført", 519336.23, 241681.0),
        ("2024-07", "Juli", "Bokført", 1837523.07, 1512209.0),
        ("2024-08", "August", "Bokført", 1757749.82, 1525162.0),
        ("2024-09", "September", "Gjenstående budsjett", 0.0, 1504399.0),
        ("2024-10", "Oktober", "Gjenstående budsjett", 0.0, 1418774.0),
        ("2024-11", "November", "Gjenstående budsjett", 0.0, 1418540.0),
        ("2024-12", "Desember", "Gjenstående budsjett", 0.0, 1554741.0)
    ]

    r_d = r_d_h + 1
    cum_avvik = 0.0
    for p, m, st_val, reg, bud in monthly_records:
        ws6.cell(r_d, 1).value = p
        ws6.cell(r_d, 1).alignment = align_center
        ws6.cell(r_d, 1).font = font_bold
        ws6.cell(r_d, 1).border = border_thin_bottom

        ws6.cell(r_d, 2).value = m
        ws6.cell(r_d, 2).font = font_regular
        ws6.cell(r_d, 2).border = border_thin_bottom

        ws6.cell(r_d, 3).value = st_val
        ws6.cell(r_d, 3).font = font_muted
        ws6.cell(r_d, 3).border = border_thin_bottom

        c4 = ws6.cell(r_d, 4)
        c4.value = reg
        c4.font = font_regular
        c4.number_format = FMT_KR
        c4.alignment = align_right
        c4.border = border_thin_bottom

        c5 = ws6.cell(r_d, 5)
        c5.value = bud
        c5.font = font_regular
        c5.number_format = FMT_KR
        c5.alignment = align_right
        c5.border = border_thin_bottom

        # Merforbruk (kr)
        c6 = ws6.cell(r_d, 6)
        if st_val == "Bokført":
            avvik = reg - bud
            cum_avvik += avvik
            c6.value = avvik
        else:
            c6.value = 0.0
        c6.font = font_bold
        c6.number_format = FMT_KR
        c6.alignment = align_right
        c6.border = border_thin_bottom

        # Akkumulert merforbruk
        c7 = ws6.cell(r_d, 7)
        c7.value = cum_avvik
        c7.font = font_bold
        c7.number_format = FMT_KR
        c7.alignment = align_right
        c7.border = border_thin_bottom

        ws6.row_dimensions[r_d].height = 20
        r_d += 1

    # Parameters & Terskler
    ws6.cell(r_d + 1, 1).value = "PARAMETERE & STYRINGSTERSKLER"
    ws6.cell(r_d + 1, 1).font = font_section

    param_headers = ["Parameter", "Verdi", "Beskrivelse / Tolkning"]
    r_p_h = r_d + 2
    for c, h in enumerate(param_headers, 1):
        ws6.cell(r_p_h, c).value = h
    format_header_row(ws6, r_p_h, len(param_headers))

    params_data = [
        ("Terskel for RØD status", 0.02, "Avvik over 2 % utløser rødt styringssignal og krav om saksfremlegg"),
        ("Terskel for GUL observasjon", 0.00, "Avvik mellom 0 % og 2 % krever skjerpet oppfølging"),
        ("Sjablong trendandel", 0.50, "Standard andel (50 %) av positivt YTD-avvik videreført i forenklet modell"),
        ("Deflator lønns- og prisvekst", 0.041, "Kristiansand kommunes standard deflatorsats (4,1 %) for 2024")
    ]

    r_p = r_p_h + 1
    for p_name, p_val, p_desc in params_data:
        ws6.cell(r_p, 1).value = p_name
        ws6.cell(r_p, 1).font = font_bold
        ws6.cell(r_p, 1).border = border_thin_bottom

        c2 = ws6.cell(r_p, 2)
        c2.value = p_val
        c2.font = font_bold
        c2.number_format = FMT_PCT
        c2.alignment = align_right
        c2.border = border_thin_bottom

        ws6.cell(r_p, 3).value = p_desc
        ws6.cell(r_p, 3).font = font_muted
        ws6.cell(r_p, 3).border = border_thin_bottom

        ws6.row_dimensions[r_p].height = 20
        r_p += 1

    auto_fit_columns(ws6)

    # Fjern default sheet hvis det finnes
    if default_sheet.title in wb.sheetnames:
        wb.remove(default_sheet)

    # Lagre workbook
    wb.save(TARGET_EXCEL)
    print(f"[OK] Ny fullverdig rapport generert: {TARGET_EXCEL}")
    print(f"     Antall ark: {len(wb.sheetnames)} -> {wb.sheetnames}")


if __name__ == "__main__":
    build_full_workbook()
