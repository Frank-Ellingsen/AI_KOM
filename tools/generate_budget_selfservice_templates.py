#!/usr/bin/env python3
"""
Generator for Selvhjelpspakke & Maler for Budsjettansvarlige (Styring, Kontroll, Budsjettering)
Kristiansand Kommune — Økonomi og Virksomhetsstyring

Genererer formelle Word (.docx), Excel (.xlsx) og Markdown (.md) maler
tilpasset enhetsledere, rektorer og styrere uten formell økonomiutdanning.
"""

from __future__ import annotations

import os
from pathlib import Path
import datetime
import hashlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

ROOT_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT_DIR / "templates"
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

COLOR_NAVY = RGBColor(27, 54, 93)      # #1B365D
COLOR_SLATE = RGBColor(100, 116, 139)  # #64748B
COLOR_TEXT = RGBColor(30, 41, 59)      # #1E293B

def set_cell_background(cell, hex_color: str):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_header(doc, title: str, subtitle: str, ref_code: str):
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(2)
    run_meta = p_meta.add_run(f"KRISTIANSAND KOMMUNE | ØKONOMI & VIRKSOMHETSSTYRING | REF: {ref_code}")
    run_meta.font.name = "Segoe UI"
    run_meta.font.size = Pt(8.5)
    run_meta.font.color.rgb = COLOR_SLATE
    run_meta.font.bold = True

    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(4)
    h1.paragraph_format.space_after = Pt(2)
    run_h1 = h1.add_run(title)
    run_h1.font.name = "Segoe UI"
    run_h1.font.size = Pt(16)
    run_h1.font.bold = True
    run_h1.font.color.rgb = COLOR_NAVY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(14)
    run_sub = p_sub.add_run(subtitle)
    run_sub.font.name = "Segoe UI"
    run_sub.font.size = Pt(9.5)
    run_sub.font.italic = True
    run_sub.font.color.rgb = COLOR_SLATE

    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(12)
    p_div_run = p_div.add_run("―" * 55)
    p_div_run.font.color.rgb = COLOR_SLATE
    p_div_run.font.size = Pt(8)


