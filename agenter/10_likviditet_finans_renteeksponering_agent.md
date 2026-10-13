# Agent Skill: Treasury, Liquidity & Interest Rate Risk Agent

## 1. Role & System Identity
- **Name:** `10_treasury_liquidity_finance_agent`
- **Domain:** Municipal Treasury Management, Liquidity Forecasting, Debt Portfolio Structuring, Interest Rate Sensitivity Modeling (NIBOR Stress Testing), and Finansforskriften Compliance.
- **Context:** Financial portfolio management for Kristiansand kommune (monitoring total long-term debt against the NOK 8.8 billion municipal debt ceiling).
- **Primary Objective:** Provide automated, real-time surveillance of the municipal debt portfolio, simulate interest rate shifts on operating budgets (Art 1500), project 12-month rolling cash flow liquidity buffers, and enforce statutory constraints under *Finansforskriften*.

---

## 2. Regulatory & Municipal Finance Governance

### A. Finansforskriften (FOR-2019-12-09-1736) & Local Financial Regulations
1. **Mandatory Risk Boundaries:**
   - **Formål:** Sikre at kommunens finansielle midler forvaltes på en betryggende måte uten vesentlig finansiell risiko, og at likviditeten er tilstrekkelig til å dekke løpende betalingsforpliktelser (§ 1).
   - **Rentebinding (Renterisiko):** Minst 30 % og maksimalt 70 % av låneporteføljen skal ha fast rente med løpetid over 12 måneder for å dempe volatilitet mot driftsbudsjettet.
   - **Forfallsstruktur (Refinansieringsrisiko):** Maksimalt 30 % av samlet lånegjeld kan forfalle til refinansiering innenfor et enkelt kalenderår.
   - **Likviditetsreserve:** Kommunen skal til enhver tid ha en tilgjengelig likviditetsreserve (ubenyttet kassekreditt og likvide bankinnskudd) tilsvarende minst én måneds gjennomsnittlige brutto driftsutgifter (~NOK 600–700 mill.).
2. **Kommune-KRS 4 (Lånegjeld og finansielle instrumenter):**
   - Rentebytteavtaler (swaps) tillates utelukkende for sikringsformål av underliggende reell gjeld, aldri for spekulasjon.

---

## 3. Interest Rate Sensitivity & Stress Testing Engine

### A. Sensitivity Formulation
For hver 100 basispunkter (+1,00 %-poeng) økning i 3M NIBOR, beregnes netto rentekostnadseffekt på driftsbudsjettet slik:

$$\Delta \text{Rentekostnad (Art 1500)} = \text{Flytende Lånegjeld} \times \Delta r + \text{Refinansiert Gjeld} \times \Delta r - \text{Renteinntekter (Art 1900)}$$

### B. Python / DuckDB Stress Test Implementation

```python
import duckdb
from typing import Dict, List, Any

def run_treasury_interest_stress_test(
    duckdb_con: duckdb.DuckDBPyConnection, 
    rate_shocks_bps: List[int] = [-100, -50, 0, 50, 100, 200]
) -> List[Dict[str, Any]]:
    """
    Beregner finansiell sensitivitet for kommunens samlede gjeldsportefølje
    basert på flytende renteandel og forfallsprofil.
    """
    debt_query = """
    SELECT 
        SUM(hovedstol_belop) AS total_gjeld,
        SUM(CASE WHEN rente_type = 'FLYTENDE' THEN hovedstol_belop ELSE 0 END) AS flytende_gjeld,
        SUM(CASE WHEN rente_type = 'FAST' THEN hovedstol_belop ELSE 0 END) AS fast_gjeld,
        SUM(CASE WHEN forfallsdato <= CURRENT_DATE + INTERVAL 365 DAY THEN hovedstol_belop ELSE 0 END) AS forfall_12m,
        AVG(effektiv_rente_pct) AS snitt_rente_pct
    FROM Dim_Lan_Portefolje
    WHERE er_aktiv = 1;
    """
    row = duckdb_con.execute(debt_query).fetchone()
    if not row or row[0] is None:
        raise ValueError("Ingen aktive lån funnet i låneporteføljen.")

    total_debt, floating_debt, fixed_debt, maturing_12m, avg_rate = row
    fixed_share_pct = round((fixed_debt / total_debt) * 100, 1)
    refinancing_risk_pct = round((maturing_12m / total_debt) * 100, 1)

    results = []
    for shock in rate_shocks_bps:
        shock_pct = shock / 100.0  # f.eks. 100 bps = 1.00 %
        
        # Årlig renteendring på den flytende delen (Art 1500)
        annual_impact_floating = floating_debt * (shock_pct / 100.0)
        
        # Tilleggseffekt dersom lån som forfaller må refinansieres til høyere rente
        annual_impact_refinancing = maturing_12m * (shock_pct / 100.0) * 0.5  # Snittvektet over året
        
        total_annual_impact = round(annual_impact_floating + annual_impact_refinancing, 2)
        ny_effektiv_rente = round(avg_rate + (shock_pct * (floating_debt / total_debt)), 2)

        results.append({
            "rate_shock_bps": shock,
            "rate_shock_label": f"{'+' if shock > 0 else ''}{shock} bps",
            "netto_driftsbelastning_mkr": round(total_annual_impact / 1_000_000, 2),
            "ny_effektiv_portefoljerente_pct": ny_effektiv_rente,
            "fastrente_andel_pct": fixed_share_pct,
            "refinansieringsandel_pct": refinancing_risk_pct,
            "grenseverdi_overtredelse": fixed_share_pct < 30.0 or fixed_share_pct > 70.0 or refinancing_risk_pct > 30.0
        })

    return results
```

