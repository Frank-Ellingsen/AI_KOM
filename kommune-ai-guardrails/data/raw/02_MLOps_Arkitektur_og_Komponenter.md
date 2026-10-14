# 02. Teknisk MLOps-Arkitektur og Komponenter

## 1. Målarkitektur for Enterprise MLOps
En robust MLOps-arkitektur for kommunal sektor er bygget opp som en **Control Plane-arkitektur** som skiller fagsystemer og sensitive data fra underliggende språkmodeller.

```
+-----------------------------------------------------------------------------------+
| 1. APPLIKASJONSLAG (ERP, Sak/Arkiv, AI-Kunnskapsassistent)                       |
+-----------------------------------------------------------------------------------+
                                      │ (SSO & Rollebasert tilgang)
                                      ▼
+-----------------------------------------------------------------------------------+
| 2. AI GATEWAY / CONTROL PLANE (PII-skjerming, Rate Limiting, FinOps, Audit Log)   |
+-----------------------------------------------------------------------------------+
                                      │
                   ┌──────────────────┴──────────────────┐
                   ▼                                     ▼
+------------------------------------+ +------------------------------------+
| 3. DATA & RAG PIPELINE             | | 4. MODEL ENGINE & INFERENCE        |
|    - Vector Database (Embeddings)  | |    - Lukkede EU-Sky Modeller       |
|    - ETL/ELT Sync (DVC)            | |      (Azure OpenAI EU / Mistral)   |
|    - Metadata & RBAC Arv           | |    - Spesialiserte ML-Modeller     |
+------------------------------------+ +------------------------------------+
                                      │
                                      ▼
+-----------------------------------------------------------------------------------+
| 5. MLOPS PLATFORM (MLflow, Model Registry, CI/CD, Observability, Kill-Switch)    |
+-----------------------------------------------------------------------------------+
```

---

## 2. Kjernekomponenter i Pipelinen

### A. Data Pipeline og Feature Store / Vector Store
* **ETL/ELT Integration:** Sikker synkronisering fra fagsystemer (f.eks. Visma/Unit4 ERP, Elements/ACOS sak-arkiv) til lukkede datalager.
* **PII-Anonymisering:** Automatiske filtre som anonymerer navn, fødselsnumre og skjermede personopplysninger før data indekseres.
* **Vector Database:** Indeksering av dokumenter, reglement og historiske rapporter som *embeddings* for kildeforankret RAG-søk.
* **Data Version Control (DVC):** Versionering av datagrunnlaget slik at endringer i kildedokumenter spores automatisk.

### B. AI Gateway (Det Sentrale Kontrollpunktet)
* **Modell-uavhengighet:** Isolering av fagsystemene fra leverandørspesifikke API-er (unngår *vendor lock-in*).
* **Tilgangskontroll (RBAC/ABAC):** Arv av brukerens tilgangsrettigheter fra Entra ID / FellesID.
* **Token- og Kostnadskontroll (FinOps):** Sett av budsjettak og kvoter per avdeling/prosjekt.

### C. Modellregister (Model Registry)
* Sentralt arkiv (f.eks. MLflow Model Registry) der godkjente modeller og RAG-indekser katalogiseres.
* Tydelige statuser: `Development` ➔ `Staging` ➔ `Production` ➔ `Archived`.
* Kun modeller med godkjent DPIA/FRIA-status og bestått Ground Truth-test kan promoteres til `Production`.

### D. CI/CD & Containerisering
* **Docker / Containerization:** Alle pipelines, mikrotjenester og evalueringstester pakkes i standardiserte Docker-containere.
* **Automatisert Deployment:** Endringer i kildekode eller prompt-maler utløser automatiske bygg- og evalueringstester via GitHub Actions / Azure DevOps.

---
*Dokumentet inngår i MLOps-implementeringspakken for kommunal sektor.*
