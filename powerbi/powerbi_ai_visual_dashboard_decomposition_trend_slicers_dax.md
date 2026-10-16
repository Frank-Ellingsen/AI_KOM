# Power BI AI Visual Dashboard
## Decomposition Tree, avvikstrend, slicere, Q&A/Copilot, AI-visualer, tooltips og komplett DAX-pakke

Denne spesifikasjonen supplerer den samlede rapportpakken med en egen analyse- og AI-side i Power BI Desktop. Siden er laget for kommunal økonomi- og controlleroppfølging og skal forklare:

```text
Hvor stort er avviket?
        ↓
Hvordan utvikler avviket seg?
        ↓
Hvor oppstår avviket?
        ↓
Hvilke dimensjoner og drivere forklarer avviket?
        ↓
Hva bør undersøkes eller følges opp?
```

> **Viktig fortegnskonvensjon i denne pakken:**
>
> `Avvik = Regnskap - Budsjett`
>
> For kostnader betyr dette:
>
> - Negativt avvik = lavere kostnad enn budsjett = **grønt/gunstig**
> - Positivt avvik = høyere kostnad enn budsjett = **rødt/ugunstig**
> - Avvik nær null = **gult/nøytralt innenfor toleranse**

---

# 1. Foreslått side

## Sidenavn

```text
8. Avviksanalyse | AI & Root Cause
```

## Undertittel

```text
Trend, drivere, naturlig språk og interaktiv rotårsaksanalyse
```

---

# 2. Konkret wireframe

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ AVVIKSANALYSE | AI & ROOT CAUSE                         Periode: [valgt]    │
│ Trend, drivere og forklaringer på budsjettavvik                             │
├──────────────────────────────────────────────────────────────────────────────┤
│ Budsjettnivå ▾  Virksomhetsområde ▾  Enhet ▾  Periode ▾  Kontogruppe ▾     │
├───────────────┬───────────────┬───────────────┬──────────────────────────────┤
│ REGNSKAP YTD  │ BUDSJETT YTD  │ AVVIK YTD     │ AVVIK YTD %                │
│ 12,6 M kr     │ 17,3 M kr     │ 🟢 -4,6 M kr  │ 🟢 -26,7 %                 │
│               │               │ Gunstig        │ Under budsjett              │
├──────────────────────────────────────────────────────────────────────────────┤
│ 🟢 STATUS                                                                   │
│ Regnskap er 4,6 M kr lavere enn budsjett. Valgt virksomhetsområde står      │
│ for [andel] av totalavviket. Trenden siste observerte periode er [retning]. │
├────────────────────────────────────────┬─────────────────────────────────────┤
│ 01 | HVORDAN UTVIKLER AVVIKET SEG?    │ 02 | HVA FORKLARER AVVIKET?        │
│                                        │                                     │
│ Linjediagram: Avvik per måned          │ Decomposition Tree                  │
│                                        │                                     │
│ +0,5M ───────────── rød sone           │ Avvik YTD                           │
│    0  ─ ─ ─ ─ ─ nullinje              │  ├ Virksomhetsområde                │
│ -0,5M     ╲__╱╲___ grønn sone          │  │  ├ Enhet / lokasjon              │
│          Actual ┆ Forecast             │  │  │  ├ Hovedgruppe                 │
│                  ░░ forventningsbånd   │  │  │  │  ├ Kontoart                  │
│                                        │  │  │  │  │  └ Kontonavn              │
├────────────────────────────────────────┼─────────────────────────────────────┤
│ 03 | HVILKE FAKTORER PÅVIRKER?        │ 04 | SPØR DATAENE                   │
│                                        │                                     │
│ Key Influencers / Top Segments         │ Copilot-pane eller Q&A-visual       │
│                                        │                                     │
│ Driver 1                               │ Forslag:                            │
│ Driver 2                               │ «Vis avvik per virksomhetsområde»   │
│ Driver 3                               │ «Hvilke kontoer har størst avvik?»  │
├────────────────────────────────────────┴─────────────────────────────────────┤
│ 05 | OPPFØLGING                                                           │
│ RAG │ Virksomhetsområde │ Enhet │ Budsjett │ Regnskap │ Avvik │ Avvik %   │
│ 🟢  │ Oppvekst          │ ...   │ ...      │ ...      │ -...  │ -... %    │
│ 🔴  │ Helse             │ ...   │ ...      │ ...      │ +...  │ +... %    │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

