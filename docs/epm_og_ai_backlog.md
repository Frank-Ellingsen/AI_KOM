# Kristiansand Kommune — EPM & AI Prosjektbacklog og MS Teams Oppgavebehandling

Dette dokumentet inneholder den overordnede prosjektbacklogen, grensesnitt- og layoutspesifikasjonen for **Microsoft Teams / MS Planner**, samt en **spesifisert backlog spisset mot neste tidsfrist i det kommunale årshjulet (2. tertialrapport 2026 & HØP 2027–2030 forberedelser)**.

---

## 💻 1. MS Teams Layout & Grensesnittarkitektur

For å sikre at ledere, økonomirådgivere og gatekeepere har én samlet digital arbeidsflate, integreres EPM- og AI-styringen direkte i **Microsoft Teams** med oppgavebehandling via **MS Planner / Tasks by Planner**:

```text
[ MS TEAMS TEAM: "KRISTIANSAND EPM & AI STYRING" ]
│
├── 💬 Kanal 1: Generelt (Central Hub, kunngjøringer, toppleder-status)
├── 📊 Kanal 2: 01-Økonomistyring-og-Rapportering (Power BI, Visma vs Framsikt)
├── 🛡️ Kanal 3: 02-AI-Governance-og-StageGate (Port 1-10, DPIA/FRIA, Audit Trail)
└── 🗓️ Kanal 4: 03-Årshjul-og-Oppgaver (MS Planner Task Board)
```

### 📱 **Fane-struktur i MS Teams (Tabs):**
1. **Fane 1: `📊 Dashboard (Power BI)`** — Live EPM Matrise med Slicere, Dekomponeringstre og What-If parametre.
2. **Fane 2: `📋 Oppgaver & Backlog (MS Planner)`** — Kan-ban tavle med bøtter (Buckets), RAG-prioritering og tidsfrister.
3. **Fane 3: `📂 Filer & Dokumenter (SharePoint)`** — Word-sjekklister (`.docx`), Excel-modeller (`.xlsx`) og PowerPoint-dekk (`.pptx`).
4. **Fane 4: `🛡️ Stage-Gate Sjekkliste (MS Lists)`** — Interaktiv status for Port 1 til 10 med godkjenningsknapper.

---

## 🗂️ 2. MS Planner Board Structure (Tavleoppsett i Teams)

Oppgavebehandlingen i MS Planner organiseres i **5 Bøtter (Buckets)** som speiler utviklingsløpet fra idé til utrulling:

```text
[ BØTTE 1: Innboks & Idéer ] ──► [ BØTTE 2: Neste Tidsfrist (T2 2026) ] ──► [ BØTTE 3: AI Governance ]
                                                                                   │
                                                                                   ▼
[ BØTTE 5: Produksjon & Drift ] ◄───────────────────────────────────── [ BØTTE 4: Framsikt HØP ]
```

* **Bøtte 1: 📋 Innboks & Idéavklaring (Port 1–2 / PAD):** Nyttevurdering, pre-screening og klassifisering jf. EU AI Act.
* **Bøtte 2: 🏃 NESTE TIDSFRIST: 2. Tertialrapport 2026 (Sprint Bøtte):** Kritiske oppgaver med frist i august/september.
* **Bøtte 3: 🛡️ AI Governance & Kvalitetsporter (Port 3–7 / POR Pilot & Optimize):** DPIA/FRIA, PII-vask, sandkassetest og HITL-tildeling.
* **Bøtte 4: 📈 Framsikt HØP 2027–2030 Forberedelser:** Rammefordeling, demografiparametre og deflatorberegning.
* **Bøtte 5: 🚀 Produksjon & Drift (Port 8–10 / POR Rollout):** Algoritmeregister, SHA-256 audit-logging og overvåking.

---

## 🎯 3. Spesifisert Backlog for NESTE Tidsfrist i Årshjulet: 2. Tertialrapport 2026

**Mål for Neste Årshjul-Sprint:** *"Kvalitetssikre og nøytralisere Visma ERP-støy i 2. tertial, innarbeide RNB 4,1 % Framsikt-deflator, og fullføre Gate 5–7 for Controller AI Portal før saksfremlegg til Bystyret."*

### 📋 **Sprint Backlog Items (Tidsfrist: August / September 2026):**

