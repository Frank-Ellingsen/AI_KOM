"""
Word Saksfremlegg og HØP Notat Generator for Kristiansand Kommune.
Implementerer:
- WORD_POLITISKE_SAKSFREMLEGG_MALER.md
- WORD_PUBLIC360_OG_DOKUMENT_AUTOMATION.md
- WORD_TERTIALRAPPORT_OG_HOP_STANDARDER.md
"""
from __future__ import annotations

import datetime
import hashlib
from pathlib import Path
from typing import Optional

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Fargepalett
COLOR_NAVY_RGB = RGBColor(0x1E, 0x3A, 0x8A)     # #1E3A8A
COLOR_DARK_RGB = RGBColor(0x1F, 0x29, 0x37)     # #1F2937
COLOR_GRAY_RGB = RGBColor(0x4B, 0x55, 0x63)     # #4B5563
COLOR_RED_RGB = RGBColor(0xDC, 0x26, 0x26)      # #DC2626
COLOR_GREEN_RGB = RGBColor(0x16, 0xA3, 0x4A)    # #16A34A


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Setter indre marginer (padding) i en tabellcelle."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_cell_background(cell, hex_color: str):
    """Setter bakgrunnsfarge i en tabellcelle."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)


def add_table_header_repeat(table):
    """Sikrer at overskriftsraden repeteres på tvers av sideskift (WCAG 2.1 AA)."""
    header_tr = table.rows[0]._tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader')
    header_tr.append(tblHeader)


def format_paragraph(p, space_after=6, line_spacing=1.15):
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing


def generate_saksfremlegg_docx(output_path: Optional[str] = None) -> str:
    """
    Bygger et formelt politisk saksfremlegg for Bystyret/Formannskapet
    i henhold til Kristiansand kommunes standard og Public360-metadata.
    """
    if output_path is None:
        target = Path(__file__).resolve().parents[4] / "word" / "Saksfremlegg_Bystyret_Budsjettendring_2026.docx"
    else:
        target = Path(output_path)

    target.parent.mkdir(parents=True, exist_ok=True)

    doc = Document()

    # 1. Marginer (Standard 2,5 cm)
    for section in doc.sections:
        section.top_margin = Inches(0.984)     # 2.5 cm
        section.bottom_margin = Inches(0.984)  # 2.5 cm
        section.left_margin = Inches(0.984)    # 2.5 cm
        section.right_margin = Inches(0.984)   # 2.5 cm

        # Topptekst & Bunntekst
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "KRISTIANSAND KOMMUNE  •  BYSTYRET / FORMANNSKAPET"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.runs[0].font.name = "Arial"
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = COLOR_GRAY_RGB

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Saksnummer: 26/04182 (Public360)  |  Offentleglova § 14  |  Hjemmel: Kommuneloven § 14-5"
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        fp.runs[0].font.name = "Arial"
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = COLOR_GRAY_RGB

    now_str = datetime.date.today().strftime("%d.%m.%Y")
    audit_hash = hashlib.sha256(f"{datetime.datetime.now().isoformat()}:SAKSFREMLEGG_BYSTYRET_2026".encode()).hexdigest()

    # Public360 Metadata-tabell øverst
    meta_table = doc.add_table(rows=4, cols=4)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    meta_rows = [
        ("Saksnummer:", "26/04182-1", "Dato:", now_str),
        ("Arkivkode:", "FE-102 & KOSTRA-202", "Utvalg:", "Bystyret / Formannskapet"),
        ("Saksbehandler:", "Frank Ellingsen, Senior Controller", "Klassering:", "Åpen / Offentlig"),
        ("Dokument-ID:", f"DOC-360-{audit_hash[:8].upper()}", "Kryptostempel:", f"SHA256:{audit_hash[:12]}")
    ]

    for r_idx, r_data in enumerate(meta_rows):
        for c_idx, val in enumerate(r_data):
            cell = meta_table.cell(r_idx, c_idx)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            set_cell_background(cell, "F9FAFB")
            p = cell.paragraphs[0]
            p.text = val
            p.runs[0].font.name = "Arial"
            p.runs[0].font.size = Pt(8.5)
            if c_idx in [0, 2]:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_NAVY_RGB
            else:
                p.runs[0].font.color.rgb = COLOR_DARK_RGB

    doc.add_paragraph()  # Avstand

    # SAKSTITTEL (Overskrift 1: 20 pt, Bold, Mørkeblå #1E3A8A)
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(8)
    run_h1 = h1.add_run("Sak 42/26: Endring av Årsbudsjett 2026 og Tiltakspakke for Enhet 202 Grunnskole")
    run_h1.font.name = "Arial"
    run_h1.font.size = Pt(20)
    run_h1.font.bold = True
    run_h1.font.color.rgb = COLOR_NAVY_RGB

    # Underoverskrift
    p_sub = doc.add_paragraph()
    format_paragraph(p_sub, space_after=14)
    r_sub = p_sub.add_run("Behandling av økonomisk avvik i 2. tertial og opprettholdelse av budsjettbalanse jf. Kommuneloven § 14-5")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_GRAY_RGB

    # --------------------------------------------------------------------------
    # 1. SAKSAMMENDRAG
    # --------------------------------------------------------------------------
    h2_1 = doc.add_paragraph()
    h2_1.paragraph_format.space_before = Pt(12)
    h2_1.paragraph_format.space_after = Pt(4)
    run = h2_1.add_run("1. Saksammendrag")
    run.font.name = "Arial"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY_RGB

    p1 = doc.add_paragraph()
    format_paragraph(p1)
    p1.add_run(
        "I forbindelse med avleggelsen av 2. tertialrapport 2026 er det avdekket et merforbruk ved "
        "Enhet 202 Grunnskole på kr 850 000 hittil i år (+12,4 % over periodisert ramme). "
        "Hovedårsaken er ekstraordinært høyt sykefravær blant undervisningspersonell i mai og juni (14,2 %), "
        "som har utløst kr 620 000 i uforutsette vikarutgifter (konto 1020), kombinert med et forsinket "
        "oppgjør av sykepengerefusjoner fra NAV (konto 1600) på kr 180 000."
    )

    p2 = doc.add_paragraph()
    format_paragraph(p2)
    p2.add_run(
        "Kommunedirektøren har utarbeidet en to-trinns tiltakspakke i samarbeid med rektor og de tillitsvalgte, "
        "bestående av klassesammenslåing ved korttidsfravær, forsterket refusjonsoppfølging og etablering av "
        "en felles vikarpool i Oppvekstsektoren. Tiltakene reduserer forventet helårsavvik fra kr 1 720 000 til "
        "kr 350 000. For å sikre budsjettmessig balanse jf. Kommuneloven § 14-5 innstilles det på at det gjenstående "
        "avviket på kr 350 000 dekkes inn gjennom omdisponering fra Oppvekstsektorens omstillingsfond."
    )

    # --------------------------------------------------------------------------
    # 2. KOMMUNEDIREKTØRENS FORSLAG TIL VEDTAK
    # --------------------------------------------------------------------------
    h2_2 = doc.add_paragraph()
    h2_2.paragraph_format.space_before = Pt(14)
    h2_2.paragraph_format.space_after = Pt(4)
    run = h2_2.add_run("2. Kommunedirektørens Forslag til Vedtak")
    run.font.name = "Arial"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY_RGB

    # Framhevet boks for forslag til vedtak
    vedtak_table = doc.add_table(rows=1, cols=1)
    vedtak_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_v = vedtak_table.cell(0, 0)
    set_cell_margins(c_v, top=140, bottom=140, left=180, right=180)
    set_cell_background(c_v, "EFF6FF")  # Lys blå bakgrunn

    pv = c_v.paragraphs[0]
    format_paragraph(pv, space_after=6)
    r_v = pv.add_run("Kommunedirektøren foreslår at Bystyret fatter følgende vedtak:")
    r_v.font.name = "Arial"
    r_v.font.size = Pt(11)
    r_v.font.bold = True
    r_v.font.color.rgb = COLOR_NAVY_RGB

    vedtakspunkter = [
        "1. Bystyret godkjenner i medhold av Kommuneloven § 14-5 en budsjettjustering der det bevilges inntil kr 350 000 i tilleggsramme til Enhet 202 Grunnskole (Ansvar 2020 / KOSTRA Funksjon 202) for driftsåret 2026.",
        "2. Tilleggsbevilgningen finansieres i sin helhet ved tilsvarende overføring fra Oppvekstsektorens omstillingsfond (Konto 1950 / Disposisjonsfond).",
        "3. Kommunedirektøren pålegges å iverksette den fremlagte tiltakspakken for vikarbruk og opprette felles vikarpool i tråd med drøftinger jf. Hovedtariffavtalen § 4.",
        "4. Status for vikarbruken og økonomisk balanse rapporteres i 3. tertialrapport 2026."
    ]

    for vp_txt in vedtakspunkter:
        p_item = c_v.add_paragraph()
        format_paragraph(p_item, space_after=6)
        r_item = p_item.add_run(vp_txt)
        r_item.font.name = "Arial"
        r_item.font.size = Pt(10.5)
        r_item.font.color.rgb = COLOR_DARK_RGB

    doc.add_paragraph()

    # --------------------------------------------------------------------------
    # 3. BAKGRUNN FOR SAKEN
    # --------------------------------------------------------------------------
    h2_3 = doc.add_paragraph()
    h2_3.paragraph_format.space_before = Pt(14)
    h2_3.paragraph_format.space_after = Pt(4)
    run = h2_3.add_run("3. Bakgrunn for Saken og Lovhjemmel")
    run.font.name = "Arial"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY_RGB

    p_bg1 = doc.add_paragraph()
    format_paragraph(p_bg1)
    p_bg1.add_run(
        "Etter Kommuneloven § 14-5 skal årsbudsjettet endres dersom det i løpet av året oppstår vesentlige avvik "
        "som utfordrer det overordnede budsjettbalansekravet. Kristiansand kommunes økonomireglement forutsetter at "
        "enhetsledere varsler sektorledelsen straks det oppstår merforbruk som overstiger 5 % av periodisert ramme. "
        "Enhet 202 Grunnskole har en tildelt årsramme på kr 13 700 000 for 2026, hvorav periodisert ramme for 1. halvår "
        "utgjør kr 6 850 000."
    )

    p_bg2 = doc.add_paragraph()
    format_paragraph(p_bg2)
    p_bg2.add_run(
        "Videre følger det av Kommuneloven § 14-6 fjerde ledd (bruttoprinsippet) at alle utgifter og inntekter skal "
        "budsjetteres og regnskapsføres brutto. Det er følgelig ikke tillatt å motregne vikarutgiftene direkte mot "
        "forventede fremtidige refusjoner fra NAV; avvikene må synliggjøres og håndteres på selvstendig grunnlag."
    )

    # --------------------------------------------------------------------------
    # 4. VURDERING OG ØKONOMISKE KONSEKVENSER
    # --------------------------------------------------------------------------
    h2_4 = doc.add_paragraph()
    h2_4.paragraph_format.space_before = Pt(14)
    h2_4.paragraph_format.space_after = Pt(4)
    run = h2_4.add_run("4. Vurdering og Økonomiske Konsekvenser")
    run.font.name = "Arial"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY_RGB

    # Tabell over avvik
    h3_tab = doc.add_paragraph()
    h3_tab.paragraph_format.space_before = Pt(8)
    h3_tab.paragraph_format.space_after = Pt(4)
    run = h3_tab.add_run("Tabell 1: Regnskapstall H1 2026 for Enhet 202 Grunnskole (Tall i NOK)")
    run.font.name = "Arial"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = COLOR_DARK_RGB

    tab = doc.add_table(rows=6, cols=5)
    tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    add_table_header_repeat(tab)

    cols_w = [Inches(2.5), Inches(1.1), Inches(1.1), Inches(1.1), Inches(0.9)]
    tab_headers = ["Kontoart / Beskrivelse", "Budsjett H1", "Regnskap H1", "Avvik Kr", "Avvik %"]

    for c_i, (h_title, w) in enumerate(zip(tab_headers, cols_w)):
        cell = tab.cell(0, c_i)
        cell.width = w
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        set_cell_background(cell, "1E3A8A")
        p = cell.paragraphs[0]
        p.text = h_title
        p.runs[0].font.name = "Arial"
        p.runs[0].font.size = Pt(9.5)
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i == 0 else WD_ALIGN_PARAGRAPH.RIGHT

    tab_rows = [
        ("Art 1010 Faste lønninger", "4 850 000", "4 890 000", "+40 000", "+0,8 %"),
        ("Art 1020 Innkjøp av vikarer (timelærere)", "1 200 000", "1 820 000", "+620 000", "+51,7 %"),
        ("Art 1090 Overtid og kveldstillegg", "57 000", "436 000", "+379 000", "+664,9 %"),
        ("Art 1600 NAV-refusjoner (sykepenger)", "-590 000", "-410 000", "+180 000", "-30,5 %"),
        ("Sum Enhet 202 Grunnskole", "6 850 000", "7 700 000", "+850 000", "+12,4 %")
    ]

    for r_i, r_vals in enumerate(tab_rows, start=1):
        is_tot = (r_i == len(tab_rows))
        for c_i, (val, w) in enumerate(zip(r_vals, cols_w)):
            cell = tab.cell(r_i, c_i)
            cell.width = w
            set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
            if is_tot:
                set_cell_background(cell, "F3F4F6")
            else:
                set_cell_background(cell, "FFFFFF" if r_i % 2 != 0 else "F9FAFB")
            p = cell.paragraphs[0]
            p.text = val
            p.runs[0].font.name = "Arial"
            p.runs[0].font.size = Pt(9.5)
            if is_tot:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_NAVY_RGB
            elif c_i == 3 and "+" in val and "40 000" not in val:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_RED_RGB
            else:
                p.runs[0].font.color.rgb = COLOR_DARK_RGB
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i == 0 else WD_ALIGN_PARAGRAPH.RIGHT

    doc.add_paragraph()

    # Avsnitt om rotårsak og tiltak
    p_v1 = doc.add_paragraph()
    format_paragraph(p_v1)
    p_v1.add_run("Rotårsaksanalyse: ").bold = True
    p_v1.add_run(
        "Avviket er i alt vesentlig konsentrert rundt vikarutgifter ved sykefravær. "
        "Gjennomsnittlig sykefravær i skolesektoren i Kristiansand er 7,8 %, mens Enhet 202 i mai måned "
        "registrerte et fravær på 14,2 % som følge av langvarig smittebølge og akutte sykemeldinger blant nøkkelpersonell. "
        "Dette nødvendiggjorde omfattende innleie av timelærere og pålegg om overtid for å opprettholde lovfestet "
        "undervisningstilbud og eksamensavvikling."
    )

    p_v2 = doc.add_paragraph()
    format_paragraph(p_v2)
    p_v2.add_run("Kvantifisert Handlingsplan: ").bold = True
    p_v2.add_run(
        "1. Klassesammenslåing i fellesfag ved korttidsfravær (< 3 dager) gir en estimert innsparing på kr 70 000 per måned.\n"
        "2. Aktiv oppfølging og samlepurring mot NAV Arbeid og Ytelser sikrer utbetaling av utestående refusjoner på kr 180 000 i 3. kvartal.\n"
        "3. Etablering av felles vikarpool i Oppvekstsektoren kutter ekstern innleie med ytterligere kr 100 000 per måned fra skolestart i august."
    )

    p_v3 = doc.add_paragraph()
    format_paragraph(p_v3)
    p_v3.add_run("Helårsprognose (EOY) og Risikovurdering: ").bold = True
    p_v3.add_run(
        "Uten tiltak (P90 / Worst Case) ville helårsavviket endt på kr 1 720 000. "
        "Med de iverksatte tiltakene reduseres helårsavviket til forventet kr 350 000 (P10 / Forventet bane). "
        "Dette beløpet lar seg finansiere i sin helhet innenfor Oppvekstsektorens omstillingsfond, slik at "
        "kommunens samlede netto driftsresultat ikke svekkes."
    )

    # --------------------------------------------------------------------------
    # 5. KONKLUSJON OG VIDERE PROSESS
    # --------------------------------------------------------------------------
    h2_5 = doc.add_paragraph()
    h2_5.paragraph_format.space_before = Pt(14)
    h2_5.paragraph_format.space_after = Pt(4)
    run = h2_5.add_run("5. Konklusjon og Videre Prosess")
    run.font.name = "Arial"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY_RGB

    p_k = doc.add_paragraph()
    format_paragraph(p_k)
    p_k.add_run(
        "Kommunedirektøren vurderer at den foreliggende saken ivaretar kravene til forsvarlig økonomistyring "
        "og realisme i budsjettet. Vedtaket gir enheten handlefrihet til å levere lovpålagte skoleoppgaver, "
        "samtidig som strukturelle tiltak begrenser de økonomiske ringvirkningene. "
        "Saken oversendes Formannskapet for innstilling og Bystyret for endelig vedtak."
    )

    # Signatur
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(24)
    p_sig.add_run("Camilla Dunsæd\nKommunedirektør").bold = True
    p_sig.runs[0].font.name = "Arial"
    p_sig.runs[0].font.size = Pt(10.5)

    p_sig2 = doc.add_paragraph()
    p_sig2.add_run("Frank Ellingsen\nSenior Controller").italic = True
    p_sig2.runs[0].font.name = "Arial"
    p_sig2.runs[0].font.size = Pt(10)
    p_sig2.runs[0].font.color.rgb = COLOR_GRAY_RGB

    doc.save(str(target))
    return str(target)


def generate_hop_notat_docx(output_path: Optional[str] = None) -> str:
    """
    Bygger et standardisert Handlings- og Økonomiplan (HØP) notat
    etter strukturen i WORD_TERTIALRAPPORT_OG_HOP_STANDARDER.md.
    """
    if output_path is None:
        target = Path(__file__).resolve().parents[4] / "word" / "Tertialrapport_og_HOP_Notat_2026.docx"
    else:
        target = Path(output_path)

    target.parent.mkdir(parents=True, exist_ok=True)

    doc = Document()

    # Marginer 2.5 cm
    for section in doc.sections:
        section.top_margin = Inches(0.984)
        section.bottom_margin = Inches(0.984)
        section.left_margin = Inches(0.984)
        section.right_margin = Inches(0.984)

        header = section.header
        hp = header.paragraphs[0]
        hp.text = "KRISTIANSAND KOMMUNE  •  HANDLINGS- OG ØKONOMIPLAN (HØP) 2027–2030"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.runs[0].font.name = "Arial"
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = COLOR_GRAY_RGB

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Styringsnotat Økonomi & Strategi  •  KOSTRA-standard  •  WCAG 2.1 AA Samsvar"
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        fp.runs[0].font.name = "Arial"
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = COLOR_GRAY_RGB

    # Tittel
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)
    r1 = h1.add_run("Handlings- og Økonomiplan (HØP) 2027–2030: Rammer og Retningslinjer")
    r1.font.name = "Arial"
    r1.font.size = Pt(20)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_NAVY_RGB

    p_lead = doc.add_paragraph()
    format_paragraph(p_lead, space_after=16)
    r_lead = p_lead.add_run("Faglig styringsnotat for tertialrapportering, sektorrammer og investeringsprioriteringer.")
    r_lead.font.name = "Arial"
    r_lead.font.size = Pt(12)
    r_lead.font.italic = True
    r_lead.font.color.rgb = COLOR_GRAY_RGB

    chapters = [
        ("Kapittel 1: Innledning og Hovedutfordringer",
         "Kristiansand kommune står overfor et stramt økonomisk handlingsrom i perioden 2027–2030 som følge av demografiske endringer "
         "med flere eldre innbyggere, reduserte skatteinntekter og økte renter på kommunens lånegjeld. "
         "Målsettingen er å opprettholde et netto driftsresultat på minst 1,75 % av brutto driftsinntekter."),
        
        ("Kapittel 2: Finansiell Ramme og Økonomiske Nøkkeltall",
         "Styringsmålene fastsetter at disposisjonsfondet skal utgjøre minst 8 % av driftsinntektene for å gi tilstrekkelig "
         "buffer mot uforutsette hendelser. Lånegjelden skal holdes under 85 % av brutto inntekter eksklusive vann og avløp."),
        
        ("Kapittel 3: Sektorvise Rammer og Tiltakspakker",
         "3.1 Oppvekst og Grunnskole: Innføring av felles vikarpool og standardiserte bemanningsnormer for å eliminere uplanlagt overforbruk.\n"
         "3.2 Helse og Mestring: Omstilling til velferdsteknologi, forebyggende hjemmetjenester og redusert overtid i turnus.\n"
         "3.3 By- og Stedsutvikling: Energieffektivisering av kommunale formålsbygg og optimalisering av vedlikeholdsprogrammet.\n"
         "3.4 Kultur og Innbyggerdialog: Digitale innbyggertjenester og målrettede samarbeidsavtaler med frivilligheten."),
        
        ("Kapittel 4: Investeringsprogram 2027–2030",
         "Samlede brutto investeringer begrenses til kr 1,2 milliarder i fireårsperioden, med hovedprioritet på utvidelse av "
         "skolekapasitet og rehabilitering av omsorgsboliger. Alle prosjekter underlegges KS2-kvalitetssikring."),
        
        ("Kapittel 5: Finans- og Fondsstrategi",
         "Avsetninger til disposisjonsfond prioriteres foran nye driftstiltak. Kommunens likviditetsstrategi baseres på "
         "langsiktige sertifikatlån med flytende rente kombinert med rentebytteavtaler (swaps) for å sikre forutsigbarhet.")
    ]

    for ch_title, ch_body in chapters:
        h2 = doc.add_paragraph()
        h2.paragraph_format.space_before = Pt(14)
        h2.paragraph_format.space_after = Pt(4)
        r = h2.add_run(ch_title)
        r.font.name = "Arial"
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = COLOR_NAVY_RGB

        p_b = doc.add_paragraph()
        format_paragraph(p_b)
        r_b = p_b.add_run(ch_body)
        r_b.font.name = "Arial"
        r_b.font.size = Pt(10.5)
        r_b.font.color.rgb = COLOR_DARK_RGB

    doc.save(str(target))
    return str(target)


def generate_raadmann_notat_docx(output_path: Optional[str] = None) -> str:
    """
    Nivå 2: Månedsrapport for Kommunedirektøren med administrativ strakstiltaksplan.
    """
    if output_path is None:
        target = Path(__file__).resolve().parents[4] / "word" / "Manedsrapport_Kommunedirektor_Strakstiltak_2026.docx"
    else:
        target = Path(output_path)

    target.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.984)
        section.bottom_margin = Inches(0.984)
        section.left_margin = Inches(0.984)
        section.right_margin = Inches(0.984)

        header = section.header
        hp = header.paragraphs[0]
        hp.text = "KRISTIANSAND KOMMUNE  •  KOMMUNEDIREKTØRENS LEDERGRUPPE"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.runs[0].font.name = "Arial"
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = COLOR_GRAY_RGB

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Månedsrapport Økonomi & Drift  |  Internkontroll jf. Kommuneloven § 14-5  |  Offl. § 14"
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        fp.runs[0].font.name = "Arial"
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = COLOR_GRAY_RGB

    # Tittel
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)
    r1 = h1.add_run("Månedsrapport Kommunedirektøren: Administrativ Strakstiltaksplan 2026")
    r1.font.name = "Arial"
    r1.font.size = Pt(18)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_NAVY_RGB

    p_sub = doc.add_paragraph()
    format_paragraph(p_sub, space_after=12)
    r_sub = p_sub.add_run("Månedlig konsernoppfølging, vikarstopp og likviditetsanalyse per 2. Tertial.")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_GRAY_RGB

    # 1. Hovedstatus
    p_h = doc.add_paragraph()
    p_h.add_run("1. Finansiell Hovedstatus & Konsernavvik").bold = True
    p_h.runs[0].font.size = Pt(13)
    p_h.runs[0].font.color.rgb = COLOR_NAVY_RGB

    p_txt1 = doc.add_paragraph()
    format_paragraph(p_txt1)
    p_txt1.add_run(
        "Akkumulert driftsregnskap per august 2026 viser et samlet netto merforbruk på kr 2 489 000 mot periodisert budsjett. "
        "Hovedårsaken til avviket er konsentrert til Sektor Oppvekst (kr 1 420 000 i vikarutgifter) og Sektor Helse og Mestring "
        "(kr 1 069 000 i overtid og døgnvakttillegg). Kommunedirektøren iverksetter umiddelbart fire administrative strakstiltak (ACT-01 til ACT-04) "
        "for å bringe helårsdriften i balanse innenfor vedtatt årsbudsjett jf. Kommuneloven § 14-5."
    )

    # Tabell over administrative strakstiltak
    table = doc.add_table(rows=5, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    add_table_header_repeat(table)

    headers = ["Tiltak ID", "Område / Sektor", "Beskrivelse av Strakstiltak", "Månedlig Effekt (kr)"]
    for c_i, th in enumerate(headers):
        cell = table.cell(0, c_i)
        cell.text = th
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)

    actions = [
        ("ACT-01", "Oppvekst & Utdanning", "Vikarstopp for korttidsfravær < 3 dager; intern omdisponering", "170 000 kr"),
        ("ACT-02", "Helse og Mestring", "Omlegging av langvakter og restriksjoner på innleie fra byrå", "145 000 kr"),
        ("ACT-03", "Kultur & Innbyggerdialog", "Innstillinger i eksterne konsulentkjøp og kursvirksomhet", "65 000 kr"),
        ("ACT-04", "Fellestjenester / IKT", "Konsolidering av programvarelisenser og utstyrsanskaffelser", "80 000 kr")
    ]

    for r_idx, row in enumerate(actions, start=1):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.runs[0].font.name = "Arial"
            p.runs[0].font.size = Pt(9)
            if c_idx == 3:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_GREEN_RGB
            elif c_idx == 0:
                p.runs[0].font.bold = True
            set_cell_background(cell, "F9FAFB" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)

    # Signatur
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(20)
    p_sig.add_run("Kristiansand, " + datetime.datetime.now().strftime("%d.%m.%Y") + "\n\n").italic = True
    p_sig.add_run("Camilla Dunsæd\nKommunedirektør").bold = True

    doc.save(str(target))
    return str(target)


def generate_sektornotat_oppvekst_docx(output_path: Optional[str] = None) -> str:
    """
    Nivå 3: Sektorstyringsnotat fra Kommunalsjef Oppvekst til Kommunedirektøren.
    """
    if output_path is None:
        target = Path(__file__).resolve().parents[4] / "word" / "Sektorstyringsnotat_Kommunalsjef_Oppvekst_2026.docx"
    else:
        target = Path(output_path)

    target.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.984)
        section.bottom_margin = Inches(0.984)
        section.left_margin = Inches(0.984)
        section.right_margin = Inches(0.984)

        header = section.header
        hp = header.paragraphs[0]
        hp.text = "KRISTIANSAND KOMMUNE  •  SEKTOR OPPVEKST OG UTDANNING"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = COLOR_GRAY_RGB

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Sektorstyringsnotat Grunnskole  |  Enhetsoppfølging T2 2026"
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = COLOR_GRAY_RGB

    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)
    r1 = h1.add_run("Sektorstyringsnotat: Oppvekst & Grunnskole 2026")
    r1.font.name = "Arial"
    r1.font.size = Pt(18)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_NAVY_RGB

    p_sub = doc.add_paragraph()
    format_paragraph(p_sub, space_after=12)
    p_sub.add_run("Enhetsvis avviksmatrise, vikarforbruk og tiltak for lærertetthet per 2. Tertial.").italic = True

    p_txt = doc.add_paragraph()
    format_paragraph(p_txt)
    p_txt.add_run(
        "Sektor Oppvekst har et akkumulert merforbruk på kr 1 420 000 ved utgangen av august. Merforbruket drives av høyt "
        "korttidsfravær og innleie av vikarer i grunnskolene (Art 1020). Kommunalsjefen har gjennomgått samtlige enheter og etablert "
        "en intern vikarring mellom skolene i Vågsbygd og Grim for å redusere kjøp fra kommersielle vikarbyråer."
    )

    # Skoleoversikt tabell
    table = doc.add_table(rows=5, cols=5)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    add_table_header_repeat(table)

    headers = ["Skoleenhet", "Elevtall", "Budsjett YTD", "Regnskap YTD", "Avvik YTD (Merforbruk)"]
    for c_i, th in enumerate(headers):
        cell = table.cell(0, c_i)
        cell.text = th
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

    schools = [
        ("Grim Skole (Enhet 2020)", "480", "4 150 000", "4 720 000", "+570 000 kr"),
        ("Lovisenlev Skole", "390", "3 400 000", "3 710 000", "+310 000 kr"),
        ("Tangvall Skole", "310", "2 650 000", "2 890 000", "+240 000 kr"),
        ("Vågsbygd Skole", "340", "2 250 000", "2 550 000", "+300 000 kr")
    ]

    for r_idx, row in enumerate(schools, start=1):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            if c_idx >= 2:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if c_idx == 4:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_RED_RGB
            set_cell_background(cell, "F9FAFB" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(20)
    p_sig.add_run("Kristin E. Bakke\nKommunalsjef Oppvekst").bold = True

    doc.save(str(target))
    return str(target)


def generate_prosjektkontroll_capex_docx(output_path: Optional[str] = None) -> str:
    """
    Nivå 4: Prosjektkontroll og Investeringstilsyn (Capex) for Kontrollutvalget jf. ISO 21508.
    """
    if output_path is None:
        target = Path(__file__).resolve().parents[4] / "word" / "Prosjektkontroll_Capex_Statusnotat_2026.docx"
    else:
        target = Path(output_path)

    target.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.984)
        section.bottom_margin = Inches(0.984)
        section.left_margin = Inches(0.984)
        section.right_margin = Inches(0.984)

        header = section.header
        hp = header.paragraphs[0]
        hp.text = "KRISTIANSAND KOMMUNE  •  KONTROLLUTVALGET & BYUTVIKLING"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = COLOR_GRAY_RGB

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Capex Statusrapport ISO 21508 EVM  |  Prosjektkontroll Frank Ellingsen"
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = COLOR_GRAY_RGB

    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)
    r1 = h1.add_run("Prosjektkontroll & Investeringstilsyn (Capex): Statusnotat 2026")
    r1.font.name = "Arial"
    r1.font.size = Pt(18)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_NAVY_RGB

    p_sub = doc.add_paragraph()
    format_paragraph(p_sub, space_after=12)
    p_sub.add_run("Earned Value Management (EVM) analyse av Vågsbygd Skole, Randesund Boenhet og VA-anlegg.").italic = True

    p_txt = doc.add_paragraph()
    format_paragraph(p_txt)
    p_txt.add_run(
        "Project Controller Frank Ellingsen har gjennomført en fullstendig EVM-avstemming av kommunens tre største investeringsprosjekter. "
        "Samlet portefølje har en vedtatt kostnadsramme (BAC) på kr 517 000 000. Per 31.08.2026 er påløpt kostnad (AC) kr 292 900 000, "
        "mens opptjent verdi (EV) utgjør kr 262 900 000. Dette gir et samlet kostnadsavvik (CV) på kr -30 000 000 og en portefølje-CPI på 0,893. "
        "Sluttoverskridelsen (VAC) estimeres til kr 80 448 796, som anbefales delvis inndekket gjennom trekk på P85-usikkerhetsavsetningene."
    )

    # EVM Tabell
    table = doc.add_table(rows=4, cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    add_table_header_repeat(table)

    headers = ["Prosjekt", "Vedtatt Ramme (BAC)", "Påløpt (AC)", "Opptjent (EV)", "Kostn.indeks (CPI)", "Sluttprognose (EAC)"]
    for c_i, th in enumerate(headers):
        cell = table.cell(0, c_i)
        cell.text = th
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)

    projects = [
        ("Vågsbygd Skole (PROJ-101)", "185 000 000", "104 500 000", "95 000 000", "0,909", "208 251 070 kr"),
        ("Randesund Boenhet (PROJ-201)", "240 000 000", "139 100 000", "117 300 000", "0,843", "299 529 558 kr"),
        ("VA Hovedledning (PROJ-301)", "92 000 000", "49 300 000", "50 600 000", "1,027", "89 668 168 kr")
    ]

    for r_idx, row in enumerate(projects, start=1):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            if c_idx >= 1:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if c_idx == 4 and "0," in val:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_RED_RGB
            set_cell_background(cell, "F9FAFB" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(20)
    p_sig.add_run("Frank Ellingsen\nProject Controller & BI-Spesialist").bold = True

    doc.save(str(target))
    return str(target)


def generate_avviksnotat_enhetsleder_docx(output_path: Optional[str] = None) -> str:
    """
    Nivå 5: Operativ Avviksrapport & Handlingsplan for Enhetsleder (MAL-AVVIK-EFFEKT-001).
    """
    if output_path is None:
        target = Path(__file__).resolve().parents[4] / "word" / "Avviksnotat_og_Handlingsplan_Enhetsleder_2026.docx"
    else:
        target = Path(output_path)

    target.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.984)
        section.bottom_margin = Inches(0.984)
        section.left_margin = Inches(0.984)
        section.right_margin = Inches(0.984)

        header = section.header
        hp = header.paragraphs[0]
        hp.text = "KRISTIANSAND KOMMUNE  •  ENHET 202 GRUNNSKOLE"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = COLOR_GRAY_RGB

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Standard Avviksmønster MAL-AVVIK-EFFEKT-001  |  Stage-Gate Port 9 Sign-off"
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = COLOR_GRAY_RGB

    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)
    r1 = h1.add_run("Operativ Avviksrapport & Handlingsplan: Enhet 202 Grunnskole")
    r1.font.name = "Arial"
    r1.font.size = Pt(18)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_NAVY_RGB

    p_sub = doc.add_paragraph()
    format_paragraph(p_sub, space_after=12)
    p_sub.add_run("Månedlig avviksoppfølging, årsaksdiagnose og 30-dagers tiltaksplan for rektor.").italic = True

    steps = [
        ("1. Avvik Hittil i År (YTD Variance)",
         "Enhet 202 Grunnskole har per august 2026 et samlet merforbruk på kr 1 420 000 (+11,4 % mot periodisert budsjett). "
         "Vedtatt årsramme er kr 18 500 000. Dersom ingen tiltak iverksettes, vil helårsavviket eskalere til kr 2 130 000."),
        
        ("2. Årsak til Avvik (Root Cause via kontonivå)",
         "Kontoart 1020 (Vikarer) viser kr 870 000 i merforbruk som følge av en fraværsbølge blant pedagogisk personale (12,8 % sykefravær). "
         "Kontoart 1090 (Overtid) har et merforbruk på kr 420 000 på grunn av pålegg om sensur og eksamensavvikling. "
         "Kontoart 1600 (NAV Refusjoner) viser etterslep på kr 150 000 på grunn av saksbehandlingstid hos NAV."),
        
        ("3. Forslag til Action Plan (0–30 dager og 30–90 dager)",
         "Tiltak 1 (0–30 dgr): Innføring av administrativt vikarstopp for korttidsfravær under 3 dager. Etablering av intern vikarring.\n"
         "Tiltak 2 (30–90 dgr): Raskere elektronisk innsending av inntektsskjema til NAV for å fremskynde refusjoner.\n"
         "Tiltak 3 (30–90 dgr): Overtidsstopp og godkjenning av all mertid direkte hos rektor."),
        
        ("4. Kvantifisert Effekt & EOY Balanse",
         "Implementering av vikarstopp gir en verifisert månedlig besparelse på kr 170 000 fra 1. september (totalt kr 680 000 i 2026). "
         "Akselerert NAV-refusjon frigjør kr 150 000. Samlet innsparing på kr 830 000 reduserer forventet sluttavvik til kr 590 000, "
         "som foreslås dekket gjennom omdisponering fra disposisjonsfondet jf. Kommuneloven § 14-5.")
    ]

    for s_title, s_body in steps:
        h2 = doc.add_paragraph()
        h2.paragraph_format.space_before = Pt(14)
        h2.paragraph_format.space_after = Pt(4)
        r = h2.add_run(s_title)
        r.font.name = "Arial"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = COLOR_NAVY_RGB

        p_b = doc.add_paragraph()
        format_paragraph(p_b)
        r_b = p_b.add_run(s_body)
        r_b.font.name = "Arial"
        r_b.font.size = Pt(10.5)
        r_b.font.color.rgb = COLOR_DARK_RGB

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(20)
    p_sig.add_run("Frank Ellingsen\nSenior Controller (Attestert Stage-Gate Port 9)").bold = True

    doc.save(str(target))
    return str(target)


if __name__ == "__main__":
    out1 = generate_saksfremlegg_docx()
    out2 = generate_hop_notat_docx()
    out3 = generate_raadmann_notat_docx()
    out4 = generate_sektornotat_oppvekst_docx()
    out5 = generate_prosjektkontroll_capex_docx()
    out6 = generate_avviksnotat_enhetsleder_docx()
    print("Alle 6 Word-dokumenter generert med suksess!")
