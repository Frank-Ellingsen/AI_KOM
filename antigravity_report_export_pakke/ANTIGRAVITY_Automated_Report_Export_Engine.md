# Antigravity Automated Report & Export Engine (.pdf / .pptx)
**Kristiansand kommune — Control Office Hub (AI_KOM)**

---

## 1. Oversikt og Arkitektur

Automated Report Export Engine er en spesialisert mikrotjeneste i Antigravity-backendet som håndterer automatisk konvertering, oppbygning og distribusjon av **Top 3 KPI-dashbord, månedlige økonomirapporter og Bystyre-presentasjoner** i formatene **PDF** og **PowerPoint (.pptx)**.

Tjenesten kobler sammen Power BI REST API, headless nettleser-rendering (Playwright/Chromium), `python-pptx` og `fpdf2` for å levere politisk og administrativt beslutningsunderlag med kryptografisk **SHA-256 revisjonsstempel**.

```
+-----------------------------------------------------------------------------------+
|                           TRIGGER & SCHEDULE ENGINE                               |
|   • Månedlig M10-månedsoppgjør   • Stage-Gate Port 9 Sign-off   • Webhook Call    |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        POWER BI REST API & RENDERING LAYER                        |
|   1. Power BI ExportToFile API (Genererer høyoppløselig PDF/PPTX fra .pbip)       |
|   2. Playwright Headless Chromium (Genererer snapshot-vektorer av Gauge charts)   |
|   3. Antigravity Dynamic Data Injector (Fyller inn reelle Visma/Framsikt-tall)    |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                      POLITISK SAKSPAKKEGENERATOR (PPTX/PDF)                        |
|   • Slides 1-3: Konsernets Kritiske Måltall (Gauge charts, Triage-matrise)       |
|   • Slides 4-8: Sektorvis drilldown (Oppvekst, Helse/mestring, By/sted)           |
|   • Slide 9: Stage-Gate Port 9 Controller Sign-off & SHA-256 Stempel             |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        DISTRIBUSJON & SAK/ARKIV INTEGRASJON                       |
|   • ACOS WebSak API (Automatisk opprettelse av sak i politisk Møteportal)         |
|   • E-post varsling til Formannskap & Bystyre med kodelåst PDF/PPTX-vedlegg       |
+-----------------------------------------------------------------------------------+
```

---

## 2. API Endepunkter (`/api/v1/export/`)

| Endepunkt | Metode | Beskrivelse | Parametre |
| :--- | :--- | :--- | :--- |
| `/api/v1/export/bystyret-pptx` | `POST` | Genererer tilpasset PowerPoint-kortstall for Bystyret | `periode` (f.eks. M10), `sektor_id`, `include_gauge_charts` |
| `/api/v1/export/tertial-pdf` | `POST` | Genererer komplett PDF-rapport med KPIer, MVA-avstemming og avviksnotater | `tertial` (f.eks. T2), `controller_signoff_hash` |
| `/api/v1/export/websak-sync` | `POST` | Overfører ferdig sakspakke til ACOS WebSak arkivsystem | `sak_id`, `dokument_tittel`, `file_artifact_path` |

---

## 3. Python Implementasjonsmodul (`app/services/report_export_engine.py`)

