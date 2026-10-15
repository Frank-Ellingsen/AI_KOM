---
name: document-parser
description: >-
  Dokumentparsing for PDF (§-chunking), Word (.docx), Excel (.xlsx) og CSV med automatisk tegnsett-deteksjon.
---

# 🛠️ Tool Skill: Document Parser & Multi-Format Ingestion Driver

> **Teknisk ekstraksjonsverktøy for PDF, Word (.docx), Excel (.xlsx), CSV, Markdown og strukturerte tekstfiler.**

---

## 1. Oversikt og Formål

Sørger for lynhurtig, robust og feilfri tekstuthenting og strukturering fra kommunale saksdokumenter, tertialrapporter, forskrifter og regneark.

---

## 2. Støttede Format-Drivere

| Filformat | Hovedbibliotek | Spesialhåndtering |
| :--- | :--- | :--- |
| **PDF** | `pypdf` / `pdftotext` / `pdfplumber` | Ekstraksjon av tabeller, paragraf-gjenkjenning (§) og overskriftshierarki. |
| **Word (.docx)** | `python-docx` / `pandoc` | Bevaring av overskriftsstiler (Heading 1-3) og tabellstrukturer. |
| **Excel (.xlsx)** | `openpyxl` / `pandas` | Automatisk deteksjon av faner, formler og tallformater. |
| **CSV / Tekst** | `chardet` / `pandas` | Automatisk gjenkjenning av tegnsett (`UTF-8`, `ISO-8859-1`, `Windows-1252`) og skilletegn (semikolon `;` vs. komma `,`). |

---

## 3. Tekst-Chunking Algoritme (Paragraf-bevaring)

```python
import re

def chunk_legal_pdf(text: str, source_filename: str):
    """Deler juridiske tekster per § (Paragraf) for optimal RAG-kontekst."""
    pattern = r'(§\s*\d+[-\w]*\.?\s*[^§]+)'
    chunks = re.findall(pattern, text)
    
    result = []
    for idx, chunk in enumerate(chunks):
        sec_match = re.search(r'§\s*\d+[-\w]*', chunk)
        section_ref = sec_match.group(0) if sec_match else "Generelt"
        
        result.append({
            "source_file": source_filename,
            "section_ref": section_ref,
            "content": chunk.strip()
        })
    return result
```

---

## 4. Kvalitetskontroll
* **Tegnsettvasking:** Automatisk fjerning av null-bytes og ugyldige Unicode-tegn.
* **Kildesporing:** Bevarer filnavn, sidetall og overskrifter i metadata.
