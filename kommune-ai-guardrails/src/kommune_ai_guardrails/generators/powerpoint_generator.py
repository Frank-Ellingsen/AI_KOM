"""
PowerPoint Generator for Kristiansand Kommune.
Implementerer POWERPOINT_BYSTYRET_OG_FORMANNSKAPET_DECKS.md,
POWERPOINT_VISUAL_STORYTELLING_FT.md og POWERPOINT_PRESENTASJONSSKAPING_AUTOMATION.md.
"""
from __future__ import annotations

import datetime
import hashlib
from pathlib import Path
from typing import Optional

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Fargepalett fra standarden
COLOR_NAVY = RGBColor(0x1E, 0x3A, 0x8A)      # #1E3A8A Kommune Mørkeblå
COLOR_BG_GRAY = RGBColor(0xF3, 0xF4, 0xF6)   # #F3F4F6 Kommune Lys Grå
COLOR_RED = RGBColor(0xDC, 0x26, 0x26)       # #DC2626 Signal Rød (Alarm)
COLOR_GREEN = RGBColor(0x16, 0xA3, 0x4A)     # #16A34A Signal Grønn (Tiltak/Gevinst)
COLOR_DARK = RGBColor(0x1F, 0x29, 0x37)      # #1F2937 Tekst Mørk Grå
COLOR_MUTED = RGBColor(0x4B, 0x55, 0x63)     # #4B5563 Muted Grå
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)     # #FFFFFF Hvit
COLOR_LIGHT_CARD = RGBColor(0xFA, 0xFA, 0xFA)


def add_header(slide, title_text: str, subtitle_text: str = ""):
    """Legger til standardisert header med FT aksjonstittel."""
    # Toppbånd / Tittelboks
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.font.name = "Arial"

    if subtitle_text:
        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_MUTED
        p2.font.name = "Arial"
        p2.space_before = Pt(4)


def add_footer(slide, sha_stempel: str, slide_num: int, total_slides: int = 7):
    """Legger til audit stempel og sidetall."""
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.4))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"Kristiansand kommune | Økonomi & Virksomhetsstyring  •  Audit ID: {sha_stempel[:12]}  •  Side {slide_num} av {total_slides}"
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_MUTED
    p.font.name = "Arial"


