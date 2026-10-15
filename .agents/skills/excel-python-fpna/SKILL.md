---
name: excel-python-fpna
description: >-
  Avansert finansiell modellering i Excel og Python, likviditetsprognoser, Monte Carlo-risikosimuleringer og FAST-standard.
---

# 📈 Agent Skill: Excel & Python FP&A Financial Modeling (`SKILL_EXCEL_PYTHON_FPNA`)

> **Versjon:** 1.0  
> **Kategori:** Financial Planning & Analysis (FP&A)  
> **Standard:** FAST Financial Modelling Standard & ICAEW Spreadsheet Practice Principles  

---

## 🎯 Formål
Dette agent-skill-et gir AI-assistenten kapasitet til å bygge, automatisere og kontrollere avanserte **Excel-modeller og Python-berikede regneark** for kommunal finansstyring, likviditetsprognoser, Monte Carlo-simuleringer og scenarieanalyser.

---

## 📐 Krav og Prinsipper (FAST & ICAEW Standard)

### 1. FAST-prinsippene
* **F - Flexible:** Modellen må enkelt kunne håndtere endringer i forutsetninger (f.eks. rentehopp, lønnsoppgjør, kommunedeflator).
* **A - Appropriate:** Strukturert oppsett uten overflødig kompleksitet.
* **S - Structured:** Strengt skille mellom **Input**, **Beregning (Calculation)** og **Rapport (Output)**.
* **T - Transparent:** Enkle, lesbare formler uten skjulte avhengigheter eller sammensatte hardkodede tall.

### 2. Python i Excel (Anaconda / OpenPyXL / Pandas)
Brukes til tunge statistiske beregninger, usikkerhetsanalyser og automatisert rapportgenerering:

```python
import pandas as pd
import numpy as np

def run_monte_carlo_budget_risk(n_simulations=10000, base_drift_exp=2_500_000_000):
    """Simulerer usikkerhet i pensjonskostnader og vikarforbruk."""
    np.random.seed(42)
    # Normale svingninger i lønnsvekst og vikarforbruk (stddev = 2.5%)
    drift_variations = np.random.normal(loc=1.0, scale=0.025, size=n_simulations)
    simulated_outcomes = base_drift_exp * drift_variations
    
    var_95 = np.percentile(simulated_outcomes, 95)
    p_deficit = np.mean(simulated_outcomes > (base_drift_exp * 1.02))
    
    return {
        "expected_mean": float(np.mean(simulated_outcomes)),
        "value_at_risk_95": float(var_95),
        "probability_of_deficit": float(p_deficit)
    }
```

### 3. Formatering for Negativer og Nytall
* **Negativt avvik (Underskudd / Merforbruk):** Formatert i rød farge med parentes: `#,##0;[Red](#,##0);"-"`.
* **Nullverdier:** Vises som tankestrekk (`"-"`) for renere visuell lesbarhet.

---

## 🛡️ Sjekkliste for Regnearkaudit (Model Check)
* [ ] Ingen hardkodede tall inne i beregningsformler.
* [ ] Ingen sirkulære referanser (*Circular references*).
* [ ] Dynamiske matriseformler (`XLOOKUP`, `LET`, `LAMBDA`, `FILTER`) benyttes i stedet for utdaterte `VLOOKUP`.
* [ ] Konsistente formler på tvers av alle rader i en tabell.
