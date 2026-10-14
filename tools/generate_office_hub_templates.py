#!/usr/bin/env python3
"""
Generator for Office Hub Maler, Maler, Skjemaer og Rapporter
Kristiansand Kommune - Økonomi og Virksomhetsstyring
Genererer formelle Word (.docx), Markdown (.md) og Excel (.xlsx) dokumenter.
"""

from __future__ import annotations

import os
from pathlib import Path
import datetime
import hashlib
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

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

ROOT_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT_DIR / "templates"
REPORTS_DIR = ROOT_DIR / "reports"

TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Farger for Word
COLOR_NAVY = RGBColor(27, 54, 93)      # #1B365D
COLOR_SLATE = RGBColor(100, 116, 139)  # #64748B
COLOR_TEXT = RGBColor(30, 41, 59)      # #1E293B


def set_cell_background(cell, hex_color: str):
    """Setter bakgrunnsfarge på en tabellcelle i docx."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Setter interne marger (padding) i tabellcelle."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def add_document_header(doc, title: str, subtitle: str, ref_code: str):
    """Legger til standardisert kommunal toppbjelke."""
    # Toppbjelke
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(2)
    run_meta = p_meta.add_run(f"KRISTIANSAND KOMMUNE | ØKONOMI OG VIRKSOMHETSSTYRING | REF: {ref_code}")
    run_meta.font.name = "Segoe UI"
    run_meta.font.size = Pt(8.5)
    run_meta.font.color.rgb = COLOR_SLATE
    run_meta.font.bold = True

    # Hovedtittel
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(4)
    h1.paragraph_format.space_after = Pt(2)
    run_h1 = h1.add_run(title)
    run_h1.font.name = "Segoe UI"
    run_h1.font.size = Pt(17)
    run_h1.font.bold = True
    run_h1.font.color.rgb = COLOR_NAVY

    # Undertittel
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(16)
    run_sub = p_sub.add_run(subtitle)
    run_sub.font.name = "Segoe UI"
    run_sub.font.size = Pt(10)
    run_sub.font.italic = True
    run_sub.font.color.rgb = COLOR_SLATE

    # Skillelinje
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(12)
    p_div_run = p_div.add_run("―" * 55)
    p_div_run.font.color.rgb = COLOR_SLATE
    p_div_run.font.size = Pt(8)


# ==============================================================================
# 1. MAL: POLITISK SAKSFREMLEGG (KOMMUNELOVEN § 14-5 & § 14-6)
# ==============================================================================
def create_saksfremlegg_template():
    filename_docx = TEMPLATES_DIR / "MAL_POLITISK_SAKSFREMLEGG_BUDSJETTENDRING.docx"
    filename_md = TEMPLATES_DIR / "MAL_POLITISK_SAKSFREMLEGG_BUDSJETTENDRING.md"

    doc = docx.Document()
    add_document_header(
        doc,
        title="SAKSFREMLEGG: BUDSJETTENDRING OG OMDISPONERING",
        subtitle="Regulering av årsbudsjettet jf. Kommuneloven § 14-5 og bruttoprinsippet § 14-6",
        ref_code="SAK-2026-T2-1405"
    )

    # Metadata tabell
    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Arkivsak / Saksnummer:", "26/08940-1"),
        ("Saksbehandler / Controller:", "Rådgiver Økonomistyring / Frank Ellingsen"),
        ("Møtedato & Utvalg:", "28. september 2026 — Formannskapet / Bystyret"),
        ("Hjemmelsgrunnlag:", "Kommuneloven § 14-5 (Handleplikt) og § 14-6 (Bruttoprinsippet)")
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = table.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.2)
        cell_val.width = Inches(4.3)
        set_cell_background(cell_lbl, "F1F5F9")
        set_cell_background(cell_val, "FFFFFF")
        set_cell_margins(cell_lbl, 60, 60, 100, 100)
        set_cell_margins(cell_val, 60, 60, 100, 100)
        
        p0 = cell_lbl.paragraphs[0]
        r0 = p0.add_run(label)
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_NAVY
        
        p1 = cell_val.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 1. TITTEL
    h2 = doc.add_heading(level=1)
    r_h2 = h2.add_run("SAKSTITTEL: OMDISPONERING OG BUDSJETTREGULERING PER 2. TERTIAL 2026")
    r_h2.font.color.rgb = COLOR_NAVY
    r_h2.font.size = Pt(13)

    # 2. VEDTAKSFORSLAG
    h_vedtak = doc.add_heading(level=2)
    h_vedtak.add_run("KOMMUNEDIREKTØRENS FORSLAG TIL VEDTAK:").font.color.rgb = COLOR_NAVY
    
    p_v1 = doc.add_paragraph()
    p_v1.add_run("1. Bystyret tar orienteringen om forventet årsavvik per 2. tertial 2026 til etterretning.\n"
                 "2. Bystyret bevilger en rammejustering på kr [Fyll inn beløp, f.eks. 3 200 000] til tjenesteområde Oppvekst / Grunnskole (KOSTRA 202) til dekning av lovpålagte vikar- og assistentutgifter.\n"
                 "3. Bystyret godkjenner omdisponering av kr [Fyll inn beløp, f.eks. 1 850 000] innenfor Helse og mestring / Bo og Miljø (KOSTRA 254) mot iverksettelse av administrativ vikarpool.\n"
                 "4. Netto merforbruk på kr [Fyll inn restbeløp] dekkes inn ved overføring fra kommunens disposisjonsfond jf. Kommuneloven § 14-5 andre ledd.")
    
    # 3. SAKSUTREDNING
    h_utred = doc.add_heading(level=2)
    h_utred.add_run("SAKSUTREDNING & FAGLIG BEGRUNNELSE:").font.color.rgb = COLOR_NAVY

    doc.add_paragraph(
        "I henhold til Kommuneloven § 14-5 plikter kommunedirektøren å fremme sak om endring av årsbudsjettet "
        "dersom det under budsjettåret oppstår vesentlige avvik som utfordrer budsjettbalansen eller realismekravet. "
        "Analysene per 2. tertial (august) avdekker et strukturelt avviksdriv spesielt innen bemanningsintensive enheter."
    )

    # Tabell over avvik
    doc.add_heading(level=3).add_run("Oversikt over vesentlige avvik på KOSTRA-funksjon:")
    t_avvik = doc.add_table(rows=4, cols=5)
    t_avvik.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Funksjon / Enhet", "Årsbudsjett", "Regnskap YTD", "Est. Sluttkostnad (EAC)", "Avvik mot ramme"]
    for i, h in enumerate(headers):
        cell = t_avvik.rows[0].cells[i]
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    avvik_rader = [
        ("KOSTRA 202 Kommunal Skole", "33 591 000 kr", "36 080 000 kr", "49 164 000 kr", "-15 573 000 kr"),
        ("KOSTRA 254 Bo og Miljø", "50 339 000 kr", "47 426 000 kr", "67 072 000 kr", "-16 733 000 kr"),
        ("TOTALT KONTROLLOMRÅDE", "83 930 000 kr", "83 506 000 kr", "116 236 000 kr", "-32 306 000 kr")
    ]
    for row_idx, data in enumerate(avvik_rader, start=1):
        for col_idx, text in enumerate(data):
            cell = t_avvik.rows[row_idx].cells[col_idx]
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            if row_idx == 3:
                bg = "F1F5F9"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)
            if row_idx == 3 or col_idx == 4:
                r.font.bold = True
            if col_idx == 4:
                r.font.color.rgb = RGBColor(192, 57, 43)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 4. BRUTTOPRINSIPPET & ANORDNING
    doc.add_heading(level=2).add_run("VURDERING AV REGNSKAPSPRINSIPPER (KOMMUNELOVEN § 14-6):").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "I samsvar med bruttoprinsippet er det ikke adgang til å nettoføre vikarutgifter mot fremtidige "
        "eller mottatte refusjoner fra NAV eller statlige tilskudd. Vikarforbruk og sykelønnsrefusjoner "
        "behandles på separate budsjettposter. Tidsforskyvning i refusjonskrav fra NAV (art 1690) utgjør "
        "et midlertidig etterslep som ikke skal benyttes til å skjule underliggende driftsmerforbruk."
    )

    # 5. TARIFF & MEDBESTEMMELSE
    doc.add_heading(level=2).add_run("MEDBESTEMMELSE & TARIFFMESSIG FORANKRING (HTA § 4):").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "De foreslåtte tiltakene som berører turnusoptimalisering, reduksjon i overtid og justering i bemanningsplan "
        "har vært gjenstand for drøfting i henhold til Hovedtariffavtalen (HTA) § 4 og Hovedavtalen del B § 3. "
        "Tillitsvalgte fra Fagforbundet, Delta og Utdanningsforbundet er orientert i møte den [Dato], og deres merknader er hensyntatt."
    )

    # 6. SIGNATUR & AUDIT
    doc.add_heading(level=2).add_run("KRYPTOGRAFISK REVISJONSBEVIS (STAGE-GATE PORT 9):").font.color.rgb = COLOR_NAVY
    p_audit = doc.add_paragraph()
    p_audit.add_run(
        "Saksbehandlingsnotat og beregningsgrunnlag er forseglet i SQLite Audit_AI_Actions.\n"
        "SHA-256 SAKSHASH: 7f8a9b2c3d4e5f6a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a\n"
        "Signert elektronisk av Frank Ellingsen (Senior Controller) — Godkjent i Control Office Hub."
    )
    p_audit.runs[0].font.name = "Consolas"
    p_audit.runs[0].font.size = Pt(8.5)
    p_audit.runs[0].font.color.rgb = COLOR_SLATE

    doc.save(filename_docx)

    # Generer også markdown
    md_content = f"""# 🏛️ SAKSFREMLEGG: BUDSJETTENDRING OG OMDISPONERING
