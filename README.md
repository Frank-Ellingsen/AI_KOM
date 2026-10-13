# 🏛️ Kommune AI Guardrails — Kristiansand Kommune

**Lokal, skjermet og etterrettelig AI & RAG-regelverksassistent for Økonomi og Virksomhetsstyring**

---

## 📌 Om Prosjektet

**Kommune AI Guardrails** er en produksjonsklar, 100 % lokal og personvernsikker RAG-assistent (Retrieval-Augmented Generation) utviklet for **Økonomi og Virksomhetsstyring i Kristiansand kommune**. 

Systemet fungerer som en intelligent beslutningsstøtte for økonomirådgivere, controllere og enhetsledere ved oppslag i komplekst kommunalt regelverk, inkludert **Kommuneloven**, **KOSTRA-forskriften**, **Selvkostforskriften**, **Finansforskriften**, det lokale **Økonomireglementet**, samt **tertialrapporter** og **budsjettvedtak**.

---

## 🛡️ Kjernefunksjoner & Governance

- **🔒 Hybrid Modellarkitektur (Gemini & Ollama):** Fleksibel inferens med **Google Gemini 3.8 Flash** som lynrask primærmodell (0 % lokal CPU-last), og **Ollama** (`llama3.1` / `qwen2.5`) for 100 % frakoblet lokal drift. All data PII-vaskes lokalt før sending.
- **🛡️ Automatisk PII-Skjerming (Port 4):** Innebygd deteksjon og vasking av fødselsnumre, navn, e-postadresser og kontonumre før spørrerunder kjøres.
- **🔍 Glass-Box RAG & Kildeidentifisering:** Hvert AI-svar krever eksplisitt §-sitering og kildekobling til KOSTRA-veiledere, kommunelov og tertialrapporter.
- **✍️ Human-in-the-Loop (HITL) Sign-Off:** Saksbehandler beholder full kontroll. AI fatter 0 autonome vedtak; saksbehandler må godkjenne (*APPROVED*), endre (*MODIFIED*) eller avvise (*REJECTED*) forslag.
- **🔒 SHA-256 Audit Trail (Port 9):** Uforanderlig kryptografisk stempling av alle spørringer, kilde-chunks og saksbehandlingsnotater i SQLite for **Kommunerevisjonen** og Kontrollutvalget.
- **🌐 Offentlig Algoritmeregister (Port 10):** Eksport i tråd med *Eurocities Algorithmic Transparency Standard*.

---

## 🏗️ Systemarkitektur

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                             USER INTERFACE (Streamlit)                          │
│          Control Office Hub (Årshjul, KPI-kort, RAG-søk, HITL Sign-off)         │
└──────────────────────────────────────┬──────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          KOMMUNE AI GUARDRAILS ENGINE                           │
│  ┌───────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐  │
│  │  PII Masker / Vasker  │  │  Hybrid Search (RRF) │  │ Glass-Box Prompting  │  │
│  └───────────────────────┘  └──────────────────────┘  └──────────────────────┘  │
└────────────────═══┬───────────────────────────────────────────┬─────────────────┘
                    │                                           │
                    ▼                                           ▼
┌──────────────────────────────────────┐    ┌─────────────────────────────────────┐
│  SQLITE GOLDEN RECORD & RAG DB       │    │  LOCAL OLLAMA INFERENCE SERVER      │
│  • Fact_Regnskap & Fact_Budsjett     │    │  • llama3.1 / qwen2.5               │
│  • Dim_Funksjon, Dim_Art, Dim_Ansvar │    │  • SentenceTransformer Embedding    │
│  • sqlite-vec (384D) & FTS5          │    │    (multilingual-e5-small)          │
│  • Audit_AI_Actions (SHA-256 Hash)   │    └─────────────────────────────────────┘
└──────────────────────────────────────┘
```

---

## 🚀 Hurtigstart & Installasjon

### Forutsatte Krav
- **OS:** Windows 11 / Windows Server / Linux
- **Python:** 3.11+
- **Ollama:** Installert lokalt med `llama3.1` eller `qwen2.5`
- **Docker & Docker Compose** *(valgfritt, for kontainerdrift)*

---

### Måte 1: Lokal Kjøring via PowerShell / Bash

1. **Klon repositoriet og opprett virtuelt miljø:**
   ```powershell
   cd kommune-ai-guardrails
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Installer avhengigheter:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Konfigurer AI-modell (Hybrid Gemini / Ollama):**
   - **Anbefalt (0 % CPU, lynrask):** Sett miljøvariabel for Google Gemini:
     ```powershell
     $env:GEMINI_API_KEY="din-nøkkel-her"
     ```
   - **Alternativt (100 % lokal/air-gapped):** Start lokal Ollama:
     ```powershell
     ollama serve
     ```

