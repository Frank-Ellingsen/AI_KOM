# Dashboard for Top 3 KPIs, Budsjetthierarki og Virksomhetsområder
**Kristiansand kommune — Control Office Hub (AI_KOM)**  
*Visualiseringsspesifikasjon, Gauge-komponenter, Hierarkisk Kaskadering og Virksomhetspesifikke Nøkkeltall*

---

## 1. Visuell Dashboard-arkitektur & Gauge Charts (Top 3 KPIs)

For å sikre umiddelbar visuell forståelse hos både politikere (Bystyret/Formannskapet) og den administrative ledelsen (Kommunedirektøren), benyttes dynamiske **Gauge Charts (Takometer-grafer)** for de tre overordnede finansielle styringsindikatorene.

```
+---------------------------------------------------------------------------------------------------+
| Top 3 Kommunale Finansielle Nøkkeltall (M10 Oktober Status)                                      |
+-----------------------------------+----------------------------------+----------------------------+
| 🟢 Netto Driftsresultat           | 🟢 Disposisjonsfond             | 🟢 Netto Lånegjeld         |
| [ Gauge: 1.25% ]                  | [ Gauge: 4.35% ]                 | [ Gauge: 76.8% ]           |
|  • Mål TBU: ≥ 1.75%               |  • Mål TBU: ≥ 5.0%               |  • Mål TBU: ≤ 80.0%        |
|  • Mål Kommune: ≥ 1.0%            |  • Mål Kommune: ≥ 4.0%           |  • Mål Kommune: ≤ 78.0%    |
|  • Status: 115 mill. kr i balanse |  • Status: 460 mill. kr i buffer |  • Status: 8.4 mrd. kr     |
+-----------------------------------+----------------------------------+----------------------------+
```

### 1.1 Detaljert Gauge-Skala & Grenseverdier

```ts
// TypeScript Specification for Recharts / ECharts Gauge Component
export interface GaugeMetric {
  id: 'netto_driftsresultat' | 'disposisjonsfond' | 'netto_laanegjeld';
  title: string;
  currentValue: number;
  unit: string;
  targets: {
    tbuNorm: number;
    municipalTarget: number;
  };
  zones: {
    criticalRed: [number, number];     // Må kreve umiddelbare kutt
    warningYellow: [number, number];   // Må overvåkes tett
    targetGreen: [number, number];     // I tråd med handlingsregelen
    optimalDarkGreen: [number, number];// Svært robust økonomi
  };
}

export const TOP3_GAUGE_CONFIG: Record<string, GaugeMetric> = {
  netto_driftsresultat: {
    id: 'netto_driftsresultat',
    title: 'Netto Driftsresultat',
    currentValue: 1.25,
    unit: '%',
    targets: { tbuNorm: 1.75, municipalTarget: 1.00 },
    zones: {
      criticalRed: [0.0, 0.50],
      warningYellow: [0.50, 1.00],
      targetGreen: [1.00, 2.50],
      optimalDarkGreen: [2.50, 5.00]
    }
  },
  disposisjonsfond: {
    id: 'disposisjonsfond',
    title: 'Disposisjonsfond',
    currentValue: 4.35,
    unit: '% av driftsinntekt',
    targets: { tbuNorm: 5.00, municipalTarget: 4.00 },
    zones: {
      criticalRed: [0.0, 2.00],
      warningYellow: [2.00, 4.00],
      targetGreen: [4.00, 8.00],
      optimalDarkGreen: [8.00, 15.00]
    }
  },
  netto_laanegjeld: {
    id: 'netto_laanegjeld',
    title: 'Netto Lånegjeld',
    currentValue: 76.8,
    unit: '% av driftsinntekt',
    targets: { tbuNorm: 80.0, municipalTarget: 78.0 },
    zones: {
      optimalDarkGreen: [0.0, 60.0],
      targetGreen: [60.0, 80.0],
      warningYellow: [80.0, 90.0],
      criticalRed: [90.0, 150.0]
    }
  }
};
```

---

## 2. Kaskadering av Top 3 KPIs Nedover i Budsjetthierarkiet

De overordnede **Top 3 KPIs** nedskaleres og tilpasses hvert nivå i kommunens budsjetthierarki slik at hver enhetsleder forstår sin direkte påvirkning på kommunens samlede balanse.