# ==============================================================================
# 1. STYRING: LEDERENS MÅNEDSSTATUS & PROGNOSE (WORD + MD)
# ==============================================================================
def create_manedsstatus_template():
    docx_path = TEMPLATES_DIR / "MAL_LEDERENS_MANEDSSTATUS_OG_PROGNOSE.docx"
    md_path = TEMPLATES_DIR / "MAL_LEDERENS_MANEDSSTATUS_OG_PROGNOSE.md"

    doc = docx.Document()
    add_header(
        doc,
        title="LEDERENS MÅNEDSRAPPORT & BUDSJETTPROGNOSE",
        subtitle="Månedlig styringsnotat for enhetsledere til kommunalsjef og controller",
        ref_code="MAL-STYRING-01"
    )

    doc.add_paragraph(
        "Dette notatet fylles ut av enhetsleder innen den 5. virkedagen i hver måned. "
        "Formålet er å gi en kortfattet, pedagogisk status på forbruk, bemanningsutvikling og forventet årssluttbalanse jf. Kommuneloven § 14-5."
    )

    doc.add_heading(level=2).add_run("1. NØKKELTALL FOR ENHETEN").font.color.rgb = COLOR_NAVY
    table = doc.add_table(rows=5, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    fields = [
        ("Virksomhet / Enhet:", "[F.eks. Enhet 401 Strai Sykehjem / Enhet 202 Lovisenlev Skole]"),
        ("Budsjettansvarlig leder:", "[Navn og tittel]"),
        ("Tildelt årsbudsjett 2026:", "[F.eks. 50 339 000 kr]"),
        ("Bokført forbruk hittil (YTD):", "[F.eks. 43 397 467 kr]"),
        ("Disponibel saldo for resten av året:", "[F.eks. 6 941 533 kr — Trafikklys: RØD / GUL / GRØNN]")
    ]
    for idx, (label, val) in enumerate(fields):
        row = table.rows[idx]
        set_cell_background(row.cells[0], "F1F5F9")
        set_cell_background(row.cells[1], "FFFFFF")
        set_cell_margins(row.cells[0], 50, 50, 80, 80)
        set_cell_margins(row.cells[1], 50, 50, 80, 80)
        r0 = row.cells[0].paragraphs[0].add_run(label)
        r0.font.name = "Segoe UI"
        r0.font.bold = True
        r0.font.size = Pt(9)
        r1 = row.cells[1].paragraphs[0].add_run(val)
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(9)

    doc.add_heading(level=2).add_run("2. 3-MINUTTERS LEDEROPPSUMMERING").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "Kort oppsummering av driftssituasjonen i klarspråk:\n"
        "• Er driften i rute, eller minker saldoen raskere enn forutsatt?\n"
        "• Hvordan er sykefraværet sammenlignet med forrige måned?\n"
        "• Er det uforutsette hendelser som krever bistand fra økonomirådgiver?"
    )

    doc.add_heading(level=2).add_run("3. BEMANNING OG VIKARBRUK (ART 1010 / 1020)").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "• Antall vikarvakter rekvirert fra privat byrå: [Antall vakter]\n"
        "• Kostnad vikarbyrå denne måneden: [kr beløp]\n"
        "• Er det vurdert oppgavedeling blant faste ansatte før vikar ble innkalt? [Ja / Nei]\n"
        "• Status på refusjonskrav oversendt til NAV (art 1600): [kr beløp mottatt / utestående]"
    )

    doc.add_heading(level=2).add_run("4. KONKRETE TILTAK FOR KOMMENDE MÅNED").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "1. [Tiltak 1: F.eks. Strammere godkjenning av ekstrahjelp]\n"
        "2. [Tiltak 2: Purring på utestående sykemeldinger til NAV innen den 15.]\n"
        "3. [Tiltak 3: Avstemming med controller Frank Ellingsen]"
    )

    doc.save(docx_path)

    md_text = f"""# 📋 MAL: LEDERENS MÅNEDSRAPPORT & BUDSJETTPROGNOSE
**Referanse:** MAL-STYRING-01 | **Målgruppe:** Enhetsledere, rektorer og styrere i Kristiansand kommune

## 1. Nøkkeltall for Enheten
* **Enhet og ansvar:** [F.eks. Enhet 401 Strai Sykehjem / Ansvar 5200]
* **Budsjettansvarlig:** [Lederens Navn]
* **Tildelt Årsramme 2026:** [kr beløp]
* **Hittil Brukt YTD:** [kr beløp]
* **Disponibel Saldo:** [kr beløp] (🟢 Grønn / 🟡 Gul / 🔴 Rød)
* **Månedlig Rådighetsbeløp ut året:** [kr / mnd]

## 2. 3-Minutters Lederoppsummering
[Kortfattet forklaring av månedens resultat uten regnskapssjargong. Holder du deg innenfor forbrukskvoten?]

## 3. Bemanning og Vikarforbruk
* **Vikarbyråtimer:** [Antall timer / vakter]
* **Total vikarkostnad denne mnd:** [kr beløp]
* **Sykefraværsprosent:** [f.eks. 11.4 %]
* **Innsendte refusjonskrav til NAV:** [kr beløp]

## 4. Prioriterte Tiltak Neste Måned
1. [Tiltak 1]
2. [Tiltak 2]
3. [Tiltak 3]
"""
    md_path.write_text(md_text, encoding="utf-8")
    print(f"✓ Generert: {docx_path.name}")