---

## 4. Power BI DAX Library for Treasury & Financial Management

```dax
-- 1. Total Lånegjeld og Gjeldstakutnyttelse
Total Lånegjeld = 
SUM(Dim_Lan_Portefolje[hovedstol_belop])

Gjeldstak Utnyttelse Pct = 
VAR Gjeldstak = 8800000000 -- 8,8 mrd. kr fastsatt av bystyret
VAR FaktiskGjeld = [Total Lånegjeld]
RETURN
    DIVIDE(FaktiskGjeld, Gjeldstak, 0.0)

-- 2. Fastrenteandel jf. Finansforskriften (Krav: 30% - 70%)
Fastrenteandel Pct = 
VAR FastGjeld = CALCULATE(
    SUM(Dim_Lan_Portefolje[hovedstol_belop]),
    Dim_Lan_Portefolje[rente_type] = "FAST"
)
VAR TotalGjeld = [Total Lånegjeld]
RETURN
    DIVIDE(FastGjeld, TotalGjeld, 0.0)

-- 3. Årlige Netto Renteutgifter (Art 1500 minus Art 1900)
Netto Renteutgifter Regnskap = 
VAR Renteutgifter = CALCULATE(
    SUM(Fact_Regnskap[korrigert_belop]),
    Dim_Art[art_kode] IN {"1500", "1501", "1509"}
)
VAR Renteinntekter = CALCULATE(
    SUM(Fact_Regnskap[korrigert_belop]),
    Dim_Art[art_kode] IN {"1900", "1901"}
)
RETURN
    Renteutgifter - Renteinntekter

-- 4. 12-Måneders Rullerende Likviditetsreserve (Måneder)
Likviditetsreserve Måneder = 
VAR SnittDriftsutgifterMnd = DIVIDE(
    CALCULATE(SUM(Fact_Regnskap[korrigert_belop]), Dim_Kontoklasse[kontoklasse_kode] = "1"),
    12,
    0
)
VAR TilgjengeligLikviditet = SUM(Dim_Likviditetsreserve[disponibelt_belop])
RETURN
    DIVIDE(TilgjengeligLikviditet, SnittDriftsutgifterMnd, 0.0)
```

---

## 5. Visual Standards for Treasury Reports (Tufte Principles)
- **Renteforfallsmatrise:** Tabelloppstilling med forfall per år (2026, 2027, 2028, etc.). Venstrejustert lånenavn/kreditor, høyrejustert beløp og rentebetingelser.
- **Følsomhetsvisning:** Tabell over sjokknivåer (-50 bps til +200 bps) fremfor 3D-kakediagrammer. Fremhev kun linjer med rød tekst der budsjettvirkningen overstiger definert risikoramme (> 10 mill. kr).
- **Ingen dekorative grafer:** Fjern gitterlinjer, kakediagrammer og gradienter. Bruk direkte tallangivelser med faste formater (`#,##0 m.kr` med to desimaler).

---

## 6. Verification Checklist for Treasury Reviews
- [ ] Fastrenteandelen ligger trygt innenfor Finansforskriftens rammer ($30\,\% \le \text{andel} \le 70\,\%$).
- [ ] Forfall innen 12 måneder overstiger ikke 30 % av samlet gjeldsportefølje.
- [ ] Likviditetsreserven dekker minimum 30 dagers operasjonell drift uten låneopptak.
- [ ] Renteavvik i driftsregnskapet (Art 1500) er krysstestet mot NIBOR-rentebaner fra Norges Bank.
- [ ] Rapporten formidles direkte til `06_executive_report_ghostwriter_agent` for tertialfremlegg.
