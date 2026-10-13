# Technical Specification: Native Power BI & Excel EPM Architecture

## 1. Oversikt og Filosofi
For å sikre 100 % fremtidssikkerhet, lisensuavhengighet og lavest mulig forvaltningskostnad i Kristiansand kommune, benyttes utelukkende **standard innebygd funksjonalitet (out-of-the-box)** i Microsoft Power BI og Microsoft Excel. Ingen tredjeparts plugins eller isolerte spesialkomponenter tillates.

---

## 2. Power BI Innebygde Analysekomponenter

### A. Dekomponeringstre (Decomposition Tree)
* **Formål:** Automatisk rotårsaksanalyse (*root-cause analysis*) for avvik i regnskap og rammer.
* **Oppsett i Power BI Desktop:**
  * **Analyze:** `[Avvik YTD Korrigert]`
  * **Explain By:**
    1. `Sektor[Sektornavn]`
    2. `Funksjon[KOSTRA Funksjon]` (f.eks. KOSTRA 202 Grunnskole)
    3. `Enhet[Tjenestedistrikt / Skole]` (f.eks. Wilds Minne Skole)
    4. `Konto[KOSTRA Art]` (f.eks. Art 1020 Vikarutgifter vs. Art 1690 NAV-refusjon)
* **AI-funksjonalitet:** Brukeren kan klikke `+` og velge **"High Value"**. Power BI finner automatisk den enheten eller arten som bidrar mest til merforbruket.

### B. Tidsserieprognose (Forecasting in Line Chart)
* **Formål:** Projisere forventet årsresultat (EOY) basert på historiske mønstre.
* **Oppsett i Analytics Pane:**
  * **X-akse:** `Dato[Måned]` (24–36 måneders historikk)
  * **Y-akse:** `[Faktisk Regnskap]` og `[Avvik YTD Korrigert]`
  * **Forecast length:** 6 måneder (frem til 31.12)
  * **Confidence Interval:** 95 % usikkerhetsvifte
  * **Seasonality:** 12 måneder (fanger opp sommerferie- og høst-effekter)

### C. What-If Parametre & Felt-parametre (Numeric Range Parameters)
* **Formål:** Interaktiv simulering av rammeendringer og tiltakseffekter i sanntid.
* **Parameter 1: `Framsikt Deflator %`** (0,02 til 0,06, standard 0,041 / 4,1 %)
* **Parameter 2: `Fraværstiltak Reduksjon %`** (0,00 til 0,03, standard 0,015 / 1,5 %)
* **Dynamisk DAX-simulering:**
  ```dax
  [Simulert EOY Netto Driftsresultat] = 
  VAR OpprinneligRamme = SUM('Framsikt Budsjett'[Vedtatt Ramme])
  VAR DeflatorTillegg = OpprinneligRamme * [Framsikt Deflator Value]
  VAR VikarInnsparing = SUM('Visma Regnskap'[Art 1020 Vikar]) * [Fraværstiltak Effektreduksjon Value]
  RETURN
      [Bokført Resultat YTD] + DeflatorTillegg + VikarInnsparing + [ERP NAV Refusjon Etterslep]
  ```

---

## 3. Excel Innebygde Standardkomponenter

### A. Slicere (Utsnittskuttere) & Tidslinjer
* Interaktive filtreringsknapper for *Sektor*, *Status (RAG)* og *Visma Støy-nøytralisering (PÅ/AV)*.

### B. Gruppering & Disposisjon (Hierarkisk Drill-Down)
* Bruk av Excels standard `Data ➔ Group / Outline` (`+` / `-` knapper) for sømløs navigasjon fra Nivå 1 (Sektor) til Nivå 2 (KOSTRA-funksjon) og Nivå 3 (Enhet).

### C. Betinget Formatering (Data Bars & RAG Symboler)
* **In-Cell Data Bars (`DataBarRule`):** Viser visuelle avviksbars direkte inne i cellen uten å forstyrre tallene.
* **RAG Icon Sets (`IconSetRule`):** Standard 🔴 🟡 🟢 ikoner koblet mot en egen redigerbar `Parametre`-fane (Ingen hardkoding).