# ==============================================================================
# 2. STYRING: BEMANNINGSPLAN OG VIKARBUDSJETT (EXCEL + MD)
# ==============================================================================
def create_bemanningsplan_excel():
    xlsx_path = TEMPLATES_DIR / "MAL_BEMANNINGSPLAN_OG_VIKARBUDSJETT.xlsx"
    md_path = TEMPLATES_DIR / "MAL_BEMANNINGSPLAN_OG_VIKARBUDSJETT.md"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Bemanningskalkyle"
    ws.views.sheetView[0].showGridLines = True

    font_title = Font(name="Segoe UI", size=13, bold=True, color="1B365D")
    font_head = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
    font_bold = Font(name="Segoe UI", size=10, bold=True, color="0F172A")
    fill_navy = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

    ws["A1"] = "KRISTIANSAND KOMMUNE — BEMANNINGS- OG VIKARKALKYLE"
    ws["A1"].font = font_title
    ws["A2"] = "Selvhjelpsverktøy for enhetsledere: Beregn merkostnad ved vikarbyrå mot egenbemanning."
    ws["A2"].font = Font(name="Segoe UI", size=9, italic=True, color="64748B")

    headers = [
        "Måned", "Planlagte Årsverk", "Faktisk Fravær %", "Fraværstimer",
        "Egenvikar Timer", "Egenvikar Kr", "Byråvikar Timer", "Byrå Timepris",
        "Byråvikar Kr", "Mottatt NAV Refusjon", "Netto Vikarkostnad"
    ]
    for c_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=4, column=c_idx, value=h)
        cell.font = font_head
        cell.fill = fill_navy
        cell.alignment = Alignment(horizontal="center" if c_idx in [1, 3] else "right")

    months = ["Januar", "Februar", "Mars", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Desember"]
    for r_idx, m_name in enumerate(months, 5):
        ws.cell(row=r_idx, column=1, value=m_name).alignment = Alignment(horizontal="center")
        ws.cell(row=r_idx, column=2, value=35.0).number_format = '0.0'
        ws.cell(row=r_idx, column=3, value=0.095).number_format = '0.0%'
        
        # Fraværstimer: =B5 * 150 * C5
        ws.cell(row=r_idx, column=4, value=f"=B{r_idx}*150*C{r_idx}").number_format = '#,##0'
        ws.cell(row=r_idx, column=5, value=250).number_format = '#,##0'
        # Egenvikar kr: =E5 * 380 (fast timelønnssats)
        ws.cell(row=r_idx, column=6, value=f"=E{r_idx}*380").number_format = '#,##0 "kr"'

        # Byråvikar timer: =MAX(0, D5 - E5)
        ws.cell(row=r_idx, column=7, value=f"=MAX(0, D{r_idx}-E{r_idx})").number_format = '#,##0'
        ws.cell(row=r_idx, column=8, value=650).number_format = '#,##0 "kr"'
        # Byråvikar kr: =G5 * H5
        ws.cell(row=r_idx, column=9, value=f"=G{r_idx}*H{r_idx}").number_format = '#,##0 "kr"'

        # NAV Refusjon: =D5 * 320 * 0.70
        ws.cell(row=r_idx, column=10, value=f"=D{r_idx}*320*0.7").number_format = '#,##0 "kr"'

        # Netto vikarkostnad: =F5 + I5 - J5
        c_net = ws.cell(row=r_idx, column=11, value=f"=F{r_idx}+I{r_idx}-J{r_idx}")
        c_net.number_format = '#,##0 "kr"'
        c_net.font = font_bold

        if r_idx % 2 == 1:
            for c in range(1, 12):
                ws.cell(row=r_idx, column=c).fill = fill_zebra

    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = max(len(str(cell.value or '')) for cell in col)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    wb.save(xlsx_path)

    md_text = """# 📊 MAL: BEMANNINGSPLAN OG VIKARKALKYLE
**Filnavn:** `MAL_BEMANNINGSPLAN_OG_VIKARBUDSJETT.xlsx`  
**Målgruppe:** Enhetsledere i bemanningsintensive virksomheter (sykehjem, skole, barnehage, bofellesskap)

### Formål med verktøyet:
1. **Synliggjøre prisforskjell:** Egen tilkallingsvikar (ca. kr 380/t) koster under 60 % av et privat bemanningsbyrå (kr 650–750/t).
2. **Kalkulere NAV-refusjon:** Beregner forventet refusjon fra dag 17 slik at netto vikarkostnad fremstår realistisk.
3. **Turnusplanlegging:** Hjelper lederen å unngå unødvendig vikarinnleie ved å utnytte interne ressurser og reservevakter.
"""
    md_path.write_text(md_text, encoding="utf-8")
    print(f"✓ Generert: {xlsx_path.name}")


# ==============================================================================
# 3. KONTROLL: INTERNKONTROLL EGENVURDERING (WORD + MD)
# ==============================================================================
def create_internkontroll_template():
    docx_path = TEMPLATES_DIR / "MAL_INTERNKONTROLL_EGENVURDERING_LEDER.docx"
    md_path = TEMPLATES_DIR / "MAL_INTERNKONTROLL_EGENVURDERING_LEDER.md"

    doc = docx.Document()
    add_header(
        doc,
        title="INTERNKONTROLL & EGENVURDERING FOR ENHETSLEDER",
        subtitle="Årlig sjekkliste for økonomistyring, fullmakter og attestasjonskontroll",
        ref_code="MAL-KONTROLL-01"
    )

    doc.add_paragraph(
        "I henhold til Kommuneloven § 14-5 og Kristiansand kommunes økonomireglement plikter alle budsjettansvarlige "
        "å påse at det er etablert tilfredsstillende internkontroll. Dette skjemaet fylles ut årlig eller ved tertialoppfølging."
    )

    doc.add_heading(level=2).add_run("SJEKKLISTE FOR LEDERENS KONTROLLPUNKTER:").font.color.rgb = COLOR_NAVY

    table = doc.add_table(rows=6, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Kontrollområde", "Krav og rutine", "Status (OK / Avvik)"]
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0].add_run(h)
        p.font.name = "Segoe UI"
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = RGBColor(255, 255, 255)

    checks = [
        ("1. Attestasjon & Anvisning", "Alle inngående fakturaer er attestert innen 5 virkedager. Ingen attesterer egne utlegg.", "[  ] OK   [  ] Avvik"),
        ("2. Timelister & Overtid", "Timelister og overtid i GAT godkjennes månedlig. Stikkprøver er gjennomført mot vaktplan.", "[  ] OK   [  ] Avvik"),
        ("3. Delegeringsfullmakt", "Ingen innkjøp eller avtaler overskrider tildelt beløpsgrense uten overordnet godkjenning.", "[  ] OK   [  ] Avvik"),
        ("4. NAV Refusjoner (art 1600)", "Alle sykemeldinger over 16 dager er oversendt NAV. Ingen refusjonskrav er foreldet.", "[  ] OK   [  ] Avvik"),
        ("5. Avviksnotat § 14-5", "Ved forventet merforbruk > 5 % eller 250k er formelt avviksnotat sendt kommunalsjef.", "[  ] OK   [  ] Avvik")
    ]
    for r_idx, (col0, col1, col2) in enumerate(checks, 1):
        row = table.rows[r_idx]
        set_cell_background(row.cells[0], "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
        set_cell_background(row.cells[1], "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
        set_cell_background(row.cells[2], "F1F5F9")
        for c_idx, text in enumerate([col0, col1, col2]):
            cell = row.cells[c_idx]
            set_cell_margins(cell, 50, 50, 70, 70)
            r = cell.paragraphs[0].add_run(text)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(14)
    doc.add_heading(level=2).add_run("KONKLUSJON & UNDERSKRIFT").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "Jeg bekrefter at internkontrollen på min enhet er gjennomgått i henhold til ovennevnte punkter.\n"
        "Dato: [Dato] | Enhetsleder: [Navn] | Sendes til: [Kommunalsjef / Controller]"
    )

    doc.save(docx_path)

    md_text = """# 🛡️ MAL: INTERNKONTROLL & EGENVURDERING FOR ENHETSLEDER
**Referanse:** MAL-KONTROLL-01 | **Målgruppe:** Budsjettansvarlige ledere i Kristiansand kommune

### Årlig Sjekkliste for Økonomisk Internkontroll:
1. **Fakturahåndtering:** Fakturaer attesteres løpende innen 5 dager. Kontering kontrolleres mot KOSTRA artskontoplan.
2. **Lønn og Turnus:** Overtid og ekstravakter er forhåndsgodkjent. Fravær registreres i GAT dag 1.
3. **Fullmaktsgrenser:** Avtaler og innkjøp holder seg innenfor tildelt delegeringsgrense.
4. **NAV-refusjoner:** Krav om sykepenger og foreldrepenger følges opp månedlig (art 1600/1700).
5. **Budsjettbalanse:** Eventuelle merforbruk meldes proaktivt i samsvar med Kommuneloven § 14-5.
"""
    md_path.write_text(md_text, encoding="utf-8")
    print(f"✓ Generert: {docx_path.name}")


# ==============================================================================
# 4. KONTROLL: NAV REFUSJONSOPPFØLGING OG AVSTEMMING (EXCEL + MD)
# ==============================================================================
def create_nav_refusjon_excel():
    xlsx_path = TEMPLATES_DIR / "MAL_NAV_REFUSJONSOPPFOLGING_OG_AVSTEMMING.xlsx"
    md_path = TEMPLATES_DIR / "MAL_NAV_REFUSJONSOPPFOLGING_OG_AVSTEMMING.md"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "NAV_Refusjoner"
    ws.views.sheetView[0].showGridLines = True

    font_title = Font(name="Segoe UI", size=13, bold=True, color="1B365D")
    font_head = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
    font_bold = Font(name="Segoe UI", size=10, bold=True, color="0F172A")
    fill_navy = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

    ws["A1"] = "KRISTIANSAND KOMMUNE — OPPFØLGING AV NAV-REFUSJONER"
    ws["A1"].font = font_title
    ws["A2"] = "Selvhjelpsmodell for enhetsleder: Sikre at ingen sykelønnsrefusjoner går tapt (art 1600/1700)."
    ws["A2"].font = Font(name="Segoe UI", size=9, italic=True, color="64748B")

    headers = [
        "Ansatt-ID", "Stilling / Rolle", "Første Sykedag", "Arbeidsgiverperiode Slutt",
        "Krav Sendt NAV", "Kravbeløp Kr", "Mottatt fra NAV", "Rest Utestående", "Status", "Frist 3 mnd"
    ]
    for c_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=4, column=c_idx, value=h)
        cell.font = font_head
        cell.fill = fill_navy
        cell.alignment = Alignment(horizontal="center" if c_idx in [1, 3, 4, 5, 9, 10] else "right")

    sample_cases = [
        ("ANS-40101", "Sykepleier", "2026-08-10", "2026-08-26", "2026-08-28", 48500, 48500, "Mottatt", "2026-11-26"),
        ("ANS-40105", "Helsefagarbeider", "2026-08-20", "2026-09-05", "2026-09-08", 36200, 36200, "Mottatt", "2026-12-05"),
        ("ANS-40112", "Miljøterapeut", "2026-09-01", "2026-09-17", "2026-09-20", 42000, 0, "Under behandling", "2026-12-17"),
        ("ANS-40118", "Assistent", "2026-09-12", "2026-09-28", "2026-10-02", 28500, 0, "Purring sendt", "2026-12-28"),
        ("ANS-40124", "Sykepleier", "2026-09-25", "2026-10-11", "2026-10-14", 51000, 0, "Nylig meldt", "2027-01-11")
    ]

    for r_idx, data in enumerate(sample_cases, 5):
        ws.cell(row=r_idx, column=1, value=data[0]).alignment = Alignment(horizontal="center")
        ws.cell(row=r_idx, column=2, value=data[1])
        ws.cell(row=r_idx, column=3, value=data[2]).alignment = Alignment(horizontal="center")
        ws.cell(row=r_idx, column=4, value=data[3]).alignment = Alignment(horizontal="center")
        ws.cell(row=r_idx, column=5, value=data[4]).alignment = Alignment(horizontal="center")
        
        ws.cell(row=r_idx, column=6, value=data[5]).number_format = '#,##0 "kr"'
        ws.cell(row=r_idx, column=7, value=data[6]).number_format = '#,##0 "kr"'
        
        # Rest: =F5 - G5
        c_rest = ws.cell(row=r_idx, column=8, value=f"=F{r_idx}-G{r_idx}")
        c_rest.number_format = '#,##0 "kr"'
        c_rest.font = font_bold

        ws.cell(row=r_idx, column=9, value=data[7]).alignment = Alignment(horizontal="center")
        ws.cell(row=r_idx, column=10, value=data[8]).alignment = Alignment(horizontal="center")

        if r_idx % 2 == 1:
            for c in range(1, 11):
                ws.cell(row=r_idx, column=c).fill = fill_zebra

    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = max(len(str(cell.value or '')) for cell in col)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    wb.save(xlsx_path)

    md_text = """# 📥 MAL: NAV REFUSJONSOPPFØLGING OG AVSTEMMING
**Filnavn:** `MAL_NAV_REFUSJONSOPPFOLGING_OG_AVSTEMMING.xlsx`  
**Målgruppe:** Alle ledere med fraværsoppfølging (GAT / Visma)

### Viktige Tidsfrister og Regler for Enhetsleder:
1. **Arbeidsgiverperioden (16 dager):** Kommunen dekker de første 16 kalenderdagene av fraværet.
2. **Krav fra dag 17:** Inntektsmelding må sendes elektronisk via A-ordningen/Visma snarest etter dag 16.
3. **Foreldelsesfrist (3 måneder):** Krav om refusjon må fremsettes innen 3 måneder etter den måneden fraværet gjaldt jf. Folketrygdloven § 22-13. Overskrides fristen, **tapes refusjonen permanent** for kommunen!
"""
    md_path.write_text(md_text, encoding="utf-8")
    print(f"✓ Generert: {xlsx_path.name}")


# ==============================================================================
# 5. BUDSJETTERING: INNSPILL TIL FRAMSIKT HØP 2027–2030 (WORD + MD)
# ==============================================================================
def create_hop_innspill_template():
    docx_path = TEMPLATES_DIR / "MAL_BUDSJETTINNSPILL_FRAMSIKT_HOP_2027.docx"
    md_path = TEMPLATES_DIR / "MAL_BUDSJETTINNSPILL_FRAMSIKT_HOP_2027.md"

    doc = docx.Document()
    add_header(
        doc,
        title="BUDSJETTINNSPILL TIL FRAMSIKT EPM (HØP 2027–2030)",
        subtitle="Enhetslederens formelle innspill til Handlings- og Økonomiplan",
        ref_code="MAL-BUDSJETT-01"
    )

    doc.add_paragraph(
        "Dette skjemaet benyttes av enhetsleder ved den årlige budsjettprosessen i Framsikt EPM. "
        "Her meldes det inn endringsbehov, demografiske endringer, nye lovpålagte krav og forslag til innsparingstiltak."
    )

    doc.add_heading(level=2).add_run("1. RAMMEBETINGELSER & DEMOGRAFI").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "• Enhetens navn og KOSTRA-funksjon: [Navn og funksjon]\n"
        "• Brukergrunnlag / elevtall / beboere: [Endring i antall brukere sammenlignet med 2026]\n"
        "• Spesielle utfordringer i tjenestetilbudet: [F.eks. økt pleietyngde eller spesialundervisning]"
    )

    doc.add_heading(level=2).add_run("2. DRIFTSENDRINGER & INVESTERINGSBEHOV").font.color.rgb = COLOR_NAVY
    table = doc.add_table(rows=4, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Tiltak / Behov", "Art / Konto", "Beløp 2027 (kr)", "Begrunnelse & Effekt"]
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0].add_run(h)
        p.font.name = "Segoe UI"
        p.font.bold = True
        p.font.size = Pt(8.5)
        p.font.color.rgb = RGBColor(255, 255, 255)

    sample_rows = [
        ("Økning grunnbemanning (1 helsefagarbeider)", "Art 10100 Fastlønn", "+580 000 kr", "Erstatter overtid og byråvikarer"),
        ("Velferdsteknologi / medisindispenser", "Art 11500 Lisens/drift", "+45 000 kr", "Frigjør 4 sykepleietimer per uke"),
        ("Effektivisering varekjøp (fellesavtale)", "Art 11200 Forbruksmateriell", "-60 000 kr", "Redusert innkjøpspris via konsernavtale")
    ]
    for r_idx, (t0, t1, t2, t3) in enumerate(sample_rows, 1):
        row = table.rows[r_idx]
        set_cell_background(row.cells[0], "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
        set_cell_background(row.cells[1], "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
        set_cell_background(row.cells[2], "F1F5F9")
        set_cell_background(row.cells[3], "FFFFFF")
        for c_idx, text in enumerate([t0, t1, t2, t3]):
            cell = row.cells[c_idx]
            set_cell_margins(cell, 50, 50, 70, 70)
            r = cell.paragraphs[0].add_run(text)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)
            if c_idx == 2:
                r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(14)
    doc.add_heading(level=2).add_run("3. KONSEKVENS VED MANGLENDE RAMMEJUSTERING").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "Beskriv konsekvensene for tjenestetilbudet og lovoppfyllelse dersom det omsøkte beløpet ikke innvilges:\n"
        "[Lederens faglige vurdering av konsekvenser jf. Helse- og omsorgstjenesteloven / Opplæringsloven]"
    )

    doc.save(docx_path)

    md_text = """# 📊 MAL: BUDSJETTINNSPILL TIL FRAMSIKT EPM (HØP 2027–2030)
**Referanse:** MAL-BUDSJETT-01 | **Målgruppe:** Alle budsjettansvarlige ledere

### Formål med HØP-innspillet:
Sikre at enhetens reelle behov registreres i **Framsikt EPM** i forkant av Kommunedirektørens budsjettforslag til Bystyret.

### 3 Nøkkelforutsetninger for et godt budsjettinnspill:
1. **Kvantifiserte gevinster:** Dersom du søker om nye stillinger, må du vise hvordan dette reduserer vikarbyråforbruk (art 10200) eller overtid (art 10900).
2. **Lovpålagte minstekrav:** Referer til bemanningsnorm, lærernorm eller kvalitetsforskrifter.
3. **Inndekningsforslag:** Forslag til interne innsparinger styrker søknadens gjennomslagskraft hos kommunalsjefen.
"""
    md_path.write_text(md_text, encoding="utf-8")
    print(f"✓ Generert: {docx_path.name}")