```
NIVÅ 1: KANTON / KONSERNNIVÅ (Kommunedirektør & Bystyre)
├── Netto Driftsresultat (≥ 1,0 %)
├── Disposisjonsfond (≥ 4,0 %)
└── Netto Lånegjeld (≤ 8,8 mrd. kr)
     │
     ▼
NIVÅ 2: KOMMUNALOMRÅDE / SEKTORNIVÅ (Kommunalsjefer)
├── Sektorordnet Netto Driftsavvik (NOK og % av rammene)
├── Sektorens Fondsoppbygging / Øremerkede reserver (NOK)
└── Investeringsramme & Gjeldsbetjening per Sektor (NOK)
     │
     ▼
NIVÅ 3: ENHETSNIVÅ / VIRKSOMHETSNIVÅ (Enhetsledere / Rektorer / Styrere)
├── Enhetens Rammeavvik YTD (Budsjett vs Regnskap)
├── Sykelønns- og Vikarbelastning (% av rammen, Art 1020 / 1090)
└── NAV-refusjonsdekningsgrad (% oppnådd av berettiget refundering)
```

### 2.1 Måltalls-matrise per Hierarkinivå

| Hierarkinivå | Top 1: Netto Driftsresultat (Løpende balanse) | Top 2: Disposisjonsfond (Buffer) | Top 3: Netto Lånegjeld (Gjeldsgrad) |
| :--- | :--- | :--- | :--- |
| **Nivå 1: Konsern (Kommunen)** | **Mål: ≥ 1,0 %** (ca. 115 mill. kr i merforbrukstoleranse) | **Mål: ≥ 4,0 %** (ca. 460 mill. kr i urørt fondssaldo) | **Mål: ≤ 78,0 %** (Lånetak 8,8 mrd. kr) |
| **Nivå 2: Sektor (f.eks. Oppvekst)** | **Sektoravvik YTD ≤ 0,0 kr** (Holdes innenfor sektorens totalramme) | **Sektorfond / Ubrukte midler** (Øremerkede midler i reserve) | **Sektorens Investeringsramme** (Akkumulert aktivert kapital) |
| **Nivå 3: Enhet (f.eks. Vågsbygd Skole)** | **Enhetsavvik YTD ≤ 0,0 kr** (Full rammelojalitet per måned) | **Konto 1020 Vikarbruk ≤ 2,5 %** av lønnsrammen | **Kjøp av inventar (Art 1120) ≤ Investeringsramme** |

---

## 3. Spesifikke Nøkkeltall per Virksomhetsområde (Sektorspesifikke KPIs)

Utenom de topp tre finansielle måltallene krever hvert virksomhetsområde operative fagindikatorer for å forklare *hvorfor* finansielle avvik oppstår.

### 3.1 Område 1: Oppvekst & Utdanning (Skole og Barnehage)
* **Kostnad per elev/barn (KOSTRA Funksjon 202, 211, 222):** Korrigert brutto driftsutgift per elev sammenslått mot KOSTRA-kommunegruppe.
* **Lærertetthet & Pedagogdekning (%):** Oppfyllelse av den statlige normen for lærertetthet (1.–4. trinn og 5.–10. trinn).
* **Vikar- og overtidsprosent (Art 1020 / 1090):** Andel vikarutgifter målt mot ordinær fastlønn (Art 1010).
* **NAV-refusjonsgrad (Art 1600 / 1690):** Gjennomsnittlig saksbehandlingstid og etterslep fra sykemelding til utbetalt NAV-refusjon.

### 3.2 Område 2: Helse & Mestring (Omsorg, Pleie og Sosiale Tjenester)
* **Brutto utgift per plass/døgn (KOSTRA Funksjon 253/254):** Døgnkostnad for sykehjem vs. hjemmebasert omsorg.
* **Dekningsgrad for sykehjemsplasser (80+ år):** Prosentandel av innbyggere over 80 år med heldøgns pleieplass.
* **Turnusdekning & Ubekvem overtid (Art 1090):** Prosentandel av helge- og kveldsvakter dekket av fast ansatte vs. overtid/innleid vikarbyrå.
* **Legemeldt sykefravær (%):** Månedlig sykefraværsprosent i pleie og omsorg (kritisk driver for vikarbruk).

