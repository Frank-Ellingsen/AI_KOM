# 🏛️ Kristiansand Kommune — AI Project Controller Hub
## Master AI Context & Repository Architecture Guide (`AGENTS.md`)

Welcome to the **Kristiansand Kommune AI Project Controller Hub** codebase. This file serves as the canonical context engineering guide for all AI agents, pairing assistants, and automated workflows operating in this workspace.

---

## 1. Professional Context & Persona

* **Domain**: Norwegian Municipal Finance, Enterprise Performance Management (EPM), and Project Controlling.
* **Lead Controller**: **Frank Ellingsen** (Senior Financial Controller, Project Controller, and Business Intelligence Specialist).
* **Target Organization**: Kristiansand Kommune (6 Virksomhetsområder, 81 enheter, 7.24 milliarder NOK årsbudsjett).
* **Operational Goal**: Provide automated variance detection, rolling EAC/ETC forecasting, legal compliance checking (§ 14-5/§ 14-6/HTA § 4), and one-click reporting across PowerPoint (Bystyret), Word (saksfremlegg), Excel (FAST-modeller), and Power BI (.pbip).

---

## 2. Core Architectural Pillars

### A. Local-First Analytical Engine
* **DuckDB**: Preferred in-memory OLAP SQL engine for high-speed variance calculation, multi-dimensional groupings, and Parquet generation.
* **SQLite**: Transactional database, Star Schema Golden Record (`kommune_golden_record.db`), and local vector embeddings (`sqlite-vec`).
* **Local LLM Orchestration**: Local-first inference via **Ollama** (`llama3.2`, `mistral`, `qwen2.5-coder`) or **LM Studio**. Zero unredacted PII or financial data transmitted to external public APIs.

### B. Edward Tufte Data-Ink Ratio Standards
* **Zero Visual Clutter**: No vertical lines in tables, no drop shadows, no decorative badges, no 3D charts.
* **Muted Color Discipline**: Slate, navy, and white base palette; bright alert colors strictly reserved for active variances:
  * 🔴 **Red (`#c0392b`)**: Unfavorable variance / merforbruk ($CV < -500\text{k}$ kr or $CPI < 0.95$).
  * 🟡 **Amber (`#d35400`)**: Moderate observation ($0.95 \le CPI < 1.00$).
  * 🟢 **Green (`#27ae60`)**: In balance / favorable ($CPI \ge 1.00$).
* **Typography & Numbers**: Left-align text; right-align numbers; vertically align decimals; direct labeling on S-curves and sparklines.

