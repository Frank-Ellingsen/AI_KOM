# Power BI Best Practice Package
## Storytelling with Data, Context, RAG, Tooltips, Forecast, Scenarios, EVM and Audit

Denne pakken samler anbefalingene for de viste rapportfanene til ett felles design- og styringsrammeverk. Målet er at rapporten skal kunne leses som en historie fra **status til handling**, samtidig som controller, leder og analytiker kan gå ned i detaljene.

---

# 1. Overordnet prinsipp

Alle rapportfaner bør støtte den samme logikken:

```text
STATUS
  ↓
KONTEKST / BENCHMARK
  ↓
AVVIK
  ↓
DRIVER / ROOT CAUSE
  ↓
PROGNOSE / SCENARIO
  ↓
TILTAK
  ↓
OPPFØLGING / AUDIT
```

Hvert visual bør svare på ett tydelig spørsmål. Tabellen bør dokumentere detaljene, mens hovedvisualene skal forklare historien.

---

# 2. Felles sidearkitektur

Anbefalt standard for de fleste analysesider:

```text
┌──────────────────────────────────────────────────────────────────────┐
│ SIDETITTEL                                      Sektor ▾ Periode ▾   │
│ Kort undertittel / formål                       Enhet ▾  Flere filtr. │
├──────────────┬──────────────┬──────────────┬─────────────────────────┤
│ KPI 1        │ KPI 2        │ KPI 3        │ KPI 4                   │
│ Actual       │ Benchmark    │ Variance     │ Forecast / driver       │
├──────────────────────────────────────────────────────────────────────┤
│ RAG EXECUTIVE SUMMARY                                               │
│ Dynamisk setning som forteller hva brukeren bør legge merke til.    │
├───────────────────────────────┬──────────────────────────────────────┤
│ 01 | HVA SKJER?              │ 02 | HVORFOR SKJER DET?             │
│ Hovedvisual                   │ Driver / root-cause visual           │
├───────────────────────────────┴──────────────────────────────────────┤
│ 03 | HVA BETYR DET FREMOVER?                                       │
│ Trend / forecast / waterfall / scenario                             │
├──────────────────────────────────────────────────────────────────────┤
│ 04 | HVA MÅ FØLGES OPP?                                            │
│ RAG-sortert detaljmatrise                                           │
└──────────────────────────────────────────────────────────────────────┘
```

---

# 3. Storytelling-regler

## 3.1 Status før detaljer

Første skjermområde skal gi svar på:

- Hva er faktisk nivå?
- Hva var planen/rammen?
- Hva er avviket?
- Hva forventes ved periodeslutt/årsslutt?

## 3.2 Kontekst før vurdering

Et isolert tall er ikke nødvendigvis et styringssignal.

Unngå:

```text
Vikarandel
10,1 %
```

Foretrekk:

```text
VIKARANDEL
10,1 %
Mål: 7,0 %
+3,1 pp over mål
🟠 Krever oppmerksomhet
```

Bruk relevante benchmarks som faktisk finnes i modellen, for eksempel:

- budsjett
- plan
- vedtatt ramme
- mål
- forecast
- forrige periode
- sammenlignbar enhet

## 3.3 Forklaring etter status

Etter at avviket er kjent, skal neste visual forklare avviket:

```text
Hva er avviket?
      ↓
Hvor oppstår det?
      ↓
Hva driver det?
```

## 3.4 Fremoverskuende perspektiv

Ikke stopp ved YTD. Når modellen har forecast eller scenario, bruk det til å besvare:

> Hvis utviklingen fortsetter eller tiltak gjennomføres, hvor ender resultatet?

---

# 4. KPI-standard

Alle KPI-kort bør, når dataene støtter det, følge:

```text
KPI-NAVN
HOVEDVERDI
Benchmark / mål
Avvik absolutt | Avvik %
RAG eller trend ved behov
```

Eksempel:

```text
KOSTNADSAVVIK YTD
-4,6 M
Budsjett: 17,3 M
-26,7 %
🔴 Ugunstig
```

## Unngå

- `[Red](5M kr)` eller andre tekniske formatteringsstrenger i brukergrensesnittet.
- RAG på et rent Actual-tall uten benchmark.
- Fire like kort uten prioritering.

---

# 5. RAG Governance

RAG = Red, Amber, Green.

RAG skal uttrykke styringsstatus, ikke dekorasjon.