### 3.3 Område 3: By- og Stedsutvikling (Teknisk, Veg, Park og VAR Selvkost)
* **Selvkostgrad for VAR (%):** Dekningsgrad for Vann, Avløp og Renovasjon (skal være eksakt 100,0 % over en 5-årsperiode jf. Selvkostforskriften).
* **Saksbehandlingstid i Byggesak (Dager):** Gjennomsnittlig saksbehandlingstid for 12-ukers og 3-ukers byggesøknader.
* **Vedlikeholdsetterslep på Kommunale Bygg (NOK/m²):** Beregnet etterslep på kommunens eiendomsmasse.
* **Snøbrøyting & Vinterdrift (Art 1270):** Akkumulert forbruk på beredskapstjenester mot klimajusterte budsjetter.

### 3.4 Område 4: Kultur, Idrett og Samfunn
* **Netto driftsutgift til kultur per innbygger (NOK):** Samlet kommunal støtte til idrettsanlegg, bibliotek og kulturskole per innbygger.
* **Deltakerfrafall / Inkluderingsrate:** Prosentandel av barn i lavinntektsfamilier som deltar i kommunale fritidsaktiviteter.

### 3.5 Område 5: Organisasjon, Styring og Fellesutgifter
* **Administrasjonskostnad per innbygger (KOSTRA Funksjon 120):** Kommunens utgifter til politisk styring, kontorhold og sentraladministrasjon.
* **Automatiseringsgrad i Regnskap (%):** Prosentandel av inngående fakturaer som behandles automatisk uten manuell bilagsbehandling.
* **Fakturabetaling til rett tid (%):** Prosentandel av kommunens leverandørfakturaer betalt innen forfall.

---

## 4. Power BI DAX-Implementasjon for Hierarkisk Drill-Down

For å støtte dynamisk visning av Top 3 KPIs i Power BI på tvers av alle nivåer i budsjetthierarkiet, benyttes følgende DAX-mål:

```dax
// DAX Measure: Dynamisk Netto Driftsresultat (% av Brutto Driftsinntekter)
NettoDriftsresultat_Prosent = 
VAR BruttoInntekter = CALCULATE(SUM(Regnskap[Beløp]), Regnskap[Art_Hovedgruppe] = "INNTAL")
VAR NettoDrift = CALCULATE(SUM(Regnskap[Beløp]), Regnskap[Konto_Type] = "NETTO_DRIFT")
RETURN
DIVIDE(NettoDrift, ABS(BruttoInntekter), 0) * 100

// DAX Measure: Hierarkisk Avviksindikasjon (Triage Status)
Triage_Status_Hierarki = 
VAR AvvikPct = [Budsjett_Avvik_Prosent]
RETURN
SWITCH(
    TRUE(),
    AvvikPct > 3.0, "🔴 RØD (Kritisk Merforbruk)",
    AvvikPct > 1.0, "🟡 GUL (Moderat Avvik)",
    "🟢 GRØNN (I Balanse / Mindreforbruk)"
)
```

---

## 5. React / Tailwind UI-komponent for Dashboard

```tsx
// React TSX snippet for rendering Top 3 Gauges and Hierarchy Tree
import React from 'react';
import { TOP3_GAUGE_CONFIG } from './kpiConfig';

export const Top3KpiDashboard: React.FC = () => {
  return (
    <div className="p-6 bg-slate-900 text-white rounded-xl shadow-2xl space-y-8">
      {/* Top 3 Gauge Header */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {Object.values(TOP3_GAUGE_CONFIG).map((metric) => (
          <div key={metric.id} className="bg-slate-800 p-5 rounded-lg border border-slate-700 flex flex-col items-center">
            <h3 className="text-lg font-semibold text-slate-200">{metric.title}</h3>
            <div className="text-4xl font-bold text-emerald-400 my-3">
              {metric.currentValue} {metric.unit}
            </div>
            <div className="text-xs text-slate-400 space-y-1 w-full text-center">
              <div>Mål TBU: <span className="font-bold text-slate-200">{metric.targets.tbuNorm}{metric.unit}</span></div>
              <div>Mål Kommune: <span className="font-bold text-slate-200">{metric.targets.municipalTarget}{metric.unit}</span></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```
