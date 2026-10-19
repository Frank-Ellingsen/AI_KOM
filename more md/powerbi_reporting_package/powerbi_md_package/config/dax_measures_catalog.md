# DAX Measures & Conditional Formatting Catalog

Dette dokumentet inneholder alle standardiserte **DAX-måltall** for Power BI Desktop og Power BI Service for Kristiansand kommune.

---

## 1. Kjerne DAX-Måltall

```dax
// 1. Total Budsjett (MNOK)
Total Budsjett = 
SUM('Fact_Regnskap'[Budsjett_MNOK])

// 2. Total Regnskap YTD (MNOK)
Total Regnskap = 
SUM('Fact_Regnskap'[Regnskap_MNOK])

// 3. Avvik i MNOK (Budsjett - Regnskap)
// Viktig: Positiv = Mindreforbruk (Mottatt spar), Negativ = Merforbruk (Underskudd)
Avvik MNOK = 
[Total Budsjett] - [Total Regnskap]

// 4. Avvik i Prosent (%)
Avvik Prosent = 
DIVIDE([Avvik MNOK], [Total Budsjett], 0) * 100

// 5. Overtid & Vikaravvik (Art 1090 + 1100)
Overtid Vikar Forbruk = 
CALCULATE(
    SUM('Fact_Regnskap'[Regnskap_MNOK]),
    'Dim_Art'[Art_Kode] IN {"1090", "1100"}
)

// 6. Uavstemt NAV Sykelønnsrefusjon Gap (Art 1600)
NAV Refusjon Gap = 
VAR ForventetRefusjon = [Overtid Vikar Forbruk] * 0.45
VAR MottattRefusjon = CALCULATE(SUM('Fact_Regnskap'[Regnskap_MNOK]), 'Dim_Art'[Art_Kode] = "1600")
RETURN
ForventetRefusjon - MottattRefusjon
```

---

## 2. Dynamic RAG Status & Conditional Formatting

```dax
// RAG Status KODE
RAG Status Code = 
VAR AvvikPct = [Avvik Prosent]
RETURN
SWITCH(
    TRUE(),
    AvvikPct >= -2.0, "GRØNN",
    AvvikPct >= -5.0, "RAV",
    "RØD"
)

// RAG Hex Color for Conditional Formatting in Power BI Table/KPI Cards
RAG Hex Color = 
VAR Status = [RAG Status Code]
RETURN
SWITCH(
    Status,
    "GRØNN", "#388E3C",  // Kristiansand Grønn
    "RAV",   "#F57C00",  // Kristiansand Rav
    "RØD",   "#D32F2F",  // Kristiansand Rød
    "#002B49"            // Default Kristiansand Navy
)
```

---

## 3. Power BI Slicer Configuration Standards

1. **Slicer 1**: `Dim_Virksomhetsomrade[Virksomhetsomrade_Navn]` (Dropdown / Tiles - Multi Select)
2. **Slicer 2**: `Dim_Ansvar[Enhet_Navn]` (Cascading dropdown filtered by Virksomhetsområde)
3. **Slicer 3**: `Dim_Funksjon[KOSTRA_Funksjon]` (KOSTRA codes 100, 202, 253, 254, 301, 340)
4. **Slicer 4**: `Fact_Regnskap[RAG_Status]` (Single/Multi-select for Rød, Rav, Grønn)
