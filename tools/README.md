# 🛠️ Kommune AI Tool Drivers & Execution Engine (`tools/`)

> **Sentral verktøykasse, tekniske lavnivå-drivere og beregningsmotorer for Kristiansand Kommune AI Controller Hub.**  
> Utviklet for **Frank Ellingsen** (Senior Financial Controller & Project Controller).

---

## 🚀 Unified CLI Runner (`run_tool.py`)

Alle verktøy kan kjøres gjennom det sentrale kommandolinjegrensesnittet:

```bash
# Vis hjelp og tilgjengelige kommandoer
python tools/run_tool.py --help

# 1. Kjør prediktiv AI-prognose (Monte Carlo P10/P50/P90 og EVM)
python tools/run_tool.py forecast --mode both

# 2. Kjør internkontroll og revisjonsvalidering jf. Kommuneloven § 14-5
python tools/run_tool.py audit

# 3. Generer offisiell Excel Controller-rapport (FAST Standard)
python tools/run_tool.py excel

# 4. Verifiser helsetilstand for Control Office Hub og database
python tools/run_tool.py verify

# 5. Start lokal Hub API-server (FastAPI)
python tools/run_tool.py server --port 8000

# 6. Parse dokument (PDF / Word / Excel) til strukturert tekst
python tools/run_tool.py parse <sti-til-fil>
```

---

## 📋 Verktøyoversikt & Skriptkatalog

| Verktøyskript | Kjernefunksjon | Teknologi / Bibliotek | Lovhjemmel / Standard |
| :--- | :--- | :--- | :--- |
| **[`run_tool.py`](./run_tool.py)** | Sentral CLI-inngangsport | Python `argparse`, `subprocess` | Standardisert CLI |
| **[`predictive_forecasting_engine.py`](./predictive_forecasting_engine.py)** | Monte Carlo P10/P50/P90 og EVM (CPI/EAC/VAC) | NumPy, SciPy, SQLite, SHA-256 | Kommuneloven § 14-5, KS2 |
| **[`audit_revisjon_validator.py`](./audit_revisjon_validator.py)** | Etterlevelsessjekk av budsjettbalanse og bruttoprinsipp | SQLite, hashlib, regex | Kommuneloven § 14-5 & § 14-6 |
| **[`generate_controller_excel_report.py`](./generate_controller_excel_report.py)** | Generering av offisielle økonomirapporter | OpenPyXL, FAST financial modeling | FAST Standard, Tufte |
| **[`document_parser.py`](./document_parser.py)** | Parsing av PDF, Word (.docx) og Excel (.xlsx) | pypdf, python-docx, openpyxl | UTF-8 / cp1252 auto-detect |
| **[`hub_api_server.py`](./hub_api_server.py)** | Lokal FastAPI REST API backend for huben | FastAPI, Uvicorn, SQLite | Local-first REST |
| **[`verify_office_hub.py`](./verify_office_hub.py)** | Helsetest og validering av database og UI | SQLite, requests, assertions | Internkontroll |
| **[`update_index_hub.py`](./update_index_hub.py)** | Vedlikeholds- og byggeskript for `index.html` | Python HTML/DOM manipulation | Tufte Data-Ink |

---

## 🗂️ Tekniske Driver-spesifikasjoner (Lag 2)

Hver spesifikasjon dokumenterer protokoll og arkitektur for AI-agentene:

* **[`TOOL_SKILL_DOCUMENT_PARSER.md`](./TOOL_SKILL_DOCUMENT_PARSER.md)**: Ekstraksjon av PDF (§-chunking), Word (.docx) og Excel (.xlsx).
* **[`TOOL_SKILL_LLM_GATEWAY.md`](./TOOL_SKILL_LLM_GATEWAY.md)**: Modellruting mellom Gemini Flash MCP og lokal Ollama.
* **[`TOOL_SKILL_OLLAMA_API_BRIDGE.md`](./TOOL_SKILL_OLLAMA_API_BRIDGE.md)**: Lokal Ollama inferens (`llama3.2`, `mistral`) med JSON-schema.
* **[`TOOL_SKILL_DUCKDB_ANALYTICS.md`](./TOOL_SKILL_DUCKDB_ANALYTICS.md)**: In-memory OLAP-analyser over SQLite Star Schema og Parquet-eksport.
* **[`TOOL_SKILL_SQLITE_VEC_EXECUTOR.md`](./TOOL_SKILL_SQLITE_VEC_EXECUTOR.md)**: Vektorsøk og semantisk KNN i `kommune_golden_record.db`.
* **[`TOOL_SKILL_PYTHON_SANDBOX_RUNNER.md`](./TOOL_SKILL_PYTHON_SANDBOX_RUNNER.md)**: Isolert kjøring av analyseskripter med feilhåndtering.
* **[`TOOL_SKILL_STREAMLIT_UI_BUILDER.md`](./TOOL_SKILL_STREAMLIT_UI_BUILDER.md)**: Interne controller-dashboards og visualiseringer.

---

## 🛡️ Tufte & Sikkerhetsprinsipper
1. **Lokal Data-Lagring**: All regnskapsinformasjon behandles utelukkende lokalt i `erp_data/kommune_golden_record.db`.
2. **Uforanderlig Logg**: Beregninger og revisjonsrapporter forsegles med kryptografisk SHA-256 kontrollsum.
3. **Avviksfokus**: Terminalutskrifter og rapporter fremhever kun avvik uten visuell støy.