# 3. Slicere

## 3.1 Primære slicere

### Budsjettnivå

Anbefalt hierarki, tilpasset feltene i den faktiske modellen:

```text
Totalramme
Sektor
Virksomhetsområde
Enhet
Lokasjon / ansvar
```

Anbefaling:

- Bruk nedtrekksliste.
- Tillat ett valg dersom nivået styrer hele rapportens aggregering.
- Synkroniser sliceren mellom relevante økonomisider.
- Bruk en egen sorteringskolonne dersom nivåene ikke sorteres logisk alfabetisk.

### Virksomhetsområde

Eksempler fra rapportpakken:

```text
Oppvekst
Helse og mestring
```

Anbefaling:

- Dropdown med søk.
- Tillat flervalg når ledelsen skal sammenligne områder.
- Bruk ett valg på root-cause-siden dersom Decomposition Tree ellers blir for kompleks.

## 3.2 Sekundære slicere

```text
Periode / måned
Tertial
År
Enhet
Lokasjon / ansvar
Hovedgruppe
Kontoart
Scenario
```

## 3.3 Slicer-panel

Primære slicere kan ligge synlig i topprekken. Sekundære slicere kan ligge i et sammenleggbart filterpanel via bookmark og knapp.

```text
[ Budsjettnivå ▾ ] [ Virksomhetsområde ▾ ] [ Periode ▾ ] [ Flere filtre ]
```

---

# 4. Forutsatt datamodell

DAX-eksemplene under bruker generiske tabell- og feltnavn:

```text
FactFinance
    [AmountActual]
    [AmountBudget]
    [DateKey]
    [AccountKey]
    [OrgKey]

DimDate
    [Date]
    [Year]
    [MonthNo]
    [MonthName]
    [YearMonth]
    [YearMonthSort]

DimOrganization
    [Budsjettnivå]
    [Virksomhetsområde]
    [Enhet]
    [Lokasjon]
    [Ansvar]

DimAccount
    [Hovedgruppe]
    [Kontoart]
    [Kontokode]
    [Kontonavn]
```

Erstatt navnene med de faktiske navnene i semantic model.

---

# 5. Basismeasures

## Regnskap

```DAX
Regnskap =
SUM(FactFinance[AmountActual])
```

## Budsjett

```DAX
Budsjett =
SUM(FactFinance[AmountBudget])
```

## Avvik

Fortegnskonvensjonen er Actual minus Budget.

```DAX
Avvik =
[Regnskap] - [Budsjett]
```

## Avvik prosent

```DAX
Avvik % =
DIVIDE(
    [Avvik],
    ABS([Budsjett])
)
```

`ABS([Budsjett])` brukes i nevneren slik at prosentfortegnet følger avviket og ikke påvirkes av eventuell regnskapsmessig fortegnsvisning i budsjettet.

---

# 6. YTD-measures

## Regnskap YTD

```DAX
Regnskap YTD =
TOTALYTD(
    [Regnskap],
    DimDate[Date]
)
```

## Budsjett YTD

```DAX
Budsjett YTD =
TOTALYTD(
    [Budsjett],
    DimDate[Date]
)
```

## Avvik YTD

```DAX
Avvik YTD =
[Regnskap YTD] - [Budsjett YTD]
```

## Avvik YTD prosent

```DAX
Avvik YTD % =
DIVIDE(
    [Avvik YTD],
    ABS([Budsjett YTD])
)
```

---

# 7. Månedlige measures til trendlinje

## Regnskap måned

```DAX
Regnskap Måned =
[Regnskap]
```

## Budsjett måned

```DAX
Budsjett Måned =
[Budsjett]
```

## Avvik måned

```DAX
Avvik Måned =
[Regnskap Måned] - [Budsjett Måned]
```

## Avvik måned prosent

```DAX
Avvik Måned % =
DIVIDE(
    [Avvik Måned],
    ABS([Budsjett Måned])
)
```

## Kumulativt avvik

```DAX
Avvik Kumulativt =
CALCULATE(
    [Avvik],
    FILTER(
        ALLSELECTED(DimDate[Date]),
        DimDate[Date] <= MAX(DimDate[Date])
    )
)
```

---

# 8. RAG med brukerens fortegnsregel

