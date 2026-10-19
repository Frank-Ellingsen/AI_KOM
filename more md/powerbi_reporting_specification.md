# Power BI Reporting Specification & DAX Architecture — Kristiansand Kommune

An enterprise reporting architecture for Kristiansand kommune's financial controlling hub, covering all **6 Virksomhetsområder (Kommunalområder)** and **81 Enheter (Ansvarssteder)** across the 7.24 BNOK municipal budget.

---

## 1. Executive Summary & Organizational Scope

This specification defines a Power BI Desktop and Service reporting framework connected to **Visma Enterprise ERP**, **Framsikt EPM**, and **SSB KOSTRA** data sources via DuckDB/Parquet golden record pipelines.

### Organizational Structure
1. **Oppvekst** (18 Enheter / Ansvarsområde 2000–2999) — KOSTRA Functions 201, 202, 211, 220, 231
2. **Helse og mestring** (22 Enheter / Ansvarsområde 5000–5999) — KOSTRA Functions 253, 254, 256, 261, 273
3. **Stedsutvikling** (12 Enheter / Ansvarsområde 3000–3999) — KOSTRA Functions 301, 302, 303, 310
4. **Kultur og innbyggerdialog** (10 Enheter / Ansvarsområde 4000–4999) — KOSTRA Functions 332, 333, 338, 345
5. **Infrastruktur og miljø** (11 Enheter / Ansvarsområde 6000–6999) — KOSTRA Functions 340, 345, 353, 360
6. **Organisasjon og styring** (8 Enheter / Ansvarsområde 1000–1999) — KOSTRA Functions 100, 120, 130, 180

**Total Scope**: 81 Ansvarssteder, ~7.24 BNOK Annual Operating Budget.

---

## 2. Interactive Power BI Slicer & Filter Hierarchy

To enable rapid drill-down for controllers and unit leaders (*Enhetsledere*), every report page implements a standardized 4-tier slicer panel:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ POWER BI SIDEBAR SLICER PANEL                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Virksomhetsområde Slicer (Multiselect across all 6 Sektorer)             │
│ 2. Enhet / Ansvarssted Slicer (Cascading dropdown filtered by Sektor — 81) │
│ 3. KOSTRA Funksjon Slicer (Select by KOSTRA code: 202, 254, 301, etc.)      │
│ 4. RAG-Status Slicer (Filter by 🔴 Rød, 🟠 Rav, 🟢 Grønn)                   │
│ 5. Text Search (Wildcard search on Enhet_Navn and Ansvar number)             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Canonical Power BI DAX Measure Catalog

The following DAX measures enforce financial directional standards (*Budsjett - Regnskap*) and dynamic Red-Amber-Green (RAG) conditional formatting.

```dax
-- ===================================================
-- 1. CORE AGGREGATION MEASURES
-- ===================================================

[Total Budsjett MNOK] = 
SUM(Fact_Regnskap[Budsjett_MNOK])

[Total Regnskap MNOK] = 
SUM(Fact_Regnskap[Regnskap_MNOK])

-- ===================================================
-- 2. DIRECTIONAL VARIANCE MEASURES
-- Rule: Positive = Savings / Less spend; Negative = Overrun / Deficit
-- ===================================================

[Avvik MNOK] = 
[Total Budsjett MNOK] - [Total Regnskap MNOK]

[Avvik Pct] = 
DIVIDE([Avvik MNOK], [Total Budsjett MNOK], 0) * 100

-- ===================================================
-- 3. RAG STATUS & COLOR DAX MEASURES
-- ===================================================

[RAG Status Code] = 
SWITCH(
    TRUE(),
    [Avvik Pct] >= -2.0, "GRØNN",
    [Avvik Pct] >= -5.0, "RAV",
    "RØD"
)

[RAG Status Label] = 
SWITCH(
    [RAG Status Code],
    "GRØNN", "🟢 Grønn (I Balanse)",
    "RAV", "🟠 Rav (Moderat Avvik)",
    "RØD", "🔴 Rød (Kritisk Merforbruk)",
    "⚪ Udefinert"
)

[RAG Hex Color] = 
SWITCH(
    [RAG Status Code],
    "GRØNN", "#388E3C",
    "RAV", "#F57C00",
    "RØD", "#D32F2F",
    "#002B49"
)

-- ===================================================
-- 4. OVERTIME & NAV REFUND GAP MEASURES
-- ===================================================

[Overtid Art 1090 kNOK] = 
SUM(Fact_Regnskap[Overtid_Art1090_kNOK])

[NAV Refusjon Art 1600 kNOK] = 
SUM(Fact_Regnskap[NAV_Refusjon_Art1600_kNOK])

[Overtid vs Refusjon Gap kNOK] = 
[Overtid Art 1090 kNOK] - [NAV Refusjon Art 1600 kNOK]
```

---

## 4. Visual Layout & Page Architecture

1. **Page 1: Executive Dashboard (Bystyret / Formannskapet)**:
   * **Top KPI Cards**: Total Budget, YTD Actuals, Net Variance MNOK, Variance %, Overall RAG Status.
   * **Side-by-Side Column Chart**: Budget vs Actuals grouped by the 6 Virksomhetsområder.
   * **RAG Distribution Bar Chart**: Count of units categorized under Grønn, Rav, and Rød.
2. **Page 2: Enhetsmatrise & Drill-Down (81 Enheter)**:
   * **Matrix Table**: Fully sortable table containing all 81 Enheter with inline SVG RAG dots, KOSTRA codes, and variance values.
   * **Single-Enhet Deep Dive**: Monte Carlo EVM year-end trajectory (P10/P50/P90) and overtime vs. NAV refund gaps.
3. **Page 3: EU AI Act Audit Ledger (Stage-Gate Port 9)**:
   * Human-in-the-Loop sign-off panel logging saksbehandler notes, masked PII, and generating SHA-256 sealed audit records for *Kommunerevisjonen*.

---

## 5. Deployment & Streamlit MVP Codebase

The complete, interactive Streamlit implementation matching this Power BI specification is available in the published Python file:
* **`ai_kom_powerbi_dashboard.py`**
