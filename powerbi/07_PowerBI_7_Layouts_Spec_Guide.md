# 📊 Power BI 7 CFO & Controller Dashboards: Implementasjonsguide

Dette dokumentet beskriver den operative oppbyggingen av de 7 standardiserte rapportlayoutene for Kristiansand kommune i Power BI Service, optimalisert for Tufte Data-Ink standard og FT Visual Storytelling.

---

## 🏛️ Layout 1: Executive CFO Control Panel (Toppledelse)
* **Målgruppe:** Kommunedirektør Camilla Dunsæd, Økonomidirektør & Finansutvalget.
* **Hovedhensikt:** Rask 10-sekunders situasjonsforståelse av kommunens samlede finansielle helse.
* **Nøkkelvisualer:**
  1. **4 Topp-kort (Tufte Cards):** Netto driftsresultat (1,75 % mål), Disposisjonsfond (kr 412 mill. / 8,2 %), YTD Budsjettavvik (+ kr 14,2 mill.), Forventet EOY Sluttbalanse (+ kr 2,8 mill.).
  2. **Viftediagram (Fan Chart):** Månedlig bane fra januar til desember med konfidensintervaller for P10 (Målsetting), P50 (Base case) og P90 (Worst case).
  3. **Sektorvis Avviksstolpe (Diverging Bar):** Horisontale stolper per sektor (Oppvekst, Helse, Byutvikling, Kultur) med fargekoding (Rød ved > 5 % avvik).
* **Interaksjon:** Klikk på en sektor filtrerer automatisk viftediagrammet og underliggende avviksmatrise.

---

## 🏫 Layout 2: Sektor Oppvekst & Grunnskole
* **Målgruppe:** Kommunalsjef Oppvekst, Skolesjefer og Rektorer.
* **Hovedhensikt:** Detaljert oppfølging av elevtallsrammer, lærertetthet og vikarbruk.
* **Nøkkelvisualer:**
  1. **Elevtall vs. Rammeforbruk per skole (Scatter / Bubble):** Viser avvik i forhold til elevtallsutvikling (GSI-data).
  2. **Vikarutvikling (Line Chart med månedlig terskel):** Månedlig forbruk på konto 1020 med markering for sesongtopper (mai/juni).
  3. **Skolematrise med Drill-down:** Hierarkisk tre fra Sektor Oppvekst ➔ Skoleklynge ➔ Enhet (f.eks. Enhet 202 Grunnskole) ➔ KOSTRA Kontoart (1010, 1020, 1090, 1600).

---

## 🏥 Layout 3: Sektor Helse & Mestring
* **Målgruppe:** Kommunalsjef Helse, Boenhetsledere og Soneledere hjemmetjeneste.
* **Hovedhensikt:** Kontroll på turnus, overtid, sykefravær og institusjonsplasser.
* **Nøkkelvisualer:**
  1. **Sykefravær vs. Vikarutgifter (Diverging Bar):** Sammenligner fraværsdager med faktiske innleieutgifter per boenhet.
  2. **Sykehusutskrivings-etterslep (Kommuneoverliggere):** Døgnkostnader påløpt som følge av forsinket overføring fra Sørlandet sykehus HF.
  3. **Turnusbalanse (Stacked Bar):** Forholdet mellom faste vakter, helgetillegg (art 1040) og overtid (art 1090).

---

## 👥 Layout 4: Lønn, Vikar & Overtidsmonitor
* **Målgruppe:** Controller Lønn, HR-sjef og Hovedtillitsvalgte (HTA § 4).
* **Hovedhensikt:** Operativ monitorering av overtidsbruk og avvik fra bemanningsplan.
* **Nøkkelvisualer:**
  1. **Kontoart-matrise:** Artsgruppene 1000 (Fastlønn), 1020 (Vikarer), 1040 (Tillegg) og 1090 (Overtid) med avvik kr og %.
  2. **Avviksvannfall (Waterfall Chart):** Viser hvordan økning i sykefravær leder direkte til overtid og vikarbyråkostnader.
  3. **Anomali-detektor (Power BI AI Visual):** Automatisk varsel når en enhet overstiger 3 standardavvik fra normal overtidsbruk.

---

## 📈 Layout 5: KOSTRA Nøkkeltallsanalyse & SSB Sammenligning
* **Målgruppe:** Strategi- og analysedirektør, Bystyrets kontrollutvalg.
* **Hovedhensikt:** Benchmarking av Kristiansand mot ASSS-nettverket (Bærum, Drammen, Stavanger, Fredrikstad m.fl.).
* **Nøkkelvisualer:**
  1. **Korrigert Brutto Driftsutgift (KBDU) per innbygger:** Sammenligning per KOSTRA-funksjon.
  2. **Tjenesteprofil (Radar Chart / Dumbbell Chart):** Kristiansands ressursbruk sammenlignet med landssnittet og ASSS-snittet.
  3. **Frie Inntekter & Skatteinngang:** Skatteprosent mot landsgjennomsnittet over tid.

---

## 🏗️ Layout 6: Investeringsstyring & Prosjektkontroll
* **Målgruppe:** Eiendomssjef, Utbyggingssjef og Prosjektcontrollere.
* **Hovedhensikt:** Prosjektoppfølging, periodiserte investeringer og låneopptaksbehov.
* **Nøkkelvisualer:**
  1. **Prosjekt-Waterfall:** Kostnadsutvikling fra opprinnelig ramme, tilleggsbevilgninger til forventet sluttkostnad.
  2. **Gantt & Fremdriftsindikator:** Fysisk fremdrift mot finansiell avregning (S-kurver).
  3. **Lånegjeld og Renteeksponering:** Finansieringsstruktur, fastrenteandel og rentefølsomhet (+100 bps).

---

## 📋 Layout 7: Tertial- og HØP-Forberedelse
* **Målgruppe:** Økonomirådgivere, Saksbehandlere for politiske saker og Kommunerevisjonen.
* **Hovedhensikt:** Formell forberedelse til Formannskapets og Bystyrets tertialbehandling jf. Kommuneloven § 14-5.
* **Nøkkelvisualer:**
  1. **Formannskapstabell (Klartekst):** Strukturert tabell som kan eksporteres direkte til saksfremlegg i Word.
  2. **Omdisponeringsmatrise:** Viser foreslåtte overføringer mellom sektorer og bruk av disposisjonsfond.
  3. **Kryptografisk Integritetsstatus (Audit Trail):** Status på SHA-256 verifikasjon av regnskapstall mot Visma Enterprise.