**Arkivsak:** 26/08940-1 | **Møtedato:** 28. september 2026 | **Utvalg:** Formannskapet / Bystyret  
**Saksbehandler:** Rådgiver Økonomistyring / Frank Ellingsen  
**Hjemmel:** Kommuneloven § 14-5 (Handleplikt) & § 14-6 (Bruttoprinsippet)

---

## KOMMUNEDIREKTØRENS FORSLAG TIL VEDTAK:
1. Bystyret tar orienteringen om forventet årsavvik per 2. tertial 2026 til etterretning.
2. Bystyret bevilger en rammejustering på kr [Beløp] til tjenesteområde Oppvekst / Grunnskole (KOSTRA 202).
3. Bystyret godkjenner omdisponering av kr [Beløp] innenfor Helse og mestring / Bo og Miljø (KOSTRA 254).
4. Netto merforbruk dekkes inn ved overføring fra kommunens disposisjonsfond jf. Kommuneloven § 14-5 andre ledd.

---

## 1. SAKSUTREDNING & FAGLIG BEGRUNNELSE
I henhold til Kommuneloven § 14-5 plikter kommunedirektøren å fremme sak om endring av årsbudsjettet dersom det under budsjettåret oppstår vesentlige avvik som utfordrer budsjettbalansen.

### Nøkkeltall for berørte KOSTRA-funksjoner:
| Funksjon / Enhet | Årsbudsjett | Regnskap YTD | Est. Sluttkostnad (EAC) | Avvik mot ramme |
| :--- | ---: | ---: | ---: | ---: |
| KOSTRA 202 Kommunal Skole | 33 591 000 kr | 36 080 000 kr | 49 164 000 kr | -15 573 000 kr |
| KOSTRA 254 Bo og Miljø | 50 339 000 kr | 47 426 000 kr | 67 072 000 kr | -16 733 000 kr |
| **TOTALT KONTROLLOMRÅDE** | **83 930 000 kr** | **83 506 000 kr** | **116 236 000 kr** | **-32 306 000 kr** |

---

## 2. REGNSKAPSPRINSIPPER (KOMMUNELOVEN § 14-6)
- **Bruttoprinsippet:** Lønnsutgifter og refusjoner fra NAV bokføres og analyseres fullt ut brutto.
- **Anordningsprinsippet:** Utgifter og inntekter er periodisert uavhengig av betalingsdato.

---

## 3. MEDBESTEMMELSE & TARIFF (HTA § 4)
Drøftingsmøte med tillitsvalgte gjennomført den [Dato]. Bemanningsjusteringer og overtidsbegrensninger er forankret i partssamarbeidet.

---

## 4. KRYPTOGRAFISK REVISJONSBEVIS (PORT 9)
```text
SHA-256 SAKSHASH: 7f8a9b2c3d4e5f6a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a
Logget i SQLite Golden Record (Audit_AI_Actions).
```
"""
    filename_md.write_text(md_content, encoding="utf-8")
    print(f"✓ Saksfremlegg-mal generert: {filename_docx.name} & {filename_md.name}")


# ==============================================================================
# 2. MAL: AVVIKSNOTAT & TILTAKSPLAN (ENHETSLEDER -> KOMMUNALSJEF)
# ==============================================================================
def create_avviksnotat_template():
    filename_docx = TEMPLATES_DIR / "MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx"
    filename_md = TEMPLATES_DIR / "MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.md"

    doc = docx.Document()
    add_document_header(
        doc,
        title="AVVIKSNOTAT OG PRESKRIPTIV TILTAKSPLAN",
        subtitle="Driftsrapportering og tiltaksvurdering (T1–T6) fra enhetsleder til kommunalsjef",
        ref_code="NOTAT-ENHET-2026-T2"
    )

    doc.add_paragraph("Mottaker: Kommunalsjef / Sektorledelse\nFra: Enhetsleder [Sett inn enhet] / Controller\nDato: [Sett inn dato]\nStatus: Til behandling jf. Stage-Gate Port 4 & 9")

    doc.add_heading(level=2).add_run("1. AVVIKSBILDE OG ÅRSAKSFORKLARING").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "Avviket hittil i år er dekomponert på følgende hoveddrivere:\n"
        "• Faste stillingslønninger (Art 1010): [Forklaring, f.eks. full bemanning, ansiennitetsopprykk]\n"
        "• Sykevikarer (Art 1020/1050): [Forklaring, f.eks. korttidsfravær 11.4 % mot budsjettert 7.0 %]\n"
        "• Overtid og helgetillegg (Art 1040/1090): [Forklaring, f.eks. turnusvakter ved udekket fravær]\n"
        "• Kjøp fra private / vikarbyrå (Art 1270): [Forklaring, f.eks. akutt behov for spesialsykepleier]\n"
        "• Sykelønnsrefusjoner (Art 1690/1170): [Forklaring, f.eks. forsinket utbetaling fra NAV]"
    )

    doc.add_heading(level=2).add_run("2. TILTAKSMENY FOR INNDEKNING (T1–T6)").font.color.rgb = COLOR_NAVY

    t = doc.add_table(rows=7, cols=6)
    headers = ["ID", "Tiltaksbeskrivelse", "Effektbase", "Sannsynlighet", "Est. EOY-effekt", "Governance / HTA § 4"]
    for i, h in enumerate(headers):
        cell = t.rows[0].cells[i]
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.size = Pt(8)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    tiltak = [
        ("T1", "Oppfølging og purring av NAV-refusjoner", "732 705 kr", "85 %", "41 324 kr", "KREVER FAGKONTROLL"),
        ("T2", "Redusere ekstern vikarbruk via intern vikarpool", "612 450 kr", "70 %", "28 872 kr", "KREVER HR/TARIFF (HTA § 4)"),
        ("T3", "Overtidsplanlegging og forhåndsgodkjenning", "1 105 444 kr", "75 %", "55 077 kr", "KREVER HR/TARIFF (HTA § 4)"),
        ("T4", "Stopp i ikke-kritiske rammeavtaleinnkjøp", "155 776 kr", "90 %", "9 520 kr", "KREVER FAGKONTROLL"),
        ("T5", "Turnus- og bemanningsanalyse for helg", "4 789 479 kr", "60 %", "27 474 kr", "KREVER HR/TARIFF (HTA § 4)"),
        ("T6", "Digital oppfølging av ressursstyring", "17 233 691 kr", "60 %", "30 701 kr", "KREVER FAGKONTROLL"),
    ]
    for row_idx, row_data in enumerate(tiltak, start=1):
        for col_idx, val in enumerate(row_data):
            cell = t.rows[row_idx].cells[col_idx]
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8)
            if col_idx == 4:
                r.font.bold = True
                r.font.color.rgb = RGBColor(21, 128, 61)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    doc.add_heading(level=2).add_run("3. ENHETSLEDERS ANBEFALING & SIGNATUR").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "Jeg bekrefter at foreslåtte tiltak er vurdert opp mot forsvarlighetskrav i sektorlovgivning, "
        "og at tillitsvalgte er involvert der tiltaket berører arbeidstidsordninger.\n\n"
        "Signert enhetsleder: ___________________________   Dato: _______________\n"
        "Signert rådgiver økonomi: _____________________   Dato: _______________"
    )

    doc.save(filename_docx)

    md_content = f"""# 📋 MAL: AVVIKSNOTAT OG PRESKRIPTIV TILTAKSPLAN
**Enhet:** [Sett inn enhet] | **KOSTRA-funksjon:** [202 / 254] | **Periode:** 2. Tertial 2026  
**Mottaker:** Kommunalsjef / Sektorledelse | **Saksbehandler:** Enhetsleder & Controller  

---

## 1. AVVIKSBILDE OG ÅRSAKSFORKLARING
- **Faste stillingslønninger (Art 1010):** [Beskrivelse av faktisk vs. budsjett]
- **Vikarforbruk (Art 1020/1050):** [Korttids- vs. langtidsfravær]
- **Overtid (Art 1040/1090):** [Turnusdekning, helgetillegg]
- **Konsulenter / Private (Art 1270):** [Vikarbyråleie]
- **NAV-refusjoner (Art 1690/1170):** [Etterslepanalyse]

---

## 2. PRIORITERT TILTAKSMENY (T1–T6)
| ID | Tiltaksbeskrivelse | Effektbase | Sannsynlighet | Est. EOY-effekt | Governance / HTA § 4 |
| :--- | :--- | ---: | :---: | ---: | :--- |
| **T1** | Purring av NAV-refusjoner | 732 705 kr | 85 % | 41 324 kr | `KREVER FAGKONTROLL` |
| **T2** | Redusere vikarbyrå via vikarpool | 612 450 kr | 70 % | 28 872 kr | `KREVER HR/TARIFF` |
| **T3** | Overtidsplanlegging og godkjenning | 1 105 444 kr | 75 % | 55 077 kr | `KREVER HR/TARIFF` |
| **T4** | Kjøpestopp ikke-kritiske varer | 155 776 kr | 90 % | 9 520 kr | `KREVER FAGKONTROLL` |
| **T5** | Helgeturnus- og kapasitetsanalyse | 4 789 479 kr | 60 % | 27 474 kr | `KREVER HR/TARIFF` |
| **T6** | Digital ressursstyring | 17 233 691 kr | 60 % | 30 701 kr | `KREVER FAGKONTROLL` |