### C. Legal & Governance Compliance
* **Kommuneloven § 14-5**: Realistic budget balance requirement. If $VAC < 0$ at year-end, Kommunedirektøren must submit a formal supplementary budget case to Bystyret.
* **Kommuneloven § 14-6**: Gross budgeting principle (bruttoprinsippet). Revenues (art 1600/1690) and expenses (art 1010/1020) must be recorded gross.
* **Kommuneloven § 13-1 & Forvaltningsloven § 17**: Utredningsplikt. Kommunedirektøren har personlig, lovpålagt ansvar for at saker som fremmes for folkevalgte organer er forsvarlig utredet; AI bistår kun med saksforberedelse under navngitt leders ansvar.
* **HTA § 4 & AML § 10-12**: Staffing reorganizations, long shifts (12.5h), and overtime require formal consultation protocols with employee unions (`MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL`).
* **Stage-Gate Port 9 (HITL)**: All AI recommendations require named human sign-off (APPROVED, MODIFIED, REJECTED) with cryptographic SHA-256 sealing jf. EU AI Act Art. 14 (se [maal_og_hensikt_human_in_the_loop.md](file:///C:/Users/frank/Desktop/AI_KOM/maal_og_hensikt_human_in_the_loop.md)).

### D. Token Economics & Execution: CLI vs. MCP
* **CLI-First for Agents**: Autonomous agents MUST prioritize unified CLI commands (`python tools/run_tool.py <command>`) over fine-grained MCP calls.
  * **Zero Schema Overhead**: Using a single execution tool avoids loading 2,000–5,000 tokens of MCP tool schemas into every prompt turn.
  * **Progressive Disclosure**: Detailed arguments and usage are resolved just-in-time via `--help` or lean skill playbooks.
  * **Tufte Payload Filtering**: CLI tools output concise, formatted summaries instead of dumping multi-megabyte raw JSON payloads into the conversation transcript.
* **MCP for External Clients**: Model Context Protocol servers (`kommune_ai_guardrails.mcp_server`) are strictly reserved for external zero-trust interactive UI clients (e.g. Streamlit sidebar chat, Excel add-ins), not for autonomous agent loop operations.

### E. The 5 Levels of AI Engineering Framework
Kristiansand Kommune AI Hub follows the canonical 5-layer AI Engineering hierarchy (see [ai_engineering_5_nivaaer_kristiansand.md](file:///C:/Users/frank/Desktop/AI_KOM/ai_engineering_5_nivaaer_kristiansand.md)):
1. **Level 1 (Prompt Engineering)**: Senior Controller persona, structured JSON schemas, and Chain-of-Thought reasoning.
2. **Level 2 (Context Engineering)**: Progressive disclosure (L1 metadata, L2 SOPs, L3 execution scripts), Hybrid RAG, and GDPR Port 4 PII masking.
3. **Level 3 (Harness Engineering)**: Isolated execution sandboxes, CLI-first execution, and OWASP LLM01/LLM02 prompt injection barriers.
4. **Level 4 (Loop Engineering)**: Self-correcting Evaluator-Optimizer cycles with 4 mandatory Quality Gates (§ 14-5, § 14-6, GDPR, Vedtak) and SHA-256 audit seals (see [loop_engineering_kristiansand.md](file:///C:/Users/frank/Desktop/AI_KOM/loop_engineering_kristiansand.md)).
5. **Level 5 (Graph Engineering)**: Statecharts and multi-agent DAG workflows (Triage Router $\rightarrow$ Controller $\rightarrow$ Juridisk $\rightarrow$ Revisjon $\rightarrow$ Stage-Gate Port 9 HITL).


---

## 3. Customization Architecture (`.agents/`)

This repository is fully configured for Antigravity native progressive disclosure:

```
.agents/
├── rules/
│   ├── 01_tufte_data_ink_rules.md              # Edward Tufte styling guidelines
│   ├── 02_project_controlling_evm_rules.md      # EVM formulas, CPI, EAC, and statutory thresholds
│   └── 03_local_first_ai_architecture_rules.md  # Data locality, DuckDB/SQLite, and PII protection
└── skills/
    ├── audit-governance/SKILL.md               # Audit trail, SHA-256 sealing, control checks
    ├── data-integration-etl/SKILL.md           # Visma ERP & Framsikt ETL pipeline
    ├── document-parser/SKILL.md                # PDF, Word (.docx), and Excel parsing
    ├── duckdb-analytics/SKILL.md               # In-memory OLAP analytics & Parquet export
    ├── epm-variance-detect/SKILL.md            # Z-score variance detection and outlier flags
    ├── excel-mcp/SKILL.md                      # MCP integration for Excel spreadsheets
    ├── excel-python-fpna/SKILL.md              # FAST standard financial modeling via Python
    ├── kostra-analyzer/SKILL.md                # KOSTRA art & function classification
    ├── llm-gateway/SKILL.md                    # Multi-model LLM routing (Ollama / Flash)
    ├── ollama-api-bridge/SKILL.md              # Local Ollama client orchestration
    ├── pii-guardrails/SKILL.md                 # PII scrubbing and anonymization
    ├── powerbi-fabric/SKILL.md                 # Power BI DAX modeling & .pbip management
    ├── predictive-forecasting/SKILL.md         # Monte Carlo P10/P50/P90 & EVM forecasting
    ├── python-sandbox/SKILL.md                 # Safe isolated execution of analysis scripts
    ├── rag-legal-query/SKILL.md                # Vector search over municipal regulations
    ├── saksfremlegg-generator/SKILL.md         # Formelt saksnotat for Bystyret / Formannskapet
    ├── sqlite-vec-executor/SKILL.md            # sqlite-vec vector database querying
    ├── streamlit-builder/SKILL.md              # Internal BI dashboards in Streamlit
    └── visual-data-communication/SKILL.md      # Tufte visualizations, sparklines, waterfalls
```

---

## 4. Repository Directory Taxonomy

| Directory | Purpose | Key Contents |
| :--- | :--- | :--- |
| **`.agents/`** | Antigravity AI Customizations | 19 native skills, 3 rule files, progressive disclosure |
| **`agenter/`** | 15 Agent Role Specifications | Detaljerte roller for ETL, DAX, RAG, Controller, Evaluering (13), Database (14), AI Engineering (15) |
| **`AI_KOM_MLOps_og_Navigasjon_pakke/`** | Layout, Navigasjon & MLOps Governance | 4-faset navigasjonsstruktur (Min Enhet, Sektor, Controller, Veiledere), Data Lineage (SHA-256) |
| **`ai-implementeringspakke-okonomi/`** | Municipal AI Implementation Guide | 9-part handbook (modul 00–08) for governance, ROI & roadmap |
| **`antigravity_backend_module_pakke/`** | Antigravity Core Backend Engine (v2.4) | FastAPI router, Polars/DuckDB data engine, Celery task queue, Qdrant/RAG, Stage-Gate Port 9 audit |
| **`antigravity_cash_management_pakke/`** | Cash Management & Likviditetsstyring | M11 rullende likviditetsprognose, kassakredittramme (150M kr) og What-If scenarier |
| **`antigravity_m10_monthend_pack/`** | M10 Month-End Monitoring & Ingestion Pack | Staging queue, webhook/file-watcher, push-button trigger, fiktivt M10 regnskap |
| **`antigravity_mva_ci_actions_pakke/`** | MVA CI/CD GitHub Actions Pack | Automatisk GitHub Actions CI/CD workflow (`mva_validering_ci.yml`) og pipeline guide |
| **`antigravity_mva_test_pakke/`** | MVA & Balansekonto 2130 Test Pack | Momskompensasjonsloven validering, balansekontroll konto 2130, testrapport generator |
| **`antigravity_report_export_pakke/`** | Bystyret & Formannskap PPTX Export | Automatisk generering av 16:9 widescreen presentasjoner med Tufte KPI-kort |
| **`antigravity_top3_kpi_visualisering_pakke/`** | Top 3 Kommunale Nøkkeltall & Hierarki | Takometer (Gauge) visning for Netto drift, Disposisjonsfond, Netto lånegjeld |
| **`antigravity-ms-pilot/`** | M365 Copilot & Antigravity Subproject | Subproject Python motor (`src/`), `run_pilot.py`, PII-vask, evaluatorer og tester |
| **`app/`** | Web Applications & Core Backend | Fast-Path Triage Router (`app/core/`), Pydantic modeller (`app/schemas/`), Hub backend (`app/services/`) |
| **`archive/`** | Historical Backups & Scratch | `backups/`, legacy exports |
| **`bruker-guides/`** | Operational Handbooks & Calendars | Budsjettansvarlige katalog, månedshjul, styringskalender 2026 |
| **`budsjett-framsikt/`** | Framsikt EPM & KOSTRA Master Package | `budsjettering-kristiansand-kommune.md`, `lonnsbudsjettering-kristiansand-framsikt.md`, driftsarter, selvkost |
| **`data/`** | Reposting & Staging Artifacts | `data/repostings/` (Ompostering korreksjonsfiler, MVA-avstemminger) |
| **`docs/`** | Unified Documentation | Architecture, user guides, specifications, and PDF publications |
| **`erp_data/`** | Municipal Data Lake | `kommune_golden_record.db`, staging queue, Visma ERP CSVs, Golden Evaluation Dataset |
| **`excel/`** | Financial Modeling | FAST models, `Kommune_Project_Controller_Reporting_2026.xlsx` |
| **`generic-ai-pilot-pakke/`** | Vendor-Neutral Enterprise AI Pilot | Generisk malverk (`enterprise-ai-pilot/`), DAX, prompts, evals, målarkitektur |
| **`mlops-implementeringspakke/`** | MLOps & LLMOps Procurement Package | 6-part specification for municipal AI operations, observability & tenders |
| **`mvp-pilot/`** | Bo og Miljø Operational Pilot | Streamlit interactive app, DuckDB analytics, EAC engine |
| **`powerbi/`** | Power BI Enterprise Assets | `pbi_reporting_project.pbip`, DAX library, Teams RLS, semantic models |
| **`powerpoint/`** | Presentation Decks | 16:9 executive decks for Bystyret, Kommunedirektøren, Oppvekst |
| **`reports/`** | Published Reports & Nettbank | Kontoutskrifter (81 units), executive briefings, waterfall charts, Bystyret PPTX |
| **`revisjon-og-kontroll/`** | Audit & Control Standards | Checklists for Kommunerevisjonen, tertialnotater, § 14-5 |
| **`scratch/`** | Scratch Scripts & Migration Utilities | One-off helper scripts, debug scripts, integration tools |
| **`spesifikasjoner/`** | Technical Specifications | Triage Router, Office Hub V2, Gemini MCP Chat, Predictive Engine specs |
| **`loop_engineering_kristiansand.md`** | Loop Engineering Spec (Lag 4) | Evaluator-Optimizer dualitet, 4 kvalitetsporter (§ 14-5, § 14-6, GDPR, Vedtak), SHA-256 |
| **`ai_engineering_5_nivaaer_kristiansand.md`** | AI Engineering Framework (5 Nivåer) | Komplett hierarki: Prompt, Context, Harness, Loop og Graph Engineering |
| **`maal_og_hensikt_human_in_the_loop.md`** | Mål, Hensikt & HITL Governance | EU AI Act Art. 14, § 13-1, § 14-5/6, HTA § 4 og Stage-Gate Port 9 sign-off |
| **`templates/`** | Municipal Templates (18 pairs) | Dual format: .docx/.xlsx for production, .md for hub preview |
| **`tests/`** | Master Test Suite | Pytest test files (70+ tester på tvers av master og piloter) |
| **`tools/`** | Operational CLI Tools | Python engines (`run_tool.py`, `loop_engine.py`, `evaluation_runner.py`, `database_runner.py`, `ai_engineering_runner.py`, etc.) |
| **`word/`** | Formal Municipal Notes | Generated Word documents (.docx) for administrative levels 1–3 |

---

## 5. Quick Commands & Operations

* **Run Full Hub**: Launch `index.html` in browser or run `python tools/hub_api_server.py`.
* **Run Loop Engineering (Lag 4)**: `python tools/run_tool.py loop --sector "Helse og mestring" --deficit 8.85` (Evaluator-Optimizer løkke med 4 kvalitetsporter og SHA-256 forsegling).
* **Run Zero-Guide UI Prototype v2**: `python tools/run_tool.py ui-v2` (Streamlit app med unntakstriage, Evaluator-Optimizer løkke og Golden Exemplar SQLite store).
* **Run Evaluation & QA (Agent 13)**: `python tools/run_tool.py eval --gate` (90 % CI/CD port), `--include-exemplars` (inkluderer HITL gulleksempler fra SQLite), eller `--sync-exemplars`.
* **Run Database & Schema (Agent 14)**: `python tools/run_tool.py db --inspect-schema` eller `--query "..."`.
* **Run AI Engineering (Agent 15)**: `python tools/run_tool.py ai-eng --status` eller `--benchmark`.
* **Run Cash Management**: `python tools/run_tool.py cash --forecast` eller `--compliance`.
* **Run Top 3 KPIs**: `python tools/run_tool.py kpi` eller `--sector OMR-02`.
* **Export Bystyret Report**: `python tools/run_tool.py pptx`.
* **Run Predictive Forecast**: `python tools/predictive_forecasting_engine.py --mode both`.
* **Run Audit Validator**: `python tools/audit_revisjon_validator.py`.
* **Run M10 Month-End Ingestion**: `python tools/run_tool.py m10-ingest --status` eller `--execute`.
* **Run MVA Balansekontroll**: `python tools/run_tool.py mva`.
* **Run Fast-Path Triage Router**: `python tools/run_tool.py triage "Hva sier § 14-5?"`.
* **Run Advisor Knowledge Ingest**: `python tools/run_tool.py advisor-ingest` (oppdaterer rådgivermoduler i Vektor-DB).
* **Run Advisor Decision Calculators**: `python tools/run_tool.py advisor-calc --calc nav-gap` / `--calc krs4` / `--calc selvkost` / `--calc mva-10y`.
* **Run Advisor Full-Year Stress Test**: `python tools/run_tool.py advisor-stress` (helårssimulering av 52 rådgiverhendelser på tvers av 6 sektorer og 12 måneder).
* **Unified Tool Runner**: `python tools/run_tool.py --help`.
* **Run Master Test Suite**: `pytest -v` (kjører samtlige 75+ tester på tvers av master og piloter).
