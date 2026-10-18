# 🏥 MVP — Helse og Mestring (Ansvar 5200 / KOSTRA 253, 254, 256)
## Kristiansand Kommune Control Office Hub (`AI_KOM`)

Dette er en spesialisert økonomistyrings- og Project Controlling-modul for sektoren **Helse og Mestring** (Ansvar 5200, årsramme **320,00 MNOK**) i Kristiansand kommune.

Løsningen kombinerer:
* **DuckDB OLAP & ISO 21508 Earned Value Management (EVM)**: Beregner periodisert YTD-budsjett ($\text{PV}$), kostnadsavvik ($\text{CV}$), kostnadsytelsesindeks ($\text{CPI}$), sluttprognose ($\text{EAC}$) og helårsavvik ($\text{VAC}$) på tvers av KOSTRA `253` (Hjemmesykepleie), `254` (Sykehjem/Helsehus) og `256` (Mestring/Psykiatri).
* **NAV-Refusjonsgap (Art 1600) & Bruttoprinsippet (§ 14-6)**: Avdekker uavstemte sykepengerefusjoner jf. *Folketrygdloven § 22-13* (3 mnd. foreldelsesfrist) og kontrollerer bruttoføring jf. *Kommuneloven § 14-6*.
* **Monte Carlo Q4-Sesongsimulator**: Simulerer 1 000 utfall (P10 / P50 / P90) for M9–M12 inkludert +5 % sesongmessig vintersykefravær.
* **Juridisk Beslutningsstøtte (§ 14-5 & HTA § 4 / AML § 10-12)**: Automatisk utkast til saksfremlegg med drøftingskrav mot tillitsvalgte ved turnusomlegging, langvakter (12,5t) og vikarpool.
* **Stage-Gate Port 4, Port 9 & Port 10**: Lokal PII-vask (FNR, D-nummer, kontonummer, telefon `+47` og e-post) og uforanderlig SQLite `Audit_AI_Actions`-revisjonslogg med SHA-256-forsegling (`APPROVED`, `MODIFIED`, `REJECTED`).

---

## 📁 Mappestruktur

```text
helse_og_mestring_mvp/
├── README.md                      ← Dokumentasjon, arkitektur og hurtigstart
├── app.py                         ← Streamlit Web-Dashboard (Tufte Data-Ink, DuckDB, EVM, SQLite Audit)
├── requirements.txt               ← Avhengigheter (streamlit, pandas, numpy, duckdb)
├── config/
│   └── dax_and_rag_rules.md       ← DAX/EVM-formler, Tufte RAG-fargekoder og §§ 14-5/14-6/HTA § 4 regler
├── data/
│   ├── helse_mestring_data.csv    ← Regnskaps- og budsjettdata for Ansvar 5200 (KOSTRA 253, 254, 256)
│   └── helse_mestring_audit.db    ← (Autogenerert) SQLite revisjonsdatabase (Audit_AI_Actions)
└── tests/
    └── test_helse_mestring_mvp.py ← Automatisert testpakke (8 enhets- og integrasjonstester)
```

---

## 🚀 Hvordan kjøre applikasjonen lokalt

### 1. Installer avhengigheter
```powershell
pip install -r requirements.txt
```

### 2. Start Streamlit Dashboard
```powershell
streamlit run app.py
```

### 3. Kjør enhetstestene
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```
