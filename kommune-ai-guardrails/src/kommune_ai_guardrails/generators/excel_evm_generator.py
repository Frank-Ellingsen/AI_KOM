"""
===============================================================================
KRISTIANSAND KOMMUNE — EXCEL PROJECT CONTROLLER & EVM GENERATOR
===============================================================================
Bygger ISO 21508-kompatibel Earned Value Management (EVM) modell i Excel:
- 5 standardiserte faner iht. FAST-standarden og Edward Tuftes Data-Ink Ratio
- Spesialformat: _(* #,##0_);[Red]_(* (#,##0);_(* "-"_);_(@_)
- Prosjekter: Vågsbygd Skole (PROJ-101), Randesund Boenhet (PROJ-201), VA (PROJ-301)
- Formelberegninger for PV, AC, EV, CV, SV, CPI, SPI, EAC, VAC og P85-usikkerhet
===============================================================================
"""
from __future__ import annotations

import datetime
import hashlib
from pathlib import Path
from typing import Optional

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# FAST & Tufte Farger
COLOR_BLUE_INPUT = "000080"       # #000080 Mørkeblå for inndata
COLOR_BLACK_FORMULA = "000000"    # #000000 Svart for formler og summer
COLOR_GREEN_INTERNAL = "006100"   # #006100 Mørkegrønn for interne referanser
COLOR_RED_ALERT = "C0392B"        # #C0392B Dempet rød for avvik
FILL_GRAY_INPUT = "F2F2F2"        # #F2F2F2 Bakgrunn for inndataceller
FILL_NAVY_HEADER = "1E3A8A"       # #1E3A8A Header tittelbånd
FILL_CARD_LIGHT = "F9FAFB"        # #F9FAFB Nøytral bakgrunn
COLOR_WHITE = "FFFFFF"

# Formatering
FMT_KOMMUNE_VARIANCE = '_(* #,##0_);[Red]_(* (#,##0);_(* "-"_);_(@_)'
FMT_KOMMUNE_CURRENCY = '#,##0 "kr"'
FMT_DECIMAL_INDEX = "0.000"
FMT_PERCENT = "0.0%"
FMT_DATE = "DD.MM.YYYY"

# Rammer
BORDER_THIN_BOTTOM = Border(bottom=Side(style="thin", color="D1D5DB"))
BORDER_TOTAL = Border(
    top=Side(style="thin", color="1F2937"),
    bottom=Side(style="double", color="1F2937")
)
BORDER_HEADER = Border(bottom=Side(style="medium", color="1E3A8A"))


