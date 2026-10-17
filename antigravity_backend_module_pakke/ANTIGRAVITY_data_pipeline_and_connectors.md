# Antigravity Backend — Data Pipeline & Connectors Specification
**Project:** AI_KOM (Kristiansand Kommune — Control Office Hub)  
**Module:** Antigravity Connectors & ETL Subsystem (`/services/connectors`)  

---

## 1. Overview & Data Flow Architecture

The **Data Pipeline Engine** in Antigravity handles high-throughput extraction, transformation, PII scrubbing, and loading (ETL/ELT) from municipal enterprise systems into the AI_KOM analytical warehouse and vector indexes.

```
+-------------------+      +-------------------+      +-------------------+
| Visma / Unit4 ERP |      |   Framsikt API    |      |  SSB KOSTRA Data  |
+-------------------+      +-------------------+      +-------------------+
          │                          │                          │
          ▼                          ▼                          ▼
+-------------------------------------------------------------------------+
|                  ANTIGRAVITY INGESTION & PII SCRUBBER                   |
|  • Masking personal IDs (Fødselsnr) & individual names in payroll       |
|  • Normalizing KOSTRA Artskonto (1000-9000) and Funksjon (100-899)      |
|  • Deduplication and Deltalake Ingestion                                |
+-------------------------------------------------------------------------+
                                     │
                                     ▼
+-------------------------------------------------------------------------+
|                      POLARS / DUCKDB ANALYTICAL ENGINE                  |
|  • In-memory aggregation of General Ledger (GL) transactions           |
|  • Automatic computation of Variance = (Actual YTD - Budget YTD)        |
|  • SHA-256 Stamping of raw dataset payload                              |
+-------------------------------------------------------------------------+
                                     │
                                     ▼
+-------------------------------------------------------------------------+
|                  STORAGE & VECTOR DB DISTRIBUTION                       |
|  1. PostgreSQL: Structured GL, KOSTRA, and Audit tables                 |
|  2. Qdrant Vector DB: Semantic chunks for RAG context retrieval          |
|  3. Power BI Gateway: Semantic model refresh pushes                     |
+-------------------------------------------------------------------------+
```

---

## 2. Connector Specifications

### 2.1 Visma / ERP Connector (`visma_connector.py`)
* **Protocol:** REST API (OAuth2 Client Credentials) / SQL Direct Staging.
* **Ingestion Schedule:** Nightly batch at 02:00 CET + On-demand trigger during month-end closing (M1–M12).
* **PII Masking Rules:**
  * `employee_id` -> Hashed via HMAC-SHA256 with municipal salt.
  * `employee_name` -> Stripped and replaced with `Job Code + Function ID`.
  * `social_security_num` -> Dropped immediately at ingestion boundary.

### 2.2 Framsikt API Connector (`framsikt_connector.py`)
* **Protocol:** GraphQL API / REST Export endpoint.
* **Data Extracted:**
  * **HØP Frames:** 4-year financial plan figures per sector and unit.
  * **Positions Grid:** Staffing headcount, position codes, vacancy estimates.
  * **Monthly Budgets:** Phased monthly budget vectors per account.
* **Handling Excel Roundtrips:** Parses exported/imported Excel templates from section leaders and verifies structural integrity prior to Framsikt re-ingestion.

### 2.3 KOSTRA & SSB Data Sync (`kostra_connector.py`)
* **Protocol:** SSB Open API (`data.ssb.no/api/v0/en/`).
* **Ingestion:** Fetches annual KOSTRA key figures (ASSS benchmark group, municipal averages, unit costs per pupil/patient).
* **Validation Engine:** Checks current municipality accounting against official KOSTRA 2026/2027 account structure rules (`kostra_kontoplan.csv`).

---

## 3. Data Transformation & KOSTRA Mapping Logic

```python
# Example Polars Transformation Pipeline in Antigravity
import polars as pl
import hashlib

def process_payroll_ingestion(raw_df: pl.DataFrame, salt: str) -> pl.DataFrame:
    """
    Ingests raw Visma payroll data, scrubs PII, and aggregates to KOSTRA Art level.
    """
    processed_df = (
        raw_df
        .filter(pl.col("kontoklasse") == 1)  # Driftsregnskap
        .with_columns([
            # PII Anonymization
            pl.col("fnr").apply(lambda x: hashlib.sha256((x + salt).encode()).hexdigest()[:16]).alias("anon_user_id"),
            # Ensure 4-digit Art code
            pl.col("art").cast(pl.Utf8).str.zfill(4).alias("kostra_art"),
            # Ensure 4-digit Funksjon code
            pl.col("funksjon").cast(pl.Utf8).str.zfill(4).alias("kostra_funksjon")
        ])
        .group_by(["ansvar", "kostra_funksjon", "kostra_art", "period"])
        .agg([
            pl.col("belop").sum().alias("belop_ytd"),
            pl.col("anon_user_id").n_unique().alias("ansatte_count")
        ])
    )
    return processed_df
```

---

## 4. SHA-256 Lineage & Audit Tracking

Every dataset ingested or processed by Antigravity receives a **Data Provenance Record** stored in the `data_lineage_log` PostgreSQL table:

```json
{
  "lineage_id": "lin_99812a4f_2026M09",
  "source_system": "Visma_ERP_Kristiansand",
  "extraction_timestamp": "2026-10-15T02:00:14Z",
  "raw_payload_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "processed_records_count": 14250,
  "schema_version": "v2026.1",
  "target_table": "gl_monthly_summaries",
  "pipeline_status": "SUCCESS"
}
```
