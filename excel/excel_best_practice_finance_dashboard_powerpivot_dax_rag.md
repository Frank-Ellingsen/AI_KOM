# Excel Best Practice Package
## Power Query, Data Model, Power Pivot, DAX, PivotTables, PivotCharts, Slicers, RAG, Tooltips og dashboards

Denne pakken viser hvordan samme styringslogikk som i Power BI-pakken kan bygges i Excel. Målbildet er en robust controller-workbook med **Power Query → Data Model → Power Pivot/DAX → PivotTables/PivotCharts → Slicers/Timeline → Dashboard → Detalj og kontroll**.

> **Fast fortegnsregel i denne pakken**
>
> `Avvik = Regnskap - Budsjett`
>
> For kostnader:
>
> - **Negativt avvik = grønt = gunstig**
> - **Positivt avvik = rødt = ugunstig**
> - **Nær null = gult = innenfor toleranse**

---

# 1. Power BI-konsept → Excel-ekvivalent

| Power BI | Excel |
|---|---|
| Power Query | Power Query / Get & Transform |
| Semantic model | Excel Data Model / Power Pivot |
| Relationships | Relationships i Data Model |
| DAX measures | Power Pivot Measures |
| Matrix | PivotTable |
| Bar/line/waterfall | PivotChart eller vanlig Excel-chart |
| Slicer | Slicer |
| Date slicer | Timeline |
| Conditional formatting | PivotTable/celle conditional formatting |
| Tooltip | Data labels, linked KPI-celler, kommentarer/notater, hjelpepanel |
| Drill/filter | Pivot expand/collapse, slicers, filters og egne detaljark |
| Executive dashboard | Dashboard-ark med PivotCharts og KPI-kort |
| Decomposition Tree | PivotTable-hierarki + drill-down/root-cause ark |
| Dynamic narrative | Formeldrevet tekstboks/celle |
| What-if | Inputceller / Scenario Manager / datatabeller + DAX/formler |

Excel kan bruke Data Model med flere relaterte tabeller, og Power Pivot kan opprette calculated columns og measures med DAX. PivotTables og PivotCharts kan deretter bygges på modellen.

---

# 2. Anbefalt workbook-arkitektur

```text
00_README
01_CONTROL
02_DASHBOARD_EXEC
03_DASHBOARD_OPPVEKST
04_DASHBOARD_HELSE
05_LONN_VIKAR
06_PROGNOSE_SCENARIO
07_EVM
08_ROOT_CAUSE
09_AUDIT
10_DETAIL
90_PIVOTS
91_HELPER
99_QA
```

## Prinsipp

- Dashboardark viser bare beslutningsrelevant informasjon.
- `90_PIVOTS` holder støtte-PivotTables som driver visualene.
- `91_HELPER` holder hjelpeceller/formler for KPI-er og dynamiske tekster.
- `99_QA` holder datakvalitetskontroller.
- Rådata bør normalt transformeres med Power Query og lastes til Data Model, ikke kopieres rundt i dashboardarkene.

---

# 3. Datamodell

Anbefalt stjerneskjema:

```text
                    DimDate
                       │
                       │
DimOrganization ─── FactFinance ─── DimAccount
                       │
                       │
                  DimScenario
```

Eksempel:

```text
FactFinance
    DateKey
    OrgKey
    AccountKey
    ScenarioKey
    Amount
    DataType

DimDate
    DateKey
    Date
    Year
    MonthNo
    MonthName
    YearMonth
    Quarter
    Tertial

DimOrganization
    OrgKey
    Budsjettnivå
    Sektor
    Virksomhetsområde
    Enhet
    Lokasjon
    Ansvar

DimAccount
    AccountKey
    Hovedgruppe
    Kontoart
    Kontokode
    Kontonavn

DimScenario
    ScenarioKey
    Scenario
```

`DataType` kan for eksempel skille `Actual`, `Budget` og eventuelt `Forecast` dersom kildestrukturen er long-format.

---

# 4. Power Query-lag

Power Query bør gjøre ETL-arbeidet før data lastes til modellen:

