# ⏱️ 60 Ways to Visualize Time — EDA Master Guide for Municipal Project Controllers
## Kristiansand Kommune AI Project Controller Hub
**Basert på**: *Andy Kriebel: 60 Ways to Visualize Time — The Complete List!* (`Time-Visuals.pdf`)  
**Standarder**: Edward Tufte Data-Ink Ratio, Kommuneloven §§ 14-5 & 14-6, FAST Financial Modeling Standard  
**Fagansvarlig**: Senior Controller Frank Ellingsen  

---

## 1. Executive Summary & Controller Formål (EDA)

I kommunal økonomistyring og virksomhetsstyring (EPM) representerer tidsdimensjonen selve nervesystemet i avvikskontrollen. Tradisjonelle kommunale månedsrapporter begrenser seg ofte til statiske tabeller eller enkle linjediagrammer, noe som skjuler:
1. **Underliggende taktskifter og akselerasjon** i vikar- og overtidsforbruk.
2. **Ekte sesongmessighet** vs. enkeltstående periodiseringsfeil eller bilagstopper.
3. **Strukturell glidning** i driftsartene over tid (f.eks. vikarbruk som spiser fastlønnsbudsjettet).
4. **Likviditetsvolatilitet** og dagsspredning i innbetalinger og refusjoner.

Med innlemmelsen av **Andy Kriebels 60 Ways to Visualize Time** i **Visual Sandbox** (`index.html#visual-sandbox`), råder Kristiansand kommune over en helhetlig suite med **96 visualiseringer** (36 Financial Times + 60 Kriebel Time EDA). Samtlige 60 tidsserievisualiseringer er implementert med:
* **Ren Edward Tufte SVG-rendering**: Ingen 3D-effekter, ingen tunge rutenett, direkte merking på linjeender, dempet fargepalett med kontrollerte avviksindikatorer.
* **Fullverdig Power BI DAX-mål**: Skrevet i henhold til beste praksis for tidsintelligens (`DATESYTD`, `DATEADD`, `DATESINPERIOD`, `AVERAGEX`, `RANKX`, `SWITCH`).
* **Sektor-dynamisk styring**: Synkronisert mot kommunens 6 virksomhetsområder og 81 resultatenheter.

---

## 2. De 8 EDA-Tidskategoriene & Kommunale Anvendelser

| Kategori | Visuals | Kjernefunksjon i Prosjekt- & Økonomistyring | Typisk Kommunal Problemstilling |
| :--- | :---: | :--- | :--- |
| **1. Linjer & Trender** | 01–10 | Kontinuerlig vs. diskret forløp, prognoseframskrivning, linjeende-etiketter | Skille faktisk regnskap fra prognose (stiplet) og fjorår (prikket) |
| **2. Arealer & Glatting** | 11–18 | Ressursvolum, 3M glidende snitt, stablede artsfordelinger | Fjerne ferie- og etterbetalingsstøy for å se reell driftstrend |
| **3. Avvik & Vekstrater** | 19–25 | Måned-til-måned Δ, vekstrater fra M1, kumulative S-kurver | Fange plutselige hopp i vikarutgifter og overvåke restbudsjett (BAC) |
| **4. Stolper & Referanser** | 26–33 | Sidestilte søyler, Bar-in-Bar, lollipops, gjennomsnittsreferanse | Kompakt måloppnåelse uten kognitiv overbelastning |
| **5. Multi-Mål & Snitt** | 34–39 | Doble akser, cycle plots over 3 år, daglig kalendermatrise | Avsløre 3-årige sesongsykluser og fakturaopphopning ved forfall |
| **6. Helning & Sommerfugl** | 40–45 | Tertialhelning (T1 vs T2), selvkostbalanse (speil), transaksjonsstrekkode | Dokumentere omstillingseffekt og transaksjonsfrekvens |
| **7. Mikro & Forløp** | 46–51 | Tabell-sparklines, sparkbars, dumbbells, sirkeltidslinjer | Gi 81 enhetsledere en 12-måneders visuell puls i regnskapstabeller |
| **8. Avansert EDA & Volatilitet** | 52–60 | Bump chart (rangskift), seismogram, 2D fasebane, candlesticks | Avdekke likviditetssjokk, relative posisjonsskifter og dagsspredning |

---

## 3. Detaljert Katalog over alle 60 Visuals

