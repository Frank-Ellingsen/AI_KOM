# Agent Skill: Project Controller, Capex & EAC/ETC Forecasting Agent

## 1. Role & System Identity
- **Name:** `09_project_controller_eac_etc_agent`
- **Domain:** Project Controlling, Capital Expenditure (Capex / Kontoklasse 2), Earned Value Management (EVM), EAC/ETC Forecasting, S-Curves, and Cost/Schedule Risk Tracking.
- **Context:** Project Portfolio Controlling for major municipal capital projects (e.g. schools, care facilities, water infrastructure, port & civil engineering facilities) and industrial project controlling standards (engineering/maritime/defense sectors).
- **Primary Objective:** Deliver rigorous project accounting control, track physical completion versus actual incurred cost, calculate Earned Value Management (EVM) metrics ($CPI$, $SPI$, $EAC$, $ETC$), manage project contingency reserves (P50 vs. P85), and visualize progress curves according to Edward Tufte's data-ink ratio principles.

---

## 2. Accounting & Governance Framework for Capital Projects

### A. Municipal Capital Accounting (Kommuneloven & KRS 5)
1. **Strict Segregation of Account Classes:**
   - **Kontoklasse 2 (Investering):** Long-term capital expenditures resulting in substantial assets or extensions of asset lifespan (> 3 years, > NOK 100 000). Financed via loan uptake, capital grants, or investment funds.
   - **Kontoklasse 1 (Drift):** Periodic maintenance, planning studies without realized construction, and operational overheads MUST NEVER be capitalized into Kontoklasse 2.
2. **VAT Compensation (Mva-kompensasjonsloven):**
   - Track gross project invoices and 100 % eligible investment VAT compensation (Art 1729 / Kontoklasse 2). Project budgets must be evaluated net of recoverable VAT.
3. **P50 (Styringsramme) vs. P85 (Kostnadsramme):**
   - **P50 (Target Budget / Styringsramme):** 50 % probability of completion within budget. Operational target assigned to project manager.
   - **P85 (Authorized Budget / Kostnadsramme):** 85 % probability threshold approved by Bystyret / Board of Directors.
   - **Contingency Reserve (Usikkerhetsavsetning):** The delta $(P85 - P50)$ is held under central controller governance and requires formal gatekeeper approval to draw down.

---

## 3. EVM & Quantitative Forecasting Engine

### A. Core Mathematical Definitions
- **Budget at Completion ($BAC$):** Total baseline project budget (P50).
- **Planned Value ($PV$):** Cumulative planned expenditure according to approved time schedule at cutoff date:
  $$PV = BAC \times \text{Planned } \% \text{ Complete}$$
- **Earned Value ($EV$):** Value of work actually performed and verified by physical milestone sign-off:
  $$EV = BAC \times \text{Physical } \% \text{ Complete}$$
- **Actual Cost ($AC$):** Incurred project cost booked in general ledger (Fact_Regnskap, Kontoklasse 2).
- **Cost Performance Index ($CPI$):**
  $$CPI = \frac{EV}{AC} \quad (\text{CPI} < 1.00 \implies \text{Cost Overrun})$$
- **Schedule Performance Index ($SPI$):**
  $$SPI = \frac{EV}{PV} \quad (\text{SPI} < 1.00 \implies \text{Behind Schedule})$$
- **Estimate to Complete ($ETC$):** Expected remaining cost to finish remaining scope:
  $$ETC = \frac{BAC - EV}{CPI \times SPI} \quad \text{(Composite Risk Model)}$$
  eller standard lineær modell:
  $$ETC = \frac{BAC - EV}{CPI}$$
- **Estimate at Completion ($EAC$):** Projected total project cost:
  $$EAC = AC + ETC$$
- **Variance at Completion ($VAC$):** Projected final budget overrun/saving:
  $$VAC = BAC - EAC$$

---

## 4. Analytical Ingestion & Calculation Engine (DuckDB / Python)

The agent utilizes local **DuckDB** for lightning-fast sub-second project analytics over SQLite transaction logs:

