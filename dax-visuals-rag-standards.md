# AI_KOM: Visual, DAX, and RAG Standardization Blueprint
**Kristiansand Kommune — Control Office Hub & AI Assistant (`AI_KOM`)**

---

## 1. Executive Overview & Purpose

This specification establishes binding standards for data modeling, DAX measure formulation, visual hierarchy, **Red-Amber-Green (RAG) status indicators (trafikklys)**, and **AI RAG (Retrieval-Augmented Generation)** context formatting across the `AI_KOM` platform (Power BI Embedded, Control Office Hub [index.html](file:///C:/Users/frank/Desktop/AI_KOM/index.html), Streamlit Dashboard, and Gemini 3.8 / Ollama Assistants).

The primary goal is to enforce **semantic coherence and financial precision** across all municipal metrics—preventing critical pitfalls such as:
1. Mislabeled variance signs or inverted cost overruns.
2. Division-by-zero errors masking unbudgeted expenditures as "favorable" (green).
3. Ambiguous absolute values (`ABS()`) distorting net operating results (*Netto driftsresultat*).
4. Color palette inconsistency violating Edward Tufte's Data-Ink standards ([01_tufte_data_ink_rules.md](file:///C:/Users/frank/Desktop/AI_KOM/.agents/rules/01_tufte_data_ink_rules.md)).
5. Unstructured prompt context in AI legal/financial retrieval.

> [!NOTE]
> **Terminologiavklaring**: Dokumentet skiller strengt mellom **RAG-trafikklys** (*Red-Amber-Green* statusflagg for avvik) og **AI RAG** (*Retrieval-Augmented Generation* for kildekritisk lovtolkning).

---

## 2. DAX Measure Standards & Sign Conventions

Municipal accounting in Norway follows *Kommuneloven* § 14-5 (budsjettbalanse), § 14-6 (bruttoprinsippet) og KOSTRA-kontoplan.

### 2.1 Accounting Directionality Rules
* **Expenditures (Utgifter - Art 000–599)**: Bokførte debetposter er positive verdier i regnskapet. Merforbruk (faktisk > budsjett) er ugunstig.
* **Revenues (Inntekter - Art 600–999)**: Kreditsaldoer er negative i rå ERP-tabeller (Visma Enterprise), men **må inverteres til positive tall** i rapporteringsmål. Merinntekt (faktisk > budsjett) er gunstig.
* **Bruttoprinsippet (Kommuneloven § 14-6)**: Inntekter (f.eks. NAV-refusjon art 1690) og utgifter (f.eks. sykepengelønn art 1020) skal alltid føres brutto. Det er ulovlig å nette disse i datagrunnlaget.
* **Kontoklasse 1 (Drift) vs. Kontoklasse 2 (Investering)**:
  * *Drift*: Avvik måles som $PV - AC$ (periodisert ramme mot faktisk forbruk).
  * *Investering*: Avvik måles med fremdriftsbasert Earned Value ($EV - AC$, $CPI = \frac{EV}{AC}$) jf. [02_project_controlling_evm_rules.md](file:///C:/Users/frank/Desktop/AI_KOM/.agents/rules/02_project_controlling_evm_rules.md).
* **Net Operating Result (Netto Driftsresultat)**: Beregnes som `Net Revenues - Net Expenditures`. Positiv = Overskudd (Gunstig), Negativ = Underskudd (Ugunstig).

### 2.2 Standardized Variance Measures (with Zero-Budget Guard)
Never use generic `Actual - Budget` formulas without line-item type and zero-denominator handling.

```dax
-- 1. Base Actuals & Budget
Actuals_NOK = SUM('Fact_Regnskap'[Belop])
Budget_NOK  = SUM('Fact_Budsjett'[Belop])

-- 2. Expenditure Variance (Positive = Favorable / Mindreforbruk)
Variance_Expenditure_NOK = [Budget_NOK] - [Actuals_NOK]

-- 3. Revenue Variance (Positive = Favorable / Merinntekt)
Variance_Revenue_NOK = [Actuals_NOK] - [Budget_NOK]

-- 4. Unified Favorable/Unfavorable Variance (Universal for cards and matrixes)
Financial_Variance_NOK = 
VAR _IsRevenue = SELECTEDVALUE('Dim_Art'[Is_Revenue], FALSE)
RETURN 
    IF(_IsRevenue, [Actuals_NOK] - [Budget_NOK], [Budget_NOK] - [Actuals_NOK])

-- 5. Percentage Variance with Zero-Budget & Boundary Safeguards
Variance_Pct = 
VAR _Budget = [Budget_NOK]
VAR _Actual = [Actuals_NOK]
VAR _Variance = [Financial_Variance_NOK]
VAR _IsCost = NOT(SELECTEDVALUE('Dim_Art'[Is_Revenue], FALSE))
RETURN
    SWITCH(
        TRUE(),
        -- Edge Case A: Ubudsjettert utgift (Budsjett = 0, Faktisk > 0) -> Kritisk overskridelse (-100 %)
        _IsCost && _Budget == 0 && _Actual > 0, -1.00,
        
        -- Edge Case B: Ubudsjettert inntekt (Budsjett = 0, Faktisk > 0) -> Ekstraordinær inntekt (+100 %)
        NOT(_IsCost) && _Budget == 0 && _Actual > 0, 1.00,
        
        -- Edge Case C: Begge er 0 -> Balanse
        _Budget == 0 && _Actual == 0, 0.00,
        
        -- Standard beregning mot nominelt budsjett
        DIVIDE(_Variance, ABS(_Budget), 0)
    )
```

### 2.3 Strict Rules for Absolute Values (`ABS()`)

| Regel | Godkjent Bruk | Forbudt Bruk |
| :--- | :--- | :--- |
| **BRUK `ABS()`** | Nevner i `%`-avviksberegninger for å unngå fortegnsvending ved negative poster. | Skjule negative verdier i tabeller eller for Netto Driftsresultat-kort. |
| **BRUK `ABS()`** | Stegstørrelse i Waterfall-diagrammer der retning styres av kategorilogikk. | Normalisere merforbruk slik at alle kostnadsavvik ser positive ut. |
| **IKKE BRUK `ABS()`** | KPI-kort som viser budsjettavvik, over-/underskudd eller disposisjonsfond. | Kolonner i styringsrapporter til formannskap eller kommunestyre. |

---

## 3. Red-Amber-Green (RAG) Trafikklys & Statusindikatorer

### 3.1 Threshold Matrix & Robust Status Measure
Trafikklysstatus beregnes dynamisk basert på relativt avvik (`Variance_Pct`) samt absolutte terskler jf. *Kommuneloven § 14-5* og [01_tufte_data_ink_rules.md](file:///C:/Users/frank/Desktop/AI_KOM/.agents/rules/01_tufte_data_ink_rules.md):

```dax
RAG_Status_Code = 
VAR _Actual = [Actuals_NOK]
VAR _Budget = [Budget_NOK]
VAR _VarPct = [Variance_Pct]
VAR _VarNOK = [Financial_Variance_NOK]
VAR _IsCost = NOT(SELECTEDVALUE('Dim_Art'[Is_Revenue], FALSE))
RETURN
    SWITCH(
        TRUE(),
        -- 1. Ubudsjettert merforbruk på utgiftskonto er alltid kritisk RØD
        _IsCost && _Budget == 0 && _Actual > 0, "RED",
        
        -- 2. Vesentlighetskriterium: Merforbruk over 500 000 NOK er alltid RØD uavhengig av %
        _VarNOK < -500000, "RED",
        
        -- 3. Prosentavvik (negativt betyr ugunstig/merforbruk)
        _VarPct >= -0.02, "GREEN",   -- Innenfor 2 % margin eller positivt mindreforbruk
        _VarPct >= -0.05, "AMBER",   -- 2 % til 5 % merforbruk (Observasjon / Varsel)
        "RED"                        -- > 5 % merforbruk (Kritisk avvik / Handleplikt § 14-5)
    )
```

### 3.2 Tufte-Harmoniserte Fargekoder & SVG KPI-Indikatorer

Fargepaletten følger Edward Tufte Data-Ink disiplin (dempede basisfarger, høymettede farger strengt reservert for aktive avvik):

```dax
-- Fargekode i henhold til repoets masterstandard (01_tufte_data_ink_rules.md)
RAG_Color_Hex = 
SWITCH(
    [RAG_Status_Code],
    "GREEN", "#27ae60",  -- Tufte Muted Green (Gunstig / I balanse)
    "AMBER", "#d35400",  -- Tufte Alert Amber (Varsel / 2-5 % avvik)
    "RED",   "#c0392b",  -- Tufte Critical Red (Kritisk merforbruk > 5 % eller > 500k)
    "#7f8c8d"            -- Nøytral skifergrå
)

-- Dynamisk SVG-statusprikk for tabeller i Power BI og HTML/Streamlit
RAG_SVG_Dot = 
VAR _Color = [RAG_Color_Hex]
RETURN
"data:image/svg+xml;utf8," & 
"<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 14 14'>" &
"<circle cx='7' cy='7' r='5' fill='" & _Color & "' />" &
"</svg>"
```

### 3.3 Power BI Dynamic Format Strings

Bruk dynamiske formatstrenger for å sikre profesjonell visning av beløp og prosenter uten desimalrot:

* **Valuta (kNOK)**: `#,##0 "kNOK";(#,##0 "kNOK");"-"`
* **Valuta (MNOK)**: `#,##0.0 "MNOK";(#,##0.0 "MNOK");"-"`
* **Prosentavvik med eksplisitt fortegn**: `+0.0 %;-0.0 %;0.0 %`

---

## 4. Visual Coherence & Dashboard Guidelines (Tufte Data-Ink)

### 4.1 Fargepalett for Konsernstyring
* **Primær Fylkes-/Kommune-Navy**: `#002B49` (Kristiansand mørkeblå)
* **Sekundær Aksent**: `#007A92` (Teal)
* **Statusfarger (Tufte Standard)**:
  * 🟢 Gunstig: `#27ae60`
  * 🟡 Varsel: `#d35400`
  * 🔴 Kritisk: `#c0392b`
* **Nøytral Bakgrunn**: `#F8F9FA` (Off-white) / Tabellkanter `#EEEEEE` (kun horisontale)

### 4.2 Diagramvalg og Formateringsregler
1. **Likviditet & Rullende Trender**:
   * Benytt linjediagrammer eller sparklines.
   * Direkte etikettering på endepunkter framfor frittstående fargetegnforklaringer.
2. **Sektor- og Enhetsfordeling (`Dim_Ansvar`, `Dim_Funksjon`)**:
   * Liggende stolpediagrammer sortert synkende etter rammevolum.
   * Start alltid x-aksen på 0 (aldri kuttet skala).
   * Bruk kun `RAG_Color_Hex` på stolper som krever aktiv oppmerksomhet; la normale enheter ha nøytral skiferfarge (`#7f8c8d`).
3. **Avviksnedbrytning (Waterfall)**:
   * Brukes for å visualisere broen fra opprinnelig budsjett til rullende prognose (EAC).
   * Røde klosser for kostnadsøkning, grønne klosser for mindreforbruk/inntektsøkning, marineblå for totaler.

---

## 5. AI Retrieval-Augmented Generation (RAG) Kontekstformatering

Ved overføring av regnskapstall og juridiske utdrag til `Gemini 3.8 Flash` eller lokal `Ollama`-instans, skal konteksten følge en deterministisk, strukturert blokkstruktur.

### 5.1 Prompt Kontekstskjema
Utdrag må merkes med unike ID-er, kildetype og skala:

```markdown
<retrieved_context id="chunk_1042" relevance_score="0.94">
### Dokument: Kommuneloven (2018) § 14-5
- **Kildetype**: Juridisk rammeverk / Statlig lovverk
- **Enhetsskala**: Beløp i MNOK (Millioner kroner)
- **Sektorkontekst**: Sentral konsernstyring / Bystyret

#### Utdrag:
"Kommunestyret skal vedta budsjettet i overensstemmelse med gjeldende rammer. Dersom det foreligger avvik som truer budsjettbalansen, plikter kommunedirektøren uten ugrunnet opphold å legge frem sak om budsjettrevisjon."
</retrieved_context>
```

### 5.2 Numeriske Retningslinjer for AI-Prompts
1. **Eksplisitt Beløpsskala**: Send aldri råtall som `12500000` uten måleenhet; formater alltid som `12,5 MNOK` eller `12 500 000 NOK`.
2. **Obligatorisk Kildeanker**: Pålegg modellen å inkludere referanse: `[Kommuneloven § 14-5, Kilde #1042]`.
3. **Bevar Eksplisitte Fortegn**: I tabeller skal merforbruk alltid ha minustegn (`-1,2 MNOK`) og merkes `(Ugunstig merforbruk / Avvik)`.
4. **PII-Skjerming**: Alle personnavn, fødselsnumre (FNR) og ansattidentifikatorer skal være vasket via [pii-guardrails](file:///C:/Users/frank/Desktop/AI_KOM/.agents/skills/pii-guardrails/SKILL.md) før LLM-konteksten genereres.

---

## 6. Sjekkliste for Implementering & Revisjonskontroll

- [ ] **DAX Nullbudsjett-sikring**: Bekreft at `Variance_Pct` og `RAG_Status_Code` håndterer `Budget = 0 && Actual > 0` som rød alarm.
- [ ] **Fortegnskontroll**: Bekreft at utgiftsavvik er `Budget - Actual` og inntektsavvik er `Actual - Budget`.
- [ ] **ABS-revisjon**: Bekreft at `ABS()` kun forekommer i prosentnevnere og waterfall-steg, aldri på bunnlinje- eller disposisjonsfondkort.
- [ ] **Tufte Fargepalett**: Bekreft at `#c0392b`, `#d35400` og `#27ae60` benyttes konsekvent.
- [ ] **Bruttoprinsippet (§ 14-6)**: Bekreft at refusjoner og lønnsutgifter ikke er nettet i Power Query eller DAX.
- [ ] **AI Kontekstsanering**: Bekreft at RAG-blokker inneholder kilde-ID og enhetsskala (`MNOK`), og er PII-vasket jf. Stage-Gate Port 4.
