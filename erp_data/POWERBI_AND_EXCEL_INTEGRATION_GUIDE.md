# 📊 Power BI & Excel Data Model & DAX Guide

**Målgruppe:** Frank Ellingsen, Financial Controller & Project Controller  
**Kildekatalog:** [`C:\Users\frank\Desktop\AI_KOM\erp_data\parquet_exports`](file:///C:/Users/frank/Desktop/AI_KOM/erp_data/parquet_exports)  
**Standarder:** Power BI Star Schema Best Practice | DAX Pattern Standard | FAST Standard

---

## 1. Power Query M-Kode for Innlesing av Parquet

Parquet-filene som genereres av `duckdb_controller_views.py` leses inn direkte i Power BI eller Excel Data Model via Power Query:

### A. Innlesing av `Fact_Regnskap`
```powerquery
let
    Source = Parquet.Document(File.Contents("C:\Users\frank\Desktop\AI_KOM\erp_data\parquet_exports\Fact_Regnskap.parquet")),
    ChangedTypes = Table.TransformColumnTypes(Source,{
        {"transaksjon_hash", type text},
        {"funksjon_key", type text},
        {"art_key", type text},
        {"ansvar_key", type text},
        {"dato_key", type text},
        {"belop", type number},
        {"er_akkumulert_ytd", Int64.Type}
    })
in
    ChangedTypes
```

### B. Innlesing av `Fact_Budsjett`
```powerquery
let
    Source = Parquet.Document(File.Contents("C:\Users\frank\Desktop\AI_KOM\erp_data\parquet_exports\Fact_Budsjett.parquet")),
    ChangedTypes = Table.TransformColumnTypes(Source,{
        {"budsjett_hash", type text},
        {"funksjon_key", type text},
        {"art_key", type text},
        {"ansvar_key", type text},
        {"dato_key", type text},
        {"budsjett_belop", type number}
    })
in
    ChangedTypes
```

### C. Innlesing av Dimensjoner (`Dim_Funksjon`, `Dim_Art`)
```powerquery
let
    Source = Parquet.Document(File.Contents("C:\Users\frank\Desktop\AI_KOM\erp_data\parquet_exports\Dim_Funksjon.parquet"))
in
    Source
```

---

## 2. Standardiserte DAX-Måltall (Measures) for Project Controlling

### Kjerne-beregninger (EVM / Avvik):
```dax
// 1. Påløpt Regnskap (Actual Cost - AC)
[Regnskap Faktisk AC] = 
SUM(Fact_Regnskap[belop])

// 2. Periodisert Budsjett (Planned Value - PV)
[Budsjett Planlagt PV] = 
SUM(Fact_Budsjett[budsjett_belop])

// 3. Årsbudsjett (Budget at Completion - BAC)
[Årsbudsjett BAC] = 
CALCULATE(
    SUM(Fact_Budsjett[budsjett_belop]),
    ALL(Dim_Dato[dato_key])
)

// 4. Kostnadsavvik (Cost Variance - CV)
// Positivt tall = Mindreforbruk (besparelse) | Negativt tall = Merforbruk (overskridelse)
[Kostnadsavvik CV] = 
[Budsjett Planlagt PV] - [Regnskap Faktisk AC]

// 5. Avvik i Prosent
[Avvik %] = 
DIVIDE([Kostnadsavvik CV], [Budsjett Planlagt PV], BLANK())

// 6. Kostnadsindeks (Cost Performance Index - CPI)
// Indikerer forbrukseffektivitet: < 1.0 betyr høyere forbruk enn budsjettert fremdrift
[CPI] = 
DIVIDE([Budsjett Planlagt PV], [Regnskap Faktisk AC], 1.0)

// 7. Sluttprognose ved årsslutt (Estimate at Completion - EAC)
[EAC Sluttprognose] = 
DIVIDE([Årsbudsjett BAC], [CPI], [Årsbudsjett BAC])

// 8. Estimert Sluttoverskridelse / Merforbruk ved årsslutt
[Est Sluttoverskridelse] = 
[EAC Sluttprognose] - [Årsbudsjett BAC]

// 9. Gjenstående Forbruk til Fullføring (Estimate to Complete - ETC)
[ETC Gjenstående] = 
[EAC Sluttprognose] - [Regnskap Faktisk AC]
```

---

## 3. Dynamisk Matrise og Hierarkistyring (`ISINSCOPE`)

For å hindre misvisende summeringer på tvers av kontoklasser (Drift vs. Investering jf. Kommuneloven § 14-9):

```dax
Vis_Avvik_Hierarki = 
IF(
    ISINSCOPE(Dim_Art[art_kode]),
    [Kostnadsavvik CV],
    IF(
        ISINSCOPE(Dim_Funksjon[funksjon_kode]),
        [Kostnadsavvik CV],
        BLANK()
    )
)
```

### Dynamisk Formatering:
```dax
Format_Dynamisk_Tall = 
SWITCH(
    TRUE(),
    ISINSCOPE(Dim_Art[art_kode]), "#,##0 kr;[Red](#,##0 kr);\"-\"",
    ISINSCOPE(Dim_Funksjon[tjenesteomrade]), "#,##0.0 'mill. kr';[Red](#,##0.0 'mill. kr');\"-\"",
    "#,##0"
)
```

---

## 4. Row-Level Security (RLS) for Kommunale Enhetsledere

For å sikre at enhetsledere kun ser tall for sitt eget ansvarsområde:

```dax
// Filteruttrykk på tabellen Dim_Ansvar:
[ansvar_kode] = LOOKUPVALUE(
    User_Permissions[ansvar_kode],
    User_Permissions[user_principal_name],
    USERPRINCIPALNAME()
)
```