def generate_bystyret_deck(output_path: Optional[str] = None) -> str:
    """
    Bygger et fullverdig 7-slides dekk for Bystyret & Formannskapet
    i henhold til de kommunale spesifikasjonene.
    """
    if output_path is None:
        target = Path(__file__).resolve().parents[4] / "powerpoint" / "Presentasjon_Bystyret_Tertialrapport_2026.pptx"
    else:
        target = Path(output_path)

    target.parent.mkdir(parents=True, exist_ok=True)

    prs = Presentation()
    # 16:9 Widescreen (13.333 x 7.5 tommer)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]
    now_str = datetime.date.today().strftime("%d.%m.%Y")
    audit_hash = hashlib.sha256(f"{datetime.datetime.now().isoformat()}:BYSTYRET_DECK_2026".encode()).hexdigest()

    # --------------------------------------------------------------------------
    # SLIDE 1: Tittelslide (Mørkeblå #1E3A8A)
    # --------------------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.color.rgb = COLOR_NAVY

    # Tittel & Saksinformasjon
    t_box1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(3.5))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "KRISTIANSAND KOMMUNE"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)  # Lys blå
    p.font.name = "Arial"

    p2 = tf1.add_paragraph()
    p2.text = "Økonomisk Status & 2. Tertialrapport 2026"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.font.name = "Arial"
    p2.space_before = Pt(12)

    p3 = tf1.add_paragraph()
    p3.text = "Avviksanalyse, Tiltakspakke og Helårsprognose (EOY) for Enhet 202 Grunnskole"
    p3.font.size = Pt(18)
    p3.font.color.rgb = COLOR_BG_GRAY
    p3.font.name = "Arial"
    p3.space_before = Pt(8)

    # Metadata boks nederst på tittelslide
    m_box1 = slide1.shapes.add_textbox(Inches(1.2), Inches(5.4), Inches(11.0), Inches(1.2))
    tf_m = m_box1.text_frame
    p_m1 = tf_m.paragraphs[0]
    p_m1.text = f"Saksbehandler: Frank Ellingsen, Senior Controller  |  Møte: Bystyret / Formannskapet  |  Dato: {now_str}"
    p_m1.font.size = Pt(11)
    p_m1.font.color.rgb = RGBColor(0xBF, 0xDB, 0xFE)

    p_m2 = tf_m.add_paragraph()
    p_m2.text = f"Kommune-Audit Stempel (SHA-256): {audit_hash[:24]}...  |  Hjemmel: Kommuneloven § 14-5"
    p_m2.font.size = Pt(10)
    p_m2.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
    p_m2.space_before = Pt(4)

    # --------------------------------------------------------------------------
    # SLIDE 2: Hovedbudskap / Executive Summary (3 store KPI-kort)
    # --------------------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(
        slide2,
        "Hovedbudskap: Merforbruk i Grunnskolen isolert – Tiltak sikrer balanse",
        "Executive Summary: YTD avvik krever justering, men handlingsplan reduserer helårsbelastningen til kr 350 000"
    )

    card_data = [
        ("YTD MERFORBRUK", "+850 000 kr", "+12,4 % over budsjettramme Q2", COLOR_RED),
        ("HOVEDÅRSAK VIKAR", "620 000 kr", "Konto 1020 (14,2 % sesongsykefravær)", COLOR_NAVY),
        ("FORVENTET EOY BALANSE", "+350 000 kr", "Dekkes inn via omstillingsfond (§ 14-5)", COLOR_GREEN),
    ]

    left_margin = 0.8
    card_width = 3.6
    gap = 0.4
    for i, (kpi_title, kpi_val, kpi_sub, color_accent) in enumerate(card_data):
        c_left = Inches(left_margin + i * (card_width + gap))
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.8), Inches(card_width), Inches(2.5))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_CARD
        card.line.color.rgb = RGBColor(0xE5, 0xE7, 0xEB)

        tb = slide2.shapes.add_textbox(c_left + Inches(0.2), Inches(2.0), Inches(card_width - 0.4), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = kpi_title
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_MUTED

        p2 = tf.add_paragraph()
        p2.text = kpi_val
        p2.font.size = Pt(28)
        p2.font.bold = True
        p2.font.color.rgb = color_accent
        p2.space_before = Pt(10)

        p3 = tf.add_paragraph()
        p3.text = kpi_sub
        p3.font.size = Pt(11)
        p3.font.color.rgb = COLOR_DARK
        p3.space_before = Pt(8)

    # Konklusjonsboks under kortene
    info_box = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.7), Inches(1.8))
    info_box.fill.solid()
    info_box.fill.fore_color.rgb = COLOR_BG_GRAY
    info_box.line.color.rgb = RGBColor(0xDB, 0xEA, 0xFE)

    tf_info = info_box.text_frame
    tf_info.word_wrap = True
    p_i = tf_info.paragraphs[0]
    p_i.text = "Viktigste observasjoner for Kommunedirektøren og Bystyret:"
    p_i.font.size = Pt(13)
    p_i.font.bold = True
    p_i.font.color.rgb = COLOR_NAVY

    p_i2 = tf_info.add_paragraph()
    p_i2.text = "• Avviket er konsentrert til Enhet 202 Grunnskole – øvrige skoler i Kristiansand leverer innenfor tildelt budsjettramme."
    p_i2.font.size = Pt(11)
    p_i2.font.color.rgb = COLOR_DARK
    p_i2.space_before = Pt(4)

    p_i3 = tf_info.add_paragraph()
    p_i3.text = "• Refusjonsetterslep fra NAV (konto 1600) på kr 180 000 vil reverseres i Q3 etter oversendelse av samlekrav."
    p_i3.font.size = Pt(11)
    p_i3.font.color.rgb = COLOR_DARK

    p_i4 = tf_info.add_paragraph()
    p_i4.text = "• Med iverksatte tiltak fra 1. august holdes samlet årsresultat innenfor rammene av Kommuneloven § 14-5."
    p_i4.font.size = Pt(11)
    p_i4.font.color.rgb = COLOR_DARK

    add_footer(slide2, audit_hash, 2)

    # --------------------------------------------------------------------------
    # SLIDE 3: YTD Avviksstatus (Tabell og avviksstolper)
    # --------------------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(
        slide3,
        "YTD Avviksstatus: Enhet 202 har 12,4 % merforbruk per 30.06.2026",
        "Regnskap mot periodisert ramme iht. KOSTRA-artsfordeling i Visma Enterprise ERP"
    )

    # Tabell med regnskapstall
    table_shape = slide3.shapes.add_table(5, 5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(3.2))
    table = table_shape.table
    table.columns[0].width = Inches(3.8)
    table.columns[1].width = Inches(2.0)
    table.columns[2].width = Inches(2.0)
    table.columns[3].width = Inches(2.0)
    table.columns[4].width = Inches(1.9)

    headers = ["Kontoart / Beskrivelse", "Budsjett Q2", "Faktisk Q2", "Avvik Kr", "Avvik %"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.RIGHT

    rows_data = [
        ("Art 1010 Faste lønninger", "4 850 000 kr", "4 890 000 kr", "+40 000 kr", "+0,8 %"),
        ("Art 1020 Innkjøp av vikarer (timelærere)", "1 200 000 kr", "1 820 000 kr", "+620 000 kr", "+51,7 %"),
        ("Art 1090 Overtid og kveldstillegg", "57 000 kr", "436 000 kr", "+379 000 kr", "+664,9 %"),
        ("Art 1600 NAV-refusjoner (sykepenger)", "-590 000 kr", "-410 000 kr", "+180 000 kr", "-30,5 %"),
    ]

    for row_idx, r_vals in enumerate(rows_data, 1):
        for col_idx, val in enumerate(r_vals):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_LIGHT_CARD if row_idx % 2 == 0 else COLOR_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.name = "Arial"
            if col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = COLOR_RED if "+" in val and "40 000" not in val else COLOR_DARK
            p.alignment = PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.RIGHT

    # Oppsummeringslinje under tabellen
    sum_box = slide3.shapes.add_textbox(Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.3))
    tf_sum = sum_box.text_frame
    p_s = tf_sum.paragraphs[0]
    p_s.text = "Totalt Enhet 202 Grunnskole: Budsjett kr 6 850 000  |  Faktisk kr 7 700 000  |  Avvik: +850 000 kr (+12,4 %)"
    p_s.font.size = Pt(13)
    p_s.font.bold = True
    p_s.font.color.rgb = COLOR_RED

    p_s2 = tf_sum.add_paragraph()
    p_s2.text = "Merk: Jf. bruttoprinsippet i Kommuneloven § 14-6 fjerde ledd er det ikke adgang til å motregne vikarutgiftene mot forventede refusjoner. Hver post må føres og rapporteres brutto."
    p_s2.font.size = Pt(10.5)
    p_s2.font.color.rgb = COLOR_MUTED
    p_s2.space_before = Pt(4)

    add_footer(slide3, audit_hash, 3)

    # --------------------------------------------------------------------------
    # SLIDE 4: Rotårsak & Nedbrytning (Waterfall / Avviksbro)
    # --------------------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(
        slide4,
        "Rotårsak: Vikarforbruk og refusjonsetterslep utgjør 94 % av avviket",
        "Avviksbro (Waterfall) fra opprinnelig tildelt ramme til faktisk regnskapsført forbruk"
    )

    steps = [
        ("Tildelt Ramme", "6 850 000", "Opprinnelig budsjett", COLOR_NAVY),
        ("+ Vikarer (1020)", "+620 000", "14,2 % sesongfravær", COLOR_RED),
        ("+ Overtid (1090)", "+379 000", "Akutt vikarmangel", COLOR_RED),
        ("- NAV Refusjon (1600)", "+180 000", "48 dg saksbehandling", COLOR_RED),
        ("Øvrig Drift", "-329 000", "Innsparing læremidler", COLOR_GREEN),
        ("Faktisk Regnskap", "7 700 000", "Sum per 30.06.2026", COLOR_NAVY),
    ]

    w_width = 1.75
    w_gap = 0.22
    for i, (lbl, belop, sub, col) in enumerate(steps):
        s_left = Inches(0.8 + i * (w_width + w_gap))
        s_box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s_left, Inches(2.0), Inches(w_width), Inches(3.2))
        s_box.fill.solid()
        s_box.fill.fore_color.rgb = COLOR_LIGHT_CARD
        s_box.line.color.rgb = col
        s_box.line.width = Pt(1.5)

        tf = s_box.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = lbl
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_DARK

        p2 = tf.add_paragraph()
        p2.text = belop
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = col
        p2.space_before = Pt(8)

        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = COLOR_MUTED
        p3.space_before = Pt(6)

    # Diagnose-forklaring
    exp_box = slide4.shapes.add_textbox(Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.1))
    tf_exp = exp_box.text_frame
    p_e = tf_exp.paragraphs[0]
    p_e.text = "Årsaksdiagnose for Bystyret:"
    p_e.font.size = Pt(12)
    p_e.font.bold = True
    p_e.font.color.rgb = COLOR_NAVY

    p_e2 = tf_exp.add_paragraph()
    p_e2.text = "1. Vikarbruken skyldes en opphopning av langtidssykefravær blant kontaktlærere i mai og juni.\n2. NAV-etterslepet representerer et midlertidig likviditets- og periodiseringsavvik som reverseres ved utbetaling."
    p_e2.font.size = Pt(10.5)
    p_e2.font.color.rgb = COLOR_DARK

    add_footer(slide4, audit_hash, 4)

    # --------------------------------------------------------------------------
    # SLIDE 5: Handlingsplan & Kvantifisert Effekt (Tiltaksliste)
    # --------------------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(
        slide5,
        "Handlingsplan: To-trinns tiltakspakke kutter månedlig merforbruk med 170 000 kr",
        "Kvantifiserte strakstiltak (0–30 dager) og strukturelle endringer (30–90 dager) forankret i partssamarbeid"
    )

    t1_box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(3.6))
    t1_box.fill.solid()
    t1_box.fill.fore_color.rgb = COLOR_LIGHT_CARD
    t1_box.line.color.rgb = COLOR_GREEN
    t1_box.line.width = Pt(1.5)

    tf_t1 = t1_box.text_frame
    tf_t1.word_wrap = True
    p = tf_t1.paragraphs[0]
    p.text = "FASE 1: STRAKSTILTAK (0–30 DAGER)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    items1 = [
        ("Klassesammenslåing:", "Ved korttidsfravær < 3 dager slås parallellklasser sammen i fellesfag."),
        ("Samlepurring NAV:", "Aktiv oppfølging av utestående refusjonskrav på 180 000 kr."),
        ("Innkjøpsfrys:", "Midlertidig stans i ikke-kritiske læremiddelanskaffelser."),
        ("Effekt:", "Kutter vikarutgifter med ca. 70 000 kr/mnd fra august.")
    ]
    for title, desc in items1:
        p = tf_t1.add_paragraph()
        p.text = f"• {title} {desc}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_DARK
        p.space_before = Pt(5)

    t2_box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(3.6))
    t2_box.fill.solid()
    t2_box.fill.fore_color.rgb = COLOR_LIGHT_CARD
    t2_box.line.color.rgb = COLOR_NAVY
    t2_box.line.width = Pt(1.5)

    tf_t2 = t2_box.text_frame
    tf_t2.word_wrap = True
    p = tf_t2.paragraphs[0]
    p.text = "FASE 2: STRUKTURELLE TILTAK (30–90 DAGER)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    items2 = [
        ("Felles Vikarpool:", "Etablering av fast ansatte ressurspersoner på tvers av skolene i Oppvekstsektoren."),
        ("Partssamarbeid (HTA § 4):", "Drøftet med Utdanningsforbundet og Fagforbundet med positiv tilslutning."),
        ("Seniorordninger:", "Bruk av seniorkompetanse ved eksamen og vurdering fremfor eksterne vikarer."),
        ("Helårseffekt:", "Kutter strukturelle ekstrakostnader med ca. 680 000 kr på årsbasis.")
    ]
    for title, desc in items2:
        p = tf_t2.add_paragraph()
        p.text = f"• {title} {desc}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_DARK
        p.space_before = Pt(5)

    sum_t = slide5.shapes.add_textbox(Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.0))
    tf_st = sum_t.text_frame
    p = tf_st.paragraphs[0]
    p.text = "Samlet kvantifisert effekt: 170 000 kr i reduserte månedlige driftsutgifter i 2. halvår = 850 000 kr total besparelse."
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    add_footer(slide5, audit_hash, 5)

    # --------------------------------------------------------------------------
    # SLIDE 6: Prognosebane EOY per 31.12 (Fan Chart P10/P50/P90)
    # --------------------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(
        slide6,
        "Prognosebane EOY: Helårsavvik reduseres fra 1,72 mill. til 350 000 kr",
        "Monte Carlo-simulerte utfall (P10 / P50 / P90) per 31.12.2026 med og uten tiltakspakke"
    )

    scenarios = [
        ("P90: Worst Case (Uten tiltak)", "+1 720 000 kr", "Sykefravær forblir 14 % og ingen tiltak iverksettes. Krever omfattende kutt i andre sektorer.", COLOR_RED),
        ("P50: Base Case (Moderat effekt)", "+850 000 kr", "Halvparten av tiltakene slår inn og NAV-refusjoner forsinkes til Q4.", COLOR_NAVY),
        ("P10: Målsetting (Full tiltakseffekt)", "+350 000 kr", "Full gjennomføring av vikarpool og sammenslåing. Dekkes inn via disposisjonsfond.", COLOR_GREEN),
    ]

    for i, (sc_title, sc_val, sc_desc, sc_col) in enumerate(scenarios):
        b_top = Inches(1.8 + i * 1.5)
        box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), b_top, Inches(11.7), Inches(1.3))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_LIGHT_CARD
        box.line.color.rgb = sc_col
        box.line.width = Pt(1.5)

        tf = box.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"{sc_title}   ───   {sc_val}"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = sc_col

        p2 = tf.add_paragraph()
        p2.text = sc_desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_DARK
        p2.space_before = Pt(3)

    cov_box = slide6.shapes.add_textbox(Inches(0.8), Inches(6.1), Inches(11.7), Inches(0.7))
    tf_c = cov_box.text_frame
    p = tf_c.paragraphs[0]
    p.text = "Dekningskilde: Det gjenstående avviket på 350 000 kr foreslås dekket inn via Oppvekstsektorens omstillingsfond jf. § 14-5."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    add_footer(slide6, audit_hash, 6)

    # --------------------------------------------------------------------------
    # SLIDE 7: Oppsummering & Anbefalt Politisk Vedtak
    # --------------------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(
        slide7,
        "Kommunedirektørens forslag til vedtak i Bystyret",
        "Formell sak fremmet i medhold av Kommuneloven § 14-5 for 2. tertialrapport 2026"
    )

    vedtak_box = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.3))
    vedtak_box.fill.solid()
    vedtak_box.fill.fore_color.rgb = COLOR_BG_GRAY
    vedtak_box.line.color.rgb = COLOR_NAVY
    vedtak_box.line.width = Pt(2)

    tf_v = vedtak_box.text_frame
    tf_v.word_wrap = True

    p = tf_v.paragraphs[0]
    p.text = "Kommunedirektøren innstiller overfor Bystyret følgende vedtak:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    vedtakspunkter = [
        "1. Bystyret tar orienteringen om den økonomiske situasjonen i Enhet 202 Grunnskole per 2. tertial 2026 til etterretning.",
        "2. Bystyret godkjenner i medhold av Kommuneloven § 14-5 at et forventet merforbruk på inntil kr 350 000 dekkes inn gjennom omdisponering fra Oppvekstsektorens omstillingsfond.",
        "3. Kommunedirektøren pålegges å iverksette tiltakspakken for vikarbruk, herunder opprettelse av felles vikarpool i tråd med Hovedtariffavtalen § 4, med virkning fra 1. august 2026.",
        "4. Status for tiltakene og oppdatert helårsprognose legges frem i forbindelse med 3. tertialrapport 2026 og budsjett 2027."
    ]

    for v in vedtakspunkter:
        p = tf_v.add_paragraph()
        p.text = v
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_DARK
        p.space_before = Pt(10)

    # Signaturfelt
    p_sig = tf_v.add_paragraph()
    p_sig.text = "Kristiansand, " + now_str + "  •  Camilla Dunsæd, Kommunedirektør  /  Frank Ellingsen, Senior Controller"
    p_sig.font.size = Pt(10)
    p_sig.font.italic = True
    p_sig.font.color.rgb = COLOR_MUTED
    p_sig.space_before = Pt(14)

    add_footer(slide7, audit_hash, 7)

    prs.save(str(target))
    return str(target)


