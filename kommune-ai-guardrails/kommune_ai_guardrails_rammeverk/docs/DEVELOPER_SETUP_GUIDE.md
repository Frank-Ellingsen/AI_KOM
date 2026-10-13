# 💻 Utvikler- og Oppsettsveileder (Developer Setup Guide)

> **Teknisk veileder for oppsett, lokal kjøring, databasemigrering og testing av Kommune AI Guardrails.**

---

## 🛠️ Systemkrav og Infrastruktur

* **Operativsystem:** Windows 10/11, macOS eller Linux (Ubuntu 22.04+)
* **RAM:** Minimum 16 GB RAM (32 GB anbefales for 8B/14B LLM-er)
* **Lagring:** Minimum 10 GB ledig SSD-plass
* **Programvare:**
  * Python 3.10, 3.11 eller 3.12
  * Ollama Desktop / CLI
  * Git

---

## 🚀 Oppsett i PowerShell (Windows)

### 1. Klon prosjekt og opprett virtuelt miljø
```powershell
# Naviger til ønsket mappe
cd C:\Users\bruker\Desktop\AI_PROJECTS

# Opprett prosjektmappe
mkdir kommune-ai-guardrails
cd kommune-ai-guardrails

# Opprett virtuelt Python-miljø
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Installer avhengigheter
Opprett filen `requirements.txt` med følgende innhold:
```text
sentence-transformers>=2.2.2
sqlite-vec>=0.1.1
ollama>=0.1.6
streamlit>=1.30.0
pyyaml>=6.0
pypdf>=3.17.0
pandas>=2.0.0
pytest>=7.4.0
```

Kjør installasjonen:
```powershell
pip install -r requirements.txt
```

### 3. Last ned lokal Ollama LLM
Kjør i en ny PowerShell-fane:
```powershell
# Last ned Llama 3.1 8B
ollama pull llama3.1

# (Valgfritt) Last ned Qwen 2.5 7B
ollama pull qwen2.5
```

---

## 🧪 Kjøre Ingestion og Test-skripter

### 1. Bygg eller oppdater vektordatabasen
Legg kildedokumenter (.pdf, .csv, .md) i `data/raw/` og kjør:
```powershell
python src/kommune_ai_guardrails/ingest.py
```

### 2. Test RAG-motoren direkte i CLI
```powershell
python src/kommune_ai_guardrails/rag.py
```

### 3. Start Streamlit Web-App
```powershell
# Kan startes med Streamlit CLI eller direkte med ren Python:
streamlit run app/app.py
# eller: python app/app.py
```

---

## 🔍 Feilsøking (Troubleshooting)

| Problem | Årsak | Løsning |
| :--- | :--- | :--- |
| `Error: listen tcp 127.0.0.1:11434: bind` | Ollama kjører allerede som Windows-tjeneste i bakgrunnen. | Alt er i orden! Du trenger ikke kjøre `ollama serve` manuelt. |
| `ModuleNotFoundError: No module named 'kommune_ai_guardrails'` | Python finner ikke `src`-mappen. | Sjekk at `sys.path.insert(0, ...)` peker på `src` i `app/app.py`. |
| `sqlite3.OperationalError: no such module: vec0` | `sqlite-vec` extension er ikke lastet inn. | Sjekk at `sqlite_vec.load(conn)` kalles etter `sqlite3.connect()`. |
