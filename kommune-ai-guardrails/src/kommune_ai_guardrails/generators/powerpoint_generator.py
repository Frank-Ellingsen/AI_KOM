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


if __name__ == "__main__":
    out = generate_bystyret_deck()
    print(f"PowerPoint-fil opprettet: {out}")
