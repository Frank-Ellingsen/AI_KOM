# Power BI økonomisk status
## Wireframe, storytelling, RAG-formattering og DAX-pakke

Denne spesifikasjonen samler hele anbefalingen for en Power BI-side for økonomisk status. Målet er å gjøre rapporten ledelsesvennlig og handlingsorientert gjennom historien **Status → Diagnose → Drivere → Prognose → Handling**.

> **Merk:** RAG-tersklene og fargepaletten nedenfor er anbefalte designvalg. Tilpass tersklene til virksomhetens vedtatte toleransegrenser.

---

## 1. Designprinsipp

Rapportsiden skal svare på fem spørsmål i denne rekkefølgen:

1. **Hvordan ligger vi an?**
2. **Hvor oppstår avviket?**
3. **Hva driver avviket?**
4. **Hvor forventer vi å ende?**
5. **Hvor må ledelsen følge opp?**

Bruk blått og nøytrale farger til ordinære økonomiske data. Reserver RAG-fargene til styringssignaler, unntak, risiko og prognose.

---

## 2. Konkret wireframe

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ ØKONOMISK STATUS                                      Periode: [valgt]     │
│ Sektor ▾        Tertial ▾        Enhet ▾                  Filtre            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  REGNSKAP YTD       BUDSJETT YTD       AVVIK YTD          EOY PROGNOSE     │
│                                                                             │
│    12,6 M              17,3 M          🔴 -4,6 M           🔴 -4,6 M       │
│                                             -26,7 %                          │
│  av 17,3 M budsjett                       Ugunstig       Forventet årsavvik │
│  ███████████░░░░░                                                         │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔴 ØKONOMISK STATUS                                                        │
│ Regnskap ligger 4,6 M under periodisert budsjett. Kommunal Boenhet          │
│ står for hoveddelen av det samlede avviket.                                 │
├─────────────────────────────────────┬───────────────────────────────────────┤
│ 01  HVOR OPPSTÅR AVVIKET?          │ 02  HVA DRIVER AVVIKET?              │
│                                     │                                       │
│ Avvik per enhet                     │ Avvik per hovedgruppe                 │
│                                     │                                       │
│ Enhet 202          ███ +0,9 M 🟢    │ Lønn             ████████ -3,2 M 🔴 │
│                         │           │ Tjenester         ███      -0,8 M 🔴 │
│ ------------------------0---------- │ Andre kostnader  ██       -0,4 M 🟠 │
│                         │████████   │ Inntekter         █        -0,2 M 🟠 │
│ Kommunal Boenhet        │ -4,6 M 🔴│                                       │
│                                     │                                       │
├─────────────────────────────────────┴───────────────────────────────────────┤
│ 03  HVOR FORVENTER VI Å ENDE?                                              │
│                                                                             │
│ Årsbudsjett → YTD-avvik → Lønn → Tjenester → øvrig → EOY prognose          │
│      ████        ▼         ▼        ▼                  🔴 ███               │
│                         Waterfall                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ 04  HVILKE ENHETER KREVER OPPFØLGING?                                      │
│                                                                             │
│ Status │ Enhet              │ Budsjett │ Regnskap │ Avvik │ Avvik % │ EOY │
│ 🔴     │ Kommunal Boenhet   │ 17,2 M   │ 12,6 M   │-4,6M │ -26,8% │-4,6M│
│ 🟢     │ Enhet 202          │ 18 K     │ 19 K     │+1 K  │  +5,3% │+1 K │
└─────────────────────────────────────────────────────────────────────────────┘
```

Tallene i wireframet er illustrative og bygger på eksempelet i den eksisterende rapportsiden.

---

## 3. Visuelt hierarki

### Rad 1: Tittel og filtre

Hold filterområdet kompakt og horisontalt:

```text
Sektor [Alle ▾]    Tertial [T2 ▾]    Enhet [Alle ▾]
```

Dette frigjør plassen som i dagens layout brukes av et stort filterpanel på venstre side.

### Rad 2: KPI-er

Prioriter styringsinformasjonen:

- Regnskap YTD
- Budsjett YTD
- Avvik YTD i kroner
- Avvik YTD i prosent
- EOY prognose / forventet årsavvik

Avvik og prognose skal ha sterkere visuelt hierarki enn regnskap og budsjett.

### Rad 3: Executive Summary

En dynamisk forklaring skal tolke KPI-ene for leseren.

Eksempel:

> **Ugunstig utvikling:** Regnskap ligger 4,6 M under periodisert budsjett. Kommunal Boenhet står for hoveddelen av avviket.

Bruk en tynn RAG-farget stripe eller indikator. Ikke fargelegg hele tekstboksen rødt eller grønt.

### Rad 4: Diagnose

Venstre visual svarer på **hvor** avviket ligger. Høyre visual svarer på **hva** som driver avviket.

### Rad 5: Prognose

Bruk waterfall eller tilsvarende broanalyse for å knytte nåsituasjonen til forventet årsresultat.

### Rad 6: Handling

Avslutt siden med en oppfølgingstabell som viser hvilke enheter som krever oppmerksomhet.

---

## 4. RAG-modell

RAG = Red, Amber, Green.

Anbefalt eksempel på terskler:

| Status | Avvik % | Tolkning |
|---|---:|---|
| 🟢 Green | >= -2 % | Innenfor toleranse |
| 🟠 Amber | < -2 % og >= -5 % | Krever oppmerksomhet |
| 🔴 Red | < -5 % | Krever tiltak |

### Hvorfor prosent?

RAG bør normalt vurderes relativt til budsjett eller annen styringsbaseline. Samme kroneavvik kan ha svært ulik betydning mellom små og store enheter.

---

## 5. Fargepalett

```text
Canvas / sidebakgrunn   #F5F6F8
Kort / visualbakgrunn   #FFFFFF
Primær tekst            #2B2B2B
Sekundær tekst          #6B6B6B
Standard dataserie      #2589E8

