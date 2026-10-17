# ANTIGRAVITY Cash Management & Likviditetsmodul

**Modulnavn:** `app.modules.cash_management`  
**Sektor:** Kommunal finansforvaltning, likviditetsstyring og kassekredittoppfølging  
**Regelverk:** Kommuneloven §§ 14-1, 14-13, 14-14, 14-15, Forskrift om garantier og finans- og gjeldsforvaltning (finansforskriften).

---

## 1. Formål og Funksjonalitet

Cash Management-modulen i **Antigravity Engine** tilbyr automatisert, helhetlig og sanntids likviditetsforvaltning for norske kommuner. Modulen bygger bro mellom **Visma ERP / Hovedbank** (daglige kontostand, banktransaksjoner og konsernkontoordning) og **Framsikt** (periodisert budsjett, skatteinngangsprognoser og terminutbetalinger fra staten).

### Hovedfunksjoner:
1. **12-Måneders & 30-Dagers Rullende Likviditetsprognose (`CashFlowEngine`):**
   * Modellering av forutsigbare kommunale likviditetstopper og -bunner.
   * Håndtering av terminer for **rammetilskudd** (januar, mars, mai, juli, september, november) og **skatteforfall**.
   * Identifisering av kritiske likviditetsbunner (f.eks. utbetaling av fastlønn den 12. hver måned før statlige overføringer triller inn den 15.).
2. **Kassakreditt & Rammeoppfølging (`CreditLimitMonitor`):**
   * Sanntids overvåking av utnyttelsesgrad på kommunestyrets vedtatte **driftskredittramme** (jf. Kommuneloven § 14-14).
   * Automatisk varsling ved fare for å overskride godkjent låneramme eller ved unødvendig trekk på rentebærende kreditt.
3. **Plasserings- og Renteoptimering (`LiquidityBufferOptimizer`):**
   * Automatiserte anbefalinger for flytting av overskuddslikviditet mellom konsernkonto, kortsiktige plasseringer (bankinnskudd/pengemarkedsfond) og nedbetaling av trekkrettigheter for å minimere nettoramrenter.
4. **Finansforskriften & Reglementskontroll (`ComplianceGuard`):**
   * Automatisk sjekk av at all likviditet er plassert i **NOK**, i godkjente finansinstitusjoner, og at løpetid/risikoprofil er i tråd med kommunens vedtatte **Finansreglement**.

---

## 2. Systemarkitektur & Datastream Pipeline

```
[ ERP / Visma API ] ──► (Daglig Saldobalanse / Konsernkonto) ┐
                                                           ├─► [ CashFlowEngine ] ──► [ Liquidity Dashboard ]
[ Framsikt API ]   ──► (Periodisert Budsjett / Terminplan)  │        │
                                                           │        ▼
[ Skatteetaten ]   ──► (Skatteprognoser / MVA-refusjon)   ┘  [ ComplianceCheck ] ──► [ Alert & Stage-Gate Port 9 ]
```

---

## 3. API Spesifikasjon (FastAPI Endepunkter)

### `GET /api/v1/cash/position`
Henter nåværende konsernsaldo, utnyttelse av kassakreditt og disponibel likviditetsbuffer.

### `GET /api/v1/cash/forecast`
Henter 30-dagers og 12-måneders rullende likviditetsprognose.
* **Query Params:** `period_start` (YYYY-MM-DD), `granularity` (`DAILY` | `WEEKLY` | `MONTHLY`).

### `POST /api/v1/cash/simulate`
Kjører "What-If" scenariesimuleringer på likviditetsstrømmen.
* **Payload:**
```json
{
  "scenario_name": "Forsinket Skatteinngang & Snøbrøyting",
  "tax_revenue_delta_percent": -5.0,
  "state_grant_delay_days": 10,
  "extraordinary_expense_nok": 2500000.0,
  "expense_account_art": 1270
}
```

---

## 4. Pydantic Datamodeller (`app/schemas/cash.py`)

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class CashPosition(BaseModel):
    as_of_date: date
    bank_balance_nok: float = Field(..., description="Innestående på kommunens konsernkonto")
    credit_facility_limit_nok: float = Field(..., description="Vedtatt ramme for driftskreditt/kassakreditt")
    credit_facility_used_nok: float = Field(..., description="Benyttet driftskreditt per i dag")
    available_liquidity_nok: float = Field(..., description="Total disponibel likviditet (Bank + Unytta kreditt)")
    utilization_rate_percent: float