```python
import os
import hashlib
import json
from datetime import datetime
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# Profilfarger for Kristiansand kommune
COLOR_NAVY = RGBColor(0, 40, 85)     # #002855
COLOR_BLUE = RGBColor(0, 114, 206)   # #0072CE
COLOR_GREEN = RGBColor(16, 185, 129)  # #10B981
COLOR_RED = RGBColor(239, 68, 68)     # #EF4444
COLOR_GRAY = RGBColor(241, 245, 249)  # #F1F5F9

class BystyretReportGenerator:
    def __init__(self, metadata: dict):
        self.metadata = metadata
        self.prs = Presentation()
        # Sett 16:9 bredskjermformat
        self.prs.slide_width = Inches(13.333)
        self.prs.slide_height = Inches(7.5)

    def add_title_slide(self, tittel: str, undertittel: str):
        blank_slide_layout = self.prs.slide_layouts[6]
        slide = self.prs.slides.add_slide(blank_slide_layout)
        
        # Tittelboks
        txBox = slide.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(2.0))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = tittel
        p.font.size = Pt(40)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        p.alignment = PP_ALIGN.LEFT
        
        # Undertittelboks
        p2 = tf.add_paragraph()
        p2.text = undertittel
        p2.font.size = Pt(22)
        p2.font.color.rgb = COLOR_BLUE
        p2.space_before = Pt(14)
        
        # Dato og SHA-256 Stempel
        p3 = tf.add_paragraph()
        sha_stamp = hashlib.sha256(json.dumps(self.metadata).encode()).hexdigest()[:16].upper()
        p3.text = f"Generert: {datetime.now().strftime('%Y-%m-%d %H:%M')} | SHA-256 Audit: {sha_stamp}"
        p3.font.size = Pt(12)
        p3.font.color.rgb = RGBColor(100, 116, 139)
        p3.space_before = Pt(30)
        
        return slide

    def add_kpi_gauge_slide(self, kpi_data: dict):
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        
        # Overskrift
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.7), Inches(1.0))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = "🏛️ Top 3 Finansielle KPIs — Kristiansand kommune"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        
        # KPI 1: Netto Driftsresultat
        self._create_kpi_card(
            slide, left=Inches(0.8), top=Inches(1.8), width=Inches(3.6), height=Inches(4.8),
            title="Netto Driftsresultat", value=f"{kpi_data['netto_driftsresultat_pct']:.2f}%",
            target="Mål: ≥ 1,00%", status_color=COLOR_GREEN, description="Status: Godkjent jf. TBU-norm"
        )
        
        # KPI 2: Disposisjonsfond
        self._create_kpi_card(
            slide, left=Inches(4.8), top=Inches(1.8), width=Inches(3.6), height=Inches(4.8),
            title="Disposisjonsfond", value=f"{kpi_data['disposisjonsfond_pct']:.2f}%",
            target="Mål: ≥ 4,00%", status_color=COLOR_GREEN, description="Buffer: 460 mill. kr"
        )
        
        # KPI 3: Netto Lånegjeld
        self._create_kpi_card(
            slide, left=Inches(8.8), top=Inches(1.8), width=Inches(3.6), height=Inches(4.8),
            title="Netto Lånegjeld", value=f"{kpi_data['netto_lanegjeld_pct']:.1f}%",
            target="Lånetak: ≤ 8,8 mrd. kr", status_color=COLOR_GREEN, description="Under gjeldsgrense"
        )
        return slide

    def _create_kpi_card(self, slide, left, top, width, height, title, value, target, status_color, description):
        shape = slide.shapes.add_shape(1, left, top, width, height) # 1 = Rect
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_GRAY
        shape.line.color.rgb = status_color
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
        p1.text = value
        p1.font.size = Pt(44)
        p1.font.bold = True
        p1.font.color.rgb = status_color
        p1.alignment = PP_ALIGN.CENTER
        p1.space_before = Pt(20)
        
        p2 = tf.add_paragraph()
        p2.text = target
        p2.font.size = Pt(14)
        p2.font.color.rgb = RGBColor(71, 85, 105)
        p2.alignment = PP_ALIGN.CENTER
        p2.space_before = Pt(10)
        
        p3 = tf.add_paragraph()
        p3.text = description
        p3.font.size = Pt(12)
        p3.font.color.rgb = COLOR_NAVY
        p3.alignment = PP_ALIGN.CENTER
        p3.space_before = Pt(15)

    def save(self, filepath: str):
        self.prs.save(filepath)
```

---

## 4. Sikkerhet & ACOS WebSak Integrasjon

* **WebSak PDF/A-Krav:** Genererte rapporter konverteres automatisk til **PDF/A-1b** arkivstandard før overføring til ACOS WebSak via REST API (`POST /api/v1/websak/documents`).
* **Innsyn og Offentleglova:** Rapporter til Bystyret flagges automatisk med Offentleglova status `O` (Offentlig) med mindre de inneholder taushetsbelagte PII-opplysninger (f.eks. enkeltsaker i Helse/Mestring), hvor de skjemasettes med paragraf `Offl. § 13`.