## Eksempel på terskler

| Status | Relativt avvik | Tolkning |
|---|---:|---|
| 🟢 Green | >= -2 % | Innenfor toleranse |
| 🟠 Amber | < -2 % og >= -5 % | Krever oppmerksomhet |
| 🔴 Red | < -5 % | Krever tiltak |

Tersklene er designforslag og må erstattes av virksomhetens vedtatte regler.

## Materialitet

På kontonivå bør prosent ses sammen med absolutt beløp.

```text
Høy prosent + uvesentlig kroner = kan være lav prioritet
Moderat prosent + stort kronebeløp = kan være høy prioritet
```

Et produksjonsklart RAG-regelverk bør derfor kunne kombinere:

```text
Relativt avvik
+
Absolutt avvik/materialitet
+
Forecast-status
```

---

# 6. DAX for RAG

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

---

# 7. Separat Actual- og Forecast-RAG

Det er verdifullt å skille nåsituasjonen fra forventet sluttstatus.

```text
Enhet                  YTD      EOY
Kommunal Boenhet       🔴       🔴
Enhet A                🔴       🟠
Enhet B                🟢       🟢
```

Dette gjør det mulig å identifisere:

- vedvarende risiko
- forventet forbedring
- forventet forverring

---

# 8. Executive Summary

Alle styringssider bør ha et kort dynamisk budskap under KPI-raden.

Eksempel:

```text
🔴 Ugunstig utvikling
Avvik YTD er -4,6 M. Kommunal Boenhet står for hoveddelen av avviket,
og forecast indikerer at avviket ikke er fullt ut hentet inn ved årsslutt.
```

Design:

- hvit eller svært lys bakgrunn
- RAG-farget venstre stripe
- 1 overskrift
- maksimalt 2–3 korte setninger
- ingen tekniske DAX/navn

---

# 9. Fargepalett

```text
Canvas                  #F5F6F8
Cards                    #FFFFFF
Primary text             #2B2B2B
Secondary text           #6B6B6B
Primary data blue        #2589E8
Neutral                  #D8DDE3
RAG Green                #3A8F5C
RAG Amber                #E6A23C
RAG Red                  #D64545
```

Bruk RAG selektivt. Ordinære dataserier bør hovedsakelig bruke blått og nøytrale toner.

---

# 10. Tooltip-strategi

Tooltips skal gi kontekst uten å overfylle hovedsiden.

## Standard økonomi-tooltip

```text
ENHET / KONTO
─────────────────
Regnskap YTD
Budsjett YTD
Avvik YTD
Avvik YTD %
RAG YTD

EOY Forecast
EOY Avvik
RAG EOY
```

## Vikar/overtid-tooltip

```text
ENHET
─────────────────
Vikarutgift YTD
Vikarandel
Overtid YTD
Overtidsandel
Benchmark/mål
Avvik mot benchmark
```

## EVM-tooltip

```text
ENHET / PROSJEKT
─────────────────
PV
AC
CV
CPI
Status
Forecast dersom tilgjengelig
```

## Tooltip-regler

- Vis bare relevant kontekst.
- Ikke kopier hele detaljtabellen.
- Unngå scroll.
- Bruk drillthrough dersom brukeren skal interagere med detaljene.
- Bruk hjelp-tooltip til å forklare ukjente KPI-er som CPI, CV eller avanserte scenarioforutsetninger.

---

# 11. Side 1: Økonomisk Status

## Formål

Ledelsesoversikt over YTD-status og EOY-forventning.

## Historie

```text
Regnskap vs budsjett
       ↓
Avvik
       ↓
Hvor oppstår avviket?
       ↓
Hva driver det?
       ↓
Hvor ender vi?
       ↓
Hvem må følges opp?
```

## Anbefalte visualer

1. KPI-rad: Actual, Budget, Variance, EOY.
2. Executive Summary.
3. Diverging bar: avvik per enhet.
4. Top-N: største avviksdrivere.
5. Waterfall: budsjett til forecast.
6. RAG-matrise for oppfølging.

---

# 12. Side 2: Oppvekst og Grunnskole

## Formål

Analysere kostnadsnivå, vikarbruk og kostnad per elev.

## KPI-er

```text
Forbruk YTD
Avvik YTD
Vikarandel
Netto kostnad per elev
```