```text
Hent
  ↓
Standardiser kolonnenavn og typer
  ↓
Rens tekst/nøkler
  ↓
Unpivot/pivot ved behov
  ↓
Map konto og organisasjon
  ↓
Kontroller duplikater og nullverdier
  ↓
Last dimensioner + faktatabell til Data Model
```

## Best practice

- Legg transformasjonslogikk i queries, ikke i dashboardceller.
- Bruk egne staging-queries når datakilden trenger flere transformasjonssteg.
- Last store faktatabeller til Data Model fremfor til synlige ark når det er hensiktsmessig.
- Hold dimensjoner entydige på nøkkelkolonnene.

---

# 5. Relationships

Eksempel:

```text
DimDate[DateKey]          1 → * FactFinance[DateKey]
DimOrganization[OrgKey]  1 → * FactFinance[OrgKey]
DimAccount[AccountKey]   1 → * FactFinance[AccountKey]
DimScenario[ScenarioKey] 1 → * FactFinance[ScenarioKey]
```

Excel Data Model/Power Pivot støtter modellrelasjoner og hierarkier som kan brukes i PivotTables.

---

# 6. DAX i Excel Power Pivot

DAX i Power Pivot kan brukes til calculated columns og measures. For dashboardet bør kjerne-KPI-er normalt være measures slik at beregningene reagerer på PivotTable-/slicer-filterkontekst.

Nedenfor brukes en long-format faktatabell med `[Amount]` og `[DataType]`.

## Regnskap

```DAX
Regnskap :=
CALCULATE(
    SUM(FactFinance[Amount]),
    FactFinance[DataType] = "Actual"
)
```

## Budsjett

```DAX
Budsjett :=
CALCULATE(
    SUM(FactFinance[Amount]),
    FactFinance[DataType] = "Budget"
)
```

## Avvik

```DAX
Avvik :=
[Regnskap] - [Budsjett]
```

## Avvik prosent

```DAX
Avvik % :=
DIVIDE(
    [Avvik],
    ABS([Budsjett])
)
```

---

# 7. YTD measures

Forutsetter en korrekt datotabell.

```DAX
Regnskap YTD :=
TOTALYTD(
    [Regnskap],
    DimDate[Date]
)
```

```DAX
Budsjett YTD :=
TOTALYTD(
    [Budsjett],
    DimDate[Date]
)
```

```DAX
Avvik YTD :=
[Regnskap YTD] - [Budsjett YTD]
```

```DAX
Avvik YTD % :=
DIVIDE(
    [Avvik YTD],
    ABS([Budsjett YTD])
)
```

---

# 8. Forecast measures

Hvis faktatabellen inneholder forecast:

```DAX
Forecast :=
CALCULATE(
    SUM(FactFinance[Amount]),
    FactFinance[DataType] = "Forecast"
)
```

```DAX
Forecast Avvik :=
[Forecast] - [Budsjett]
```

```DAX
Forecast Avvik % :=
DIVIDE(
    [Forecast Avvik],
    ABS([Budsjett])
)
```

---

# 9. RAG-logikk

## Anbefalt toleransemodell

Eksempel:

```text
Avvik < -2 %         GREEN
-2 % til +2 %        AMBER
Avvik > +2 %         RED
```

Tersklene skal tilpasses virksomhetens faktiske styringsregler.

## RAG Status

```DAX
RAG Status :=
VAR Pct = [Avvik YTD %]
RETURN
SWITCH(
    TRUE(),
    ISBLANK(Pct), "N/A",
    Pct < -0.02, "Green",
    Pct >  0.02, "Red",
    "Amber"
)
```

## Streng variant

```DAX
RAG Status Streng :=
VAR Value = [Avvik YTD]
RETURN
SWITCH(
    TRUE(),
    ISBLANK(Value), "N/A",
    Value < 0, "Green",
    Value > 0, "Red",
    "Amber"
)
```

## Numerisk RAG-kode

Denne er nyttig i Excel conditional formatting:

```DAX
RAG Code :=
SWITCH(
    [RAG Status],
    "Green", -1,
    "Amber",  0,
    "Red",    1,
    BLANK()
)
```

---