# ==============================================================================
# DEKK 2: KOMMUNEDIREKTØRENS LEDERGRUPPE (NIVÅ 2: KONSERN)
# ==============================================================================
def generate_konsern_deck(output_path: Optional[str] = None) -> str:
    """
    Bygger et 7-slides dekk for Kommunedirektørens ledergruppe:
    Månedlig konsernoppfølging, vikarstopp-effekt og likviditetsbilde.
    """
    if output_path is None:
        target = Path(__file__).resolve().parents[4] / "powerpoint" / "Presentasjon_Kommunedirektoren_Konsernstyring_2026.pptx"
    else:
        target = Path(output_path)

    target.parent.mkdir(parents=True, exist_ok=True)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    now_str = datetime.date.today().strftime("%d.%m.%Y")
    audit_hash = hashlib.sha256(f"{datetime.datetime.now().isoformat()}:KONSERN_DECK_2026".encode()).hexdigest()

    # SLIDE 1: Tittel
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.color.rgb = COLOR_NAVY

    tb1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(3.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "KRISTIANSAND KOMMUNE  •  KOMMUNEDIREKTØRENS LEDERGRUPPE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)

    p2 = tf1.add_paragraph()
    p2.text = "Månedsrapport: Konsernoppfølging & Strakstiltaksplan 2026"
    p2.font.size = Pt(30)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(12)

    p3 = tf1.add_paragraph()
    p3.text = "Status Driftsregnskap per 2. Tertial  |  Internkontroll jf. Kommuneloven § 14-5  |  Offl. § 14"
    p3.font.size = Pt(15)
    p3.font.color.rgb = RGBColor(0xE0, 0xE7, 0xFF)
    p3.space_before = Pt(8)

    p4 = tf1.add_paragraph()
    p4.text = f"Dato: {now_str}  •  Camilla Dunsæd, Kommunedirektør  /  Frank Ellingsen, Senior Controller"
    p4.font.size = Pt(11.5)
    p4.font.color.rgb = RGBColor(0xBF, 0xDB, 0xFE)
    p4.space_before = Pt(28)

    p5 = tf1.add_paragraph()
    p5.text = f"Audit Stempel (SHA-256): {audit_hash[:24]}...  |  Stage-Gate Port 9 Attestert"
    p5.font.size = Pt(9.5)
    p5.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
    p5.space_before = Pt(4)

    # SLIDE 2: Konsern KPI-Dashboard
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(
        slide2,
        "Konsernstatus: Netto merforbruk på 2,49 mill. kr – Strakstiltak ACT 01–04 iverksatt",
        "Executive Dashboard for Kommunedirektøren: Månedsoppfølging av driftsbalanse, likviditet og lånegjeld"
    )

    kpis = [
        ("NETTO DRIFTSRESULTAT", "1,75 %", "Mål: >= 1,75 % av brutto inntekter", COLOR_GREEN),
        ("DISPOSISJONSFOND", "8,2 % / 615 Mkr", "Mål: >= 8,0 % (Robust reserve)", COLOR_NAVY),
        ("LÅNEGJELD KONSOLIDERT", "83,1 % / 6,8 mrd", "Maks 85 % av inntekter ekskl. VA", COLOR_RED),
    ]
    for i, (kt, kv, ks, kc) in enumerate(kpis):
        c_left = Inches(0.8 + i * 4.0)
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.8), Inches(3.7), Inches(2.5))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_CARD
        card.line.color.rgb = RGBColor(0xE5, 0xE7, 0xEB)

        tb = slide2.shapes.add_textbox(c_left + Inches(0.2), Inches(2.0), Inches(3.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = kt
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED

        p2 = tf.add_paragraph()
        p2.text = kv
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = kc
        p2.space_before = Pt(8)

        p3 = tf.add_paragraph()
        p3.text = ks
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = COLOR_DARK
        p3.space_before = Pt(6)

    ib2 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.7), Inches(1.9))
    ib2.fill.solid()
    ib2.fill.fore_color.rgb = COLOR_BG_GRAY
    ib2.line.color.rgb = RGBColor(0xDB, 0xEA, 0xFE)
    tf_ib2 = ib2.text_frame
    tf_ib2.word_wrap = True
    p = tf_ib2.paragraphs[0]
    p.text = "Konklusjon for ledergruppen:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p2 = tf_ib2.add_paragraph()
    p2.text = "• Samlet konsernavvik på 2 489 000 kr drives av Oppvekst (1,42M) og Helse (1,07M) – Byutvikling har mindreforbruk (-0,2M)."
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_DARK
    p2.space_before = Pt(4)
    p3 = tf_ib2.add_paragraph()
    p3.text = "• Strakstiltakene ACT-01 til ACT-04 frigjør kr 460 000 per måned fra 1. september og bringer helårsdriften i balanse."
    p3.font.size = Pt(11)
    p3.font.color.rgb = COLOR_DARK
    add_footer(slide2, audit_hash, 2)

    # SLIDE 3: Sektorvis Driftsavvik
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(
        slide3,
        "Sektoravvik: Oppvekst og Helse står for 100 % av driftsmerforbruket i konsernet",
        "Periodisert driftsregnskap per august 2026 i henhold til KOSTRA-rammer og bruttoprinsippet § 14-6"
    )
    t_shape3 = slide3.shapes.add_table(7, 5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.2))
    table3 = t_shape3.table
    table3.columns[0].width = Inches(3.7)
    table3.columns[1].width = Inches(2.0)
    table3.columns[2].width = Inches(2.0)
    table3.columns[3].width = Inches(2.0)
    table3.columns[4].width = Inches(2.0)

    heads3 = ["Sektor / Virksomhetsområde", "Budsjett YTD", "Regnskap YTD", "Avvik Kr", "Avvik %"]
    for c_i, h in enumerate(heads3):
        cell = table3.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.LEFT if c_i == 0 else PP_ALIGN.RIGHT

    s_rows = [
        ("01 Oppvekst og Utdanning (Grunnskole/Barnehage)", "850 000 000 kr", "851 420 000 kr", "+1 420 000 kr", "+0,17 %", COLOR_RED),
        ("02 Helse og Mestring (Omsorgssentre/Hjemmetjeneste)", "920 000 000 kr", "921 069 000 kr", "+1 069 000 kr", "+0,12 %", COLOR_RED),
        ("03 By- og Stedsutvikling (Eiendom, Samferdsel, Park)", "310 000 000 kr", "309 800 000 kr", "-200 000 kr", "-0,06 %", COLOR_GREEN),
        ("04 Kultur og Innbyggerdialog (Bibliotek, Idrett)", "180 000 000 kr", "180 100 000 kr", "+100 000 kr", "+0,06 %", COLOR_MUTED),
        ("05 Sentral Administrasjon & Fellestjenester", "140 000 000 kr", "140 100 000 kr", "+100 000 kr", "+0,07 %", COLOR_MUTED),
        ("TOTALT KONSOLIDERT DRIFTSREGNSKAP", "2 400 000 000 kr", "2 402 489 000 kr", "+2 489 000 kr", "+0,10 %", COLOR_RED)
    ]
    for r_i, (s_name, b_val, r_val, v_val, v_pct, v_col) in enumerate(s_rows, 1):
        vals = [s_name, b_val, r_val, v_val, v_pct]
        for c_i, v in enumerate(vals):
            cell = table3.cell(r_i, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_LIGHT_CARD if r_i % 2 == 0 else COLOR_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = v
            p.font.size = Pt(10)
            p.alignment = PP_ALIGN.LEFT if c_i == 0 else PP_ALIGN.RIGHT
            if r_i == 6:
                p.font.bold = True
            if c_i in (3, 4):
                p.font.bold = True
                p.font.color.rgb = v_col
    add_footer(slide3, audit_hash, 3)

    # SLIDE 4: Administrative Strakstiltak (ACT-01 til ACT-04)
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(
        slide4,
        "Strakstiltaksplan: 4 administrative grep kutter 460 000 kr/mnd fra 1. september",
        "Iverksatt av Kommunedirektøren i medhold av internkontrollbestemmelsene i Kommuneloven § 14-5"
    )
    acts = [
        ("ACT-01: Vikarstopp Grunnskole", "Sektor Oppvekst", "Stopp for korttidsinnleie (< 3 dager). Etablering av intern vikarring mellom skolene i Vågsbygd og Grim.", "170 000 kr / mnd", COLOR_GREEN),
        ("ACT-02: Bemanningsjustering Helse", "Sektor Helse og Mestring", "Innføring av langvakter, omfordeling av turnus og restriksjoner på kjøp av private helsevikarer.", "145 000 kr / mnd", COLOR_GREEN),
        ("ACT-03: Konsulent- og Kursstopp", "Sektor Kultur & Organisasjon", "Full stopp for nye eksterne konsulentavtaler, seminarer og ikke-lovpålagt kompetanseheving.", "65 000 kr / mnd", COLOR_GREEN),
        ("ACT-04: IKT & Lisenskonsolidering", "Fellestjenester", "Oppsigelse av overlappende programvarelisenser og utsettelse av administrative PC-kjøp.", "80 000 kr / mnd", COLOR_GREEN),
    ]
    for i, (act_t, act_s, act_d, act_e, act_c) in enumerate(acts):
        row = i // 2
        col = i % 2
        c_left = Inches(0.8 + col * 6.0)
        c_top = Inches(1.8 + row * 2.3)
        box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, c_top, Inches(5.7), Inches(2.1))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_LIGHT_CARD
        box.line.color.rgb = RGBColor(0xDB, 0xEA, 0xFE)

        tb = slide4.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.15), Inches(5.3), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = act_t
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY

        p2 = tf.add_paragraph()
        p2.text = f"{act_s}  •  Beregnet effekt: {act_e}"
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = act_c
        p2.space_before = Pt(3)

        p3 = tf.add_paragraph()
        p3.text = act_d
        p3.font.size = Pt(10)
        p3.font.color.rgb = COLOR_DARK
        p3.space_before = Pt(4)
    add_footer(slide4, audit_hash, 4)

    # SLIDE 5: Likviditet & Rentefølsomhet
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(
        slide5,
        "Likviditet og Rentefølsomhet: 62 % fastrente beskytter mot videre renteoppgang",
        "Finansiell risikoprofil for Kristiansand kommunes samlede låneportefølje på 6,8 milliarder kr"
    )
    fin_kpis = [
        ("LIKVIDITETSRESERVE", "420 Mkr", "Ubenyttede trekkrettigheter og bankinnskudd", COLOR_NAVY),
        ("RENTESENSITIVITET (+50 bps)", "+12,9 Mkr", "Årlig merkostnad på usikret flytende gjeld", COLOR_RED),
        ("FASTRENTEANDEL (SWAPS)", "62,4 %", "I tråd med finansreglementets krav (50–70 %)", COLOR_GREEN),
    ]
    for i, (ft, fv, fs, fc) in enumerate(fin_kpis):
        c_left = Inches(0.8 + i * 4.0)
        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.8), Inches(3.7), Inches(2.4))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_CARD
        card.line.color.rgb = RGBColor(0xE5, 0xE7, 0xEB)

        tb = slide5.shapes.add_textbox(c_left + Inches(0.2), Inches(1.95), Inches(3.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = ft
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED
        p2 = tf.add_paragraph()
        p2.text = fv
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = fc
        p2.space_before = Pt(8)
        p3 = tf.add_paragraph()
        p3.text = fs
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = COLOR_DARK
        p3.space_before = Pt(6)

    # Forfallsprofil boks
    fb = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.5), Inches(11.7), Inches(2.1))
    fb.fill.solid()
    fb.fill.fore_color.rgb = COLOR_BG_GRAY
    fb.line.color.rgb = RGBColor(0xDB, 0xEA, 0xFE)
    tf_fb = fb.text_frame
    tf_fb.word_wrap = True
    p = tf_fb.paragraphs[0]
    p.text = "Gjeldsstruktur og refinansieringsrisiko:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p2 = tf_fb.add_paragraph()
    p2.text = "• Sertifikatlån på kr 450 000 000 forfaller i Q4 2026. Refinansieres via Kommunalbanken med 5-årig fastrentelån."
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_DARK
    p2.space_before = Pt(4)
    p3 = tf_fb.add_paragraph()
    p3.text = "• Gjennomsnittlig rentebindingstid er 3,8 år. Kommunens likviditetsbuffer tilfredsstiller stresstest for 30 dagers drift."
    p3.font.size = Pt(11)
    p3.font.color.rgb = COLOR_DARK
    add_footer(slide5, audit_hash, 5)

    # SLIDE 6: Helårsprognose Konsern EOY
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(
        slide6,
        "Helårsprognose EOY: Forventet netto driftsresultat lander på 225 mill. kr (1,81 %)",
        "Scenariovurdering for årsresultat 2026 basert på strakstiltak og forventet skatteinngang"
    )
    scenarios = [
        ("P90 / Worst Case (Uten tiltak)", "178 Mkr (1,43 %)", "Risiko for brudd på handlingsregelen (krav 1,75 %). Inndekning krever kutt i disposisjonsfond.", COLOR_RED),
        ("P50 / Forventet Bane (Med strakstiltak)", "225 Mkr (1,81 %)", "Tiltakspakken på 460k/mnd gjenoppretter balanse. Robust margin på 7,5 Mkr over måltall.", COLOR_GREEN),
        ("P10 / Best Case (Full tiltakseffekt + skatt)", "248 Mkr (1,99 %)", "Akselerert NAV-refusjon og ekstraordinær skatteinngang gir solid overskudd til disposisjonsfond.", COLOR_NAVY)
    ]
    for i, (st, sv, sd, sc) in enumerate(scenarios):
        box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8 + i * 1.5), Inches(11.7), Inches(1.3))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_LIGHT_CARD
        box.line.color.rgb = sc
        box.line.width = Pt(1.5)
        tb = slide6.shapes.add_textbox(Inches(1.0), Inches(1.85 + i * 1.5), Inches(11.3), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f"{st}  ───  {sv}"
        p1.font.size = Pt(13.5)
        p1.font.bold = True
        p1.font.color.rgb = sc
        p2 = tf.add_paragraph()
        p2.text = sd
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_DARK
        p2.space_before = Pt(3)
    add_footer(slide6, audit_hash, 6)

    # SLIDE 7: Beslutningspunkter for Ledergruppen
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(
        slide7,
        "Oppsummering & Beslutningsliste for Kommunedirektørens Ledergruppe",
        "Oppfølgingspunkter for september–desember 2026 jf. internkontrollforskriften"
    )
    vb7 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.5))
    vb7.fill.solid()
    vb7.fill.fore_color.rgb = COLOR_BG_GRAY
    vb7.line.color.rgb = COLOR_NAVY
    vb7.line.width = Pt(2)
    tf_vb7 = vb7.text_frame
    tf_vb7.word_wrap = True

    p = tf_vb7.paragraphs[0]
    p.text = "Ledergruppens vedtatte tiltaksbeslutninger:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    decisions = [
        "1. Kommunalsjef Oppvekst rapporterer ukentlig vikarforbruk til økonomisjef inntil månedskostnad er stabilisert under 80 000 kr.",
        "2. Kommunalsjef Helse iverksetter turnusjustering med langvakter for å eliminere uplanlagt overtid fra uke 36.",
        "3. Innkjøpsavdelingen stenger for nye konsulentrekvisisjoner uten personlig forhåndsgodkjenning fra kommunedirektøren.",
        "4. Økonomiavdelingen forbereder sak til Formannskapet om omdisponering av kr 3,2M fra disposisjonsfondet jf. Kommuneloven § 14-5."
    ]
    for d in decisions:
        pd = tf_vb7.add_paragraph()
        pd.text = d
        pd.font.size = Pt(11.5)
        pd.font.color.rgb = COLOR_DARK
        pd.space_before = Pt(10)

    p_sig = tf_vb7.add_paragraph()
    p_sig.text = "Kristiansand, " + now_str + "  •  Camilla Dunsæd, Kommunedirektør  /  Frank Ellingsen, Senior Controller"
    p_sig.font.size = Pt(10)
    p_sig.font.italic = True
    p_sig.font.color.rgb = COLOR_MUTED
    p_sig.space_before = Pt(14)
    add_footer(slide7, audit_hash, 7)

    prs.save(str(target))
    return str(target)