---

## 3. FORMELT HITL SIGN-OFF
- Beslutning: `[ GODKJENT / ENDRET / AVVIST ]`
- Kontroll dokumentert: `[ JA / NEI ]`
- Begrunnelse: [Saksbehandlers skriftlige vurdering]
- SHA-256 revisjonsstempel genereres i Control Office Hub.
"""
    filename_md.write_text(md_content, encoding="utf-8")
    print(f"✓ Avviksnotat-mal generert: {filename_docx.name} & {filename_md.name}")


# ==============================================================================
# 3. MAL: HTA § 4 DRØFTINGSPROTOKOLL (PARTSSAMARBEID)
# ==============================================================================
def create_hta_protokoll_template():
    filename_docx = TEMPLATES_DIR / "MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.docx"
    filename_md = TEMPLATES_DIR / "MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.md"

    doc = docx.Document()
    add_document_header(
        doc,
        title="DRØFTINGSPROTOKOLL: HOVEDTARIFFVTALEN § 4",
        subtitle="Protokoll for drøfting av turnusendringer, overtidsbegrensning og vikarbruk",
        ref_code="PROT-HTA-2026-v1"
    )

    doc.add_paragraph(
        "Møtested: Kristiansand rådhus / Digitalt Teams-møte\n"
        "Dato og tidspunkt: [Sett inn dato]\n"
        "Hjemmel: Hovedtariffavtalen (HTA) § 4, Hovedavtalen del B § 3 og Arbeidsmiljøloven kap. 10\n"
        "Deltakere:\n"
        "• For arbeidsgiver: Enhetsleder [Navn], Rådgiver HR [Navn], Controller [Navn]\n"
        "• For arbeidstakerorganisasjonene: Tillitsvalgt Fagforbundet [Navn], Tillitsvalgt Delta [Navn], Tillitsvalgt NSF / Utdanningsforbundet [Navn]"
    )

    doc.add_heading(level=2).add_run("1. SAKENS FORMÅL").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "Drøfting av økonomiske innstrammingstiltak knyttet til bemanningsplan, overtid og vikarbruk for å sikre "
        "budsjettbalanse jf. Kommuneloven § 14-5, samtidig som et fullt forsvarlig arbeidsmiljø og lovpålagte "
        "tjenestekrav opprettholdes jf. HTA § 4."
    )

    doc.add_heading(level=2).add_run("2. ARBEIDSGIVERS REDEGJØRELSE").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "Arbeidsgiver presenterte regnskapsstatus per 2. tertial, som viser et samlet merforbruk på lønn og vikarer "
        "på kr [Beløp]. For å gjenopprette balanse foreslås følgende operative justeringer:\n"
        "1. Forhåndsgodkjenning av overtid av leder (unntak ved akutt fare for liv og helse).\n"
        "2. Primær bruk av kommunens interne vikarpool før innleie fra kommersielle vikarbyråer.\n"
        "3. Gjennomgang av helgeturnus for å jevne ut vaktbelastning og redusere behovet for doble vakter."
    )

    doc.add_heading(level=2).add_run("3. ARBEIDSTAKERNES BEMERKNINGER").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "De tillitsvalgte uttalte:\n"
        "• [Sett inn merknad, f.eks.: Fagforbundet understreker viktigheten av at vikarpoolen har tilstrekkelig kompetanse på brukergruppen.]\n"
        "• [Sett inn merknad, f.eks.: NSF påpeker at helgebemanningen må ivareta forsvarlig legemiddelhåndtering.]\n"
        "• [Sett inn merknad, f.eks.: Partene er enige om at HMS og hviletidsbestemmelser i AML § 10-8 skal overholdes ubetinget.]"
    )

    doc.add_heading(level=2).add_run("4. KONKLUSJON & VIDERE OPPFØLGING").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "Partene er enige om følgende oppfølging:\n"
        "• Tiltakene iverksettes med virkning fra [Dato].\n"
        "• Evaluering gjennomføres i nytt partssammensatt møte om 6 uker.\n"
        "• Avvik fra hviletid eller økning i sykefravær skal meldes verneombud umiddelbart."
    )

    doc.add_paragraph(
        "\n\nUnderskrifter:\n\n"
        "For arbeidsgiver: ______________________      For Fagforbundet: ______________________\n\n"
        "For Delta: _____________________________      For NSF / Utd.forb: ____________________"
    )

    doc.save(filename_docx)

    md_content = f"""# 🤝 MAL: DRØFTINGSPROTOKOLL — HOVEDTARIFFVTALEN (HTA) § 4
**Tema:** Drøfting av turnusendringer, overtidsbegrensning og vikarbruk  
**Hjemmel:** HTA § 4, Hovedavtalen del B § 3 & Arbeidsmiljøloven kap. 10  
**Virksomhet:** Kristiansand kommune | Enhet: [Navn]  

---

## 1. MØTEDELTAKERE
- **Arbeidsgiver:** Enhetsleder, HR-rådgiver, Økonomirådgiver
- **Tillitsvalgte:** Fagforbundet, Delta, Norsk Sykepleierforbund, Utdanningsforbundet

---

## 2. ARBEIDSGIVERS FORSLAG TIL TILTAK
1. **Overtid:** Krav om skriftlig forhåndsgodkjenning av overtid (art 1040/1090).
2. **Vikarbruk:** Prioritert bruk av kommunens interne vikarpool framfor eksterne byråer (art 1270).
3. **Turnus:** Kapasitetsjustering av helgevakter iht. AML § 10-8.

---

## 3. TILLITSVALGTES VURDERING
- Faglig forsvarlighet og pasient-/elevsikkerhet
- Belastning på faste ansatte og arbeidsmiljø (HMS)
- Eventuelle protokolltilførsler

---

## 4. KONKLUSJON & PROTKOLLUNDERSKRIFT
Protokollen registreres i arkiv og legges ved som obligatorisk dokumentasjon i Stage-Gate Port 8 og politisk saksfremlegg.
"""
    filename_md.write_text(md_content, encoding="utf-8")
    print(f"✓ HTA § 4 Protokoll generert: {filename_docx.name} & {filename_md.name}")


# ==============================================================================
# 4. MAL: STAGE-GATE PORT 9 HITL SIGNOFF PROTOKOLL
# ==============================================================================
def create_stage_gate_signoff_template():
    filename_docx = TEMPLATES_DIR / "MAL_STAGE_GATE_PORT_9_HITL_SIGNOFF.docx"
    filename_md = TEMPLATES_DIR / "MAL_STAGE_GATE_PORT_9_HITL_SIGNOFF.md"

    doc = docx.Document()
    add_document_header(
        doc,
        title="STAGE-GATE PORT 9: HUMAN-IN-THE-LOOP SIGNOFF",
        subtitle="Menneskelig overprøving og uforanderlig SHA-256 revisjonslogg (EU AI Act Art. 14 & GDPR Art. 22)",
        ref_code="GATE-09-HITL-2026"
    )

    doc.add_paragraph(
        "Kvalitetsport 9 utgjør den ufravikelige kontrollbarrieren mellom AI-assistert analyse og administrative vedtak i Kristiansand kommune.\n"
        "AI-systemer fatter 0 autonome vedtak. En kvalifisert saksbehandler må gjennomgå, vurdere og signere enhver anbefaling."
    )

    t = doc.add_table(rows=8, cols=2)
    fields = [
        ("Saksreferanse / AI Anomali-ID:", "ANOM-2026-T2-0894 / KOSTRA 202 & 254"),
        ("Saksbehandler / Rolle:", "Frank Ellingsen — Senior Controller"),
        ("AI-Modell & Konfidensgrad:", "Kommune AI Guardrails / Ollama llama3.1 (Konfidensscore: 94 %)"),
        ("Status Beslutning:", "[ X ] APPROVED (Godkjent)   [  ] MODIFIED (Endret)   [  ] REJECTED (Avvist)"),
        ("Kontroll dokumentert jf. instruks:", "[ X ] JA     [  ] NEI"),
        ("Saksbehandlers faglige begrunnelse:", "Avvik på vikarer og overtid er bekreftet i Visma ERP. Foreslåtte tiltak T1–T4 er forankret i delegeringsreglementet og HTA § 4. Ingen pasientsikkerhet eller lovkrav svekkes."),
        ("Kryptografisk Hash (SHA-256):", "7f8a9b2c3d4e5f6a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a"),
        ("Lagret i revisjonsdatabase:", "SQLite kommune_golden_record.db -> Tabell: Audit_AI_Actions")
    ]
    for i, (lbl, val) in enumerate(fields):
        r = t.rows[i]
        c0, c1 = r.cells[0], r.cells[1]
        c0.width = Inches(2.5)
        c1.width = Inches(4.0)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 60, 60, 80, 80)
        set_cell_margins(c1, 60, 60, 80, 80)
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(lbl)
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(9)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_NAVY
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(9)
        if "SHA-256" in lbl:
            r1.font.name = "Consolas"
            r1.font.size = Pt(8)
            r1.font.bold = True

    doc.add_paragraph("\nElektronisk signatur forseglet i Control Office Hub jf. Kommuneloven kap. 24 og EU AI Act Art. 14.")
    doc.save(filename_docx)

    md_content = f"""# 🛡️ MAL: STAGE-GATE PORT 9 — HITL SIGNOFF PROTOKOLL