RAG Green               #3A8F5C
RAG Amber               #E6A23C
RAG Red                 #D64545
Neutral                 #D8DDE3
```

### Regel

- Blå = ordinære økonomiske data
- Grå = referanse, akser, budsjett og sekundær informasjon
- Grønn/gul/rød = status eller styringssignal

Unngå å bruke RAG-fargene dekorativt.

---

## 6. DAX: RAG-status

Forutsetningen er at modellen har et mål tilsvarende `[Avvik YTD %]`.

```DAX
RAG Status =
VAR AvvikPct = [Avvik YTD %]
RETURN
    SWITCH(
        TRUE(),
        ISBLANK(AvvikPct), "N/A",
        AvvikPct < -0.05, "Red",
        AvvikPct < -0.02, "Amber",
        "Green"
    )
```

---

## 7. DAX: RAG-farge

```DAX
RAG Color =
SWITCH(
    [RAG Status],
    "Red",   "#D64545",
    "Amber", "#E6A23C",
    "Green", "#3A8F5C",
    "#A0A0A0"
)
```

Dette målet kan brukes som grunnlag for betinget formatering der det aktuelle visualet støtter feltverdi som fargevalg.

---

## 8. DAX: RAG-symbol

```DAX
RAG Symbol =
SWITCH(
    [RAG Status],
    "Red", "●",
    "Amber", "●",
    "Green", "●",
    "○"
)
```

Fargen bør komme fra `[RAG Color]`. Kombinasjonen av symbol, farge og numerisk verdi gjør statusen lettere å forstå enn farge alene.

---

## 9. Separat RAG for YTD og EOY

Actual og forecast bør vurderes separat.

### YTD

```DAX
RAG YTD =
VAR x = [Avvik YTD %]
RETURN
SWITCH(
    TRUE(),
    ISBLANK(x), "N/A",
    x < -0.05, "Red",
    x < -0.02, "Amber",
    "Green"
)
```

### EOY

```DAX
RAG EOY =
VAR x = [EOY Avvik %]
RETURN
SWITCH(
    TRUE(),
    ISBLANK(x), "N/A",
    x < -0.05, "Red",
    x < -0.02, "Amber",
    "Green"
)
```

Dette åpner for styringssignal som:

```text
Enhet                  YTD     EOY
Kommunal Boenhet       🔴      🔴
Enhet A                🔴      🟠
Enhet B                🟢      🟢
```

En overgang fra rød YTD til gul EOY kan brukes til å kommunisere forventet forbedring, mens rød/rød peker på et vedvarende avvik.

---

## 10. KPI-design

### Regnskap YTD

```text
REGNSKAP YTD
12,6 M

Budsjett: 17,3 M
████████████░░░░
```

### Avvik YTD

```text
AVVIK YTD
🔴
-4,6 M
-26,7 %
Ugunstig
```

### EOY Forecast

```text
EOY FORECAST
🔴
-4,6 M
Forventet årsavvik
```

RAG-signalet skal bare brukes der KPI-en faktisk uttrykker status eller risiko.

---

## 11. Visual 01: Avvik per enhet

Formål: identifisere **hvor avviket oppstår**.

Anbefalt diverging bar:

```text
              GUNSTIG        │       UGUNSTIG
                             │
