# AI_KOM: Visual, DAX, and RAG Standardization Blueprint
**Kristiansand Kommune — Control Office Hub & AI Assistant (`AI_KOM`)**

---

## 1. Executive Overview & Purpose

This specification establishes binding standards for data modeling, DAX measure formulation, visual hierarchy, Red-Amber-Green (RAG) status indicators, and AI RAG (Retrieval-Augmented Generation) context formatting across the `AI_KOM` platform (Power BI Embedded, Streamlit Dashboard, and Gemini 3.8 Assistant).

The primary goal is to enforce **semantic coherence** across all financial metrics—preventing common pitfalls such as mislabeled variance signs, ambiguous absolute values (`ABS()`), inconsistent color coding across municipal sectors, or unstructured prompt context in AI retrieval.

---

## 2. DAX Measure Standards & Sign Conventions

Municipal accounting in Norway follows *Kommuneloven* § 14-5 and KOSTRA grouping standards. Financial measures must maintain strict directional logic.

### 2.1 Accounting Directionality Rules
* **Expenditures (Utgifter - Art 000–599)**: Debit balances are positive values.
* **Revenues (Inntekter - Art 600–999)**: Credit balances are negative in raw ERP tables, but **must be inverted to positive numbers** in presentation measures.
* **Net Operating Result (Netto Driftsresultat)**: Calculated as `Net Revenues - Net Expenditures`. Positive = Surplus (Favorable), Negative = Deficit (Unfavorable).

### 2.2 Standardized Variance Measures
Never use generic `Actual - Budget` formulas without accounting for line item type.

```dax
-- 1. Base Actuals & Budget
Actuals_NOK = SUM('Fact_Regnskap'[Belop])
Budget_NOK  = SUM('Fact_Budsjett'[Belop])

-- 2. Expenditure Variance (Positive = Favorable / Under Budget)
Variance_Expenditure_NOK = [Budget_NOK] - [Actuals_NOK]

-- 3. Revenue Variance (Positive = Favorable / Over Budget)
Variance_Revenue_NOK = [Actuals_NOK] - [Budget_NOK]

-- 4. Unified Favorable/Unfavorable Variance (For Universal Cards)
Financial_Variance_NOK = 
VAR _IsRevenue = SELECTEDVALUE('Dim_Art'[Is_Revenue], FALSE)
RETURN 
    IF(_IsRevenue, [Actuals_NOK] - [Budget_NOK], [Budget_NOK] - [Actuals_NOK])

-- 5. Percentage Variance
Variance_Pct = 
DIVIDE([Financial_Variance_NOK], ABS([Budget_NOK]), 0)
```

### 2.3 Strict Rules for Absolute Values (`ABS()`)

| Rule | Approved Use Case | Forbidden Use Case |
| :--- | :--- | :--- |
| **DO USE `ABS()`** | Denominator in `%` variance calculations to prevent sign inversion on negative budgets. | Hiding negative values in variance reporting tables or Net Operating Result cards. |
| **DO USE `ABS()`** | Waterfall chart step sizing where orientation (increase/decrease) is handled by category logic. | Normalizing cost overruns to make all deviations look positive. |
| **DO NOT USE `ABS()`** | KPI Cards displaying budget drift, net surplus, or deficit balances. | Financial table columns comparing sector performances. |

---

## 3. Red-Amber-Green (RAG) Status Indicators

### 3.1 Threshold Matrix
RAG statuses are calculated dynamically based on relative budget deviation (`Variance_Pct`):

```dax
RAG_Status_Code = 
VAR _VarPct = [Variance_Pct]
RETURN
    SWITCH(
        TRUE(),
        _VarPct >= -0.02, "GREEN",   -- Within 2% threshold or favorable
        _VarPct >= -0.05, "AMBER",   -- 2% to 5% overrun (Warning)
        "RED"                        -- > 5% budget overrun (Critical Alert)
    )
```

### 3.2 Dynamic Hex Color & SVG KPI Measures

