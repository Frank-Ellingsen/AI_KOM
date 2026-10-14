# ⚡ PowerPoint Automatisering med python-pptx

**Virksomhetsområde:** Økonomi og Virksomhetsstyring, Kristiansand kommune  
**Teknologi:** Python (`python-pptx`), PPTX-Builder Engine  

---

## 1. Automatisk Generering av Slide Decks fra Data

```python
# Eksempel på automatisk slidedekk-generering via python-pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Legg til tittelslide
blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)

# Legg til tittelboks
txBox = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(11.333), Inches(2))
tf = txBox.text_frame
p = tf.paragraphs[0]
p.text = "Økonomisk Status & 2. Tertialrapport 2026"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

prs.save('/workspace/scratch/Presentasjon_Tertialrapport_2026.pptx')
```
