# Full DAX-Pakke for KOSTRA & Kommunal Økonomistyring
## Kristiansand Kommune — Enterprise Power BI Model & DAX Measure Library

Dette dokumentet inneholder en komplett, produksjonsklar DAX-pakke (Data Analysis Expressions) skreddersydd for kommunal økonomistyring, KOSTRA-rapportering, rullerende EOY-prognoser, matrisestyring med `ISINSCOPE` og visuelle avviksflagg i Power BI.

---

## 1. Grunnleggende Regnskaps- og Budsjettmåltall (Base Measures)

Disse måltallene danner fundamentet for alle videre kalkulasjoner i stjerne-skjemaet (`Fact_Regnskap` koblet mot `Dim_KOSTRA_Kontoplan`, `Dim_Ansvar` og `Dim_Dato`).

```dax
// -----------------------------------------------------------------------------
// 1.1 Regnskap YTD (Påløpt Regnskap)
// -----------------------------------------------------------------------------
Regnskap YTD = 
CALCULATE(
    SUM(Fact_Regnskap[korrigert_belop]),
    KEEPFILTERS(Fact_Regnskap[kontoklasse_id] = 1) -- 1 = Driftsregnskap
)

// -----------------------------------------------------------------------------
// 1.2 Budsjett YTD (Periodisert Årsbudsjett)
// -----------------------------------------------------------------------------
Budsjett YTD = 
CALCULATE(
    SUM(Fact_Regnskap[budsjett_belop]),
    KEEPFILTERS(Fact_Regnskap[kontoklasse_id] = 1)
)

// -----------------------------------------------------------------------------
// 1.3 Avvik YTD i Kroner
// Positivt tall = Merforbruk (Ugunstig for utgifter, gunstig for inntekter)
// -----------------------------------------------------------------------------
Avvik YTD = 
[Regnskap YTD] - [Budsjett YTD]

// -----------------------------------------------------------------------------
// 1.4 Avvik YTD i Prosent
// -----------------------------------------------------------------------------
Avvik YTD % = 
DIVIDE(
    [Avvik YTD],
    ABS([Budsjett YTD]),
    0
)
```

---

## 2. Lovpålagte KOSTRA-Nøkkeltall (Statutory KPIs)

I tråd med Kommuneloven § 14-9 og SSB KOSTRA-standarder beregner disse måltallene de sentrale finansielle nøkkeltallene for Kristiansand kommune.

```dax
// -----------------------------------------------------------------------------
// 2.1 Brutto Driftsresultat i Kroner
// Formel: Brutto Driftsinntekter (Art 6000-8900) - Brutto Driftsutgifter (Art 0000-5900)
// -----------------------------------------------------------------------------
Brutto Driftsresultat = 
VAR Driftsinntekter = 
    CALCULATE(
        [Regnskap YTD],
        Dim_KOSTRA_Kontoplan[Niva_1_Kode] = "Serie 6-8 Inntekter"
    )
VAR Driftsutgifter = 
    CALCULATE(
        [Regnskap YTD],
        Dim_KOSTRA_Kontoplan[Niva_1_Kode] IN {"Serie 0-1 Lønn", "Serie 2 Kjøp av varer/tjenester", "Serie 3/4 Overføringer"}
    )
RETURN
    Driftsinntekter - Driftsutgifter

// -----------------------------------------------------------------------------
// 2.2 Brutto Driftsresultat i % av Brutto Driftsinntekter
// Handlingsregel Kristiansand kommune: Mål om minimum 1,7 % over tid
// -----------------------------------------------------------------------------
Brutto Driftsresultat % = 
VAR TotaleInntekter = 
    CALCULATE(
        [Regnskap YTD],
        Dim_KOSTRA_Kontoplan[Niva_1_Kode] = "Serie 6-8 Inntekter"
    )
RETURN
    DIVIDE([Brutto Driftsresultat], ABS(TotaleInntekter), 0)

// -----------------------------------------------------------------------------
// 2.3 Korrigert Netto Driftsresultat
// Formel: Netto Driftsresultat korrigert for bruk/avsetning bundne fond
// Ref: 1. tertialrapport 2026 Kristiansand kommune (Mål: >= 1,0 %)
// -----------------------------------------------------------------------------
Korrigert Netto Driftsresultat = 
VAR BruttoRes = [Brutto Driftsresultat]
VAR FinansPoster = 
    CALCULATE(
        [Regnskap YTD],
        Dim_KOSTRA_Kontoplan[Niva_2_Kode] IN {"50 Renter/Avdrag", "90 Renteinntekter/Utbytte"}
    )
VAR Fondstrakninger = 
    CALCULATE(
        [Regnskap YTD],
        Dim_KOSTRA_Kontoplan[Niva_2_Kode] IN {"55 Avsetninger", "95 Bruk av fond"}
    )
RETURN
    BruttoRes + FinansPoster + Fondstrakninger

Korrigert Netto Driftsresultat % = 
VAR TotaleInntekter = 
    CALCULATE(
        [Regnskap YTD],
        Dim_KOSTRA_Kontoplan[Niva_1_Kode] = "Serie 6-8 Inntekter"
    )
RETURN
    DIVIDE([Korrigert Netto Driftsresultat], ABS(TotaleInntekter), 0)

// -----------------------------------------------------------------------------
// 2.4 Disposisjonsfond i % av Brutto Driftsinntekter (Bufferkapital)
// -----------------------------------------------------------------------------
Disposisjonsfond Grad % = 
VAR DisposisjonsfondSaldo = 
    CALCULATE(
        SUM(Fact_Regnskap[korrigert_belop]),
        Fact_Regnskap[kontoklasse_id] = 3, -- Balanse
        Dim_KOSTRA_Kontoplan[Niva_3_Kode] = "2.80 Disposisjonsfond"
    )
VAR TotaleInntekter = 
    CALCULATE(
        [Regnskap YTD],
        Dim_KOSTRA_Kontoplan[Niva_1_Kode] = "Serie 6-8 Inntekter"
    )
RETURN
    DIVIDE(ABS(DisposisjonsfondSaldo), ABS(TotaleInntekter), 0)
```

