# Kristiansand Kommune — Power BI Template & Profilfarger (.pbip / .pbit)
**Control Office Hub (AI_KOM) & Antigravity Backend Engine**

---

## 1. Visuell Profil & Fargepalett

Power BI-rapportmalen bygger på den offisielle den visuelle profilen til Kristiansand kommune kombinert med tilgjengelighetskrav (WCAG 2.1 AA) for universell utforming i offentlig sektor:

* 🟦 **Hovedfarge (Mørk Blå):** `#002855` (Kommuneblå - benyttes til overskrifter, korttitler og primære dataserier)
* 🔷 **Sekundærfarge (Profil Blå):** `#0072CE` (Aktiv farge, knapper og aktive faner)
* 🟢 **Status Grønn (Godkjent / Mål nådd):** `#10B981` (TBU-mål oppfylt)
* 🟡 **Status Gul (Advarsel / Tiltak kreves):** `#F59E0B` (Avvik 1–3 %)
* 🔴 **Status Rød (Kritisk / Rødflagg):** `#EF4444` (Avvik > 3 % eller vesentlig TBU-brudd)
* ⚪ **Bakgrunn:** `#F8FAFC` (Nøytral gråhvit bakgrunn for redusert skjermtretthet)
* 📦 **Kort og Visuals:** Hvit bakgrunn (`#FFFFFF`) med svak ramme (`#E2E8F0`) og 8px avrundede hjørner.

---

## 2. Struktur på Power BI Prosjektfil (.pbip)

I nyere versjoner av Power BI Desktop benyttes **Power BI Project Format (.pbip)** som muliggjør Git-versjonskontroll på tvers av økonomi- og IT-teamet.

```
AI_KOM_Rapport_2026.pbip
├── AI_KOM_Rapport_2026.Dataset/
│   ├── definition.pbidataset
│   ├── model.bim                   <-- DAX-mål, tabellrelasjoner og KOSTRA-hierarki
│   └── item.config.json
└── AI_KOM_Rapport_2026.Report/
    ├── definition.pbi-report
    ├── StaticResources/
    │   └── RegisteredResources/
    │       └── Kristiansand_Kommune_PowerBI_Theme.json  <-- Importert profiltema
    └── item.config.json
```

---

## 3. Sidearkitektur i Power BI-Rapporten

Rapporten er delt inn i **4 hovedsider** i tråd med den rollebaserte navigeringsmodellen:

### Side 1: 🏛️ Konsernoverblikk & Top 3 KPIs (Executive Dashboard)
* **Topplinje:** Kompakt KPI-rekke med 3 Takometer/Gauge-visualer:
  * *Netto Driftsresultat (%)* (Mål ≥ 1,0 %)
  * *Disposisjonsfond (%)* (Mål ≥ 4,0 %)
  * *Netto Lånegjeld (%)* (Mål ≤ 8,8 mrd. kr)
* **Midtfelt:** Konsernets Triage-matrise (Rødflagg-rangering av de 16 mest avviksutsatte enhetene).
* **Bunnfelt:** Trendkort for regnskapsutvikling YTD sammenlignet med samme periode i fjor.

### Side 2: 🏫 Område- & Sektorstyring (Kommunalsjefer)
* **Kaskadert Avviksmatrise:** Matrix-visual basert på `ISINSCOPE()` som lar brukeren drille fra Kommunalområde -> Virksomhet -> Enhet.
* **Driveranalyse:** Bar-charts som viser fordeling av avvik på *Vikarer (Art 1020)*, *Overtid (Art 1090)* og *Etterslep på NAV-refusjoner (Art 1600/1690)*.

### Side 3: 📊 Controller Hub & MVA-Balansering (Økonomirådgivere)
* **Balansekontroll Konto 2130:** Dedikert tabell for MVA-kompensasjonsavstemming mot Skatteetaten.
* **Transaksjons-drillthrough:** Tabell på laveste bilagsnivå med SHA-256 kryptografisk revisjonsstempel.

### Side 4: 🛠️ Scenario- & Tiltakssimulator (Lederverktøy)
* **What-If Parametere:** Interaktive sliders for simulering av kutt i vikarinnleie (0–30 %) og effekten på konsernets Netto Driftsresultat.

---

## 4. Slik importerer du temaet i Power BI Desktop

1. Åpne **Power BI Desktop**.
2. Gå til fanen **Vis (View)** i toppmenyen.
3. Klikk på rullegardinmenyen for **Temaer (Themes)** og velg **Se etter temaer (Browse for themes)**.
4. Velg den vedlagte filen `Kristiansand_Kommune_PowerBI_Theme.json`.
5. Alle farger, skrifttyper (Segoe UI), kortrammer og takometerfarger oppdateres automatisk til kommunens profildesign.
