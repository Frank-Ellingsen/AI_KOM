# 🐍 Python in Excel & Microsoft Copilot Integrasjonsarkitektur

**Virksomhetsområde:** Økonomi og Virksomhetsstyring, Kristiansand kommune  
**Teknologi:** Python in Excel (Anaconda Cloud/Local Kernel), Microsoft Copilot for Excel  

---

## 1. Python in Excel (Py-funksjonen)

Python i Excel kjører direkte i cellene via `=PY(...)` og gir tilgang til Pandas, NumPy, SciPy og Statsmodels for avansert tidsrekkeanalyse.

### Eksempel: Månedlig Avviks- & Trendprognose via Pandas

```python
# Kjøres i Excel-celle via =PY()
import pandas as pd
import numpy as np

# Hent data fra Excel-tabellen "VismaRegnskap"
df = xl("VismaRegnskap[#All]", headers=True)

# Beregn hittil-i-år (YTD) og rullende 3-måneders snitt
df['YTD_Avvik'] = df['Regnskap_YTD'] - df['Budsjett_YTD']
df['Rullende_Snitt'] = df['Regnskap_Måned'].rolling(window=3).mean()

# Fremskriv EOY per enhet
df['EOY_Prognose'] = df['Regnskap_YTD'] + (df['Rullende_Snitt'] * (12 - df['Måned_Nr'].max()))

# Returner kun enheter med kritisk merforbruk > 500,000 kr
kritiske_enheter = df[df['EOY_Prognose'] - df['Budsjett_År'] > 500000]
kritiske_enheter[['Enhet_Navn', 'YTD_Avvik', 'EOY_Prognose']]
```

---

## 2. Copilot & Generativ AI i Excel

1. **Prompt-mal for Avviksdiagnose:**
   > *"Analyser kolonnen 'YTD_Avvik' mot 'Vikarutgifter_Art1020'. Identifiser de 5 enhetene der vikarforbruk utgjør mer enn 60 % av det totale merforbruket, og lag en oppsummering for Kommunalsjef."*

2. **Automatisert Formelgenerering:**
   Copilot benyttes til å bygge avanserte dynamiske matriseformler med `=LET()` for å hindre ytelsestap i store modeller.