### Del 1: Linjer & Trender (01–10)
1. **01. Discrete Line Chart**: Diskrete tertial- eller kvartalsnivåer (T1–T3) forbundet med rette segmenter for å unngå feilaktig interpolering mellom uavhengige bevilgningsperioder.  
   *DAX: `[EDA_01_Discrete_Line_NOK]`*
2. **02. Continuous Line Chart**: Sammenhengende månedskurve for helhetlig driftstrend. Avslører underliggende retningsendringer og stabilitet i drift.  
   *DAX: `[EDA_02_Continuous_Line_NOK]`*
3. **03. Line Chart with Markers**: Markerer hvert månedlige rapporteringstidspunkt for å synliggjøre bokføringsfrekvens og avdekke manglende registreringer.  
   *DAX: `[EDA_03_Line_Markers_NOK]`*
4. **04. Line Chart with Circle Markers**: Tydelige sirkelnoder ved avstemte månedstall (M1–M10) som gjør det lett å kryssjekke mot tertialrapporter.  
   *DAX: `[EDA_04_Circle_Markers_NOK]`*
5. **05. Dashed Line Chart**: Skiller faktisk bokførte måneder (solid linje) fra usikre framtidige prognosemåneder (stiplet linje) jf. god regnskapsskikk.  
   *DAX: `[EDA_05_Dashed_Forecast_NOK]`*
6. **06. Dotted Line Chart**: Fjorårets regnskapsbane som prikket bakgrunnskurve. Isolerer sesongmessig normalitet fra årets merforbruk.  
   *DAX: `[EDA_06_Dotted_PriorYear_NOK]`*
7. **07. Stepped Line Chart**: Trappetrinn som viser at bevilgede rammer forblir konstante inntil Bystyret vedtar formell omdisponering jf. Kommuneloven § 14-5.  
   *DAX: `[EDA_07_Stepped_BudgetCap_NOK]`*
8. **08. Line Chart Multiple Dimensions**: Sammenligner alle 6 sektorer i samme diagram for å identifisere hvilke områder som divergerer fra vedtatt ramme.  
   *DAX: `[EDA_08_MultiDim_Line_NOK]`*
9. **09. Line Chart Multiple Measures**: Faktisk, Budsjett og EAC prognose i samme visning; gir umiddelbar oversikt over avvikssituasjonen.  
   *DAX: `[EDA_09_MultiMeasure_Actual]`, `[EDA_09_MultiMeasure_Budget]`, `[EDA_09_MultiMeasure_EAC]`*
10. **10. Line Chart Ends of Line Labels**: Tufte-standard som plasserer sluttverdi og kurvenavn direkte ved kurvens sluttpunkt for å eliminere separat tegnforklaring.  
    *DAX: `[EDA_10_EndLabel_Val]`*

### Del 2: Arealer & Glatting (11–18)
11. **11. Moving Average**: Glidende 3-måneders snitt som demper månedlig støy fra feriepenger og sesongtopper.  
    *DAX: `[EDA_11_MovingAvg_3M_NOK]`*
12. **12. Area Chart**: Viser det samlede månedlige ressursvolumet som flyter gjennom kommunekassen over året.  
    *DAX: `[EDA_12_Area_Volume_NOK]`*
13. **13. Area Chart + Line Chart**: Lyst areal for periodisert budsjettramme overlagt med solid mørk linje for faktisk forbruk.  
    *DAX: `[EDA_13_Area_Budget_Base]`, `[EDA_13_Line_Actual]`*
14. **14. Area Chart + Dashed Line**: Faktisk forbruksareal med stiplet grenseverdi for maksimalt tillatt overskridelse.  
    *DAX: `[EDA_14_Area_Actual]`, `[EDA_14_Dashed_Ceiling_Limit]`*
15. **15. Area Chart + Dotted Line**: Årets forbruk som fylt areal sammenholdt med fjorårets referansekurve.  
    *DAX: `[EDA_15_Area_Actual]`, `[EDA_15_Dotted_PY_Line]`*
16. **16. Stacked Area Chart**: Viser samlet kostnadsvekst og hvordan lønn, vikarer og drift bygger opp den månedlige totalen.  
    *DAX: `[EDA_16_Stacked_Area_Art]`*