Hver ratio bør ha en benchmark når dataene støtter det.

## Avviksdrivere

Erstatt brede kontoartsdiagrammer med Top-N-divergerende barer:

```text
Fastlønn              █████████ -x M
Vikar                  █████     -x M
Overtid                ███       -x M
Ekstrahjelp            ██        +x M
```

Detaljene beholdes i kontospesifikasjonen.

## Skolesammenligning

Løft enhetssammenligningen slik at den viser:

```text
Enhet | Avvik % | Vikarandel | Kost/elev | RAG
```

Når datagrunnlaget er egnet kan scatter plot vurderes:

```text
X = vikarandel
Y = kostnad per elev
Size = forbruk
Color = RAG
```

Scatter-visualet bør tolkes som sammenheng, ikke automatisk som årsak.

---

# 13. Side 3: Helse og Mestring

Bildet viser blant annet:

- Forbruk Helse & Mestring
- Overtid & Tillegg
- Overtidsandel i Turnus
- estimert sluttavvik etter tiltak
- avvik per boenhet/lokasjon
- månedlig utvikling døgnvakter
- turnus- og overtidsfordeling

## Anbefalt historie

```text
Hva koster tjenesten?
      ↓
Hvor stort er avviket?
      ↓
Er overtid/turnus en vesentlig driver?
      ↓
Hvilke lokasjoner driver avviket?
      ↓
Hvordan utvikler det seg måned for måned?
      ↓
Hva forventes etter tiltak?
```

## Forbedringer

- Gi overtidsandel et mål/benchmark.
- Vis Top-N lokasjoner med største avvik.
- Bruk månedstrend for overtid/døgnvakt, ikke bare absolutte søyler når trend er hovedspørsmålet.
- Bytt stor kontoliste i hovedflaten mot driveranalyse, og legg detaljene i matrise/drillthrough.

---

# 14. Side 4: Lønn og Vikarmonitor

Bildet viser:

- samlet lønnskostnad YTD
- vikarforbruk
- overtid
- NAV-refusjoner
- månedlig vikarutvikling
- vikarandel per enhet
- detaljert lønns- og refusjonsmatrise

## Anbefalt historie

```text
Total lønn
   ↓
Hvor mye skyldes vikar/overtid?
   ↓
Hvordan utvikler kostnaden seg?
   ↓
Hvilke enheter har høyest andel?
   ↓
Hvilke lønnskontoer/refusjoner forklarer avviket?
```

## KPI-forbedring

NAV-refusjon = 0 bør få kontekst dersom modellen har forventet refusjon eller periodisert krav:

```text
NAV-REFUSJON
0 kr
Forventet: X kr
Avvik: -X kr
RAG dersom styringsregel finnes
```

Ikke marker `0 kr` som problem uten en definert benchmark.

## Trend

Månedlig vikarutvikling bør brukes til å fremheve:

- siste observerte måned
- trendretning
- eventuelt sammenligning mot plan/mål

---

# 15. Side 5: Prognose og Scenario

Bildet viser:

- vedtatt årsramme
- prognose EOY uten tiltak
- tiltaksbesparelse
- simulert EOY-sluttavvik
- What-if lønnsdeflator
- What-if fraværsreduksjon
- forventet årsavvik per enhet
- scenariooversikt
- simulert netto driftsramme ved årsslutt

Dette er en sterk kandidat for rapportens mest beslutningsorienterte side.

## Anbefalt historie

```text
VEDTATT RAMME
     ↓
BASELINE FORECAST UTEN TILTAK
     ↓
TILTAKSEFFEKT
     ↓
WHAT-IF FORUTSETNINGER
     ↓
SIMULERT EOY
     ↓
RESTAVVIK / BESLUTNINGSBEHOV
```

## Waterfall

Anbefalt hovedvisual:

```text
Vedtatt årsramme
       ↓
Baseline forecast gap
       ↓
Tiltaksbesparelse
       ↓
Lønnsdeflator-effekt
       ↓
Fraværsreduksjon
       ↓
Simulert EOY sluttposisjon
```

## Scenario-kort

Vis eksplisitt valgt scenario:

```text
AKTIVT SCENARIO
Lønnsdeflator: 2,3 %
Fraværsreduksjon: 0,8 %
─────────────────
Simulert EOY: 22 M
Restavvik: -4 M
🔴 Tiltaksgap
```

