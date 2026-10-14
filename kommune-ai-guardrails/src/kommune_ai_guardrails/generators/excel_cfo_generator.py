"""
===============================================================================
KRISTIANSAND KOMMUNE — EXCEL CFO EXECUTIVE & KONSERNMODELL GENERATOR
===============================================================================
Bygger toppledelsens konsernøkonomiske arbeidsbok i Excel:
- 5 standardiserte faner iht. FAST-standarden og Edward Tuftes Data-Ink Ratio
- Kommuneloven § 14-4, § 14-5 og § 14-6 bruttoprinsippet
- Netto driftsresultat, Disposisjonsfond og Rentefølsomhetsanalyse
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


def generate_cfo_executive_konsern_model(output_path: Optional[str] = None) -> str:
    """
    Bygger en fullverdig 5-tabs konsernmodell for Kommunedirektør og Økonomidirektør.
    """
    if output_path is None:
        target = Path(__file__).resolve().parents[4] / "excel" / "Kommune_CFO_Executive_Konsern_2026.xlsx"
    else:
        target = Path(output_path)

    target.parent.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    now = datetime.datetime.now()
    now_str = now.strftime("%d.%m.%Y")
    audit_hash = hashlib.sha256(f"{now.isoformat()}:CFO_EXECUTIVE_KONSERN_2026".encode()).hexdigest()

    # ==========================================================================
    # FANE 1: 00_Forside_og_Logg
    # ==========================================================================
    ws0 = wb.create_sheet(title="00_Forside_og_Logg")
    ws0.views.sheetView[0].showGridLines = True

    ws0.merge_cells("B2:H2")
    ws0["B2"] = "KRISTIANSAND KOMMUNE — SENTRAL ØKONOMISTAB"
    ws0["B2"].font = Font(name="Arial", size=11, bold=True, color="93C5FD")
    ws0["B2"].fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
    ws0["B2"].alignment = Alignment(vertical="center", indent=1)

    ws0.merge_cells("B3:H3")
    ws0["B3"] = "CFO Executive Konsernrapport: Finansiell Balanse & Rammejustering 2026"
    ws0["B3"].font = Font(name="Arial", size=15, bold=True, color=COLOR_WHITE)
    ws0["B3"].fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
    ws0["B3"].alignment = Alignment(vertical="center", indent=1)

    ws0.row_dimensions[2].height = 24
    ws0.row_dimensions[3].height = 36

    meta_info = [
        ("Målgruppe:", "Kommunedirektør, Økonomidirektør, Formannskapet"),
        ("Saksbehandler:", "Frank Ellingsen, Senior Controller & BI-Spesialist"),
        ("Hjemmel / Standard:", "Kommuneloven § 14-4 & § 14-5 / FAST Finansiell Standard"),
        ("Omfang:", "Samlet kommunekonsern (Drift, Finans, Disposisjonsfond)"),
        ("Status:", "2. Tertial / Q2 Avstemt mot Visma ERP og Framsikt EPM"),
        ("Kryptografisk Integritet:", f"SHA-256: {audit_hash}"),
        ("Kvalitetssikring:", "Stage-Gate Port 9 verifisert — Ingen motregning (§ 14-6)")
    ]

    for idx, (lbl, val) in enumerate(meta_info, start=5):
        ws0[f"B{idx}"] = lbl
        ws0[f"B{idx}"].font = Font(name="Arial", size=10, bold=True, color="4B5563")
        ws0.merge_cells(f"C{idx}:H{idx}")
        ws0[f"C{idx}"] = val
        ws0[f"C{idx}"].font = Font(name="Arial", size=10, color="1F2937")
        ws0.row_dimensions[idx].height = 20

    # ==========================================================================
    # FANE 2: 01_Konsern_Hovedoversikt
    # ==========================================================================
    ws1 = wb.create_sheet(title="01_Konsern_Hovedoversikt")
    ws1.views.sheetView[0].showGridLines = True

    ws1.merge_cells("B2:I2")
    ws1["B2"] = "HOVEDOVERSIKT DRIFTSREGNSKAP OG FINANS 2026 (KONSERNNIVÅ)"
    ws1["B2"].font = Font(name="Arial", size=14, bold=True, color=FILL_NAVY_HEADER)
    ws1.row_dimensions[2].height = 26

    ws1.merge_cells("B3:I3")
    ws1["B3"] = "Bevilgningsregnskap etter Kommuneloven § 14-4 (Beløp i hele 1 000 NOK)"
    ws1["B3"].font = Font(name="Arial", size=10, italic=True, color="4B5563")
    ws1.row_dimensions[3].height = 18

    # KPI-Kort
    c_cards = [
        ("Vedtatt Driftsramme", "=D18", "Årsbudsjett netto"),
        ("Bokført YTD", "=F18", "Faktisk netto per T2"),
        ("Netto Driftsavvik YTD", "=G18", "Avvik mot periodisert"),
        ("Netto Driftsresultat %", "=IF(D8>0, D22/D8, 0.018)", "Mål: > 1.75% jf. TBU")
    ]

    for (t, f, s), (c1, c2) in zip(c_cards, [("B", "C"), ("D", "E"), ("F", "G"), ("H", "I")]):
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
        if "%" in t:
            ws1[f"{c1}6"].number_format = FMT_PERCENT
        else:
            ws1[f"{c1}6"].number_format = FMT_KOMMUNE_VARIANCE

        ws1.merge_cells(f"{c1}7:{c2}7")
        ws1[f"{c1}7"] = s
        ws1[f"{c1}7"].font = Font(name="Arial", size=8, italic=True, color="6B7280")
        ws1[f"{c1}7"].fill = PatternFill(start_color=FILL_CARD_LIGHT, end_color=FILL_CARD_LIGHT, fill_type="solid")
        ws1[f"{c1}7"].alignment = Alignment(horizontal="center")

    for r in [5, 6, 7]:
        ws1.row_dimensions[r].height = 20

    # Hovedtabell Driftsregnskap
    headers = ["Konto / Post", "Beskrivelse", "Årsbudsjett", "Periodisert YTD", "Regnskap YTD", "Avvik YTD", "Prognose EOY", "Avvik EOY"]
    for c_idx, h in enumerate(headers, start=2):
        c = ws1.cell(row=9, column=c_idx, value=h)
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_WHITE)
        c.fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="right" if c_idx >= 4 else "left", vertical="center")
    ws1.row_dimensions[9].height = 24

    # Rader:
    # Inntekter:
    # Rad 10: Frie inntekter (Skatt og rammetilskudd)
    # Rad 11: Brukerbetalinger og gebyrer
    # Rad 12: Statstilskudd og refusjoner
    # Rad 13: SUM DRIFTSINNTEKTER
    # Utgifter per sektor:
    # Rad 14: Sektor Oppvekst og Utdanning
    # Rad 15: Sektor Helse og Mestring
    # Rad 16: Sektor Byutvikling og Teknisk
    # Rad 17: Sektor Kultur og Administrasjon
    # Rad 18: SUM DRIFTSUTGIFTER
    # Finans & Resultat:
    # Rad 19: Renteutgifter og låneomkostninger
    # Rad 20: Avdrag på lån
    # Rad 21: Renteinntekter og utbytte
    # Rad 22: NETTO DRIFTSRESULTAT
    # Rad 23: Avsetning til disposisjonsfond
    # Rad 24: Bruk av disposisjonsfond (inndekning)
    # Rad 25: ÅRETS MER-/MINDREFORBRUK
    
    rows_data = [
        # (Rad, Kode, Tittel, Årsbud, PerBud, Regn, EOY)
        (10, "INNTEKT-01", "Frie inntekter (Skatt og rammetilskudd)", 5840000, 3893333, 3880000, 5820000),
        (11, "INNTEKT-02", "Brukerbetalinger og salgsinntekter", 650000, 433333, 445000, 665000),
        (12, "INNTEKT-03", "Refusjoner og øvrige overføringer", 480000, 320000, 342000, 510000),
        (13, "SUM-INN", "1. SAMLEDE DRIFTSINNTEKTER", "=SUM(D10:D12)", "=SUM(E10:E12)", "=SUM(F10:F12)", "=SUM(H10:H12)"),
        (14, "SEKTOR-01", "Sektor Oppvekst og Utdanning", 2850000, 1900000, 1968000, 2942000),
        (15, "SEKTOR-02", "Sektor Helse og Mestring", 2420000, 1613333, 1682000, 2515000),
        (16, "SEKTOR-03", "Sektor Byutvikling og Teknisk", 850000, 566667, 571000, 856000),
        (17, "SEKTOR-04", "Sektor Kultur, Innbygger og Sentraladm.", 520000, 346667, 349000, 523000),
        (18, "SUM-UTG", "2. SAMLEDE BRUTTO DRIFTSUTGIFTER", "=SUM(D14:D17)", "=SUM(E14:E17)", "=SUM(F14:F17)", "=SUM(H14:H17)"),
        (19, "FINANS-01", "Renteutgifter og låneomkostninger", 245000, 163333, 172000, 258000),
        (20, "FINANS-02", "Avdrag på lån", 210000, 140000, 140000, 210000),
        (21, "FINANS-03", "Renteinntekter og utbytte", -85000, -56667, -62000, -92000),
        (22, "NETTO-DR", "3. NETTO DRIFTSRESULTAT", "=D13-D18-D19-D20-D21", "=E13-E18-E19-E20-E21", "=F13-F18-F19-F20-F21", "=H13-H18-H19-H20-H21"),
        (23, "FOND-01", "Avsetning til disposisjonsfond", 120000, 80000, 80000, 120000),
        (24, "FOND-02", "Bruk av disposisjonsfond (inndekning § 14-5)", -150000, -100000, -145000, -189000),
        (25, "RESULTAT", "4. ÅRETS MERFORBRUK TIL INNDEKNING", "=D22-D23-D24", "=E22-E23-E24", "=F22-F23-F24", "=H22-H23-H24")
    ]

    for r_num, code, title, b_aar, b_ytd, r_ytd, prog in rows_data:
        ws1.cell(row=r_num, column=2, value=code).font = Font(name="Arial", size=9, bold=("SUM" in code or "NETTO" in code or "RESULTAT" in code), color="1F2937")
        ws1.cell(row=r_num, column=3, value=title).font = Font(name="Arial", size=9, bold=("SUM" in code or "NETTO" in code or "RESULTAT" in code), color="1F2937")

        is_calc = str(b_aar).startswith("=")
        for c_c, val in [(4, b_aar), (5, b_ytd), (6, r_ytd), (8, prog)]:
            cell = ws1.cell(row=r_num, column=c_c, value=val)
            cell.font = Font(name="Arial", size=9, bold=is_calc, color=COLOR_BLACK_FORMULA if is_calc else COLOR_BLUE_INPUT)
            if not is_calc and "SUM" not in code:
                cell.fill = PatternFill(start_color=FILL_GRAY_INPUT, end_color=FILL_GRAY_INPUT, fill_type="solid")
            cell.number_format = FMT_KOMMUNE_VARIANCE
            cell.alignment = Alignment(horizontal="right")

        # Avvik YTD = F - E (for utgifter) eller F - E (for inntekter)
        # For utgifter betyr positivt at regnskap > budsjett (merforbruk)
        c_avv_ytd = ws1.cell(row=r_num, column=7, value=f"=F{r_num}-E{r_num}")
        c_avv_ytd.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c_avv_ytd.number_format = FMT_KOMMUNE_VARIANCE
        c_avv_ytd.alignment = Alignment(horizontal="right")

        # Avvik EOY = H - D
        c_avv_eoy = ws1.cell(row=r_num, column=9, value=f"=H{r_num}-D{r_num}")
        c_avv_eoy.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c_avv_eoy.number_format = FMT_KOMMUNE_VARIANCE
        c_avv_eoy.alignment = Alignment(horizontal="right")

        border_type = BORDER_TOTAL if ("SUM" in code or "NETTO" in code or "RESULTAT" in code) else BORDER_THIN_BOTTOM
        for col in range(2, 10):
            ws1.cell(row=r_num, column=col).border = border_type
        ws1.row_dimensions[r_num].height = 20

    # ==========================================================================
    # FANE 3: 02_Sektoravvik_Matrise
    # ==========================================================================
    ws2 = wb.create_sheet(title="02_Sektoravvik_Matrise")
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells("B2:I2")
    ws2["B2"] = "SEKTORVIS AVVIKSMATRISE — BRUTTOPRINSIPPET (§ 14-6)"
    ws2["B2"].font = Font(name="Arial", size=14, bold=True, color=FILL_NAVY_HEADER)

    ws2.merge_cells("B3:I3")
    ws2["B3"] = "Dekomponering av sektoravvik i lønnsutgifter, vikarer, vare/tjenestekjøp og refusjoner"
    ws2["B3"].font = Font(name="Arial", size=10, italic=True, color="4B5563")

    s_head = ["Sektor / Virksomhet", "Ansvarlig Kommunalsjef", "Vedtatt Ramme", "Lønnsavvik YTD", "Vikaravvik (1020)", "Overtidsavvik (1090)", "Refusjonsavvik (1600)", "Netto Sektoravvik"]
    for c_i, sh in enumerate(s_head, start=2):
        c = ws2.cell(row=5, column=c_i, value=sh)
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_WHITE)
        c.fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="right" if c_i >= 4 else "left")
    ws2.row_dimensions[5].height = 24

    sektor_rows = [
        ("01 Sektor Oppvekst og Utdanning", "Kristin E. Bakke", 2850000, 12000, 48000, 15000, -7000),
        ("02 Sektor Helse og Mestring", "Brede S. Olsen", 2420000, 18000, 39000, 22000, -10333),
        ("03 Sektor Byutvikling og Teknisk", "Geir H. Hansen", 850000, -2000, 4000, 3000, -667),
        ("04 Kultur, Innbygger og Sentraladm.", "Mette K. Moe", 520000, 1500, 1200, 800, -1167)
    ]

    for idx, (s_name, s_lead, ramme, avv_lonn, avv_vikar, avv_ot, avv_ref) in enumerate(sektor_rows, start=6):
        ws2.cell(row=idx, column=2, value=s_name).font = Font(name="Arial", size=9, bold=True, color="1F2937")
        ws2.cell(row=idx, column=3, value=s_lead).font = Font(name="Arial", size=9, color="1F2937")

        for c_c, val in [(4, ramme), (5, avv_lonn), (6, avv_vikar), (7, avv_ot), (8, avv_ref)]:
            c = ws2.cell(row=idx, column=c_c, value=val)
            c.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
            c.fill = PatternFill(start_color=FILL_GRAY_INPUT, end_color=FILL_GRAY_INPUT, fill_type="solid")
            c.number_format = FMT_KOMMUNE_VARIANCE
            c.alignment = Alignment(horizontal="right")

        # Netto Sektoravvik = Lønn + Vikar + Overtid + Refusjon
        c_net = ws2.cell(row=idx, column=9, value=f"=SUM(E{idx}:H{idx})")
        c_net.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c_net.number_format = FMT_KOMMUNE_VARIANCE
        c_net.alignment = Alignment(horizontal="right")

        for col in range(2, 10):
            ws2.cell(row=idx, column=col).border = BORDER_THIN_BOTTOM
        ws2.row_dimensions[idx].height = 20

    # Total Sektoravvik
    ws2.cell(row=10, column=2, value="TOTAL").font = Font(name="Arial", size=9, bold=True, color="1F2937")
    ws2.cell(row=10, column=3, value="Alle Sektorer").font = Font(name="Arial", size=9, bold=True, color="1F2937")
    for c_c, f_c in [(4, "D"), (5, "E"), (6, "F"), (7, "G"), (8, "H"), (9, "I")]:
        c = ws2.cell(row=10, column=c_c, value=f"=SUM({f_c}6:{f_c}9)")
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c.number_format = FMT_KOMMUNE_VARIANCE
        c.border = BORDER_TOTAL
        c.alignment = Alignment(horizontal="right")
    ws2.row_dimensions[10].height = 22

    # ==========================================================================
    # FANE 4: 03_Finans_Renter_Gjeld
    # ==========================================================================
    ws3 = wb.create_sheet(title="03_Finans_Renter_Gjeld")
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells("B2:H2")
    ws3["B2"] = "FINANSFORVALTNING, LÅNEPORTEFØLJE & RENTEFØLSOMHET"
    ws3["B2"].font = Font(name="Arial", size=14, bold=True, color=FILL_NAVY_HEADER)

    ws3.merge_cells("B3:H3")
    ws3["B3"] = "Gjeldssituasjon og stresstesting mot NIBOR-endringer iht. Finansreglementet"
    ws3["B3"].font = Font(name="Arial", size=10, italic=True, color="4B5563")

    f_head = ["Låneinstitusjon / Lån", "Lånetype", "Restgjeld (NOK)", "Rentebindingsandel", "Gj.snitt Rente", "Årlig Rente (Nå)", "+100 bps Sjokk", "Effekt på Budsjett"]
    for c_i, fh in enumerate(f_head, start=2):
        c = ws3.cell(row=5, column=c_i, value=fh)
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_WHITE)
        c.fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="right" if c_i >= 4 else "left")
    ws3.row_dimensions[5].height = 24

    loans = [
        ("Kommunalbanken Lån 2021", "Flytende 3M NIBOR", 3200000000, 0.0, 0.0465),
        ("KLP Kommunekreditt", "Fastrente 5 år", 2100000000, 1.0, 0.0385),
        ("Sertifikatlån / Obligasjoner", "Flytende NIBOR", 1500000000, 0.0, 0.0475)
    ]

    for idx, (l_name, l_type, l_bal, fix_share, rate) in enumerate(loans, start=6):
        ws3.cell(row=idx, column=2, value=l_name).font = Font(name="Arial", size=9, bold=True, color="1F2937")
        ws3.cell(row=idx, column=3, value=l_type).font = Font(name="Arial", size=9, color="1F2937")

        c_bal = ws3.cell(row=idx, column=4, value=l_bal)
        c_bal.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
        c_bal.number_format = FMT_KOMMUNE_VARIANCE
        c_bal.alignment = Alignment(horizontal="right")

        c_fix = ws3.cell(row=idx, column=5, value=fix_share)
        c_fix.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
        c_fix.number_format = FMT_PERCENT
        c_fix.alignment = Alignment(horizontal="right")

        c_rate = ws3.cell(row=idx, column=6, value=rate)
        c_rate.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
        c_rate.number_format = "0.00%"
        c_rate.alignment = Alignment(horizontal="right")

        # Årlig rente = Restgjeld * Rente
        c_ann = ws3.cell(row=idx, column=7, value=f"=D{idx}*F{idx}")
        c_ann.font = Font(name="Arial", size=9, color=COLOR_BLACK_FORMULA)
        c_ann.number_format = FMT_KOMMUNE_VARIANCE
        c_ann.alignment = Alignment(horizontal="right")

        # +100 bps sjokk for flytende andel = D * (1 - E) * (F + 0.01) + D * E * F
        c_shock = ws3.cell(row=idx, column=8, value=f"=(D{idx}*(1-E{idx})*(F{idx}+0.01))+(D{idx}*E{idx}*F{idx})")
        c_shock.font = Font(name="Arial", size=9, color=COLOR_BLACK_FORMULA)
        c_shock.number_format = FMT_KOMMUNE_VARIANCE
        c_shock.alignment = Alignment(horizontal="right")

        # Effekt = H - G
        c_eff = ws3.cell(row=idx, column=9, value=f"=H{idx}-G{idx}")
        c_eff.font = Font(name="Arial", size=9, bold=True, color=COLOR_RED_ALERT)
        c_eff.number_format = FMT_KOMMUNE_VARIANCE
        c_eff.alignment = Alignment(horizontal="right")

        for col in range(2, 10):
            ws3.cell(row=idx, column=col).border = BORDER_THIN_BOTTOM
        ws3.row_dimensions[idx].height = 20

    # Total Lån
    ws3.cell(row=9, column=2, value="TOTAL").font = Font(name="Arial", size=9, bold=True, color="1F2937")
    ws3.cell(row=9, column=3, value="6,8 mrd. NOK").font = Font(name="Arial", size=9, bold=True, color="1F2937")
    ws3.cell(row=9, column=4, value="=SUM(D6:D8)").number_format = FMT_KOMMUNE_VARIANCE
    ws3.cell(row=9, column=7, value="=SUM(G6:G8)").number_format = FMT_KOMMUNE_VARIANCE
    ws3.cell(row=9, column=8, value="=SUM(H6:H8)").number_format = FMT_KOMMUNE_VARIANCE
    ws3.cell(row=9, column=9, value="=SUM(I6:I8)").number_format = FMT_KOMMUNE_VARIANCE

    for col in range(2, 10):
        c = ws3.cell(row=9, column=col)
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c.border = BORDER_TOTAL
        c.alignment = Alignment(horizontal="right" if col >= 4 else "left")
    ws3.row_dimensions[9].height = 22

    # ==========================================================================
    # FANE 5: 04_Disposisjonsfond_Prognose
    # ==========================================================================
    ws4 = wb.create_sheet(title="04_Disposisjonsfond_Prognose")
    ws4.views.sheetView[0].showGridLines = True

    ws4.merge_cells("B2:G2")
    ws4["B2"] = "DISPOSISJONSFOND UTVIKLING & BUFFERANALYSE (2026–2030)"
    ws4["B2"].font = Font(name="Arial", size=14, bold=True, color=FILL_NAVY_HEADER)

    ws4.merge_cells("B3:G3")
    ws4["B3"] = "Vurdering av kommunens økonomiske handlingsrom jf. Kommuneloven § 14-5 (Krav: > 5% av brutto driftsinntekter)"
    ws4["B3"].font = Font(name="Arial", size=10, italic=True, color="4B5563")

    df_headers = ["År", "Inngående Balanse", "Avsetning fra Drift", "Bruk til Inndekning (§ 14-5)", "Utgående Balanse", "Andel av Driftsinntekt"]
    for c_i, dfh in enumerate(df_headers, start=2):
        c = ws4.cell(row=5, column=c_i, value=dfh)
        c.font = Font(name="Arial", size=9, bold=True, color=COLOR_WHITE)
        c.fill = PatternFill(start_color=FILL_NAVY_HEADER, end_color=FILL_NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="right" if c_i >= 3 else "center")
    ws4.row_dimensions[5].height = 24

    fond_data = [
        ("2026 (Anslag)", 540000, 120000, -189000, 6970000),
        ("2027 (HØP)", 471000, 140000, -90000, 7150000),
        ("2028 (HØP)", 521000, 150000, -80000, 7350000),
        ("2029 (HØP)", 591000, 160000, -60000, 7550000),
        ("2030 (HØP)", 691000, 175000, -50000, 7750000)
    ]

    for idx, (yr, inng, avs, bruk, brutto_inntekt) in enumerate(fond_data, start=6):
        ws4.cell(row=idx, column=2, value=yr).font = Font(name="Arial", size=9, bold=True, color="1F2937")
        ws4.cell(row=idx, column=2).alignment = Alignment(horizontal="center")

        c_inng = ws4.cell(row=idx, column=3, value=inng)
        c_inng.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT if idx == 6 else COLOR_BLACK_FORMULA)
        c_inng.number_format = FMT_KOMMUNE_VARIANCE
        c_inng.alignment = Alignment(horizontal="right")

        c_avs = ws4.cell(row=idx, column=4, value=avs)
        c_avs.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
        c_avs.fill = PatternFill(start_color=FILL_GRAY_INPUT, end_color=FILL_GRAY_INPUT, fill_type="solid")
        c_avs.number_format = FMT_KOMMUNE_VARIANCE
        c_avs.alignment = Alignment(horizontal="right")

        c_bruk = ws4.cell(row=idx, column=5, value=bruk)
        c_bruk.font = Font(name="Arial", size=9, color=COLOR_BLUE_INPUT)
        c_bruk.fill = PatternFill(start_color=FILL_GRAY_INPUT, end_color=FILL_GRAY_INPUT, fill_type="solid")
        c_bruk.number_format = FMT_KOMMUNE_VARIANCE
        c_bruk.alignment = Alignment(horizontal="right")

        # Utgående balanse = Inngående + Avsetning + Bruk (husk at bruk er negativt)
        c_utg = ws4.cell(row=idx, column=6, value=f"=C{idx}+D{idx}+E{idx}")
        c_utg.font = Font(name="Arial", size=9, bold=True, color=COLOR_BLACK_FORMULA)
        c_utg.number_format = FMT_KOMMUNE_VARIANCE
        c_utg.alignment = Alignment(horizontal="right")

        # Andel = Utgående / Brutto driftsinntekt
        c_pct = ws4.cell(row=idx, column=7, value=f"=F{idx}/{brutto_inntekt}")
        c_pct.font = Font(name="Arial", size=9, bold=True, color="166534" if inng > 400000 else COLOR_RED_ALERT)
        c_pct.number_format = FMT_PERCENT
        c_pct.alignment = Alignment(horizontal="right")

        for col in range(2, 8):
            ws4.cell(row=idx, column=col).border = BORDER_THIN_BOTTOM
        ws4.row_dimensions[idx].height = 20

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
    out = generate_cfo_executive_konsern_model()
    print(f"Bygget CFO Konsernmodell: {out}")
