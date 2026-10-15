# Local-First AI Architecture & Privacy Protection Rules
# Applied to Municipal Data & Antigravity Agents

## 1. Local-First Principle
* **Data Locality**: All municipal accounting data, personnel rosters, and citizen services records must remain 100% on-premise/local.
* **Database Engine Priority**:
  * **DuckDB**: Use for analytical OLAP aggregations, time-series projections, and Parquet conversions.
  * **SQLite**: Use for transactional lookup, Star Schema Golden Record (`Fact_Regnskap`, `Dim_Art`, `Dim_Funksjon`, `Dim_Ansvar`), and vector embeddings (`sqlite-vec`).
* **Local LLM Inference**:
  * Default to local inference engines: **Ollama** (`llama3.2`, `mistral`, `qwen2.5-coder`) or **LM Studio**.
  * No cloud transmission of unredacted payroll or patient identifiers.

## 2. Guardrails & Human-in-the-Loop (HITL)
* **Stage-Gate Port 9 (HITL)**:
  * Any AI recommendation involving budget transfers, position freezes, or legal assessments MUST include a human review step (APPROVED, MODIFIED, REJECTED) with named reviewer credentials and reason.
* **Audit Trail & Cryptographic Hashing**:
  * Every generated administrative note, report, or formal case submission must append an immutable SHA-256 digest (`SHA-256: <hash>`).
  * Log all actions to `Audit_AI_Actions` table in SQLite.

## 3. PII & Sensitive Information Scrubbing
* Replace real citizen names, national identity numbers (Fødselsnummer 11 siffer), and health diagnoses with synthetic surrogates before vector embedding or LLM prompting:
  * `[BRUKER_ID_XXXX]` for citizen IDs.
  * `[PERSON_ANONYM_YY]` for employees.
  * Aggregate department-level totals rather than single individual entries.
