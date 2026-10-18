# Kristiansand Kommune Control Office Hub (AI_KOM) Optimization Blueprint

An architectural and technical optimization plan for the Kristiansand Kommune Control Office Hub & AI Assistant (`AI_KOM`).

---

## 1. Executive Summary & Core Objectives

The **AI_KOM** project integrates municipal financial controlling (*Kommuneloven § 14-5*, *KOSTRA*, *EVM*), Glass-Box RAG (`sqlite-vec`), DuckDB financial analytics, and Stage-Gate Port 9 AI governance.

To scale the platform to production across 6 municipal sectors and 81 organizational units, this document outlines five key optimization domains:
1. RAG & Retrieval Performance
2. Data Engineering & OLAP Analytics
3. Security & EU AI Act Governance
4. UI/UX & Session Latency
5. Standardization via Agent Skills

---

## 2. RAG Architecture & Retrieval Optimization

### Hierarchical & Parent-Child Chunking
* **Challenge**: Municipal legislation (*Kommuneloven*, *Hovedtariffavtalen*) contains long nested sections where small vector chunks lose overarching legal context.
* **Solution**: Implement **Parent-Child Chunking**:
  * Index small **child chunks** (128–256 tokens) for fine-grained vector similarity search in `sqlite-vec`.
  * Retrieve and inject the overarching **parent section** (1,024–2,048 tokens) into the Gemini context window.

### Two-Stage Retrieval with Reranking
```
User Query
    │
    ▼
[sqlite-vec / BM25 Hybrid Search] ──► Retrieves Top 30 Candidate Chunks
                                               │
                                               ▼
                                  [Cross-Encoder Reranker]
                                               │
                                               ▼
                                   Top 5 High-Precision Chunks ──► LLM Context
```

---

## 3. Data Engineering & OLAP Analytics (DuckDB + Parquet)

### Columnar In-Memory Analytics
* **Storage Format**: Convert static accounting journals (*Fact_Regnskap*) and budget dimensions (`Dim_Ansvar`, `Dim_Funksjon`, `Dim_Art`) into compressed **Apache Parquet** files.
* **Engine**: Execute DuckDB in-memory analytical queries over Parquet files for sub-millisecond aggregation across 7.24 BNOK budget totals.

### Change Data Capture (CDC) Delta Ingestion
* Replace nightly full table reloads with delta sync endpoints connecting to **Visma Enterprise** and **Framsikt GraphQL APIs**, updating only modified accounting vouchers.

---

## 4. Security, OWASP ASI06 & EU AI Act Compliance

### Indirect Prompt Injection Defense (OWASP ASI06)
* Apply **Spotlighting Delimiters** around all retrieved municipal documents and external text:
  ```xml
  <UNTRUSTED_MUNICIPAL_DOC_a9f81>
  [Retrieved text from PDF or invoice note]
  </UNTRUSTED_MUNICIPAL_DOC_a9f81>
  ```
* Enforce **Tool Result Parsing** to extract rigid JSON data types, filtering out natural language injection attempts.

### Audit Ledger (EU AI Act Article 14)
Every AI-assisted financial decision logs a SHA-256 sealed audit record:

```json
{
  "timestamp": "2026-10-18T07:30:00Z",
  "user_upn": "controller@kristiansand.kommune.no",
  "query_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "retrieved_chunk_ids": ["doc_43_chunk_12", "doc_08_chunk_04"],
  "ai_recommendation": "APPROVED_VARIANCES_WITHIN_KOMMUNELOVEN_PAR_14_5",
  "human_decision": "APPROVED",
  "sha256_seal": "8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4"
}
```

---

## 5. UI/UX Optimization (Streamlit + Power BI)

* **Lazy Loading**: Wrap heavy tabs (30-day liquidity curves, Power BI DAX showcases) in `@st.cache_data` and render them only on active tab selection.
* **Row-Level Security (RLS) Pre-Filtering**: When a unit leader (*Enhetsleder*) logs in, apply DuckDB query-level filtering on `Dim_Ansvar = 202` before rendering DOM components.

---

## 6. Standardizing Workflows via Agent Skills

Package core municipal workflows into `SKILL.md` Agent Skills:
* `MAL-AVVIK-EFFEKT-001` (4-step variance analysis protocol)
* `NAV-REFUND-GAP` (NAV sick leave refund reconciliation)
* `SELVKOST-5YR` (5-year self-cost calculation model)

Each skill loads procedural knowledge into model context only when triggered, preventing system prompt bloat.
