# 📊 Standardisert Rapporteringsmønster: Avvik, Årsak, Action og Effektprognose

**Dokument-ID:** MAL-AVVIK-EFFEKT-001  
**Versjon:** 1.0  
**Gjelder:** Alle ledelsesnivåer (Fra Enhetsleder til Bystyret), Kristiansand kommune  
**Standard:** Krav om obligatorisk 4-punkts struktur for alle måneds- og tertialrapporter  

---

## 1. Det Obligatoriske 4-Punkts Mønsteret

For å sikre at alle rapporter er handlingorienterte og gir ledelsen et realistisk styringsgrunnlag, skal alle avviksnotater bygges opp etter denne faste 4-stegs strukturen:

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 1. AVVIK HITTIL I ÅR (YTD Variance)                                             │
│    • Presist avvik i kroner og prosent mot periodisert budsjett i Visma ERP     │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 2. ÅRSAK TIL AVVIK (Root Cause Analysis - Glass-Box RAG)                         │
│    • Dypdykk i underliggende drivere (sykefravær, NAV-etterslep, prisstigning)   │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 3. FORSLAG TIL ACTION (Corrective Action Plan)                                   │
│    • Prioriterte strakstiltak (0–30 d) og strukturelle tiltak (30–90 d)          │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 4. KVANTIFISERT EFFEKT PÅ PROGNOSEBANE OG EOY BALANSE                            │
│    • Eksakt beregning av hvordan tiltaket endrer helårsresultatet per 31.12      │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Detaljert Beskrivelse av Komponentene

### Component 1: Avvik hittil i år (YTD Variance)
* **Datakilde:** Automatisk uthenting fra `Fact_Regnskap` vs `Fact_Budsjett` i Visma ERP.
* **Format:** `[Avvik i NOK] ([Avvik i %])`
* **Eksempel:** `+1 240 000 NOK (+12.4 % merforbruk per 31.08)`

### Component 2: Årsak til avvik (Root Cause Analysis)
* **Metode:** RAG Glass-Box analyse som krysskobler regnskapsarter (art 1020 vikarer, art 1600 NAV-refusjoner, art 1090 overtid) med HR-data og fagsystemer.
* **Kildeforankring:** Må referere til spesifikke kontoklasser, KOSTRA-funksjoner og avviksutløsende hendelser.

### Component 3: Forslag til Action (Tiltaksplan)
* **Strakstiltak (0–30 dager):** Umiddelbare operative grep (f.eks. inndragning av ubesatte stillinger, intensivert purring på NAV-refusjoner, vikarstopp).
* **Strukturelle tiltak (30–90 dager):** Omdisponeringer innenfor rammen, klassesammenslåing eller justering av tjenestenivå.
* **Politiske tiltak (> 90 dager):** Omdisponeringer på tværs av kommunalsjefområder eller bruk av disposisjonsfond som krever Bystyrevedtak.

### Component 4: Kvantifisert Effekt på Prognosebane og EOY Balanse (End of Year Balance)
* **Metode:** Prediktiv Monte Carlo tidsserieanalyse.
* **Effektberegning:**
  * **Uten tiltak (Status Quo Prognose):** Forventet helårsavvik per 31.12 (p50 Worst/Expected).
  * **Med tiltak (Korrigerende Prognosebane):** Innsparingseffekt i kroner.
  * **End-of-Year Balanse (EOY Netto):** Resultat ved årets slutt etter iverksatte tiltak.

---

## 3. Eksempel på Utfylt Rapporteringselement (Enhet 202 Grunnskole)

```markdown
### 📍 Avviks- og Tiltaksrapport: Enhet 202 Grunnskole (Per September M9)

* **1. Avvik hittil i år (YTD):**
  * Periodisert budsjett: 10 000 000 NOK
  * Regnskap hittil: 11 240 000 NOK
  * **YTD Avvik: +1 240 000 NOK (+12.4 % merforbruk)** [🔴 RØD ALARM]

* **2. Årsak til avvik:**
  * Høyt sykefravær i K1 og K2 (14.2 % mot normalt 7.0 %) har medført uvanlig høyt vikarforbruk på art 1020 (Vikarer).
  * Samtidig har NAV-saksbehandlingstid ført til etterslep på inntektsføring av sykepengerefusjoner på art 1600 (410 000 NOK utestående).

* **3. Forslag til Action:**
  1. *Strakstiltak (0-30d):* Etablere ukentlig purreroutine mot NAV for art 1600.
  2. *Operativt tiltak (30-60d):* Gjennomføre intern klassesammenslåing ved korttidsfravær i stedet for å leie inn eksterne vikarer.
  3. *Budsjettmessig tiltak:* Fremme sak om omdisponering av 500 000 NOK fra enhetens udisponerte driftsmidler i T2.

* **4. Kvantifisert Effekt på Prognosebane og EOY Balanse:**
  * **Prognose uten tiltak (31.12):** +1 850 000 NOK merforbruk.
  * **Kvantifisert effekt av tiltak 1-3:** -1 250 000 NOK innsparing/refusjon.
  * **Revidert EOY Balanse per 31.12:** +600 000 NOK merforbruk (Dekkes inn innenfor sektorens samlede ramme jf. Kommuneloven § 14-5).
```

---

## 4. Betydning for Kommunerevisjonen (Stage-Gate Port 9)

Hver genererte avviks- og effektrapport lagrer en **SHA-256 hash** i databasen. Dette sikrer at Kommunerevisjonen og Kontrollutvalget i ettertid kan verifisere at de forutsatte tiltakene faktisk ble fulgt opp og at prognoseberegningene var metodisk forsvarlige.