# 10. RAG conditional formatting i Excel

## Prinsipp

På kostnadsavvik skal visuell semantikk være:

```text
NEGATIVT = GRØNT
NULL/NÆR NULL = GULT
POSITIVT = RØDT
```

## PivotTable

Bruk conditional formatting på avvikskolonnen med regler som følger styringsgrensene.

Eksempel med streng regel:

```text
Cell Value < 0   → grønn skrifttype/fyll
Cell Value = 0   → amber/gul
Cell Value > 0   → rød skrifttype/fyll
```

Eksempel med ±2 % toleranse på prosentkolonnen:

```text
< -2 %            → grønn
-2 % til +2 %     → amber
> +2 %             → rød
```

## Designregel

Ikke fargelegg hele tabellen. Bruk heller:

- ikon/statuskolonne
- fontfarge på avvik
- svak cellebakgrunn
- databar der det gir mening

---

# 11. Slicers

Slicers kan filtrere Excel-tabeller og PivotTables. En slicer kan også kobles til andre PivotTables når PivotTables deler samme datakilde.

## Primære slicers

```text
Budsjettnivå
Virksomhetsområde
År
Tertial / periode
```

## Sekundære slicers

```text
Enhet
Lokasjon
Ansvar
Hovedgruppe
Kontoart
Scenario
```

## Anbefalt oppsett

```text
┌ Budsjettnivå ┐ ┌ Virksomhetsområde ┐ ┌ År ┐ ┌ Tertial ┐
│ Sektor       │ │ Oppvekst          │ │2026│ │ T2      │
└──────────────┘ └───────────────────┘ └────┘ └─────────┘
```

Koble samme slicer til alle relevante PivotTables via Report Connections når de deler datakilde/model.

---

# 12. Timeline

For tidsfiltrering kan dashboardet bruke Timeline sammen med PivotTables der det er tilgjengelig.

Praktisk design:

```text
[Slicers]                              [Timeline: Jan ───── Dec]
```

Bruk enten Timeline eller en periode-slicer som primær tidskontroll. Ikke overlast siden med flere kontroller som gjør samme jobb.

---

# 13. Executive Dashboard

