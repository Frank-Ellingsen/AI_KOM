# 🧠 Kommune AI Agent Skills (`kommune_ai_agent_skills/`)

> **Funksjonelle agentferdigheter, regelverk, domenekunnskap og saksbehandlingsregler for kommunal økonomi og virksomhetsstyring.**

---

## 📋 Ferdighetskatalog (Domain Skills)

| Kategori | Ferdighet | Filnavn | Standard & Hjemmel |
| :--- | :--- | :--- | :--- |
| **Dataintegrasjon** | Data Integration & ETL | [`SKILL_DATA_INTEGRATION_ETL.md`](./skills/SKILL_DATA_INTEGRATION_ETL.md) | Star Schema, Idempotent SHA-256 |
| **Sikkerhet & PII** | PII Scrubbing & Guardrails | [`SKILL_PII_AND_GUARDRAILS.md`](./skills/SKILL_PII_AND_GUARDRAILS.md) | Stage-Gate Port 4, Norsk FNR/DNR, +47 |
| **Regelverk (KOSTRA)**| KOSTRA Account Analyzer | [`SKILL_KOSTRA_ANALYZER.md`](./skills/SKILL_KOSTRA_ANALYZER.md) | Kommuneloven § 14-9 (Drift vs. Inv), Selvkost |
| **Avviksdeteksjon** | EPM Variance Detect | [`SKILL_EPM_VARIANCE_DETECT.md`](./skills/SKILL_EPM_VARIANCE_DETECT.md) | Avvik > 5 % / > 250k, Kommuneloven § 14-5 |
| **Finansiell Modellering**| Excel & Python FP&A | [`SKILL_EXCEL_PYTHON_FPNA.md`](./skills/SKILL_EXCEL_PYTHON_FPNA.md) | FAST Standard, Monte Carlo-risikosimulering |
| **Excel & Power Query**| Excel MCP Integration | [`SKILL_EXCEL_MCP_INTEGRATION.md`](./skills/SKILL_EXCEL_MCP_INTEGRATION.md) | Power Query M, DAX `ISINSCOPE` |
| **BI & Fabric** | Power BI & Fabric Analytics | [`SKILL_POWERBI_FABRIC_ANALYTICS.md`](./skills/SKILL_POWERBI_FABRIC_ANALYTICS.md) | Star Schema, Dynamiske Formatstrenger, RLS |
| **Jus & RAG** | RAG Legal & Governance Query | [`SKILL_RAG_LEGAL_QUERY.md`](./skills/SKILL_RAG_LEGAL_QUERY.md) | Hybrid Gemini/Ollama, Kildehenvisning (§) |
| **Saksbehandling** | Saksfremlegg & Rapportgenerator| [`SKILL_SAKSFREMLEGG_GENERATOR.md`](./skills/SKILL_SAKSFREMLEGG_GENERATOR.md) | Kommuneloven § 13-1, Klarspråk, HITL Utkast |
| **Visualisering** | Visual Data Communication | [`SKILL_VISUAL_DATA_COMMUNICATION.md`](./skills/SKILL_VISUAL_DATA_COMMUNICATION.md) | Edward Tufte Data-Ink, Cleveland & McGill |
| **Revisjon & Innsyn** | Audit Governance & Registry | [`SKILL_AUDIT_GOVERNANCE_REGISTRY.md`](./skills/SKILL_AUDIT_GOVERNANCE_REGISTRY.md) | Eurocities Transparency, SHA-256 Audit Trail |

---

## 🔄 Samspill med Tekniske Verktøy
Ferdighetene i denne mappen orkestrerer de underliggende tekniske verktøydriverne i [`../tools/`](../tools/):
1. ETL kaller `document-parser` og `sqlite-vec-executor`.
2. EPM Variance kaller `duckdb-analytics`.
3. RAG Legal kaller `llm-gateway`.
4. Visual Data Communication kaller `streamlit-builder`.