| ID | Oppgave / User Story | Kategori / System | Ansvarlig | Pri | Gate / Fase | Status |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **T2-01** | **Avstemme Visma Art 1690 vs Art 1020:** Kjøre automatisert avstemming av vikarkostnader mot beregnet NAV-refusjonskrav for mai–august. | Visma ERP / EPM | Controller | 🔥 Høy | Port 4 | ⏳ Pågår |
| **T2-02** | **Oppdatere Framsikt Deflator (RNB 4,1 %):** Importere oppjustert deflator (156 mill. kr) i Framsikt og fordela på skole, helse og byutvikling. | Framsikt API | Økonomirådgiver | 🔥 Høy | Årshjul T2 | 🟢 Fullført |
| **T2-03** | **Kjøre Port 5 (DPIA/FRIA) for T2 AI-Avviksdiagnose:** Fullføre samordnet personvern- og rettighetsvurdering for AI-tekstgenerering i saksfremlegget. | Governance / DPO | Juridisk / DPO | 🔥 Høy | Port 5 | ⏳ Pågår |
| **T2-04** | **Formell Tildeling av HITL-Ansvar (Port 7):** Oppnevne navngitte saksbehandlere som skal overprøve AI-forslag før T2-behandling i formannskapet. | Menneskelig Tilsyn | Økonomidirektør | 🟡 Med | Port 7 | 🟢 Fullført |
| **T2-05** | **Generere 10-Sekunders Visuals i Power BI:** Konfigurere Waterfall-bro og Bullet Charts for T2-rapporten med RAG-symboler. | Datavisualisering | BI-Utvikler | 🟡 Med | Best Practice | 🟢 Fullført |
| **T2-06** | **Etablere SHA-256 Audit Log for T2-analyser:** Verifisere at alle AI-genererte avviksanalyser lagres uforanderlig i `Audit_AI_Actions`. | IT / Sikkerhet | Systemansvarlig | 🟡 Med | Port 9 | ⏳ Pågår |
| **T2-07** | **Klargjøre Framsikt HØP 2027–2030 Rammemodell:** Sette opp What-If parametre i Excel/Power BI for rammekutt vs. demografivekst. | Framsikt / FP&A | Controller | 🔵 Lav | Årshjul HØP | ⏳ Pågår |

---

## 🏛️ 4. Overordnet EPM & AI Prosjektbacklog (Epics & Feature Backlog)

### **Epic 1: Dataintegrasjon & Automatisering (Visma & Framsikt)**
* **US-1.1:** Etablere daglig inkrementell innlasting med 60-dagers rullende vindu for Visma regnskap. *(Status: Fullført)*
* **US-1.2:** Konfigurere nattlig Framsikt Batch reload med Delta `MERGE` for rammer og deflatorer. *(Status: Fullført)*
* **US-1.3:** Bygge automatisert avstemmingsmåler `[ERP NAV Refusjon Etterslep]` i DAX. *(Status: Fullført)*

### **Epic 2: AI Governance & Stage-Gate Etterlevelse (EU AI Act & GDPR)**
* **US-2.1:** Implementere 10-stegs Stage-Gate prosess med formelle beslutningsporter. *(Status: Fullført)*
* **US-2.2:** Integrere lokal PII-vask (`pii_scrubber`) for å anonymisere fødselsnummer før AI-analyse. *(Status: Fullført)*
* **US-2.3:** Opprette uforanderlig SHA-256 audit-logg i databasen for Kommunerevisjonen. *(Status: Fullført)*
* **US-2.4:** Publisere kommunens AI-systemer i offentlig Algoritmeregister (Eurocities-standard). *(Status: Planlagt for Gate 10)*

### **Epic 3: Best Practice Visualisering & MS Teams Integration**
* **US-3.1:** Implementere 10-sekunders regelen med aksjonstitler og RAG-fargekoding (`#1B365D` / `#4A77A0`). *(Status: Fullført)*
* **US-3.2:** Bygge interaktiv Power BI rapport med Dekomponeringstre, Prognose og What-If parametre. *(Status: Fullført)*
* **US-3.3:** Sette opp MS Teams arbeidsflate med Planner-bøtter, kanaler og faneintegrasjon. *(Status: Fullført)*