4. **Start Web UI (Streamlit):**
   ```powershell
   streamlit run app/app.py
   ```
   *Nettleseren åpnes automatisk på `http://localhost:8501`.*

---

### Måte 2: Kontainerdrift via Docker Compose (Anbefalt for IT/Drift)

```bash
# Bygg og start alle mikrotjenester (App + Ollama) i bakgrunnen
docker compose up -d --build

# Sjekk status på kontainerne
docker compose ps
```

---

## 📂 Prosjektstruktur

```text
kommune-ai-guardrails/
├── app/
│   └── app.py                      # Streamlit Control Office Hub Web UI (Tufte-style)
├── config/
│   └── config.yaml                 # Systemkonfigurasjon (vektorer, modeller, stier)
├── data/
│   ├── raw/                        # Innleste PDF-er, CSV-er fra Visma/Framsikt
│   └── processed/                  # Bearbeidede vektorer og SQLite db
├── docs/                           # Fullstendig rammeverksdokumentasjon
│   ├── README.md                   # Prosjektoversikt
│   ├── STAGE_GATE_FRAMEWORK.md     # 10-stegs kommunal styringsmodell
│   ├── RAG_ARCHITECTURE_SPEC.md    # Hybrid saks- og regelsøksspesifikasjon
│   ├── SQLITE_DATA_ARCHITECTURE_SPEC.md # Star Schema datamodell
│   ├── SKILLS_AND_TOOLS_CATALOG.md # Agent & Tool Skills katalog
│   ├── KOMMUNEREVISJONEN_AUDIT_CHECKLIST.md # Revisjons- og kontrollutvalgssjekkliste
│   ├── OFFICE_DASHBOARD_HUB_SPEC.md # Control Office Hub UI spesifikasjon
│   ├── OPPSTARTSVEILEDER_STARTKNAPP.md # Startknapp og intranettlaunching
│   ├── DOCKER_AND_MLOPS_DEPLOYMENT.md # Docker & MLOps eval-guide
│   └── USER_GUIDE_SOP.md           # Operativ brukerveiledning
├── src/
│   └── kommune_ai_guardrails/
│       ├── database/               # SQLite, FTS5 & sqlite-vec drivere
│       ├── guardrails/             # PII-maskering og SHA-256 audit-logging
│       ├── ingestion/              # ETL pipeline fra Visma/Framsikt til Star Schema
│       └── rag/                    # Hybrid BM25/Vector RRF-søkemotor
├── tests/
│   └── test_rag_eval.py            # Automated RAG Golden Evaluation Suite
├── Dockerfile                      # App-kontainer spesifikasjon
├── docker-compose.yml              # Multi-container orkestrering
└── start_app.bat                   # Enkel Windows-startknapp
```

---

## 🧩 Agent & Tool Skills Katalog

Systemet benytter 11 faglige **Agent Skills** og 5 tekniske **Tool Skills**:
1. `SKILL_RAG_LEGAL_QUERY`: Kildekritisk oppslag i lover, forskrifter og økonomireglement.
2. `SKILL_KOSTRA_ANALYZER`: Kontoplanvalidering, selvkost og korrigert brutto driftsresultat.
3. `SKILL_EPM_VARIANCE_DETECT`: Deteksjon av vesentlige avvik mellom Visma og Framsikt.
4. `SKILL_PII_AND_GUARDRAILS`: Automatisk PII-vasking og SHA-256 Audit Trail.
5. `SKILL_EXCEL_MCP_INTEGRATION`: Power Query M-kode og DAX-automatisering.
6. `SKILL_POWERBI_FABRIC_ANALYTICS`: Star Schema, DAX-matriser (`ISINSCOPE`) og RLS.
7. `SKILL_EXCEL_PYTHON_FPNA`: FAST Financial Modelling Standard og Monte Carlo i Excel.
8. `SKILL_SAKSFREMLEGG_GENERATOR`: Politiske saksfremlegg og tertialrapportutkast.
9. `SKILL_AUDIT_GOVERNANCE_REGISTRY`: Algoritmeregister og revisjonsstempling.
10. `SKILL_DATA_INTEGRATION_ETL`: Ingestion til SQLite Star Schema.
11. `SKILL_VISUAL_DATA_COMMUNICATION`: Grafisk persepsjon, Cleveland & McGill og colormaps.

---

## 📄 Lisens & Eierskap

Utviklet for og av **Kristiansand kommune**. Offentlig tilgjengelig under **MIT-lisensen** for gjenbruk i norske kommuner og fylkeskommuner.
