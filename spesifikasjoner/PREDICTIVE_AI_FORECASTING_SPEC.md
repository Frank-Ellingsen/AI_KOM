---
title: "Prediktiv AI & Scenariomodellering i Kommunal Økonomi"
domain: "spesifikasjoner"
category: "prediktiv-ai"
author: "Frank Ellingsen"
statutory_references:
  - "Kommuneloven § 14-5"
  - "Statens Prosjektmodell (KS2 / P50/P85)"
  - "EU AI Act Art. 26/86"
summary: "Teknisk og finansiell spesifikasjon for rullende EOY-prognoser, Monte Carlo P10/P50/P90 usikkerhet, EVM prosjektkontroll (BAC, EAC, ETC, CPI, SPI) og SHA-256 forsegling."
keywords: ["prediktiv AI", "prognoser", "Monte Carlo", "EVM", "EAC", "ETC", "CPI", "KS2", "P50", "P85", "Tufte"]
---

# 📊 Spesifikasjon: Prediktiv AI & Scenariomodellering i Kommunal Økonomi (`PREDICTIVE_AI_FORECASTING_SPEC.md`)

> **System:** Kommune AI Guardrails – Kristiansand kommune  
> **Modul:** Prediktiv AI, Trendanalyse, Project Controlling (EVM) & Økonomisk Fremskriving  
> **Målgruppe:** Frank Ellingsen (Senior Financial & Project Controller), Kommunalsjefer, Kommunedirektøren  
> **Standarder:** Kommuneloven § 14-5 | Statens Prosjektmodell (KS2 / P50/P85) | Edward Tufte Data-Ink Ratio | EU AI Act Art. 26/86  
> **Sist oppdatert:** Oktober 2026

---

## 1. Innledning & Formål

Målet med den prediktive AI-spesifikasjonen er å transformere kommunens økonomi- og prosjektstyring fra **reaktiv historisk rapportering** til **proaktiv, sannsynlighetsbasert fremskriving**. 

I stedet for kun å rapportere historiske regnskapstall per tertial, etablerer løsningen:
1. **Driftsprognoser (Operational Run-Rate):** Sesongjustert tidsserieanalyse og driverbasert Monte Carlo-simulering for driftsutgifter (lønn, vikarer, overtid, varer/tjenester).
2. **Prosjektkontroll & Investering (EVM / KS2):** Formell Earned Value Management-prognostisering ($EAC$, $ETC$, $VAC$) koblet mot usikkerhetsanalyser (P50/P85) for kommunale investerings- og anleggsprosjekter.
3. **Scenariomodellering (What-If):** Hurtigtesting av politiske og administrative tiltak for å sikre balanse jf. **Kommuneloven § 14-5**.

---

## 2. Dobbeltløps Arkitektur for Prediktiv Økonomistyring

```text
                                        ┌──► [ MODUS 1: DRIFTSPROGNOSE (SESONG & DRIVERE) ]
                                        │    ├─ Visma Månedsregnskap + KOSTRA Sesongvekter
                                        │    ├─ Driverbasert Monte Carlo (10 000 løp)
                                        │    └─ p10 (Stramt) / p50 (Forventet) / p90 (Konservativt)
[ Visma ERP Transaksjoner ] ──┐         │
[ Framsikt EPM Budsjett ]  ───┼──► [ ETL & PII-Vask ]
[ KOSTRA SSB Historikk ]   ───┤    (Port 4 Guardrail)
[ Prosjektregnskap (WBS) ] ───┘         │
                                        └──► [ MODUS 2: PROSJEKTKONTROLL & EVM (KS2) ]
                                             ├─ BAC, PV, EV, AC, CPI, SPI per prosjekt
                                             ├─ Statistisk EAC = AC + (BAC - EV) / (CPI * SPI)
                                             └─ Usikkerhetsavsetning P50 vs. P85 kostnadsramme
                                                                │
                                                                ▼
                                                [ KRITISK AVVIKSDETEKSJON ]
                                                (Flagg ved p50-avvik > 500k kr jf. § 14-5)
                                                                │
                                                                ▼
                                                [ KRYPTOGRAFISK REVISJONSSPOR ]
                                                (SHA-256 Hash -> Fact_Prognose_Logg & Port 9)
                                                                │
                                                                ▼
                                                [ KONSUMASJON & DASHBOARD ]
                                                ├─ Control Office Hub UI (Tufte Fan Charts)
                                                ├─ Streamlit Scenariomodell (Port 8501)
                                                └─ Power BI Parquet Eksport
```

---

## 3. Metodisk & Algoritmisk Modellering

