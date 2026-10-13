# Antigravity EPM Framework & Agentic AI Architecture
## Complete End-to-End System Documentation & Operational Playbook
**Municipality:** Kristiansand Kommune  
**Department:** Økonomi og Virksomhetsstyring  
**Target Environment:** Single Source of Truth (SQLite Golden Record), Power BI, Microsoft Excel, Streamlit HITL Portal  
**Compliance Standards:** EU AI Act (Art. 10, 13, 14, 27 FRIA), GDPR (Art. 35 DPIA), Kommuneloven (§§ 13-1, 14-4, 14-5, 14-6), KOSTRA Kontoplan 2026  

---

## 1. System Overview & Architecture Diagram

The **Antigravity EPM Framework** translates overreaching municipal AI principles and financial regulations into an operative, glass-box performance management ecosystem. It bridges raw data extractions from Visma Enterprise (schools), Agresso (care homes), Framsikt, and SSB into a unified **SQLite Golden Record** (`kristiansand_golden_record.db`).

### High-Level Workflow Architecture

```
[ KILDEDATA: ERP & CSV ] ──> Visma (Skole) / Agresso (Boenhet) / Framsikt / SSB API
                                       │
                                       ▼
[ ETL & DEDUPLICATION ]  ──> SHA-256 Deterministic Hashing & KOSTRA Mapping
                                       │
                                       ▼
[ GOLDEN RECORD DB ]     ──> SQLite / Fabric Lakehouse (Star Schema: Fact_Regnskap)
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
[ GLASS-BOX RAG ENGINE ]                                [ POWER BI & EXCEL ]
(Retrieves KOSTRA Rules & Tertial Notes)                (DAX Time Intelligence & Matrix)
            │                                                     │
            ▼                                                     │
[ HITL CONTROLLER PORTAL ] <──────────────────────────────────────┘
(Streamlit / Power Apps UI: Review Reasoning Chain & Confidence)
            │
            ▼
[ AUDIT LOG & SIGN-OFF ] ──> Immutable Audit_AI_Actions Table (EU AI Act & GDPR)
            │
            ▼
[ MULTI-LEVEL REPORTING ] ──> 5-Tier Tailored Outputs (Unit Head to Bystyret)
```

---

## 2. Single Source of Truth (SSOT) & KOSTRA Golden Record

All reporting and AI analysis query a single, canonical database structure (`kristiansand_golden_record.db`).

### A. Database Schema Definition (DDL)

```sql
-- Fact_Regnskap: Canonical Transaction Table
CREATE TABLE IF NOT EXISTS Fact_Regnskap (
    transaksjon_id TEXT PRIMARY KEY,           -- SHA-256 Hash ID
    kilde_system TEXT NOT NULL,                -- Visma / Agresso / Framsikt
    kontoklasse_id INTEGER NOT NULL,           -- 1 = Drift, 2 = Investering
    funksjon_key INTEGER NOT NULL,             -- FK to Dim_Funksjon (KOSTRA)
    art_key INTEGER NOT NULL,                  -- FK to Dim_Art (KOSTRA)
    ansvar_key INTEGER NOT NULL,               -- FK to Dim_Ansvar (Municipal Hierarchy)
    dato_key INTEGER NOT NULL,                 -- YYYYMMDD
    belop REAL NOT NULL,                       -- Raw amount
    korrigert_belop REAL NOT NULL,             -- Sign-adjusted for gross principle (+/-)
    budsjett_belop REAL DEFAULT 0.0,
    avvik_belop REAL GENERATED ALWAYS AS (belop - budsjett_belop) VIRTUAL,
    sist_oppdatert TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funksjon_key) REFERENCES Dim_Funksjon(funksjon_key),
    FOREIGN KEY (art_key) REFERENCES Dim_Art(art_key),
    FOREIGN KEY (ansvar_key) REFERENCES Dim_Ansvar(ansvar_key)
);

-- Audit_AI_Actions: Compliance & HITL Sign-off Log
CREATE TABLE IF NOT EXISTS Audit_AI_Actions (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    agent_navn TEXT NOT NULL,
    anomali_detektert TEXT NOT NULL,
    konfidens_score REAL NOT NULL,
    foreslaatt_tiltak TEXT NOT NULL,
    hitl_status TEXT NOT NULL CHECK (hitl_status IN ('PENDING', 'APPROVED', 'REJECTED', 'MODIFIED')),
    saksbehandler_id TEXT,
    begrunnelse TEXT,
    stage_gate_referanse TEXT NOT NULL
);
```

### B. Deduplication Logic (SHA-256 Hashing)
To prevent duplicate rows when re-importing monthly CSVs from units, a deterministic SHA-256 hash is generated per row:
$$	ext{Txn\_ID} = 	ext{SHA256}(	ext{Kilde} \parallel 	ext{Dato} \parallel 	ext{Ansvar} \parallel 	ext{Funksjon} \parallel 	ext{Art} \parallel 	ext{Beløp})[:16]$$

---

## 3. The 8 Agent Skill Modules (`.agent/skills/`)

The framework deploys 8 specialized agent roles, configured via Markdown skill instructions:

1. **`01_data_integration_etl_agent.md`**: Ingests, cleans, and maps heterogeneous CSVs/APIs to KOSTRA dimensions.
2. **`02_bi_dax_modeler_agent.md`**: Builds Star Schema, Query Folding, and DAX measures (`ISINSCOPE`, `EOY Årsprognose`).
3. **`03_predictive_anomaly_agent.md`**: Detects cost anomalies (Z-score > 2.0) 60–90 days ahead of formal tertial reports.
4. **`04_prescriptive_hitl_agent.md`**: Generates legal micro-actions and manages Human-in-the-Loop logging.
5. **`05_ethics_governance_gatekeeper_agent.md`**: Enforces the 10-Stage-Gate framework, FRIA (EU AI Act Art. 27), DPIA, and DPO veto powers.
6. **`06_executive_report_ghostwriter_agent.md`**: Drafts formal municipal memos (*Saksfremlegg*) to the CFO, Municipal Director, and Bystyret.
7. **`07_excel_powerbi_reporting_expert_agent.md`**: Enforces FAST Financial Modelling Standards, WCAG 2.1 AA accessibility, and FT Visual Vocabulary.
8. **`08_multilevel_stakeholder_reporting_agent.md`**: Tailors outputs to 5 distinct municipal stakeholder tiers.

---

## 4. Glass-Box RAG Engine & Power Query Integration (`fxOpenAI_RAG.m`)

To prevent "black-box" hallucinations, AI calculations in Excel and Power BI execute on-demand via a Power Query custom function (`fxOpenAI_RAG.m`).

### Key Features:
* **Manual Execution:** Runs strictly when the user refreshes Power Query or clicks "Run AI Diagnosis" (never auto-recalculates dynamically).
* **RAG Context Grounding:** Combines transaction data with retrieved passages from KOSTRA 2026 guidelines, local financial regulations (*Økonomireglement*), and 1. tertialrapport 2026 notes.
* **Glass-Box Output Schema:** Mandates strict JSON output with `reasoning_chain`, `confidence_score`, and `governance_reference`.

---

## 5. Human-in-the-Loop (HITL) Controller Portal (`hitl_writeback_ui.py`)

The Streamlit web application (`hitl_writeback_ui.py`) serves as the primary controller workbench.

### Workflow Steps:
1. **Anomaly Detection Display:** Shows flagged variances (e.g. Art 1090 +kr 117,000 at *Kommunal Boenhet*, Art 1020 +kr 47,000 at *Kommunal Skole*).
2. **Glass-Box Transparency Panel:** Displays the step-by-step reasoning chain, model confidence score (e.g. 92%), and regulatory references.
3. **Human Sign-off Form:** The budget controller selects `APPROVED`, `MODIFIED`, or `REJECTED` and inputs manual notes.
4. **Audit Log Write-back:** Writes the decision, user ID, timestamp, and notes permanently into `Audit_AI_Actions`.

---

## 6. Stage-Gate Decision Matrix & Governance Framework

The AI lifecycle is governed by 10 sequential Decision Gates:

| Gate | Phase | Key Requirement | Role / Approval |
| :--- | :--- | :--- | :--- |
| **Gate 1** | Organizational Foundation | AI literacy & cross-functional team | CFO / IT Director |
| **Gate 2** | Problem Definition | Need alignment & non-AI baseline check | Financial Advisor |
| **Gate 3** | Ethical Screening | Ethical self-assessment & HITL commitment | DPO / Ethics Committee |
| **Gate 4** | Budget & Capacity | Business case & cloud cost clearance | CFO / Municipal Director |
| **Gate 5** | Vendor & Procurement | Lock-in prevention & data ownership | Procurement Head |
| **Gate 6** | Sandbox Testing | Testing with historical/anonymized KOSTRA data | Data Engineer |
| **Gate 7** | Risk Assessment | Mandatory **FRIA** (EU AI Act Art. 27) & **DPIA** (GDPR) | DPO / Legal Counsel (Veto) |
| **Gate 8** | Regulatory Anchoring | Public Algorithm Register entry (Eurocities v0.3.1) | Municipal Director |
| **Gate 9** | Production Operation | Model drift monitoring & parallel runs | Lead Controller |
| **Gate 10** | Evaluation & Sunsetting | Annual benefit measurement or system termination | CFO / Bystyret |

---

## 7. Multi-Level Stakeholder Reporting Framework

Data and narratives are customized across 5 municipal tiers:

1. **Unit Leader (School Head / Care Home Head):** Operative variance control on Arts 1010, 1020, 1090, 1690 via Power BI Unit Cards & Excel Action Lists.
2. **Sector Head (Oppvekst / Helse & Mestring):** Cross-unit balancing, KOSTRA function matrices (Functions 202, 253, 330), and sector EOY forecasts.
3. **Chief Financial Officer (CFO):** Total EPM, Corrected Net Operating Result (target $\ge 1.0\%$), liquidity, interest rates, and ERP Visma tracking.
4. **Municipal Director (Kommunedirektør):** Enterprise risk landscape, debt ceiling (8.8 mrd kr), HØP 2027–2030 alignment, and strategic trade-offs.
5. **Politicians (Formannskapet / Bystyret):** Formal decision memos (*Saksfremlegg* jf. Kommuneloven § 14-5), plain-language summaries, and political resolutions.

---

## 8. Summary of Workspace Deliverables

All components of this architecture have been compiled and published to the Studio panel:

* **Diagram Image:** `epm_workflow_diagram.png` (High-res 16:9 architecture visual)
* **SQLite Database:** `kristiansand_golden_record.db` (Golden Record DB with 1. Tertial 2026 data & Audit Trail)
* **Pipeline Script:** `epm_agentic_pipeline.py` (Python ETL & pipeline runner)
* **HITL Web App:** `hitl_writeback_ui.py` (Streamlit controller interface)
* **Power Query M Script:** `fxOpenAI_RAG.m` (RAG-grounded Power Query function)
* **Agent Skills:** `01_...md` through `08_...md` (8 specialized agent skill files)
* **Executive Documents:** `saksfremlegg_epm_okonomidirektor.docx`, `use_case_kristiansand_kommune-v4.docx`