**Hjemmel:** EU AI Act Art. 14 (Human Oversight), GDPR Art. 22 (Forbud mot helautomatisering)  
**System:** Kristiansand Kommune — Control Office Hub  

---

## KONTROLLSKJEMA FOR SAKSBEHANDLER:
- **Saksnummer:** [ANOM-2026-T2-XXXX]
- **Saksbehandler:** [Navn, Tittel]
- **AI-modell & Konfidensgrad:** [Ollama llama3.1 / Gemini 3.8 Flash, XX %]
- **Beslutning:** `[ APPROVED / MODIFIED / REJECTED ]`
- **Kontroll dokumentert:** `[ JA / NEI ]`
- **Faglig begrunnelse:** [Skriftlig redegjørelse for vurderingen]
- **Kryptografisk Hash:** `SHA-256: [64 tegn heksadesimal hash]`
- **Arkivering:** Skrives til `Audit_AI_Actions` for innsyn av Kommunerevisjonen.
"""
    filename_md.write_text(md_content, encoding="utf-8")
    print(f"✓ Stage-Gate Port 9 Signoff-mal generert: {filename_docx.name} & {filename_md.name}")


# ==============================================================================
# 5. MAL: FRIA & DPIA KONSEKVENSVURDERING (EU AI ACT ART. 27 & GDPR ART. 35)
# ==============================================================================
def create_fria_dpia_template():
    filename_docx = TEMPLATES_DIR / "MAL_FRIA_OG_DPIA_RISIKOVURDERING.docx"
    filename_md = TEMPLATES_DIR / "MAL_FRIA_OG_DPIA_RISIKOVURDERING.md"

    doc = docx.Document()
    add_document_header(
        doc,
        title="STAGE-GATE PORT 7: FRIA & DPIA VURDERING",
        subtitle="Konsekvensvurdering for Grunnleggende Rettigheter (EU AI Act Art. 27) og Personvern (GDPR Art. 35)",
        ref_code="GATE-07-FRIA-DPIA"
    )

    doc.add_paragraph(
        "Offentlig sektor i Norge er underlagt strenge krav ved innføring av AI-systemer som påvirker tjenestetilbud og ressursallokering.\n"
        "Denne vurderingen krever eksplisitt godkjenning fra Personvernombud (DPO) og juridisk rådgiver, med absolutt VETORETT ved uakseptabel risiko."
    )

    doc.add_heading(level=2).add_run("1. SYSTEMBESKRIVELSE & FORMÅL").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "System: Antigravity EPM & Kommune AI Guardrails (Kristiansand kommune)\n"
        "Formål: Rådgivende beslutningsstøtte for tidligvarsling av budsjettavvik og preskriptiv tiltaksanalyse.\n"
        "Klassifisering: Beslutningsstøtte uten autonom vedtaksmyndighet (High Oversight Low Autonomy)."
    )

    doc.add_heading(level=2).add_run("2. PERSONVERN & DATAMINIMERING (GDPR ART. 5 & 35)").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "• Behandles personopplysninger? NEI. All regnskaps- og lønnsdata er aggregert på KOSTRA-art og kostnadssted.\n"
        "• PII-filter i Port 4: Automatisk regex- og NER-vasking fjerner eventuelle fødselsnumre, navn eller personadresser i bilagstekst.\n"
        "• Lagring: 100 % lokal lagring i SQLite/DuckDB bak kommunens brannmur. Ingen data deles med eksterne AI-tjenester uten eksplisitt DPA."
    )

    doc.add_heading(level=2).add_run("3. GRUNNLEGGENDE RETTIGHETER & ANTI-BIAS (EU AI ACT ART. 27)").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "• Likebehandling: Statistisk likebehandling mellom virksomhetsenheter (ingen skjevhet mot enkeltskoler eller boenheter).\n"
        "• Pasientsikkerhet & Elevrettigheter: AI-modellen har sperre mot å foreslå kutt i lovpålagte enkeltvedtak (spesialundervisning, 1-til-1 pleie).\n"
        "• Arbeidstakerrettigheter: Tiltak som berører arbeidstid krever obligatorisk partssamarbeid jf. HTA § 4."
    )

    doc.add_heading(level=2).add_run("4. KONKLUSJON & DPO-GODKJENNING").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "Konklusjon: Restrisiko er vurdert som LAV.\n\n"
        "Personvernombud (DPO): ______________________   Status: [ X ] GODKJENT   [  ] VETO\n"
        "Juridisk rådgiver: ___________________________   Dato: ___________________"
    )

    doc.save(filename_docx)

    md_content = f"""# 🛡️ MAL: STAGE-GATE PORT 7 — FRIA & DPIA VURDERING
**Hjemmel:** EU AI Act Art. 27 (FRIA), GDPR Art. 35 (DPIA), Kommuneloven § 13-1  
**Ansvarlig:** DPO / Personvernombud og Juridisk direktør (Obligatorisk Vetorett)  

---

## 1. FORMÅL & METODE
Konsekvensvurdering for innføring av AI-drevet tidligvarsling og preskriptiv tiltaksstøtte for økonomi i Kristiansand kommune.

## 2. KONTROLLOMRÅDER
1. **Dataminimering (GDPR Art. 5):** Aggregerte lønnsposter; 0 personidentifiserbare data.
2. **Ingen profilering (GDPR Art. 22):** Analysen evaluerer KOSTRA-arter, aldri individuelle arbeidstakere.
3. **Anti-bias & rettferdighet (Art. 27):** Objektiv $Z$-score avviksscreening.
4. **Veto-myndighet:** DPO og juridisk rådgiver kan stanse systemet ved mistanke om brudd på grunnleggende rettigheter.
"""
    filename_md.write_text(md_content, encoding="utf-8")
    print(f"✓ FRIA & DPIA-mal generert: {filename_docx.name} & {filename_md.name}")


# ==============================================================================
# 6. MAL: PERIODELUKKING OG AVSTEMMINGSRUTINE
# ==============================================================================
def create_periodelukking_template():
    filename_docx = TEMPLATES_DIR / "MAL_PERIODELUKKING_OG_AVSTEMMING.docx"
    filename_md = TEMPLATES_DIR / "MAL_PERIODELUKKING_OG_AVSTEMMING.md"

    doc = docx.Document()
    add_document_header(
        doc,
        title="KONTROLLINSTRUKS: PERIODELUKKING & AVSTEMMING",
        subtitle="Månedlig og tertialvis rutine for kommunal controller og regnskapsavdeling",
        ref_code="INST-LUKKING-2026"
    )

    doc.add_paragraph(
        "Denne instruksen fastsetter obligatoriske avstemmingskontroller for å sikre korrekt regnskapsrapportering "
        "og etterlevelse av god kommunal regnskapsskikk (GKRS) og Kommuneloven kap. 14."
    )

    doc.add_heading(level=2).add_run("1. MÅNEDLIGE HOVEDKONTROLLER (DAG 1–5 ETTER MÅNEDSSLUTT)").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "1. Bankavstemming: Fullstendig avstemming av samtlige drifts- og skattekontoer.\n"
        "2. A-melding: Avstemming av lønns- og trekkontoer mot kvittering fra Skatteetaten.\n"
        "3. Leverandørreskontro: Avstemming av uoppgjorte poster og fakturamottak i Visma.\n"
        "4. Kundreskontro: Purring og renteberegning av kommunale krav og gebyrer."
    )

    doc.add_heading(level=2).add_run("2. TERTIALVIS LUKKING & PROGNOSE (T1, T2, T3)").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "1. Periodisering av kjente inntekter og utgifter jf. anordningsprinsippet (§ 14-6).\n"
        "2. Validering av NAV sykepengerefusjoner (art 1690) og avstemming mot sykefraværsstatistikk.\n"
        "3. Kjøring av EOY-prognose i Power BI / DuckDB for tidligvarsling av avvik.\n"
        "4. Klargjøring av administrativt tiltaksnotat til kommunalsjef jf. Stage-Gate Port 9."
    )

    doc.save(filename_docx)

    md_content = f"""# 📑 MAL: KONTROLLINSTRUKS FOR PERIODELUKKING OG AVSTEMMING
**Målgruppe:** Controllere, økonomirådgivere og regnskapsførere  
**Hjemmel:** Kommuneloven kap. 14, regnskapsforskriften & GKRS  

---

## 1. MÅNEDSLUKKING (SJEKKLISTE)
- [ ] Bankavstemminger godkjent
- [ ] A-melding avstemt mot lønnsarter
- [ ] Mellomregningskontoer i null
- [ ] Mva-kompensasjon (Kontoklasse 2) kontrollert

