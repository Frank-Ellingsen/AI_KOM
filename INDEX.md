# 📚 Kristiansand Kommune — Master Documentation & Artifact Index (`INDEX.md`)

> **Sentral innholdsfortegnelse og arkivkatalog for Kristiansand Kommune AI Controller Hub.**  
> Utarbeidet for **Frank Ellingsen** (Senior Financial Controller & Project Controller).  
> Standarder: **Edward Tufte Data-Ink Ratio**, **Kommuneloven §§ 14-5/14-6**, **FAST Standard**, **KS2**.

---

## 🧭 Hurtignavigasjon

* [1. System- og AI-Arkitektur](#1-system--og-ai-arkitektur)
* [2. Antigravity Skills & Regler (`.agents/`)](#2-antigravity-skills--regler-agents)
* [3. De 12 Spesialiserte Agentene (`agenter/`)](#3-de-12-spesialiserte-agentene-agenter)
* [4. Brukerveiledninger & Månedshjul (`bruker-guides/`)](#4-brukerveiledninger--månedshjul-bruker-guides)
* [5. Revisjon, Kontrollutvalg & Lover (`revisjon-og-kontroll/`)](#5-revisjon-kontrollutvalg--lover-revisjon-og-kontroll)
* [6. Spesifikasjonsbunter per Verktøy (PowerPoint, Word, Excel, Power BI)](#6-spesifikasjonsbunter-per-verktøy)
* [7. Offisielle Dokumentmaler (`templates/`)](#7-offisielle-dokumentmaler-templates)
* [8. Brukerguider & Styringsrutiner (`bruker-guides/`)](#8-brukerguider--styringsrutiner-bruker-guides)
* [9. Kjørbare Verktøy & Skript (`tools/`)](#9-kjørbare-verktøy--skript-tools)
* [10. Data & Golden Record (`erp_data/`)](#10-data--golden-record-erp_data)
* [11. Framsikt EPM & Budsjettstyring (`budsjett-framsikt/`)](#11-framsikt-epm--budsjettstyring-budsjett-framsikt)

---

## 1. System- og AI-Arkitektur

| Dokument | Kjerneinnhold & Målgruppe | Filsti |
| :--- | :--- | :--- |
| **Hovedveileder for AI-Agenter** | Persona, arkitektur, Tufte-regler og styringsprinsipper | [`AGENTS.md`](./AGENTS.md) |
| **README & Prosjektoversikt** | Rask oppstart, Docker-oppsett og systemoversikt | [`README.md`](./README.md) |
| **Control Office Hub Web-app** | Komplett interaktivt dashboard med dynamisk sektorsynkronisering | [`index.html`](./index.html) |
| **Kommunal Budsjettmodul (Framsikt)** | Stillings- og lønnsmotor, selvkostkalkulator for VAR, KOSTRA-tabell og QA-motor | [`index.html#budsjett-modul-seksjon`](./index.html#budsjett-modul-seksjon) |
| **Office Dashboard Hub Spec** | Teknisk funksjonsspesifikasjon for web-huben | [`spesifikasjoner/OFFICE_DASHBOARD_HUB_SPEC.md`](./spesifikasjoner/OFFICE_DASHBOARD_HUB_SPEC.md) |
| **Office Hub V2 Workflow UI** | Brukergrensesnitt for månedshjulet og operativ arbeidsflyt | [`spesifikasjoner/OFFICE_DASHBOARD_HUB_V2_WORKFLOW_UI.md`](./spesifikasjoner/OFFICE_DASHBOARD_HUB_V2_WORKFLOW_UI.md) |
| **Gemini Flash MCP Chat Spec** | Spesifikasjon for MCP AI-assistent og slide-out chat | [`spesifikasjoner/GEMINI_FLASH_MCP_CHAT_DEMO_SPEC.md`](./spesifikasjoner/GEMINI_FLASH_MCP_CHAT_DEMO_SPEC.md) |
| **Predictive AI Forecasting Spec** | Spesifikasjon for Monte Carlo og EVM tidsserieprognoser | [`spesifikasjoner/PREDICTIVE_AI_FORECASTING_SPEC.md`](./spesifikasjoner/PREDICTIVE_AI_FORECASTING_SPEC.md) |
| **Docker & MLOps Deployment** | Containerisering, miljøvariabler og lokal hosting | [`spesifikasjoner/DOCKER_AND_MLOPS_DEPLOYMENT.md`](./spesifikasjoner/DOCKER_AND_MLOPS_DEPLOYMENT.md) |

---

## 2. Antigravity Skills & Regler (`.agents/`)

Repositoryet følger Antigravity sin oppdagelsesstandard for lokale agenter:

### A. Prosjektregler (`.agents/rules/`)
* **[`01_tufte_data_ink_rules.md`](./.agents/rules/01_tufte_data_ink_rules.md)**: Edward Tufte styling, tabelloppsett og fargedisiplin.
* **[`02_project_controlling_evm_rules.md`](./.agents/rules/02_project_controlling_evm_rules.md)**: EVM-matematikk, CPI/EAC/VAC terskler og lovkrav (§ 14-5/§ 14-6).
* **[`03_local_first_ai_architecture_rules.md`](./.agents/rules/03_local_first_ai_architecture_rules.md)**: Lokal datalagring, DuckDB/SQLite, Ollama-inferens og PII-vask.

### B. Ferdigheter (`.agents/skills/`)
* **[`kostra-analyzer`](./.agents/skills/kostra-analyzer/SKILL.md)**: Kontoplan, drift vs investering (§ 14-9), KOSTRA arts- og funksjonsanalyse.
* **[`epm-variance-detect`](./.agents/skills/epm-variance-detect/SKILL.md)**: Z-score avviksdeteksjon i periodiserte budsjetter mot Visma ERP.
* **[`duckdb-analytics`](./.agents/skills/duckdb-analytics/SKILL.md)**: In-memory OLAP-analyser over SQLite Star Schema og Parquet-eksport.
* **[`predictive-forecasting`](./.agents/skills/predictive-forecasting/SKILL.md)**: Rullende EOY-prognoser, Monte Carlo P10/P50/P90 og KS2 EVM.
* **[`saksfremlegg-generator`](./.agents/skills/saksfremlegg-generator/SKILL.md)**: Generering av formelle politiske saksfremlegg (§ 14-5).
* **[`rag-legal-query`](./.agents/skills/rag-legal-query/SKILL.md)**: RAG-spørringer mot kommuneloven, økonomireglement og HTA § 4.
* **[`visual-data-communication`](./.agents/skills/visual-data-communication/SKILL.md)**: Tufte-visualisering, waterfall-diagrammer og sparklines.
* **[`powerbi-fabric`](./.agents/skills/powerbi-fabric/SKILL.md)**: DAX-formler, stjernemodell og .pbip rapportstruktur.
* **[`excel-python-fpna`](./.agents/skills/excel-python-fpna/SKILL.md)**: FAST finansiell modellering via Python openpyxl.
* **[`excel-mcp`](./.agents/skills/excel-mcp/SKILL.md)**: Integrasjon mot Excel via MCP og skripting.
* **[`pii-guardrails`](./.agents/skills/pii-guardrails/SKILL.md)**: PII-skjerming og GDPR-vasking for kommunale data.
* **[`audit-governance`](./.agents/skills/audit-governance/SKILL.md)**: Internkontroll, revisjonsspor og SHA-256 forsegling.
* **[`document-parser`](./.agents/skills/document-parser/SKILL.md)**: Dokumentekstraksjon fra PDF, Word og Excel.
* **[`sqlite-vec-executor`](./.agents/skills/sqlite-vec-executor/SKILL.md)**: Vektorsøk og semantisk indeksering med sqlite-vec.
* **[`ollama-api-bridge`](./.agents/skills/ollama-api-bridge/SKILL.md)**: Lokal Ollama inferens og JSON-schema orkestrering.
* **[`python-sandbox`](./.agents/skills/python-sandbox/SKILL.md)**: Sikker lokal kjøring av analyse- og valideringsskripter.
* **[`llm-gateway`](./.agents/skills/llm-gateway/SKILL.md)**: Ruting og fallback mellom lokale modeller og Gemini Flash.
* **[`streamlit-builder`](./.agents/skills/streamlit-builder/SKILL.md)**: Bygging av interne BI-apper i Streamlit.

---

## 3. De 12 Spesialiserte Agentene (`agenter/`)

| Agent | Rolle | Filsti |
| :--- | :--- | :--- |
| **01** | Dataintegrasjon & ETL Agent | [`agenter/01_dataintegrasjon_etl_agent.md`](./agenter/01_dataintegrasjon_etl_agent.md) |
| **02** | BI & DAX Modellering Agent | [`agenter/02_bi_dax_modellering_agent.md`](./agenter/02_bi_dax_modellering_agent.md) |
| **03** | Prediktiv Anomali Agent | [`agenter/03_prediktiv_anomali_agent.md`](./agenter/03_prediktiv_anomali_agent.md) |
| **04** | Preskriptiv HITL Agent (Stage-Gate Port 9) | [`agenter/04_preskriptiv_hitl_agent.md`](./agenter/04_preskriptiv_hitl_agent.md) |
| **05** | Etikk & Styring Portvakt Agent | [`agenter/05_etikk_styring_portvakt_agent.md`](./agenter/05_etikk_styring_portvakt_agent.md) |
| **06** | Ledelsesrapport Skribent Agent | [`agenter/06_ledelsesrapport_skribent_agent.md`](./agenter/06_ledelsesrapport_skribent_agent.md) |
| **07** | Excel & Power BI Rapportering Agent | [`agenter/07_excel_powerbi_rapportering_agent.md`](./agenter/07_excel_powerbi_rapportering_agent.md) |
| **08** | Flernivå Interessent Rapportering Agent | [`agenter/08_flerniva_interessent_rapportering_agent.md`](./agenter/08_flerniva_interessent_rapportering_agent.md) |
| **09** | Prosjektcontroller EAC/ETC Agent | [`agenter/09_prosjektcontroller_eac_etc_agent.md`](./agenter/09_prosjektcontroller_eac_etc_agent.md) |
| **10** | Likviditet, Finans & Renteeksponering Agent | [`agenter/10_likviditet_finans_renteeksponering_agent.md`](./agenter/10_likviditet_finans_renteeksponering_agent.md) |
| **11** | Selvkost & Gebyrkalkyle Agent | [`agenter/11_selvkost_gebyr_kalkyle_agent.md`](./agenter/11_selvkost_gebyr_kalkyle_agent.md) |
| **12** | Revisjon, Internkontroll & Sporbarhet Agent | [`agenter/12_revisjon_internkontroll_sporbarhet_agent.md`](./agenter/12_revisjon_internkontroll_sporbarhet_agent.md) |

---

## 4. Brukerveiledninger & Månedshjul (`bruker-guides/`)

* **Månedlig Avviksrapport Rammeverk**: [`bruker-guides/MANEDLIG_AVVIKSRAPPORT_RAMMEVERK.md`](./bruker-guides/MANEDLIG_AVVIKSRAPPORT_RAMMEVERK.md)
* **Styringskalender & Årshjul 2026**: [`bruker-guides/STYRINGSKALENDER_OG_ARSHJUL_2026.md`](./bruker-guides/STYRINGSKALENDER_OG_ARSHJUL_2026.md)
* **Operativ Brukerguide & Sjekkliste**: [`bruker-guides/BRUKERGUIDE.md`](./bruker-guides/BRUKERGUIDE.md)
* **Budsjettansvarlige & Delegeringskatalog 2026**: [`bruker-guides/BUDSJETTANSVARLIGE_OG_DELEGERINGSKATALOG_2026.md`](./bruker-guides/BUDSJETTANSVARLIGE_OG_DELEGERINGSKATALOG_2026.md)
* **Stage-Gate Rammeverk (Port 1–10)**: [`bruker-guides/stage_gate_rammeverk.md`](./bruker-guides/stage_gate_rammeverk.md)
* **Oppstartsveileder & Startknapp**: [`bruker-guides/OPPSTARTSVEILEDER_STARTKNAPP.md`](./bruker-guides/OPPSTARTSVEILEDER_STARTKNAPP.md)
* **RAG-arkitektur og Kunnskapsbase Forklaring**: [`bruker-guides/rag_forklaring.md`](./bruker-guides/rag_forklaring.md)

---

## 5. Revisjon, Kontrollutvalg & Lover (`revisjon-og-kontroll/`)

* **Controller Sjekkliste og Periodelukking**: [`revisjon-og-kontroll/CONTROLLER_CHECKLIST_OG_PERIODELUKKING.md`](./revisjon-og-kontroll/CONTROLLER_CHECKLIST_OG_PERIODELUKKING.md)
* **Kommunerevisjonens Audit Checklist**: [`revisjon-og-kontroll/KOMMUNEREVISJONEN_AUDIT_CHECKLIST.md`](./revisjon-og-kontroll/KOMMUNEREVISJONEN_AUDIT_CHECKLIST.md)
* **Notat til Kontrollutvalget og Revisjonen**: [`revisjon-og-kontroll/NOTAT_TIL_KONTROLLUTVALGET_OG_REVISJONEN.md`](./revisjon-og-kontroll/NOTAT_TIL_KONTROLLUTVALGET_OG_REVISJONEN.md)
* **Tertialrapport Notat og Saksfremlegg**: [`revisjon-og-kontroll/TERTIALRAPPORT_NOTAT_OG_SAKSFREMLEGG.md`](./revisjon-og-kontroll/TERTIALRAPPORT_NOTAT_OG_SAKSFREMLEGG.md)

---

## 6. Spesifikasjonsbunter per Verktøy

### A. PowerPoint Decks (`powerpoint/powerpoint_kommune_spec_bundle_v1/`)
* **Visual Storytelling & FT-standard**: [`POWERPOINT_VISUAL_STORYTELLING_FT.md`](./powerpoint/powerpoint_kommune_spec_bundle_v1/POWERPOINT_VISUAL_STORYTELLING_FT.md)
* **Bystyret & Formannskapet Decks**: [`POWERPOINT_BYSTYRET_OG_FORMANNSKAPET_DECKS.md`](./powerpoint/powerpoint_kommune_spec_bundle_v1/POWERPOINT_BYSTYRET_OG_FORMANNSKAPET_DECKS.md)
* **Presentasjonsautomatisering via Python**: [`POWERPOINT_PRESENTASJONSSKAPING_AUTOMATION.md`](./powerpoint/powerpoint_kommune_spec_bundle_v1/POWERPOINT_PRESENTASJONSSKAPING_AUTOMATION.md)

### B. Word Saksfremlegg (`word/word_kommune_spec_bundle_v1/`)
* **Politiske Saksfremlegg Maler**: [`WORD_POLITISKE_SAKSFREMLEGG_MALER.md`](./word/word_kommune_spec_bundle_v1/WORD_POLITISKE_SAKSFREMLEGG_MALER.md)
* **Public 360 & Dokumentautomatisering**: [`WORD_PUBLIC360_OG_DOKUMENT_AUTOMATION.md`](./word/word_kommune_spec_bundle_v1/WORD_PUBLIC360_OG_DOKUMENT_AUTOMATION.md)
* **Tertialrapport & HØP Standarder**: [`WORD_TERTIALRAPPORT_OG_HOP_STANDARDER.md`](./word/word_kommune_spec_bundle_v1/WORD_TERTIALRAPPORT_OG_HOP_STANDARDER.md)

### C. Excel FAST Modellering (`excel/excel_kommune_spec_bundle_v1/`)
* **FAST Financial Modelling Standard**: [`EXCEL_FPA_FINANCIAL_MODELLING_FAST.md`](./excel/excel_kommune_spec_bundle_v1/EXCEL_FPA_FINANCIAL_MODELLING_FAST.md)
* **Excel Automatisering & MCP Server**: [`EXCEL_AUTOMATION_AND_MCP_SERVER.md`](./excel/excel_kommune_spec_bundle_v1/EXCEL_AUTOMATION_AND_MCP_SERVER.md)
* **Python & Copilot Integrasjon**: [`EXCEL_PYTHON_AND_COPILOT_INTEGRATION.md`](./excel/excel_kommune_spec_bundle_v1/EXCEL_PYTHON_AND_COPILOT_INTEGRATION.md)

### D. Power BI & DAX Library (`powerbi/power_bi_kommune_spec_bundle_v1/`)
* **Star Schema Datamodell**: [`POWER_BI_DATA_MODEL_STAR_SCHEMA.md`](./powerbi/power_bi_kommune_spec_bundle_v1/POWER_BI_DATA_MODEL_STAR_SCHEMA.md)
* **DAX Mål & Beregningsmotor**: [`POWER_BI_DAX_MEASURES_LIBRARY.md`](./powerbi/power_bi_kommune_spec_bundle_v1/POWER_BI_DAX_MEASURES_LIBRARY.md)
* **Dashboards & 7 Rapportoppsett**: [`POWER_BI_DASHBOARDS_AND_LAYOUTS.md`](./powerbi/power_bi_kommune_spec_bundle_v1/POWER_BI_DASHBOARDS_AND_LAYOUTS.md)
* **Visuals & Tufte Storytelling**: [`POWER_BI_VISUALS_AND_STORYTELLING.md`](./powerbi/power_bi_kommune_spec_bundle_v1/POWER_BI_VISUALS_AND_STORYTELLING.md)

---

## 7. Offisielle Dokumentmaler (`templates/`)

* **Rapportmal Nivå 1: Avdelingsleder**: [`templates/RAPPORTMAL_AVDELINGSLEDER.md`](./templates/RAPPORTMAL_AVDELINGSLEDER.md)
* **Rapportmal Nivå 2: Kommunalsjef**: [`templates/RAPPORTMAL_KOMMUNALSJEF.md`](./templates/RAPPORTMAL_KOMMUNALSJEF.md)
* **Rapportmal Nivå 3: Kommunedirektør**: [`templates/RAPPORTMAL_KOMMUNEDIREKTOR.md`](./templates/RAPPORTMAL_KOMMUNEDIREKTOR.md)
* **Rapportmal Bystyret / Formannskapet**: [`templates/RAPPORTMAL_KOMMUNESTYRET.md`](./templates/RAPPORTMAL_KOMMUNESTYRET.md)
* **Mønsterrapport: Avvik og Effektprognose**: [`templates/RAPPORTMONSTER_AVVIK_OG_EFFEKTPROGNOSE.md`](./templates/RAPPORTMONSTER_AVVIK_OG_EFFEKTPROGNOSE.md)
* **Drøftingsprotokoll HTA § 4**: [`templates/MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.md`](./templates/MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.md)
* **Stage-Gate Port 9 HITL Sign-off**: [`templates/MAL_STAGE_GATE_PORT_9_HITL_SIGNOFF.md`](./templates/MAL_STAGE_GATE_PORT_9_HITL_SIGNOFF.md)
* **FRIA & DPIA Risikovurdering**: [`templates/MAL_FRIA_OG_DPIA_RISIKOVURDERING.md`](./templates/MAL_FRIA_OG_DPIA_RISIKOVURDERING.md)

---

## 8. Brukerguider & Styringsrutiner (`bruker-guides/`)

* **Register over Budsjettansvarlige & Delegeringskatalog**: [`bruker-guides/BUDSJETTANSVARLIGE_OG_DELEGERINGSKATALOG_2026.md`](./bruker-guides/BUDSJETTANSVARLIGE_OG_DELEGERINGSKATALOG_2026.md)
* **Månedlig Avviksrapport Rammeverk**: [`bruker-guides/MANEDLIG_AVVIKSRAPPORT_RAMMEVERK.md`](./bruker-guides/MANEDLIG_AVVIKSRAPPORT_RAMMEVERK.md)
* **Styringskalender & Årshjul 2026**: [`bruker-guides/STYRINGSKALENDER_OG_ARSHJUL_2026.md`](./bruker-guides/STYRINGSKALENDER_OG_ARSHJUL_2026.md)

---

## 9. Kjørbare Verktøy & Skript (`tools/`)

* **[`tools/run_tool.py`](./tools/run_tool.py)**: Hovedinngangsport for kommandolinjen (`forecast`, `audit`, `excel`, `verify`, `server`, `parse`).
* **[`tools/build_budsjettansvarlige_register.py`](./tools/build_budsjettansvarlige_register.py)**: Bygger JSON, CSV og SQLite register over budsjettansvarlige på Nivå 1–4.
* **[`tools/predictive_forecasting_engine.py`](./tools/predictive_forecasting_engine.py)**: Monte Carlo og EVM tidsserieberegning.
* **[`tools/audit_revisjon_validator.py`](./tools/audit_revisjon_validator.py)**: Revisjonsvalidering jf. § 14-5 og § 14-6 med SHA-256 stempel.
* **[`tools/generate_controller_excel_report.py`](./tools/generate_controller_excel_report.py)**: Bygger FAST regneark for Kristiansand kommune.
* **[`tools/hub_api_server.py`](./tools/hub_api_server.py)**: FastAPI backend for `index.html`.
* **[`tools/document_parser.py`](./tools/document_parser.py)**: Tekstekstraksjon fra PDF, Word og Excel.

---

## 10. Data & Golden Record (`erp_data/`)

* **`kommune_golden_record.db`**: SQLite stjernemodell med `Fact_Regnskap`, `Fact_Budsjett`, `Dim_Funksjon`, `Dim_Art`, `Dim_Ansvar`, `Dim_Budsjettansvarlige`.
* **`budsjettansvarlige_register.json` / `.csv`**: Komplett katalog over alle budsjettansvarlige på Nivå 1–4 med kontaktinfo, delegering og skjemaflyt.
* **Råfiler**: Syntetiske regnskapstrekk fra Visma ERP og periodiserte budsjettrammer fra Framsikt EPM.

---

## 11. Framsikt EPM & Budsjettstyring (`budsjett-framsikt/`)

| Dokument | Hovedinnhold & Standard | Filsti |
| :--- | :--- | :--- |
| **Budsjettering & Årshjul** | Måltall (11,48 mrd ramme, $\ge 1,0\%$ driftsres, $\ge 4,0\%$ fond, $<8,8$ mrd lån), 8-faset internt årshjul fra mai til 31. des. | [`budsjett-framsikt/budsjettering-kristiansand-kommune.md`](./budsjett-framsikt/budsjettering-kristiansand-kommune.md) |
| **Stillings- & Lønnsbudsjett** | Fastlønn (1010) vs variable potter (1020/1050/1090), feriepenger (12%/14,3%), SPK vs KLP, AGA Sone 1 (14,1%), bruttoføring jf. § 14-6. | [`budsjett-framsikt/lonnsbudsjettering-kristiansand-framsikt.md`](./budsjett-framsikt/lonnsbudsjettering-kristiansand-framsikt.md) |
| **Driftsarter & Selvkost** | Varekjøp (1100–1270), overføringer (1300–1480), finans/fond (1500–1930), selvkostkalkyler for VAR & Byggesak (3400/3450/3500/3600) med 5-årsregel. | [`budsjett-framsikt/driftsarter-og-selvkost-alle-omrader-framsikt.md`](./budsjett-framsikt/driftsarter-og-selvkost-alle-omrader-framsikt.md) |
| **KOSTRA Konteringsregler** | Lønnsarter, sosiale kostnader og refusjoner (1690). Bruttoføringskrav og controller-sjekkliste før budsjettlåsing i Framsikt. | [`budsjett-framsikt/kostra-artskontoer-konteringsregler-framsikt.md`](./budsjett-framsikt/kostra-artskontoer-konteringsregler-framsikt.md) |
| **Framsikt Master Index (README)** | Samlet inngangsport og hurtigreferanse for AI-agenter og controllere. | [`budsjett-framsikt/README.md`](./budsjett-framsikt/README.md) |