Flytt lange What-if-lister til kompakte kontroller dersom rapportdesignet tillater det.

---

# 16. Side 6: Investering og Capex / EVM

Bildet viser:

- Planlagt verdi (PV)
- Påløpt kostnad (AC)
- Kostnadsavvik (CV = PV - AC)
- Kostnadsindeks (CPI)
- kostnadsavvik per enhet
- visualer med kapasitets-/lisensfeilmelding

## KPI-historie

```text
PV → AC → CV → CPI
```

Disse fire KPI-ene bør leses som én sammenhengende EVM-historie, ikke fire uavhengige kort.

## Kontekst

CPI trenger forklaring/benchmark. Når virksomheten har fastsatte regler, knytt RAG til dem.

Eksempel på presentasjon:

```text
CPI
1,365
Benchmark: 1,00
Status: [virksomhetens RAG-regel]
```

## Feilvisualer

Visualer som viser kapasitets-/lisensfeil bør ikke opptre som tomme produksjonsfelt. Før publisering bør rapporten testes i målmiljøet, og en støttet alternativ visualisering bør brukes dersom den valgte visualtypen ikke kan vises for målgruppen.

---

# 17. Side 7: Revisjon og Audit Trail

Bildet viser:

- verifisert transaksjonssum
- totalavvik gransket
- signerte tiltak
- uforanderlig revisjonslogg `Audit_AI_Actions`
- tidsstempel, enhetskode, AI-tiltak, lederbeslutning, saksbehandler, begrunnelse og SHA256-hash

Denne siden bør behandles annerledes enn økonomisidene. Formålet er sporbarhet og kontroll.

## Anbefalt struktur

```text
KONTROLLSTATUS
────────────────────────
Verifisert beløp | Gransket avvik | Signerte tiltak

FILTER / SØK
────────────────────────
Enhet | Beslutningsstatus | periode

AUDIT LOG
────────────────────────
Tidsstempel
Enhet
AI-forslag
Beslutning
Begrunnelse
Hash / integritetsreferanse
```

## RAG på audit-siden

Bruk RAG bare hvis statusene har eksplisitte kontrollregler. Eksempelvis bør `APPROVED` eller `MODIFIED` ikke automatisk oversettes til grønn/gul/rød uten en definert styringsbetydning.

---

# 18. Tabellenes rolle

Tabeller og matriser er viktige, men bør normalt være siste ledd i historien.

Standard:

```text
Status | Enhet/Konto | Budget | Actual | Variance | Variance % | Forecast
```

## Formatering

- numeriske verdier høyrejusteres
- enheter/kontonavn venstrejusteres
- samme K/M-format på tvers av faner
- RAG i én dedikert kolonne
- ikke fargelegg hele tabellen
- fremhev Total nøytralt
- sorter etter styringsrelevans når det er naturlig

---

# 19. Top-N + drillthrough

På driverdiagrammer bør hovedsiden normalt vise bare de mest relevante elementene.

Eksempel:

```text
Top 5 største avvik
+ Andre
```

Bruk detaljmatrise eller drillthrough for resten.

Dette reduserer:

- lange kategorilister
- vertikale etiketter
- scrollbars
- visuell støy

---

# 20. Drillthrough-struktur

Foreslått hierarki:

```text
Executive
   ↓
Sektor
   ↓
Enhet
   ↓
Driver / konto
   ↓
Transaksjon / audit
```

Mulige drillthrough-sider:

1. Enhetsdetalj
2. Kontodetalj
3. Lønn/vikardetalj
4. Scenarioforklaring
5. Prosjekt/EVM-detalj
6. Audit-detalj

---

# 21. Interaksjonsdesign

Brukeren bør kunne:

1. velge sektor/enhet/periode
2. se at alle relevante KPI-er oppdateres
3. velge et avvik i hovedvisualet
4. se drivervisualet filtreres
5. åpne tooltip for rask kontekst
6. bruke drillthrough for full analyse

Unngå interaksjoner som filtrerer tilfeldige eller irrelevante visualer.

---

# 22. Trend og tid

Når målet er utvikling, skal tid være visuelt tydelig.

For månedsgrafer:

- behold kronologisk rekkefølge
- fremhev siste faktiske periode
- skill fremtid/forecast fra actual dersom begge vises
- vurder referanselinje for mål eller gjennomsnitt når dataene støtter det

