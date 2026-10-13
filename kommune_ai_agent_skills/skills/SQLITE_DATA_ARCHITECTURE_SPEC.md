# 🏛️ Generic Municipal SQLite Data Architecture Specification

> **A Modular, Multi-Source Star-Schema & Vector Store Architecture for Municipal EPM, AI-RAG, and Audit Governance**

---

## 1. Executive Summary & Core Principles

This specification defines a **generic, production-ready SQLite database architecture** designed to combine heterogeneous data streams—including Enterprise Resource Planning (ERP), Enterprise Performance Management (EPM), flat files (CSV/Excel), and national standards (KOSTRA/SSB)—into a single, unified, local "Golden Record" database.

### Key Architectural Principles:
1. **Unified Storage (`Golden Record`):** Structured financial transactions, dimension hierarchies, unstructured text chunks (`sqlite-vec` + `FTS5`), and immutable audit logs (`SHA-256`) reside in a single SQLite database (`kommune_golden_record.db`).
2. **Star Schema Data Modeling:** Clear separation between high-volume quantitative facts (`Fact_Regnskap`, `Fact_Budsjett`) and shared conformed dimensions (`Dim_Funksjon`, `Dim_Art`, `Dim_Ansvar`, `Dim_Dato`).
3. **Automated PII Masking (Stage-Gate Port 4):** All incoming data passes through an automated sanitization layer to strip personally identifiable information (PII) before vectorization or LLM retrieval.
4. **Idempotent Ingestion & Deduplication:** Transactions are assigned a cryptographic hash ID (`SHA-256`), enabling repeatable, conflict-free batch processing (`INSERT OR REPLACE`).
5. **Immutable Audit Governance (Stage-Gate Port 9):** Every AI query, retrieved chunk set, and human-in-the-loop action is logged with an immutable hash for municipal audit compliance.

---

## 2. Multi-Tiered Data Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        RAW DATA SOURCES                                │
│   Visma / ERP  │  Framsikt / EPM  │  CSV / Excel  │  KOSTRA / SSB API  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 1. STAGING LAYER (stg_*)                                              │
│ - Raw Schema Preservation                                              │
│ - PII Anonymization & Sanitization                                      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. CORE STAR SCHEMA (Golden Record)                                    │
│ - Fact_Regnskap  (Actual Expenditures)                                 │
│ - Fact_Budsjett  (Approved & Adjusted Budgets)                         │
│ - Conformed Dimensions (Dim_Funksjon, Dim_Art, Dim_Ansvar, Dim_Dato)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                   ┌────────────────┴────────────────┐
                   ▼                                 ▼
