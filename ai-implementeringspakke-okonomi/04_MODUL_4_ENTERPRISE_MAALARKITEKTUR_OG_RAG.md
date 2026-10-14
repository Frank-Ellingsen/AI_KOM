# Modul 4: Enterprise AI Målarkitektur, RAG og Integrasjoner

## 1. Prinsipper for Kommunal AI-Arkitektur

En moderne Enterprise AI-arkitektur for økonomi og virksomhetsstyring må oppfylle fire krav:
1. **Sikkerhet og skjerming:** Følsomme økonomidata og PII (personidentifiserende informasjon) må skjermes før de når språkmodellen.
2. **Modelluavhengighet (Ingen Vendor Lock-in):** Arkitekturen må tillate sømløst bytte av underliggende språkmodell (Azure OpenAI, Mistral EU, Llama m.fl.).
3. **Kildeforankring (RAG):** Svar skal utelukkende baseres på kommunens egne verifiserte dokumenter og regnskapsdata.
4. **Arvet Tilgangsstyring (RBAC):** Brukere skal kun få svar basert på data de har formell tilgang til i fagsystemene.

---

### 2. Visuell Målarkitektur

```
+-----------------------------------------------------------------------------------+
|                           BRUKERGRENSESNITT & FAGSYSTEMER                         |
|        (ERP / Visma / Unit4 / ACOS / Sak-Arkiv / M365 Copilot / Web-portal)       |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
|                              ENTERPRISE AI GATEWAY                                |
|   • PII-Anonymisering & Maskering     • Tilgangsstyring (Entra ID / RBAC)         |
|   • Token- & Kostnadskontroll (FinOps) • Sentral Sikkerhets- & Audit-logging       |
+-----------------------------------------------------------------------------------+
                                          │
                   ┌──────────────────────┴──────────────────────┐
                   ▼                                             ▼
+------------------------------------+         +------------------------------------+
|        RAG-MOTOR & DATAINDEX       |         |          SPRÅKMODELL-LAG           |
|  • Vektordatabase (Pinecone/Qdrant)|         |  • Lukkede modeller (Azure OpenAI) |
|  • ERP-Data, Budsjett, Reglement   |         |  • Europeiske modeller (Mistral)   |
|  • Dokumenter, Avtaler, Arkiv      |         |  • Spesialiserte prediksjonsmodeller|
+------------------------------------+         +------------------------------------+
```

---

### 3. RAG-Arkitektur i Praksis (Retrieval-Augmented Generation)

RAG forhindrer hallusinasjoner ved å splitte prosessen i tre steg:
1. **Indexing (Indeksering):** Kommunens økonomireglement, avtaler og regnskapsnotater vaskes, vektoriseres og lagres i en skjermet vektordatabase.
2. **Retrieval (Uthenting):** Når en rådgiver stiller et spørsmål, henter systemet ut de 3–5 mest relevante tekstsegmentene basert på semantisk likhet og brukerens tilgangsrettigheter.
3. **Generation (Generering):** Språkmodellen mottar spørsmålet *sammen med* de uthentede kildene, og utarbeider et svar som **kun** bygger på disse kildene med direkte referanse til dokument og paragraf.

---

### 4. MLOps og LLMOps: Modellforvaltning i Drift

For å opprettholde kvalitet og sikkerhet over tid kreves:
* **Testsett (*Ground Truth*):** Et lukkede sett med 30–50 standardspørsmål og fasitsvar for kontinuerlig kvalitetstesting.
* **Observability (Overvåking):** Dashbord som måler responstid (latency), token-forbruk, feilrate og bruker-feedback (thumps up/down).
* **Versjonskontroll:** Full sporing av hvilken modellversjon, system-prompt og RAG-indeks som ble benyttet ved hver forespørsel.
