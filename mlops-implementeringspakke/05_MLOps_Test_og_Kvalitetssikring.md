# 05. MLOps Testing, Ground Truth og Kvalitetssikring

## 1. Test-Pyramiden for AI-Systemer

I MLOps må tradisjonell programvaretesting suppleres med **datatesting og modell-evaluering**:

```
           /           /   \     Level 3: Human-in-the-Loop (UAT & Saksbehandler-review)
         /-----        /       \   Level 2: Ground Truth & RAG Evaluation (Automated LLM-benchmarks)
       /---------      /           \ Level 1: Data & Code Validation (Unit tests, PII-filter, Schema checks)
     /-------------```

---

## 2. Ground Truth-Evaluering for Økonomi og Virksomhetsstyring

For å oppnå **0 % feiltoleranse på kritiske regnskapstall og rapportering**, må det etableres et kontrollert fasit-sett (*Ground Truth*).

### Oppbygging av Ground Truth-Testsett:
1. **Representative caser:** 30–50 historiske oppgaver (f.eks. avviksanalyser, oppslag i økonomireglement, bilagskontroller) utarbeidet av erfarne seniorøkonomer.
2. **Fasitsvar:** Hver oppgave inneholder:
   * *Forventet tekstuelt svar / konklusjon.*
   * *Eksakte kildehenvisninger (dokumentnavn, paragraf, sidetall).*
   * *Låste nøkkeltall og beløp.*

### Måleparametere i Automated Benchmarking:
* **Retrieval Precision & Recall:** Måler om RAG-søket henter ut de eksakt riktige kildedokumentene.
* **Faithfulness / Groundedness:** Måler om det genererte svaret KUN baserer seg på den uthentede konteksten (forhindrer hallusinasjoner).
* **Answer Relevance:** Måler om svaret direkte besvarer brukerens opprinnelige spørsmål uten avsporinger.

---

## 3. Akseptkriterier for Produksjonssetting (Gate G3)

Ingen modul eller ny versjon promoteres til produksjon før følgende krav er bestått:

- [x] **100 % pass-rate** på kritiske tallberegninger i Ground Truth-testsettet.
- [x] **Minst 90 % score** på Faithfulness og Retrieval Precision.
- [x] **0 % utslag** på PII-lekkasjetester (anonymiseringsfilter fungerer).
- [x] **Gjennomført og godkjent DPIA og FRIA** (inkludert MLOps-forvaltningsrutine).
- [x] **Aktiv audit logging** verifisert i AI Gateway.

---
*Dokumentet inngår i MLOps-implementeringspakken for kommunal sektor.*
