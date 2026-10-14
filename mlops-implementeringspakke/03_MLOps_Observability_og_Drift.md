# 03. MLOps Observability, Drift-Håndtering og FinOps

## 1. Observability i Produksjonsdrift
I tradisjonell IT holder det å overvåke om serveren er oppe (uptime/latency). I AI-systemer må man i tillegg overvåke **kvaliteten og semantikken i svarene**.

### Nøkkelmålinger for MLOps Dashbord:

```
+-----------------------------------------------------------------------------------+
|                            MLOPS OBSERVABILITY DASHBORD                           |
+---------------------+-------------------------------+-----------------------------+
| System & Ytelse     | Modellkvalitet & Semantikk    | Økonomi & FinOps            |
+---------------------+-------------------------------+-----------------------------+
| • Latency (TTFT)    | • Retrieval Accuracy (RAG)    | • Token-forbruk per dag     |
| • Error Rate (HTTP) | • Hallusinasjonsindeks (%)    | • Kostnad per forespørsel   |
| • Oppetid (SLA %)   | • Menneskelige overrides (%)  | • Avdelingsvis budsjettak   |
+---------------------+-------------------------------+-----------------------------+
```

---

## 2. Håndtering av Data Drift, Concept Drift og Prompt Drift

1. **Data Drift:**
   * *Hva er det?* Endringer i inndataene over tid (f.eks. nye kontoplaner i ERP eller endringer i innkjøpsavtaler).
   * *Tiltak:* Automatisert varsling når distribusjonen av inndata avviker fra trenings-/indekseringsgrunnlaget.
2. **Concept / Model Drift:**
   * *Hva er det?* Endringer i sammenhengen mellom inndata og forventet utdata (f.eks. ny tolkningspraksis i forvaltningsloven).
   * *Tiltak:* Utløse automatisert retrening/re-indeksering og ny validering mot Ground Truth-testsettet.
3. **Prompt & Model Version Drift:**
   * *Hva er det?* Oppdateringer fra modell-leverandøren (f.eks. at Azure OpenAI oppdaterer underliggende gpt-4o modellversjon) som endrer svarenes tone eller nøyaktighet.
   * *Tiltak:* Låse modellversjoner i AI Gateway og kjøre regresjonstester mot fasit-sett før versjonsoppgraderinger godkjennes.

---

## 3. FinOps og Kostnadsstyring

Siden LLM-tjenester avregnes per token (inndata/utdata), kreves det streng kostnadsstyring:
* **Rate Limiting:** Maksimalt antall forespørsler per minutt/time per bruker.
* **Token Caching:** Gjenbruk av RAG-embeddings og vanlige spørringer i hurtigbuffer for å redusere API-påkall.
* **Budsjett-alarmer:** Automatiske varsler til IT-direktør og økonomisjef ved 80 % og 100 % av månedlig budsjettramme.

---
*Dokumentet inngår i MLOps-implementeringspakken for kommunal sektor.*