```dax
RAG_Color_Hex = 
SWITCH(
    [RAG_Status_Code],
    "GREEN", "#388E3C",  -- Municipal Green (Favorable)
    "AMBER", "#F57C00",  -- Alert Amber (Caution)
    "RED",   "#D32F2F",  -- Critical Red (Overrun)
    "#757575"            -- Neutral Gray
)

-- Dynamic SVG Indicator for Streamlit / Power BI Tables
RAG_SVG_Dot = 
VAR _Color = [RAG_Color_Hex]
RETURN
"data:image/svg+xml;utf8," & 
"<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'>" &
"<circle cx='8' cy='8' r='6' fill='" & _Color & "' />" &
"</svg>"
```

---

## 4. Visual Coherence & Dashboard Guidelines

### 4.1 Color Palette Governance
* **Primary Brand Header**: `#002B49` (Kristiansand Navy)
* **Secondary Accent**: `#007A92` (Teal)
* **Status Colors**: `Green (#388E3C)`, `Amber (#F57C00)`, `Red (#D32F2F)`
* **Neutral Background**: `#F8F9FA` (Off-white / Light Gray)

### 4.2 Chart Selection & Formatting Rules
1. **Time-Series Liquidity & Monthly Trends**:
   * Use **Line / Area Charts**.
   * X-Axis: Monthly chronological order (`Jan` – `Dec`).
   * Y-Axis: Always include currency unit (`MNOK` or `kNOK`) in title.
2. **Sector & Unit Comparison (`Dim_Ansvar`, `Dim_Funksjon`)**:
   * Use **Horizontal Bar Charts** sorted descending by absolute budget volume.
   * Apply `RAG_Color_Hex` conditionally to bar fills to highlight units requiring control focus.
3. **Budget Decomposition & Variance Analysis**:
   * Use **Waterfall Charts**.
   * Explicitly color Increase = Red (if cost increase), Decrease = Green, Total = Navy.

---

## 5. AI Retrieval-Augmented Generation (RAG) Context Formatting

When passing financial and legal data chunks to `Gemini 3.8 Flash` or local Ollama instances, context must adhere to a standardized, deterministic Markdown structure.

### 5.1 Prompt Context Formatting Schema
Every retrieved document chunk must be wrapped in canonical XML/Markdown blocks containing explicit metadata:

```markdown
<retrieved_context id="chunk_1042" relevance_score="0.92">
### Document: Kommuneloven (2018) § 14-5
- **Source Type**: Legal Framework / Municipal Regulation
- **Unit Scale**: Values expressed in MNOK (Million NOK)
- **Sector Context**: Central Controlling / General Governance

#### Excerpt:
"Kommunestyret skal vedta budsjettet i overensstemmelse med gjeldede rammer. Avvik som overstiger 5 % på rammeområde skal uten ugrunnet opphold rapporteres til kontrollutvalget."
</retrieved_context>
```

### 5.2 Numeric Formatting Rules for AI Prompts
1. **Always State Currency Scale Explicitly**: Never pass raw numbers like `12500000` without specifying `12.5 MNOK` or `12 500 000 NOK`.
2. **Enforce Citation Anchors**: Instruct the LLM to output inline citations matching chunk IDs: `[Kommuneloven § 14-5, Chunk #1042]`.
3. **Preserve Explicit Signs**: In financial context tables, display negative variances explicitly with minus signs (`-1.2 MNOK`) and label them as `(Unfavorable Overrun)`.

---

## 6. Implementation Checklist & Verification Gates

- [ ] **DAX Audit**: Verify that all variance measures use `Budget - Actual` for costs and `Actual - Budget` for revenues.
- [ ] **ABS Check**: Confirm `ABS()` is used ONLY in denominators or waterfall magnitudes, never in net total cards.
- [ ] **RAG Consistency**: Verify that Red (`#D32F2F`) is reserved strictly for unfavorable deviations > 5%.
- [ ] **AI Context Sanitization**: Verify that retrieved RAG prompt chunks contain explicit scale units (`MNOK`) and document citations.
