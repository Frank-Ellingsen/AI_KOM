# 🧰 Katalog over AI-Ferdigheter, Verktøy & Guardrails (Skills & Tools)

> **Oversikt over gjenbrukbare AI-moduler, verktøyintegrasjoner, prompt-maler og sikkerhetsmekanismer for kommunale IT- og fagmiljøer.**

---

## 🛠️ Modulære AI-Ferdigheter (Skills)

| Skill / Ferdighet | Beskrivelse & Anvendelse | Inndata | Utdata |
| :--- | :--- | :--- | :--- |
| **`rag-legal-query`** | Utfører hybridsøk i lover, forskrifter og lokalt regelverk. | Brukerspørsmål | Forankret svar med §-referanser og kilde-chunks |
| **`kostra-analyzer`** | Analyserer KOSTRA-nøkkeltall, kontoplaner og tjenesteprofiler. | Kontokoder / Artskoder | Strukturert avviksanalyse mot ASSS-snitt |
| **`epm-variance-detect`** | Identifiserer månedlige og tertialvise budsjettavvik i Framsikt/Visma. | Regnskapsdata | Prioritert liste over avvik over vesentlighetsgrense |
| **`pii-masker`** | Skjermer fødselsnumre, navn, e-post og adresser før LLM-behandling. | Råtekst | Anonymisert tekst med plassholdere (`[PERSON]`, `[FNR]`) |
| **`audit-logger`** | Genererer uforanderlig SHA-256 hash og logger spørring/svar til SQLite. | Query, Chunks, Response | SHA-256 Hash-streng i `Audit_AI_Actions` |

---

## 📊 Verktøy- og Integrasjonsmatrise (Tools Integration)

```text
                                 ┌──► Framsikt EPM (Budsjett & Årshjul)
                                 │
[ AI Guardrails / RAG Engine ] ──┼──► Visma Enterprise / ERP (Regnskap & Lønn)
                                 │
                                 ├──► Power BI & Fabric (Visualisering & DAX)
                                 │
                                 └──► Excel / MCP Server (Rapportering & Modellering)
```

### 1. Framsikt EPM Integrasjon
* **Anvendelse:** Hente rammefordelinger, tertialrapporter og tiltaksbeskrivelser.
* **API/Datagrunnlag:** REST API / CSV-eksport fra Framsikt Plan og Økonomi.

### 2. Visma Enterprise ERP
* **Anvendelse:** Avviksanalyser på arts- og ansvarsposteringer, leverandørkontroll.
* **Sikkerhetsregel:** Kun aggregerte tall overføres; ingen sensitive bilag med PII.

### 3. Power BI & DAX
* **Anvendelse:** Generering av dynamiske DAX-mål (YTD, YoY) og RLS (Row-Level Security) for kommunalsjefer.

### 4. Excel MCP Server / Python in Excel
* **Anvendelse:** Automatisering av finansielle modeller, sjekksumvalidering og FAST-standard formatering.

---

## 🛡️ Guardrails & Sikkerhetsfilter

### Input Guardrail (PII-Filter Example)
```python
import re

def sanitize_pii(text: str) -> str:
    """Fjerner norske fødselsnumre (11 siffer) og telefonnumre."""
    # Fødselsnummer regex
    fnr_pattern = r'\b(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[012])\d{7}\b'
    text = re.sub(fnr_pattern, '[SKJERMET FNR]', text)
    
    # Telefonnummer (8 siffer)
    tlf_pattern = r'\b(\+47|0047)?\s*\d{2}\s*\d{2}\s*\d{2}\s*\d{2}\b'
    text = re.sub(tlf_pattern, '[SKJERMET TLF]', text)
    
    return text
```

### Output Guardrail (Factuality & §-Check)
```python
def validate_output_citation(answer: str, required_keyword: str = "§") -> bool:
    """Verifiserer at AI-svaret inneholder minst én paragraf- eller kildehenvisning."""
    if required_keyword not in answer and "Jfr." not in answer:
        return False
    return True
```