## Wireframe

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ØKONOMISK STATUS | EXCEL DASHBOARD                                  │
│ Budsjettnivå ▾ Virksomhetsområde ▾ År ▾ Periode ▾                  │
├──────────────┬──────────────┬──────────────┬─────────────────────────┤
│ REGNSKAP YTD │ BUDSJETT YTD │ AVVIK YTD    │ FORECAST AVVIK          │
│ 12,6 M       │ 17,3 M       │ 🟢 -4,6 M    │ 🔴 +x,x M              │
│              │              │ -26,7 %      │ +x,x %                 │
├──────────────────────────────────────────────────────────────────────┤
│ EXECUTIVE SUMMARY                                                   │
│ Dynamisk formeltekst som beskriver status og viktigste signal.      │
├───────────────────────────────┬──────────────────────────────────────┤
│ AVVIKSTREND                  │ STØRSTE AVVIKSDRIVERE               │
│ Line chart                   │ Horizontal bar / PivotChart          │
├───────────────────────────────┼──────────────────────────────────────┤
│ ENHETSSAMMENLIGNING          │ FORECAST / BRIDGE                   │
│ Bar / dot-style chart        │ Waterfall                           │
├───────────────────────────────┴──────────────────────────────────────┤
│ RAG OPPFØLGINGSMATRISE                                              │
└──────────────────────────────────────────────────────────────────────┘
```

---

# 14. KPI-kort i Excel

PivotTables kan hente measure-verdiene. Et dashboard kan vise disse i separate KPI-celler eller koblede tekstbokser.

Eksempel:

```text
AVVIK YTD
-4,6 M kr
-26,7 %
Gunstig
```

## Formeldrevet status i vanlig Excel-celle

Hvis KPI-avviket står i `B5`:

```excel
=IF(B5<0,"● Gunstig",IF(B5>0,"● Ugunstig","● Innenfor plan"))
```

Med toleranse basert på prosent i `B6`:

```excel
=IF(B6<-2%,"● Gunstig",IF(B6>2%,"● Ugunstig","● Innenfor toleranse"))
```

Bruk conditional formatting på statuscellen for å gi korrekt grønn/gul/rød farge.

---

# 15. Dynamisk Executive Summary i Excel

Eksempel der:

```text
B5 = Avvik YTD
B6 = Avvik YTD %
B7 = valgt virksomhetsområde
```

Formel:

```excel
=B7&": Regnskap er "&TEXT(ABS(B5)/1000000,"0.0")&" M kr "&
IF(B5<0,"lavere enn budsjett",IF(B5>0,"høyere enn budsjett","lik budsjett"))&
" ("&TEXT(B6,"0.0%")&"). "&
IF(B5<0,"Gunstig utvikling.",IF(B5>0,"Ugunstig utvikling.","Innenfor plan."))
```

Koble en tekstboks til cellen eller la en formatert celleblokk fungere som narrative card.

---

# 16. Avvikstrend

## Datagrunnlag

PivotTable:

```text
Rows: DimDate[YearMonth]
Values: [Avvik]
```

PivotChart:

```text
Line chart
X = YearMonth
Y = Avvik
```

## Nullinje

Legg inn en hjelpeserie med verdien `0` for alle måneder dersom charttypen ikke gir ønsket nullreferanse direkte.

Tolkning:

```text
Over 0  = rødt / ugunstig
Under 0 = grønt / gunstig
```

## Trend

Vis månedlig avvik og eventuelt kumulativt YTD-avvik som egen serie eller et eget chart.

---

# 17. Måned-over-måned DAX

```DAX
Avvik Forrige Måned :=
CALCULATE(
    [Avvik],
    DATEADD(DimDate[Date], -1, MONTH)
)
```

```DAX
Avvik Endring Måned :=
[Avvik] - [Avvik Forrige Måned]
```

```DAX
Trend Status :=
VAR ChangeValue = [Avvik Endring Måned]
RETURN
SWITCH(
    TRUE(),
    ISBLANK(ChangeValue), "N/A",
    ChangeValue < 0, "Forbedring",
    ChangeValue > 0, "Forverring",
    "Uendret"
)
```

Synkende kostnadsavvik betyr forbedring i denne fortegnsmodellen.

---

# 18. Root Cause i stedet for Decomposition Tree

Excel har ikke det samme Decomposition Tree-visualet som Power BI. Bygg derfor en root-cause PivotTable med hierarki.

## Pivot-hierarki

```text
Virksomhetsområde
  → Enhet
     → Lokasjon
        → Hovedgruppe
           → Kontoart
              → Kontonavn