## Anbefalt toleranse

Denne pakken bruker et eksempel på toleranse rundt null:

```text
Grønn: Avvik < -2 %
Gul:   Avvik mellom -2 % og +2 %
Rød:   Avvik > +2 %
```

Hvis virksomheten ønsker helt streng fortegnslogikk, kan nullgrensene settes til 0 %.

## RAG Status YTD

```DAX
RAG Status YTD =
VAR Pct = [Avvik YTD %]
VAR GreenLimit = -0.02
VAR RedLimit = 0.02
RETURN
SWITCH(
    TRUE(),
    ISBLANK(Pct), "N/A",
    Pct < GreenLimit, "Green",
    Pct > RedLimit, "Red",
    "Amber"
)
```

## RAG Color YTD

```DAX
RAG Color YTD =
SWITCH(
    [RAG Status YTD],
    "Green", "#3A8F5C",
    "Amber", "#E6A23C",
    "Red",   "#D64545",
    "#A0A0A0"
)
```

## RAG Symbol YTD

```DAX
RAG Symbol YTD =
SWITCH(
    [RAG Status YTD],
    "Green", "●",
    "Amber", "●",
    "Red",   "●",
    "○"
)
```

## RAG Label YTD

```DAX
RAG Label YTD =
SWITCH(
    [RAG Status YTD],
    "Green", "Gunstig",
    "Amber", "Innenfor toleranse",
    "Red",   "Ugunstig",
    "Ikke vurdert"
)
```

---

# 9. Streng variant uten toleranse

Bruk denne bare dersom enhver negativ verdi skal være grønn og enhver positiv verdi rød.

```DAX
RAG Status Streng =
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

```DAX
RAG Color Streng =
SWITCH(
    [RAG Status Streng],
    "Green", "#3A8F5C",
    "Amber", "#E6A23C",
    "Red",   "#D64545",
    "#A0A0A0"
)
```

---

# 10. Materialitetsjustert RAG

Bruk denne varianten på konto- eller enhetsnivå når små beløp ellers får for sterk status.

```DAX
RAG Status Materialitet =
VAR VarianceValue = [Avvik YTD]
VAR VariancePct = [Avvik YTD %]
VAR Materiality = 100000
VAR GreenPct = -0.02
VAR RedPct = 0.02
RETURN
SWITCH(
    TRUE(),
    ISBLANK(VarianceValue), "N/A",
    ABS(VarianceValue) < Materiality, "Amber",
    VariancePct < GreenPct, "Green",
    VariancePct > RedPct, "Red",
    "Amber"
)
```

`100000` er kun et eksempel. Materialitetsgrensen bør hentes fra virksomhetens styringsregler eller en egen parametertabell.

---

# 11. Dynamisk KPI-tekst

## Avvik YTD med symbol

```DAX
Avvik YTD Display =
[RAG Symbol YTD] & " " &
FORMAT([Avvik YTD], "#,##0,,.0 M kr")
```

## Avvik YTD prosent med status

```DAX
Avvik YTD Prosent Display =
FORMAT([Avvik YTD %], "0.0 %") &
" | " & [RAG Label YTD]
```

> Dersom `FORMAT()` gir uønsket separatorsyntaks i modellen, bruk measurets format string eller dynamic format string i semantic model fremfor å gjøre alle numeriske mål om til tekst.

---

# 12. Decomposition Tree

## Formål

Decomposition Tree skal brukes til rotårsaksanalyse av avvik.

## Feltoppsett

```text
Analyze:
    [Avvik YTD]

Explain by:
    DimOrganization[Budsjettnivå]
    DimOrganization[Virksomhetsområde]
    DimOrganization[Enhet]
    DimOrganization[Lokasjon]
    DimOrganization[Ansvar]
    DimAccount[Hovedgruppe]
    DimAccount[Kontoart]
    DimAccount[Kontonavn]
```

## Anbefalt analysebane

```text
Avvik YTD
  → Virksomhetsområde
      → Enhet
          → Lokasjon
              → Hovedgruppe
                  → Kontoart
                      → Kontonavn
