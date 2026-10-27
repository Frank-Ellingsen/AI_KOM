# 📚 Kristiansand Kommune — Master Documentation & Artifact Index (`INDEX.md`)

> **Sentral innholdsfortegnelse og arkivkatalog for Kristiansand Kommune AI Controller Hub.**  
> Utarbeidet for **Frank Ellingsen** (Senior Financial Controller & Project Controller).  
> Standarder: **Edward Tufte Data-Ink Ratio**, **Kommuneloven §§ 14-5/14-6**, **FAST Standard**, **KS2**.

---

## 🧭 Hurtignavigasjon

* [1. System- og AI-Arkitektur](#1-system--og-ai-arkitektur)
* [2. Antigravity Skills & Regler (`.agents/`)](#2-antigravity-skills--regler-agents)
* [3. De 15 Spesialiserte Agentene (`agenter/`)](#3-de-15-spesialiserte-agentene-agenter)
* [4. Brukerveiledninger & Månedshjul (`bruker-guides/`)](#4-brukerveiledninger--månedshjul-bruker-guides)
* [5. Revisjon, Kontrollutvalg & Lover (`revisjon-og-kontroll/`)](#5-revisjon-kontrollutvalg--lover-revisjon-og-kontroll)
* [6. Spesifikasjonsbunter per Verktøy (PowerPoint, Word, Excel, Power BI)](#6-spesifikasjonsbunter-per-verktøy)
* [7. Offisielle Dokumentmaler (`templates/`)](#7-offisielle-dokumentmaler-templates)
* [8. Brukerguider & Styringsrutiner (`bruker-guides/`)](#8-brukerguider--styringsrutiner-bruker-guides)
* [9. Kjørbare Verktøy & Skript (`tools/`)](#9-kjørbare-verktøy--skript-tools)
* [10. Data & Golden Record (`erp_data/`)](#10-data--golden-record-erp_data)
* [11. Framsikt EPM & Budsjettstyring (`budsjett-framsikt/`)](#11-framsikt-epm--budsjettstyring-budsjett-framsikt)
* [12. Generisk Enterprise AI Pilot-Pakke (`generic-ai-pilot-pakke/`)](#12-generisk-enterprise-ai-pilot-pakke-generic-ai-pilot-pakke)
* [13. Antigravity & MS Copilot Pilot Subprosjekt (`antigravity-ms-pilot/`)](#13-antigravity--ms-copilot-pilot-subprosjekt-antigravity-ms-pilot)
* [14. Antigravity Backend Engine Module (`antigravity_backend_module_pakke/`)](#14-antigravity-backend-engine-module-antigravity_backend_module_pakke)
* [15. AI_KOM Layout, Navigasjon & MLOps Governance (`AI_KOM_MLOps_og_Navigasjon_pakke/`)](#15-ai_kom-layout-navigasjon--mlops-governance-ai_kom_mlops_og_navigasjon_pakke)
* [16. M10 Oktober Month-End Staging & Ingestion Pack (`antigravity_m10_monthend_pack/`)](#16-m10-oktober-month-end-staging--ingestion-pack-antigravity_m10_monthend_pack)
* [17. MVA & Balansekonto 2130 Test- og CI/CD-Pakker](#17-mva--balansekonto-2130-test--og-cicd-pakker)
* [18. Fast-Path Triage Router & App Engine (`app/`)](#18-fast-path-triage-router--app-engine-app)
* [19. Økonomirådgiverens Håndbok & Vektor-DB (`erp_data/`, `tools/`)](#22-økonomirådgiverens-håndbok--vektor-db-utvidelse-erp_data-tools-indexhtml)
* [20. Kommunale Rådgiverkalkulatorer & Helårs Stresstest (`app/`, `tools/`, `index.html`)](#23-kommunale-rådgiverkalkulatorer--helårs-stresstest-app-tools-indexhtml)

---

## 1. System- og AI-Arkitektur

| Dokument | Kjerneinnhold & Målgruppe | Filsti |
| :--- | :--- | :--- |
| **Hovedveileder for AI-Agenter** | Persona, arkitektur, Tufte-regler og styringsprinsipper | [`AGENTS.md`](./AGENTS.md) |
| **README & Prosjektoversikt** | Rask oppstart, Docker-oppsett og systemoversikt | [`README.md`](./README.md) |
| **Control Office Hub Web-app** | Komplett interaktivt dashboard med dynamisk sektorsynkronisering | [`index.html`](./index.html) |
| **Sektorspesifikke Dashboards & Personaer** | Tilpassede visninger for Oppvekst, Helse, Byutvikling, Kultur, IKT & Ledelse | [`index.html#sektor-dashboards`](./index.html) |
| **Kommunal Nettbank for Enhetsledere** | Kontoutskrifter (HTML/CSV/Excel), saldo og proaktive råd for 81 enheter | [`index.html#kommunal-nettbank`](./index.html#kommunal-nettbank) |
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

## 3. De 15 Spesialiserte Agentene (`agenter/`)

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
| **13** | Evaluering & Kvalitetssikring (QA) Agent | [`agenter/13_evaluering_kvalitetssikring_agent.md`](./agenter/13_evaluering_kvalitetssikring_agent.md) |
| **14** | Database & Data Engineering Agent | [`agenter/14_database_data_engineering_agent.md`](./agenter/14_database_data_engineering_agent.md) |
| **15** | AI Engineering & Infrastruktur Agent | [`agenter/15_ai_engineering_infrastruktur_agent.md`](./agenter/15_ai_engineering_infrastruktur_agent.md) |

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

### D. Power BI & DAX Library (`powerbi/`)
* **Star Schema Datamodell**: [`power_bi_kommune_spec_bundle_v1/POWER_BI_DATA_MODEL_STAR_SCHEMA.md`](./powerbi/power_bi_kommune_spec_bundle_v1/POWER_BI_DATA_MODEL_STAR_SCHEMA.md)
* **DAX Mål & Beregningsmotor**: [`power_bi_kommune_spec_bundle_v1/POWER_BI_DAX_MEASURES_LIBRARY.md`](./powerbi/power_bi_kommune_spec_bundle_v1/POWER_BI_DAX_MEASURES_LIBRARY.md)
* **Dashboards & 7 Rapportoppsett**: [`power_bi_kommune_spec_bundle_v1/POWER_BI_DASHBOARDS_AND_LAYOUTS.md`](./powerbi/power_bi_kommune_spec_bundle_v1/POWER_BI_DASHBOARDS_AND_LAYOUTS.md)
* **Visuals & Tufte Storytelling**: [`power_bi_kommune_spec_bundle_v1/POWER_BI_VISUALS_AND_STORYTELLING.md`](./powerbi/power_bi_kommune_spec_bundle_v1/POWER_BI_VISUALS_AND_STORYTELLING.md)
* **Power BI Hovedrapport (PBIP v2 med DQA & 10 PBIR-sider)**: [`pbi-rep-project-rapport.pbip`](./pbi-rep-project-rapport.pbip) *(101 DAX-mål, 16 månedlige faktatabeller, DQA 0/1 kvalitetskontroll)*
* **Power BI Desktop Kopi (.pbix)**: [`pbi-rep-project-rapport.pbix`](./pbi-rep-project-rapport.pbix)
* **Power BI 101 DAX Measures Library**: [`10_PBIP_Rapport_DAX_Measures.dax`](./powerbi/10_PBIP_Rapport_DAX_Measures.dax)
* **Power BI DQA Kontrollrapport**: [`07_Data_Quality_and_Assurance_Rapport.md`](./docs/07_Data_Quality_and_Assurance_Rapport.md)
* **Power BI Prosjekt (PBIP Developer Format)**: [`pbi_reporting_project.pbip`](./powerbi/pbi_reporting_project.pbip)

---

## 7. Offisielle Dokumentmaler (`templates/`)

Samtlige 18 maler foreligger i to formater: **Produksjonsformat** (.docx / .xlsx for nedlasting og saksbehandling) og **Forhåndsvisningsformat** (.md for lynrask visning i Office Hub).

### A. Ledelses- og Styringsrapporter (Nivå 1–4 & Bystyret)
* **Rapportmal Nivå 1: Avdelingsleder**: [`RAPPORTMAL_AVDELINGSLEDER.docx`](./templates/RAPPORTMAL_AVDELINGSLEDER.docx) | [`RAPPORTMAL_AVDELINGSLEDER.md`](./templates/RAPPORTMAL_AVDELINGSLEDER.md)
* **Rapportmal Nivå 2: Seksjonsleder**: [`RAPPORTMAL_SEKSJONSLEDER.docx`](./templates/RAPPORTMAL_SEKSJONSLEDER.docx) | [`RAPPORTMAL_SEKSJONSLEDER.md`](./templates/RAPPORTMAL_SEKSJONSLEDER.md)
* **Rapportmal Nivå 3: Kommunalsjef**: [`RAPPORTMAL_KOMMUNALSJEF.docx`](./templates/RAPPORTMAL_KOMMUNALSJEF.docx) | [`RAPPORTMAL_KOMMUNALSJEF.md`](./templates/RAPPORTMAL_KOMMUNALSJEF.md)
* **Rapportmal Nivå 4: Kommunedirektør**: [`RAPPORTMAL_KOMMUNEDIREKTOR.docx`](./templates/RAPPORTMAL_KOMMUNEDIREKTOR.docx) | [`RAPPORTMAL_KOMMUNEDIREKTOR.md`](./templates/RAPPORTMAL_KOMMUNEDIREKTOR.md)
* **Rapportmal Bystyret / Formannskapet**: [`RAPPORTMAL_KOMMUNESTYRET.docx`](./templates/RAPPORTMAL_KOMMUNESTYRET.docx) | [`RAPPORTMAL_KOMMUNESTYRET.md`](./templates/RAPPORTMAL_KOMMUNESTYRET.md)
* **Mønsterrapport: Avvik og Effektprognose**: [`RAPPORTMONSTER_AVVIK_OG_EFFEKTPROGNOSE.docx`](./templates/RAPPORTMONSTER_AVVIK_OG_EFFEKTPROGNOSE.docx) | [`RAPPORTMONSTER_AVVIK_OG_EFFEKTPROGNOSE.md`](./templates/RAPPORTMONSTER_AVVIK_OG_EFFEKTPROGNOSE.md)

### B. Styring, Avvik & Saksbehandling
* **Avviksnotat og Tiltaksplan Enhetsleder**: [`MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx`](./templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx) | [`MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.md`](./templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.md)
* **Politisk Saksfremlegg Budsjettendring (§ 14-5)**: [`MAL_POLITISK_SAKSFREMLEGG_BUDSJETTENDRING.docx`](./templates/MAL_POLITISK_SAKSFREMLEGG_BUDSJETTENDRING.docx) | [`MAL_POLITISK_SAKSFREMLEGG_BUDSJETTENDRING.md`](./templates/MAL_POLITISK_SAKSFREMLEGG_BUDSJETTENDRING.md)
* **Periodelukking og Avstemmingsinstruks**: [`MAL_PERIODELUKKING_OG_AVSTEMMING.docx`](./templates/MAL_PERIODELUKKING_OG_AVSTEMMING.docx) | [`MAL_PERIODELUKKING_OG_AVSTEMMING.md`](./templates/MAL_PERIODELUKKING_OG_AVSTEMMING.md)
* **Drøftingsprotokoll HTA § 4 & AML § 10-12**: [`MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.docx`](./templates/MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.docx) | [`MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.md`](./templates/MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.md)
* **Stage-Gate Port 9 HITL Sign-off (Kryptografisk SHA-256)**: [`MAL_STAGE_GATE_PORT_9_HITL_SIGNOFF.docx`](./templates/MAL_STAGE_GATE_PORT_9_HITL_SIGNOFF.docx) | [`MAL_STAGE_GATE_PORT_9_HITL_SIGNOFF.md`](./templates/MAL_STAGE_GATE_PORT_9_HITL_SIGNOFF.md)
* **FRIA & DPIA Risikovurdering (AI Act & GDPR art. 35)**: [`MAL_FRIA_OG_DPIA_RISIKOVURDERING.docx`](./templates/MAL_FRIA_OG_DPIA_RISIKOVURDERING.docx) | [`MAL_FRIA_OG_DPIA_RISIKOVURDERING.md`](./templates/MAL_FRIA_OG_DPIA_RISIKOVURDERING.md)

### C. Selvhjelpspakke for Budsjettansvarlige (Nettbank & Verktøykasse)
* **Lederens Månedsstatus og Rullende Prognose**: [`MAL_LEDERENS_MANEDSSTATUS_OG_PROGNOSE.docx`](./templates/MAL_LEDERENS_MANEDSSTATUS_OG_PROGNOSE.docx) | [`MAL_LEDERENS_MANEDSSTATUS_OG_PROGNOSE.md`](./templates/MAL_LEDERENS_MANEDSSTATUS_OG_PROGNOSE.md)
* **Bemanningsplan, Turnus og Vikarbudsjett**: [`MAL_BEMANNINGSPLAN_OG_VIKARBUDSJETT.xlsx`](./templates/MAL_BEMANNINGSPLAN_OG_VIKARBUDSJETT.xlsx) | [`MAL_BEMANNINGSPLAN_OG_VIKARBUDSJETT.md`](./templates/MAL_BEMANNINGSPLAN_OG_VIKARBUDSJETT.md)
* **Internkontroll og Egenvurdering for Leder**: [`MAL_INTERNKONTROLL_EGENVURDERING_LEDER.docx`](./templates/MAL_INTERNKONTROLL_EGENVURDERING_LEDER.docx) | [`MAL_INTERNKONTROLL_EGENVURDERING_LEDER.md`](./templates/MAL_INTERNKONTROLL_EGENVURDERING_LEDER.md)
* **NAV-refusjonsoppfølging og Avstemming**: [`MAL_NAV_REFUSJONSOPPFOLGING_OG_AVSTEMMING.xlsx`](./templates/MAL_NAV_REFUSJONSOPPFOLGING_OG_AVSTEMMING.xlsx) | [`MAL_NAV_REFUSJONSOPPFOLGING_OG_AVSTEMMING.md`](./templates/MAL_NAV_REFUSJONSOPPFOLGING_OG_AVSTEMMING.md)
* **Budsjettinnspill Framsikt HØP 2027**: [`MAL_BUDSJETTINNSPILL_FRAMSIKT_HOP_2027.docx`](./templates/MAL_BUDSJETTINNSPILL_FRAMSIKT_HOP_2027.docx) | [`MAL_BUDSJETTINNSPILL_FRAMSIKT_HOP_2027.md`](./templates/MAL_BUDSJETTINNSPILL_FRAMSIKT_HOP_2027.md)
* **Omdisponering og Rammejustering**: [`MAL_OMDISPONERING_OG_RAMMEJUSTERING.docx`](./templates/MAL_OMDISPONERING_OG_RAMMEJUSTERING.docx) | [`MAL_OMDISPONERING_OG_RAMMEJUSTERING.md`](./templates/MAL_OMDISPONERING_OG_RAMMEJUSTERING.md)

---

## 8. Brukerguider & Styringsrutiner (`bruker-guides/`)

* **Register over Budsjettansvarlige & Delegeringskatalog**: [`bruker-guides/BUDSJETTANSVARLIGE_OG_DELEGERINGSKATALOG_2026.md`](./bruker-guides/BUDSJETTANSVARLIGE_OG_DELEGERINGSKATALOG_2026.md)
* **Månedlig Avviksrapport Rammeverk**: [`bruker-guides/MANEDLIG_AVVIKSRAPPORT_RAMMEVERK.md`](./bruker-guides/MANEDLIG_AVVIKSRAPPORT_RAMMEVERK.md)
* **Styringskalender & Årshjul 2026**: [`bruker-guides/STYRINGSKALENDER_OG_ARSHJUL_2026.md`](./bruker-guides/STYRINGSKALENDER_OG_ARSHJUL_2026.md)
* **Operativ Brukerguide & Sjekkliste**: [`bruker-guides/BRUKERGUIDE.md`](./bruker-guides/BRUKERGUIDE.md)
* **Stage-Gate Rammeverk (Port 1–10)**: [`bruker-guides/stage_gate_rammeverk.md`](./bruker-guides/stage_gate_rammeverk.md)
* **Oppstartsveileder & Startknapp**: [`bruker-guides/OPPSTARTSVEILEDER_STARTKNAPP.md`](./bruker-guides/OPPSTARTSVEILEDER_STARTKNAPP.md)
* **RAG-arkitektur og Kunnskapsbase Forklaring**: [`bruker-guides/rag_forklaring.md`](./bruker-guides/rag_forklaring.md)

---

## 9. Kjørbare Verktøy & Skript (`tools/`)

* **[`tools/run_tool.py`](./tools/run_tool.py)**: Hovedinngangsport for kommandolinjen (`forecast`, `audit`, `excel`, `verify`, `server`, `parse`).
* **[`tools/predictive_forecasting_engine.py`](./tools/predictive_forecasting_engine.py)**: Monte Carlo P10/P50/P90 og EVM tidsserieberegning.
* **[`tools/audit_revisjon_validator.py`](./tools/audit_revisjon_validator.py)**: Revisjonsvalidering jf. § 14-5 og § 14-6 med SHA-256 stempel.
* **[`tools/build_excel_master_report.py`](./tools/build_excel_master_report.py)**: 14-arks master FAST Excel-modell med dynamisk avviksanalyse.
* **[`tools/generate_controller_excel_report.py`](./tools/generate_controller_excel_report.py)**: Bygger FAST regneark for Kristiansand kommune.
* **[`tools/build_budsjettansvarlige_register.py`](./tools/build_budsjettansvarlige_register.py)**: Bygger JSON, CSV og SQLite register over budsjettansvarlige på Nivå 1–4.
* **[`tools/generate_monthly_bank_statements.py`](./tools/generate_monthly_bank_statements.py)**: Kommunal nettbank: Månedlige kontoutskrifter for alle 81 enheter.
* **[`tools/generate_budget_selfservice_templates.py`](./tools/generate_budget_selfservice_templates.py)**: Bygger 6 operative selvhjelpsmaler i Excel og Word.
* **[`tools/generate_office_hub_templates.py`](./tools/generate_office_hub_templates.py)**: Dual-generator for 12 styringsrapporter i .docx og .md.
* **[`tools/data_quality_validator.py`](./tools/data_quality_validator.py)**: Kanonisk datakvalitetsvalidering og skjema-integritet.
* **[`tools/hub_api_server.py`](./tools/hub_api_server.py)**: FastAPI backend for `index.html`.
* **[`tools/verify_office_hub.py`](./tools/verify_office_hub.py)**: Helsetest, streng HTML-parser og lenkevalidering.
* **[`tools/document_parser.py`](./tools/document_parser.py)**: Tekstekstraksjon fra PDF, Word og Excel.

---

## 10. Data, Golden Record & Kontoutskrifter (`erp_data/` & `reports/`)

* **`erp_data/kommune_golden_record.db`**: SQLite stjernemodell med `Fact_Regnskap`, `Fact_Budsjett`, `Dim_Funksjon`, `Dim_Art`, `Dim_Ansvar`, `Dim_Budsjettansvarlige`.
* **`erp_data/budsjettansvarlige_register.json` / `.csv`**: Komplett katalog over alle budsjettansvarlige på Nivå 1–4 med kontaktinfo, delegering og skjemaflyt.
* **`reports/kontoutskrifter/`**: Kommunal nettbank for alle 81 enheter (`KONTOUTSKRIFT_REGISTER_MASTER_2026.json`, `KONTOUTSKRIFT_ALLE_ENHETER_M10.csv`, `KONTOUTSKRIFT_MAL_ENHETSLEDER_2026.xlsx`, og HTML-utskrifter per enhet).
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

---

## 12. Generisk Enterprise AI Pilot-Pakke (`generic-ai-pilot-pakke/`)

> **Leverandøruavhengig og flyttbart malverk for AI-piloter i kommunal og offentlig sektor.**

| Dokument | Hovedinnhold & Målgruppe | Filsti |
| :--- | :--- | :--- |
| **Generisk Pilot Hovedindeks** | Masterveileder for pilotpakken, formål og bruksanvisning | [`generic-ai-pilot-pakke/README.md`](./generic-ai-pilot-pakke/README.md) |
| **Single Source of Truth (SSOT)** | Struktur, moduler og status for enterprise-piloten | [`generic-ai-pilot-pakke/enterprise-ai-pilot/README.md`](./generic-ai-pilot-pakke/enterprise-ai-pilot/README.md) |
| **Enterprise Målarkitektur** | AI Gateway, PII-filter, RAG og Zero Trust kontrollplan | [`enterprise-ai-pilot/docs/architecture/01_maalarkitektur...`](./generic-ai-pilot-pakke/enterprise-ai-pilot/docs/architecture/01_maalarkitektur-okonomi-ai-kristiansand.md) |
| **Gevinstmodell & Følsomhet** | FinOps-kalkyle, break-even og gevinstrealisering | [`enterprise-ai-pilot/docs/financials/01_folsomhetsanalyse...`](./generic-ai-pilot-pakke/enterprise-ai-pilot/docs/financials/01_folsomhetsanalyse-gevinstmodell-ai.md) |
| **Politisk Saksfremlegg** | Formelt saksfremlegg om AI-veikart for økonomi | [`enterprise-ai-pilot/docs/governance/01_saksframlegg...`](./generic-ai-pilot-pakke/enterprise-ai-pilot/docs/governance/01_saksframlegg-ai-veikart-okonomi.md) |
| **Sponsorkort (Cheat Sheet)** | 1-sides beslutningsgrunnlag til toppledelsen | [`enterprise-ai-pilot/docs/governance/02_cheat-sheet...`](./generic-ai-pilot-pakke/enterprise-ai-pilot/docs/governance/02_cheat-sheet-sponsormote-ai.md) |
| **Oppstartsnotat for Pilot** | Operativ veiledning, superbruker-instruks og tidsplan | [`enterprise-ai-pilot/docs/pilot_and_ops/01_oppstartsnotat...`](./generic-ai-pilot-pakke/enterprise-ai-pilot/docs/pilot_and_ops/01_oppstartsnotat-pilotgruppe-ai.md) |
| **Risikovurdering (FRIA/DPIA)** | EU AI Act, GDPR art. 35 og forvaltningsloven § 25 | [`enterprise-ai-pilot/docs/security_and_legal/01_risiko...`](./generic-ai-pilot-pakke/enterprise-ai-pilot/docs/security_and_legal/01_risikovurdering-og-evalueringsskjema-ai-pilot.md) |
| **Ground Truth Fasitsett** | RAGAS fasitsett for Faithfulness og Context Recall | [`enterprise-ai-pilot/evals/01_ground_truth_eval_template.json`](./generic-ai-pilot-pakke/enterprise-ai-pilot/evals/01_ground_truth_eval_template.json) |
| **Copilot Mønsterprompter** | Kvalitetssikrede prompter for Excel (`=PY`), BI og Word | [`enterprise-ai-pilot/prompts/01_promptsett-m365-copilot-kostra.md`](./generic-ai-pilot-pakke/enterprise-ai-pilot/prompts/01_promptsett-m365-copilot-kostra.md) |
| **Generisk DAX & RAG** | Standardisert DAX-formatering (korrigert avvik & RAG-hex) | [`enterprise-ai-pilot/dax_and_analytics/01_generisk_dax...`](./generic-ai-pilot-pakke/enterprise-ai-pilot/dax_and_analytics/01_generisk_dax_og_rag_formatering.dax) |

---

## 13. Antigravity & MS Copilot Pilot Subprosjekt (`antigravity-ms-pilot/`)

> **Operasjonelt subprosjekt for Kristiansand kommune med kildekode, tester og M365 Copilot-prompter.**

| Modul / Fil | Beskrivelse & Formål | Filsti |
| :--- | :--- | :--- |
| **Subproject Master (README)** | Komplett arkitektur, status og hurtigkommandoer | [`antigravity-ms-pilot/README.md`](./antigravity-ms-pilot/README.md) |
| **Subproject Package Config** | Python `pyproject.toml` og `requirements.txt` | [`antigravity-ms-pilot/pyproject.toml`](./antigravity-ms-pilot/pyproject.toml) |
| **CLI Runner (`run_pilot.py`)** | Operativ test- og compliance-motor for piloten | [`antigravity-ms-pilot/run_pilot.py`](./antigravity-ms-pilot/run_pilot.py) |
| **PII Scrubber & Rate Limiter** | PII-maskering (FNR/TLF/E-post) og FinOps token-begrenser | [`antigravity-ms-pilot/src/gateway/pii_scrubber.py`](./antigravity-ms-pilot/src/gateway/pii_scrubber.py) |
| **Hybrid Retriever & Chunker** | Tabellbevarende chunking og BM25 hybrid-søk | [`antigravity-ms-pilot/src/rag/hybrid_retriever.py`](./antigravity-ms-pilot/src/rag/hybrid_retriever.py) |
| **Kryptografisk Audit Logger** | SHA-256 forsegling for Kommunerevisjonen (Port 9) | [`antigravity-ms-pilot/src/utils/audit_logger.py`](./antigravity-ms-pilot/src/utils/audit_logger.py) |
| **Automatisert Testsuite** | Pytest-tester for PII, token limits, RAG og revisjon | [`antigravity-ms-pilot/tests/test_pilot_subproject.py`](./antigravity-ms-pilot/tests/test_pilot_subproject.py) |
| **Kristiansand Promptsett** | KOSTRA- og vikaravviksprompter for Excel `=PY` og Teams | [`antigravity-ms-pilot/prompts/01_promptsett-m365-copilot-kostra.md`](./antigravity-ms-pilot/prompts/01_promptsett-m365-copilot-kostra.md) |
| **Fasitsett (Evals)** | Ground truth fasitsett for Kristiansand kommune | [`antigravity-ms-pilot/evals/01_ground_truth_eval_template.json`](./antigravity-ms-pilot/evals/01_ground_truth_eval_template.json) |

---

## 14. Antigravity Backend Engine Module (`antigravity_backend_module_pakke/`)

> **Teknisk mikrotjeneste- og backend-spesifikasjon (v2.4.0) for enterprise AI_KOM-arkitektur.**

| Modul / Fil | Beskrivelse & Formål | Filsti |
| :--- | :--- | :--- |
| **Backend Arkitektur & Spesifikasjon** | FastAPI router, Polars/DuckDB motor, Celery/Redis og Stage-Gate Port 9 audit | [`antigravity_backend_module_pakke/ANTIGRAVITY_backend_architecture.md`](./antigravity_backend_module_pakke/ANTIGRAVITY_backend_architecture.md) |
| **Konnektorer & ETL Dataflyt** | Integrasjon mot Visma Enterprise, Framsikt API og SSB KOSTRA med PII-maskering | [`antigravity_backend_module_pakke/ANTIGRAVITY_data_pipeline_and_connectors.md`](./antigravity_backend_module_pakke/ANTIGRAVITY_data_pipeline_and_connectors.md) |
| **AI, RAG & Governance Services** | Grounded RAG-arkitektur, Qdrant/sqlite-vec, og Stage-Gate Port 9 godkjenning | [`antigravity_backend_module_pakke/ANTIGRAVITY_ai_rag_services.md`](./antigravity_backend_module_pakke/ANTIGRAVITY_ai_rag_services.md) |
| **API Spesifikasjon & DevOps** | OpenAPI 3.1 REST-endepunkter (`/api/v1`), produksjons-Dockerfile og CI/CD | [`antigravity_backend_module_pakke/ANTIGRAVITY_api_spec_and_deployment.md`](./antigravity_backend_module_pakke/ANTIGRAVITY_api_spec_and_deployment.md) |

---

## 15. AI_KOM Layout, Navigasjon & MLOps Governance (`AI_KOM_MLOps_og_Navigasjon_pakke/`)

> **Layoutspesifikasjon for portalens 4 persona-faner, Data Lineage graf og MLOps livsløp.**

| Modul / Fil | Beskrivelse & Formål | Filsti |
| :--- | :--- | :--- |
| **Portallayout & Navigasjon (v2)** | 4-faset struktur: Min Enhet, Sektor & Konsern, Controller Hub, Veiledere & Maler | [`AI_KOM_MLOps_og_Navigasjon_pakke/AI_KOM_layout_og_navigasjon-v2.md`](./AI_KOM_MLOps_og_Navigasjon_pakke/AI_KOM_layout_og_navigasjon-v2.md) |
| **MLOps, Data Lineage & Governance** | End-to-End sporbarhet: Visma -> Framsikt -> DAX -> RAG -> Sak med SHA-256 | [`AI_KOM_MLOps_og_Navigasjon_pakke/AI_KOM_MLOps_og_Data_Lineage.md`](./AI_KOM_MLOps_og_Navigasjon_pakke/AI_KOM_MLOps_og_Data_Lineage.md) |
| **Pakkeoversikt (README)** | Dokumentpakke for layout, navigasjon og MLOps mot GitHub Pages | [`AI_KOM_MLOps_og_Navigasjon_pakke/README.md`](./AI_KOM_MLOps_og_Navigasjon_pakke/README.md) |

---

## 16. M10 Oktober Month-End Staging & Ingestion Pack (`antigravity_m10_monthend_pack/`)

> **Overvåking av månedslutt (M10), staging-kø og saksbehandlerstyrt "Push Button" datafangst.**

| Modul / Fil | Beskrivelse & Formål | Filsti |
| :--- | :--- | :--- |
| **Month-End Monitoring & Staging Spec** | Dual-deteksjon (webhook/file-watcher), staging-kø og HITL trigger API | [`antigravity_m10_monthend_pack/ANTIGRAVITY_M10_MonthEnd_Monitoring_and_Staging.md`](./antigravity_m10_monthend_pack/ANTIGRAVITY_M10_MonthEnd_Monitoring_and_Staging.md) |
| **Fiktivt M10 Regnskap Datasett** | Realistisk testdatasett for oktober (Oppvekst, Helse, Byutvikling og IKT) | [`antigravity_m10_monthend_pack/M10_Oktober_2026_Regnskap_Fiktiv.csv`](./antigravity_m10_monthend_pack/M10_Oktober_2026_Regnskap_Fiktiv.csv) |

---

## 17. MVA & Balansekonto 2130 Test- og CI/CD-Pakker

> **Momskompensasjonsloven validering, balansekontroll konto 2130 og GitHub Actions automasjon.**

| Modul / Fil | Beskrivelse & Formål | Filsti |
| :--- | :--- | :--- |
| **MVA CI/CD Workflow** | GitHub Actions pipeline for automatisk validering av omposteringer og MVA-komp | [`.github/workflows/mva_validering_ci.yml`](./.github/workflows/mva_validering_ci.yml) |
| **MVA CI/CD Pipeline Guide** | Veileder for automatisk trigger, Python 3.12 runner og 90-dagers revisjonsartifact | [`docs/ANTIGRAVITY_MVA_CI_CD_Pipeline_Guide.md`](./docs/ANTIGRAVITY_MVA_CI_CD_Pipeline_Guide.md) |
| **MVA Balansekontroll Motor** | Python valideringsmotor med Tufte-rapportering og SHA-256 stempel | [`tools/mva_balanse_validator.py`](./tools/mva_balanse_validator.py) |
| **MVA Testrapport (Konto 2130)** | Siste godkjente valideringsrapport for korreksjonsfil med 0.00 differanse | [`reports/test_mva_balanse_2130_rapport.md`](./reports/test_mva_balanse_2130_rapport.md) |
| **MVA Pytest Integrasjon** | Enhetstest i repositoriets master-testsuite | [`tests/test_mva_balanse_2130.py`](./tests/test_mva_balanse_2130.py) |

---

## 18. Fast-Path Triage Router & App Engine (`app/`)

> **Sentral forespørselshåndterer som ruter mellom Direct MCP, RAG Lookup, Skill Workflow og Memory Context på < 2ms.**

| Modul / Fil | Beskrivelse & Formål | Filsti |
| :--- | :--- | :--- |
| **Triage Router Spesifikasjon** | Arkitektur, regex-mønstre, ruteringsregler og audit hashing | [`spesifikasjoner/ANTIGRAVITY_Triage_Router_Spec.md`](./spesifikasjoner/ANTIGRAVITY_Triage_Router_Spec.md) |
| **Triage Pydantic Modeller** | `TriageRequest`, `TriageDecision`, `TriageCategory`, `ExecutionPriority` | [`app/schemas/triage.py`](./app/schemas/triage.py) |
| **Triage Router Kjerne** | Fast-path regelbasert klassifiseringsmotor med SHA-256 audit stempel | [`app/core/triage_router.py`](./app/core/triage_router.py) |
| **Triage CLI Verktøy** | CLI-kommando for direkte rutingstest via `run_tool.py triage` | [`tools/triage_cli.py`](./tools/triage_cli.py) |
## 22. Økonomirådgiverens Håndbok & Vektor-DB Utvidelse (`erp_data/`, `tools/`, `index.html`)

> **30 kvalitetssikrede kunnskapsmoduler, FTS5 fulltekstsøk, Framsikt/delegeringsreglement og interaktiv FAQ-matrise i Office Hub.**

| Modul / Fil | Beskrivelse & Formål | Filsti |
| :--- | :--- | :--- |
| **Rådgiver Kunnskapsdatasett** | 30 strukturerte kunnskapsbiter for delegering, Framsikt, MVA, selvkost, tilskudd og HTA | [`erp_data/municipal_advisor_knowledge_chunks.json`](./erp_data/municipal_advisor_knowledge_chunks.json) |
| **Ingestion Motor (Vektor & Golden)** | Skript som injiserer og indekserer kunnskap i `kommune_golden_record.db` og `kommune_rag_store.db` | [`tools/ingest_municipal_advisor_knowledge.py`](./tools/ingest_municipal_advisor_knowledge.py) |
| **MCP & RAG Lovoppslag** | Utvidet `search_municipal_law` med FTS5 sparse search over selvkost, MVA og reglement | [`kommune-ai-guardrails/src/kommune_ai_guardrails/mcp_server.py`](./kommune-ai-guardrails/src/kommune_ai_guardrails/mcp_server.py) |
| **Office Hub FAQ Matrise** | Interaktivt oppslagsverk i `index.html` (Fane 4) med sanntidsfiltrering og hurtigkopiering | [`index.html`](./index.html) |
| **Advisor REST Endepunkter** | `GET /api/v1/advisor/faq` og `POST /api/v1/advisor/search` i Hub API-serveren | [`tools/hub_api_server.py`](./tools/hub_api_server.py) |
| **Pytest Integrasjonstest** | Enhetstest i `tests/test_project_master.py` som verifiserer kunnskapsbitene og søk | [`tests/test_project_master.py`](./tests/test_project_master.py) |

---

## 23. Kommunale Rådgiverkalkulatorer & Helårs Stresstest (`app/`, `tools/`, `index.html`)

> **Automatisert helårssimulering for alle 6 sektorer og 12 månedshjul-milepæler, samt 4 lovbaserte rådgiverkalkulatorer med SHA-256 forsegling.**

| Modul / Fil | Beskrivelse & Formål | Filsti |
| :--- | :--- | :--- |
| **Helårs Stresstestmotor** | 52 reelle rådgiverhendelser (Oppvekst, Helse, Byutvikling, VAR, Kultur, Finans) med benchmarking av Triage, RAG og SQLite WAL | [`tools/advisor_stresstest_engine.py`](./tools/advisor_stresstest_engine.py) |
| **Rådgiverkalkulator Pydantic Skjemaer** | Datakontrakter for NAV-refusjonsgap, KRS 4 Drift vs Inv, Selvkost VAR og 10-års MVA-justering | [`app/schemas/calculator.py`](./app/schemas/calculator.py) |
| **Kommunal Kalkulatortjeneste** | Presis forretnings- og lovlogikk (§ 14-6, KRS 4, Selvkostforskrift § 5/§ 7, Momskompensasjonsloven § 7) | [`app/services/municipal_calculator_service.py`](./app/services/municipal_calculator_service.py) |
| **Kalkulator CLI Runner** | CLI-kommando for rådgiverberegninger via `run_tool.py advisor-calc` og `run_tool.py advisor-stress` | [`tools/advisor_calculator_runner.py`](./tools/advisor_calculator_runner.py) |
| **Hub API Kalkulator-endepunkter** | `POST /api/v1/advisor/calculate/{nav-gap,krs4,selvkost,mva-10y}` | [`tools/hub_api_server.py`](./tools/hub_api_server.py) |
| **Office Hub Kalkulatorgrensesnitt** | 4 interaktive beregningsfaner i `index.html` (Fane 4) med live beregning, Tufte-merker og klient-side fallback | [`index.html#advisor-calculators-seksjon`](./index.html#advisor-calculators-seksjon) |
| **Pytest Integrasjonstester** | Master-testsuite for alle 4 beregningsmotorer og helårs stresstest | [`tests/test_project_master.py`](./tests/test_project_master.py) |