```

Values:

```text
Avvik YTD
Avvik YTD %
```

Bruk expand/collapse til å bore ned i avviket.

## Visuell companion

Koble et horisontalt PivotChart til samme PivotTable eller en egen Top-N PivotTable.

---

# 19. Top-N avviksdrivere

Bruk PivotTable Value Filters → Top 10 eller et DAX-rankingsmål.

```DAX
Rang Ugunstig Avvik :=
RANKX(
    ALLSELECTED(DimAccount[Kontonavn]),
    [Avvik YTD],
    ,
    DESC,
    DENSE
)
```

I denne modellen er de høyeste positive avvikene de største ugunstige kostnadsavvikene.

Dashboardvisual:

```text
Fastlønn               █████████ +2,1 M 🔴
Vikar                   █████     +0,8 M 🔴
Overtid                 ███       +0,4 M 🔴
Andre                   ██        +0,2 M 🟠
```

---

# 20. Oppvekst / Grunnskole

Dashboardet kan gjenbruke samme struktur som Power BI-versjonen:

```text
Forbruk YTD
Avvik YTD
Vikarandel
Kostnad per elev
```

Deretter:

```text
Top-N kontodrivere
Vikarutvikling
Skolesammenligning
Kontospesifikasjon
```

## Ratio measures

Eksempel:

```DAX
Vikarandel :=
DIVIDE(
    [Vikarutgift],
    [Lønnskostnad]
)
```

```DAX
Kostnad per Elev :=
DIVIDE(
    [Netto Driftskostnad],
    [Antall Elever]
)
```

---

# 21. Helse & Mestring

Anbefalt Excel-side:

```text
Forbruk
Avvik
Overtid
Overtidsandel
Forecast etter tiltak
```

Visualer:

```text
Avvik per boenhet/lokasjon
Månedlig overtidsutvikling
Top-N kontodrivere
Oppfølgingsmatrise
```

---

# 22. Lønn & Vikarmonitor

KPI-er:

```text
Lønn YTD
Vikarutgift
Overtid
NAV-refusjon
```

Visualer:

```text
Månedlig vikarutvikling
Vikarandel per enhet
Lønns-/refusjonsmatrise
```

Eksempel measures:

```DAX
Vikarutgift :=
CALCULATE(
    [Regnskap],
    DimAccount[Kontoart] = "1020"
)
```

```DAX
Overtid :=
CALCULATE(
    [Regnskap],
    DimAccount[Kontoart] = "1090"
)
```

Tilpass filterverdiene til kontoplanen.

---

# 23. Prognose og scenario

Excel er godt egnet for synlige scenarioforutsetninger.

## Inputområde

```text
Lønnsdeflator             [2,3 %]
Fraværsreduksjon          [0,8 %]
Planlagt tiltakseffekt    [3,0 M]
```

Bruk blå font for brukerinput i en ny finansmodell og tydelig markering av scenariofeltene.

## Scenario output

```text
Årsramme
Forecast uten tiltak
Tiltakseffekt
Simulert EOY
Restavvik
```

## Waterfall

Bygg et vanlig Excel Waterfall Chart fra en liten helper-tabell:

```text
Årsramme
Forecast-gap
Tiltakseffekt
Lønns-/fraværseffekt
Simulert sluttposisjon
```

---

# 24. EVM

Measures:

```DAX
PV := SUM(FactEVM[PV])
```

```DAX
AC := SUM(FactEVM[AC])
```

```DAX
CV := [PV] - [AC]
```

```DAX
CPI := DIVIDE([PV], [AC])
```

> Merk: behold den EVM-definisjonen som faktisk er vedtatt i løsningen. Dokumenter definisjonene på `00_README`.

Visualer:

```text
PV / AC KPI
CV per enhet
CPI
Trend
Prosjektdetalj
```

---

# 25. Audit Trail

Eget ark:

```text
09_AUDIT
```

Vis:

```text
Tidsstempel
Enhet
Tiltak/forslag
Beslutning
Saksbehandler
Begrunnelse
Integritetsreferanse/hash
```

Bruk Excel Table med filterknapper og eventuelt slicers for felter som egner seg.

RAG skal ikke brukes på `APPROVED`, `MODIFIED` eller andre beslutningskoder med mindre virksomheten har definert hva grønn/gul/rød faktisk betyr.

---

# 26. Tooltip-alternativer i Excel

Excel har ikke samme report-page-tooltip-opplevelse som Power BI. Bruk derfor en kombinasjon av:

1. **Hjelpeceller ved siden av chart/KPI**
2. **Datalabels** på viktige punkter
3. **Cell Notes/Comments** for definisjoner
4. **Et eget HELP-panel** som åpnes/vises på dashboardarket
5. **Detaljark** for full analyse

Eksempel HELP-panel:

```text
AVVIK
Avvik = Regnskap - Budsjett.
Negativt kostnadsavvik er gunstig og markeres grønt.
Positivt kostnadsavvik er ugunstig og markeres rødt.
```

---

# 27. Drillthrough-alternativ i Excel

Bruk tre nivåer:

```text
Dashboard
   ↓
Root Cause Pivot
   ↓
Detail Pivot / Excel Table
```

PivotTable expand/collapse kan brukes til å gå fra virksomhetsområde til konto. Et eget detaljark kan inneholde filtrert transaksjons- eller kontospesifikasjon.

---

# 28. Interaksjonsdesign

Alle hoved-PivotTables bør bruke samme Data Model slik at felles slicers kan kobles via Report Connections.

Eksempel:

```text
Budsjettnivå slicer ─┬─ KPI Pivot
                     ├─ Trend Pivot
                     ├─ Root Cause Pivot
                     ├─ Driver Pivot
                     └─ Matrix Pivot

