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
AI_KOM/
├── agenter/                       # 12 operative personas for økonomi- og prosjektstyring
│   ├── 01_dataintegrasjon_etl_agent.md ... 12_revisjon_internkontroll_sporbarhet_agent.md
│   └── README.md                  # Samlende agentmatrise og arbeidsflyt
├── reports/                       # Ledelsesrapporter, Tufte IBCS-visualiseringer og modeller
│   ├── chart_netzero_waterfall.png, sektor_faktisk_vs_budsjett_bullet.png, visma_stoy_waterfall_chart.png
│   ├── Kristiansand_EPM_Status_Prognose_Tiltaksrapport.pdf/.pptx, epm_presentasjon_okonomidirektor_v2.pptx
│   └── kristiansand_epm_modell_v4_interactive.xlsx, Kommune_Project_Controller_Reporting_2026.xlsx
├── kristiansand_epm_rammeverk_norsk/ # Komplett norsk EPM & AI rammeverk
│   ├── README_NO.md, dokumentasjon/ (saksfremlegg, AI-rapport, KOSTRA DAX-pakke, RAG-spec)
│   ├── kildekode/ (datalinje/epm_agent_pipeline.py, sikkerhet/pii_scrubber.py, brukergrensesnitt/)
│   └── data/ (kontor_oversikt_og_arshjul.xlsx, kristiansand_golden_record.db)
├── docs/                          # Arkitektur, forvaltningsdokumentasjon og kildedokumenter
│   ├── epm_full_workflow_documentation.md, antigravity_usecase_epm.md, dax_kostra_kpi_package.md
│   ├── framsikt_epm_integrasjon_spesifikasjon.md, visual_storytelling_og_stakeholder_design.md
│   └── references/ (1.-tertialrapport-2026, økonomiplan 2027-2030, økonomireglement, nøkkeltall)
├── powerbi/                       # Power BI Fabric arkitektur, DAX-bibliotek og TMDL
│   ├── 02_DAX_Measures_Library.dax, 04_KOSTRA_DAX_KPI_Package.dax, 01_PowerQuery_M_Code.pq
│   ├── fxOpenAI_RAG.m, 03_PowerBI_Model_Architecture.md, generate_excel_powerbi_model.py
│   └── projects/Skole enhet project.SemanticModel/ (PBIP TMDL definisjoner for _Measures, Fact, Dim)
├── revisjon-og-kontroll/          # Sjekklister, kontrollnotater og politiske saksfremlegg
│   ├── KOMMUNEREVISJONEN_AUDIT_CHECKLIST.md, NOTAT_TIL_KONTROLLUTVALGET_OG_REVISJONEN.md
│   ├── CONTROLLER_CHECKLIST_OG_PERIODELUKKING.md, TERTIALRAPPORT_NOTAT_OG_SAKSFREMLEGG.md
│   └── README.md                  # Revisjonsindeks
├── bruker-guides/                 # Brukerveiledninger, oppstartsguider og årshjul
│   ├── BRUKERGUIDE.md, OPPSTARTSVEILEDER_STARTKNAPP.md, STYRINGSKALENDER_OG_ARSHJUL_2026.md
│   ├── rag_forklaring.md, stage_gate_rammeverk.md
│   └── README.md                  # Guide-indeks
├── spesifikasjoner/               # Arkitektur, prediktive modeller og MLOps-rigg
│   ├── PREDICTIVE_AI_FORECASTING_SPEC.md, SKILL_PREDICTIVE_FORECASTING_AI.md
│   ├── OFFICE_DASHBOARD_HUB_SPEC.md, DOCKER_AND_MLOPS_DEPLOYMENT.md
│   └── README.md                  # Spesifikasjonsindeks
├── mvp-pilot/                     # Operativ pilot for Bo og Miljø (Streamlit, DuckDB, SQLite)
│   ├── app_ui.py, etl.py, eac_forecasting.py, hitl_governance.py, run_pilot.py
│   └── README.md
├── kommune-ai-guardrails/         # Kjerne RAG-motor, PII-vasker, Control Office Hub & sqlite-vec
├── tools/                         # Hjelpeverktøy og API-servere
├── start_kommune_ai.bat           # Hovedoppstartskript for Control Office Hub
├── oppdater_vektor_db.bat         # Reindeksering av RAG-vektordatabase
└── README.md                      # Hovedprosjektoversikt
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