17. **17. % of Total Area Chart**: Normaliserer månedene til 100 % for å avdekke strukturell forskyvning i kostnadsmiksen.  
    *DAX: `[EDA_17_Pct_Total_Area]`*
18. **18. Line Chart + Moving Avg**: Kombinerer månedlige rådata (lys kurve) med glattet 3-måneders retningskurve (mørk linje).  
    *DAX: `[EDA_18_Line_Actual_Raw]`, `[EDA_18_MovingAvg_Trend]`*

### Del 3: Avvik & Vekstrater (19–25)
19. **19. Difference from Previous**: Måned-for-måned nominell differanse (MoM Δ) for å fange brå kostnadshopp.  
    *DAX: `[EDA_19_Diff_From_Previous_MoM]`*
20. **20. % Difference from Previous**: Månedlig vekstrate i prosent som måler om forbruket akselererer eller bremser opp.  
    *DAX: `[EDA_20_Pct_Diff_From_Previous]`*
21. **21. Difference vs. First**: Spacing mot grunnperiode M1 som dokumenterer akkumulert kostnadsdrift siden årets start.  
    *DAX: `[EDA_21_Diff_Vs_First]`*
22. **22. % Difference vs. First**: Indeksert vekst med M1 som 0 % basis for å sammenligne enheters vekstrater uavhengig av rammevolum.  
    *DAX: `[EDA_22_Pct_Diff_Vs_First]`*
23. **23. Running Total**: Akkumulert YTD-kostnadskurve som viser gjenstående budsjettrom fram mot årsslutt.  
    *DAX: `[EDA_23_Running_Total_YTD]`*
24. **24. Running Total Area Chart**: Fylt kumulativ S-kurve for prosjektcontrolling; synliggjør perioden der ressursforbruket var mest intensivt.  
    *DAX: `[EDA_24_Running_Total_Area]`*
25. **25. Running Total from 1st Sale**: For flerårige investeringsprosjekter jf. § 14-9 der framdrift måles fra oppstart uavhengig av årsskifte.  
    *DAX: `[EDA_25_Running_Total_From_Start]`*

### Del 4: Stolper, Søyler & Referanser (26–33)
26. **26. Bar Chart**: Horisontale stolper som gir optimal lesbarhet for månedsetiketter og enhetskoder uten skråstilt tekst.  
    *DAX: `[EDA_26_Horizontal_Bar_NOK]`*
27. **27. Stacked Bar Chart**: Dekomponerer hver måneds utgifter i lønn og drift horisontalt.  
    *DAX: `[EDA_27_Stacked_Bar_Art_NOK]`*
28. **28. % of Total Stacked Bars**: 100 % normaliserte stolper som viser hvordan kostnadsandelene forskyver seg over året.  
    *DAX: `[EDA_28_Pct_Stacked_Bars]`*
29. **29. Paired Column Chart**: Faktisk vs. Periodisert budsjett side-om-side per måned for umiddelbar visuell avstemming.  
    *DAX: `[EDA_29_Paired_Actual]`, `[EDA_29_Paired_Budget]`*
30. **30. Column Chart**: Klassisk månedssøyleoversikt over årets regnskapsforløp med tallverdier direkte på søylene.  
    *DAX: `[EDA_30_Monthly_Column_NOK]`*
31. **31. Lollipop Chart**: Tynn linje med sirkel på toppen; minimerer blekkmengden og leder blikket presist til måleverdien.  
    *DAX: `[EDA_31_Lollipop_Value_NOK]`*
32. **32. Bar-in-Bar Chart**: Smal faktisk søyle inni en bredere budsjettsøyle; kompakt måloppnåelse uten behov for to diagrammer.  
    *DAX: `[EDA_32_BarInBar_Actual]`, `[EDA_32_BarInBar_Budget]`*
33. **33. Bar Chart w/ Reference Line**: Månedssøyler med horisontal gjennomsnittsreferanse for å vise hvilke måneder som avviker fra normalen.  
    *DAX: `[EDA_33_RefLine_Target]`*

### Del 5: Multi-Mål & Avvik mot Snitt (34–39)
34. **34. Dual Axis w/ Different Measures**: Forbruk i Mkr på venstre akse mot sykefravær i % på høyre akse for å avdekke samvariasjon.  
    *DAX: `[EDA_34_DualAxis_Spend_MNOK]`, `[EDA_34_DualAxis_Frav_Pct]`*
