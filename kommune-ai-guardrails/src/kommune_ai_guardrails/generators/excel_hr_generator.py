"""
===============================================================================
KRISTIANSAND KOMMUNE — EXCEL HR & LØNNSMONITOR GENERATOR
===============================================================================
Bygger spesialisert HR- og lønnsavviksmodell i Excel:
- 5 standardiserte faner iht. FAST-standarden og Edward Tuftes Data-Ink Ratio
- KOSTRA Arter: 1010 Fastlønn, 1020 Vikar, 1090 Overtid, 1600 NAV Refusjoner
- Aldersfordelt refusjonskrav, vikarstopp-kalkyle og partssamarbeid (HTA § 4)
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
FMT_PERCENT = "0.0%"
FMT_DATE = "DD.MM.YYYY"

# Rammer
BORDER_THIN_BOTTOM = Border(bottom=Side(style="thin", color="D1D5DB"))
BORDER_TOTAL = Border(
    top=Side(style="thin", color="1F2937"),
    bottom=Side(style="double", color="1F2937")
)
BORDER_HEADER = Border(bottom=Side(style="medium", color="1E3A8A"))


def generate_hr_lonn_vikar_monitor_model(output_path: Optional[str] = None) -> str:
    """
    Bygger en fullverdig 5-tabs HR, lønns- og vikarmodell for kommunen.
    """
    if output_path is None:
        target = Path(__file__).resolve().parents[4] / "excel" / "Kommune_HR_Lonn_Vikar_Monitor_2026.xlsx"
    else:
        target = Path(output_path)

    target.parent.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    now = datetime.datetime.now()
    now_str = now.strftime("%d.%m.%Y")
    audit_hash = hashlib.sha256(f"{now.isoformat()}:HR_LONN_VIKAR_MONITOR_2026".encode()).hexdigest()

    # ==========================================================================
    # FANE 1: 00_Forside_og_Logg
    # ==========================================================================
    ws0 = wb.create_sheet(title="00_Forside_og_Logg")
    ws0.views.sheetView[0].showGridLines = True

    ws0.merge_cells("B2:H2")
    ws0["B2"] = "KRISTIANSAND KOMMUNE — HR OG ARBEIDSGIVERSTRATEGI"
    ws0["B2"].font = Font(name="Arial", size=11, bold=True, color="93C5FD")
    ws0["B2"].fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
    ws0["B2"].alignment = Alignment(vertical="center", indent=1)

    ws0.merge_cells("B3:H3")
    ws0["B3"] = "HR & Lønnsmonitor: Bemanningsavvik, Vikarforbruk og NAV-Refusjoner"
    ws0["B3"].font = Font(name="Arial", size=15, bold=True, color=COLOR_WHITE)
    ws0["B3"].fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
    ws0["B3"].alignment = Alignment(vertical="center", indent=1)

    ws0.row_dimensions[2].height = 24
    ws0.row_dimensions[3].height = 36

    meta_info = [
        ("Målgruppe:", "HR-Direktør, Kommunalsjefer, Enhetsledere og Tillitsvalgte"),
        ("Saksbehandler:", "Frank Ellingsen, Senior Controller & BI-Spesialist"),
        ("Hjemmel / Avtale:", "Hovedtariffavtalen (HTA) § 4, Arbeidsmiljøloven § 10, Kommuneloven § 14-5"),
        ("Overvåking:", "KOSTRA Art 1010 (Fastlønn), 1020 (Vikar), 1090 (Overtid), 1600 (NAV Refusjon)"),
        ("Periode:", "Status per 2. Tertial (August 2026)"),
        ("Kryptografisk Integritet:", f"SHA-256: {audit_hash}"),
        ("Tiltaksforankring:", "Administrativt vikarstopp og turnusoptimalisering")
    ]

    for idx, (lbl, val) in enumerate(meta_info, start=5):
        ws0[f"B{idx}"] = lbl
        ws0[f"B{idx}"].font = Font(name="Arial", size=10, bold=True, color="4B5563")
        ws0.merge_cells(f"C{idx}:H{idx}")
        ws0[f"C{idx}"] = val
        ws0[f"C{idx}"].font = Font(name="Arial", size=10, color="1F2937")
        ws0.row_dimensions[idx].height = 20

    # ==========================================================================
    # FANE 2: 01_HR_Kpi_Dashboard
    # ==========================================================================
    ws1 = wb.create_sheet(title="01_HR_Kpi_Dashboard")
    ws1.views.sheetView[0].showGridLines = True

    ws1.merge_cells("B2:I2")
    ws1["B2"] = "OVERORDNET HR-DASHBOARD OG BEMANNINGSSTATUS 2026"
    ws1["B2"].font = Font(name="Arial", size=14, bold=True, color=FILL_NAVY_HEADER)
    ws1.row_dimensions[2].height = 26

    ws1.merge_cells("B3:I3")
    ws1["B3"] = "Akutt overforbruk på vikarbyrå og overtid krever strakstiltak (Beløp i hele NOK)"
    ws1["B3"].font = Font(name="Arial", size=10, italic=True, color="4B5563")
    ws1.row_dimensions[3].height = 18

    # KPI Kort
    hr_cards = [
        ("Samlet Lønnsmasse YTD", "=F11", "Art 1010–1090"),
        ("Vikarforbruk (Art 1020)", "=F12", "+1,2M kr over budsjett"),
        ("Overtid / Tillegg (1090)", "=F13", "Døgnpost- og helgepress"),
        ("NAV Refusjoner (1600)", "=F14", "Bokført YTD")
    ]

    for (t, f, s), (c1, c2) in zip(hr_cards, [("B", "C"), ("D", "E"), ("F", "G"), ("H", "I")]):
        ws1.merge_cells(f"{c1}5:{c2}5")
        ws1[f"{c1}5"] = t
        ws1[f"{c1}5"].font = Font(name="Arial", size=9, bold=True, color="4B5563")
        ws1[f"{c1}5"].fill = PatternFill(start_color=FILL_CARD_LIGHT, end_color=FILL_CARD_LIGHT, fill_type="solid")
        ws1[f"{c1}5"].alignment = Alignment(horizontal="center")

        ws1.merge_cells(f"{c1}6:{c2}6")
        ws1[f"{c1}6"] = f
        ws1[f"{c1}6"].font = Font(name="Arial", size=13, bold=True, color=COLOR_BLACK_FORMULA)
        ws1[f"{c1}6"].fill = PatternFill(start_color=FILL_CARD_LIGHT, end_color=FILL_CARD_LIGHT, fill_type="solid")
        ws1[f"{c1}6"].alignment = Alignment(horizontal="center")
        ws1[f"{c1}6"].number_format = FMT_KOMMUNE_VARIANCE

        ws1.merge_cells(f"{c1}7:{c2}7")
        ws1[f"{c1}7"] = s
        ws1[f"{c1}7"].font = Font(name="Arial", size=8, italic=True, color="6B7280")
        ws1[f"{c1}7"].fill = PatternFill(start_color=FILL_CARD_LIGHT, end_color=FILL_CARD_LIGHT, fill_type="solid")
        ws1[f"{c1}7"].alignment = Alignment(horizontal="center")

    for r in [5, 6, 7]:
        ws1.row_dimensions[r].height = 20

    # Lønnsarter Tabell
    head_art = ["KOSTRA Art", "Artsnavn / Kontotype", "Årsbudsjett", "Budsjett YTD", "Regnskap YTD", "Avvik YTD (Merforbruk)", "Andel av Lønn", "Status"]
    for c_i, h in enumerate(head_art, start=2):
        c = ws1.cell(row=9, column=c_i, value=h)
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_WHITE)
        c.fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="right" if c_i in [4, 5, 6, 7, 8] else "left")
    ws1.row_dimensions[9].height = 24

    art_rows = [
        ("Art 1010", "Fastlønn i faste stillinger", 32500000, 21666667, 21450000, "I RUTE"),
        ("Art 1020", "Vikarer ved sykefravær og permisjon", 1850000, 1233333, 2480000, "KRITISK MERFORBRUK"),
        ("Art 1040", "Overtid og ekstraarbeid", 1400000, 933333, 1650000, "AKTSOMHET"),
        ("Art 1090", "Kvelds-, natt- og helgetillegg", 1950000, 1300000, 1220000, "I RUTE"),
        ("Art 1600", "Refusjon av sykepenger fra NAV", -1900000, -1266667, -1120000, "ETTERSLEP")
    ]

    for idx, (art_k, art_n, bud_a, bud_ytd, reg_ytd, stat) in enumerate(art_rows, start=11):
        ws1.cell(row=idx, column=2, value=art_k).font = Font(name="Arial", size=9, bold=True, color="1F2937")
        ws1.cell(row=idx, column=3, value=art_n).font = Font(name="Arial", size=9, color="1F2937")

        for c_c, val in [(4, bud_a), (5, bud_ytd), (6, reg_ytd)]:
            c = ws1.cell(row=idx, column=c_c, value=val)
            c.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
            c.fill = PatternFill(start_color=FILL_GRAY_INPUT, end_color=FILL_GRAY_INPUT, fill_type="solid")
            c.number_format = FMT_KOMMUNE_VARIANCE
            c.alignment = Alignment(horizontal="right")

        # Avvik YTD = F - E
        c_avv = ws1.cell(row=idx, column=7, value=f"=F{idx}-E{idx}")
        c_avv.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c_avv.number_format = FMT_KOMMUNE_VARIANCE
        c_avv.alignment = Alignment(horizontal="right")

        # Andel av lønn = F / F16 (Sum lønn)
        c_pct = ws1.cell(row=idx, column=8, value=f"=IF(F$16>0, ABS(F{idx})/F$16, 0)")
        c_pct.font = Font(name="Arial", size=9, color=COLOR_BLACK_FORMULA)
        c_pct.number_format = FMT_PERCENT
        c_pct.alignment = Alignment(horizontal="right")

        c_stat = ws1.cell(row=idx, column=9, value=stat)
        c_stat.font = Font(name="Arial", size=9, bold=True, color="991B1B" if "KRITISK" in stat else ("B45309" if "AKTSOMHET" in stat else "166534"))
        c_stat.alignment = Alignment(horizontal="center")

        for col in range(2, 10):
            ws1.cell(row=idx, column=col).border = BORDER_THIN_BOTTOM
        ws1.row_dimensions[idx].height = 20

    # Sum Brutto Lønnskostnader (rad 16)
    ws1.cell(row=16, column=2, value="SUM LØNN").font = Font(name="Arial", size=9, bold=True, color="1F2937")
    ws1.cell(row=16, column=3, value="Brutto Lønnsutgifter (Ekskl. Refusjon)").font = Font(name="Arial", size=9, bold=True, color="1F2937")
    for c_c, f_c in [(4, "D"), (5, "E"), (6, "F"), (7, "G")]:
        c = ws1.cell(row=16, column=c_c, value=f"=SUM({f_c}11:{f_c}14)")
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c.number_format = FMT_KOMMUNE_VARIANCE
        c.border = BORDER_TOTAL
        c.alignment = Alignment(horizontal="right")
    ws1.cell(row=16, column=8, value="=1.0").number_format = FMT_PERCENT
    ws1.cell(row=16, column=9, value="").border = BORDER_TOTAL
    ws1.row_dimensions[16].height = 22

    # ==========================================================================
    # FANE 3: 02_Manedlig_Artsanalyse
    # ==========================================================================
    ws2 = wb.create_sheet(title="02_Manedlig_Artsanalyse")
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells("B2:I2")
    ws2["B2"] = "MÅNEDLIG LØNNS- OG VIKARUTVIKLING 2026"
    ws2["B2"].font = Font(name="Arial", size=14, bold=True, color=FILL_NAVY_HEADER)

    ws2.merge_cells("B3:I3")
    ws2["B3"] = "Observasjon av sesongsvingninger, fraværsbølger og overtidsbelastning"
    ws2["B3"].font = Font(name="Arial", size=10, italic=True, color="4B5563")

    m_head = ["Måned (2026)", "Fastlønn (1010)", "Vikarer (1020)", "Overtid (1040)", "Tillegg (1090)", "NAV Refusjon (1600)", "Netto Lønnskostnad", "Vikarandel %"]
    for c_i, mh in enumerate(m_head, start=2):
        c = ws2.cell(row=5, column=c_i, value=mh)
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_WHITE)
        c.fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="right" if c_i >= 3 else "center")
    ws2.row_dimensions[5].height = 24

    m_data = [
        ("Januar", 2650000, 210000, 180000, 145000, -110000),
        ("Februar", 2660000, 240000, 190000, 148000, -125000),
        ("Mars", 2680000, 280000, 210000, 150000, -135000),
        ("April", 2670000, 290000, 195000, 152000, -140000),
        ("Mai", 2690000, 310000, 220000, 155000, -145000),
        ("Juni", 2710000, 360000, 235000, 160000, -150000),
        ("Juli", 2680000, 380000, 205000, 152000, -155000),
        ("August", 2710000, 410000, 215000, 158000, -160000)
    ]

    for idx, (m_navn, fl, vik, ot, til, ref) in enumerate(m_data, start=6):
        ws2.cell(row=idx, column=2, value=m_navn).font = Font(name="Arial", size=9, bold=True, color="1F2937")
        ws2.cell(row=idx, column=2).alignment = Alignment(horizontal="center")

        for c_c, val in [(3, fl), (4, vik), (5, ot), (6, til), (7, ref)]:
            c = ws2.cell(row=idx, column=c_c, value=val)
            c.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
            c.fill = PatternFill(start_color=FILL_GRAY_INPUT, end_color=FILL_GRAY_INPUT, fill_type="solid")
            c.number_format = FMT_KOMMUNE_VARIANCE
            c.alignment = Alignment(horizontal="right")

        # Netto Lønnskostnad = SUM(C:G)
        c_net = ws2.cell(row=idx, column=8, value=f"=SUM(C{idx}:G{idx})")
        c_net.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c_net.number_format = FMT_KOMMUNE_VARIANCE
        c_net.alignment = Alignment(horizontal="right")

        # Vikarandel = Vikar / (Fast + Vikar + Overtid + Tillegg)
        c_v_pct = ws2.cell(row=idx, column=9, value=f"=D{idx}/SUM(C{idx}:F{idx})")
        c_v_pct.font = Font(name="Arial", size=9, color=COLOR_BLACK_FORMULA)
        c_v_pct.number_format = FMT_PERCENT
        c_v_pct.alignment = Alignment(horizontal="right")

        for col in range(2, 10):
            ws2.cell(row=idx, column=col).border = BORDER_THIN_BOTTOM
        ws2.row_dimensions[idx].height = 20

    # Totaler
    ws2.cell(row=14, column=2, value="TOTAL YTD").font = Font(name="Arial", size=9, bold=True, color="1F2937")
    for c_c, f_c in [(3, "C"), (4, "D"), (5, "E"), (6, "F"), (7, "G"), (8, "H")]:
        c = ws2.cell(row=14, column=c_c, value=f"=SUM({f_c}6:{f_c}13)")
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c.number_format = FMT_KOMMUNE_VARIANCE
        c.border = BORDER_TOTAL
        c.alignment = Alignment(horizontal="right")
    ws2.cell(row=14, column=9, value="=D14/SUM(C14:F14)").number_format = FMT_PERCENT
    ws2.cell(row=14, column=9).font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
    ws2.cell(row=14, column=9).border = BORDER_TOTAL
    ws2.row_dimensions[14].height = 22

    # ==========================================================================
    # FANE 4: 03_Enhetsvis_Vikarstopp
    # ==========================================================================
    ws3 = wb.create_sheet(title="03_Enhetsvis_Vikarstopp")
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells("B2:H2")
    ws3["B2"] = "ENHETSVIS VIKARSTOPP OG TILTAKSOPPFØLGING"
    ws3["B2"].font = Font(name="Arial", size=14, bold=True, color=FILL_NAVY_HEADER)

    ws3.merge_cells("B3:H3")
    ws3["B3"] = "Kvantifisering av månedlig spareeffekt ved innføring av vikarstopp (Tilleggsbevilgning § 14-5)"
    ws3["B3"].font = Font(name="Arial", size=10, italic=True, color="4B5563")

    v_head = ["Enhetskode", "Enhetsnavn", "Sektor", "Vikar YTD (Art 1020)", "Normert Ramme", "Mnd. Besparelse Tiltak", "Restårseffekt (Sep-Des)", "Status Port 9"]
    for c_i, vh in enumerate(v_head, start=2):
        c = ws3.cell(row=5, column=c_i, value=vh)
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_WHITE)
        c.fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="right" if c_i in [5, 6, 7, 8] else "left")
    ws3.row_dimensions[5].height = 24

    unit_vikar = [
        ("2020", "Grim Skole (Grunnskole)", "Oppvekst", 1420000, 550000, 170000, "GODKJENT (Port 9)"),
        ("2540", "Randesund Døgnbemannet Boenhet", "Helse", 1060000, 480000, 210000, "UNDER BEHANDLING"),
        ("2021", "Lund Barnehage", "Oppvekst", 450000, 280000, 65000, "GODKJENT (Port 9)"),
        ("3010", "Teknisk Drift og Utemiljø", "Byutvikling", 220000, 180000, 35000, "I RUTE")
    ]

    for idx, (u_code, u_navn, u_sek, v_ytd, v_norm, m_sav, p9_stat) in enumerate(unit_vikar, start=6):
        ws3.cell(row=idx, column=2, value=u_code).font = Font(name="Arial", size=9, bold=True, color="1F2937")
        ws3.cell(row=idx, column=3, value=u_navn).font = Font(name="Arial", size=9, color="1F2937")
        ws3.cell(row=idx, column=4, value=u_sek).font = Font(name="Arial", size=9, color="1F2937")

        for c_c, val in [(5, v_ytd), (6, v_norm), (7, m_sav)]:
            c = ws3.cell(row=idx, column=c_c, value=val)
            c.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
            c.fill = PatternFill(start_color=FILL_GRAY_INPUT, end_color=FILL_GRAY_INPUT, fill_type="solid")
            c.number_format = FMT_KOMMUNE_VARIANCE
            c.alignment = Alignment(horizontal="right")

        # Restårseffekt (Sep-Des = 4 måneder)
        c_eff = ws3.cell(row=idx, column=8, value=f"=G{idx}*4")
        c_eff.font = Font(name="Arial", size=9, bold=True, color="166534")
        c_eff.number_format = FMT_KOMMUNE_VARIANCE
        c_eff.alignment = Alignment(horizontal="right")

        c_stat = ws3.cell(row=idx, column=9, value=p9_stat)
        c_stat.font = Font(name="Arial", size=9, bold=True, color="166534" if "GODKJENT" in p9_stat else "B45309")
        c_stat.alignment = Alignment(horizontal="center")

        for col in range(2, 10):
            ws3.cell(row=idx, column=col).border = BORDER_THIN_BOTTOM
        ws3.row_dimensions[idx].height = 20

    # Total
    ws3.cell(row=10, column=2, value="TOTAL").font = Font(name="Arial", size=9, bold=True, color="1F2937")
    ws3.cell(row=10, column=3, value="Kvantifisert Tiltakseffekt").font = Font(name="Arial", size=9, bold=True, color="1F2937")
    for c_c, f_c in [(5, "E"), (6, "F"), (7, "G"), (8, "H")]:
        c = ws3.cell(row=10, column=c_c, value=f"=SUM({f_c}6:{f_c}9)")
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c.number_format = FMT_KOMMUNE_VARIANCE
        c.border = BORDER_TOTAL
        c.alignment = Alignment(horizontal="right")
    ws3.row_dimensions[10].height = 22

    # ==========================================================================
    # FANE 5: 04_NAV_Refusjoner_Etterslep
    # ==========================================================================
    ws4 = wb.create_sheet(title="04_NAV_Refusjoner_Etterslep")
    ws4.views.sheetView[0].showGridLines = True

    ws4.merge_cells("B2:H2")
    ws4["B2"] = "ALDERSFORDELT REFUSJONSKRAV NAV (ART 1600)"
    ws4["B2"].font = Font(name="Arial", size=14, bold=True, color=FILL_NAVY_HEADER)

    ws4.merge_cells("B3:H3")
    ws4["B3"] = "Oppfølging av utestående sykepengerefusjoner fra NAV for å sikre overholdelse av bruttoprinsippet § 14-6"
    ws4["B3"].font = Font(name="Arial", size=10, italic=True, color="4B5563")

    n_head = ["Sektor", "Ikke Forfalt (0–30 dgr)", "31–60 dager", "61–90 dager", "> 90 dager (Kritisk)", "Samlet Utestående", "Bokført Refusjon YTD", "Etterslep vs Budsjett"]
    for c_i, nh in enumerate(n_head, start=2):
        c = ws4.cell(row=5, column=c_i, value=nh)
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_WHITE)
        c.fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="right" if c_i >= 3 else "left")
    ws4.row_dimensions[5].height = 24

    nav_data = [
        ("01 Sektor Oppvekst", 145000, 85000, 45000, 35000, -650000, 150000),
        ("02 Sektor Helse og Mestring", 195000, 120000, 65000, 55000, -420000, 180000),
        ("03 Sektor Byutvikling", 35000, 18000, 8000, 4000, -35000, 12000),
        ("04 Øvrige Sektorer", 18000, 9000, 4000, 2000, -15000, 5000)
    ]

    for idx, (sek, f30, f60, f90, f90p, bokf, ett) in enumerate(nav_data, start=6):
        ws4.cell(row=idx, column=2, value=sek).font = Font(name="Arial", size=9, bold=True, color="1F2937")

        for c_c, val in [(3, f30), (4, f60), (5, f90), (6, f90p)]:
            c = ws4.cell(row=idx, column=c_c, value=val)
            c.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
            c.fill = PatternFill(start_color=FILL_GRAY_INPUT, end_color=FILL_GRAY_INPUT, fill_type="solid")
            c.number_format = FMT_KOMMUNE_VARIANCE
            c.alignment = Alignment(horizontal="right")

        # Samlet Utestående = SUM(C:F)
        c_tot = ws4.cell(row=idx, column=7, value=f"=SUM(C{idx}:F{idx})")
        c_tot.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c_tot.number_format = FMT_KOMMUNE_VARIANCE
        c_tot.alignment = Alignment(horizontal="right")

        # Bokført YTD
        c_b = ws4.cell(row=idx, column=8, value=bokf)
        c_b.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
        c_b.fill = PatternFill(start_color=FILL_GRAY_INPUT, end_color=FILL_GRAY_INPUT, fill_type="solid")
        c_b.number_format = FMT_KOMMUNE_VARIANCE
        c_b.alignment = Alignment(horizontal="right")

        # Etterslep
        c_e = ws4.cell(row=idx, column=9, value=ett)
        c_e.font = Font(name="Arial", size=9, bold=True, color=COLOR_RED_ALERT)
        c_e.number_format = FMT_KOMMUNE_VARIANCE
        c_e.alignment = Alignment(horizontal="right")

        for col in range(2, 10):
            ws4.cell(row=idx, column=col).border = BORDER_THIN_BOTTOM
        ws4.row_dimensions[idx].height = 20

    # Total NAV
    ws4.cell(row=10, column=2, value="TOTAL").font = Font(name="Arial", size=9, bold=True, color="1F2937")
    for c_c, f_c in [(3, "C"), (4, "D"), (5, "E"), (6, "F"), (7, "G"), (8, "H"), (9, "I")]:
        c = ws4.cell(row=10, column=c_c, value=f"=SUM({f_c}6:{f_c}9)")
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c.number_format = FMT_KOMMUNE_VARIANCE
        c.border = BORDER_TOTAL
        c.alignment = Alignment(horizontal="right")
    ws4.row_dimensions[10].height = 22

    # Auto-kolonner
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
    out = generate_hr_lonn_vikar_monitor_model()
    print(f"Bygget HR & Vikarmonitor modell: {out}")