---

## 3. Time Intelligence & Rullerende EOY-Prognoser (Predictive DAX)

Denne modulen leverer sammenligning mot fjorår (YoY) samt en dynamisk, rullerende **End-of-Year (EOY) årsprognose** som oppdager avvik 60–90 dager før de offisielle tertialrapportene.

```dax
// -----------------------------------------------------------------------------
// 3.1 Fjorår Samme Periode (Prior Year YTD)
// -----------------------------------------------------------------------------
Regnskap PY YTD = 
CALCULATE(
    [Regnskap YTD],
    SAMEPERIODLASTYEAR(Dim_Dato[full_dato])
)

// -----------------------------------------------------------------------------
// 3.2 Endring mot Fjorår (YoY Endring i Kr og %)
// -----------------------------------------------------------------------------
Endring YoY Kr = [Regnskap YTD] - [Regnskap PY YTD]

Endring YoY % = DIVIDE([Endring YoY Kr], ABS([Regnskap PY YTD]), 0)

// -----------------------------------------------------------------------------
// 3.3 Dynamic Rolling EOY Forecast (End-of-Year Årsprognose)
// Kombinerer registrert regnskap hittil i år med gjenstående periodisert budsjett
// -----------------------------------------------------------------------------
EOY Årsprognose = 
VAR SisteRegistrerteDato = MAX(Fact_Regnskap[sist_oppdatert])
VAR PåløptRegnskap = [Regnskap YTD]
VAR GjenståendeBudsjett = 
    CALCULATE(
        [Budsjett YTD],
        DATESBETWEEN(
            Dim_Dato[full_dato],
            NEXTDAY(SisteRegistrerteDato),
            ENDOFYEAR(Dim_Dato[full_dato])
        )
    )
RETURN
    IF(
        ISBLANK(PåløptRegnskap),
        BLANK(),
        PåløptRegnskap + GjenståendeBudsjett
    )

// -----------------------------------------------------------------------------
// 3.4 EOY Avvik mot Opprinnelig Årsbudsjett
// -----------------------------------------------------------------------------
EOY Projisert Avvik = 
VAR VedtattAarsbudsjett = 
    CALCULATE(
        [Budsjett YTD],
        ALL(Dim_Dato[tertial]),
        ALL(Dim_Dato[maned])
    )
RETURN
    [EOY Årsprognose] - VedtattAarsbudsjett
```

---

## 4. Matrisestyring & Dynamisk Drill-Down (`ISINSCOPE`)

Ved stram rapportering i Power BI Matrix Visuals sikrer `ISINSCOPE` at måltallene formateres og beregnes riktig avhengig av om brukeren ser på **Tjenesteområde**, **Virksomhet**, **KOSTRA-funksjon** eller **Art**.