### 3.1. Modus 1: Driftsprognose (Driverbasert Monte Carlo)
Kommunale driftsutgifter følger en systematisk årssyklus. Enkeltstående lineære ekstrapoleringer feiler fordi feriepenger utbetales i juni, juli har lav aktivitet, og vikarforbruk topper seg ved influensasesong og skolestart i Q3/Q4.

1. **Sesongjustering ($S_m$):**
   Historiske vekter $S_m$ per måned $m \in \{1, \dots, 12\}$ der $\sum_{m=1}^{12} S_m = 1.0$.
2. **Driverbasert simulering for gjenstående periode ($ETC$):**
   I stedet for statisk normalstøy, simuleres usikkerheten i faktiske kostnadsdrivere:
   * **Sykefravær ($f$):** Modellert via Beta-fordeling kalibrert mot historisk fravær i Kristiansand (snitt 8,5 %, spenn 6,5 % – 12,0 %).
   * **Vikarpris- og overtidstillegg ($p$):** Lognormalfordeling for innleiepriser og tariffpåslag.
   * **NAV Refusjonsetterslep ($r$):** Forsinkelse i mottak av refusjoner for ressurskrevende tjenester.
3. **Utfallsprofil:**
   $$ETC_i = \left( BAC \cdot \sum_{m=\text{aktuell}+1}^{12} S_m \right) \cdot \left(1 + \beta_{\text{vikar}} (f_i - f_{\text{basis}})\right) \cdot p_i - r_i$$
   $$EOY_i = AC_{\text{YTD}} + ETC_i$$
   Fra 10 000 simulerte utfall hentes:
   * **p10 (Optimistisk utfall):** 10 % sannsynlighet for at kostnadene blir lavere.
   * **p50 (Forventet sluttresultat):** Grunnlag for tertialrapportering.
   * **p90 (Konservativt risikoutfall):** Grunnlag for nødvendig buffer og fondsavsetning.

---

### 3.2. Modus 2: Prosjektkontroll & EVM (Investering & Anlegg)
For kommunens investeringsportefølje (skolebygg, helsehus, VA-ledningsnett, digitalisering) anvendes Earned Value Management i henhold til **FAST Standard** og **Statens Prosjektmodell (KS2)**:

| Måltall | Betegnelse | Formel / Beregning | Faglig Betydning for Controller |
| :--- | :--- | :--- | :--- |
| **BAC** | Budget at Completion | Vedtatt totalramme | Prosjektets styringsramme vedtatt av Bystyret. |
| **PV** | Planned Value | $\text{Periodisert budsjett YTD}$ | Planlagt verdiskaping til nå. |
| **EV** | Earned Value | $BAC \times \text{Fysisk ferdigstillelse \%}$ | Faktisk godkjent opptjent verdi i felt. |
| **AC** | Actual Cost | Faktisk bokført kostnad | Uthentet direkte fra Visma Prosjektregnskap. |
| **CV** | Cost Variance | $EV - AC$ | Negativ verdi = overskridelse mot levert arbeid. |
| **SV** | Schedule Variance | $EV - PV$ | Negativ verdi = tidsmessig forsinkelse. |
| **CPI** | Cost Performance Index | $EV / AC$ | Kostnadseffektivitet ($<1.0$ indikerer merforbruk). |
| **SPI** | Schedule Performance Index | $EV / PV$ | Fremdriftsindeks ($<1.0$ indikerer forsinkelse). |
| **EAC** | Estimate at Completion | $AC + \frac{BAC - EV}{CPI \times SPI}$ | Sluttprognose som vekter både kostnad og tid. |
| **ETC** | Estimate to Complete | $EAC - AC$ | Gjenstående kapitalbehov for ferdigstillelse. |
| **VAC** | Variance at Completion | $BAC - EAC$ | Estimert sluttoverskridelse eller besparelse. |
| **P85** | Kostnadsramme KS2 | $EAC_{\text{p50}} + \text{Usikkerhetsavsetning}$ | Formell kostnadsramme overfor Bystyret. |

---

## 4. Edward Tufte Data-Ink Visualiseringsstandard

Visualisering av prognoser i Control Office Hub og Streamlit skal følge Edward Tuftes prinsipper:

1. **Viftediagram (Fan Charts for Drift):**
   * **Ingen 3D-ribboner, ingen tunge gradienter, ingen bakgrunnsrutenett.**
   * p10–p90 usikkerhetsbåndet tegnes i en dempet lys nøytral farge (`rgba(30, 41, 59, 0.08)`).
   * p50-banen tegnes som en distinkt, mørkeblå heltrukket linje (`#1B365D`, 2px).
   * Vedtatt budsjettramme tegnes som en tynn, horisontal stiplet referanselinje (`#64748B`, 1px).
   * **Direkte merking:** Verdiene for p10, p50 og p90 merkes direkte ved linjeenden på 31.12 fremfor i en separat tegnforklaring.
   * **Rød markering:** Rød farge (`#C0392B`) benyttes **kun** på arealet der p50 overstiger budsjettrammen.