```

## AI-splits

Bruk:

```text
High value
```

for å finne dimensjonsverdien med størst positivt avvik, altså størst ugunstig kostnadsoverskridelse etter denne pakkens fortegnskonvensjon.

Bruk:

```text
Low value
```

for å finne størst negativt avvik, altså størst gunstig mindreforbruk.

## Designregel

Decomposition Tree blir bredt. Gi visualet minst halv sidebredde, og vurder focus mode for detaljert analyse.

---

# 13. Linjediagram for avvikstrend

## Foreslått oppsett

```text
X-axis:
    DimDate[YearMonth]

Y-axis:
    [Avvik Måned]

Tooltip:
    [Regnskap Måned]
    [Budsjett Måned]
    [Avvik Måned]
    [Avvik Måned %]
    [RAG Label Måned]
```

Sorter `DimDate[YearMonth]` etter `DimDate[YearMonthSort]`.

## Månedlig RAG

```DAX
RAG Status Måned =
VAR Pct = [Avvik Måned %]
RETURN
SWITCH(
    TRUE(),
    ISBLANK(Pct), "N/A",
    Pct < -0.02, "Green",
    Pct > 0.02, "Red",
    "Amber"
)
```

```DAX
RAG Label Måned =
SWITCH(
    [RAG Status Måned],
    "Green", "Gunstig",
    "Amber", "Innenfor toleranse",
    "Red", "Ugunstig",
    "Ikke vurdert"
)
```

## Nullinje

Legg til en konstantlinje på `0`.

Tolkning:

```text
Over null  = positivt kostnadsavvik = rødt/ugunstig
Under null = negativt kostnadsavvik = grønt/gunstig
```

## Trendmål

```DAX
Avvik Forrige Måned =
CALCULATE(
    [Avvik Måned],
    DATEADD(DimDate[Date], -1, MONTH)
)
```

```DAX
Avvik Endring Måned =
[Avvik Måned] - [Avvik Forrige Måned]
```

```DAX
Avvik Trend Retning =
VAR ChangeValue = [Avvik Endring Måned]
RETURN
SWITCH(
    TRUE(),
    ISBLANK(ChangeValue), "Ingen sammenligning",
    ChangeValue < 0, "Forbedring",
    ChangeValue > 0, "Forverring",
    "Uendret"
)
```

Her betyr synkende avvik en forbedring fordi avviket beveger seg i negativ/grønn retning.

## Forecast og forventningsbånd

Bruk Analytics-panelet på et støttet linjediagram dersom historikken og visualoppsettet støtter forecast. Skill tydelig mellom actual og forecast med stiplet linje eller nøytral gråtone.

## Anomalier

Anomaly detection kan legges til linjediagrammet for å markere uventede topper og fall. Bruk felt som virksomhetsområde, enhet, hovedgruppe og kontoart som relevante forklaringsdimensjoner når modellen og visualet støtter dette.

---

# 14. Trend-tooltip

Lag en egen report page tooltip:

```text
PERIODE
────────────────────
Regnskap måned
Budsjett måned
Avvik måned
Avvik måned %
RAG-status

Endring fra forrige måned
Trendretning
Kumulativt avvik YTD
```

Tooltipsiden skal være kompakt og uten slicere eller scrollbar.

---

# 15. Dynamiske titler

## Valgt virksomhetsområde

```DAX
Valgt Virksomhetsområde =
SELECTEDVALUE(
    DimOrganization[Virksomhetsområde],
    "Alle virksomhetsområder"
)
```

## Valgt budsjettnivå

```DAX
Valgt Budsjettnivå =
SELECTEDVALUE(
    DimOrganization[Budsjettnivå],
    "Alle budsjettnivåer"
)
```

## Tittel avvikstrend

```DAX
Tittel Avvikstrend =
"Hvordan utvikler avviket seg? | " &
[Valgt Virksomhetsområde] &
" | " & [Valgt Budsjettnivå]
```

## Tittel Decomposition Tree

```DAX
Tittel Decomposition Tree =
"Hva forklarer avviket? | " &
[Valgt Virksomhetsområde]
```

---

# 16. Executive Summary DAX

```DAX
Executive Summary Avvik =
VAR VarianceValue = [Avvik YTD]
VAR VariancePct = [Avvik YTD %]
VAR StatusLabel = [RAG Label YTD]
VAR Area = [Valgt Virksomhetsområde]
VAR Direction =
    IF(
        VarianceValue < 0,
        "lavere enn budsjett",
        IF(VarianceValue > 0, "høyere enn budsjett", "lik budsjett")
    )