┌────────────────────────────────────┐ ┌─────────────────────────────────┐
│ 3. VECTOR & TEXT SEARCH STORE      │ │ 4. AUDIT & GOVERNANCE LOGS      │
│ - legal_chunks (Text + Metadata)   │ │ - Audit_AI_Actions              │
│ - vec_legal_chunks (sqlite-vec 384)│ │ - SHA-256 Hash Verification     │
│ - legal_fts (FTS5 BM25 Engine)     │ │ - Human-in-the-Loop Tracking    │
└────────────────────────────────────┘ └─────────────────────────────────┘
```

---

## 3. SQL DDL Schema Specification

### A. Staging Layer (Raw Multi-Source Ingestion)

```sql
-- Staging table for ERP Accounting Exports
CREATE TABLE IF NOT EXISTS stg_erp_transactions (
    raw_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_system TEXT NOT NULL,
    voucher_number TEXT,
    accounting_date TEXT,
    account_code TEXT,
    function_code TEXT,
    cost_center_code TEXT,
    amount REAL,
    description TEXT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Staging table for EPM Budget & Forecast Data
CREATE TABLE IF NOT EXISTS stg_epm_budget (
    raw_id INTEGER PRIMARY KEY AUTOINCREMENT,
    budget_version TEXT NOT NULL, -- e.g., 'ORIGINAL', 'TERTIAL_1', 'TERTIAL_2'
    fiscal_year INTEGER NOT NULL,
    function_code TEXT NOT NULL,
    art_code TEXT NOT NULL,
    cost_center_code TEXT NOT NULL,
    budget_amount REAL NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### B. Core Conformed Dimension Tables

```sql
-- Dimension: KOSTRA Functions (SSB / Municipal Services)
CREATE TABLE IF NOT EXISTS Dim_Funksjon (
    funksjon_kode TEXT PRIMARY KEY,
    funksjon_navn TEXT NOT NULL,
    tjenesteomrade TEXT NOT NULL, -- e.g., 'Oppvekst', 'Helse og Omsorg'
    hovedfunksjon TEXT NOT NULL
);

-- Dimension: KOSTRA Object / Expense Types (Arter)
CREATE TABLE IF NOT EXISTS Dim_Art (
    art_kode TEXT PRIMARY KEY,
    art_navn TEXT NOT NULL,
    art_gruppe TEXT NOT NULL      -- e.g., 'Lønn', 'Kjøp av tjenester', 'Finans'
);

-- Dimension: Organizational Structure (Cost Center / Ansvar)
CREATE TABLE IF NOT EXISTS Dim_Ansvar (
    ansvar_kode TEXT PRIMARY KEY,
    enhet_navn TEXT NOT NULL,
    sektor TEXT NOT NULL,
    leder_stilling TEXT
);

-- Dimension: Calendar & Municipal Governance Cycle (Dato / Årshjul)
CREATE TABLE IF NOT EXISTS Dim_Dato (
    dato_key TEXT PRIMARY KEY,    -- YYYY-MM-DD
    aar INTEGER NOT NULL,
    maned INTEGER NOT NULL,
    kvartal TEXT NOT NULL,
    tertial TEXT NOT NULL,        -- 'T1', 'T2', 'T3'
    arshjul_fase TEXT             -- e.g., '1. Tertialrapportering', 'Budsjettbehandling'
);
```

---

### C. Core Fact Tables

```sql
-- Fact Table: General Ledger Transactions (Actuals)
CREATE TABLE IF NOT EXISTS Fact_Regnskap (
    transaksjon_hash TEXT PRIMARY KEY, -- SHA-256 hash of core transaction fields
    kilde_system TEXT NOT NULL,        -- 'VISMA_ERP', 'CSV_BATCH', etc.
    kontoklasse_id INTEGER NOT NULL,   -- 1=Drift, 2=Investering
    funksjon_key TEXT NOT NULL,
    art_key TEXT NOT NULL,
    ansvar_key TEXT NOT NULL,
    dato_key TEXT NOT NULL,
    belop REAL NOT NULL,
    sist_oppdatert TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funksjon_key) REFERENCES Dim_Funksjon(funksjon_kode),
    FOREIGN KEY (art_key) REFERENCES Dim_Art(art_kode),
    FOREIGN KEY (ansvar_key) REFERENCES Dim_Ansvar(ansvar_kode),
    FOREIGN KEY (dato_key) REFERENCES Dim_Dato(dato_key)
);

-- Fact Table: Budgets & Financial Forecasts
CREATE TABLE IF NOT EXISTS Fact_Budsjett (
    budsjett_hash TEXT PRIMARY KEY,    -- SHA-256 hash
    budsjett_type TEXT NOT NULL,       -- 'VEDTATT', 'TERTIAL_1', 'TERTIAL_2', 'PROGNOSE'
    aar INTEGER NOT NULL,
    funksjon_key TEXT NOT NULL,
    art_key TEXT NOT NULL,
    ansvar_key TEXT NOT NULL,
    budsjett_belop REAL NOT NULL,
    sist_oppdatert TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funksjon_key) REFERENCES Dim_Funksjon(funksjon_kode),
    FOREIGN KEY (art_key) REFERENCES Dim_Art(art_kode),
    FOREIGN KEY (ansvar_key) REFERENCES Dim_Ansvar(ansvar_kode)
);
```

---

### D. RAG Vector Engine & Full-Text Search Schema

```sql
-- Text Chunks & Metadata
CREATE TABLE IF NOT EXISTS legal_chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file TEXT NOT NULL,
    category TEXT NOT NULL,      -- 'Kommuneloven', 'KOSTRA', 'Økonomireglement'
    section_ref TEXT,           -- '§ 14-5'
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Full-Text Search Table (FTS5 BM25 Engine)
CREATE VIRTUAL TABLE IF NOT EXISTS legal_fts USING fts5(
    title,
    content,
    section_ref,
    content='legal_chunks',
    content_rowid='id'
);

-- Vector Embeddings Store (sqlite-vec 384 Dimensions)
-- Note: Activated via sqlite-vec extension
```

---

### E. Governance & Audit Trail Schema (Stage-Gate Port 9)

```sql
-- Immutable Audit Log for Municipal Revision & Control Committee
CREATE TABLE IF NOT EXISTS Audit_AI_Actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_query TEXT NOT NULL,
    retrieved_chunk_ids TEXT NOT NULL, -- JSON array of chunk IDs
    llm_response TEXT NOT NULL,
    human_decision TEXT DEFAULT 'APPROVED', -- 'APPROVED', 'MODIFIED', 'REJECTED'
    sha256_hash TEXT NOT NULL,         -- Cryptographic signature
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. Generic Ingestion & Deduplication Logic

When ingesting CSVs, ERP, or EPM data:
1. **PII Masking:** Sanitize personal data (SSNs, full names) from transaction descriptions.
2. **SHA-256 Fingerprinting:** Generate `tx_hash = sha256(source + date + function + art + cost_center + amount)`.
3. **Idempotent Storage:** Insert using `INSERT OR REPLACE INTO Fact_Regnskap` to ensure duplicate batch uploads are safely handled.

---

## 5. Analytical Query Pattern (Actual vs. Budget Variance)

```sql
SELECT 
    f.tjenesteomrade,
    r.funksjon_key,
    df.funksjon_navn,
    SUM(r.belop) AS faktisk_forbruk,
    SUM(b.budsjett_belop) AS vedtatt_budsjett,
    (SUM(r.belop) - SUM(b.budsjett_belop)) AS avvik_kroner,
    ROUND(((SUM(r.belop) - SUM(b.budsjett_belop)) / NULLIF(SUM(b.budsjett_belop), 0)) * 100, 2) AS avvik_prosent
FROM Fact_Regnskap r
LEFT JOIN Fact_Budsjett b 
    ON r.funksjon_key = b.funksjon_key 
   AND r.art_key = b.art_key 
   AND r.ansvar_key = b.ansvar_key
JOIN Dim_Funksjon df ON r.funksjon_key = df.funksjon_kode
GROUP BY f.tjenesteomrade, r.funksjon_key, df.funksjon_navn
ORDER BY avvik_kroner DESC;
```

---

## 6. Key Benefits

- **Zero External Dependencies:** Single-file SQLite database easy to back up, share, and query locally.
- **Hybrid Search Capabilities:** Seamlessly blends structured financial reporting (Star Schema) with unstructured document QA (sqlite-vec RAG).
- **Audit Compliance:** SHA-256 hashed audit log satisfies Municipal Auditor requirements (Stage-Gate Port 9).
