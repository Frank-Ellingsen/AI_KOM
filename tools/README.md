# 🛠️ Kommune AI Tool Drivers & Execution Engine (`tools/`)

> **Tekniske lavnivå-drivere, infrastrukturmoduler og I/O-broer for Kommune AI Guardrails.**

---

## 📋 Verktøykatalog

| Verktøydriver | Filnavn | Kjernefunksjon & Teknologi |
| :--- | :--- | :--- |
| **Document Parser** | [`TOOL_SKILL_DOCUMENT_PARSER.md`](./TOOL_SKILL_DOCUMENT_PARSER.md) | Ekstraksjon av PDF (§-chunking), Word (.docx), Excel (.xlsx) og CSV med automatisk tegnsett-deteksjon (`cp1252`/`UTF-8`). |
| **Hybrid LLM Gateway** | [`TOOL_SKILL_LLM_GATEWAY.md`](./TOOL_SKILL_LLM_GATEWAY.md) | Intelligent modell-ruting: **Gemini 3.8 Flash** primært (0 % lokal CPU-last) med fallback til **Ollama** ved frakoblet drift. |
| **Ollama API Bridge** | [`TOOL_SKILL_OLLAMA_API_BRIDGE.md`](./TOOL_SKILL_OLLAMA_API_BRIDGE.md) | Lokal Ollama inferens (`llama3.1`, `qwen2.5`) med tvungen JSON Schema-modus og temperaturkontroll. |
| **DuckDB Analytics** | [`TOOL_SKILL_DUCKDB_ANALYTICS.md`](./TOOL_SKILL_DUCKDB_ANALYTICS.md) | In-memory OLAP-analyser over SQLite Star Schema, Project Controlling (EAC, CPI) og Parquet-eksport for Power BI. |
| **SQLite & Vector DB** | [`TOOL_SKILL_SQLITE_VEC_EXECUTOR.md`](./TOOL_SKILL_SQLITE_VEC_EXECUTOR.md) | Lavnivå-tilkobling til `kommune_golden_record.db`, WAL-modus, FTS5 fritekst og 384D vektor-KNN via `sqlite-vec`. |
| **Python Sandbox Runner** | [`TOOL_SKILL_PYTHON_SANDBOX_RUNNER.md`](./TOOL_SKILL_PYTHON_SANDBOX_RUNNER.md) | Sikker subprocess-kjøring av dataanalyse-skripter med timeout, feilhåndtering og isolert `scratch/`-mappe. |
| **Streamlit UI Builder** | [`TOOL_SKILL_STREAMLIT_UI_BUILDER.md`](./TOOL_SKILL_STREAMLIT_UI_BUILDER.md) | Brukergrensesnitt for Control Office Hub (`app/app.py`), tilstandsbevaring (*Session State*), caching og CSV-eksport. |

---

## 🏗️ Arkitektur & Bruksmønster
Disse tekniske verktøyene utgjør infrastruktur-laget (Lag 2). De kalles dynamisk av de overordnede forretningsferdighetene i [`kommune_ai_agent_skills`](../kommune_ai_agent_skills/).
