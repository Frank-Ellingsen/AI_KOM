# 01. MLOps og LLMOps i Offentlig Sektor: Oversikt og Prinsipper

## 1. Innledning
Machine Learning Operations (MLOps) og Large Language Model Operations (LLMOps) utgjør den operasjonelle og teknologiske ryggraden for bærekraftig bruk av kunstig intelligens i offentlig sektor og kommunal økonomistyring. 

Tradisjonell programvareutvikling (DevOps) håndterer kode og infrastruktur. MLOps utvider dette ved å håndtere en treveis avhengighet mellom **kode, data og modeller**. I offentlig sektor er dette avgjørende for å gå fra uformelle teknologipiloter til trygg, skalerbar og regelverkskonform produksjonsdrift.

---

## 2. Forskjellen på DevOps, MLOps og LLMOps

| Dimensjon | Tradisjonell DevOps | Classic MLOps (Prediktiv AI) | LLMOps (Generativ AI & RAG) |
| :--- | :--- | :--- | :--- |
| **Kjerneelementer** | Kode, Konfigurasjon | Kode, Data, ML-Modeller | Kode, Data, Prompt, RAG-Index, LLM |
| **Endringsårsak** | Endringer i kildekode | Data drift & Model drift | Prompt drift, Kunnskapsendringer, RAG-oppdatering |
| **Testing & Kvalitet** | Unit tests, Integration tests | Presisjon, Recall, F1-score | Ground Truth, Hallusinasjonsmåling, XAI |
| **Etterlevelse** | IT-sikkerhet, Personvern | GDPR, Bias-analyser | EU AI Act (Deployer-krav), FRIA, Logging |

---

## 3. Kjørneprinsipper for Kommunal MLOps

1. **Automatiserte Pipelines:** Erstatte manuelle skript og ad-hoc kjøringer med kodebaserte og gjenbrukbare pipelines fra datainntak til modellbygging og evaluering.
2. **Kildesporbarhet og Reproduserbarhet:** Enhver rapport, prognose eller avviksanalyse produsert av et AI-system skal kunne rekonstrueres ved å kjenne eksakt hvilken kildekode, datakilde, modellversjon, system-prompt og RAG-indeks som ble benyttet.
3. **Menneskelig Kontroll (Human-in-the-Loop):** AI-systemer i økonomi og saksbehandling skal være leseorienterte (read-only) og levere forslag til utkast. Ingen direkte skriveoperasjon til fagsystem/ERP skjer uten godkjenning fra fagansvarlig.
4. **Sikkerhet og Datakontroll (Control Plane):** Alle modellforespørsler sluses gjennom en AI Gateway som håndterer PII-skjerming, SSO (Entra ID), tilgangsstyring (RBAC) og audit logging.
5. **Kontinuerlig Overvåking og Nødknapp (Kill-Switch):** Løpende måling av svarpresisjon, latency, kostnader (FinOps) og mulighet for umiddelbar utkobling dersom systemet avviker.

---

## 4. Livsløp for Kommunale AI-modeller

```
[Datainntak & PII-vasking] ➔ [RAG-Indeksering / Trening] ➔ [Validering mot Ground Truth]
                                                                  │
                                                                  ▼
[Produksjonsdrift / Monitoring] ◄── [CI/CD Deployment] ◄── [Modellregister & AI Gateway]
```

---
*Dokumentet inngår i MLOps-implementeringspakken for kommunal sektor.*