2. **S-kurver for Prosjekter (Investering):**
   * PV-kurve (planlagt fremdrift): Grå stiplet linje (`#94A3B8`).
   * EV-kurve (opptjent fremdrift): Heltrukket mørkeblå linje (`#1B365D`).
   * AC-kurve (faktiske kostnader): Heltrukket oransje/rød linje ved avvik (`#D97706`).
   * Fjern vertikale rutelinjer. Behold kun horisontale beløpsmarkører med god avstand.

---

## 5. Databasestruktur: DDL for Prognosearkiv (`kommune_golden_record.db`)

For å ivareta full sporbarhet og revisjonskontroll lagres samtlige prognosekjøringer i databasen:

```sql
-- Hovedlogg for godkjente og beregnede prognoser
CREATE TABLE IF NOT EXISTS Fact_Prognose_Logg (
    prognose_id TEXT PRIMARY KEY,
    ansvar_kode TEXT NOT NULL,
    kostra_funksjon TEXT,
    art_kategori TEXT,
    periode_ytd INTEGER NOT NULL, -- f.eks. 8 (august / T2)
    regnskapsar INTEGER NOT NULL,  -- f.eks. 2026
    modell_type TEXT NOT NULL,     -- 'DRIVER_MONTE_CARLO', 'HOLT_WINTERS', 'EVM_KS2'
    hittil_regnskap_ac REAL NOT NULL,
    vedtatt_ramme_bac REAL NOT NULL,
    p10_belop REAL NOT NULL,
    p50_belop REAL NOT NULL,
    p90_belop REAL NOT NULL,
    estimert_avvik_p50 REAL NOT NULL,
    cpi REAL,
    spi REAL,
    status TEXT NOT NULL,          -- 'I_RUTE', 'OBSERVASJON', 'KRITISK_MERFORBRUK'
    driver_forutsetninger JSON,    -- {"sykefravaer": 0.084, "vikarpris_stot": 1.05, "rente": 0.045}
    saksbehandler TEXT NOT NULL,   -- 'Frank Ellingsen'
    sha256_hash TEXT NOT NULL,
    opprettet_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ansvar_kode) REFERENCES Dim_Ansvar(ansvar_kode)
);

-- Underliggende simuleringsdistribusjon for viftediagram
CREATE TABLE IF NOT EXISTS Fact_Forecast_Simulations (
    sim_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prognose_id TEXT NOT NULL,
    persentil INTEGER NOT NULL,    -- 10, 25, 50, 75, 90
    maned INTEGER NOT NULL,        -- 1 til 12
    simulert_belop REAL NOT NULL,
    FOREIGN KEY (prognose_id) REFERENCES Fact_Prognose_Logg(prognose_id)
);
```

---

## 6. Stage-Gate Governance & Lovhjemmel

| Stage-Gate Port | Krav i Prediktiv Modell | Hjemmel / Standard |
| :--- | :--- | :--- |
| **Port 4 (PII-Vask)** | All aggregering må skje på konto-/arts-/stillingskodenivå. Ingen ansatt-ID eller fødselsnumre tillates i feature-vektorene. | GDPR Art. 5 (Dataminimering) |
| **Port 8 (Glass-Box)** | Enhver prognose som overstiger rammen må automatisk generere sitat til **Kommuneloven § 14-5** om plikt til budsjettrevisjon. | Kommuneloven § 14-5 |
| **Port 9 (SHA-256 Audit)**| Hele prognoseresultatet (forutsetninger + utfall) hashes med SHA-256 og lagres uforanderlig i `Fact_Prognose_Logg`. | EU AI Act Art. 26(6) |
| **Port 10 (Transparens)**| Modellen kan ikke benytte "Black Box" dype nevrale nett uten forklarbarhet. Kun åpne statistiske modeller (Holt-Winters, Monte Carlo, EVM). | Eurocities Algorithmic Standard |

---

## 7. Integrasjonsgrensesnitt

1. **Python / DuckDB:** Kjører Monte Carlo-simuleringen på in-memory tabeller på under 200 ms.
2. **Control Office Hub (`index.html`):** Viser oppdaterte nøkkeltall og gir direkte nedlastingslenker til prognoserapporter.
3. **Streamlit UI (`app/office_hub_app.py`):** Interaktiv scenariomodellering der rådgivere kan justere fraværsskyvere og se viftediagrammet endre seg i sanntid.
4. **Excel & Power BI:** Automatisk eksport til `reports/Kommune_Project_Controller_Reporting_2026.xlsx` og Parquet-filer i `erp_data/parquet_exports`.
