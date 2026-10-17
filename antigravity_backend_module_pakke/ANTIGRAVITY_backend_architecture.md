# Antigravity Backend Module — Architecture & Technical Specification
**Project:** AI_KOM (Kristiansand Kommune — Control Office Hub)  
**Module:** Antigravity Core Backend Engine (`/backend/antigravity`)  
**Version:** v2.4.0  
**Status:** Production Ready / Microservices Architecture  

---

## 1. Executive Summary & Engine Overview

**Antigravity** is the high-performance backend processing engine powering the **AI_KOM** municipal financial portal. Designed specifically for Norwegian municipal financial workflows (Kommuneloven § 14, KOSTRA, and Framsikt/Visma ecosystems), Antigravity acts as the central middleware layer between municipal source ERPs, vector stores, Power BI semantic models, and generative AI services.

### Core Objectives:
* **Deterministic Financial Computation:** Zero-tolerance for LLM hallucinations in raw financial accounting (KOSTRA artskontore, AGA calculations, selvkost, EVM metrics).
* **Cryptographic Data Lineage:** End-to-end audit trails (SHA-256) tracing every AI-generated variance note back to Visma/Framsikt transaction logs.
* **Asynchronous High Throughput:** Built on **FastAPI** and **Celery/Redis** to handle large-scale municipal datasets (100k+ GL lines) asynchronously.
* **Role-Based Security (RBAC):** Native integration with Identum eADM, Azure AD / Entra ID, and WebSak archive protocols.

---

## 2. System Architecture & Tech Stack

```
                                +---------------------------------------+
                                |      Frontend / UI Layer (AI_KOM)     |
                                |   GitHub Pages / React / Power BI     |
                                +---------------------------------------+
                                                    │
                                                    │ REST API / WebSockets
                                                    ▼
+---------------------------------------------------------------------------------------------------+
|                                 ANTIGRAVITY BACKEND ENGINE                                        |
|                                                                                                   |
|  +---------------------------+   +---------------------------+   +-----------------------------+  |
|  |     API Gateway / Router  |   |    Data Pipeline Engine    |   |     AI & RAG Orchestrator   |  |
|  |   FastAPI + Pydantic v2   |   |   Polars / DuckDB / Pandas|   |   LangChain / LlamaIndex    |  |
|  +---------------------------+   +---------------------------+   +-----------------------------+  |
|                │                               │                                │                 |
|                ▼                               ▼                                ▼                 |
|  +---------------------------+   +---------------------------+   +-----------------------------+  |
|  |  Auth & RBAC Middleware   |   | KOSTRA & Selvkost Rules   |   | Stage-Gate Port 9 Audit Engine|
|  |  Azure AD / eADM OAuth2   |   | Municipal Financial Logic |   | SHA-256 Ledger / Vector DB  |  |
|  +---------------------------+   +---------------------------+   +-----------------------------+  |
+---------------------------------------------------------------------------------------------------+
                                   │                   │                  │
                +------------------+                   │                  +------------------+
                ▼                                      ▼                                     ▼
+-------------------------------+    +----------------------------------+    +------------------------------+
|   Municipal ERP Connectors    |    |      Data Stores & Caching       |    |      AI / LLM Providers      |
| • Visma / Unit4 Enterprise    |    | • PostgreSQL / TimescaleDB       |    | • Azure OpenAI / Local LLM   |
| • Framsikt API (GraphQL/REST) |    | • Redis (Queue & Token Cache)    |    | • Qdrant / Chroma Vector DB  |
| • ACOS WebSak / Elements      |    | • Parquet / Delta Lake Storage   |    | • Ollama (Air-gapped)        |
+-------------------------------+    +----------------------------------+    +------------------------------+
```

### Technology Stack Table:

