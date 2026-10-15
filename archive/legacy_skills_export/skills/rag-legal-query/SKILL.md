---
name: rag-legal-query
description: >-
  Kildekritisk oppslag i kommunalt regelverk med hybrid Gemini/Ollama, paragrafsitering (§) og SHA-256 revisjonsstempel.
---

# 🛠️ Agent Skill: RAG Legal & Governance Query (`rag-legal-query`)

> **Formål:** Automatisert og kildekritisk oppslag i kommunens regelverksdatabase (Kommuneloven, KOSTRA, Selvkost, Finansforskriften, Lokalt Økonomireglement) med 100 % kildeforankring (§) og uforanderlig SHA-256 revisjonsstempel.

---

## 📋 Skill Spesifikasjon & Metadata

| Egenskap | Verdi |
| :--- | :--- |
| **Skill Name** | `rag-legal-query` |
| **Versjon** | `1.0.0` |
| **Innebygde Gate-sjekker** | Gate 3 (Etikk), Gate 8 (Samsvar med Økonomireglementet), Gate 9 (Audit Log) |
| **Avhengigheter** | `sqlite-vec`, `FTS5`, `multilingual-e5-small`, `Gemini 3.8 Flash` (Primær, 0 % CPU), `Ollama` (Offline fallback) |

---

## ⚙️ Workflow & System Prompting

### Steg 1: Hybrid Søk
1. Generer 384D query-embedding via `multilingual-e5-small`.
2. Kjør parallelt vektorsøk (`sqlite-vec`) og eksaktsøk (`FTS5` på §-numre).
3. Kombiner og rangér treffene via **Reciprocal Rank Fusion (RRF)**.

### Steg 2: Glass-Box System Prompting
Når kilde-chunks er hentet og vasket for PII, sendes følgende instruks til LLM (Gemini 3.8 Flash eller lokal Ollama):

```text
Du er en spesialisert juridisk og økonomisk rådgiver for kommunen.
Besvar brukerens spørsmål UTLUKKENDE basert på den oppgitte kildekonteksten.

STRENGE INSTRUKSER:
1. Svaret må være 100 % forankret i de oppgitte kildene.
2. Du MÅ eksplisitt sitere lover og paragrafer (f.eks. "Jfr. Kommuneloven § 14-5...").
3. Dersom kildene ikke gir tilstrekkelig hjemmel, sier du: "Finner ikke tilstrekkelig hjemmel for dette i regelverksdatabasen."
4. Gjør ingen ekstrapoleringer eller gjetninger fra ekstern kunnskap.
```

### Steg 3: Audit Trail Signering
Svaret og benyttede Chunk-ID-er signeres med SHA-256 hash og lagres i `Audit_AI_Actions`.