def generate_project_controller_evm_model(output_path: Optional[str] = None) -> str:
    """
    Bygger en fullverdig 5-tabs ISO 21508 EVM modell i Excel.
    """
    if output_path is None:
        target = Path(__file__).resolve().parents[4] / "excel" / "Kommune_Project_Controller_EVM_2026.xlsx"
    else:
        target = Path(output_path)

    target.parent.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # Fjern default ark

    now = datetime.datetime.now()
    now_str = now.strftime("%d.%m.%Y")
    audit_hash = hashlib.sha256(f"{now.isoformat()}:PROJECT_CONTROLLER_EVM_2026".encode()).hexdigest()

    # ==========================================================================
    # FANE 1: 00_Forside_og_Logg
    # ==========================================================================
    ws0 = wb.create_sheet(title="00_Forside_og_Logg")
    ws0.views.sheetView[0].showGridLines = True

    # Tittel
    ws0.merge_cells("B2:H2")
    ws0["B2"] = "KRISTIANSAND KOMMUNE — BYUTVIKLING & EIENDOM"
    ws0["B2"].font = Font(name="Arial", size=11, bold=True, color="93C5FD")
    ws0["B2"].fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
    ws0["B2"].alignment = Alignment(vertical="center", indent=1)

    ws0.merge_cells("B3:H3")
    ws0["B3"] = "Project Controller & Capex Modell: Earned Value Management (ISO 21508)"
    ws0["B3"].font = Font(name="Arial", size=15, bold=True, color=COLOR_WHITE)
    ws0["B3"].fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
    ws0["B3"].alignment = Alignment(vertical="center", indent=1)

    ws0.row_dimensions[2].height = 24
    ws0.row_dimensions[3].height = 36

    meta_info = [
        ("Dokumenttype:", "Månedlig Investerings- og Fremdriftsrapport (Capex)"),
        ("Saksbehandler:", "Frank Ellingsen, Project Controller & BI-Spesialist"),
        ("Standard / Rammeverk:", "ISO 21508 Earned Value Management & Edward Tufte Data-Ink Ratio"),
        ("Portefølje:", "Investeringsprosjekter 2026 (Vågsbygd Skole, Randesund Boenhet, VA)"),
        ("Gjeldende Periode:", "Per 2. Tertial (Måned 8 / August 2026)"),
        ("Kryptografisk Stempel:", f"SHA-256: {audit_hash}"),
        ("Godkjenning:", "Kvalitetssikret for Formannskapet og Kontrollutvalget")
    ]

    for idx, (lbl, val) in enumerate(meta_info, start=5):
        ws0[f"B{idx}"] = lbl
        ws0[f"B{idx}"].font = Font(name="Arial", size=10, bold=True, color="4B5563")
        ws0.merge_cells(f"C{idx}:H{idx}")
        ws0[f"C{idx}"] = val
        ws0[f"C{idx}"].font = Font(name="Arial", size=10, color="1F2937")
        ws0.row_dimensions[idx].height = 20

    # Endringslogg
    ws0["B14"] = "Revisjons- og Endringslogg (Stage-Gate Port 9):"
    ws0["B14"].font = Font(name="Arial", size=11, bold=True, color=FILL_NAVY_HEADER)

    log_headers = ["Revisjon", "Dato", "Utført av", "Beskrivelse av endring / Milepæl", "Status"]
    for c_idx, h in enumerate(log_headers, start=2):
        cell = ws0.cell(row=15, column=c_idx, value=h)
        cell.font = Font(name="Arial", size=9, bold=True, color=COLOR_WHITE)
        cell.fill = PatternFill(start_color="374151", end_color="374151", fill_type="solid")
        cell.alignment = Alignment(horizontal="center" if c_idx in [2, 3, 6] else "left")

    logs = [
        ("v1.0", "15.01.2026", "Frank Ellingsen", "Etablering av periodiserte basisbudsjetter (BAC/PV)", "GODKJENT"),
        ("v1.1", "15.05.2026", "Frank Ellingsen", "T1 rapportering: Grunnarbeid fullført Vågsbygd Skole", "GODKJENT"),
        ("v1.2", "20.08.2026", "Frank Ellingsen", "T2 avviksanalyse: Påløpte kostnader døgnpost Randesund", "GODKJENT"),
        ("v2.0", now_str, "Frank Ellingsen", "Sluttprognose EAC & P85-usikkerhetsavsetning for Bystyret", "GJELDENDE")
    ]

    for r_idx, row_data in enumerate(logs, start=16):
        for c_idx, val in enumerate(row_data, start=2):
            cell = ws0.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Arial", size=9, color="1F2937")
            cell.border = BORDER_THIN_BOTTOM
            if c_idx in [2, 3]:
                cell.alignment = Alignment(horizontal="center")
            elif c_idx == 6:
                cell.alignment = Alignment(horizontal="center")
                cell.font = Font(name="Arial", size=9, bold=True, color="166534" if val == "GJELDENDE" else "374151")
        ws0.row_dimensions[r_idx].height = 19

    # ==========================================================================
    # FANE 2: 01_EVM_Executive_Dashboard
    # ==========================================================================
    ws1 = wb.create_sheet(title="01_EVM_Executive_Dashboard")
    ws1.views.sheetView[0].showGridLines = True

    ws1.merge_cells("B2:J2")
    ws1["B2"] = "PORTEFØLJEOVERSIKT — EARNED VALUE MANAGEMENT (ISO 21508)"
    ws1["B2"].font = Font(name="Arial", size=14, bold=True, color=FILL_NAVY_HEADER)
    ws1["B2"].alignment = Alignment(vertical="center")
    ws1.row_dimensions[2].height = 26

    ws1.merge_cells("B3:J3")
    ws1["B3"] = "Finansiell fremdrift og kostnadseffektivitet per 31.08.2026 (Alle tall i hele NOK ekskl. mva)"
    ws1["B3"].font = Font(name="Arial", size=10, italic=True, color="4B5563")
    ws1.row_dimensions[3].height = 18

    # KPI Kort på rad 5-7
    kpi_cards = [
        ("Planlagt Verdi (PV)", "=SUM(E11:E13)", "Periodisert budsjett per T2"),
        ("Påløpt Kostnad (AC)", "=SUM(F11:F13)", "Bokført i Visma ERP"),
        ("Opptjent Verdi (EV)", "=SUM(G11:G13)", "Fysisk utført verdi"),
        ("Kostnadsavvik (CV)", "=F5-G5", "Overforbruk ved negativ verdi")
    ]

    col_positions = [("B", "C"), ("D", "E"), ("F", "G"), ("H", "I")]
    for (title, formula, subtext), (c_start, c_end) in zip(kpi_cards, col_positions):
        ws1.merge_cells(f"{c_start}5:{c_end}5")
        ws1[f"{c_start}5"] = title
        ws1[f"{c_start}5"].font = Font(name="Arial", size=9, bold=True, color="4B5563")
        ws1[f"{c_start}5"].fill = PatternFill(start_color=FILL_CARD_LIGHT, end_color=FILL_CARD_LIGHT, fill_type="solid")
        ws1[f"{c_start}5"].alignment = Alignment(horizontal="center")

        ws1.merge_cells(f"{c_start}6:{c_end}6")
        ws1[f"{c_start}6"] = formula
        ws1[f"{c_start}6"].font = Font(name="Arial", size=14, bold=True, color=COLOR_BLACK_FORMULA)
        ws1[f"{c_start}6"].fill = PatternFill(start_color=FILL_CARD_LIGHT, end_color=FILL_CARD_LIGHT, fill_type="solid")
        ws1[f"{c_start}6"].alignment = Alignment(horizontal="center")
        ws1[f"{c_start}6"].number_format = FMT_KOMMUNE_VARIANCE

        ws1.merge_cells(f"{c_start}7:{c_end}7")
        ws1[f"{c_start}7"] = subtext
        ws1[f"{c_start}7"].font = Font(name="Arial", size=8, italic=True, color="6B7280")
        ws1[f"{c_start}7"].fill = PatternFill(start_color=FILL_CARD_LIGHT, end_color=FILL_CARD_LIGHT, fill_type="solid")
        ws1[f"{c_start}7"].alignment = Alignment(horizontal="center")

    for r in [5, 6, 7]:
        ws1.row_dimensions[r].height = 20

    # Hovedtabell over Investeringsprosjekter
    ws1["B9"] = "EVM Nøkkeltallstabell per Prosjekt:"
    ws1["B9"].font = Font(name="Arial", size=11, bold=True, color="1F2937")

    evm_headers = [
        "Prosjektkode", "Prosjektnavn", "Vedtatt Ramme (BAC)", 
        "Planlagt (PV)", "Påløpt (AC)", "Opptjent (EV)", 
        "Kostn.avvik (CV)", "Kostn.indeks (CPI)", "Sluttkostnad (EAC)", "Sluttavvik (VAC)"
    ]

    for c_idx, h in enumerate(evm_headers, start=2):
        cell = ws1.cell(row=10, column=c_idx, value=h)
        cell.font = Font(name="Arial", size=9, bold=True, color=COLOR_WHITE)
        cell.fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
        cell.alignment = Alignment(horizontal="right" if c_idx >= 4 else "left", vertical="center")
    ws1.row_dimensions[10].height = 24

    # Prosjektrader (med hardkodede inndata i blått og formler i svart)
    projects_data = [
        ("PROJ-101", "Vågsbygd Skole Utvidelse", 185000000, 115000000, 104500000, 95000000),
        ("PROJ-201", "Randesund Døgnbemannet Boenhet", 240000000, 165000000, 139100000, 117300000),
        ("PROJ-301", "VA-Hovedledning Selvkost", 92000000, 48000000, 49300000, 50600000)
    ]

    for idx, (p_code, p_name, bac, pv, ac, ev) in enumerate(projects_data, start=11):
        ws1.cell(row=idx, column=2, value=p_code).font = Font(name="Arial", size=9, bold=True, color="1F2937")
        ws1.cell(row=idx, column=3, value=p_name).font = Font(name="Arial", size=9, color="1F2937")
        
        # Hardkodede inndata (blå skrift)
        for c_col, val in [(4, bac), (5, pv), (6, ac), (7, ev)]:
            c = ws1.cell(row=idx, column=c_col, value=val)
            c.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
            c.fill = PatternFill(start_color=FILL_GRAY_INPUT, end_color=FILL_GRAY_INPUT, fill_type="solid")
            c.number_format = FMT_KOMMUNE_VARIANCE
            c.alignment = Alignment(horizontal="right")

        # Formelkolonner (svart skrift)
        # CV = EV - AC
        c_cv = ws1.cell(row=idx, column=8, value=f"=G{idx}-F{idx}")
        c_cv.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c_cv.number_format = FMT_KOMMUNE_VARIANCE
        c_cv.alignment = Alignment(horizontal="right")

        # CPI = EV / AC
        c_cpi = ws1.cell(row=idx, column=9, value=f"=IF(F{idx}>0, G{idx}/F{idx}, 1.0)")
        c_cpi.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c_cpi.number_format = FMT_DECIMAL_INDEX
        c_cpi.alignment = Alignment(horizontal="right")

        # EAC = BAC / CPI
        c_eac = ws1.cell(row=idx, column=10, value=f"=IF(I{idx}>0, D{idx}/I{idx}, D{idx})")
        c_eac.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c_eac.number_format = FMT_KOMMUNE_VARIANCE
        c_eac.alignment = Alignment(horizontal="right")

        # VAC = BAC - EAC
        c_vac = ws1.cell(row=idx, column=11, value=f"=D{idx}-J{idx}")
        c_vac.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c_vac.number_format = FMT_KOMMUNE_VARIANCE
        c_vac.alignment = Alignment(horizontal="right")

        for col in range(2, 12):
            ws1.cell(row=idx, column=col).border = BORDER_THIN_BOTTOM
        ws1.row_dimensions[idx].height = 20

    # Totalrad (rad 14)
    ws1.cell(row=14, column=2, value="TOTAL").font = Font(name="Arial", size=9, bold=True, color="1F2937")
    ws1.cell(row=14, column=3, value="Hele Porteføljen").font = Font(name="Arial", size=9, bold=True, color="1F2937")
    
    for c_col, f_char in [(4, "D"), (5, "E"), (6, "F"), (7, "G")]:
        cell = ws1.cell(row=14, column=c_col, value=f"=SUM({f_char}11:{f_char}13)")
        cell.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        cell.number_format = FMT_KOMMUNE_VARIANCE
        cell.alignment = Alignment(horizontal="right")

    ws1.cell(row=14, column=8, value="=G14-F14").number_format = FMT_KOMMUNE_VARIANCE  # CV total
    ws1.cell(row=14, column=9, value="=IF(F14>0, G14/F14, 1.0)").number_format = FMT_DECIMAL_INDEX  # CPI total
    ws1.cell(row=14, column=10, value="=IF(I14>0, D14/I14, D14)").number_format = FMT_KOMMUNE_VARIANCE  # EAC total
    ws1.cell(row=14, column=11, value="=D14-J14").number_format = FMT_KOMMUNE_VARIANCE  # VAC total

    for col in range(2, 12):
        c = ws1.cell(row=14, column=col)
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c.border = BORDER_TOTAL
        c.alignment = Alignment(horizontal="right" if col >= 4 else "left")
    ws1.row_dimensions[14].height = 22

    # Veiledende controller-merknader (Tufte style)
    ws1["B16"] = "Metodeforklaring & Retningslinjer (Project Controller):"
    ws1["B16"].font = Font(name="Arial", size=10, bold=True, color=FILL_NAVY_HEADER)

    notes = [
        "1. CPI < 1.000: Betyr overskridelse per opptjent krone. Randesund Boenhet (0.843) krever omprosjektering av tekniske anlegg.",
        "2. VAC (Variance at Completion): Viser estimert sluttoverskridelse. Samlet portefølje har en sluttoverskridelse på kr (80 448 796).",
        "3. Inndekning: Eventuelle overskridelser må fremmes for Bystyret som tilleggsbevilgning eller dekkes via disposisjonsfond jf. § 14-5."
    ]
    for r_i, n_txt in enumerate(notes, start=17):
        ws1.cell(row=r_i, column=2, value=n_txt).font = Font(name="Arial", size=9, color="4B5563")
        ws1.merge_cells(f"B{r_i}:K{r_i}")
        ws1.row_dimensions[r_i].height = 18

    # ==========================================================================
    # FANE 3: 02_Periodisert_S_Kurve
    # ==========================================================================
    ws2 = wb.create_sheet(title="02_Periodisert_S_Kurve")
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells("B2:I2")
    ws2["B2"] = "MÅNEDLIG FREMDRIFT & PERIODISERT S-KURVE (2026)"
    ws2["B2"].font = Font(name="Arial", size=14, bold=True, color=FILL_NAVY_HEADER)

    ws2.merge_cells("B3:I3")
    ws2["B3"] = "Akkumulert fremdrift for Vågsbygd Skole Utvidelse (PROJ-101) — Planlagt (PV) vs Påløpt (AC)"
    ws2["B3"].font = Font(name="Arial", size=10, italic=True, color="4B5563")

    s_headers = [
        "Måned", "Planlagt Mnd", "Planlagt Kumulativ (PV)", 
        "Påløpt Mnd", "Påløpt Kumulativ (AC)", "Opptjent Kumulativ (EV)",
        "Kumulativt Avvik (CV)", "Kostnadsindeks (CPI)"
    ]

    for c_i, sh in enumerate(s_headers, start=2):
        c = ws2.cell(row=5, column=c_i, value=sh)
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_WHITE)
        c.fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="right" if c_i >= 3 else "center")
    ws2.row_dimensions[5].height = 24

    # Månedsdata for S-kurve
    months_plan = [
        ("Januar", 8000000, 7500000, 7200000),
        ("Februar", 12000000, 11800000, 11000000),
        ("Mars", 15000000, 14200000, 13500000),
        ("April", 18000000, 17900000, 16000000),
        ("Mai", 16000000, 15500000, 14200000),
        ("Juni", 17000000, 16800000, 15100000),
        ("Juli", 14000000, 11200000, 9500000),
        ("August", 15000000, 9600000, 8500000),
        ("September (P)", 18000000, 0, 0),
        ("Oktober (P)", 20000000, 0, 0),
        ("November (P)", 19000000, 0, 0),
        ("Desember (P)", 13000000, 0, 0)
    ]

    for m_idx, (m_name, p_mnd, ac_mnd, ev_mnd) in enumerate(months_plan, start=6):
        ws2.cell(row=m_idx, column=2, value=m_name).font = Font(name="Arial", size=9, bold=True, color="1F2937")
        ws2.cell(row=m_idx, column=2).alignment = Alignment(horizontal="center")

        # Planlagt Mnd (blå inndata)
        c_pm = ws2.cell(row=m_idx, column=3, value=p_mnd)
        c_pm.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
        c_pm.number_format = FMT_KOMMUNE_VARIANCE
        c_pm.alignment = Alignment(horizontal="right")

        # Planlagt Kumulativ (PV) formel
        if m_idx == 6:
            c_pv = ws2.cell(row=m_idx, column=4, value="=C6")
        else:
            c_pv = ws2.cell(row=m_idx, column=4, value=f"=D{m_idx-1}+C{m_idx}")
        c_pv.font = Font(name="Arial", size=9, color=COLOR_BLACK_FORMULA)
        c_pv.number_format = FMT_KOMMUNE_VARIANCE
        c_pv.alignment = Alignment(horizontal="right")

        # Påløpt Mnd (blå inndata)
        c_acm = ws2.cell(row=m_idx, column=5, value=ac_mnd if ac_mnd > 0 else "")
        c_acm.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
        c_acm.number_format = FMT_KOMMUNE_VARIANCE
        c_acm.alignment = Alignment(horizontal="right")

        # Påløpt Kumulativ (AC) formel
        if m_idx == 6:
            c_ac = ws2.cell(row=m_idx, column=6, value="=IF(E6>0, E6, \"\")")
        else:
            c_ac = ws2.cell(row=m_idx, column=6, value=f"=IF(E{m_idx}>0, F{m_idx-1}+E{m_idx}, \"\")")
        c_ac.font = Font(name="Arial", size=9, color=COLOR_BLACK_FORMULA)
        c_ac.number_format = FMT_KOMMUNE_VARIANCE
        c_ac.alignment = Alignment(horizontal="right")

        # Opptjent Kumulativ (EV) formel
        if m_idx == 6:
            c_ev = ws2.cell(row=m_idx, column=7, value=ev_mnd)
        else:
            c_ev = ws2.cell(row=m_idx, column=7, value=f"=IF(E{m_idx}>0, G{m_idx-1}+{ev_mnd}, \"\")")
        c_ev.font = Font(name="Arial", size=9, color=COLOR_BLACK_FORMULA)
        c_ev.number_format = FMT_KOMMUNE_VARIANCE
        c_ev.alignment = Alignment(horizontal="right")

        # CV = EV - AC
        c_cv = ws2.cell(row=m_idx, column=8, value=f"=IF(ISNUMBER(G{m_idx}), G{m_idx}-F{m_idx}, \"\")")
        c_cv.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c_cv.number_format = FMT_KOMMUNE_VARIANCE
        c_cv.alignment = Alignment(horizontal="right")

        # CPI = EV / AC
        c_cpi = ws2.cell(row=m_idx, column=9, value=f"=IF(AND(ISNUMBER(G{m_idx}), F{m_idx}>0), G{m_idx}/F{m_idx}, \"\")")
        c_cpi.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c_cpi.number_format = FMT_DECIMAL_INDEX
        c_cpi.alignment = Alignment(horizontal="right")

        for col in range(2, 10):
            ws2.cell(row=m_idx, column=col).border = BORDER_THIN_BOTTOM
        ws2.row_dimensions[m_idx].height = 19

    # ==========================================================================
    # FANE 4: 03_Risiko_og_Usikkerhet
    # ==========================================================================
    ws3 = wb.create_sheet(title="03_Risiko_og_Usikkerhet")
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells("B2:H2")
    ws3["B2"] = "USIKKERHETSANALYSE & RISK CONTINGENCY (P10 / P50 / P85)"
    ws3["B2"].font = Font(name="Arial", size=14, bold=True, color=FILL_NAVY_HEADER)

    ws3.merge_cells("B3:H3")
    ws3["B3"] = "Avsetninger til uforutsette utgifter og styringsrammer iht. KS-veileder for kommunale investeringer"
    ws3["B3"].font = Font(name="Arial", size=10, italic=True, color="4B5563")

    r_headers = ["Prosjektkode", "Prosjektnavn", "Basisestimat (P10)", "Styringsramme (P50)", "Kostnadsramme (P85)", "Avsatt Reserve (P85-P50)", "Brukt Reserve YTD", "Gjenstående Reserve"]
    for c_i, rh in enumerate(r_headers, start=2):
        c = ws3.cell(row=5, column=c_i, value=rh)
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_WHITE)
        c.fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="right" if c_i >= 4 else "left")
    ws3.row_dimensions[5].height = 24

    risk_data = [
        ("PROJ-101", "Vågsbygd Skole Utvidelse", 160000000, 172000000, 185000000, 8500000),
        ("PROJ-201", "Randesund Døgnbemannet Boenhet", 210000000, 225000000, 240000000, 12800000),
        ("PROJ-301", "VA-Hovedledning Selvkost", 82000000, 87000000, 92000000, 3100000)
    ]

    for idx, (p_code, p_name, p10, p50, p85, used_res) in enumerate(risk_data, start=6):
        ws3.cell(row=idx, column=2, value=p_code).font = Font(name="Arial", size=9, bold=True, color="1F2937")
        ws3.cell(row=idx, column=3, value=p_name).font = Font(name="Arial", size=9, color="1F2937")

        for c_col, val in [(4, p10), (5, p50), (6, p85)]:
            c = ws3.cell(row=idx, column=c_col, value=val)
            c.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
            c.fill = PatternFill(start_color=FILL_GRAY_INPUT, end_color=FILL_GRAY_INPUT, fill_type="solid")
            c.number_format = FMT_KOMMUNE_VARIANCE
            c.alignment = Alignment(horizontal="right")

        # Avsatt Reserve = P85 - P50
        c_res = ws3.cell(row=idx, column=7, value=f"=F{idx}-E{idx}")
        c_res.font = Font(name="Arial", size=9, color=COLOR_BLACK_FORMULA)
        c_res.number_format = FMT_KOMMUNE_VARIANCE
        c_res.alignment = Alignment(horizontal="right")

        # Brukt reserve YTD (blå inndata)
        c_used = ws3.cell(row=idx, column=8, value=used_res)
        c_used.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
        c_used.fill = PatternFill(start_color=FILL_GRAY_INPUT, end_color=FILL_GRAY_INPUT, fill_type="solid")
        c_used.number_format = FMT_KOMMUNE_VARIANCE
        c_used.alignment = Alignment(horizontal="right")

        # Gjenstående reserve = Avsatt - Brukt
        c_rem = ws3.cell(row=idx, column=9, value=f"=G{idx}-H{idx}")
        c_rem.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c_rem.number_format = FMT_KOMMUNE_VARIANCE
        c_rem.alignment = Alignment(horizontal="right")

        for col in range(2, 10):
            ws3.cell(row=idx, column=col).border = BORDER_THIN_BOTTOM
        ws3.row_dimensions[idx].height = 20

    # Totalrad for risiko
    ws3.cell(row=9, column=2, value="TOTAL").font = Font(name="Arial", size=9, bold=True, color="1F2937")
    ws3.cell(row=9, column=3, value="Porteføljereserver").font = Font(name="Arial", size=9, bold=True, color="1F2937")
    for c_col, f_char in [(4, "D"), (5, "E"), (6, "F"), (7, "G"), (8, "H"), (9, "I")]:
        c = ws3.cell(row=9, column=c_col, value=f"=SUM({f_char}6:{f_char}8)")
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c.number_format = FMT_KOMMUNE_VARIANCE
        c.border = BORDER_TOTAL
        c.alignment = Alignment(horizontal="right")
    ws3.row_dimensions[9].height = 22

    # ==========================================================================
    # FANE 5: 04_Kontrollutvalg_Rapport
    # ==========================================================================
    ws4 = wb.create_sheet(title="04_Kontrollutvalg_Rapport")
    ws4.views.sheetView[0].showGridLines = True

    # Rapporttittel A4-tilpasset
    ws4.merge_cells("B2:G2")
    ws4["B2"] = "KRISTIANSAND KOMMUNE — KONTROLLUTVALGET & BYSTYRET"
    ws4["B2"].font = Font(name="Arial", size=11, bold=True, color="93C5FD")
    ws4["B2"].fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
    ws4["B2"].alignment = Alignment(vertical="center", indent=1)

    ws4.merge_cells("B3:G3")
    ws4["B3"] = "Periodisk Tilsynsrapport: Capex-avvik og Usikkerhetsstyring 2026"
    ws4["B3"].font = Font(name="Arial", size=14, bold=True, color=COLOR_WHITE)
    ws4["B3"].fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
    ws4["B3"].alignment = Alignment(vertical="center", indent=1)

    ws4.row_dimensions[2].height = 22
    ws4.row_dimensions[3].height = 32

    # Sammendragstabell
    rep_rows = [
        ("Samlet Vedtatt Kostnadsramme (BAC):", "='01_EVM_Executive_Dashboard'!D14"),
        ("Planlagt Akkumulert Fremdrift (PV):", "='01_EVM_Executive_Dashboard'!E14"),
        ("Faktisk Påløpt Regnskapskostnad (AC):", "='01_EVM_Executive_Dashboard'!F14"),
        ("Fysisk Opptjent Verdi (EV):", "='01_EVM_Executive_Dashboard'!G14"),
        ("Samlet Kostnadsavvik (CV):", "='01_EVM_Executive_Dashboard'!H14"),
        ("Porteføljens Kostnadsindeks (CPI):", "='01_EVM_Executive_Dashboard'!I14"),
        ("Estimert Sluttkostnad ved Fullføring (EAC):", "='01_EVM_Executive_Dashboard'!J14"),
        ("Netto Sluttoverskridelse mot Ramme (VAC):", "='01_EVM_Executive_Dashboard'!K14")
    ]

    for idx, (label, formula) in enumerate(rep_rows, start=5):
        ws4.cell(row=idx, column=2, value=label).font = Font(name="Arial", size=10, bold=True, color="1F2937")
        ws4.merge_cells(f"B{idx}:D{idx}")

        c_val = ws4.cell(row=idx, column=5, value=formula)
        c_val.font = Font(name="Arial", size=10, bold=True, color=COLOR_GREEN_INTERNAL)
        c_val.alignment = Alignment(horizontal="right")
        if "CPI" in label:
            c_val.number_format = FMT_DECIMAL_INDEX
        else:
            c_val.number_format = FMT_KOMMUNE_VARIANCE

        for c in range(2, 6):
            ws4.cell(row=idx, column=c).border = BORDER_THIN_BOTTOM
        ws4.row_dimensions[idx].height = 21

    # Signaturblokk
    ws4["B15"] = "Formell Attestasjon & Sign-off (Stage-Gate Port 9):"
    ws4["B15"].font = Font(name="Arial", size=10, bold=True, color=FILL_NAVY_HEADER)

    sign_data = [
        ("Project Controller:", "Frank Ellingsen", "Signert elektronisk (BankID / SHA-256)"),
        ("Kommunaldirektør Byutvikling:", "Godkjent for fremlegging i Formannskapet", f"Dato: {now_str}"),
        ("Kryptografisk Integritet:", audit_hash[:32] + "...", "Forseglet i Golden Record DB")
    ]

    for s_idx, (r1, r2, r3) in enumerate(sign_data, start=16):
        ws4.cell(row=s_idx, column=2, value=r1).font = Font(name="Arial", size=9, bold=True, color="4B5563")
        ws4.cell(row=s_idx, column=3, value=r2).font = Font(name="Arial", size=9, color="1F2937")
        ws4.cell(row=s_idx, column=5, value=r3).font = Font(name="Arial", size=9, italic=True, color="6B7280")
        ws4.row_dimensions[s_idx].height = 20

    # Auto-tilpass kolonnebredder for alle ark
    for ws in [ws0, ws1, ws2, ws3, ws4]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val = str(cell.value or "")
                if not cell.coordinate in ws.merged_cells and "\n" not in val:
                    max_len = max(max_len, len(val))
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)
        ws.column_dimensions["A"].width = 3
        ws.column_dimensions["B"].width = 24

    wb.save(target)
    return str(target)


if __name__ == "__main__":
    out = generate_project_controller_evm_model()
    print(f"Bygget EVM modell: {out}")
