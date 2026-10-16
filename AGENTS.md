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
* **HTA § 4 & AML § 10-12**: Staffing reorganizations, long shifts (12.5h), and overtime require formal consultation protocols with employee unions.
* **Stage-Gate Port 9 (HITL)**: All AI recommendations require named human sign-off (APPROVED, MODIFIED, REJECTED) with cryptographic SHA-256 sealing.

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
| **`agenter/`** | 12 Agent Role Specifications | Detailed roles for ETL, DAX, RAG, Controller, etc. |
| **`antigravity-ms-pilot/`** | M365 Copilot & Antigravity Subproject | Subproject Python motor (`src/`), `run_pilot.py`, PII-vask, evaluatorer og tester |
| **`app/`** | Web Applications & APIs | FastAPI server, Streamlit pilots, UI components |
| **`archive/`** | Historical Backups & Scratch | `backups/`, `scratch/`, legacy exports |
| **`budsjett-framsikt/`** | Framsikt EPM & KOSTRA Master Package | `budsjettering-kristiansand-kommune.md`, `lonnsbudsjettering-kristiansand-framsikt.md`, `driftsarter-og-selvkost-alle-omrader-framsikt.md`, `kostra-artskontoer-konteringsregler-framsikt.md` |
| **`docs/`** | Unified Documentation | Architecture, user guides, specifications, and PDF publications |
| **`erp_data/`** | Municipal Data Lake | `kommune_golden_record.db`, Visma ERP CSVs, Framsikt extracts |
| **`excel/`** | Financial Modeling | FAST models, `Kommune_Project_Controller_Reporting_2026.xlsx` |
| **`generic-ai-pilot-pakke/`** | Vendor-Neutral Enterprise AI Pilot | Generisk malverk (`enterprise-ai-pilot/`), DAX, prompts, evals, målarkitektur |
| **`powerbi/`** | Power BI Enterprise Assets | `pbi_reporting_project.pbip`, DAX library, semantic models |
| **`powerpoint/`** | Presentation Decks | 16:9 executive decks for Bystyret, Kommunedirektøren, Oppvekst |
| **`reports/`** | Published Reports | Executive briefings, waterfall charts, status reports |
| **`templates/`** | Municipal Templates | Word (.docx) & Markdown templates for meetings and saksfremlegg |
| **`tools/`** | Operational CLI Tools | Python engines (`predictive_forecasting_engine.py`, `run_tool.py`) |
| **`word/`** | Formal Municipal Notes | Generated Word documents (.docx) for administrative levels 1–3 |

---

## 5. Quick Commands & Operations

* **Run Full Hub**: Launch `index.html` in browser or run `python tools/hub_api_server.py`.
* **Run Predictive Forecast**: `python tools/predictive_forecasting_engine.py --mode both`.
* **Run Audit Validator**: `python tools/audit_revisjon_validator.py`.
* **Unified Tool Runner**: `python tools/run_tool.py --help`.
* **Run Test Suite**: `pytest -v` (kjører samtlige 32 tester på tvers av master og subprosjekter).
