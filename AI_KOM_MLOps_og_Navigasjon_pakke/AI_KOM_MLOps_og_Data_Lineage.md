# MLOps, Data Lineage & Governance Architecture
**Kristiansand kommune — Control Office Hub (AI_KOM)**

---

## 1. Oversikt og Formål
I et kommunalt AI- og styringssystem som **AI_KOM** er MLOps (Machine Learning Operations) og Data Lineage avgjørende for å sikre **sporbarhet, datasikkerhet (GDPR), etterrettelighet og juridsisk overholdelse** overfor Kommunerevisjonen, Kontrollutvalget og Bystyret.

Når AI-modeller genererer avviksanalyser, saksfremlegg og prognoser basert på Framsikt, Visma og KOSTRA, må enhver overskrift og kronesum kunne spores 100 % tilbake til sin kildeversjon.

---

## 2. Arkitektur for Data Handling & Pipeline Ingestion

```
+-----------------------------------------------------------------------------------+
|                            KOMMUNALE KILDESYSTEMER                                |
|  [Visma / ERP]      [Framsikt API]      [KOSTRA / SSB]      [ACOS WebSak Archive] |
| (Lønn / HR Data)  (Budsjett/Prognose)  (Nøkkeltall/SSB)   (Saksdokumenter/HØP) |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        DATA HANDLING & INGESTION LAYER                            |
|  1. PII Anonymization Engine (Maskering av personopplysninger i faste/variable lønn) |
|  2. Schema Validation & KOSTRA Kontoplan Mapper (Automatisert validering)          |
|  3. Power BI Dataflows & Delta Lake Staging (Inkrementell lasting)                |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                      DATA LINEAGE & TRACEABILITY ENGINE                           |
|  • SHA-256 Hash Generation for kildedata og beregningskjøringer                    |
|  • Metadata Indexing: Timestamp, Kildeversjon, Endringshistorikk                   |
|  • End-to-End Lineage Map: Visma/Framsikt -> DAX -> RAG Embeddings -> AI Sak      |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                      MLOPS & RAG LIFECYCLE MANAGEMENT                             |
|  • RAG Vector Store (ChromaDB / Qdrant): Indeksering av HØP, Lover & Reglement     |
|  • Prompt Version Control & Model Registry (v1.0, v2.1 med System Prompts)       |
|  • Hallucination & Groundedness Evaluator (Citasjonskontroll mot kilder)          |
|  • Stage-Gate Port 9 Sign-off (APPROVED / REJECTED med digitalt stempel)          |
+-----------------------------------------------------------------------------------+
```

---

## 3. Komponentbeskrivelse

### A. Data Handling & Ingestion (Datafangst og Anonymisering)
1. **PII Maskering (Personvern & GDPR):**
   * Lønns- og personalskjemadata fra Visma/Unit4 vaskes automatisk for fødselsnumre, navn og direkte personidentifikatorer før data lastes inn i AI-modeller.
   * Aggergering skjer på **stillingskode, avdeling/funksjon og art** for å bevare full økonomisk presisjon uten å eksponere enkeltsaker.
2. **Standardisert Validering:**
   * Automatisk sjekk mot KOSTRA kontoplan for å fange opp feilkontering (f.eks. ulovlig kombinasjon av funksjon 2020 og art 1600 uten gyldig refusjonskode).

### B. Data Lineage & Sporbarhet (Audit Trail)
1. **Kryptografisk SHA-256 Stempling:**
   * Hver datakjøring og generert avviksnotat tildeles en unikt kryptografisk hash (f.eks. `a4523fff-19ea-44bc-88f9-5882936f75af`).
2. **Kilde-til-rapport Kartlegging:**
   * Brukere kan klikke på et avvikstall i rapporten og få opp den eksakte kildekjeden:
     `Visma Transaksjons-ID #88219 -> Framsikt M9 Eksport -> DAX Måltall [VariabelLønnAvvik] -> AI RAG Context -> Saksavsnitt 2.1`.

### C. MLOps & RAG Lifecycle Management
1. **Model Registry & Prompt Versioning:**
   * Alle system-prompter, temperaturinnstillinger og LLM-versjoner (f.eks. Gemini / GPT-4o) versjonsstyres i repository under `/prompts/` og `/models/`.
2. **RAG Vector Database:**
   * Kommuneloven, Økonomireglementet for Kristiansand, HØP 2027–2030 og KOSTRA-veiledere er oppdelt i semantiske vegger og vektorindeksert med automatiske oppdateringer når nye forskrifter vedtas.
3. **Groundedness & Citations Evaluator:**
   * AI-assistenten kjører automatisk validering på at alle påstander i saksfremlegget har direkte sitater `[i]` til godkjente kommunale kilder. Påstander uten kildedekning flagges automatisk som *"Uverifisert påstand"*.

### D. Security, RBAC & Offentleglova
1. **Role-Based Access Control (RBAC):**
   * Enhetsledere har kun tilgang til sin enhets lineage-logger.
   * Controllere og MLOps-administratorer har full tilgang til modeller, logs, vektordatabasen og pipeline-metrikker.
2. **Offentleglova & Innsyn:**
   * Genererte MLOps-logger og prompt-historikk kan eksporteres i standardisert JSON/PDF-format ved innsynsbegjæringer jf. Offentleglova.

---

## 4. Inpassing i AI_KOM Portallayout (Fane 3)

MLOps og Data Lineage-modulen plasseres under **📊 Fane 3: Controller Hub & Analyse** som en egen undermodul:

* **📊 Fane 3: Controller Hub & Analyse**
  * `3.1` KOSTRA & Framsikt Engine
  * `3.2` Power BI & Enterprise Data Hub
  * `3.3` Stage-Gate Port 9 & AI Governance
  * **`3.4` MLOps, Data Lineage & Pipeline Status (NY)**
    * *Data Ingestion Health & API Latency*
    * *Data Lineage Graph Explorer (Visma -> Framsikt -> Power BI -> AI)*
    * *RAG Knowledge Base Status & Vector Index Refreshes*
    * *Audit Logs & SHA-256 Verification Center*