Virksomhetsområde ───┴─ samme rapportobjekter
```

Dette er nøkkelen til å få Excel-dashboardet til å oppleves mer som en interaktiv BI-rapport.

---

# 29. Dashboard-storytelling

Hold samme historie gjennom hele workbooken:

```text
STATUS
  ↓
KONTEKST
  ↓
AVVIK
  ↓
TREND
  ↓
ROOT CAUSE
  ↓
FORECAST / SCENARIO
  ↓
TILTAK
  ↓
AUDIT
```

---

# 30. Visual-standard

## Bruk

- KPI-celler / tekstbokser
- Line chart for tid
- Horisontal bar for ranking/avviksdrivere
- Waterfall for bridge
- PivotTable for hierarki og root cause
- Scatter når du undersøker sammenheng mellom to numeriske KPI-er
- Små tabeller/matriser for oppfølging

## Unngå

- mange 3D-charts
- pie charts med mange kategorier
- brede diagrammer med vertikale kontonavn
- dekorativ RAG
- dashboards med synlige støtte-PivotTables

---

# 31. Fargepalett

```text
Canvas / arkbakgrunn       #F5F6F8
Cards                      #FFFFFF
Primary blue               #2589E8
Text                        #2B2B2B
Secondary text              #6B6B6B
Green / gunstig             #3A8F5C
Amber / toleranse           #E6A23C
Red / ugunstig              #D64545
Neutral                     #D8DDE3
```

---

# 32. Tallformat

Dashboard:

```text
12 641 753 kr → 12,6 M kr
1 224 900 kr  → 1,2 M kr
18 902 kr     → 18,9 K kr
0,101         → 10,1 %
```

Detaljark kan vise full presisjon.

I finansielle støttetabeller kan null vises som `-`. Hold dashboardets RAG-semantikk separat fra et generelt regnskapsformat som farger negative tall røde, fordi **negative kostnadsavvik skal være grønne i denne løsningen**.

---

# 33. Materialitetsjustert RAG

Prosent alene er ikke nok på kontonivå.

Eksempel:

```DAX
RAG Materialitet :=
VAR VarianceValue = [Avvik YTD]
VAR VariancePct = [Avvik YTD %]
VAR Materiality = 100000
RETURN
SWITCH(
    TRUE(),
    ISBLANK(VarianceValue), "N/A",
    ABS(VarianceValue) < Materiality, "Amber",
    VariancePct < -0.02, "Green",
    VariancePct >  0.02, "Red",
    "Amber"
)
```

Flytt gjerne `Materiality`, grønn terskel og rød terskel til en kontroll-/parametertabell slik at de ikke blir skjulte magic numbers i løsningen.

---

# 34. Kontrollark

`01_CONTROL` bør holde synlige styringsforutsetninger:

```text
RAG green threshold      -2,0 %
RAG red threshold         2,0 %
Materiality              100 000 kr
Aktivt år                2026
Oppdateringsdato         [dato]
Datakilde                [beskrivelse]
```

Dette gjør modellen enklere å forvalte.

---

# 35. QA-ark

`99_QA` kan inneholde:

```text
Rader i FactFinance
Manglende OrgKey
Manglende AccountKey
Manglende dato
Actual uten budsjett
Budsjett uten actual
Duplikate nøkler i dimensjoner
Siste tilgjengelige periode
```

Dashboardet bør ikke publiseres/brukes til styring før kritiske modellkontroller er akseptable.

---

# 36. Refresh-strategi

Anbefalt arbeidsflyt:

```text
Oppdater datakilder
      ↓
Refresh All
      ↓
Power Query oppdateres
      ↓
Data Model oppdateres
      ↓
DAX measures beregnes
      ↓
PivotTables / PivotCharts oppdateres
      ↓