Enhet 202         █████████  │ +0,9 M
                             │
─────────────────────────────┼──────────────────────
                             │
Enhet A                      │███ -0,4 M
                             │
Kommunal Boenhet             │████████████████ -4,6 M
                             │
                             0
```

### Designregler

- Nullinje skal være tydelig.
- Gunstig og ugunstig side skal kunne skilles raskt.
- Sorter etter styringsrelevans, for eksempel størrelsen på avviket.
- Bruk datalabels i kroner.
- Bruk tooltip til prosent, budsjett, actual og forecast.

---

## 12. Visual 02: Avviksdrivere

Erstatt eller suppler dagens `Forbruk per Hovedgruppe` med et visual som besvarer:

> **Hva driver avviket?**

Eksempel:

```text
Lønn                -3,20 M  ███████████████ 🔴
Kjøp av tjenester   -0,80 M  ████            🔴
Andre kostnader     -0,40 M  ██              🟠
Inntekter           -0,20 M  █               🟠
Finans               +0,10 M  ▌              🟢
```

Sorter driverne etter bidrag til avviket, slik at vesentlige forklaringer blir synlige først.

---

## 13. Visual 03: EOY Waterfall

Formål: forklare hvordan nåsituasjonen og forventede effekter leder til sluttprognosen.

Konsept:

```text
Årsbudsjett
    │
    ├── YTD-avvik
    ├── forventet lønnseffekt
    ├── forventet vare-/tjenesteeffekt
    ├── øvrige prognoseendringer
    ↓
EOY Forecast
```

Storytelling:

```text
Hva var planen?
      ↓
Hva har skjedd?
      ↓
Hva forventer vi videre?
      ↓
Hvor ender året?
```

---

## 14. Oppfølgingstabell

Anbefalte kolonner:

| Felt | Formål |
|---|---|
| Status | Primært RAG-signal |
| Enhet | Ansvar / organisatorisk nivå |
| Budsjett YTD | Baseline |
| Regnskap YTD | Faktisk |
| Avvik YTD | Kroneavvik |
| Avvik % | Relativt avvik |
| EOY Forecast | Sluttprognose |
| EOY % | Prognostisert relativt avvik |
| Trend | Retning / utvikling dersom modellen støtter dette |

Eksempel:

```text
🔴 Kommunal Boenhet   17,2M   12,6M   -4,6M   -26,8%   -4,6M   ↓
🟠 Enhet A             8,1M    7,8M   -0,3M    -3,7%   -0,2M   ↑
🟢 Enhet 202           6,2M    6,3M   +0,1M    +1,6%   +0,1M   →
```

### Formateringsregler

- RAG i første kolonne.
- Negativt styringsavvik kan fremheves, men unngå å fargelegge hele raden.
- Totalrad skal være tydelig, men nøytral.
- Høyrejuster alle numeriske kolonner.
- Bruk konsistente display units: K / M.

---

## 15. Executive Summary som dynamisk tekst

Rapporten bør ha en kort tolkningsboks mellom KPI-ene og diagnosevisualene.

Eksempel på ønsket format:

```text
🔴 Ugunstig utvikling
Regnskap ligger 4,6 M under periodisert budsjett.
Kommunal Boenhet står for hoveddelen av avviket.
```

Mulig DAX-struktur dersom de nødvendige målene finnes:

```DAX
Executive Summary =
VAR Avvik = [Avvik YTD]
VAR AvvikPct = [Avvik YTD %]
VAR Rag = [RAG Status]
RETURN
    "Status: " & Rag &
    " | Avvik YTD: " & FORMAT(Avvik, "#,##0,,.0 M") &
    " | Avvik %: " & FORMAT(AvvikPct, "0.0%")
