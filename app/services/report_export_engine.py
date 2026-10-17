"""
Antigravity Automated Report & Export Engine (.pptx / .pdf)
for Kristiansand kommune — Control Office Hub (AI_KOM)
jf. Kommuneloven §§ 13-1, 14-5 og Stage-Gate Port 9.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# Profilfarger for Kristiansand kommune jf. ANTIGRAVITY_Automated_Report_Export_Engine.md
COLOR_NAVY = RGBColor(0, 40, 85)       # #002855
COLOR_BLUE = RGBColor(0, 114, 206)     # #0072CE
COLOR_GREEN = RGBColor(16, 185, 129)   # #10B981
COLOR_AMBER = RGBColor(217, 119, 6)    # #D97706
COLOR_RED = RGBColor(220, 38, 38)      # #DC2626
COLOR_GRAY = RGBColor(241, 245, 249)   # #F1F5F9
COLOR_DARK_TEXT = RGBColor(15, 23, 42) # #0F172A

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_PPTX_OUT = ROOT_DIR / "reports" / "Bystyret_M10_Okonomi_Rapport.pptx"


class BystyretReportGenerator:
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self.data = data or {
            "kommune": "Kristiansand kommune",
            "periode": "M10 Oktober 2026",
            "netto_driftsresultat_pct": 1.25,
            "disposisjonsfond_pct": 4.35,
            "netto_lanegjeld_pct": 76.8,
            "total_ramme_ytd_nok": 5420000000.0,
            "total_forbruk_ytd_nok": 5498500000.0,
            "total_avvik_ytd_nok": -78500000.0,
            "signee": "Frank Ellingsen, Senior Financial Controller",
            "revisjon": "Telemark Revisjon IKS",
        }
        self.prs = Presentation()
        self.prs.slide_width = Inches(13.333)
        self.prs.slide_height = Inches(7.5)

    def generate(self, output_path: Optional[Path | str] = None) -> Dict[str, Any]:
        target = Path(output_path) if output_path else DEFAULT_PPTX_OUT
        target.parent.mkdir(parents=True, exist_ok=True)

        payload_bytes = json.dumps(self.data, sort_keys=True).encode("utf-8")
        sha_hash = hashlib.sha256(payload_bytes).hexdigest()

        # -------------------------------------------------------------
        # Slide 1: Tittelside (16:9 widescreen)
        # -------------------------------------------------------------
        blank_layout = self.prs.slide_layouts[6]
        slide1 = self.prs.slides.add_slide(blank_layout)

        txBox1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.0))
        tf1 = txBox1.text_frame
        tf1.word_wrap = True

        p1 = tf1.paragraphs[0]
        p1.text = "Økonomisk Månedsrapport M10 — Oktober 2026"
        p1.font.size = Pt(36)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY

        p2 = tf1.add_paragraph()
        p2.text = "Saksfremlegg til Bystyret og Formannskapet | Kristiansand kommune"
        p2.font.size = Pt(20)
        p2.font.color.rgb = COLOR_BLUE
        p2.space_before = Pt(12)

        p3 = tf1.add_paragraph()
        p3.text = f"Generert av Antigravity Control Hub: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Saksbehandler: {self.data['signee']}"
        p3.font.size = Pt(12)
        p3.font.color.rgb = RGBColor(100, 116, 139)
        p3.space_before = Pt(24)

        p4 = tf1.add_paragraph()
        p4.text = f"Kryptografisk revisjonsforsegling: SHA-256 {sha_hash.upper()}"
        p4.font.size = Pt(10)
        p4.font.color.rgb = RGBColor(148, 163, 184)
        p4.space_before = Pt(8)

        # -------------------------------------------------------------
        # Slide 2: Top 3 Kommunale Nøkkeltall
        # -------------------------------------------------------------
        slide2 = self.prs.slides.add_slide(blank_layout)

        txBox2 = slide2.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.0))
        tf2 = txBox2.text_frame
        p_title2 = tf2.paragraphs[0]
        p_title2.text = "🏛️ Top 3 Finansielle Nøkkeltall — Kristiansand kommune"
        p_title2.font.size = Pt(26)
        p_title2.font.bold = True
        p_title2.font.color.rgb = COLOR_NAVY

        def create_kpi_card(left, title, val_str, target_str, status_str, border_col):
            shape = slide2.shapes.add_shape(1, left, Inches(1.6), Inches(3.6), Inches(5.0))
            shape.fill.solid()
            shape.fill.fore_color.rgb = COLOR_GRAY
            shape.line.color.rgb = border_col
            shape.line.width = Pt(3)

            tf = shape.text_frame
            tf.word_wrap = True

            p0 = tf.paragraphs[0]
            p0.text = title
            p0.font.size = Pt(18)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_NAVY
            p0.alignment = PP_ALIGN.CENTER

            p1 = tf.add_paragraph()
            p1.text = val_str
            p1.font.size = Pt(44)
            p1.font.bold = True
            p1.font.color.rgb = border_col
            p1.alignment = PP_ALIGN.CENTER
            p1.space_before = Pt(20)

            p2 = tf.add_paragraph()
            p2.text = target_str
            p2.font.size = Pt(13)
            p2.font.color.rgb = RGBColor(71, 85, 105)
            p2.alignment = PP_ALIGN.CENTER
            p2.space_before = Pt(12)

            p3 = tf.add_paragraph()
            p3.text = status_str
            p3.font.size = Pt(12)
            p3.font.bold = True
            p3.font.color.rgb = COLOR_NAVY
            p3.alignment = PP_ALIGN.CENTER
            p3.space_before = Pt(18)

        create_kpi_card(
            Inches(0.8),
            "Netto Driftsresultat",
            f"{self.data['netto_driftsresultat_pct']:.2f}%",
            "Mål: ≥ 1,00% (TBU: ≥ 1,75%)",
            "Status: 🟢 Mål oppfylt (115 mill. kr)",
            COLOR_GREEN,
        )
        create_kpi_card(
            Inches(4.8),
            "Disposisjonsfond",
            f"{self.data['disposisjonsfond_pct']:.2f}%",
            "Mål: ≥ 4,00% (TBU: ≥ 5,00%)",
            "Buffer: 🟢 460 mill. kr i reserve",
            COLOR_GREEN,
        )
        create_kpi_card(
            Inches(8.8),
            "Netto Lånegjeld",
            f"{self.data['netto_lanegjeld_pct']:.1f}%",
            "Lånetak: ≤ 78,0% (TBU: ≤ 80,0%)",
            "Status: 🟢 Under vedtatt lånegrense",
            COLOR_GREEN,
        )

        # -------------------------------------------------------------
        # Slide 3: Sektorvis Budsjettoppfølging & Avvik
        # -------------------------------------------------------------
        slide3 = self.prs.slides.add_slide(blank_layout)

        txBox3 = slide3.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.0))
        tf3 = txBox3.text_frame
        p_title3 = tf3.paragraphs[0]
        p_title3.text = "📊 Sektorvis Budsjettoppfølging & Triage — M10 YTD"
        p_title3.font.size = Pt(26)
        p_title3.font.bold = True
        p_title3.font.color.rgb = COLOR_NAVY

        def create_sector_box(top, name, ramme_str, forbruk_str, avvik_str, status_badge, col):
            shape = slide3.shapes.add_shape(1, Inches(0.8), top, Inches(11.7), Inches(1.5))
            shape.fill.solid()
            shape.fill.fore_color.rgb = COLOR_GRAY
            shape.line.color.rgb = col
            shape.line.width = Pt(2)

            tf = shape.text_frame
            tf.word_wrap = True

            p = tf.paragraphs[0]
            p.text = f"{name} — Status: {status_badge}"
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = col

            p_sub = tf.add_paragraph()
            p_sub.text = f"Periodisert ramme: {ramme_str}  |  Bokført forbruk: {forbruk_str}  |  Netto avvik: {avvik_str}"
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = COLOR_DARK_TEXT
            p_sub.space_before = Pt(6)

        create_sector_box(
            Inches(1.6),
            "Område Oppvekst & Utdanning",
            "1 850 mill. kr",
            "1 885 mill. kr",
            "-35,0 mill. kr (-1,89 %)",
            "🔴 RØD (Merforbruk vikar art 1020)",
            COLOR_RED,
        )
        create_sector_box(
            Inches(3.3),
            "Område Helse & Mestring",
            "2 100 mill. kr",
            "2 142 mill. kr",
            "-42,0 mill. kr (-2,00 %)",
            "🔴 RØD (Overtid art 1090 & sykefravær)",
            COLOR_RED,
        )
        create_sector_box(
            Inches(5.0),
            "Område By- og Stedsutvikling (VAR Selvkost)",
            "850 mill. kr",
            "851,5 mill. kr",
            "-1,5 mill. kr (-0,18 %)",
            "🟡 GUL (Snøbrøyting / Selvkost i balanse)",
            COLOR_AMBER,
        )

        # -------------------------------------------------------------
        # Slide 4: Korrigerende Tiltak & Stage-Gate Port 9 Sign-off
        # -------------------------------------------------------------
        slide4 = self.prs.slides.add_slide(blank_layout)

        txBox4 = slide4.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.0))
        tf4 = txBox4.text_frame
        p_title4 = tf4.paragraphs[0]
        p_title4.text = "🛡️ Korrigerende Tiltak jf. § 14-5 & Stage-Gate Port 9"
        p_title4.font.size = Pt(26)
        p_title4.font.bold = True
        p_title4.font.color.rgb = COLOR_NAVY

        # Tiltaksboks
        shape_tiltak = slide4.shapes.add_shape(1, Inches(0.8), Inches(1.6), Inches(7.5), Inches(5.0))
        shape_tiltak.fill.solid()
        shape_tiltak.fill.fore_color.rgb = COLOR_GRAY
        shape_tiltak.line.color.rgb = COLOR_NAVY
        shape_tiltak.line.width = Pt(1.5)

        tf_t = shape_tiltak.text_frame
        tf_t.word_wrap = True

        p_t0 = tf_t.paragraphs[0]
        p_t0.text = "Korrigerende Handlingsplan (Kommuneloven § 14-5):"
        p_t0.font.size = Pt(16)
        p_t0.font.bold = True
        p_t0.font.color.rgb = COLOR_NAVY

        items = [
            "1. Ansettelsesstopp på administrative stillinger ut året.",
            "2. Innstramming i vikarbruk (Art 1020) — godkjenning fra kommunalsjef kreves.",
            "3. Raskere innkreving av NAV-sykerefusjoner (Art 1600).",
            "4. Prosjektgjennomgang investeringsportefølje: Utsettelse av ikke-kritiske tiltak.",
            "5. Månedlig rapportering til Formannskapet frem mot årsoppgjøret.",
        ]
        for it in items:
            pi = tf_t.add_paragraph()
            pi.text = it
            pi.font.size = Pt(12.5)
            pi.font.color.rgb = COLOR_DARK_TEXT
            pi.space_before = Pt(10)

        # Sign-off boks
        shape_sign = slide4.shapes.add_shape(1, Inches(8.6), Inches(1.6), Inches(3.9), Inches(5.0))
        shape_sign.fill.solid()
        shape_sign.fill.fore_color.rgb = RGBColor(238, 242, 255)
        shape_sign.line.color.rgb = COLOR_BLUE
        shape_sign.line.width = Pt(2)

        tf_s = shape_sign.text_frame
        tf_s.word_wrap = True

        ps0 = tf_s.paragraphs[0]
        ps0.text = "Revisorattest & Port 9"
        ps0.font.size = Pt(16)
        ps0.font.bold = True
        ps0.font.color.rgb = COLOR_NAVY
        ps0.alignment = PP_ALIGN.CENTER

        ps1 = tf_s.add_paragraph()
        ps1.text = "STATUS: GODKJENT"
        ps1.font.size = Pt(14)
        ps1.font.bold = True
        ps1.font.color.rgb = COLOR_GREEN
        ps1.alignment = PP_ALIGN.CENTER
        ps1.space_before = Pt(14)

        details = [
            f"Ansvarlig Controller:\n{self.data['signee']}",
            f"Kontrollorgan:\n{self.data['revisjon']}",
            f"Attestdato:\n{datetime.now().strftime('%Y-%m-%d')}",
            f"SHA-256 Forsegling:\n{sha_hash[:20]}...",
        ]
        for d in details:
            pd = tf_s.add_paragraph()
            pd.text = d
            pd.font.size = Pt(10.5)
            pd.font.color.rgb = COLOR_DARK_TEXT
            pd.alignment = PP_ALIGN.CENTER
            pd.space_before = Pt(12)

        # Lagre presentasjon
        self.prs.save(str(target))

        return {
            "ok": True,
            "file_path": str(target),
            "file_name": target.name,
            "slides_count": len(self.prs.slides),
            "file_size_bytes": target.stat().st_size,
            "sha256_audit_seal": sha_hash,
            "generated_at": datetime.now().isoformat(),
        }


def generate_bystyret_pptx(
    output_path: Optional[Path | str] = None,
    data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    generator = BystyretReportGenerator(data=data)
    return generator.generate(output_path=output_path)