# ==============================================================================
# DEKK 3: SEKTOR OPPVEKST & UTDANNING (NIVÅ 3: KOMMUNALSJEF / REKTORER)
# ==============================================================================
def generate_oppvekst_deck(output_path: Optional[str] = None) -> str:
    """
    Bygger et 7-slides dekk for Sektor Oppvekst og Utdanning:
    Bemanningskontroll, lærernorm og vikaroptimalisering for grunnskolene.
    """
    if output_path is None:
        target = Path(__file__).resolve().parents[4] / "powerpoint" / "Presentasjon_Oppvekst_Bemanningskontroll_2026.pptx"
    else:
        target = Path(output_path)

    target.parent.mkdir(parents=True, exist_ok=True)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    now_str = datetime.date.today().strftime("%d.%m.%Y")
    audit_hash = hashlib.sha256(f"{datetime.datetime.now().isoformat()}:OPPVEKST_DECK_2026".encode()).hexdigest()

    # SLIDE 1: Tittel
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.color.rgb = COLOR_NAVY

    tb1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(3.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "KRISTIANSAND KOMMUNE  •  SEKTOR OPPVEKST OG UTDANNING"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)

    p2 = tf1.add_paragraph()
    p2.text = "Bemanningskontroll, Lærernorm & Vikaroptimalisering 2026"
    p2.font.size = Pt(30)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(12)

    p3 = tf1.add_paragraph()
    p3.text = "Enhetsvis Avviksoppfølging  |  Opplæringsloven § 8-2  |  KOSTRA 1020 Innleie"
    p3.font.size = Pt(15)
    p3.font.color.rgb = RGBColor(0xE0, 0xE7, 0xFF)
    p3.space_before = Pt(8)

    p4 = tf1.add_paragraph()
    p4.text = f"Dato: {now_str}  •  Kristin E. Bakke, Kommunalsjef  /  Frank Ellingsen, Senior Controller"
    p4.font.size = Pt(11.5)
    p4.font.color.rgb = RGBColor(0xBF, 0xDB, 0xFE)
    p4.space_before = Pt(28)
    p5 = tf1.add_paragraph()
    p5.text = f"Audit Stempel: {audit_hash[:24]}...  |  Møte med Grunnskolerektorene"
    p5.font.size = Pt(9.5)
    p5.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
    p5.space_before = Pt(4)

    # SLIDE 2: Hovedutfordring Oppvekst
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(
        slide2,
        "Oppvekst: Vikarforbruk i grunnskolen utgjør 1,42 mill. kr i udekket merforbruk",
        "Executive Summary for rektormøtet: Bakgrunn for iverksetting av felles vikarring og vikarstopp"
    )
    kpis = [
        ("YTD MERFORBRUK SKOLER", "+1 420 000 kr", "Grim og Vågsbygd driver 61 % av avviket", COLOR_RED),
        ("SYKEFRAVÆR PED. PERSONALE", "12,8 %", "Hovedsakelig sesongpreget korttidsfravær", COLOR_NAVY),
        ("VIKARSTOPP INNSPARING", "-680 000 kr", "Beregnet effekt 1. sept – 31. des 2026", COLOR_GREEN),
    ]
    for i, (kt, kv, ks, kc) in enumerate(kpis):
        c_left = Inches(0.8 + i * 4.0)
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.8), Inches(3.7), Inches(2.5))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_CARD
        card.line.color.rgb = RGBColor(0xE5, 0xE7, 0xEB)
        tb = slide2.shapes.add_textbox(c_left + Inches(0.2), Inches(2.0), Inches(3.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = kt
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED
        p2 = tf.add_paragraph()
        p2.text = kv
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = kc
        p2.space_before = Pt(8)
        p3 = tf.add_paragraph()
        p3.text = ks
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = COLOR_DARK
        p3.space_before = Pt(6)

    ib2 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.7), Inches(1.9))
    ib2.fill.solid()
    ib2.fill.fore_color.rgb = COLOR_BG_GRAY
    ib2.line.color.rgb = RGBColor(0xDB, 0xEA, 0xFE)
    tf_ib2 = ib2.text_frame
    tf_ib2.word_wrap = True
    p = tf_ib2.paragraphs[0]
    p.text = "Fokusområder for rektorene i høstsemesteret:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p2 = tf_ib2.add_paragraph()
    p2.text = "• Vikarbruk skal forhåndsklareres internt: Korttidsfravær dag 1–2 løses ved sammenslåing eller timebytte."
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_DARK
    p2.space_before = Pt(4)
    p3 = tf_ib2.add_paragraph()
    p3.text = "• NAV-refusjonskrav skal sendes digitalt senest 5 dager etter endt fraværsperiode for å unngå likviditetsetterslep."
    p3.font.size = Pt(11)
    p3.font.color.rgb = COLOR_DARK
    add_footer(slide2, audit_hash, 2)

    # SLIDE 3: Skolevis Avviksmatrise
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(
        slide3,
        "Skolematrise: Grim og Lovisenlev har de høyeste avvikene mot periodisert budsjett",
        "Regnskapstall per 31.08.2026 for de fire største grunnskolene i Kristiansand"
    )
    t_shape3 = slide3.shapes.add_table(5, 5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(3.6))
    table3 = t_shape3.table
    table3.columns[0].width = Inches(3.7)
    table3.columns[1].width = Inches(2.0)
    table3.columns[2].width = Inches(2.0)
    table3.columns[3].width = Inches(2.0)
    table3.columns[4].width = Inches(2.0)

    heads3 = ["Skoleenhet", "Elevtall", "Budsjett YTD", "Regnskap YTD", "Avvik YTD (Merforbruk)"]
    for c_i, h in enumerate(heads3):
        cell = table3.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.LEFT if c_i == 0 else PP_ALIGN.RIGHT

    schools_data = [
        ("Grim Skole (Enhet 2020)", "480", "4 150 000 kr", "4 720 000 kr", "+570 000 kr"),
        ("Lovisenlev Skole", "390", "3 400 000 kr", "3 710 000 kr", "+310 000 kr"),
        ("Tangvall Skole", "310", "2 650 000 kr", "2 890 000 kr", "+240 000 kr"),
        ("Vågsbygd Skole", "340", "2 250 000 kr", "2 550 000 kr", "+300 000 kr"),
    ]
    for r_i, (s_name, e_count, b_val, r_val, v_val) in enumerate(schools_data, 1):
        vals = [s_name, e_count, b_val, r_val, v_val]
        for c_i, v in enumerate(vals):
            cell = table3.cell(r_i, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_LIGHT_CARD if r_i % 2 == 0 else COLOR_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = v
            p.font.size = Pt(10.5)
            p.alignment = PP_ALIGN.LEFT if c_i == 0 else PP_ALIGN.RIGHT
            if c_i == 4:
                p.font.bold = True
                p.font.color.rgb = COLOR_RED
    add_footer(slide3, audit_hash, 3)

    # SLIDE 4: Rotårsak på KOSTRA-kontoer
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(
        slide4,
        "Årsaksanalyse: Innkjøp av vikarer (Art 1020) står for 61 % av sektorens merforbruk",
        "Nedbrytning av avviket i Visma ERP viser at faste lønninger følger budsjettplanen"
    )
    acc_cards = [
        ("Art 1010 Faste Lønninger", "+40 000 kr", "Stabil grunnbemanning. Følger planlagt lønnsoppgjør.", COLOR_NAVY),
        ("Art 1020 Innkjøp Vikarer", "+870 000 kr", "Akutt overforbruk pga. sesongsykefravær. Krever stans.", COLOR_RED),
        ("Art 1090 Overtid / Mertid", "+420 000 kr", "Sensur- og eksamensavvikling. Overtidsstopp innført.", COLOR_RED),
        ("Art 1600 NAV-Refusjoner", "+150 000 kr", "Refusjonsetterslep. Saksbehandlingstid hos NAV.", COLOR_GREEN),
    ]
    for i, (at, av, ad, ac) in enumerate(acc_cards):
        row = i // 2
        col = i % 2
        c_left = Inches(0.8 + col * 6.0)
        c_top = Inches(1.8 + row * 2.3)
        box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, c_top, Inches(5.7), Inches(2.1))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_LIGHT_CARD
        box.line.color.rgb = RGBColor(0xDB, 0xEA, 0xFE)
        tb = slide4.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.15), Inches(5.3), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = at
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY
        p2 = tf.add_paragraph()
        p2.text = f"Avvik YTD: {av}"
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = ac
        p2.space_before = Pt(3)
        p3 = tf.add_paragraph()
        p3.text = ad
        p3.font.size = Pt(10)
        p3.font.color.rgb = COLOR_DARK
        p3.space_before = Pt(4)
    add_footer(slide4, audit_hash, 4)

    # SLIDE 5: Lærernorm & Kapasitetsutnyttelse
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(
        slide5,
        "Lærernorm: Skolene oppfyller lovkravet på 1:15 og 1:20 med betryggende margin",
        "Opplæringsloven § 8-2 stiller krav til maksimal lærertetthet per trinn"
    )
    norm_kpis = [
        ("1.–4. TRINN (NORM 1:15)", "13,8 elever / lærer", "Oppfyller lærernormen (+1,2 margin)", COLOR_GREEN),
        ("5.–7. TRINN (NORM 1:20)", "17,9 elever / lærer", "Oppfyller lærernormen (+2,1 margin)", COLOR_GREEN),
        ("8.–10. TRINN (NORM 1:20)", "18,4 elever / lærer", "Oppfyller lærernormen (+1,6 margin)", COLOR_GREEN),
    ]
    for i, (nt, nv, ns, nc) in enumerate(norm_kpis):
        c_left = Inches(0.8 + i * 4.0)
        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.8), Inches(3.7), Inches(2.4))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_CARD
        card.line.color.rgb = RGBColor(0xE5, 0xE7, 0xEB)
        tb = slide5.shapes.add_textbox(c_left + Inches(0.2), Inches(1.95), Inches(3.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = nt
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED
        p2 = tf.add_paragraph()
        p2.text = nv
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = nc
        p2.space_before = Pt(8)
        p3 = tf.add_paragraph()
        p3.text = ns
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = COLOR_DARK
        p3.space_before = Pt(6)

    cb5 = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.5), Inches(11.7), Inches(2.1))
    cb5.fill.solid()
    cb5.fill.fore_color.rgb = COLOR_BG_GRAY
    cb5.line.color.rgb = RGBColor(0xDB, 0xEA, 0xFE)
    tf_cb5 = cb5.text_frame
    tf_cb5.word_wrap = True
    p = tf_cb5.paragraphs[0]
    p.text = "Controllerens vurdering av bemanning:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p2 = tf_cb5.add_paragraph()
    p2.text = "• Merforbruket skyldes ikke underfinansiering av lovpålagt lærernorm, men overdreven bruk av eksterne vikarer ved korttidsfravær."
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_DARK
    p2.space_before = Pt(4)
    p3 = tf_cb5.add_paragraph()
    p3.text = "• Innføring av felles vikarring gjør det mulig å opprettholde lovlig lærertetthet uten å leie inn kommersielle byråvikarer."
    p3.font.size = Pt(11)
    p3.font.color.rgb = COLOR_DARK
    add_footer(slide5, audit_hash, 5)

    # SLIDE 6: Tiltakskalender
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(
        slide6,
        "Tiltakskalender: 3 operative grep kutter 170 000 kr per måned fra 1. september",
        "Tidsplan og milepæler for rektorene i Vågsbygd, Grim, Tangvall og Lovisenlev"
    )
    plan_steps = [
        ("Fase 1: 0–30 dager (1. sept – 30. sept)", "Vikarstopp for fravær < 3 dager. Etablering av felles vikarring mellom naboskoler. Ukentlig rapportering.", COLOR_NAVY),
        ("Fase 2: 30–60 dager (1. okt – 31. okt)", "Akselerert innsending av refusjonskrav til NAV. Avstemming av konto 1600. Overtidsstopp.", COLOR_GREEN),
        ("Fase 3: 60–90 dager (1. nov – 31. des)", "Evaluering av helårsbalanse før 3. tertialrapport. Justering av rammetildeling for budsjett 2027.", COLOR_NAVY),
    ]
    for i, (pt, pd, pc) in enumerate(plan_steps):
        box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8 + i * 1.5), Inches(11.7), Inches(1.3))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_LIGHT_CARD
        box.line.color.rgb = pc
        box.line.width = Pt(1.5)
        tb = slide6.shapes.add_textbox(Inches(1.0), Inches(1.85 + i * 1.5), Inches(11.3), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = pt
        p1.font.size = Pt(13.5)
        p1.font.bold = True
        p1.font.color.rgb = pc
        p2 = tf.add_paragraph()
        p2.text = pd
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_DARK
        p2.space_before = Pt(3)
    add_footer(slide6, audit_hash, 6)

    # SLIDE 7: Rektors Styringskontrakt
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(
        slide7,
        "Oppsummering: Samtlige rektorer forplikter seg til balansert helårsdrift",
        "Styringskontrakt mellom Kommunalsjef Oppvekst og enhetslederne for 2. halvår 2026"
    )
    vb7 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.5))
    vb7.fill.solid()
    vb7.fill.fore_color.rgb = COLOR_BG_GRAY
    vb7.line.color.rgb = COLOR_NAVY
    vb7.line.width = Pt(2)
    tf_vb7 = vb7.text_frame
    tf_vb7.word_wrap = True

    p = tf_vb7.paragraphs[0]
    p.text = "Styringsforpliktelser for skoleledelsen:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    mandates = [
        "1. Hver rektor er personlig ansvarlig for at årsrammen ikke overskrides ved utgangen av 2026 jf. fullmaktsmatrisen.",
        "2. Ekstern innleie av vikarer skal godkjennes skriftlig av kommunalsjefen dersom fraværet overstiger 5 virkedager.",
        "3. Etablert vikarring mellom Grim og Vågsbygd skal prioriteres foran eksterne leverandører.",
        "4. Oppdatert regnskapsprognose rapporteres i Visma EPM innen den 5. i hver måned."
    ]
    for m in mandates:
        pm = tf_vb7.add_paragraph()
        pm.text = m
        pm.font.size = Pt(11.5)
        pm.font.color.rgb = COLOR_DARK
        pm.space_before = Pt(10)

    p_sig = tf_vb7.add_paragraph()
    p_sig.text = "Kristiansand, " + now_str + "  •  Kristin E. Bakke, Kommunalsjef  /  Frank Ellingsen, Senior Controller"
    p_sig.font.size = Pt(10)
    p_sig.font.italic = True
    p_sig.font.color.rgb = COLOR_MUTED
    p_sig.space_before = Pt(14)
    add_footer(slide7, audit_hash, 7)

    prs.save(str(target))
    return str(target)