Bruk linje når retning og trend er viktigere enn kategori-sammenligning.

---

# 23. Variance-design

Avvik bør presenteres konsistent gjennom rapporten.

```text
Actual
vs
Plan/Budget
=
Variance
```

For controller-rapportering bør brukeren normalt se både:

```text
Variance kr
Variance %
```

Sørg for at fortegnskonvensjonen er konsistent og dokumentert, spesielt der lavere kostnad er gunstig men matematisk avvik kan være negativt eller positivt avhengig av definisjonen.

---

# 24. Gunstig/Ugunstig semantikk

Bestem én forretningsregel for kostnader.

Eksempel på konsept:

```text
GUNSTIG  ←──── 0 ────→  UGUNSTIG
```

Hvis rapportmodellen bruker `PV - AC`, `Budget - Actual` eller `Actual - Budget` på ulike sider, bør brukergrensesnittet likevel presentere korrekt **Gunstig/Ugunstig** semantikk konsekvent.

---

# 25. Tilgjengelighet

RAG må aldri være kun farge.

Bruk:

```text
🔴 Krever tiltak
🟠 Krever oppmerksomhet
🟢 Innenfor toleranse
```

eller symbol + tekst/verdi.

Andre anbefalinger:

- tydelig kontrast
- meningsfulle visualtitler
- alt-tekst på viktige visualer
- logisk tab-/leserekkefølge
- unngå små skrifttyper
- unngå å kommunisere kritisk betydning kun med grønn/rød

---

# 26. Tallformat

Standardiser på tvers av rapporten.

```text
12 641 753 kr → 12,6 M kr på KPI
1 224 900 kr  → 1,2 M kr
18 902 kr     → 18,9 K kr
10.1%         → 10,1 % i norsk presentasjon
```

Bruk fullverdi i tooltip eller detaljtabell når presisjon er nødvendig.

---

# 27. Titler som forteller historien

Svak:

```text
Avvik per ansvar_navn
```

Bedre:

```text
Hvor oppstår avviket?
Avvik YTD per enhet
```

Svak:

```text
Vikarutvikling per Måned
```

Bedre:

```text
Hvordan utvikler vikarforbruket seg?
Vikarutgift per måned
```

Svak:

```text
Kostnadsavvik (CV) per Enhet
```

Bedre:

```text
Hvilke enheter driver kostnadsavviket?
CV per enhet
```

---

# 28. Sidetitler

Foreslått standardisering:

```text
1. Økonomisk Status
2. Oppvekst | Grunnskole
3. Helse & Mestring
4. Lønn & Vikarmonitor
5. Prognose & Scenario
6. Investering & Capex | EVM
7. Revisjon & Audit Trail
```

Legg til en kort formålslinje under hver sidetittel.

---

# 29. Navigasjon

Rapportreisen kan struktureres slik:

```text
OVERSIKT
Økonomisk Status
      ↓
DRIVERANALYSE
Oppvekst / Helse / Lønn
      ↓
FREMTID
Prognose & Scenario
      ↓
PROSJEKTSTYRING
EVM
      ↓
KONTROLL
Audit Trail
```

Dette gir rapportpakken en begynnelse, midtdel og avslutning.

---

# 30. Visuell standard

## Typografi

```text
Page title          20–24 px
Section title       14–16 px
Visual title        12–14 px
KPI value           24–32 px
Secondary text      10–12 px
```

## Spacing

Bruk et konsistent spacing-system:

```text
8 px
16 px
24 px
32 px
```

## Kort

- hvit bakgrunn
- subtil border
- moderat avrunding
- liten eller ingen skygge
- venstrejustert overskrift
- tydelig verdi

---

# 31. Hva rapporten bør unngå

1. Tekniske formatteringsmarkører som `[Red]` i sluttbrukertekst.
2. Scrollbare hoveddiagrammer med svært mange kategorier.
3. Vertikale kategorietiketter når Top-N eller horisontal bar fungerer bedre.
4. KPI-er uten benchmark når KPI-en krever benchmark for å tolkes.
5. Hele visualer eller tabellrader i kraftig RAG-farge.
6. Samme visuelle vekt på alt.
7. Detail-first layout.
8. Uforklarte akronymer som CPI/CV uten tooltip/hjelp.
9. Scenario uten synlige forutsetninger.
10. Feilvisualer i publisert styringsrapport.

---