35. **35. Dual Axis w/ Related Measures**: Brutto utgifter og inntekter på felles synkronisert skala jf. bruttoprinsippet § 14-6.  
    *DAX: `[EDA_35_DualAxis_Expenses]`, `[EDA_35_DualAxis_Revenues]`*
36. **36. Variance to Overall Average**: Hver måneds differanse fra årets gjennomsnittlige månedsforbruk; isolerer toppene.  
    *DAX: `[EDA_36_Variance_To_Overall_Avg]`*
37. **37. Variance to Pane Average**: Avvik fra tertialets lokale gjennomsnitt; avslører om merforbruk oppsto brått i en delperiode.  
    *DAX: `[EDA_37_Variance_To_Pane_Avg]`*
38. **38. Cycle Plot**: Sammenligner alle januarmåneder, februarmåneder osv. over 3 regnskapsår for å skille sann sesong fra tilfeldigheter.  
    *DAX: `[EDA_38_Cycle_Plot_Seasonal_Mean]`*
39. **39. Single Month Calendar**: Dag 1–31 i kalenderrutenett; avslører ukedagsmønstre, helgetillegg og fakturahoper ved månedsslutt.  
    *DAX: `[EDA_39_Daily_Spend_Intensity]`*

### Del 6: Helning, Sommerfugl & Milepæler (40–45)
40. **40. Discrete Slope Graph**: Sammenligner sektorenes kostnadsnivå mellom T1 og T2 med rette linjer for å vise endringshastighet.  
    *DAX: `[EDA_40_Slope_Start]`, `[EDA_40_Slope_End]`*
41. **41. Continuous Slope Graph**: Flertrinns helningsgraf over påfølgende tertialer (T1 -> T2 -> T3) for å identifisere akselerasjon.  
    *DAX: `[EDA_41_Continuous_Slope]`*
42. **42. Butterfly Chart Single Axis**: Speilvendte stolper på felles nullakse: Utgifter til venstre, inntekter til høyre for selvkostområder.  
    *DAX: `[EDA_42_Butterfly_Expense]`, `[EDA_42_Butterfly_Revenue]`*
43. **43. Butterfly Chart Dual Axis**: Speilvendte stolper med uavhengige enheter: Vikarforbruk i kr vs overtidstimer i antall.  
    *DAX: `[EDA_43_Butterfly_Vikar_NOK]`, `[EDA_43_Butterfly_Overtid_Timer]`*
44. **44. Dot Plot**: Punkter plassert langs en tidslinje for å markere store investeringsutbetalinger eller formelle vedtaksdatoer.  
    *DAX: `[EDA_44_Milestone_Event_NOK]`*
45. **45. Barcode Chart**: Tette vertikale linjer der linjetettheten gjenspeiler fakturafrekvens og periodiseringspropper.  
    *DAX: `[EDA_45_Barcode_Tx_Density]`*

### Del 7: Mikro-Visuals & Forløp (46–51)
46. **46. Sparklines**: Aksefrie miniatyrkurver designet for tabeller; gir 81 enhetsledere en umiddelbar 12-måneders visuell puls.  
    *DAX: `[EDA_46_Sparkline_Monthly]`*
47. **47. Sparkbars**: Miniatyrsøyler for rask avlesning av månedlige topper og bunner direkte i enhetstabeller.  
    *DAX: `[EDA_47_Sparkbar_Monthly]`*
48. **48. Spark Area Chart**: Kompakt fylt miniatyrareal for visning av kumulativ ressursbruk i konsernnotater.  
    *DAX: `[EDA_48_SparkArea_Monthly]`*
49. **49. Connected Dot Plot**: Viser spennet fra M1 til M10 for hver sektor med direkte forbindelsesstrek mellom punktene.  
    *DAX: `[EDA_49_Dumbbell_Start]`, `[EDA_49_Dumbbell_End]`*
50. **50. Enclosed Dot Plot**: Månedlige punkter omgitt av et statistisk toleransebånd (±1 standardavvik) for normalvariasjon.  
    *DAX: `[EDA_50_Enclosed_Center]`, `[EDA_50_Enclosed_Band]`*
51. **51. Circle Timeline**: Sirkler skalert proporsjonalt med budsjettavvikets størrelse plassert langs tidslinjen.  
    *DAX: `[EDA_51_Circle_Timeline_Radius]`*

