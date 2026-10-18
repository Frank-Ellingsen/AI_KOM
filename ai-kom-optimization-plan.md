# Kristiansand Kommune Control Office Hub (AI_KOM) Optimization Blueprint

An architectural and technical optimization plan for the Kristiansand Kommune Control Office Hub & AI Assistant (`AI_KOM`).

---

## 1. Executive Summary & Core Objectives

The **AI_KOM** platform is the central operational hub for financial controlling across Kristiansand Kommune's **6 virksomhetsområder** (Oppvekst, Helse og mestring, By- og stedsutvikling, Kultur og innbyggerdialog, Organisasjon og teknologi, samt Økonomi og konsernstyring), **81 organisatoriske enheter**, og et årsbudsjett på **7,24 milliarder NOK**.

The platform unifies municipal regulatory compliance (*Kommuneloven § 14-5/§ 14-6*, *KOSTRA*, *EVM*), Glass-Box RAG (`sqlite-vec`), DuckDB in-memory OLAP analytics, og Stage-Gate Port 9 AI governance.

To scale the platform to full enterprise production, this blueprint details 6 core optimization pillars:
1. Legal-Aware RAG & Hybrid Retrieval
2. Data Engineering & DuckDB/SQLite Golden Record
3. Security, PII Guardrails, OWASP ASI06 & EU AI Act Art. 14
4. UI/UX Architecture & Client-Side Rendering ([index.html](file:///C:/Users/frank/Desktop/AI_KOM/index.html) + Streamlit)
5. Model Gateway & Hybrid Routing (Gemini 3.8 Flash + Ollama)
6. Modular Agent Skills Standard

---

## 2. RAG Architecture & Legal Retrieval Optimization

### 2.1 Paragraph-Aware Chunking (`§`-Boundary Chunking)
* **Challenge**: Fixed-token chunking (e.g. 128 or 256 tokens) splits legal statutes midway through sentences, breaking the connection between legal conditions (*Kommuneloven § 14-5 første ledd*) and the statutory duty to act (*annet ledd*).
* **Optimization**: Implement **Paragraf- og ledd-basert chunking** via [document-parser](file:///C:/Users/frank/Desktop/AI_KOM/.agents/skills/document-parser/SKILL.md):
  * **Child Chunks**: Formal legal sections (`§ 14-5 ledd 1-3`, `HTA § 4 pkt 4.2`, `Momskompensasjonsloven § 4`).
  * **Parent Context**: Overarching law/chapter and municipal administrative guidelines (1 024–2 048 tokens) injected into model context window.
  * **Metadata Anchoring**: Every chunk tags `lov_hjemmel`, `paragraf_nummer`, `kapittel`, og `gyldighetsaar`.

### 2.2 Two-Stage Hybrid Retrieval with Cross-Encoder Reranking
```
Bruker- eller Controller-spørring
              │
              ▼
    [Query Normalizer & PII Scrub]
              │
              ▼
   ┌──────────────────────┬──────────────────────┐
   │ BM25 Fritekstsøk     │ sqlite-vec KNN       │
   │ (Juridiske termer)   │ (384-dim all-MiniLM) │
   └──────────┬───────────┴──────────┬───────────┘
              │                      │
              └──────────┬───────────┘
                         ▼
              [RRF / Rank Fusion] ──► Topp 30 Kandidat-chunks
                         │
                         ▼
             [Cross-Encoder Reranker]
                         │
                         ▼
              Topp 5 Høypresisjons-chunks ──► LLM Kontekst (Gemini 3.8 / Ollama)
```

---

## 3. Data Engineering & OLAP Analytics (DuckDB + SQLite)

### 3.1 Zero-Copy In-Memory Analytics
* **Master Transactional Store**: SQLite Star Schema Golden Record (`erp_data/kommune_golden_record.db`).
* **DuckDB OLAP Engine**: DuckDB kobles direkte til SQLite via native SQLite-scanner uten duplisering:
  ```sql
  ATTACH 'erp_data/kommune_golden_record.db' AS golden (TYPE SQLITE);
  ```
* **Cold Storage i Parquet**: Avsluttede regnskapsår (2020–2025) partisjoneres i Apache Parquet-filer (`data/parquet/regnskap_aar=2025/`). DuckDB kjører analytiske spørringer på tvers av 7,24 milliarder NOK på under 15 ms.

### 3.2 Change Data Capture (CDC) Delta Ingestion
* Erstatt tunge nattlige totalopplastinger med differensiell CDC-synkronisering mot **Visma Enterprise ERP** og **Framsikt EPM**.
* Ingestion-køen (`erp_data/staging_queue/`) behandler kun modifiserte bilag og periodiseringsendringer med SHA-256 verifisering.

---

## 4. Security, PII Guardrails, OWASP ASI06 & EU AI Act Governance

### 4.1 PII Scrubbing Gate (Stage-Gate Port 4)
* **GDPR Art. 9 & Personopplysningsloven**: Ingen rå fødselsnumre (FNR), ansattnumre, kontonumre eller personnavn skal overføres til offentlige eksterne sky-API-er.
* Alle forespørsler kjøres gjennom [pii-guardrails](file:///C:/Users/frank/Desktop/AI_KOM/.agents/skills/pii-guardrails/SKILL.md) før eventuell dispatch til `Gemini 3.8 Flash`.
* Dersom saksbehandlingen krever uanonymiserte helse- eller personalopplysninger, rutes forespørselen automatisk til **lokal frakoblet Ollama** (`qwen2.5-coder` / `llama3.2`).

### 4.2 Indirect Prompt Injection Defense (OWASP ASI06)
* Dokumenter fra uverifiserte kilder (inngående fakturavedlegg, e-poster, eksterne PDF-er) innkapsles med kryptografiske avgrensninger:
  ```xml
  <UNTRUSTED_MUNICIPAL_DOC_a9f81 sha256="4e8a...">
  [Uverifisert tekst fra fakturavedlegg eller henvendelse]
  </UNTRUSTED_MUNICIPAL_DOC_a9f81>
  ```
* Systeminstruksen pålegger modellen å ignorere instruksjoner inne i `<UNTRUSTED_...>`-blokken.

### 4.3 Stage-Gate Port 9 Audit Ledger (EU AI Act Article 14)
Enhver AI-assistert budsjettanbefaling eller avviksvurdering forsegles med SHA-256 hash og krever eksplisitt menneskelig godkjenning (HITL - Human-In-The-Loop):

```json
{
  "timestamp": "2026-10-18T14:30:00Z",
  "controller_upn": "frank.ellingsen@kristiansand.kommune.no",
  "sector_id": "OMR-01",
  "unit_id": "ENH-002",
  "query_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "retrieved_chunk_ids": ["lov_14_5_chunk_02", "hta_4_chunk_11"],
  "ai_recommendation": "SUPPLEMENTARY_BUDGET_REQUIRED_PAR_14_5",
  "human_decision": "APPROVED",
  "sha256_seal": "8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4"
}
```

---

## 5. UI/UX Architecture & Client-Side Rendering

* **Primær Hub ([index.html](file:///C:/Users/frank/Desktop/AI_KOM/index.html))**:
  * 4-faset personanavigasjon: *Min Enhet*, *Sektor & Konsernstyring*, *Controller Hub*, og *Veiledere & Maler*.
  * Matematisk streng SVG-rendering for takometre (Gauges) som eliminerer tunge JavaScript-biblioteker og rendrer på under 2 ms.
  * Tufte Data-Ink disiplin: Ingen vertikale skillelinjer, dempede bakgrunner, og fargebruk reservert for faktiske avvik (`#c0392b`, `#d35400`, `#27ae60`).
* **Row-Level Security (RLS) Pre-Filtering**:
  * Ved pålogging for enhetsleder filtreres datagrunnlaget i DuckDB/SQLite på `Dim_Ansvar = X` før DOM-elementer bygges.
* **Streamlit Pilot (`mvp-pilot/`)**:
  * Caching via `@st.cache_data` for What-If scenarioberegninger og Monte Carlo-simuleringer.

---

## 6. Standardizing Workflows via Agent Skills

Ferdigheter organiseres etter prinsippet om **Progressive Disclosure** i `.agents/skills/`:
* [epm-variance-detect](file:///C:/Users/frank/Desktop/AI_KOM/.agents/skills/epm-variance-detect/SKILL.md): Z-score avviksdeteksjon og terskelvarsling jf. § 14-5.
* [predictive-forecasting](file:///C:/Users/frank/Desktop/AI_KOM/.agents/skills/predictive-forecasting/SKILL.md): Monte Carlo P10/P50/P90 og rullende Earned Value (EAC/ETC).
* [kostra-analyzer](file:///C:/Users/frank/Desktop/AI_KOM/.agents/skills/kostra-analyzer/SKILL.md): Kontoplan, drifts- vs. investeringsskille og selvkost 5-år.
* [saksfremlegg-generator](file:///C:/Users/frank/Desktop/AI_KOM/.agents/skills/saksfremlegg-generator/SKILL.md): Formelle politiske saksnotater til Formannskapet og Bystyret.
* [audit-governance](file:///C:/Users/frank/Desktop/AI_KOM/.agents/skills/audit-governance/SKILL.md): SHA-256 forsegling og revisjonseksporter for Kommunerevisjonen.