RETURN
Area & ": Regnskap er " &
FORMAT(ABS(VarianceValue), "#,##0,,.0 M kr") &
" " & Direction &
" (" & FORMAT(VariancePct, "0.0 %") & "). " &
"Status: " & StatusLabel & "."
```

---

# 17. Oppfølgingsmatrise

## Kolonner

```text
RAG-symbol
Virksomhetsområde
Enhet
Lokasjon
Budsjett YTD
Regnskap YTD
Avvik YTD
Avvik YTD %
Trendretning
```

## Conditional formatting

Bruk `[RAG Color YTD]` som feltverdi for:

- RAG-symbol
- fontfarge på avvik
- eventuelt en tynn statusindikator

Ikke fargelegg hele raden.

## Sortering

Standard sortering bør fremheve største positive avvik først, fordi positive kostnadsavvik er røde og ugunstige i denne modellen.

---

# 18. Key Influencers

## Formål

Bruk Key Influencers til å undersøke hvilke faktorer som påvirker avviket eller sannsynligheten for rød status.

## Variant A: numerisk analyse

```text
Analyze:
    [Avvik YTD]

Explain by:
    Virksomhetsområde
    Enhet
    Lokasjon
    Hovedgruppe
    Kontoart
    Måned
```

## Variant B: kategorisk analyse

Lag en klassifisering:

```DAX
RAG Is Red =
IF([RAG Status YTD] = "Red", "Red", "Not Red")
```

Bruk deretter kategorien i en egnet modell-/visualkontekst for å analysere hva som kjennetegner røde avvik.

## Forsiktighet

Key Influencers identifiserer statistiske drivere og segmenter i tilgjengelige data. Resultatene bør brukes som analysehypoteser og valideres faglig før tiltak besluttes.

---

# 19. Q&A og Copilot

## Q&A-visual

Q&A lar brukeren stille spørsmål i naturlig språk og få svar som visual. Eksempler på foreslåtte spørsmål:

```text
Vis avvik YTD per virksomhetsområde
Vis positive avvik per enhet
Hvilke kontoarter har størst positivt avvik?
Vis avvik måned for måned
Vis regnskap og budsjett for Helse og mestring
Vis topp 10 enheter etter avvik YTD
```

## Viktig produktretning

Power BI Q&A er varslet avviklet i februar 2027. For en ny, langsiktig rapport bør Copilot for Power BI være hovedretningen, mens Q&A eventuelt brukes som en midlertidig eller eksisterende funksjon.

## Copilot-panelet

Aktuelle bruksområder:

- stille spørsmål om rapportdata
- be om sammendrag av en side
- lage eller redigere visualer med naturlig språk
- få hjelp til DAX
- opprette narrative sammendrag

Copilot krever at organisasjonens kapasitet, administratorinnstillinger, region og brukerens tilgang støtter funksjonen.

## Modellforberedelse for naturlig språk

Bruk forretningsvennlige navn:

```text
Avvik YTD
Virksomhetsområde
Budsjettnivå
Regnskap YTD
Budsjett YTD
```

Unngå tekniske navn som:

```text
fact_fin_amt_act
org_lvl_02
var_ytd_calc_v3
```

Legg inn synonymer og beskrivelser i modellen der dette er relevant, eksempelvis:

```text
Virksomhetsområde: sektor, tjenesteområde, område
Regnskap: actual, faktisk, forbruk
Budsjett: plan, ramme
Avvik: variance, differanse
```

---

# 20. Smart Narrative

Bruk Narrative visual som et kort tekstlig sammendrag, ikke som en lang rapport.

Anbefalt plassering:

```text
Under KPI-raden
```

Anbefalt innhold:

```text
1. Total status
2. Største driver
3. Trendretning
4. Forecast/risiko dersom tilgjengelig
```

Custom mode kan knyttes til egne mål som `[Executive Summary Avvik]`. Copilot mode kan brukes når lisens- og kapasitetskravene er oppfylt.

---

# 21. Help tooltips

Legg hjelp-tooltip på:

- Avvik
- RAG
- Decomposition Tree
- Key Influencers
- CPI/CV på EVM-siden
- Forecast og scenario

Eksempel:

```text
Hvordan tolkes avvik?
Avvik = Regnskap - Budsjett.
Negativt avvik betyr lavere kostnad enn budsjett og vises grønt.
Positivt avvik betyr høyere kostnad enn budsjett og vises rødt.
```

---

# 22. Bokmerker og analysemønstre

Anbefalte visningsmodi:

```text
[ Trend ] [ Root Cause ] [ AI Insights ]
```

- Trend viser linjediagram og periodisk analyse.
- Root Cause viser Decomposition Tree og Top-N-driverne.
- AI Insights viser Key Influencers, Narrative og Copilot/Q&A-inngang.

Bruk bookmarks og selection pane for å bytte visning uten å overfylle siden.

---

# 23. Top-N-driveranalyse

Decomposition Tree bør suppleres med en stabil, ledervennlig Top-N-visning.

## Rangering

```DAX
Rang Avvik Ugunstig =
RANKX(
    ALLSELECTED(DimAccount[Kontonavn]),
    [Avvik YTD],
    ,
    DESC,
    DENSE
)
```

## Vis Top 10

```DAX
Vis Top 10 Avvik =
IF([Rang Avvik Ugunstig] <= 10, 1, 0)
```

Legg `[Vis Top 10 Avvik] = 1` som visualfilter.

Siden positive avvik er ugunstige i denne modellen, sorteres de høyeste positive avvikene først.

---

# 24. Andel av totalavvik

```DAX
Avvik Andel av Valgt Total =
DIVIDE(
    [Avvik YTD],
    CALCULATE(
        [Avvik YTD],
        ALLSELECTED(DimOrganization[Enhet])
    )
)
```

Dette kan brukes i tooltip og Executive Summary til å vise hvor stor del av det valgte totalavviket en enhet representerer.

---

# 25. Siste faktiske periode

```DAX
Siste Faktiske Dato =
CALCULATE(
    MAX(DimDate[Date]),
    FILTER(
        ALL(DimDate[Date]),
        NOT ISBLANK(CALCULATE([Regnskap]))
    )
)
```

```DAX
Siste Faktiske Periode =
VAR LastDate = [Siste Faktiske Dato]
RETURN
FORMAT(LastDate, "MMM yyyy")
```

Bruk dette i undertittel eller tooltip slik at brukeren ser hvor ferske tallene er.

---

# 26. Datakvalitetsmål

## Manglende virksomhetsområde

```DAX
Rader Uten Virksomhetsområde =
CALCULATE(
    COUNTROWS(FactFinance),
    ISBLANK(DimOrganization[Virksomhetsområde])
)
```

## Manglende konto

```DAX
Rader Uten Konto =
CALCULATE(
    COUNTROWS(FactFinance),
    ISBLANK(DimAccount[Kontokode])
)
```

Disse målene kan plasseres på en skjult QA-side eller i en datakvalitets-tooltip.

---

# 27. Tilgjengelighet

RAG skal aldri kommuniseres bare med farge.

Bruk:

```text
● Gunstig
● Innenfor toleranse
● Ugunstig
```

Sørg også for:

- meningsfull alt-tekst
- logisk tab-rekkefølge
- høy nok kontrast
- tydelige visualtitler
- fontstørrelser som kan leses i presentasjonsmodus
- hjelp-tooltip for ukjente AI-visualer

---

# 28. Visuell standard

```text
Canvas                  #F5F6F8
Cards                    #FFFFFF
Primary blue             #2589E8
Text                      #2B2B2B
Secondary text            #6B6B6B
Green / gunstig           #3A8F5C
Amber / toleranse         #E6A23C
Red / ugunstig            #D64545
Neutral                   #D8DDE3
```

På avvikstrenden:

```text
Positivt område / ugunstig   svak rød bakgrunn eller rød markør
Nullinje                     mørk grå
Negativt område / gunstig    svak grønn bakgrunn eller grønn markør
Forecast                     grå stiplet linje / grått intervall
```

---

# 29. Implementeringsrekkefølge

## Fase 1: Modell og DAX

1. Kontroller fortegnskonvensjonen.
2. Opprett basis-, YTD- og trendmeasures.
3. Opprett RAG med negativt = grønt og positivt = rødt.
4. Opprett dynamiske titler og Executive Summary.
5. Opprett sorteringskolonner for måned og budsjettnivå.

## Fase 2: Slicere og KPI-er

1. Budsjettnivå.
2. Virksomhetsområde.
3. Periode.
4. Enhet.
5. KPI-rad med conditional formatting.

## Fase 3: Hovedvisualer

1. Linjediagram med nullinje.
2. Decomposition Tree.
3. Top-N-driverdiagram.
4. Oppfølgingsmatrise.

## Fase 4: AI og kontekst

1. Anomaly detection når visual/data støtter funksjonen.
2. Key Influencers.
3. Smart Narrative.
4. Copilot-panelet når miljøet støtter det.
5. Q&A bare dersom rapportstrategien aksepterer avviklingen i februar 2027.

## Fase 5: UX og QA

1. Report page tooltips.
2. Help tooltips.
3. Bookmarks.
4. Drillthrough.
5. Accessibility-test.
6. Testing i Power BI Service og målkapasitet.

---

# 30. QA-sjekkliste

## DAX og fortegn

- [ ] Er `Avvik = Regnskap - Budsjett` brukt konsekvent?
- [ ] Blir negativt kostnadsavvik grønt?
- [ ] Blir positivt kostnadsavvik rødt?
- [ ] Er avvik nær null håndtert med toleranse eller gul status?
- [ ] Er prosentmålet basert på absolutt budsjett i nevneren?

## Slicere

- [ ] Finnes Budsjettnivå?
- [ ] Finnes Virksomhetsområde?
- [ ] Er slicere synkronisert der det er hensiktsmessig?
- [ ] Er slicer-interaksjoner testet mot alle visualer?
- [ ] Er sekundære filtre skjult i filterpanel dersom siden blir tett?

## Trend

- [ ] Er måned sortert kronologisk?
- [ ] Er nullinjen tydelig?
- [ ] Er actual og forecast visuelt adskilt?
- [ ] Er siste faktiske periode synlig?
- [ ] Er tooltip koblet til trendvisualet?

## Decomposition Tree

- [ ] Bruker Analyze `[Avvik YTD]`?
- [ ] Inneholder Explain by relevante organisasjons- og kontodimensjoner?
- [ ] Er High value forklart som ugunstig positivt kostnadsavvik?
- [ ] Er Low value forklart som gunstig negativt kostnadsavvik?
- [ ] Er visualet stort nok eller tilgjengelig i focus mode?

## AI

- [ ] Er Copilot aktivert og tilgjengelig i riktig kapasitet?
- [ ] Er semantic model forberedt med gode navn og beskrivelser?
- [ ] Er Key Influencers-resultater behandlet som analysehypoteser?
- [ ] Er Q&A-bruk vurdert opp mot avvikling i februar 2027?
- [ ] Har ukjente AI-funksjoner help tooltips?

---

# 31. Anbefalt sluttfortelling

```text
KPI
Hvordan ligger vi an?
        ↓