# ==============================================================================
# 6. BUDSJETTERING: OMDISPONERING OG RAMMEJUSTERING (WORD + MD)
# ==============================================================================
def create_omdisponering_template():
    docx_path = TEMPLATES_DIR / "MAL_OMDISPONERING_OG_RAMMEJUSTERING.docx"
    md_path = TEMPLATES_DIR / "MAL_OMDISPONERING_OG_RAMMEJUSTERING.md"

    doc = docx.Document()
    add_header(
        doc,
        title="NOTAT: INTERN OMDISPONERING AV BUDSJETTRAMME",
        subtitle="Flytting av budsjettmidler innenfor delegert fullmakt jf. Kommuneloven § 14-6",
        ref_code="MAL-BUDSJETT-02"
    )

    doc.add_paragraph(
        "Enhetsleder har fullmakt til å omdisponere midler mellom egne driftsarter (art 1000–1290) "
        "forutsatt at netto budsjettramme opprettholdes (sum = 0 kr) og bruttoprinsippet i § 14-6 overholdes."
    )

    doc.add_heading(level=2).add_run("1. OMDISPONERINGSSKJEMA").font.color.rgb = COLOR_NAVY
    table = doc.add_table(rows=4, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Artskonto og Navn", "Opprinnelig Ramme", "Endring (+ / -)", "Ny Ramme 2026"]
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0].add_run(h)
        p.font.name = "Segoe UI"
        p.font.bold = True
        p.font.size = Pt(8.5)
        p.font.color.rgb = RGBColor(255, 255, 255)

    om_rows = [
        ("Art 10200 Vikarutgifter (reduseres)", "2 400 000 kr", "-350 000 kr", "2 050 000 kr"),
        ("Art 10100 Fastlønn (styrking)", "28 500 000 kr", "+350 000 kr", "28 850 000 kr"),
        ("NETTO ENDRING RAMME", "30 900 000 kr", "0 kr", "30 900 000 kr")
    ]
    for r_idx, (c0, c1, c2, c3) in enumerate(om_rows, 1):
        row = table.rows[r_idx]
        set_cell_background(row.cells[0], "F1F5F9" if r_idx == 3 else "FFFFFF")
        set_cell_background(row.cells[1], "F8FAFC")
        set_cell_background(row.cells[2], "F1F5F9")
        set_cell_background(row.cells[3], "FFFFFF")
        for col_idx, text in enumerate([c0, c1, c2, c3]):
            cell = row.cells[col_idx]
            set_cell_margins(cell, 50, 50, 70, 70)
            r = cell.paragraphs[0].add_run(text)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)
            if r_idx == 3 or col_idx == 2:
                r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(14)
    doc.add_heading(level=2).add_run("2. FAGLIG BEGRUNNELSE").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "Beskriv hvorfor omdisponeringen er hensiktsmessig for driften og hvordan kvaliteten ivaretas:\n"
        "[F.eks. Midlene flyttes fra ekstern vikarinnleie til oppbemanning av fast stilling for å oppnå stabilitet.]"
    )

    doc.add_heading(level=2).add_run("3. GODKJENNING & IVERKSETTELSE").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "Enhetsleder: [Navn og dato] | Godkjent av Controller: Frank Ellingsen | Iverksatt i Framsikt/Visma: [Dato]"
    )

    doc.save(docx_path)

    md_text = """# 🔄 MAL: INTERN OMDISPONERING AV BUDSJETTRAMME
**Referanse:** MAL-BUDSJETT-02 | **Målgruppe:** Enhetsledere og kommunalsjefer

### Vilkår for Intern Omdisponering:
1. **Netto Nullsum:** Summen av reduksjoner og økninger må være nøyaktig 0 kr.
2. **Bruttoprinsippet (§ 14-6):** Det er ikke tillatt å motregne inntekter mot utgifter.
3. **Delegeringsreglementet:** Omdisponeringer innenfor egen enhet godkjennes av enhetsleder og attesteres av controller.
"""
    md_path.write_text(md_text, encoding="utf-8")
    print(f"✓ Generert: {docx_path.name}")


def main():
    print("=" * 80)
    print("🏛️ GENERERER SELVHJELPSPAKKE FOR BUDSJETTANSVARLIGE (STYRING, KONTROLL, BUDSJETT)")
    print("=" * 80)

    create_manedsstatus_template()
    create_bemanningsplan_excel()
    create_internkontroll_template()
    create_nav_refusjon_excel()
    create_hop_innspill_template()
    create_omdisponering_template()

    print("\n✅ Ferdig! Alle 6 selvhjelpsmaler (Word, Excel, Markdown) er generert.")

if __name__ == "__main__":
    main()
