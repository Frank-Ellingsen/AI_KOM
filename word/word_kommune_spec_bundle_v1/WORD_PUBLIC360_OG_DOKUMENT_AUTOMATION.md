# 🔄 Word Automatisering & Public360 Integration

**Virksomhetsområde:** Økonomi og Virksomhetsstyring, Kristiansand kommune  
**Teknologi:** Python (`python-docx`), Pandoc, Public360 REST API  

---

## 1. Automatisk Generering av Saksdokumenter (Python Pipeline)

```python
# Eksempel på automatisk bygging av Word-saksdokument fra Python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Sett mørkeblå overskrift
heading = doc.add_heading('Saksfremlegg: Endring av Årsbudsjett 2026', level=1)
run = heading.runs[0]
run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A) # #1E3A8A

# Legg til vedtaksparagraf
p = doc.add_paragraph()
p.add_run('Kommunedirektørens forslag til vedtak:
').bold = True
p.add_run('1. Bystyret godkjenner omdisponering av kr 3 200 000 fra sentralt disposisjonsfond til Enhet 202 Grunnskole.
')
p.add_run('2. Endringen innarbeides i 2. tertialrapport 2026 jf. Kommuneloven § 14-5.')

doc.save('/workspace/scratch/Saksfremlegg_Bystyret_2026.docx')
```

---

## 2. Integrasjon mot Public360 Sak/Arkiv

* Unik metadata-tagging av alle genererte DOCX-filer (`Archive_ID`, `Case_Number`, `Access_Code`).
* Automatisk konvertering til **PDF/A-1b** for langtidsarkivering via Pandoc / MS Word Automation Service.