# 32. QA-sjekkliste før publisering

## Storytelling

- [ ] Kan en leder forstå status på få sekunder?
- [ ] Er benchmark synlig der det trengs?
- [ ] Forklarer neste visual hvorfor KPI-en ser slik ut?
- [ ] Finnes forecast eller fremoverskuende perspektiv der det er relevant?
- [ ] Ender siden med oppfølging eller handling?

## RAG

- [ ] Er tersklene dokumentert?
- [ ] Brukes materialitet der nødvendig?
- [ ] Er Actual og Forecast-status skilt der det gir mening?
- [ ] Betyr rødt det samme på tvers av siden?
- [ ] Finnes symbol/tekst i tillegg til farge?

## Tooltips

- [ ] Har viktige visualer kontekst-tooltip?
- [ ] Viser tooltip benchmark og variance?
- [ ] Er tooltip kort nok til å leses uten scroll?
- [ ] Brukes drillthrough når interaksjon kreves?

## Visualer

- [ ] Er Top-N brukt på lange kategorilister?
- [ ] Er tidsserier kronologiske?
- [ ] Er tallformat konsistent?
- [ ] Er unødvendige gridlines/etiketter fjernet?
- [ ] Er alle visualer testet i målmiljøet?

## Tilgjengelighet

- [ ] Er kontrasten god?
- [ ] Er RAG forståelig uten fargesyn?
- [ ] Er titler beskrivende?
- [ ] Er alt-tekst satt på viktige visualer?
- [ ] Er tab-/leserekkefølge gjennomgått?

---

# 33. Prioritert forbedringsplan

## P1: Gjør først

1. Fjern `[Red]`-tekst og erstatt med ekte conditional formatting.
2. Standardiser KPI-kortene med benchmark + variance + status.
3. Legg Executive Summary på alle primære styringssider.
4. Erstatt brede konto-/kategorigrafer med Top-N driveranalyse.
5. Etabler én RAG-governance-modell.
6. Standardiser norsk tallformat og K/M-enheter.
7. Bytt eller korriger visualer som viser kapasitets-/lisensfeil.

## P2: Neste

8. Bygg standard tooltip-sider.
9. Legg Actual/Forecast-RAG der forecast finnes.
10. Gjør Scenario-siden til en tydelig bridge fra baseline → tiltak → simulert EOY.
11. Løft enhets-/skolesammenligning til et sentralt analysevisual.
12. Etabler drillthrough for enhet, konto og audit.

## P3: Modning

13. Dynamiske narrativer.
14. Materialitetsjustert RAG.
15. Trendindikatorer.
16. Scenario-/forecast-sammenligning på tvers av perioder.
17. Full accessibility QA.
18. Dokumentert visual- og formatteringsstandard for hele rapportpakken.

---

# 34. Endelig styringshistorie for hele rapportpakken

```text
1. ØKONOMISK STATUS
Hvordan ligger vi an?
        ↓

2–4. OPERATIVE DRIVERE
Hvor oppstår avviket og hvorfor?
Oppvekst | Helse | Lønn
        ↓

5. PROGNOSE & SCENARIO
Hvor forventer vi å ende, og hva kan tiltak endre?
        ↓

6. EVM
Hvordan presterer investering/prosjekt mot plan?
        ↓

7. AUDIT TRAIL
Er beslutninger, tiltak og kontrollspor dokumentert?
```

Dette gjør rapporten til mer enn en samling dashboards. Rapporten blir et sammenhengende styringsløp fra **observasjon → diagnose → prognose → beslutning → kontroll**.

---

# 35. Referanser brukt for Power BI-funksjoner

Microsofts dokumentasjon beskriver at visual tooltips gir kontekst ved hover, at ekstra felt kan legges i Tooltip-feltet, og at tooltips kan støtte drillhandlinger der visualet støtter dette.

Microsofts dokumentasjon beskriver også report page tooltips som egne rapportsider for rikere kontekst med visualer og KPI-er. Report page tooltips er ikke interaktive og bør derfor ikke inneholde elementer som brukeren forventes å operere; bruk drillthrough når interaksjon er nødvendig.

Microsofts accessibility-veiledning beskriver blant annet tastaturnavigasjon, skjermleserstøtte, high-contrast-visning og alt-tekst som relevante tilgjengelighetsfunksjoner og hensyn i Power BI-rapporter.