class DailyCashFlowEntry(BaseModel):
    entry_date: date
    inflow_tax_nok: float = 0.0
    inflow_state_grants_nok: float = 0.0
    inflow_other_nok: float = 0.0
    outflow_payroll_nok: float = 0.0
    outflow_suppliers_nok: float = 0.0
    outflow_debt_service_nok: float = 0.0
    net_cash_flow_nok: float
    projected_end_balance_nok: float
    credit_draw_nok: float
```

---

## 5. Cash Management Engine Core (`app/services/cash_engine.py`)

```python
import polars as pl
from datetime import date, timedelta

class CashManagementEngine:
    def __init__(self, credit_limit: float = 150_000_000.0):
        self.credit_limit = credit_limit

    def calculate_daily_forecast(
        self, 
        start_balance: float, 
        df_flows: pl.DataFrame
    ) -> pl.DataFrame:
        """
        Beregner rullende saldo, trekk på kassakreditt og rentebelastning.
        """
        forecast_records = []
        current_balance = start_balance

        for row in df_flows.iter_rows(named=True):
            inflow = row['inflow_tax'] + row['inflow_state_grants'] + row['inflow_other']
            outflow = row['outflow_payroll'] + row['outflow_suppliers'] + row['outflow_debt_service']
            net = inflow - outflow
            current_balance += net

            credit_draw = 0.0
            if current_balance < 0:
                credit_draw = abs(current_balance)
                if credit_draw > self.credit_limit:
                    status = "CRITICAL_OVERDRAFT"
                else:
                    status = "CREDIT_UTILIZED"
            else:
                status = "SURPLUS_LIQUIDITY"

            forecast_records.append({
                "entry_date": row["entry_date"],
                "inflow_total": inflow,
                "outflow_total": outflow,
                "net_change": net,
                "closing_balance": current_balance,
                "credit_draw": credit_draw,
                "available_credit_remaining": max(0.0, self.credit_limit - credit_draw),
                "status": status
            })

        return pl.DataFrame(forecast_records)
```

---

## 6. Frontend UI Komponent (`CashManagementDashboard.tsx`)

```tsx
import React, { useState } from 'react';

export const CashManagementDashboard: React.FC = () => {
  const [creditLimit] = useState(150000000); // 150 mill kr ramme
  const [creditUsed] = useState(24500000);   // 24.5 mill kr trukket

  const utilization = ((creditUsed / creditLimit) * 100).toFixed(1);

  return (
    <div className="p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-800">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold flex items-center gap-2">
          💳 Cash Management & Likviditetsstyring
        </h2>
        <span className="bg-emerald-500/20 text-emerald-400 text-xs px-3 py-1 rounded-full border border-emerald-500/30">
          Status: LIKVIDITET I BALANSE
        </span>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-slate-800/80 p-4 rounded-lg border border-slate-700">
          <p className="text-xs text-slate-400">Konsernkonto Balance</p>
          <p className="text-xl font-bold text-emerald-400">42 850 000 NOK</p>
        </div>
        <div className="bg-slate-800/80 p-4 rounded-lg border border-slate-700">
          <p className="text-xs text-slate-400">Vedtatt Kassakredittramme</p>
          <p className="text-xl font-bold text-slate-200">150 000 000 NOK</p>
        </div>
        <div className="bg-slate-800/80 p-4 rounded-lg border border-slate-700">
          <p className="text-xs text-slate-400">Benyttet Kassakreditt</p>
          <p className="text-xl font-bold text-amber-400">24 500 000 NOK</p>
          <p className="text-xs text-slate-500 mt-1">Utnyttelsesgrad: {utilization}%</p>
        </div>
        <div className="bg-slate-800/80 p-4 rounded-lg border border-slate-700">
          <p className="text-xs text-slate-400">Disponibel Buffer</p>
          <p className="text-xl font-bold text-blue-400">168 350 000 NOK</p>
        </div>
      </div>

      {/* Likviditetsfeller & Varsler */}
      <div className="p-4 bg-amber-500/10 border border-amber-500/30 rounded-lg text-amber-200 text-sm mb-6">
        <strong>⚠️ Likviditetsvarsel (M11 November):</strong>
        Fastlønn (Art 1010) på 82 mill. kr utbetales 12. november. Statlig rammetilskudd på 68 mill. kr utbetales 15. november. Estimert midlertidig kassakreditt-trekk i 3 dager: <strong>39.1 mill. kr</strong>.
      </div>
    </div>
  );
};
```