## 2. TERTIALRAPPORT (AVSTEMMINGSFLYTER)
- [ ] Diff-sjekk Visma ERP vs. Framsikt EPM
- [ ] Refusjonskrav mot NAV registrert
- [ ] EOY Rullende prognose beregnet
- [ ] SHA-256 forsegling i Audit Trail
"""
    filename_md.write_text(md_content, encoding="utf-8")
    print(f"✓ Periodelukkings-mal generert: {filename_docx.name} & {filename_md.name}")


# ==============================================================================
# 7. MAL: EXCEL ARBEIDSBOK FOR SAKSBEHANDLING & TILTAK (Edward Tufte Standard)
# ==============================================================================
def create_saksbehandling_excel_model():
    excel_path = REPORTS_DIR / "Mal_Saksbehandling_Tiltak_Avstemming_2026.xlsx"

    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # Fjern standardark

    # Farger & Fonter
    f_title = Font(name="Segoe UI", size=14, bold=True, color="1B365D")
    f_sub = Font(name="Segoe UI", size=9.5, italic=True, color="64748B")
    f_head = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")
    f_bold = Font(name="Segoe UI", size=9.5, bold=True, color="1E293B")
    f_reg = Font(name="Segoe UI", size=9.5, color="1E293B")
    f_muted = Font(name="Segoe UI", size=8.5, color="64748B")
    f_red = Font(name="Segoe UI", size=9.5, bold=True, color="C0392B")
    f_green = Font(name="Segoe UI", size=9.5, bold=True, color="15803D")

    fill_navy = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    fill_tot = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    fill_alert = PatternFill(start_color="FDF2F2", end_color="FDF2F2", fill_type="solid")
    fill_success = PatternFill(start_color="F0FDF4", end_color="F0FDF4", fill_type="solid")

    b_thin = Side(style="thin", color="CBD5E1")
    b_double = Side(style="double", color="1B365D")
    border_head = Border(top=b_thin, bottom=b_thin)
    border_row = Border(bottom=Side(style="thin", color="E2E8F0"))
    border_tot = Border(top=b_thin, bottom=b_double)

    # --------------------------------------------------------------------------
    # FANE 1: AVVIKSANALYSE PER KOSTRA ART
    # --------------------------------------------------------------------------
    ws1 = wb.create_sheet(title="Avviksanalyse_KOSTRA")
    ws1.views.sheetView[0].showGridLines = True
    ws1.cell(row=2, column=2, value="🏛️ KRISTIANSAND KOMMUNE — AVVIKSANALYSE KOSTRA ART").font = f_title
    ws1.cell(row=3, column=2, value="Måneds- og tertialavstemming jf. bruttoprinsippet (Kommuneloven § 14-6)").font = f_sub

    headers1 = ["KOSTRA Art", "Art Navn", "Enhet / Ansvar", "Periodisert Budsjett", "Faktisk Regnskap", "Avvik i NOK", "Avvik %", "Status Vurdering"]
    for c, h in enumerate(headers1, start=2):
        cell = ws1.cell(row=5, column=c, value=h)
        cell.font = f_head
        cell.fill = fill_navy
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_head

    rows_data1 = [
        ("1010", "Fast lønn lærere / ansatte", "4100 Kommunal Skole", 15729000, 18197000, "Kritisk merforbruk"),
        ("1020", "Sykemeldte vikarer", "4100 Kommunal Skole", 202000, 847000, "Kritisk merforbruk"),
        ("1040", "Overtidslønn", "4100 Kommunal Skole", 57000, 436000, "Kritisk merforbruk"),
        ("1090", "Arbeidsgiveravgift & pensjon", "4100 Kommunal Skole", 3785000, 4216000, "Merforbruk"),
        ("1200", "Innkjøp undervisningsmateriell", "4100 Kommunal Skole", 450000, 520000, "Avvik"),
        ("1690", "Sykelønnsrefusjon NAV", "4100 Kommunal Skole", -350000, -180000, "Etterslep refusjon"),
        ("1010", "Fast lønn helsefagarbeidere", "5200 Bo og Miljø", 28450000, 29200000, "Merforbruk"),
        ("1040", "Overtidslønn og helgetillegg", "5200 Bo og Miljø", 1450000, 2980000, "Kritisk merforbruk"),
        ("1050", "Ekstrahjelp og timevikarer", "5200 Bo og Miljø", 1120000, 1940000, "Kritisk merforbruk"),
        ("1270", "Kjøp fra private / vikarbyrå", "5200 Bo og Miljø", 0, 382656, "Ubudsjettert sprek"),
        ("1690", "Sykelønnsrefusjon NAV", "5200 Bo og Miljø", -850000, -420000, "Etterslep refusjon"),
    ]

    for idx, r in enumerate(rows_data1, start=6):
        art, navn, enh, bud, reg, stat = r
        ws1.cell(row=idx, column=2, value=art).font = f_bold
        ws1.cell(row=idx, column=3, value=navn).font = f_reg
        ws1.cell(row=idx, column=4, value=enh).font = f_reg
        
        c_bud = ws1.cell(row=idx, column=5, value=bud)
        c_bud.font = f_reg
        c_bud.number_format = '#,##0 "kr"'
        c_bud.alignment = Alignment(horizontal="right")

        c_reg = ws1.cell(row=idx, column=6, value=reg)
        c_reg.font = f_reg
        c_reg.number_format = '#,##0 "kr"'
        c_reg.alignment = Alignment(horizontal="right")

        # Excel formel: Budsjett - Regnskap (negativt = merforbruk)
        c_avv = ws1.cell(row=idx, column=7, value=f"=E{idx}-F{idx}")
        c_avv.font = f_red if "merforbruk" in stat or "sprek" in stat else f_reg
        c_avv.number_format = '#,##0 "kr"'
        c_avv.alignment = Alignment(horizontal="right")

        # Excel formel: Avvik %
        c_pst = ws1.cell(row=idx, column=8, value=f"=IF(E{idx}<>0, G{idx}/ABS(E{idx}), 0)")
        c_pst.font = f_red if "merforbruk" in stat or "sprek" in stat else f_reg
        c_pst.number_format = '0.0%'
        c_pst.alignment = Alignment(horizontal="right")

        c_stat = ws1.cell(row=idx, column=9, value=stat)
        c_stat.font = f_red if "Kritisk" in stat else f_reg
        if "Kritisk" in stat:
            c_stat.fill = fill_alert

        for c in range(2, 10):
            ws1.cell(row=idx, column=c).border = border_row

    # Sum-rad
    tot_row = len(rows_data1) + 6
    ws1.cell(row=tot_row, column=2, value="TOTALT").font = f_bold
    ws1.cell(row=tot_row, column=3, value="Konsolidert kontrollutvalg").font = f_bold
    ws1.cell(row=tot_row, column=4, value="Alle enheter").font = f_bold
    
    ws1.cell(row=tot_row, column=5, value=f"=SUM(E6:E{tot_row-1})").font = f_bold
    ws1.cell(row=tot_row, column=5).number_format = '#,##0 "kr"'
    ws1.cell(row=tot_row, column=5).alignment = Alignment(horizontal="right")

    ws1.cell(row=tot_row, column=6, value=f"=SUM(F6:F{tot_row-1})").font = f_bold
    ws1.cell(row=tot_row, column=6).number_format = '#,##0 "kr"'
    ws1.cell(row=tot_row, column=6).alignment = Alignment(horizontal="right")

    ws1.cell(row=tot_row, column=7, value=f"=SUM(G6:G{tot_row-1})").font = f_red
    ws1.cell(row=tot_row, column=7).number_format = '#,##0 "kr"'
    ws1.cell(row=tot_row, column=7).alignment = Alignment(horizontal="right")

    ws1.cell(row=tot_row, column=8, value=f"=G{tot_row}/ABS(E{tot_row})").font = f_red
    ws1.cell(row=tot_row, column=8).number_format = '0.0%'
    ws1.cell(row=tot_row, column=8).alignment = Alignment(horizontal="right")

    ws1.cell(row=tot_row, column=9, value="SAMLET DRIFTSMERFORBRUK").font = f_red

    for c in range(2, 10):
        cell = ws1.cell(row=tot_row, column=c)
        cell.border = border_tot
        cell.fill = fill_tot

    # --------------------------------------------------------------------------
    # FANE 2: PRESKRIPTIV TILTAKSPLAN (T1–T6)
    # --------------------------------------------------------------------------
    ws2 = wb.create_sheet(title="Preskriptiv_Tiltaksplan")
    ws2.views.sheetView[0].showGridLines = True
    ws2.cell(row=2, column=2, value="🎯 KRISTIANSAND KOMMUNE — PRESKRIPTIV TILTAKSPLAN (T1–T6)").font = f_title
    ws2.cell(row=3, column=2, value="Risikovektede innsparingstiltak med Stage-Gate kontroll og tariffbetingelser (HTA § 4)").font = f_sub

    headers2 = ["ID", "Tiltaksbeskrivelse", "Horisont", "Effektbase", "Sannsynlighet", "Beregnet Effekt", "HTA § 4 Status", "Beslutning", "Kontroll Dok.", "Effekt i Modell"]
    for c, h in enumerate(headers2, start=2):
        cell = ws2.cell(row=5, column=c, value=h)
        cell.font = f_head
        cell.fill = fill_navy
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_head

    tiltak_rows = [
        ("T1", "Oppfølging og purring av NAV refusjonskrav", "Kort", 732705, 0.85, "KREVER FAGKONTROLL", "Godkjent", "Ja"),
        ("T2", "Redusere vikarbyrå via kommunal vikarpool", "Kort", 612450, 0.70, "KREVER HR/TARIFF (HTA § 4)", "Godkjent", "Ja"),
        ("T3", "Overtidsplanlegging og forhåndsgodkjenning", "Kort", 1105444, 0.75, "KREVER HR/TARIFF (HTA § 4)", "Godkjent", "Ja"),
        ("T4", "Stopp i ikke-kritiske rammeavtaleinnkjøp", "Kort", 155776, 0.90, "KREVER FAGKONTROLL", "Godkjent", "Ja"),
        ("T5", "Turnus- og bemanningsanalyse for helgevakter", "Lang", 4789479, 0.60, "KREVER HR/TARIFF (HTA § 4)", "Kandidat", "Nei"),
        ("T6", "Digital ressursstyring og vaktbokintegrasjon", "Lang", 17233691, 0.60, "KREVER FAGKONTROLL", "Kandidat", "Nei"),
    ]

    for idx, t in enumerate(tiltak_rows, start=6):
        tid, desc, hor, base, prob, tariff, beslutn, dok = t
        ws2.cell(row=idx, column=2, value=tid).font = f_bold
        ws2.cell(row=idx, column=3, value=desc).font = f_reg
        ws2.cell(row=idx, column=4, value=hor).font = f_muted
        
        c_base = ws2.cell(row=idx, column=5, value=base)
        c_base.font = f_reg
        c_base.number_format = '#,##0 "kr"'
        c_base.alignment = Alignment(horizontal="right")

        c_prob = ws2.cell(row=idx, column=6, value=prob)
        c_prob.font = f_reg
        c_prob.number_format = '0%'
        c_prob.alignment = Alignment(horizontal="right")

        # Formel for beregnet effekt
        c_eff = ws2.cell(row=idx, column=7, value=f"=E{idx}*F{idx}*0.06")
        c_eff.font = f_green
        c_eff.number_format = '#,##0 "kr"'
        c_eff.alignment = Alignment(horizontal="right")

        c_tar = ws2.cell(row=idx, column=8, value=tariff)
        c_tar.font = f_red if "HTA" in tariff else f_muted

        c_bes = ws2.cell(row=idx, column=9, value=beslutn)
        c_bes.font = f_bold
        c_bes.alignment = Alignment(horizontal="center")

        c_dok = ws2.cell(row=idx, column=10, value=dok)
        c_dok.font = f_bold
        c_dok.alignment = Alignment(horizontal="center")

        # Tvingende HITL formel: =IF(AND(I6="Godkjent", J6="Ja"), G6, 0)
        c_mod = ws2.cell(row=idx, column=11, value=f'=IF(AND(I{idx}="Godkjent", J{idx}="Ja"), G{idx}, 0)')
        c_mod.font = f_bold
        c_mod.number_format = '#,##0 "kr"'
        c_mod.alignment = Alignment(horizontal="right")
        c_mod.fill = fill_success if dok == "Ja" else fill_zebra

        for c in range(2, 12):
            ws2.cell(row=idx, column=c).border = border_row

    # Sum tiltak
    s_row = len(tiltak_rows) + 6
    ws2.cell(row=s_row, column=2, value="TOTALT").font = f_bold
    ws2.cell(row=s_row, column=3, value="Sum realiserbare tiltak i 2026").font = f_bold
    ws2.cell(row=s_row, column=7, value=f"=SUM(G6:G{s_row-1})").font = f_bold
    ws2.cell(row=s_row, column=7).number_format = '#,##0 "kr"'
    ws2.cell(row=s_row, column=7).alignment = Alignment(horizontal="right")

    ws2.cell(row=s_row, column=11, value=f"=SUM(K6:K{s_row-1})").font = f_green
    ws2.cell(row=s_row, column=11).number_format = '#,##0 "kr"'
    ws2.cell(row=s_row, column=11).alignment = Alignment(horizontal="right")
    
    for c in range(2, 12):
        cell = ws2.cell(row=s_row, column=c)
        cell.border = border_tot
        cell.fill = fill_tot

    # --------------------------------------------------------------------------
    # FANE 3: HITL SIGNOFF PROTOKOLL
    # --------------------------------------------------------------------------
    ws3 = wb.create_sheet(title="HITL_Signoff_Protokoll")
    ws3.views.sheetView[0].showGridLines = True
    ws3.cell(row=2, column=2, value="🛡️ KRISTIANSAND KOMMUNE — STAGE-GATE PORT 9 HITL SIGNOFF").font = f_title
    ws3.cell(row=3, column=2, value="Menneskelig overprøving og uforanderlig SHA-256 forsegling jf. EU AI Act Art. 14").font = f_sub

    sign_fields = [
        ("Saksnummer:", "SAK-2026-T2-08940"),
        ("Saksbehandler / Tittel:", "Frank Ellingsen — Senior Controller"),
        ("Tjenesteområde:", "Oppvekst (Skole) og Helse/Mestring (Bo og Miljø)"),
        ("Dato for godkjenning:", datetime.date.today().strftime("%Y-%m-%d")),
        ("Status Beslutning:", "APPROVED (Godkjent administrativt tiltaksnivå)"),
        ("Faglig begrunnelse:", "Avvik i vikarutgifter bekreftet i Visma ERP. Tiltak T1–T4 iverksettes umiddelbart innenfor delegert ramme. Resterende merforbruk fremmes for Bystyret."),
        ("Medbestemmelse (HTA § 4):", "Drøftet med Fagforbundet og Utdanningsforbundet. Ingen merknader til midlertidig vikarpool."),
        ("Kryptografisk Hash (SHA-256):", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
        ("Arkivreferanse Public360:", "DOC-2026-99214-FINAL")
    ]

    r_idx = 5
    for lbl, val in sign_fields:
        c1 = ws3.cell(row=r_idx, column=2, value=lbl)
        c1.font = f_bold
        c1.fill = fill_zebra
        c1.border = border_row
        
        c2 = ws3.cell(row=r_idx, column=3, value=val)
        c2.font = f_reg
        c2.border = border_row
        if "SHA-256" in lbl:
            c2.font = Font(name="Consolas", size=9.5, color="1B365D", bold=True)
        r_idx += 1

    # Autotilpass kolonner
    for ws in [ws1, ws2, ws3]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            if col[0].column == 1:
                ws.column_dimensions[col_letter].width = 3
                continue
            for cell in col:
                val_str = str(cell.value or "")
                if cell.row in [2, 3]:
                    continue
                max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    wb.save(excel_path)
    print(f"✓ Excel Saksbehandlingsmodell generert: {excel_path.name}")


# ==============================================================================
# 8. MAL: KOMMUNESTYRET / BYSTYRET (NIVÅ 1)
# ==============================================================================
def create_rapportmal_kommunestyret():
    filename_docx = TEMPLATES_DIR / "RAPPORTMAL_KOMMUNESTYRET.docx"
    doc = docx.Document()
    add_document_header(
        doc,
        title="MÅNEDLIG AVVIKS- OG TILTAKSRAPPORT — KOMMUNESTYRET / BYSTYRET",
        subtitle="Månedlig strategisk økonomirapport for Bystyret jf. Kommuneloven § 14-5",
        ref_code="RAP-2026-M09-BYSTYRE"
    )

    doc.add_heading(level=2).add_run("EXECUTIVE SUMMARY (BYSTYRET):").font.color.rgb = COLOR_NAVY
    p_meta = doc.add_paragraph(
        "• Rapporteringsperiode: Måned 9 (September) / 2026\n"
        "• Samlet netto driftsavvik: +94,9 mill. kr (+1.9 % av årsbudsjett)\n"
        "• Prognose EOY (31.12): +116,5 mill. kr i forventet merforbruk\n"
        "• Kritiske saksforhold som krever politisk vedtak: 2 saker (Helse og Mestring / Disposisjonsfond)"
    )

    doc.add_heading(level=3).add_run("1. Sektorvis Avviksoversikt (Bystyrenivå):")
    t = doc.add_table(rows=7, cols=6)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdrs = ["Kommunalsjefområde", "Vedtatt Ramme", "Påløpt Hittil", "Avvik Hittil", "EOY Prognose", "Status"]
    for i, h in enumerate(hdrs):
        c = t.rows[0].cells[i]
        set_cell_background(c, "1B365D")
        set_cell_margins(c, 80, 80, 80, 80)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    data = [
        ("Oppvekst & Grunnskole", "2 450 MNOK", "1 685 MNOK", "+38,5 MNOK (+2.3%)", "+45,0 MNOK", "🔴 Kritiske avvik"),
        ("Helse & Mestring", "3 100 MNOK", "2 140 MNOK", "+62,0 MNOK (+2.9%)", "+78,0 MNOK", "🔴 Kritiske avvik"),
        ("By- og Stedsutvikling", "850 MNOK", "560 MNOK", "-4,2 MNOK (-0.8%)", "-5,0 MNOK", "🟢 Innenfor ramme"),
        ("Kultur & Innbyggerdialog", "420 MNOK", "280 MNOK", "+1,1 MNOK (+0.4%)", "+1,5 MNOK", "🟡 Mildt avvik"),
        ("Sentralstyring & Staber", "680 MNOK", "450 MNOK", "-2,5 MNOK (-0.6%)", "-3,0 MNOK", "🟢 Innenfor ramme"),
        ("TOTALT DRIFT", "7 500 MNOK", "5 115 MNOK", "+94,9 MNOK (+1.9%)", "+116,5 MNOK", "🔴 Kritiske avvik")
    ]
    for r_idx, row_data in enumerate(data, start=1):
        for c_idx, val in enumerate(row_data):
            cell = t.rows[r_idx].cells[c_idx]
            bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            if r_idx == 6:
                bg = "F1F5F9"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)
            if r_idx == 6 or "🔴" in val:
                r.font.bold = True
            if "🔴" in val:
                r.font.color.rgb = RGBColor(192, 57, 43)

    doc.add_heading(level=2).add_run("2. Forslag til Vedtak (Politiske tiltak):").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "1. Bystyret tar månedlig avviksrapport per september til orientering.\n"
        "2. Bystyret vedtar omdisponering av 15,0 mill. kr fra prosjekt 4021 til drift i Helse og Mestring.\n"
        "3. Bystyret godkjenner bruk av udisponert disposisjonsfond med inntil 25,0 mill. kr dersom EOY-prognosen opprettholdes.\n"
        "4. Kommunedirektøren bes legge frem helhetlig omstillingsplan innen neste bystyremøte."
    )

    doc.add_heading(level=2).add_run("3. Revisorstempel & Sign-off (Stage-Gate Port 9):").font.color.rgb = COLOR_NAVY
    p_sign = doc.add_paragraph(
        "Saksbehandler: Frank Ellingsen (Senior Controller) | Dato: 2026-09-28\n"
        "Kryptografisk Hash: SHA256:a8f9c1e3b2d4f5e6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0"
    )
    p_sign.runs[0].font.name = "Consolas"
    p_sign.runs[0].font.size = Pt(8.5)
    doc.save(filename_docx)
    print(f"✓ Mal generert: {filename_docx.name}")


# ==============================================================================
# 9. MAL: KOMMUNEDIREKTØREN (NIVÅ 2)
# ==============================================================================
def create_rapportmal_kommunedirektor():
    filename_docx = TEMPLATES_DIR / "RAPPORTMAL_KOMMUNEDIREKTOR.docx"
    doc = docx.Document()
    add_document_header(
        doc,
        title="MÅNEDLIG AVVIKS- OG TILTAKSRAPPORT — KOMMUNEDIREKTØREN",
        subtitle="Toppledelsens månedsrapport med administrative direktiver og strakstiltak",
        ref_code="RAP-2026-M09-KOMDIR"
    )

    doc.add_heading(level=2).add_run("OVERSIKT TOPPLEDELSE:").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "• Samlet driftsbudsjett 2026: 7 500 mill. kr (Forbruk hittil: 5 115 mill. kr / 68.2 %)\n"
        "• Påløpt driftsavvik hittil: +94,9 mill. kr | EOY Helårsprognose: +116,5 mill. kr\n"
        "• Sykepengerefusjoner fra NAV (Etterslep > 60 dager): -12,4 mill. kr utestående\n"
        "• Vikarbyråkostnader påløpt: 34,2 mill. kr (85 % av årsrammen er allerede brukt)\n"
        "• Finans- og rentekostnader: -4,5 mill. kr (Mindreforbruk pga. gunstig likviditetsplassering)"
    )

    doc.add_heading(level=2).add_run("ADMINISTRATIVE STRAKSTILTAK (KOMMUNEDIREKTØRENS DIREKTIVER):").font.color.rgb = COLOR_NAVY
    t_act = doc.add_table(rows=5, cols=5)
    t_act.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdrs = ["ID", "Administrativt Strakstiltak", "Ansvarlig", "Frist", "Forventet Effekt"]
    for i, h in enumerate(hdrs):
        c = t_act.rows[0].cells[i]
        set_cell_background(c, "1B365D")
        set_cell_margins(c, 80, 80, 80, 80)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    acts = [
        ("ACT-01", "Ansettelsesstopp for ikke-kritiske stabsstillinger", "HR-direktør", "Umiddelbart", "-8 000 000 kr"),
        ("ACT-02", "Innkjøpsstopp for konsulenttjenester", "Anskaffelsessjef", "Umiddelbart", "-5 000 000 kr"),
        ("ACT-03", "Skjerpet godkjenning av vikarbyråbruk (signaturkrav)", "Kommunalsjefer", "3 dager", "-12 000 000 kr"),
        ("ACT-04", "Purrerutine og dedikert team for NAV-refusjoner", "Regnskapssjef", "5 dager", "+10 000 000 kr likviditet")
    ]
    for r_idx, (aid, desc, ans, fr, eff) in enumerate(acts, start=1):
        for c_idx, val in enumerate([aid, desc, ans, fr, eff]):
            cell = t_act.rows[r_idx].cells[c_idx]
            set_cell_background(cell, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)
            if c_idx == 4:
                r.font.bold = True

    doc.add_heading(level=2).add_run("SIGN-OFF & BESLUTNING:").font.color.rgb = COLOR_NAVY
    p_dec = doc.add_paragraph(
        "Rapport generert av: Controller AI / Seniorrådgiver Frank Ellingsen\n"
        "Kommunedirektørens beslutning: [ APPROVED ] | Dato: 2026-09-28\n"
        "SHA-256: c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8"
    )
    p_dec.runs[0].font.name = "Consolas"
    p_dec.runs[0].font.size = Pt(8.5)
    doc.save(filename_docx)
    print(f"✓ Mal generert: {filename_docx.name}")


# ==============================================================================
# 10. MAL: KOMMUNALSJEF (NIVÅ 3)
# ==============================================================================
def create_rapportmal_kommunalsjef():
    filename_docx = TEMPLATES_DIR / "RAPPORTMAL_KOMMUNALSJEF.docx"
    doc = docx.Document()
    add_document_header(
        doc,
        title="MÅNEDLIG AVVIKS- OG TILTAKSRAPPORT — KOMMUNALSJEF",
        subtitle="Sektorvis månedsrapport — Oppvekst og Grunnskole",
        ref_code="RAP-2026-M09-KOMSJEF-OPPV"
    )

    doc.add_heading(level=2).add_run("SEKTOROVERSIKT OPPVEKST:").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "• Sektorens årsramme: 2 450 000 tNOK | Påløpt avvik hittil: +38 500 tNOK (+2.3 %)\n"
        "• EOY Helårsprognose: +45 000 tNOK (Merforbruk dersom tiltak ikke iverksettes)\n"
        "• Hoveddrivere: Lønnsart 1020 Vikarer (+18.2M / 47.3 %), Art 1090 Overtid (+6.4M), Spesialundervisning (+9.1M)"
    )

    doc.add_heading(level=3).add_run("Enhetsvis Avviksmatrise (Skoler):")
    t_skoler = doc.add_table(rows=6, cols=6)
    t_skoler.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdrs = ["Enhetsnr", "Skole / Virksomhet", "Ramme", "Påløpt", "Avvik", "Status"]
    for i, h in enumerate(hdrs):
        c = t_skoler.rows[0].cells[i]
        set_cell_background(c, "1B365D")
        set_cell_margins(c, 80, 80, 80, 80)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    skoler = [
        ("201", "Grim Skole", "45 000 tNOK", "32 100 tNOK", "+1 800 tNOK (+5.9%)", "🔴 Kritiske avvik"),
        ("202", "Lovisenlev Skole", "52 000 tNOK", "37 400 tNOK", "+3 200 tNOK (+9.3%)", "🔴 Kritiske avvik"),
        ("203", "Tangvall Skole", "68 000 tNOK", "46 100 tNOK", "-800 tNOK (-1.7%)", "🟢 Innenfor ramme"),
        ("204", "Vågsbygd Skole", "74 000 tNOK", "51 200 tNOK", "+2 100 tNOK (+4.3%)", "🟡 Mildt avvik"),
        ("210", "PPT & Fellesenheter", "35 000 tNOK", "23 800 tNOK", "+400 tNOK (+1.7%)", "🟢 Innenfor ramme")
    ]
    for r_idx, row in enumerate(skoler, start=1):
        for c_idx, val in enumerate(row):
            cell = t_skoler.rows[r_idx].cells[c_idx]
            set_cell_background(cell, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)
            if "🔴" in val:
                r.font.bold = True
                r.font.color.rgb = RGBColor(192, 57, 43)

    doc.add_heading(level=2).add_run("SEKTORVISE TILTAK (ACTION ITEMS):").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "• OPP-01: Etablere intern vikarring på tvers av Grim, Lovisenlev og Vågsbygd skoler (-450k/md).\n"
        "• OPP-02: Re-evaluere enkeltvedtak om spesialundervisning (gruppetiltak vs 1-til-1) (-800k/md).\n"
        "• OPP-03: Midlertidig frys i utstyrsinnkjøp og læremidler utover kritiske digitale lisenser (-300k/md)."
    )

    p_sign = doc.add_paragraph(
        "Kommunalsjef Oppvekst: Signert elektronisk | Dato: 2026-09-28\n"
        "SHA-256: d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2"
    )
    p_sign.runs[0].font.name = "Consolas"
    p_sign.runs[0].font.size = Pt(8.5)
    doc.save(filename_docx)
    print(f"✓ Mal generert: {filename_docx.name}")


# ==============================================================================
# 11. MAL: SEKSJONSLEDER / STABSSJEF (NIVÅ 4)
# ==============================================================================
def create_rapportmal_seksjonsleder():
    filename_docx = TEMPLATES_DIR / "RAPPORTMAL_SEKSJONSLEDER.docx"
    doc = docx.Document()
    add_document_header(
        doc,
        title="MÅNEDLIG AVVIKS- OG TILTAKSRAPPORT — SEKSJONSLEDER / STABSSJEF",
        subtitle="Seksjon: Anskaffelser og Innkjøp — Kristiansand kommune",
        ref_code="RAP-2026-M09-SEKSJON-INNKJ"
    )

    doc.add_heading(level=2).add_run("SEKSJONSOVERSIKT:").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "• Årsramme: 28 500 tNOK | Påløpt avvik: +1 450 tNOK (Merforbruk)\n"
        "• Hovedårsak: Konsulentbistand i forbindelse med gjennomføring av rammeavtaleanbud for IT og VVS."
    )

    t = doc.add_table(rows=5, cols=5)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdrs = ["Art", "Beskrivelse", "Årsbudsjett", "Påløpt", "Avvik"]
    for i, h in enumerate(hdrs):
        c = t.rows[0].cells[i]
        set_cell_background(c, "1B365D")
        set_cell_margins(c, 80, 80, 80, 80)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    data = [
        ("1010", "Fast lønn stabsansatte", "21 000 tNOK", "14 200 tNOK", "+200 tNOK"),
        ("1090", "Overtid ved anbudsfrister", "500 tNOK", "850 tNOK", "+350 tNOK 🔴"),
        ("1270", "Juridisk/teknisk konsulentbistand", "4 000 tNOK", "4 900 tNOK", "+900 tNOK 🔴"),
        ("1370", "Lisenser KGV/KAV fagsystem", "3 000 tNOK", "3 000 tNOK", "0 tNOK 🟢")
    ]
    for r_idx, row in enumerate(data, start=1):
        for c_idx, val in enumerate(row):
            cell = t.rows[r_idx].cells[c_idx]
            set_cell_background(cell, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)

    doc.add_heading(level=2).add_run("TILTAKSPLAN FOR SEKSJONEN:").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "1. [ACT-SEK-01]: Avslutte ekstern juridisk konsulentbistand innen 14 dager; overføre restoppgaver internt (-600 000 kr).\n"
        "2. [ACT-SEK-02]: Innføre overtidsforbud for konsulentoppfølging uten forhåndsgodkjenning (-200 000 kr)."
    )

    p_sign = doc.add_paragraph("Seksjonsleder: Signert | SHA256:e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0")
    p_sign.runs[0].font.name = "Consolas"
    p_sign.runs[0].font.size = Pt(8.5)
    doc.save(filename_docx)
    print(f"✓ Mal generert: {filename_docx.name}")


# ==============================================================================
# 12. MAL: AVDELINGSLEDER / ENHETSLEDER (NIVÅ 5)
# ==============================================================================
def create_rapportmal_avdelingsleder():
    filename_docx = TEMPLATES_DIR / "RAPPORTMAL_AVDELINGSLEDER.docx"
    doc = docx.Document()
    add_document_header(
        doc,
        title="MÅNEDLIG OPERATIV AVVIKSRAPPORT — AVDELINGSLEDER / ENHETSLEDER",
        subtitle="Enhet 202: Lovisenlev Skole — Operativ avviks- og tiltaksrapport",
        ref_code="RAP-2026-M09-ENHET-202"
    )

    doc.add_heading(level=2).add_run("OPERATIV STATUS ENHET 202:").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "• Tildelt Årsramme: 52 000 tNOK | Påløpt hittil: 37 400 tNOK\n"
        "• Avvik hittil i år: +3 200 tNOK (+9.3 % Merforbruk) — 🔴 RØD ALARM\n"
        "• Hovedårsak: Vikarutgifter timelærere (Art 10200) +2 300 tNOK pga. sykefravær på 12.4 %"
    )

    doc.add_heading(level=3).add_run("Linjeavvik på Kontonivå (Visma ERP):")
    t = doc.add_table(rows=6, cols=5)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdrs = ["Konto", "Kontonavn", "Årsramme", "Påløpt", "Avvik"]
    for i, h in enumerate(hdrs):
        c = t.rows[0].cells[i]
        set_cell_background(c, "1B365D")
        set_cell_margins(c, 80, 80, 80, 80)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    rows = [
        ("10100", "Fast lønn lærere", "38 000 tNOK", "25 800 tNOK", "+400 tNOK"),
        ("10200", "Vikarutgifter timelærere", "2 500 tNOK", "4 800 tNOK", "+2 300 tNOK 🔴"),
        ("10900", "Overtid / Ekstratimer", "300 tNOK", "650 tNOK", "+350 tNOK 🔴"),
        ("11200", "Undervisningsmateriell", "1 200 tNOK", "1 350 tNOK", "+150 tNOK"),
        ("12000", "Inventar og utstyr", "800 tNOK", "800 tNOK", "0 tNOK 🟢")
    ]
    for r_idx, rdata in enumerate(rows, start=1):
        for c_idx, val in enumerate(rdata):
            cell = t.rows[r_idx].cells[c_idx]
            set_cell_background(cell, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)
            if "🔴" in val:
                r.font.bold = True
                r.font.color.rgb = RGBColor(192, 57, 43)

    doc.add_heading(level=2).add_run("30-DAGERS OPERATIV HANDLINGSPLAN:").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "• ACT-202-A: Klassesammenslåing ved korttidsfravær < 3 dager (-80 000 kr/md).\n"
        "• ACT-202-B: NAV-oppfølging med lønnskontor for refusjoner (+650 000 kr likviditet).\n"
        "• ACT-202-C: IA-oppfølging og Tett-på-samtaler for å bringe fravær under 8 %.\n"
        "• ACT-202-D: Innkjøpsstopp for rekvisita og inventar ut året (-50 000 kr/md)."
    )

    p_sign = doc.add_paragraph("Enhetsleder: Signert | SHA256:f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1")
    p_sign.runs[0].font.name = "Consolas"
    p_sign.runs[0].font.size = Pt(8.5)
    doc.save(filename_docx)
    print(f"✓ Mal generert: {filename_docx.name}")


# ==============================================================================
# 13. MAL: STANDARDIZERT 4-PUNKTS AVVIK OG EFFEKTPROGNOSE
# ==============================================================================
def create_rapportmonster_avvik_effekt():
    filename_docx = TEMPLATES_DIR / "RAPPORTMONSTER_AVVIK_OG_EFFEKTPROGNOSE.docx"
    doc = docx.Document()
    add_document_header(
        doc,
        title="STANDARDIZERT RAPPORTERINGSMØNSTER: AVVIK & EFFEKTPROGNOSE",
        subtitle="Obligatorisk 4-stegs struktur: YTD Avvik → Årsak → Action → Kvantifisert EOY Effekt",
        ref_code="MAL-AVVIK-EFFEKT-001"
    )

    doc.add_heading(level=2).add_run("DET OBLIGATORISKE 4-PUNKTS MØNSTERET:").font.color.rgb = COLOR_NAVY
    p_box = doc.add_paragraph(
        "1. AVVIK HITTIL I ÅR (YTD Variance): Presist avvik i kroner og prosent mot periodisert budsjett i Visma ERP.\n"
        "2. ÅRSAK TIL AVVIK (Root Cause Analysis): Dypdykk i drivere (sykefravær, NAV-etterslep, prisstigning) via Glass-Box RAG.\n"
        "3. FORSLAG TIL ACTION (Corrective Action Plan): Strakstiltak (0–30 dager), operative tiltak (30–90 dager), politiske tiltak.\n"
        "4. KVANTIFISERT EFFEKT PÅ PROGNOSEBANE & EOY BALANSE: Monte Carlo-beregning av effekt på sluttresultat per 31.12."
    )
    p_box.runs[0].font.name = "Segoe UI"
    p_box.runs[0].font.size = Pt(9.5)

    doc.add_heading(level=2).add_run("EKSEMPEL: ENHET 202 GRUNNSKOLE (SEPTEMBER M9):").font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "• 1. YTD Avvik: Periodisert budsjett 10,0M | Regnskap 11,24M | YTD Avvik: +1 240 000 NOK (+12.4 %) [🔴 RØD ALARM]\n"
        "• 2. Årsak: Høyt sykefravær (14.2 %) + NAV-etterslep på sykepengerefusjoner på 410 000 NOK.\n"
        "• 3. Action: Strakstiltak ukentlig NAV-purring, intern klassesammenslåing, samt omdisponering i T2.\n"
        "• 4. Kvantifisert Effekt: Status quo EOY: +1,85M -> Tiltakseffekt: -1,25M -> Revidert EOY Balanse: +600k (innenfor ramme)."
    )

    p_audit = doc.add_paragraph(
        "Forseglet i SQLite Audit_AI_Actions jf. Stage-Gate Port 9\n"
        "SHA-256: b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3"
    )
    p_audit.runs[0].font.name = "Consolas"
    p_audit.runs[0].font.size = Pt(8.5)
    doc.save(filename_docx)
    print(f"✓ Mal generert: {filename_docx.name}")


# ==============================================================================
# HOVEDKJØRING
# ==============================================================================
if __name__ == "__main__":
    print("=" * 80)
    print("🚀 GENERERER MALER, SKJEMAER OG RAPPORTER FOR OFFICE HUB")
    print("=" * 80)

    create_saksfremlegg_template()
    create_avviksnotat_template()
    create_hta_protokoll_template()
    create_stage_gate_signoff_template()
    create_fria_dpia_template()
    create_periodelukking_template()
    create_saksbehandling_excel_model()

    # De 5 hierarkiske rapportene og 4-punkts mønsteret
    create_rapportmal_kommunestyret()
    create_rapportmal_kommunedirektor()
    create_rapportmal_kommunalsjef()
    create_rapportmal_seksjonsleder()
    create_rapportmal_avdelingsleder()
    create_rapportmonster_avvik_effekt()

    print("\n✅ Samtlige 13 maler og arbeidsbøker er vellykket generert!")

