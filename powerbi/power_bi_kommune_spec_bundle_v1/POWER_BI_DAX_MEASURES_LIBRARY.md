# Power BI DAX Measures Library: Kommunal Økonomistyring

## 1. Basismålinger (Base Measures)
```dax
Regnskap YTD = SUM(Fact_Regnskap[Belop_YTD])

Budsjett YTD = SUM(Fact_Budsjett[Budsjett_Revidert])

Budsjettavvik Kr = [Budsjett YTD] - [Regnskap YTD]

Budsjettavvik % = 
DIVIDE([Budsjettavvik Kr], [Budsjett YTD], 0)
```

## 2. Tidskorrigert & EOY Prognose (Time Intelligence & Forecasting)
```dax
Regnskap Fjorar YTD = 
CALCULATE(
    [Regnskap YTD],
    SAMEPERIODLASTYEAR(Dim_Tid[Dato])
)

EOY_Prognose = 
VAR GjenværendeMaaneder = 12 - MAX(Dim_Tid[Maaned])
VAR SnittMaanedForbruk = DIVIDE([Regnskap YTD], MAX(Dim_Tid[Maaned]), 0)
RETURN
    [Regnskap YTD] + (SnittMaanedForbruk * GjenværendeMaaneder)

EOY_Forventet_Balanse = [Budsjett YTD] - [EOY_Prognose]
```

## 3. Dynamisk Formatering & Hierarchy Scope (ISINSCOPE)
```dax
Dynamisk_Tittel_Nivaa = 
IF(
    ISINSCOPE(Dim_Ansvar[Enhet_Navn]),
    "Detaljnivå: Enhet " & SELECTEDVALUE(Dim_Ansvar[Enhet_Navn]),
    IF(
        ISINSCOPE(Dim_Ansvar[Kommunalsjef_Omraade]),
        "Sektornivå: " & SELECTEDVALUE(Dim_Ansvar[Kommunalsjef_Omraade]),
        "Samlet Kommunenivå"
    )
)
```

## 4. RAG-status & Betinget Formatering (Conditional Formatting)
```dax
Avvik Status Fargekode = 
SWITCH(
    TRUE(),
    [Budsjettavvik %] < -0.05, "#DC2626", // Rød (Merforbruk / overskridelse > 5 %)
    [Budsjettavvik %] < -0.02, "#F59E0B", // Gul/Amber (Moderat merforbruk 2-5 %)
    "#16A34A"                             // Grønn (Mindreforbruk / under ramme)
)
```
