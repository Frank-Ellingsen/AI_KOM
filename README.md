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

4. **Start Web UI (Streamlit eller Control Office Hub V2):**
   - **Alternativ A — Control Office Hub V2 (Anbefalt, Tufte-standard, lynrask):**
     Dobbeltklikk `start_kommune_ai.bat` eller åpne `index.html` direkte i nettleseren (`file:///.../index.html`). Hub API-serveren starter automatisk på `http://127.0.0.1:8766`.
   - **Alternativ B — Streamlit Guardrails App:**
     ```powershell
     streamlit run app/app.py
     ```
     *Nettleseren åpnes automatisk på `http://localhost:8501`.*

5. **Kjør Master Test Suite:**
   ```powershell
   pytest tests/test_project_master.py -v
   ```
   *Kjører 6/6 kjernevalideringer (Office Hub V2, revisjonssjekk, EVM, MVP-pilot, MCP-server og Hub API).*

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
├── index.html                     # Control Office Hub V2 (Zero-Click Triage, WCAG 2.1 AA, Tufte-standard)
├── tests/                         # Master Test Suite (Validerer alle 6 kjernedimensjoner)
│   └── test_project_master.py     # 100 % dekning for Hub V2, revisjon, EVM, MVP, MCP og API
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
├── templates/                     # Offisielle maler, saksfremlegg og rapporter (.docx og .md)
│   ├── RAPPORTMAL_KOMMUNESTYRET.docx/.md (Nivå 1: Bystyret)
│   ├── RAPPORTMAL_KOMMUNEDIREKTOR.docx/.md (Nivå 2: Kommunedirektøren)
│   ├── RAPPORTMAL_KOMMUNALSJEF.docx/.md (Nivå 3: Sektor Oppvekst)
│   ├── RAPPORTMAL_SEKSJONSLEDER.docx/.md (Nivå 4: Stab Anskaffelser)
│   ├── RAPPORTMAL_AVDELINGSLEDER.docx/.md (Nivå 5: Enhet 202 Skole)
│   ├── RAPPORTMONSTER_AVVIK_OG_EFFEKTPROGNOSE.docx/.md (Standardisert 4-punkts mønster)
│   ├── MAL_POLITISK_SAKSFREMLEGG_BUDSJETTENDRING.docx/.md (Kommuneloven § 14-5 & § 14-6)
│   ├── MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx/.md (Tiltaksplan T1–T6)
│   ├── MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.docx/.md (Partssamarbeid)
│   ├── MAL_STAGE_GATE_PORT_9_HITL_SIGNOFF.docx/.md (Menneskelig overprøving)
│   ├── MAL_FRIA_OG_DPIA_RISIKOVURDERING.docx/.md (EU AI Act & GDPR)
│   └── MAL_PERIODELUKKING_OG_AVSTEMMING.docx/.md (Kontrollinstruks)
├── docs/                          # Arkitektur, forvaltningsdokumentasjon og kildedokumenter
│   ├── VISUAL_STORYTELLING_FT_GUIDE.md (Financial Times Visual Vocabulary & Cleveland-McGill)
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
│   ├── MANEDLIG_AVVIKSRAPPORT_RAMMEVERK.md (Rammeverk for 5 ledelsesnivåer, terskler og rutiner)
│   ├── BRUKERGUIDE.md, OPPSTARTSVEILEDER_STARTKNAPP.md, STYRINGSKALENDER_OG_ARSHJUL_2026.md
│   ├── rag_forklaring.md, stage_gate_rammeverk.md
│   └── README.md                  # Guide-indeks
├── spesifikasjoner/               # Arkitektur, prediktive modeller og MLOps-rigg
│   ├── OFFICE_DASHBOARD_HUB_V2_WORKFLOW_UI.md (V2 UI, Zero-Click Triage & 4-punkts flyt)
│   ├── OFFICE_HUB_GEMINI_MCP_CHAT_SPEC.md (Gemini Flash API & MCP Client integrasjon)
│   ├── PREDICTIVE_AI_FORECASTING_SPEC.md, SKILL_PREDICTIVE_FORECASTING_AI.md
│   ├── OFFICE_DASHBOARD_HUB_SPEC.md, DOCKER_AND_MLOPS_DEPLOYMENT.md
│   └── README.md                  # Spesifikasjonsindeks
├── mvp-pilot/                     # Operativ pilot for Bo og Miljø (Streamlit, DuckDB, SQLite)
│   ├── app_ui.py, etl.py, eac_forecasting.py, hitl_governance.py, run_pilot.py
│   └── README.md
├── ai-implementeringspakke-okonomi/  # 9-delt Håndbok & Rammeverk for kommunal AI (KS, Digdir, EU AI Act)
│   ├── 00_INNHOLD_OG_OVERSIKT.md, 01_MODUL_1_KONSEPT_OG_BESLUTNINGSGRUNNLAG.md
│   ├── 02_MODUL_2_AI_READINESS_OG_MATURITY_FRAMEWORK.md, 03_MODUL_3_GOVERNANCE_ETIKK_OG_GDPR.md
│   ├── 04_MODUL_4_ENTERPRISE_MAALARKITEKTUR_OG_RAG.md, 05_MODUL_5_USE_CASE_PRIORITERING_OG_PILOTMETODIKK.md
│   ├── 06_MODUL_6_SKALERING_GEVINST_OG_ROADMAP_KRISTIANSAND.md, 07_JURIDISK_SJEKKLISTE_FRIA_DPIA.md
│   └── 08_GEVINSTMODELL_OG_FINANSIELL_HANDBOK.md
├── mlops-implementeringspakke/        # 6-delt MLOps & LLMOps drift- og styringspakke
│   ├── 01_MLOps_Oversikt_og_Prinsipper.md, 02_MLOps_Arkitektur_og_Komponenter.md
│   ├── 03_MLOps_Observability_og_Drift.md, 04_MLOps_Governance_og_Sikkerhet.md
│   └── 05_MLOps_Test_og_Kvalitetssikring.md, 06_MLOps_Anbud_og_Innkjøpsmal.md
├── kommune-ai-guardrails/         # Kjerne RAG-motor, PII-vasker, Control Office Hub & sqlite-vec
├── tools/                         # Hjelpeverktøy, mal-generatorer og valideringsskripter
├── start_kommune_ai.bat           # Hovedoppstartskript for Control Office Hub
├── oppdater_vektor_db.bat         # Reindeksering av RAG-vektordatabase
└── README.md                      # Hovedprosjektoversikt
```

---

## 🎯 Håndbok & Rammeverk: AI-implementering for Økonomi og Virksomhetsstyring

Prosjektet inkluderer et komplett, operasjonelt rammeverk for implementering av AI i kommunal sektor, forankret i føringer fra **Digitaliseringsdirektoratet (Digdir)**, **KS**, **EU AI Act** og **Kristiansand kommunes Økonomiplan 2027–2030**:

| Modul | Fil | Tittel & Målgruppe | Nøkkeltema |
| :--- | :--- | :--- | :--- |
| **00** | [`00_INNHOLD_OG_OVERSIKT.md`](file:///c:/Users/frank/Desktop/AI_KOM/ai-implementeringspakke-okonomi/00_INNHOLD_OG_OVERSIKT.md) | **Masteroversikt & Struktur**<br>*(Kommunedirektør & Ledergruppe)* | Overordnet dokumentkompleks og tverrgående prinsipper. |
| **01** | [`01_MODUL_1_KONSEPT_OG_BESLUTNINGSGRUNNLAG.md`](file:///c:/Users/frank/Desktop/AI_KOM/ai-implementeringspakke-okonomi/01_MODUL_1_KONSEPT_OG_BESLUTNINGSGRUNNLAG.md) | **Konseptuelt & Beslutningsgrunnlag**<br>*(Politikere & Toppledelse)* | Demografisk klemme, RPA vs. RAG vs. Agentic AI, verdipotensial. |
| **02** | [`02_MODUL_2_AI_READINESS_OG_MATURITY_FRAMEWORK.md`](file:///c:/Users/frank/Desktop/AI_KOM/ai-implementeringspakke-okonomi/02_MODUL_2_AI_READINESS_OG_MATURITY_FRAMEWORK.md) | **Readiness & Modenhetsrammeverk**<br>*(Økonomidirektør & IT-sjef)* | L1 (Umoden) til L5 (Transformert) over 9 kjerneområder. |
| **03** | [`03_MODUL_3_GOVERNANCE_ETIKK_OG_GDPR.md`](file:///c:/Users/frank/Desktop/AI_KOM/ai-implementeringspakke-okonomi/03_MODUL_3_GOVERNANCE_ETIKK_OG_GDPR.md) | **Governance, Etikk, GDPR & EU AI Act**<br>*(Personvernombud & Jurister)* | Kommunen som *deployer*, FRIA, DPIA, forbud mot leverandørtrening. |
| **04** | [`04_MODUL_4_ENTERPRISE_MAALARKITEKTUR_OG_RAG.md`](file:///c:/Users/frank/Desktop/AI_KOM/ai-implementeringspakke-okonomi/04_MODUL_4_ENTERPRISE_MAALARKITEKTUR_OG_RAG.md) | **Enterprise AI Målarkitektur & RAG**<br>*(Virksomhetsarkitekter & IT)* | AI Gateway, PII-maskering, hybrid søk (RRF) og modelluavhengighet. |
| **05** | [`05_MODUL_5_USE_CASE_PRIORITERING_OG_PILOTMETODIKK.md`](file:///c:/Users/frank/Desktop/AI_KOM/ai-implementeringspakke-okonomi/05_MODUL_5_USE_CASE_PRIORITERING_OG_PILOTMETODIKK.md) | **Use-Case-Prioritering & Pilotmetodikk**<br>*(Prosjekteiere & Faglige rådgivere)* | Netto prioriteringsformel, Bølge 1–3, 4-trinns pilot og Gate G1–G4. |
| **06** | [`06_MODUL_6_SKALERING_GEVINST_OG_ROADMAP_KRISTIANSAND.md`](file:///c:/Users/frank/Desktop/AI_KOM/ai-implementeringspakke-okonomi/06_MODUL_6_SKALERING_GEVINST_OG_ROADMAP_KRISTIANSAND.md) | **Skalering, Gevinst & Roadmap 2025–2030**<br>*(Formannskap & Controller)* | Kristiansand-case: Kapasitetsreallokering, konsulentkutt og FinOps. |
| **07** | [`07_JURIDISK_SJEKKLISTE_FRIA_DPIA.md`](file:///c:/Users/frank/Desktop/AI_KOM/ai-implementeringspakke-okonomi/07_JURIDISK_SJEKKLISTE_FRIA_DPIA.md) | **Operasjonell Juridisk Sjekkliste**<br>*(Saksbehandlere & Jurister)* | 5-trinns skriveklar sjekkliste for screening, hjemmel og godkjenning. |
| **08** | [`08_GEVINSTMODELL_OG_FINANSIELL_HANDBOK.md`](file:///c:/Users/frank/Desktop/AI_KOM/ai-implementeringspakke-okonomi/08_GEVINSTMODELL_OG_FINANSIELL_HANDBOK.md) | **Finansiell Håndbok & Gevinstmodell**<br>*(Controllere & Økonomirådgivere)* | Manual for `gevinstmodell-ai-okonomi.xlsx`, 3-års ROI og payback. |

---

## ⚙️ MLOps & LLMOps: Operasjonell Plattform, Drift & Anskaffelse

For å sikre trygg, skalerbar og regelverkskonform drift i tråd med **EU AI Act art. 26**, **GDPR art. 22**, **Forvaltningsloven § 25** og **ISO 42001 (AIMS)**, inkluderer prosjektet en skriveklar 6-delt MLOps-pakke:

| Modul | Fil | Tittel & Målgruppe | Nøkkeltema |
| :--- | :--- | :--- | :--- |
| **01** | [`01_MLOps_Oversikt_og_Prinsipper.md`](file:///c:/Users/frank/Desktop/AI_KOM/mlops-implementeringspakke/01_MLOps_Oversikt_og_Prinsipper.md) | **MLOps & LLMOps Oversikt & Prinsipper**<br>*(Kommunedirektør & IT-sjef)* | DevOps vs MLOps vs LLMOps, 5 kjørneprinsipper, livsløp for kommunale AI-modeller. |
| **02** | [`02_MLOps_Arkitektur_og_Komponenter.md`](file:///c:/Users/frank/Desktop/AI_KOM/mlops-implementeringspakke/02_MLOps_Arkitektur_og_Komponenter.md) | **Teknisk MLOps-Arkitektur & Komponenter**<br>*(Løsningsarkitekter & MLOps Engineers)* | Enterprise Control Plane, AI Gateway, PII-vask, DVC, Model Registry (MLflow) og CI/CD. |
| **03** | [`03_MLOps_Observability_og_Drift.md`](file:///c:/Users/frank/Desktop/AI_KOM/mlops-implementeringspakke/03_MLOps_Observability_og_Drift.md) | **Observability, Drift-Håndtering & FinOps**<br>*(Driftsansvarlige & Controllere)* | Overvåking av data-, concept- og prompt-drift, token caching og avdelingsvise budsjettak. |
| **04** | [`04_MLOps_Governance_og_Sikkerhet.md`](file:///c:/Users/frank/Desktop/AI_KOM/mlops-implementeringspakke/04_MLOps_Governance_og_Sikkerhet.md) | **MLOps Governance, EU AI Act & Sikkerhet**<br>*(CISO, Personvernombud & Jurister)* | Deployer-krav, 4-delt operativ rollestruktur, lovpålagt audit logg (art. 26) og Kill-Switch. |
| **05** | [`05_MLOps_Test_og_Kvalitetssikring.md`](file:///c:/Users/frank/Desktop/AI_KOM/mlops-implementeringspakke/05_MLOps_Test_og_Kvalitetssikring.md) | **Testing, Ground Truth & Kvalitetssikring**<br>*(Kvalitetsledere & Fagøkonomer)* | Test-pyramide for AI, Ground Truth fasitsett, Faithfulness og Gate G3 akseptkriterier. |
| **06** | [`06_MLOps_Anbud_og_Innkjøpsmal.md`](file:///c:/Users/frank/Desktop/AI_KOM/mlops-implementeringspakke/06_MLOps_Anbud_og_Innkjøpsmal.md) | **Kravspesifikasjon & Anbudsmal**<br>*(Innkjøpere & Fagledere)* | K-01 til K-10 A/B-kravmatrise, datasuverenitet og forbud mot leverandørtrening på data. |

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