# ==============================================================================
# DEKK 4: PROSJEKTKONTROLL & CAPEX EVM (NIVÅ 4: KONTROLLUTVALGET & CAPEX)
# ==============================================================================
def generate_capex_evm_deck(output_path: Optional[str] = None) -> str:
    """
    Bygger et 7-slides dekk for Prosjektkontroll & Investeringstilsyn (Capex):
    ISO 21508 Earned Value Management (EVM), S-kurver og usikkerhetsstyring.
    """
    if output_path is None:
        target = Path(__file__).resolve().parents[4] / "powerpoint" / "Presentasjon_Prosjektkontroll_Capex_EVM_2026.pptx"
    else:
        target = Path(output_path)

    target.parent.mkdir(parents=True, exist_ok=True)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    now_str = datetime.date.today().strftime("%d.%m.%Y")
    audit_hash = hashlib.sha256(f"{datetime.datetime.now().isoformat()}:CAPEX_EVM_DECK_2026".encode()).hexdigest()

    # SLIDE 1: Tittel
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.color.rgb = COLOR_NAVY

    tb1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(3.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "KRISTIANSAND KOMMUNE  •  KONTROLLUTVALGET & BYUTVIKLING"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)

    p2 = tf1.add_paragraph()
    p2.text = "Prosjektkontroll & Capex Status: Investeringsportefølje & EVM 2026"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(12)

    p3 = tf1.add_paragraph()
    p3.text = "Investeringstilsyn jf. ISO 21508 EVM, KS2-Kvalitetssikring & Kommuneloven § 14-4"
    p3.font.size = Pt(15)
    p3.font.color.rgb = RGBColor(0xE0, 0xE7, 0xFF)
    p3.space_before = Pt(8)

    p4 = tf1.add_paragraph()
    p4.text = f"Dato: {now_str}  •  Frank Ellingsen, Project Controller & BI-Spesialist"
    p4.font.size = Pt(11.5)
    p4.font.color.rgb = RGBColor(0xBF, 0xDB, 0xFE)
    p4.space_before = Pt(28)
    p5 = tf1.add_paragraph()
    p5.text = f"Audit Stempel: {audit_hash[:24]}...  |  Portefølje-EVM Avstemt per 31.08.2026"
    p5.font.size = Pt(9.5)
    p5.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
    p5.space_before = Pt(4)

    # SLIDE 2: Porteføljeoversikt EVM
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(
        slide2,
        "Porteføljestatus: Portefølje-CPI på 0,893 indikerer sluttoverskridelse på 80,4 Mkr",
        "Earned Value Management (ISO 21508) for 517 Mkr portefølje: Vågsbygd Skole, Randesund og VA"
    )
    evm_kpis = [
        ("KOSTNADSINDEKS (CPI)", "0,893", "Påløpt (AC): 292,9M  vs.  Opptjent (EV): 262,9M", COLOR_RED),
        ("FREMDRIFTSINDEKS (SPI)", "0,935", "Planlagt (PV): 281,2M  vs.  Opptjent (EV): 262,9M", COLOR_NAVY),
        ("SLUTTPROGNOSE (EAC)", "597,4 Mkr", "Sluttoverskridelse (VAC): -80,4 Mkr mot BAC 517M", COLOR_RED),
    ]
    for i, (et, ev, es, ec) in enumerate(evm_kpis):
        c_left = Inches(0.8 + i * 4.0)
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.8), Inches(3.7), Inches(2.5))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_CARD
        card.line.color.rgb = RGBColor(0xE5, 0xE7, 0xEB)
        tb = slide2.shapes.add_textbox(c_left + Inches(0.2), Inches(2.0), Inches(3.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = et
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED
        p2 = tf.add_paragraph()
        p2.text = ev
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = ec
        p2.space_before = Pt(8)
        p3 = tf.add_paragraph()
        p3.text = es
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = COLOR_DARK
        p3.space_before = Pt(6)

    ib2 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.7), Inches(1.9))
    ib2.fill.solid()
    ib2.fill.fore_color.rgb = COLOR_BG_GRAY
    ib2.line.color.rgb = RGBColor(0xDB, 0xEA, 0xFE)
    tf_ib2 = ib2.text_frame
    tf_ib2.word_wrap = True
    p = tf_ib2.paragraphs[0]
    p.text = "Sentrale funn fra investeringstilsynet:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p2 = tf_ib2.add_paragraph()
    p2.text = "• Randesund Boenhet (PROJ-201) har et kritisk kostnadsavvik med CPI på 0,843 som følge av krevende grunnforhold og stålprisvekst."
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_DARK
    p2.space_before = Pt(4)
    p3 = tf_ib2.add_paragraph()
    p3.text = "• VA Hovedledning (PROJ-301) leverer foran plan med CPI 1,027 og genererer kr 2,3M i forventet mindreforbruk."
    p3.font.size = Pt(11)
    p3.font.color.rgb = COLOR_DARK
    add_footer(slide2, audit_hash, 2)

    # SLIDE 3: ISO 21508 Tabell
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(
        slide3,
        "Prosjektoversikt: Randesund Boenhet og Vågsbygd Skole driver kostnadsavviket",
        "EVM statusavstemming per 31.08.2026 i henhold til ISO 21508 standarden"
    )
    t_shape3 = slide3.shapes.add_table(5, 6, Inches(0.8), Inches(1.8), Inches(11.7), Inches(3.6))
    table3 = t_shape3.table
    table3.columns[0].width = Inches(3.2)
    table3.columns[1].width = Inches(1.8)
    table3.columns[2].width = Inches(1.7)
    table3.columns[3].width = Inches(1.7)
    table3.columns[4].width = Inches(1.5)
    table3.columns[5].width = Inches(1.8)

    heads3 = ["Prosjekt / Investering", "Vedtatt Ramme (BAC)", "Påløpt (AC)", "Opptjent (EV)", "CPI Indeks", "Sluttprognose (EAC)"]
    for c_i, h in enumerate(heads3):
        cell = table3.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.LEFT if c_i == 0 else PP_ALIGN.RIGHT

    p_rows = [
        ("Vågsbygd Skole (PROJ-101)", "185 000 000 kr", "104 500 000 kr", "95 000 000 kr", "0,909", "208 251 070 kr", COLOR_RED),
        ("Randesund Boenhet (PROJ-201)", "240 000 000 kr", "139 100 000 kr", "117 300 000 kr", "0,843", "299 529 558 kr", COLOR_RED),
        ("VA Hovedledning (PROJ-301)", "92 000 000 kr", "49 300 000 kr", "50 600 000 kr", "1,027", "89 668 168 kr", COLOR_GREEN),
        ("SUM PORTEFØLJE CAPEX", "517 000 000 kr", "292 900 000 kr", "262 900 000 kr", "0,893", "597 448 796 kr", COLOR_RED),
    ]
    for r_i, (p_name, bac_v, ac_v, ev_v, cpi_v, eac_v, col_v) in enumerate(p_rows, 1):
        vals = [p_name, bac_v, ac_v, ev_v, cpi_v, eac_v]
        for c_i, v in enumerate(vals):
            cell = table3.cell(r_i, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_LIGHT_CARD if r_i % 2 == 0 else COLOR_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = v
            p.font.size = Pt(10)
            p.alignment = PP_ALIGN.LEFT if c_i == 0 else PP_ALIGN.RIGHT
            if r_i == 4:
                p.font.bold = True
            if c_i in (4, 5):
                p.font.bold = True
                p.font.color.rgb = col_v
    add_footer(slide3, audit_hash, 3)

    # SLIDE 4: S-Kurve og Earned Value Analyse
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(
        slide4,
        "S-Kurve Analyse: Avviksgapet mellom kostnad (AC) og verdi (EV) eskalerte i Q2",
        "Kumulativ verdiskaping mot påløpte kostnader over prosjektets tidsakse 2025–2027"
    )
    s_cards = [
        ("PLANLAGT VERDI (PV)", "281,2 mill. kr", "Den opprinnelige baseline-fremdriftskurven godkjent i KS2.", COLOR_NAVY),
        ("OPPTJENT VERDI (EV)", "262,9 mill. kr", "Fysisk ferdigstilt arbeid godkjent av byggherrens byggeleder.", COLOR_GREEN),
        ("PÅLØPT KOSTNAD (AC)", "292,9 mill. kr", "Bokførte entreprenørfakturaer og materialkjøp i regnskapet.", COLOR_RED),
        ("KOSTNADSAVVIK (CV)", "-30,0 mill. kr", "Akkumulert overforbruk som krever inndekning via usikkerhetsreserve.", COLOR_RED),
    ]
    for i, (st, sv, sd, sc) in enumerate(s_cards):
        row = i // 2
        col = i % 2
        c_left = Inches(0.8 + col * 6.0)
        c_top = Inches(1.8 + row * 2.3)
        box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, c_top, Inches(5.7), Inches(2.1))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_LIGHT_CARD
        box.line.color.rgb = RGBColor(0xDB, 0xEA, 0xFE)
        tb = slide4.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.15), Inches(5.3), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = st
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY
        p2 = tf.add_paragraph()
        p2.text = sv
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = sc
        p2.space_before = Pt(3)
        p3 = tf.add_paragraph()
        p3.text = sd
        p3.font.size = Pt(10)
        p3.font.color.rgb = COLOR_DARK
        p3.space_before = Pt(4)
    add_footer(slide4, audit_hash, 4)

    # SLIDE 5: P85 Usikkerhetsanalyse & Reserveforbruk
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(
        slide5,
        "Usikkerhetsstyring: Sluttoverskridelsen dekkes delvis av P85-usikkerhetsreserven",
        "Kvalitativ og kvantitativ risikovurdering for prosjektporteføljen jf. KS2-krav"
    )
    p85_kpis = [
        ("BASISESTIMAT (P50)", "465,0 Mkr", "Prosjektleders forventede produksjonskostnad", COLOR_NAVY),
        ("USIKKERHETSAVSETNING (P85)", "52,0 Mkr", "Vedtatt buffer for uforutsette grunnforhold", COLOR_GREEN),
        ("GJENSTÅENDE RESERVE", "22,0 Mkr", "Kr 30,0M allerede bundet opp i endringsordrer", COLOR_RED),
    ]
    for i, (pt, pv, ps, pc) in enumerate(p85_kpis):
        c_left = Inches(0.8 + i * 4.0)
        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.8), Inches(3.7), Inches(2.4))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_CARD
        card.line.color.rgb = RGBColor(0xE5, 0xE7, 0xEB)
        tb = slide5.shapes.add_textbox(c_left + Inches(0.2), Inches(1.95), Inches(3.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = pt
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED
        p2 = tf.add_paragraph()
        p2.text = pv
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = pc
        p2.space_before = Pt(8)
        p3 = tf.add_paragraph()
        p3.text = ps
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = COLOR_DARK
        p3.space_before = Pt(6)

    rb5 = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.5), Inches(11.7), Inches(2.1))
    rb5.fill.solid()
    rb5.fill.fore_color.rgb = COLOR_BG_GRAY
    rb5.line.color.rgb = RGBColor(0xDB, 0xEA, 0xFE)
    tf_rb5 = rb5.text_frame
    tf_rb5.word_wrap = True
    p = tf_rb5.paragraphs[0]
    p.text = "Risiko- og tiltaksvurdering for Kontrollutvalget:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p2 = tf_rb5.add_paragraph()
    p2.text = "• Det gjenstår kun 22 Mkr av P85-avsetningen. Dersom CPI på Randesund Boenhet ikke forbedres, vil kostnadsrammen sprekke med 28 Mkr."
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_DARK
    p2.space_before = Pt(4)
    p3 = tf_rb5.add_paragraph()
    p3.text = "• Anbefaling: Etablere frys på opsjonsbestillinger og reforhandle kontraktspakker med totalentreprenør for trinn 2."
    p3.font.size = Pt(11)
    p3.font.color.rgb = COLOR_DARK
    add_footer(slide5, audit_hash, 5)

    # SLIDE 6: EAC Scenariomatrise
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(
        slide6,
        "Sluttprognoser (EAC): Tre scenarioer for resterende produksjonskostnad (ETC)",
        "Fremskrivning av sluttkostnad basert på historisk ytelse og korrigerende tiltak"
    )
    eac_scenarios = [
        ("Scenario 1: Uendret Ytelse (CPI = 0,893)", "EAC 597,4 Mkr (Overskridelse 80,4 Mkr)", "Fortsetter dagens avvikstakt uten inngripen. Krever tilleggsbevilgning i Bystyret.", COLOR_RED),
        ("Scenario 2: Normalisert Ytelse (CPI = 1,0 på ETC)", "EAC 547,0 Mkr (Overskridelse 30,0 Mkr)", "Resterende arbeid leveres på budsjett. Overskridelsen dekkes i sin helhet av P85-reserven.", COLOR_GREEN),
        ("Scenario 3: Kritisk Eskalering (CPI = 0,80)", "EAC 634,5 Mkr (Overskridelse 117,5 Mkr)", "Stresstest med ytterligere geotekniske forsinkelser og entreprenørtvister.", COLOR_RED)
    ]
    for i, (et, ev, ed, ec) in enumerate(eac_scenarios):
        box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8 + i * 1.5), Inches(11.7), Inches(1.3))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_LIGHT_CARD
        box.line.color.rgb = ec
        box.line.width = Pt(1.5)
        tb = slide6.shapes.add_textbox(Inches(1.0), Inches(1.85 + i * 1.5), Inches(11.3), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f"{et}  ───  {ev}"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = ec
        p2 = tf.add_paragraph()
        p2.text = ed
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_DARK
        p2.space_before = Pt(3)
    add_footer(slide6, audit_hash, 6)

    # SLIDE 7: Controllerens Anbefalinger
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(
        slide7,
        "Oppsummering & Controllerens Anbefalinger til Kontrollutvalget",
        "Operative tiltak for Capex-styring og gjenetablering av kostnadskontroll jf. ISO 21508"
    )
    vb7 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.5))
    vb7.fill.solid()
    vb7.fill.fore_color.rgb = COLOR_BG_GRAY
    vb7.line.color.rgb = COLOR_NAVY
    vb7.line.width = Pt(2)
    tf_vb7 = vb7.text_frame
    tf_vb7.word_wrap = True

    p = tf_vb7.paragraphs[0]
    p.text = "Project Controllerens 4 tiltaksanbefalinger:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    recs = [
        "1. Innføre ukentlig Change Control Board (CCB) for å stanse uautoriserte endringsordrer på Randesund Boenhet.",
        "2. Fryse alle ikke-kritiske opsjoner på Vågsbygd Skole inntil CPI er gjenetablert over 0,950.",
        "3. Frigjøre kr 22 000 000 fra P85-usikkerhetsavsetningen til inndekning av verifiserte grunnarbeidskostnader.",
        "4. Gjennomføre en uavhengig KS2-etterkontroll før oppstart av byggetrinn 2 for å sikre overholdelse av kostnadsrammen."
    ]
    for r in recs:
        pr = tf_vb7.add_paragraph()
        pr.text = r
        pr.font.size = Pt(11.5)
        pr.font.color.rgb = COLOR_DARK
        pr.space_before = Pt(10)

    p_sig = tf_vb7.add_paragraph()
    p_sig.text = "Kristiansand, " + now_str + "  •  Frank Ellingsen, Project Controller & BI-Spesialist (Attestert Stage-Gate Port 9)"
    p_sig.font.size = Pt(10)
    p_sig.font.italic = True
    p_sig.font.color.rgb = COLOR_MUTED
    p_sig.space_before = Pt(14)
    add_footer(slide7, audit_hash, 7)

    prs.save(str(target))
    return str(target)