### Del 8: Avansert EDA & Volatilitet (52–60)
52. **52. Bump Chart**: Viser hvordan de 6 sektorenes rangering etter merforbruk endrer seg fra M1 til M10.  
    *DAX: `[EDA_52_Bump_Sector_Rank]`*
53. **53. Seismogram**: Høyfrekvente svingninger rundt null; fanger likviditetsbølger, skattetrekk og store momsoppgjør.  
    *DAX: `[EDA_53_Seismogram_Daily_Shock]`*
54. **54. Parallel Coordinates**: Sporer enheters nøkkeltall over 2024, 2025 og 2026 på parallelle akser for å vurdere omstilling.  
    *DAX: `[EDA_54_Parallel_Metric_Yr]`*
55. **55. Small Multiple Donut Charts**: En serie smultringer for Q1–Q4 som viser hvordan fordelingen mellom lønn og drift gradvis roterer.  
    *DAX: `[EDA_55_Donut_Art_Share]`*
56. **56. Connected Scatterplot**: Plott av Vikarer (X) mot Overtid (Y) forbundet kronologisk for å spore faseforskyvning.  
    *DAX: `[EDA_56_Scatter_X_Vikar]`, `[EDA_56_Scatter_Y_Overtid]`*
57. **57. Connected Scatterplot Dotted Lines**: Samme som 56, men med stiplet kurve for framskrevne forventede måneder M11–M12.  
    *DAX: `[EDA_57_Scatter_Future_Track]`*
58. **58. Animated Connected Scatterplot**: Trinnvis tidsnavigasjon som lar controlleren trykke seg måned for måned gjennom samvariasjonsstien.  
    *DAX: `[EDA_58_Animation_Frame]`*
59. **59. Waterfall Chart**: Viser månedlige netto kontantstrømmer som bygger fra inngående kassebeholdning til utgående saldo.  
    *DAX: `[EDA_59_Waterfall_Monthly_Flow]`*
60. **60. Stock Chart (High-Low-Close)**: Minste dagsforbruk, høyeste dagsforbruk og saldo ved månedsslutt; overvåker likviditetsrisiko.  
    *DAX: `[EDA_60_Stock_High]`, `[EDA_60_Stock_Low]`, `[EDA_60_Stock_Close]`*

---

## 4. Relevante Lovhjemler & Styringsstandarder

1. **Kommuneloven § 14-5 (Balansekrav)**: Hvis et avviksdiagram (f.eks. *05 Dashed Line*, *07 Stepped Line* eller *23 Running Total*) indikerer at årsavviket blir negativt ($VAC < 0$), plikter Kommunedirektøren å fremme formell sak om budsjettjustering til Bystyret.
2. **Kommuneloven § 14-6 (Bruttoprinsippet)**: Diagrammer som *35 Dual Axis (Related)* og *42 Butterfly Chart* tvinger fram separat visning av utgifter og inntekter uten ulovlig motregning.
3. **Kommuneloven § 14-9 (Investeringsregnskap)**: Diagrammer som *25 Running Total from Start* og *44 Dot Plot (Milepæler)* støtter flerårige prosjekter som strekker seg over flere bevilgningsår.
4. **Hovedtariffavtalen (HTA) § 4 & AML § 10-12**: Korrelasjonsdiagrammer som *34 Dual Axis*, *43 Butterfly Dual Axis* og *56 Connected Scatterplot* dokumenterer sammenhengen mellom høyt sykefravær, overtid og vikarbruk før drøftingsmøter med tillitsvalgte.

---

## 5. Tilgang og Bruk

* **Visual Sandbox (Web Hub)**: Åpne `index.html#visual-sandbox`. Velg Master Suite: **Andy Kriebel: 60 Ways to Visualize Time (EDA)**. Bruk søkefeltet eller kategori-knappene til å filtrere diagrammene. Trykk **📊 DAX** for å se og kopiere formelen, eller **📋 SVG** for å eksportere ren vektorgrafikk til presentasjoner.
* **Master DAX-fil**: `powerbi/09_Andy_Kriebel_60_Time_Visuals_EDA_Measures.dax`.
* **Streamlit Portal**: `streamlit run app/frontend.py` (Fane 3: *FT Visuals & 60 Time Visuals EDA Suite*).