TREND
Blir avviket bedre eller verre?
        ↓
DECOMPOSITION TREE
Hvor oppstår avviket?
        ↓
KEY INFLUENCERS
Hvilke faktorer kjennetegner avviket?
        ↓
COPILOT / NATURLIG SPRÅK
Hvilke tilleggsspørsmål vil brukeren undersøke?
        ↓
OPPFØLGINGSMATRISE
Hvilke områder krever handling?
```

Dette gir en moderne Power BI-side som kombinerer tradisjonell controlleranalyse med guidet rotårsaksanalyse, tidstrend, naturlig språk og AI-støttede innsikter.

---

# 32. Offisielle Power BI-funksjoner som ligger til grunn

- Decomposition Tree kan analysere ett mål på tvers av flere dimensjoner, støtter fri drillrekkefølge og AI-splits for å finne neste dimensjon etter valgte kriterier.
- Analytics-panelet kan legge trendlinjer, referanselinjer, forecast og anomaly detection på støttede visualer.
- Anomaly detection kan markere uventede topper/fall i tidsserier og tilby forklaringer basert på utvalgte felter.
- Key Influencers analyserer og rangerer faktorer som påvirker et valgt mål og kan vise top segments.
- Narrative visual kan brukes i Custom mode med dynamiske verdier, og Copilot mode krever relevant Copilot-tilgang.
- Copilot i Power BI kan støtte spørsmål om data, sammendrag, rapportoppretting/-redigering og DAX-generering, men har kapasitets-, administrator-, region- og tilgangskrav.
- Q&A-visualet støtter naturlig språk, men Power BI Q&A er varslet avviklet i februar 2027.
