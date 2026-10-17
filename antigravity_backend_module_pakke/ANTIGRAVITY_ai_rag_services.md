# Antigravity Backend — AI, RAG & Governance Services
**Project:** AI_KOM (Kristiansand Kommune — Control Office Hub)  
**Module:** Antigravity AI & RAG Engine (`/services/ai_rag`)  

---

## 1. RAG Architecture & Governance Engine

The **AI & RAG Subsystem** in Antigravity empowers the AI_KOM portal with legal grounding, automated variance explanation generation, and Stage-Gate Port 9 audit signing.

```
+-----------------------------------------------------------------------------------+
|                               USER QUERY / PROMPT                                 |
|          "Forklar avviket på Art 1020 i Sektor Oppvekst for M9"                   |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                          ANTIGRAVITY RAG ORCHESTRATOR                             |
|  1. Fetch Financial Context: Query DuckDB for M9 actuals vs budget (Visma/Framsikt)|
|  2. Fetch Legal Context: Search Qdrant Vector DB for Økonomireglement & HØP       |
|  3. Construct Grounded Prompt Matrix (Enforcing citation rules [i])               |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                              AZURE OPENAI / LOCAL LLM                             |
|  • System Prompt: Municipal Controller Persona (No hallucinations, exact figures) |
|  • Execution: Generates draft 4-point variance note                               |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        GROUNDEDNESS & AUDIT GUARDRAILS                            |
|  • Citation Verifier: Validates that all factual statements match retrieved chunks  |
|  • Stage-Gate Port 9 Signer: Generates SHA-256 cryptographic signature           |
|  • Export Service: Formats to ACOS WebSak XML / Word / PDF                        |
+-----------------------------------------------------------------------------------+
```

---

## 2. Vector DB & Knowledge Base Indexing

Antigravity indexes all relevant municipal documents into a **Qdrant Vector Database** using hybrid dense/sparse embeddings (`text-embedding-3-large` + BM25):

### Indexed Legal & Strategy Corpus:
1. **Kommuneloven (2018) Kapittel 14 & Forskrifter:** Budsjett, regnskap, minimumsavdrag, selvkost, og ROBEK-regler.
2. **Økonomireglement for Kristiansand kommune:** Lokale måltall (1.0% netto driftsresultat, 4.0% disposisjonsfond, 8.8 mrd. kr lånetak).
3. **Handlings- og økonomiplan (HØP 2027–2030):** Handlingsrammer, innsparingstiltak, og investeringsprosjekter.
4. **KOSTRA Kontoplan 2026/2027:** Artskontoer, funksjoner, og konteringsregler.

---

## 3. Stage-Gate Port 9 & SHA-256 Audit Signing

To ensure full compliance with municipal governance, generated financial variance notes and budget adjustments must pass **Stage-Gate Port 9**:

### Gate Approval Flow:
1. **Draft Generation:** AI constructs draft variance note based on financial data.
2. **Controller Inspection:** Controller reviews note in *Controller Hub*.
3. **Decision Options:** `APPROVED` | `MODIFIED` | `REJECTED`.
4. **Cryptographic Signing:** Upon approval, Antigravity generates a permanent audit certificate:

```json
{
  "stage_gate": "Port_9_Final_Approval",
  "municipality": "Kristiansand_Kommune",
  "document_type": "Budsjettavviksnotat_M9",
  "unit_id": "Unit_2020_Grunnskole",
  "financial_variance_nok": -1420000,
  "approved_by_user": "controller_882",
  "approval_timestamp": "2026-10-17T08:15:22Z",
  "document_sha256": "4799479f1be94f20a7acdd92c53f6796c0f6fec5780144eaa2529f275a83e4ee",
  "websak_archive_reference": "26/10982-1"
}
```

---

## 4. Prompt Engineering Matrix (Controller System Prompt)

```markdown
You are Antigravity Controller AI, an expert municipal financial analyst for Kristiansand kommune.

STRICT CONSTRAINTS:
1. Ground every claim strictly in the provided Visma/Framsikt financial data and municipal legal documents.
2. Every factual statement or figure MUST end with a bracketed citation `[i]` matching the context passage.
3. Use exact municipal terminology (Netto driftsresultat, Disposisjonsfond, Netto lånegjeld, KOSTRA Funksjon/Art).
4. Never invent numbers, dates, or legal rules outside the retrieved sources.
5. Provide crisp, professional output ready for the Municipal Director (Kommunedirektøren) and Formannskapet.
```