```dax
// -----------------------------------------------------------------------------
// 4.1 Hierarkisk Tittel- og Kontekstdetektor
// -----------------------------------------------------------------------------
Aktiv Hierarki Kontekst = 
SWITCH(
    TRUE(),
    ISINSCOPE(Dim_KOSTRA_Kontoplan[Niva_3_Navn]), "Detaljert Konto / Art",
    ISINSCOPE(Dim_KOSTRA_Kontoplan[Niva_2_Navn]), "KOSTRA Funksjon",
    ISINSCOPE(Dim_KOSTRA_Kontoplan[Niva_1_Navn]), "Hovedfunksjon / Sektor",
    "Kommunenivå (Totalt)"
)

// -----------------------------------------------------------------------------
// 4.2 Dynamisk Smart Avviksvisning (Gjelder både Saldo og Prosent)
// -----------------------------------------------------------------------------
Smart Avviksvisning = 
IF(
    ISINSCOPE(Dim_KOSTRA_Kontoplan[Niva_3_Navn]),
    -- På laveste nivå: Vis eksakt kronesum
    FORMAT([Avvik YTD], "#,##0 kr;(#,##0 kr);"-""),
    -- På høyere nivåer: Vis både kroneavvik og prosentavvik
    FORMAT([Avvik YTD], "#,##0 kr;(#,##0 kr);"-"") & " (" & FORMAT([Avvik YTD %], "0.0 %") & ")"
)

// -----------------------------------------------------------------------------
// 4.3 Visuelt Avviksflagg for Conditional Formatting (Fargekoding)
// Returnerer fargekode for fyll eller ikon i Power BI-matrisen
// -----------------------------------------------------------------------------
Avvik Status Farge = 
VAR AvvikPct = [Avvik YTD %]
VAR VesentlighetsGrense = 0.05 -- 5 % terskel jf. Økonomireglementet
RETURN
    SWITCH(
        TRUE(),
        AvvikPct > VesentlighetsGrense, "#D9534F", -- Rød (Alvorlig merforbruk)
        AvvikPct > 0.02, "#F0AD4E",                 -- Gul (Moderat merforbruk)
        AvvikPct < -VesentlighetsGrense, "#337AB7", -- Blå (Mindreforbruk)
        "#5CB85C"                                   -- Grønn (I henhold til budsjett)
    )
```

---

## 5. Dynamiske Formatstrenger (Dynamic Format Strings)

Med Power BIs *Dynamic Format Strings* eller *Calculation Groups* kan enkeltmåltall skifte format dynamisk basert på valgt måleenhet uten å opprette separate måltall.

```dax
// -----------------------------------------------------------------------------
// Dynamic Format String for [Valgt KPI]
// -----------------------------------------------------------------------------
IF(
    SELECTEDVALUE(Dim_Måleenhet[EnhetsType]) = "Prosent",
    "0.0 %",
    "#,##0 kr;(#,##0 kr);"-""
)
```

---

## 6. Organizational Hierarchy Row-Level Security (RLS)

Sikrer at enhetsledere (f.eks. for *Kommunal Skole* eller *Kommunal Boenhet*) kun ser sine egne KOSTRA-ansvarssteder, mens kommunalsjefer og økonomidirektør ser hele sektoren.

```dax
// -----------------------------------------------------------------------------
// RLS Filter på Dim_Ansvar for Enhetsleder (Azure AD / Entra ID UPN Lookup)
// -----------------------------------------------------------------------------
[Leder_Epost] = USERPRINCIPALNAME()
||
LOOKUPVALUE(
    Dim_Ansvar[Sektorsjef_Epost],
    Dim_Ansvar[Sektorsjef_Epost], USERPRINCIPALNAME()
) = USERPRINCIPALNAME()
```

---

## 7. Handlingsregler & Vesentlighetsgrenser i Kristiansand Kommune

| Nøkkeltall / KPI | Måltall / Grenseverdi | Hjemmel / Forankring | DAX Måltall |
| :--- | :--- | :--- | :--- |
| **Korrigert Netto Driftsresultat** | **>= 1,0 %** | Bystyrets handlingsregel | `[Korrigert Netto Driftsresultat %]` |
| **Disposisjonsfond** | **>= 5,0 %** | Buffer mot uforutsette hendelser | `[Disposisjonsfond Grad %]` |
| **Lånegjeld / Gjeldstak** | **Max 8,8 mrd. kr** | Bystyrevedtak HØP 2026–2029 | `[Nettogjeld Sum]` |
| **Avviksrapportering** | **> 5,0 % eller 500' kr** | Økonomireglementet § 4 | `[Avvik Status Farge]` |

---
*Generert for Kristiansand kommune EPM Framework — Versjon 1.0 (2026)*