```

Dette er en basisvariant. En mer avansert versjon kan hente frem største avviksdriver/enhet dersom datamodellen støtter en entydig rangering.

---

## 16. Filterstrategi

Flytt store venstrestilte slicere til et kompakt filterområde over rapporten.

Anbefalt:

```text
Sektor      [Alle ▼]
Tertial     [T2 ▼]
Enhet       [Alle ▼]
```

Ved behov kan mer detaljerte filtre legges i et separat filterpanel/bookmark-oppsett.

---

## 17. Interaksjon mellom visualer

Anbefalt brukerflyt:

1. Brukeren velger sektor/tertial.
2. KPI-er og Executive Summary viser total status.
3. Brukeren velger en enhet i avviksvisualet.
4. Avviksdriver-visualet filtreres til valgt enhet.
5. Waterfall viser relevant forecast-kontekst.
6. Tabellen viser detaljene og RAG-status.

Målet er å støtte en naturlig drill-down fra aggregert status til forklaring og handling.

---

## 18. Tooltip-design

For avviksvisualene anbefales en egen tooltip-side med:

```text
Enhet
──────────────
Budsjett YTD
Regnskap YTD
Avvik YTD
Avvik %

RAG YTD
EOY Forecast
RAG EOY
```

Hold tooltipen kompakt. Den skal gi kontekst uten å duplisere hele detaljtabellen.

---

## 19. Visuell standard

### Kort

- Hvit bakgrunn
- Svært subtil border
- Moderat avrunding
- Minst mulig skygge
- Venstrejustert tittel
- Tydelig hovedverdi

### Tekst

```text
Sidetittel            20–24 px
Seksjonsoverskrift    14–16 px
Visualtittel          12–14 px
KPI-verdi             24–32 px
Sekundær tekst        10–12 px
```

### Luft

Bruk konsekvent spacing, eksempelvis et 8-punkts system:

```text
8 px
16 px
24 px
32 px
```

---

## 20. Hva som bør fjernes eller tones ned fra dagens side

1. Store vertikale filterområder som reduserer analyseflaten.
2. Tekniske statusuttrykk som `[Red]` inne i KPI-tekst.
3. RAG på elementer som ikke representerer status eller risiko.
4. Diagrammer som primært viser volum dersom styringsspørsmålet egentlig handler om avvik.
5. For mange like KPI-kort uten visuelt hierarki.

---

## 21. Anbefalt sidehistorie

### 01 STATUS

**Hvordan ligger vi an?**

Regnskap → Budsjett → Avvik → Forecast

### 02 DIAGNOSE

**Hvor oppstår avviket?**

Sektor → Enhet

### 03 DRIVER

**Hva forklarer avviket?**

Hovedgruppe → kostnads-/inntektsdriver

### 04 PROGNOSE

**Hvor forventer vi å ende?**

YTD → forventede effekter → EOY

### 05 HANDLING

**Hvor må ledelsen følge opp?**

RAG → avvik → forecast → trend

---

## 22. Foreslått implementeringsrekkefølge

### Fase A: Measures

- `[Regnskap YTD]`
- `[Budsjett YTD]`
- `[Avvik YTD]`
- `[Avvik YTD %]`
- `[EOY Forecast]`
- `[EOY Avvik]`
- `[EOY Avvik %]`
- `[RAG Status]`
- `[RAG Color]`
- `[RAG YTD]`
- `[RAG EOY]`

### Fase B: Layout

1. Etabler sidebakgrunn og grid.
2. Flytt slicere til toppområdet.
3. Bygg KPI-raden.
4. Legg til Executive Summary.
5. Bygg avvik per enhet.
6. Bygg avviksdrivere.
7. Bygg EOY waterfall.
8. Bygg oppfølgingstabell.

### Fase C: Formatting

1. Legg inn RAG-reglene.
2. Standardiser tallformat.
3. Standardiser titler.
4. Standardiser datalabels.
5. Test kontrast og lesbarhet.

### Fase D: Storytelling-test

En bruker skal kunne svare på følgende innen kort tid:

- Er økonomien innenfor plan?
- Hvor stort er avviket?
- Hvilken enhet er mest relevant å undersøke?
- Hva driver avviket?
- Forventes situasjonen å forbedres eller forverres?
- Hvilke enheter krever oppfølging?

Hvis rapporten krever at brukeren leter etter disse svarene, bør layouten forenkles ytterligere.

---

## 23. Kort designoppsummering

Den anbefalte rapportarkitekturen er:

```text
STATUS
  ↓
DIAGNOSE
  ↓
DRIVER
  ↓
PROGNOSE
  ↓
HANDLING
```

RAG fungerer som et **styringsspråk** gjennom hele siden:

```text
🟢 Innenfor toleranse
🟠 Krever oppmerksomhet
🔴 Krever tiltak
```

Det viktigste designprinsippet er at hvert visual skal svare på ett konkret spørsmål og føre brukeren naturlig videre til neste spørsmål.