| Layer | Component | Description & Selection Rationale |
| :--- | :--- | :--- |
| **Framework** | FastAPI (Python 3.12) | Asynchronous, OpenAPI auto-docs, strict Pydantic v2 data validation. |
| **Data Engine** | Polars & DuckDB | In-memory analytical query processing 20x faster than Pandas for large GL dumps. |
| **Task Queue** | Celery + Redis | Asynchronous background processing for KOSTRA validation and report generation. |
| **Vector DB** | Qdrant / ChromaDB | Hybrid dense/sparse vector indexing for municipal statutes and Økonomireglement. |
| **ORM / Storage** | SQLAlchemy 2.0 + PostgreSQL | Async ORM paired with PostgreSQL for structured metadata, audit logs, and SHA-256 hashes. |
| **Authentication** | OAuth2 + OIDC | Azure AD / Entra ID integration with Identum eADM claims mapping. |

---

## 3. Core Subsystems & Services

### 3.1 Connector Service (`/services/connectors`)
* **Framsikt API Client:** Fetches budget frames, staffing grids, and HØP projections via REST/GraphQL.
* **Visma / ERP Ingestion Engine:** Parses GL (General Ledger) transactions, salary runs (Art 1010-1090), and NAV refund registers (Art 1600/1690).
* **KOSTRA SSB Extractor:** Ingests official Statistics Norway benchmarks and KOSTRA account matrices.

### 3.2 Calculation & Financial Rules Engine (`/services/finance_engine`)
* **Salary & Payroll Engine:** Automatically computes AGA (Zone 1: 14.1%), KLP/SPK pension premiums (Art 1200), holiday pay accruals (12.0%/14.3%), and NAV sick leave refund lags.
* **Selvkost Engine:** Implements the 5-year self-cost fund model (Water, Sewage, Waste, Building Permits) according to *Selvkostforskriften*.
* **EVM & Variance Tracker:** Calculates Earned Value Management indicators (CPI, SPI, Cost Variance) for major capital/investment projects.

### 3.3 AI & RAG Pipeline (`/services/ai_rag`)
* **Grounded RAG Pipeline:** Retrieves exact legal paragraphs from Kommuneloven, Økonomireglement, and HØP 2027–2030 context chunks.
* **Hallucination Guardrail:** Ensures generative LLM output includes citation markers `[i]` matching source passages; automatically flags ungrounded statements.
* **Audit Trail & SHA-256 Generator:** Generates immutable hash signatures for every report and variance note before sending to ACOS WebSak.

---

## 4. Directory Structure (`/backend/antigravity`)

```
/backend/antigravity/
├── app/
│   ├── api/                    # FastAPI route handlers (v1)
│   │   ├── endpoints/          # Route modules (budgets, payroll, kostra, rag, audit)
│   │   └── router.py           # Main API router aggregator
│   ├── core/                   # Core configuration, security, and logging
│   │   ├── config.py           # Environment variables (Pydantic Settings)
│   │   ├── security.py         # OAuth2, JWT validation, eADM claims
│   │   └── logging.py          # Structured JSON logging & OpenTelemetry
│   ├── db/                     # Database models, migrations, and sessions
│   │   ├── models/             # SQLAlchemy 2.0 ORM models
│   │   └── session.py          # Async session factory
│   ├── services/               # Core business logic modules
│   │   ├── connectors/         # Visma, Framsikt, KOSTRA, WebSak clients
│   │   ├── finance_engine/     # KOSTRA rules, AGA/Pension, Selvkost, EVM
│   │   ├── ai_rag/             # RAG chain, Qdrant store, Prompt templates
│   │   └── audit/              # SHA-256 hasher, Stage-Gate Port 9 signer
│   ├── schemas/                # Pydantic v2 models (Request/Response DTOs)
│   └── main.py                 # FastAPI application entrypoint
├── tests/                      # Pytest suite (unit, integration, e2e)
├── Dockerfile                  # Production container definition
├── docker-compose.yml          # Local orchestration setup
└── requirements.txt            # Python dependencies
```
