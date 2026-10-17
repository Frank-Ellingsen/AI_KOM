# 🏛️ Kristiansand Kommune — AI Project Controller Hub & Guardrails

**Lokal, skjermet og etterrettelig AI- og EPM-plattform for Prosjektcontrolling, Budsjettstyring og Kommunal Virksomhetsstyring**

[![Edward Tufte](https://img.shields.io/badge/Visual_Standard-Edward_Tufte_Data--Ink-0f172a)](./.agents/rules/01_tufte_data_ink_rules.md)
[![Kommuneloven](https://img.shields.io/badge/Lovverk-Kommuneloven_%C2%A7%C2%A7_14--5%2F14--6-c0392b)](./revisjon-og-kontroll/KOMMUNEREVISJONEN_AUDIT_CHECKLIST.md)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity_Skills-19_Native-2563eb)](./.agents/skills/)
[![Golden Record](https://img.shields.io/badge/Data_Lake-SQLite_Star_Schema-059669)](./erp_data/)
[![Audit Trail](https://img.shields.io/badge/Audit_Trail-SHA--256_Sealed-d97706)](./tools/audit_revisjon_validator.py)

---

## 📌 Om Prosjektet

**Kristiansand Kommune AI Project Controller Hub** er en produksjonsklar, lokal-først beslutningsstøtte- og automatiseringsplattform utviklet for økonomistyring, prosjektcontrolling og regelverksetterlevelse i **Kristiansand kommune**.

Plattformen understøtter **6 virksomhetsområder**, **81 enheter** og et totalbudsjett på **7,24 milliarder NOK**. Løsningen forener automatisert avviksdeteksjon i Visma ERP mot Framsikt EPM, rullende EAC/ETC-prognoser (Earned Value Management), kontroll av lovkrav (**Kommuneloven §§ 14-5 og 14-6**, **HTA § 4**), og ett-klikks eksport til **PowerPoint** (Bystyret), **Word** (saksfremlegg), **Excel** (FAST-standard) og **Power BI** (.pbip).

---

## 🛡️ Kjernefunksjoner & Arkitekturprinsipper

* **🔒 Hybrid Modellarkitektur (Gemini & Ollama):** Fleksibel inferens med **Google Gemini 3.8 Flash** som primærmodell (0 % lokal CPU-last), og lokal **Ollama** (`llama3.2`, `mistral`, `qwen2.5-coder`) for 100 % frakoblet drift.
* **🛡️ Lokal PII-Skjerming (Stage-Gate Port 4):** Fødselsnumre, navn, kontonumre og kontaktdata maskeres og anonymiseres lokalt før analyse.
* **📊 Edward Tufte Data-Ink Ratio:** Rent grensesnitt uten unødig støy, tabeller uten vertikale linjer, direkte etikettering på kurver, dempede basisfarger og fargekoder kun for aktive avvik:
  * 🔴 **Rød (`#c0392b`)**: Vesentlig merforbruk ($CV < -500\text{k}$ kr eller $CPI < 0.95$).
  * 🟡 **Gul (`#d35400`)**: Observasjon ($0.95 \le CPI < 1.00$).
  * 🟢 **Grønn (`#27ae60`)**: I balanse / mindreforbruk ($CPI \ge 1.00$).
* **⚖️ Lov- & Virksomhetsstyring:**
  * **Kommuneloven § 14-5:** Realistisk budsjettbalanse. Hvis $VAC < 0$ ved årets slutt, genereres saksfremlegg om budsjettjustering til Bystyret.
  * **Kommuneloven § 14-6:** Bruttoprinsippet for inntekter og utgifter.
  * **HTA § 4 & AML § 10-12:** Automatiske drøftingsprotokoller ved bemanningsendringer og overtid.
* **✍️ Stage-Gate Port 9 (HITL Sign-Off):** 0 autonome vedtak; alle AI-tiltak krever saksbehandlers overprøving (*APPROVED*, *MODIFIED*, *REJECTED*).
* **🔒 SHA-256 Audit Trail:** Uforanderlig kryptografisk stempling av analyser, revisjonssjekker og saksnotater for Kommunerevisjonen og Kontrollutvalget.
* **🌐 Algoritmeregister (Port 10):** Transparens og rapportering i samsvar med *Eurocities Algorithmic Transparency Standard*.

---

## 🏗️ Systemarkitektur

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│              BRUKERGRENSESNITT (Control Office Hub V2 / index.html)              │
│       Zero-Click Triage • Framsikt Budsjettmodul • Årshjul • HITL Sign-off      │
└──────────────────────────────────────┬──────────────────────────────────────────┘
                                       │ HTTP / REST (Port 8766)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                   KOMMUNE AI CONTROLLER ENGINE & FASTAPI BACKEND                 │
│  ┌───────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐  │
│  │  PII Guardrails / Vask│  │  Predictive Engine   │  │ Glass-Box Prompting  │  │
│  │  (Regex & Spacy lokal)│  │  (Monte Carlo & EVM) │  │ (§-kildehenvisning)  │  │
│  └───────────────────────┘  └──────────────────────┘  └──────────────────────┘  │
└────────────────═══┬───────────────────────────────────────────┬─────────────────┘
                    │                                           │
                    ▼                                           ▼
┌──────────────────────────────────────┐    ┌─────────────────────────────────────┐
│  SQLITE STAR SCHEMA & DUCKDB OLAP    │    │  HYBRID LLM INFERENCE GATEWAY       │
│  • Fact_Regnskap & Fact_Budsjett     │    │  • Google Gemini 3.8 Flash (Sky)    │
│  • Dim_Funksjon, Dim_Art, Dim_Ansvar │    │  • Ollama llama3.2/qwen2.5 (Lokal)  │
│  • Dim_Budsjettansvarlige (81 enheter│    │  • sqlite-vec (384D) & FTS5 søk     │
│  • Audit_Trail (SHA-256 Hash)        │    │  • SentenceTransformer Embeddings   │
└──────────────────────────────────────┘    └─────────────────────────────────────┘
```

---

## 🚀 Hurtigstart & Operasjonelle Kommandoer

### Systemkrav
- **OS:** Windows 11 / Windows Server / Linux
- **Python:** 3.11+
- **Nettleser:** Edge, Chrome eller Firefox (for `index.html`)
- **Ollama:** *(Valgfritt for lokal offline-inferens)* med `llama3.2` eller `qwen2.5`

---

### 1. Oppstart av Control Office Hub V2
Det interaktive hoveddashboardet kan startes på to måter:
* **Hurtigstart via batch-fil:** Dobbeltklikk [`start_kommune_ai.bat`](./start_kommune_ai.bat)
* **Manuell oppstart via PowerShell:**
  ```powershell
  # Start FastAPI backend-tjenesten
  python tools/hub_api_server.py
  ```
  Åpne deretter [`index.html`](./index.html) direkte i nettleseren. Backend kjører på `http://127.0.0.1:8766`.

---

### 2. Unified CLI Tool Runner (`tools/run_tool.py`)
Alle operative kontrollmotorer kan kjøres via et felles kommandolinjegrensesnitt:

```powershell
# Vis alle tilgjengelige verktøymoduler
python tools/run_tool.py --help

# 1. Kjør rullende Monte Carlo og EVM tidsserieprognoser (P10/P50/P90)
python tools/run_tool.py forecast --mode both

# 2. Utfør lovpålagt revisjons- og kontrollvalidering (§§ 14-5/14-6)
python tools/run_tool.py audit --check-all

# 3. Generer FAST-kompatibel Excel-modell for Kristiansand kommune
python tools/run_tool.py excel --year 2026

# 4. Verifiser integriteten til Control Office Hub og KPI-data
python tools/run_tool.py verify

# 5. Start Hub API-serveren
python tools/run_tool.py server --port 8766
```

---

### 3. Validering og Testkjøring
Verifiser at alle 6 kjernedimensjoner (Hub UI, revisjonsmotor, EVM, MVP-pilot, MCP-server, API og MS-pilot subprosjekt) fungerer feilfritt:

```powershell
# Kjører full testsuite (32 tester i tests/ og antigravity-ms-pilot/tests/)
pytest -v
```

---

### 4. Kontainerdrift via Docker Compose
For produksjons- eller staging-miljø:

```bash
docker compose up -d --build
docker compose ps
```

---

## 📂 Repositoriets Katalogstruktur

```text
AI_KOM/
├── .agents/                       # Antigravity AI Customizations (19 skills, 3 prosjektregler)
│   ├── rules/                     # Tufte Data-Ink, EVM-formler og Local-First AI regler
│   └── skills/                    # Native Antigravity ferdigheter med SKILL.md
├── AGENTS.md                      # Master AI Context & Repository Architecture Guide
├── INDEX.md                       # Sentral dokumentasjonsindeks og arkivkatalog
├── index.html                     # Control Office Hub V2 (Zero-Click Triage, Framsikt Budsjettmodul)
├── agenter/                       # 12 operative personas for økonomistyring og prosjektcontrolling
├── budsjett-framsikt/             # Framsikt EPM & KOSTRA Master Package (Stillings-/lønnsmotor, selvkost)
├── erp_data/                      # Municipal Data Lake (kommune_golden_record.db, delegeringskatalog)
├── tools/                         # Operative CLI-motorer (run_tool.py, predictive_forecasting_engine.py)
├── tests/                         # Master Test Suite (test_project_master.py, 100 % kjernevalidering)
├── powerpoint/                    # 16:9 executive decks og automatiseringsspesifikasjoner
├── word/                          # Politiske saksfremleggsmaler og Public 360-standarder
├── excel/                         # FAST Financial Modelling, MCP-integrasjon og openpyxl-modeller
├── powerbi/                       # Power BI Fabric arkitektur, DAX-bibliotek og .pbip-modeller
├── reports/                       # Ledelsesrapporter, Tufte-visualiseringer og regnskapsmodeller
├── templates/                     # Offisielle maler for Bystyret, drøftingsprotokoller og saksfremlegg
├── revisjon-og-kontroll/          # Sjekklister for Kommunerevisjonen, kontrollnotater og tertialnotat
├── bruker-guides/                 # Brukerveiledninger, månedshjul, årskalender og delegeringskatalog
├── spesifikasjoner/               # Tekniske spesifikasjoner for web-hub, prediksjon og MLOps
├── mvp-pilot/                     # Operativ pilot for Bo og Miljø (Streamlit, DuckDB, SQLite)
├── generic-ai-pilot-pakke/        # Leverandøruavhengig Enterprise AI Pilot-pakke (malverk for alle virksomheter)
├── antigravity-ms-pilot/          # Kristiansand M365 Copilot & Antigravity subprosjekt (motor, evaluator, tester)
├── ai-implementeringspakke-okonomi/  # 9-delt Håndbok for kommunal AI-implementering
├── mlops-implementeringspakke/        # 6-delt MLOps & LLMOps styrings- og anskaffelsespakke
├── start_kommune_ai.bat           # Hurtigoppstart av Control Office Hub
├── oppdater_vektor_db.bat         # Reindeksering av lokal kunnskapsbase
└── README.md                      # Prosjektoversikt og hurtigguide
```

---

## 🧠 Antigravity AI Customization (`.agents/`)

Repositoryet er bygget etter Antigravity sin standard for progressiv kontekst og spesialisering:

### A. Prosjektregler (`.agents/rules/`)
* **[`01_tufte_data_ink_rules.md`](./.agents/rules/01_tufte_data_ink_rules.md)**: Edward Tufte styling, fargedisiplin, fjerning av vertikale linjer og direkte kurve-etikettering.
* **[`02_project_controlling_evm_rules.md`](./.agents/rules/02_project_controlling_evm_rules.md)**: Earned Value-formler (CPI, SPI, EAC, ETC, VAC) og lovpålagte terskler jf. §§ 14-5/14-6.
* **[`03_local_first_ai_architecture_rules.md`](./.agents/rules/03_local_first_ai_architecture_rules.md)**: Lokal datalagring i DuckDB/SQLite, PII-vask og datavern.

### B. 19 Native Antigravity Skills (`.agents/skills/`)
| Kategori | Ferdighet | Formål & Nøkkelstandard |
| :--- | :--- | :--- |
| **Governance & Revisjon** | [`audit-governance`](./.agents/skills/audit-governance/SKILL.md) | SHA-256 forsegling, Eurocities transparens og revisjonslogg |
| | [`pii-guardrails`](./.agents/skills/pii-guardrails/SKILL.md) | Lokal PII-skjerming (FNR, navn, konto, tlf) før modellkall |
| | [`rag-legal-query`](./.agents/skills/rag-legal-query/SKILL.md) | Kildekritiske oppslag i kommunelov, forskrifter og økonomireglement |
| | [`saksfremlegg-generator`](./.agents/skills/saksfremlegg-generator/SKILL.md) | Formelle politiske saksnotater til Bystyret jf. § 14-5 |
| **Finans & Controlling** | [`epm-variance-detect`](./.agents/skills/epm-variance-detect/SKILL.md) | Z-score avviksdeteksjon mellom Visma ERP og periodiserte budsjetter |
| | [`predictive-forecasting`](./.agents/skills/predictive-forecasting/SKILL.md) | Monte Carlo P10/P50/P90, rullende EAC/ETC og KS2-usikkerhet |
| | [`kostra-analyzer`](./.agents/skills/kostra-analyzer/SKILL.md) | Drift vs. investering (§ 14-9), selvkost og KOSTRA-nøkkeltall |
| | [`duckdb-analytics`](./.agents/skills/duckdb-analytics/SKILL.md) | In-memory OLAP-spørringer mot Golden Record og Parquet-eksport |
| **Modellering & BI** | [`excel-python-fpna`](./.agents/skills/excel-python-fpna/SKILL.md) | FAST Standard finansiell modellering via Python openpyxl |
| | [`excel-mcp`](./.agents/skills/excel-mcp/SKILL.md) | Power Query M-kode og DAX-automatisering via MCP |
| | [`powerbi-fabric`](./.agents/skills/powerbi-fabric/SKILL.md) | Star Schema datamodellering, dynamiske DAX-formler og .pbip |
| | [`visual-data-communication`](./.agents/skills/visual-data-communication/SKILL.md) | Tufte-visualiseringer, sparklines, waterfalls og IBCS |
| **Data & Infrastruktur** | [`data-integration-etl`](./.agents/skills/data-integration-etl/SKILL.md) | Visma ERP & Framsikt EPM datafangst til SQLite Star Schema |
| | [`sqlite-vec-executor`](./.agents/skills/sqlite-vec-executor/SKILL.md) | 384D vektor-KNN og FTS5 hybridtekstsøk i SQLite |
| | [`document-parser`](./.agents/skills/document-parser/SKILL.md) | Tekstekstraksjon fra PDF (§-chunking), Word (.docx) og Excel |
| | [`python-sandbox`](./.agents/skills/python-sandbox/SKILL.md) | Isolert og trygg kjøring av analyseskripter |
| **AI Orchestration** | [`llm-gateway`](./.agents/skills/llm-gateway/SKILL.md) | Hybrid modellruting mellom Google Gemini Flash og Ollama |
| | [`ollama-api-bridge`](./.agents/skills/ollama-api-bridge/SKILL.md) | Lokal Ollama-klient med tvungen JSON Schema-respons |
| | [`streamlit-builder`](./.agents/skills/streamlit-builder/SKILL.md) | Rask prototypebygging av interne BI-apper |

---

## 📊 Framsikt EPM & Budsjettstyring (`budsjett-framsikt/`)

I samsvar med Kristiansand kommunes økonomiplan og gjeldende budsjettpraksis er budsjettmotoren dokumentert i et eget fagkompleks og direkte integrert i web-huben:

* **[`budsjettering-kristiansand-kommune.md`](./budsjett-framsikt/budsjettering-kristiansand-kommune.md)**: Kommunens rammer (11,48 mrd samlet budsjett, $\ge 1,0\%$ netto driftsresultat, $\ge 4,0\%$ disposisjonsfond, lånegjeld $<8,8$ mrd) og 8-trinns årshjul fra mai til desember.
* **[`lonnsbudsjettering-kristiansand-framsikt.md`](./budsjett-framsikt/lonnsbudsjettering-kristiansand-framsikt.md)**: Stillings- og lønnsbudsjettering i Framsikt: Fastlønn (art 1010) vs variable potter (1020/1050/1090), feriepenger (12,0 % / 14,3 %), pensjon (SPK/KLP), arbeidsgiveravgift Sone 1 (14,1 %) og bruttoføring jf. § 14-6.
* **[`driftsarter-og-selvkost-alle-omrader-framsikt.md`](./budsjett-framsikt/driftsarter-og-selvkost-alle-omrader-framsikt.md)**: Driftsarter (1100–1270 varekjøp, 1300–1480 overføringer, 1500–1930 finans) og selvkostkalkyler for VAR og Byggesak med 5-års fremføringsregel.
* **[`kostra-artskontoer-konteringsregler-framsikt.md`](./budsjett-framsikt/kostra-artskontoer-konteringsregler-framsikt.md)**: KOSTRA-konteringsregler og controllerens kvalitetssjekkliste før låsing i Framsikt.
* **Integrert Budsjettmodul i Hub:** Se [`index.html#budsjett-modul-seksjon`](./index.html#budsjett-modul-seksjon) for kalkulator for nye stillinger, selvkost for VAR og register over budsjettansvarlige.

---

## 💾 Data Lake & Golden Record (`erp_data/`)

* **`kommune_golden_record.db`**: SQLite Star Schema med `Fact_Regnskap`, `Fact_Budsjett`, `Dim_Funksjon`, `Dim_Art`, `Dim_Ansvar`, `Dim_Budsjettansvarlige` og `Audit_AI_Actions`.
* **Delegeringskatalog 2026:** [`budsjettansvarlige_register.json`](./erp_data/budsjettansvarlige_register.json) og [`.csv`](./erp_data/budsjettansvarlige_register.csv) dekker **81 enheter** fordelt på 6 virksomhetsområder (Oppvekst, Helse og mestring, By- og stedsutvikling, Kultur og innbyggerdialog, Økonomi og eierskap, Organisasjon).
* **Delegeringshåndbok:** [`bruker-guides/BUDSJETTANSVARLIGE_OG_DELEGERINGSKATALOG_2026.md`](./bruker-guides/BUDSJETTANSVARLIGE_OG_DELEGERINGSKATALOG_2026.md) gir full oversikt over anvisningsmyndighet, fullmaktsgrenser og kontaktflate.

---

## 🤖 De 12 Spesialiserte Agentene (`agenter/`)

Plattformen definerer 12 operative personas som samarbeider under Stage-Gate-styring:
1. [`01_dataintegrasjon_etl_agent.md`](./agenter/01_dataintegrasjon_etl_agent.md) — Visma ERP og Framsikt datafangst.
2. [`02_bi_dax_modellering_agent.md`](./agenter/02_bi_dax_modellering_agent.md) — Star Schema og DAX-beregninger.
3. [`03_prediktiv_anomali_agent.md`](./agenter/03_prediktiv_anomali_agent.md) — Z-score og statistiske avviksvarsler.
4. [`04_preskriptiv_hitl_agent.md`](./agenter/04_preskriptiv_hitl_agent.md) — Stage-Gate Port 9 tiltak og saksbehandlergodkjenning.
5. [`05_etikk_styring_portvakt_agent.md`](./agenter/05_etikk_styring_portvakt_agent.md) — PII-skjerming og etiske retningslinjer.
6. [`06_ledelsesrapport_skribent_agent.md`](./agenter/06_ledelsesrapport_skribent_agent.md) — Konsise tertial- og månedsrapporter.
7. [`07_excel_powerbi_rapportering_agent.md`](./agenter/07_excel_powerbi_rapportering_agent.md) — FAST-modellering og Fabric-leveranser.
8. [`08_flerniva_interessent_rapportering_agent.md`](./agenter/08_flerniva_interessent_rapportering_agent.md) — Rapportering tilpasset Nivå 1 (Bystyret) til Nivå 5 (Enhetsleder).
9. [`09_prosjektcontroller_eac_etc_agent.md`](./agenter/09_prosjektcontroller_eac_etc_agent.md) — Investeringsprosjekter, EVM og KS2.
10. [`10_likviditet_finans_renteeksponering_agent.md`](./agenter/10_likviditet_finans_renteeksponering_agent.md) — Finansreglement og gjeldsportefølje.
11. [`11_selvkost_gebyr_kalkyle_agent.md`](./agenter/11_selvkost_gebyr_kalkyle_agent.md) — VAR-gebyrer og selvkostfond.
12. [`12_revisjon_internkontroll_sporbarhet_agent.md`](./agenter/12_revisjon_internkontroll_sporbarhet_agent.md) — Kommunerevisjonen, SHA-256 og § 14-5.

---

## 🎯 Håndbok & Rammeverk: AI-implementering for Økonomi og Virksomhetsstyring

Prosjektet inkluderer et komplett, operasjonelt rammeverk for implementering av AI i kommunal sektor, forankret i føringer fra **Digitaliseringsdirektoratet (Digdir)**, **KS**, **EU AI Act** og **Kristiansand kommunes Økonomiplan 2027–2030**:

| Modul | Fil | Tittel & Målgruppe | Nøkkeltema |
| :--- | :--- | :--- | :--- |
| **00** | [`00_INNHOLD_OG_OVERSIKT.md`](./ai-implementeringspakke-okonomi/00_INNHOLD_OG_OVERSIKT.md) | **Masteroversikt & Struktur**<br>*(Kommunedirektør & Ledergruppe)* | Overordnet dokumentkompleks og tverrgående prinsipper. |
| **01** | [`01_MODUL_1_KONSEPT_OG_BESLUTNINGSGRUNNLAG.md`](./ai-implementeringspakke-okonomi/01_MODUL_1_KONSEPT_OG_BESLUTNINGSGRUNNLAG.md) | **Konseptuelt & Beslutningsgrunnlag**<br>*(Politikere & Toppledelse)* | Demografisk klemme, RPA vs. RAG vs. Agentic AI, verdipotensial. |
| **02** | [`02_MODUL_2_AI_READINESS_OG_MATURITY_FRAMEWORK.md`](./ai-implementeringspakke-okonomi/02_MODUL_2_AI_READINESS_OG_MATURITY_FRAMEWORK.md) | **Readiness & Modenhetsrammeverk**<br>*(Økonomidirektør & IT-sjef)* | L1 (Umoden) til L5 (Transformert) over 9 kjerneområder. |
| **03** | [`03_MODUL_3_GOVERNANCE_ETIKK_OG_GDPR.md`](./ai-implementeringspakke-okonomi/03_MODUL_3_GOVERNANCE_ETIKK_OG_GDPR.md) | **Governance, Etikk, GDPR & EU AI Act**<br>*(Personvernombud & Jurister)* | Kommunen som *deployer*, FRIA, DPIA, forbud mot leverandørtrening. |
| **04** | [`04_MODUL_4_ENTERPRISE_MAALARKITEKTUR_OG_RAG.md`](./ai-implementeringspakke-okonomi/04_MODUL_4_ENTERPRISE_MAALARKITEKTUR_OG_RAG.md) | **Enterprise AI Målarkitektur & RAG**<br>*(Virksomhetsarkitekter & IT)* | AI Gateway, PII-maskering, hybrid søk (RRF) og modelluavhengighet. |
| **05** | [`05_MODUL_5_USE_CASE_PRIORITERING_OG_PILOTMETODIKK.md`](./ai-implementeringspakke-okonomi/05_MODUL_5_USE_CASE_PRIORITERING_OG_PILOTMETODIKK.md) | **Use-Case-Prioritering & Pilotmetodikk**<br>*(Prosjekteiere & Faglige rådgivere)* | Netto prioriteringsformel, Bølge 1–3, 4-trinns pilot og Gate G1–G4. |
| **06** | [`06_MODUL_6_SKALERING_GEVINST_OG_ROADMAP_KRISTIANSAND.md`](./ai-implementeringspakke-okonomi/06_MODUL_6_SKALERING_GEVINST_OG_ROADMAP_KRISTIANSAND.md) | **Skalering, Gevinst & Roadmap 2025–2030**<br>*(Formannskap & Controller)* | Kristiansand-case: Kapasitetsreallokering, konsulentkutt og FinOps. |
| **07** | [`07_JURIDISK_SJEKKLISTE_FRIA_DPIA.md`](./ai-implementeringspakke-okonomi/07_JURIDISK_SJEKKLISTE_FRIA_DPIA.md) | **Operasjonell Juridisk Sjekkliste**<br>*(Saksbehandlere & Jurister)* | 5-trinns skriveklar sjekkliste for screening, hjemmel og godkjenning. |
| **08** | [`08_GEVINSTMODELL_OG_FINANSIELL_HANDBOK.md`](./ai-implementeringspakke-okonomi/08_GEVINSTMODELL_OG_FINANSIELL_HANDBOK.md) | **Finansiell Håndbok & Gevinstmodell**<br>*(Controllere & Økonomirådgivere)* | Manual for `gevinstmodell-ai-okonomi.xlsx`, 3-års ROI og payback. |

---

## ⚙️ MLOps & LLMOps: Operasjonell Plattform, Drift & Anskaffelse

For å sikre trygg, skalerbar og regelverkskonform drift i tråd med **EU AI Act art. 26**, **GDPR art. 22**, **Forvaltningsloven § 25** og **ISO 42001 (AIMS)**, inkluderer prosjektet en skriveklar 6-delt MLOps-pakke:

| Modul | Fil | Tittel & Målgruppe | Nøkkeltema |
| :--- | :--- | :--- | :--- |
| **01** | [`01_MLOps_Oversikt_og_Prinsipper.md`](./mlops-implementeringspakke/01_MLOps_Oversikt_og_Prinsipper.md) | **MLOps & LLMOps Oversikt & Prinsipper**<br>*(Kommunedirektør & IT-sjef)* | DevOps vs MLOps vs LLMOps, 5 kjørneprinsipper, livsløp for kommunale AI-modeller. |
| **02** | [`02_MLOps_Arkitektur_og_Komponenter.md`](./mlops-implementeringspakke/02_MLOps_Arkitektur_og_Komponenter.md) | **Teknisk MLOps-Arkitektur & Komponenter**<br>*(Løsningsarkitekter & MLOps Engineers)* | Enterprise Control Plane, AI Gateway, PII-vask, DVC, Model Registry (MLflow) og CI/CD. |
| **03** | [`03_MLOps_Observability_og_Drift.md`](./mlops-implementeringspakke/03_MLOps_Observability_og_Drift.md) | **Observability, Drift-Håndtering & FinOps**<br>*(Driftsansvarlige & Controllere)* | Overvåking av data-, concept- og prompt-drift, token caching og avdelingsvise budsjettak. |
| **04** | [`04_MLOps_Governance_og_Sikkerhet.md`](./mlops-implementeringspakke/04_MLOps_Governance_og_Sikkerhet.md) | **MLOps Governance, EU AI Act & Sikkerhet**<br>*(CISO, Personvernombud & Jurister)* | Deployer-krav, 4-delt operativ rollestruktur, lovpålagt audit logg (art. 26) og Kill-Switch. |
| **05** | [`05_MLOps_Test_og_Kvalitetssikring.md`](./mlops-implementeringspakke/05_MLOps_Test_og_Kvalitetssikring.md) | **Testing, Ground Truth & Kvalitetssikring**<br>*(Kvalitetsledere & Fagøkonomer)* | Test-pyramide for AI, Ground Truth fasitsett, Faithfulness og Gate G3 akseptkriterier. |
| **06** | [`06_MLOps_Anbud_og_Innkjoepsmal.md`](./mlops-implementeringspakke/06_MLOps_Anbud_og_Innkjoepsmal.md) | **Kravspesifikasjon & Anbudsmal**<br>*(Innkjøpere & Fagledere)* | K-01 til K-10 A/B-kravmatrise, datasuverenitet og forbud mot leverandørtrening på data. |

---

## 🌐 Generisk Enterprise AI Pilot-Pakke (`generic-ai-pilot-pakke/`)

For virksomheter som ønsker en **leverandøruavhengig, flyttbar standard**, inkluderer repositoriet [`generic-ai-pilot-pakke/`](./generic-ai-pilot-pakke/README.md). Den inneholder det komplette enterprise-malverket [`enterprise-ai-pilot/`](./generic-ai-pilot-pakke/enterprise-ai-pilot/README.md) med parametriserte moduler for:
* **Målarkitektur**: AI Gateway, PII-vask og Zero Trust Control Plane.
* **FinOps & Følsomhet**: +1,06 mill. kr netto gevinstmodell og break-even kalkyle.
* **Governance**: Formelt saksfremlegg og 1-sides sponsorkort.
* **Juss & Risiko**: Full DPIA/FRIA-sjekkliste og evalueringsskjema.
* **Prompter & DAX**: Standardiserte KOSTRA-prompter og korrigert DAX-avvikslogikk.

---

## 🚀 Antigravity & Microsoft 365 Copilot Subprosjekt (`antigravity-ms-pilot/`)

[`antigravity-ms-pilot/`](./antigravity-ms-pilot/README.md) er et fullverdig, operasjonelt subprosjekt skreddersydd for Kristiansand kommune:
* **Kildekode (`src/`)**: Innebygd PII-maskering (`src/gateway/`), hybrid retrieval med tabellbevaring (`src/rag/`), og SHA-256 revisjonslogging (`src/utils/`).
* **CLI Runner**: `python run_pilot.py --check-compliance` for automatisk verifikasjon av PII, token limits og revisjonsstempel.
* **Testsuite**: Egen pytest-suite i `antigravity-ms-pilot/tests/`.
* **Standarder**: Full etterlevelse av Kommuneloven §§ 14-5/14-6, HTA § 4 og Stage-Gate Port 9 HITL.

---

## ⚡ Antigravity Backend Engine Module (`antigravity_backend_module_pakke/`)

[`antigravity_backend_module_pakke/`](./antigravity_backend_module_pakke/) utgjør den tekniske mikrotjeneste- og backend-spesifikasjonen (v2.4.0) for enterprise-drift av AI_KOM:
* **[`ANTIGRAVITY_backend_architecture.md`](./antigravity_backend_module_pakke/ANTIGRAVITY_backend_architecture.md)**: Teknisk systemarkitektur: FastAPI router, Polars/DuckDB in-memory analytisk motor, Celery/Redis bakgrunnskø og Stage-Gate Port 9 audit motor.
* **[`ANTIGRAVITY_data_pipeline_and_connectors.md`](./antigravity_backend_module_pakke/ANTIGRAVITY_data_pipeline_and_connectors.md)**: Integrasjonskonnektorer for Visma Enterprise ERP, Framsikt API (REST/GraphQL) og SSB KOSTRA, med lokal HMAC-SHA256 PII-maskering.
* **[`ANTIGRAVITY_ai_rag_services.md`](./antigravity_backend_module_pakke/ANTIGRAVITY_ai_rag_services.md)**: Grounded RAG-arkitektur, semantisk oppstykking, Qdrant/sqlite-vec vektorindeksering og Stage-Gate Port 9 godkjenningsflyt.
* **[`ANTIGRAVITY_api_spec_and_deployment.md`](./antigravity_backend_module_pakke/ANTIGRAVITY_api_spec_and_deployment.md)**: RESTful OpenAPI 3.1 endepunkter (`/api/v1/finance`, `/api/v1/ai`, `/api/v1/governance`), produksjonsklar `Dockerfile` og Kubernetes manifest.

---

## 🧭 AI_KOM Layout, Navigasjon & MLOps Governance (`AI_KOM_MLOps_og_Navigasjon_pakke/`)

[`AI_KOM_MLOps_og_Navigasjon_pakke/`](./AI_KOM_MLOps_og_Navigasjon_pakke/) definerer layoutstrukturen og sporbarhetsmodellen for webportalen:
* **[`AI_KOM_layout_og_navigasjon-v2.md`](./AI_KOM_MLOps_og_Navigasjon_pakke/AI_KOM_layout_og_navigasjon-v2.md)**: Hovedspesifikasjon for portalens 4-fasede rollebaserte navigasjon (Fane 1: Min Enhet, Fane 2: Sektor & Konsern, Fane 3: Controller Hub, Fane 4: Veiledere & Maler).
* **[`AI_KOM_MLOps_og_Data_Lineage.md`](./AI_KOM_MLOps_og_Navigasjon_pakke/AI_KOM_MLOps_og_Data_Lineage.md)**: Full sporbarhet (End-to-End Lineage Graph) fra rådata i Visma/Framsikt -> DAX Måltall -> RAG Vektorindeks -> AI Sak med SHA-256 kryptografisk revisjonsstempel.
* **[`README.md`](./AI_KOM_MLOps_og_Navigasjon_pakke/README.md)**: Pakkeoversikt og sjekkliste mot live GitHub Pages-portal.

---

## 📦 M10 Oktober Month-End Staging & Ingestion Pack (`antigravity_m10_monthend_pack/`)

[`antigravity_m10_monthend_pack/`](./antigravity_m10_monthend_pack/) etablerer arkitekturen for automatisk ankomstovervåking (webhook og file-watcher), staging-kø og saksbehandlerstyrt "Push Button" datafangst:
* **[`ANTIGRAVITY_M10_MonthEnd_Monitoring_and_Staging.md`](./antigravity_m10_monthend_pack/ANTIGRAVITY_M10_MonthEnd_Monitoring_and_Staging.md)**: Teknisk spesifikasjon for ankomst-webhook (`POST /api/v1/events/month-end`), staging-kø (`STAGED_AWAITING_HUMAN_APPROVAL`), og manuell igangsetting (`POST /api/v1/ingestion/m10/execute`).
* **[`M10_Oktober_2026_Regnskap_Fiktiv.csv`](./antigravity_m10_monthend_pack/M10_Oktober_2026_Regnskap_Fiktiv.csv)**: Realistisk fiktivt M10-regnskap datasett fordelt på Oppvekst (vikaravvik), Helse (overtid), Byutvikling (brøyting/VAR) og IKT.
* **Portal Staging Banner:** Integrert interaktiv bannerkomponent i [`index.html`](./index.html) for direkte manuell utløsing og SHA-256 stempling.

---

## 🧾 MVA Balansekonto 2130 & CI/CD Actions (`antigravity_mva_ci_actions_pakke/` & `antigravity_mva_test_pakke/`)

Integrert kvalitetssikring for Momskompensasjonsloven og automatisk avstemming mot Balansekonto 2130:
* **GitHub Actions Workflow:** [`.github/workflows/mva_validering_ci.yml`](./.github/workflows/mva_validering_ci.yml) kjører automatisk validering ved push eller manuell workflow_dispatch.
* **Pipeline Veileder:** [`docs/ANTIGRAVITY_MVA_CI_CD_Pipeline_Guide.md`](./docs/ANTIGRAVITY_MVA_CI_CD_Pipeline_Guide.md) forklarer arkitekturen, revisjonssporet og 90-dagers audit retention.
* **Valideringsmotor:** [`tools/mva_balanse_validator.py`](./tools/mva_balanse_validator.py) og [`tests/test_mva_balanse_2130.py`](./tests/test_mva_balanse_2130.py) sikrer $\text{Differanse}(\text{MVA-Komp} - \text{Konto 2130}) = 0{,}00\text{ kr}$.
* **Testrapport:** [`reports/test_mva_balanse_2130_rapport.md`](./reports/test_mva_balanse_2130_rapport.md).

---

## 🚦 Fast-Path Triage Router & App Engine (`app/`)

[`app/core/triage_router.py`](./app/core/triage_router.py) fungerer som sentral forespørselshåndterer for AI_KOM:
* **Sub-2ms klassifisering:** Rask regex-analyse ruter innkommende henvendelser til `DIRECT_MCP`, `RAG_LOOKUP`, `SKILL_WORKFLOW` eller `MEMORY_CONTEXT`.
* **Pydantic v2 Datakontrakter:** [`app/schemas/triage.py`](./app/schemas/triage.py) definerer `TriageRequest`, `TriageDecision` og `ExecutionPriority`.
* **Kryptografisk Integritet:** Hver ruteringsbeslutning stemples med et unikt SHA-256 auditstempel for full sporbarhet.
* **CLI-Kommando:** `python tools/run_tool.py triage "Hva sier § 14-5?"` for direkte interaktiv testing.

---

## 📄 Lisens & Eierskap

Utviklet for og av **Kristiansand kommune**. Tilgjengelig under **MIT-lisensen** for fri gjenbruk og tilpasning i norske kommuner, fylkeskommuner og offentlige virksomheter.