# ==============================================================================
# DEKK 5: OPERATIV AVVIKSRAPPORT (NIVÅ 5: ENHETSLEDER MAL-AVVIK-EFFEKT-001)
# ==============================================================================
def generate_enhet202_deck(output_path: Optional[str] = None) -> str:
    """
    Bygger et 7-slides dekk for Enhetsleder (Enhet 202 Grunnskole):
    4-punkts operativ avviksrapport (MAL-AVVIK-EFFEKT-001) for månedlig økonomidialog.
    """
    if output_path is None:
        target = Path(__file__).resolve().parents[4] / "powerpoint" / "Presentasjon_Enhet202_Operativ_Avviksrapport_2026.pptx"
    else:
        target = Path(output_path)

    target.parent.mkdir(parents=True, exist_ok=True)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    now_str = datetime.date.today().strftime("%d.%m.%Y")
    audit_hash = hashlib.sha256(f"{datetime.datetime.now().isoformat()}:ENHET202_DECK_2026".encode()).hexdigest()

    # SLIDE 1: Tittel
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.color.rgb = COLOR_NAVY

    tb1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(3.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "KRISTIANSAND KOMMUNE  •  ENHET 202 GRUNNSKOLE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)

    p2 = tf1.add_paragraph()
    p2.text = "Operativ Avviksrapport & Handlingsplan: Enhet 202"
    p2.font.size = Pt(30)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(12)

    p3 = tf1.add_paragraph()
    p3.text = "Månedlig Avviksoppfølging  |  Standardmønster MAL-AVVIK-EFFEKT-001  |  Stage-Gate Port 9"
    p3.font.size = Pt(15)
    p3.font.color.rgb = RGBColor(0xE0, 0xE7, 0xFF)
    p3.space_before = Pt(8)

    p4 = tf1.add_paragraph()
    p4.text = f"Dato: {now_str}  •  Rektor, Enhet 202 Grunnskole  /  Frank Ellingsen, Senior Controller"
    p4.font.size = Pt(11.5)
    p4.font.color.rgb = RGBColor(0xBF, 0xDB, 0xFE)
    p4.space_before = Pt(28)
    p5 = tf1.add_paragraph()
    p5.text = f"Audit Stempel: {audit_hash[:24]}...  |  Statusrapport Økonomidialog"
    p5.font.size = Pt(9.5)
    p5.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
    p5.space_before = Pt(4)

    # SLIDE 2: Punkt 1 - Avvik Hittil i År
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(
        slide2,
        "Punkt 1: Enhet 202 har et akkumulert merforbruk på 1 420 000 kr (+11,4 %)",
        "Avvik hittil i år per 31.08.2026 målt mot periodisert budsjettramme i Visma Enterprise"
    )
    kpis = [
        ("VEDTATT ÅRSRAMME", "18 500 000 kr", "Samlet bevilgning til Enhet 202 Grunnskole", COLOR_NAVY),
        ("MERFORBRUK HITTIL I ÅR", "+1 420 000 kr", "+11,4 % over periodisert budsjett (Rød alarm)", COLOR_RED),
        ("HELÅRSPROGNOSE UTEN TILTAK", "+2 130 000 kr", "Worst case-eskalering ved uendret drift", COLOR_RED),
    ]
    for i, (kt, kv, ks, kc) in enumerate(kpis):
        c_left = Inches(0.8 + i * 4.0)
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.8), Inches(3.7), Inches(2.5))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_CARD
        card.line.color.rgb = RGBColor(0xE5, 0xE7, 0xEB)
        tb = slide2.shapes.add_textbox(c_left + Inches(0.2), Inches(2.0), Inches(3.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = kt
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED
        p2 = tf.add_paragraph()
        p2.text = kv
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = kc
        p2.space_before = Pt(8)
        p3 = tf.add_paragraph()
        p3.text = ks
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = COLOR_DARK
        p3.space_before = Pt(6)

    ib2 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.7), Inches(1.9))
    ib2.fill.solid()
    ib2.fill.fore_color.rgb = COLOR_BG_GRAY
    ib2.line.color.rgb = RGBColor(0xDB, 0xEA, 0xFE)
    tf_ib2 = ib2.text_frame
    tf_ib2.word_wrap = True
    p = tf_ib2.paragraphs[0]
    p.text = "Rektors situasjonsbilde:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p2 = tf_ib2.add_paragraph()
    p2.text = "• Avviket skyldes en ekstraordinær fraværsbølge blant lærere og fagarbeidere i 1. halvår, kombinert med høy vikarbruk."
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_DARK
    p2.space_before = Pt(4)
    p3 = tf_ib2.add_paragraph()
    p3.text = "• Det er nødvendig med umiddelbare korrigerende tiltak for å overholde kommunedirektørens krav om balanse innen årets slutt."
    p3.font.size = Pt(11)
    p3.font.color.rgb = COLOR_DARK
    add_footer(slide2, audit_hash, 2)

    # SLIDE 3: Punkt 2 - Rotårsak på Kontoart
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(
        slide3,
        "Punkt 2: Årsaken er 12,8 % sykefravær og høyt innkjøp av vikarer (Art 1020)",
        "Detaljert regnskapsanalyse fordelt på kontoarter i henhold til KOSTRA-standarden"
    )
    t_shape3 = slide3.shapes.add_table(5, 5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(3.6))
    table3 = t_shape3.table
    table3.columns[0].width = Inches(3.7)
    table3.columns[1].width = Inches(2.0)
    table3.columns[2].width = Inches(2.0)
    table3.columns[3].width = Inches(2.0)
    table3.columns[4].width = Inches(2.0)

    heads3 = ["Kontoart / Beskrivelse", "Budsjett YTD", "Regnskap YTD", "Avvik Kr", "Driver / Forklaring"]
    for c_i, h in enumerate(heads3):
        cell = table3.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.LEFT if c_i == 0 else PP_ALIGN.RIGHT

    r_accs = [
        ("Art 1020 Vikarer (Timelærere)", "1 200 000 kr", "2 070 000 kr", "+870 000 kr", "12,8 % korttidsfravær ped. personale"),
        ("Art 1090 Overtid / Mertid", "80 000 kr", "500 000 kr", "+420 000 kr", "Sensur- og eksamensgjennomføring"),
        ("Art 1600 NAV-Refusjoner", "-590 000 kr", "-440 000 kr", "+150 000 kr", "Refusjonsetterslep hos NAV"),
        ("Øvrige driftsutgifter (1100–1400)", "650 000 kr", "630 000 kr", "-20 000 kr", "Mindreforbruk læremidler"),
    ]
    for r_i, (a_name, b_val, r_val, v_val, v_desc) in enumerate(r_accs, 1):
        vals = [a_name, b_val, r_val, v_val, v_desc]
        for c_i, v in enumerate(vals):
            cell = table3.cell(r_i, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_LIGHT_CARD if r_i % 2 == 0 else COLOR_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = v
            p.font.size = Pt(10)
            p.alignment = PP_ALIGN.LEFT if c_i in (0, 4) else PP_ALIGN.RIGHT
            if c_i == 3:
                p.font.bold = True
                p.font.color.rgb = COLOR_RED if "+" in v else COLOR_GREEN
    add_footer(slide3, audit_hash, 3)

    # SLIDE 4: Punkt 3 - Kvantifisert Handlingsplan
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(
        slide4,
        "Punkt 3: Handlingsplan med 3 tiltak gir 830 000 kr i samlet innsparing i 2026",
        "0–30 dagers strakstiltak og 30–90 dagers strukturelle grep i regi av rektor"
    )
    plan_cards = [
        ("Tiltak 1: Vikarstopp korttidsfravær", "0–30 dager (Fra 1. sept)", "Ingen vikarinnleie for fravær under 3 dager. Felles vikarring med naboskole.", "680 000 kr innsparing", COLOR_GREEN),
        ("Tiltak 2: Akselerert NAV-innsending", "30–60 dager (Oktober)", "Raskere digital oversendelse av inntektsskjema sikrer utestående refusjoner.", "150 000 kr frigjøres", COLOR_GREEN),
        ("Tiltak 3: Overtidsstopp og godkjenning", "Løpende (Høst 2026)", "All mertid krever skriftlig forhåndsgodkjenning av rektor. Ingen uplanlagt overtid.", "Stram kostnadskontroll", COLOR_NAVY),
    ]
    for i, (pt, ps, pd, pe, pc) in enumerate(plan_cards):
        box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8 + i * 1.5), Inches(11.7), Inches(1.3))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_LIGHT_CARD
        box.line.color.rgb = pc
        box.line.width = Pt(1.5)
        tb = slide4.shapes.add_textbox(Inches(1.0), Inches(1.85 + i * 1.5), Inches(11.3), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f"{pt}   ───   {pe}"
        p1.font.size = Pt(13.5)
        p1.font.bold = True
        p1.font.color.rgb = pc
        p2 = tf.add_paragraph()
        p2.text = f"Tidsramme: {ps}  •  {pd}"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_DARK
        p2.space_before = Pt(3)
    add_footer(slide4, audit_hash, 4)

    # SLIDE 5: Punkt 4 - Helårsprognose (EOY)
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(
        slide5,
        "Punkt 4: Helårsavvik reduseres fra 2,13 mill. kr til 590 000 kr ved full effekt",
        "Sluttprognose per 31.12.2026 og anbefalt inndekning via omstillingsfondet jf. § 14-5"
    )
    eoy_cards = [
        ("UTEN TILTAK (WORST CASE)", "+2 130 000 kr", "Eskalering truer skolens driftsbalanse", COLOR_RED),
        ("KVANTIFISERT TILTAKSEFFEKT", "-830 000 kr", "Vikarstopp (680k) + NAV refusjoner (150k)", COLOR_GREEN),
        ("FORVENTET SLUTTAVVIK EOY", "+590 000 kr", "Søkes dekket via omstillingsfond (§ 14-5)", COLOR_NAVY),
    ]
    for i, (et, ev, es, ec) in enumerate(eoy_cards):
        c_left = Inches(0.8 + i * 4.0)
        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.8), Inches(3.7), Inches(2.4))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_CARD
        card.line.color.rgb = RGBColor(0xE5, 0xE7, 0xEB)
        tb = slide5.shapes.add_textbox(c_left + Inches(0.2), Inches(1.95), Inches(3.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = et
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED
        p2 = tf.add_paragraph()
        p2.text = ev
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = ec
        p2.space_before = Pt(8)
        p3 = tf.add_paragraph()
        p3.text = es
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = COLOR_DARK
        p3.space_before = Pt(6)

    eb5 = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.5), Inches(11.7), Inches(2.1))
    eb5.fill.solid()
    eb5.fill.fore_color.rgb = COLOR_BG_GRAY
    eb5.line.color.rgb = RGBColor(0xDB, 0xEA, 0xFE)
    tf_eb5 = eb5.text_frame
    tf_eb5.word_wrap = True
    p = tf_eb5.paragraphs[0]
    p.text = "Inndekning og politisk forankring:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p2 = tf_eb5.add_paragraph()
    p2.text = "• Det gjenstående avviket på 590 000 kr kan ikke kuttes ytterligere uten å true lovpålagt undervisningstilbud."
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_DARK
    p2.space_before = Pt(4)
    p3 = tf_eb5.add_paragraph()
    p3.text = "• Foreslås innarbeidet i 2. tertialrapport som sak til Bystyret med inndekning over Oppvekstsektorens omstillingsfond jf. § 14-5."
    p3.font.size = Pt(11)
    p3.font.color.rgb = COLOR_DARK
    add_footer(slide5, audit_hash, 5)

    # SLIDE 6: Månedlig Vikarkurve & Fraværstrend
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(
        slide6,
        "Månedlig Vikarkurve: Vikarkostnadene reduseres fra 210 000 kr til 40 000 kr/mnd",
        "Faktisk utvikling januar–august og prognosert bane september–desember etter vikarstopp"
    )
    t_shape6 = slide6.shapes.add_table(5, 5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(3.6))
    table6 = t_shape6.table
    table6.columns[0].width = Inches(2.5)
    table6.columns[1].width = Inches(2.3)
    table6.columns[2].width = Inches(2.3)
    table6.columns[3].width = Inches(2.3)
    table6.columns[4].width = Inches(2.3)

    heads6 = ["Periode / Kvartal", "Fraværsprosent", "Vikartimer / Mnd", "Månedlig Kostnad", "Status / Tiltak"]
    for c_i, h in enumerate(heads6):
        cell = table6.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.LEFT if c_i == 0 else PP_ALIGN.RIGHT

    curve_rows = [
        ("Q1 (Jan–Mar)", "14,2 % (Vinterbølge)", "620 timer / mnd", "210 000 kr", "Uplanlagt innleie"),
        ("Q2 (Apr–Jun)", "11,8 % (Vårsemester)", "480 timer / mnd", "175 000 kr", "Eksamensavvikling"),
        ("Q3 (Jul–Sep)", "8,4 % (Skolestart)", "220 timer / mnd", "85 000 kr", "Vikarstopp trer i kraft"),
        ("Q4 (Okt–Des)", "6,5 % (Målsetting)", "110 timer / mnd", "40 000 kr", "Felles vikarring i drift"),
    ]
    for r_i, (p_name, f_pct, v_hrs, m_cost, s_note) in enumerate(curve_rows, 1):
        vals = [p_name, f_pct, v_hrs, m_cost, s_note]
        for c_i, v in enumerate(vals):
            cell = table6.cell(r_i, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_LIGHT_CARD if r_i % 2 == 0 else COLOR_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = v
            p.font.size = Pt(10.5)
            p.alignment = PP_ALIGN.LEFT if c_i in (0, 4) else PP_ALIGN.RIGHT
            if c_i == 3:
                p.font.bold = True
                p.font.color.rgb = COLOR_GREEN if r_i >= 3 else COLOR_RED
    add_footer(slide6, audit_hash, 6)

    # SLIDE 7: Stage-Gate Port 9 Sign-off
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(
        slide7,
        "Stage-Gate Port 9: Attestert Avviksavtale for Enhet 202 Grunnskole",
        "Formell godkjenning av handlingsplan og oppfølgingsmandat jf. MAL-AVVIK-EFFEKT-001"
    )
    vb7 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.5))
    vb7.fill.solid()
    vb7.fill.fore_color.rgb = COLOR_BG_GRAY
    vb7.line.color.rgb = COLOR_NAVY
    vb7.line.width = Pt(2)
    tf_vb7 = vb7.text_frame
    tf_vb7.word_wrap = True

    p = tf_vb7.paragraphs[0]
    p.text = "Attestasjon og forpliktelser (Stage-Gate Port 9):"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    sign_mandates = [
        "1. Rektor bekrefter iverksetting av vikarstopp for korttidsfravær (< 3 dager) fra 1. september 2026.",
        "2. Skolen tilknyttes den etablerte vikarringen med naboskoler for å dekke uunngåelig fravær.",
        "3. Økonomiavdelingen oversender samlet refusjonskrav på kr 150 000 til NAV for umiddelbar oppgjør.",
        "4. Sluttoppfølging og effektmåling gjennomføres i månedlig dialogmøte 5. oktober 2026."
    ]
    for sm in sign_mandates:
        pm = tf_vb7.add_paragraph()
        pm.text = sm
        pm.font.size = Pt(11.5)
        pm.font.color.rgb = COLOR_DARK
        pm.space_before = Pt(10)

    p_sig = tf_vb7.add_paragraph()
    p_sig.text = "Kristiansand, " + now_str + "  •  Rektor, Enhet 202  /  Frank Ellingsen, Senior Controller (Stage-Gate Port 9 Attestert)"
    p_sig.font.size = Pt(10)
    p_sig.font.italic = True
    p_sig.font.color.rgb = COLOR_MUTED
    p_sig.space_before = Pt(14)
    add_footer(slide7, audit_hash, 7)

    prs.save(str(target))
    return str(target)


if __name__ == "__main__":
    out1 = generate_bystyret_deck()
    out2 = generate_konsern_deck()
    out3 = generate_oppvekst_deck()
    out4 = generate_capex_evm_deck()
    out5 = generate_enhet202_deck()
    print("Alle 5 PowerPoint-presentasjoner generert med suksess!")