Dashboard viser ny status
```

---

# 37. Excel Dashboard QA

## Model

- [ ] Faktatabell og dimensioner er tydelig separert.
- [ ] Relasjoner bruker entydige dimensjonsnøkler.
- [ ] Datotabellen dekker relevante perioder.
- [ ] Measures, ikke tilfeldige celleformler, driver sentrale KPI-er.

## RAG

- [ ] `Avvik = Regnskap - Budsjett`.
- [ ] Negativt kostnadsavvik vises grønt.
- [ ] Positivt kostnadsavvik vises rødt.
- [ ] Toleranseområdet er dokumentert.
- [ ] Materialitet er vurdert.

## Slicers

- [ ] Budsjettnivå er tilgjengelig.
- [ ] Virksomhetsområde er tilgjengelig.
- [ ] År/periode kan filtreres.
- [ ] Report Connections er satt på alle relevante PivotTables.
- [ ] Dashboardet viser tydelig aktiv filterkontekst.

## Visuals

- [ ] Trend bruker kronologisk måned.
- [ ] Avviksgraf har tydelig nullinje.
- [ ] Top-N brukes på lange kategorilister.
- [ ] Root-cause-hierarkiet kan expand/collapse.
- [ ] Detaljdata er flyttet bort fra executive dashboard.

## UX

- [ ] Gridlines er skjult på dashboardark.
- [ ] Ingen støtte-Pivots er synlige på executive-siden.
- [ ] Alle KPI-er har enhet.
- [ ] Farger brukes konsekvent.
- [ ] Dashboardet fungerer etter Refresh All.

---

# 38. Implementeringsplan

## Fase 1

```text
Power Query
Data Model
Relationships
Date dimension
Basismeasures
```

## Fase 2

```text
YTD measures
Avvik
RAG
Forecast
Ratio KPI-er
```

## Fase 3

```text
PivotTables
Slicers
Timeline
Report Connections
```

## Fase 4

```text
KPI dashboard
Trend
Top-N drivers
Root Cause
Waterfall
RAG matrix
```

## Fase 5

```text
Scenario
EVM
Audit
QA
README
```

---

# 39. Hva Excel kan matche godt og hva som bør løses annerledes

## Svært godt egnet i Excel

```text
Power Query ETL
Data Model
Relationships
DAX measures
PivotTables
PivotCharts
Slicers
Timeline
RAG conditional formatting
Scenario-input
Detaljanalyse
Controllerarbeid
```

## Bør designes annerledes enn i Power BI

```text
Decomposition Tree → hierarkisk Pivot + Top-N/root-cause side
Report page tooltip → hjelpepanel/notater/detaljark
AI narrative → formeldrevet narrative eller tilgjengelige Copilot-funksjoner
Svært interaktive rapportreiser → slicers + report connections + egne analyseark
```

Målet er ikke å kopiere hvert Power BI-objekt én til én. Målet er å bevare samme **styringslogikk, datamodell, filterkontekst og beslutningsreise** med Excels egne styrker.

---

# 40. Sluttarkitektur

```text
POWER QUERY
   ↓
DATA MODEL / POWER PIVOT
   ↓
DAX MEASURES
   ↓
PIVOTTABLES
   ↓
SLICERS / TIMELINE
   ↓
PIVOTCHARTS + KPI CELLS
   ↓
RAG + STORYTELLING
   ↓
ROOT CAUSE / SCENARIO / AUDIT
```

Dette gir et Excel-oppsett som ligger svært nær Power BI-konseptet på modell- og analyseplanet, samtidig som workbooken beholder Excels styrke i controllerarbeid, scenarioinput og detaljanalyse.

---

# 41. Microsoft-referanser

- Power Pivot gir avansert datamodellering i Excel og støtter Data Model med tabeller, relasjoner, calculated columns og measures.
- DAX i Power Pivot er et formelspråk for calculated columns og measures, med blant annet filterkontekst og time-intelligence-scenarier.
- PivotTables kan bygges fra workbookens Data Model, inkludert modeller med flere tabeller og custom measures.
- PivotCharts kan bruke PivotTable-feltoppsettet for å analysere og visualisere data.
- Slicers filtrerer tabeller/PivotTables og kan kobles til flere PivotTables som deler samme datakilde.
- PivotTable-layout kan bruke conditional formatting.