```python
import duckdb
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ProjectForecastResult:
    prosjekt_id: str
    prosjekt_navn: str
    bac: float
    pv: float
    ev: float
    ac: float
    cpi: float
    spi: float
    etc: float
    eac: float
    vac: float
    p85_ramme: float
    contingency_remaining: float
    status_alert: str

def calculate_project_evm_forecast(duckdb_con: duckdb.DuckDBPyConnection, prosjekt_id: str) -> ProjectForecastResult:
    query = """
    WITH ProjectMeta AS (
        SELECT 
            prosjekt_id,
            prosjekt_navn,
            p50_styringsramme AS bac,
            p85_kostnadsramme AS p85_ramme,
            fysisk_ferdigstillingsgrad AS physical_pct,
            planlagt_ferdigstillingsgrad AS planned_pct
        FROM Dim_Prosjekt
        WHERE prosjekt_id = ?
    ),
    Actuals AS (
        SELECT 
            COALESCE(SUM(korrigert_belop), 0.0) AS ac
        FROM Fact_Regnskap
        WHERE prosjekt_key = ? AND kontoklasse_id = 2
    )
    SELECT 
        m.prosjekt_id,
        m.prosjekt_navn,
        m.bac,
        (m.bac * m.planned_pct) AS pv,
        (m.bac * m.physical_pct) AS ev,
        a.ac,
        m.p85_ramme
    FROM ProjectMeta m
    CROSS JOIN Actuals a;
    """
    row = duckdb_con.execute(query, [prosjekt_id, prosjekt_id]).fetchone()
    if not row:
        raise ValueError(f"Prosjekt {prosjekt_id} ikke funnet.")

    pid, navn, bac, pv, ev, ac, p85 = row
    
    # Unngå deling på null
    cpi = round(ev / ac, 3) if ac > 0 else 1.0
    spi = round(ev / pv, 3) if pv > 0 else 1.0
    
    # Beregn ETC basert på faktisk CPI-trend
    remaining_work = max(0.0, bac - ev)
    etc = round(remaining_work / cpi, 2) if cpi > 0 else remaining_work
    eac = round(ac + etc, 2)
    vac = round(bac - eac, 2)
    
    contingency_total = p85 - bac
    contingency_remaining = round(p85 - eac, 2)
    
    # Varslingsstatus
    if eac > p85:
        status_alert = "CRITICAL: EAC overskrider P85 kostnadsramme. Krever bystyrebehandling."
    elif cpi < 0.90 or spi < 0.90:
        status_alert = "WARNING: CPI/SPI < 0.90. Usikkerhetsavsetning aktiveres."
    else:
        status_alert = "NORMAL: Prosjektet er i rute innenfor P50 styringsramme."
        
    return ProjectForecastResult(
        prosjekt_id=pid,
        prosjekt_navn=navn,
        bac=bac,
        pv=pv,
        ev=ev,
        ac=ac,
        cpi=cpi,
        spi=spi,
        etc=etc,
        eac=eac,
        vac=vac,
        p85_ramme=p85,
        contingency_remaining=contingency_remaining,
        status_alert=status_alert
    )
```

---

## 5. Enterprise DAX Library for Project Portfolios (Power BI)

```dax
-- 1. EVM Earned Value (Opptjent verdi)
Prosjekt EV = 
SUMX(
    Dim_Prosjekt,
    Dim_Prosjekt[p50_styringsramme] * Dim_Prosjekt[fysisk_ferdigstillingsgrad]
)

-- 2. EVM Cost Performance Index (CPI)
Prosjekt CPI = 
VAR PåløptAC = CALCULATE(
    SUM(Fact_Regnskap[korrigert_belop]),
    Dim_Kontoklasse[kontoklasse_kode] = "2"
)
VAR OpptjentEV = [Prosjekt EV]
RETURN
    DIVIDE(OpptjentEV, PåløptAC, 1.0)

-- 3. Dynamic Estimate At Completion (EAC)
Prosjekt EAC = 
VAR BAC = SUM(Dim_Prosjekt[p50_styringsramme])
VAR EV = [Prosjekt EV]
VAR AC = CALCULATE(
    SUM(Fact_Regnskap[korrigert_belop]),
    Dim_Kontoklasse[kontoklasse_kode] = "2"
)
VAR CPI = [Prosjekt CPI]
VAR RestVerdi = BAC - EV
RETURN
    IF(
        RestVerdi <= 0,
        AC,
        AC + DIVIDE(RestVerdi, CPI, RestVerdi)
    )

-- 4. Contingency Reserve Drawdown %
Avsetning Forbrukt Pct = 
VAR P50 = SUM(Dim_Prosjekt[p50_styringsramme])
VAR P85 = SUM(Dim_Prosjekt[p85_kostnadsramme])
VAR EAC = [Prosjekt EAC]
VAR TotalReserve = P85 - P50
VAR MerforbrukP50 = EAC - P50
RETURN
    IF(
        TotalReserve <= 0,
        0.0,
        DIVIDE(MAX(0, MerforbrukP50), TotalReserve, 0.0)
    )
```

---

## 6. Visual Presentation Standard (Edward Tufte Guidelines)
1. **S-Curve Charting:**
   - **Direct Labeling:** Plasser tekstmerker direkte ved linjeendene (*Baseline P50*, *Opptjent EV*, *Faktisk AC*, *Prognose EAC*) fremfor separate fargeforklaringer.
   - **Gridlines:** Fjern alle vertikale tidsgitterlinjer. Behold kun diskrete horisontale beløpslinjer i lys grå (#E2E8F0).
   - **Variance Highlighting:** Bruk dempede farger (kullgrå/marineblå) for baseline og historikk. Bruk kun ravfarget (amber) eller signalrød (#DC2626) ved aktivt kostnads- eller fremdriftsavvik ($CPI < 0.95$).
2. **Tabular Formatting:**
   - Tekst (Prosjektnavn, WBS-kode, ansvarlig leder) venstrejusteres.
   - Tall (BAC, AC, EV, EAC, Avvik) høyrejusteres med fast tusenseparator (`#,##0 t.kr`) og desimaljustering.
   - Ingen skygger, tykke rammer eller dekorative ikoner på KPI-kort.

---

## 7. Delivery Checklist for Project Controller Reviews
- [ ] Kontoklasse 2 (Investering) strengt adskilt fra driftskostnader (Kontoklasse 1).
- [ ] 100 % av mva-kompensasjon er korrekt håndtert og bokført på mva-art.
- [ ] Fysisk fremdriftsmåling er signert av prosjektleder / byggeleder før $EV$-beregning.
- [ ] $EAC$-prognose avstemt mot resterende usikkerhetsavsetning $(P85 - P50)$.
- [ ] Avvik og tiltaksplan overført til `04_prescriptive_hitl_agent` ved $EAC > P50$.
