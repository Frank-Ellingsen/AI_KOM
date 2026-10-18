# MVP - Helse og Mestring (Ansvar 5200 / KOSTRA 254)
## Kristiansand Kommune Control Office Hub (AI_KOM)

Dette er en komplett MVP-pakke (Minimum Viable Product) skreddersydd for sektoren **Helse og Mestring** (Ansvar 5200) i Kristiansand kommune. Pakken kombinerer lokal PII-skjerming, KOSTRA 254 underfunksjonsanalyse, NAV-refusjonsgap (art 1600), Monte Carlo-prognoser for Q4-sykefravær, samt juridisk saksfremlegg jf. *Kommuneloven § 14-5* og revisjonsgodkjenning (EU AI Act Art. 14).

---

## 📁 Mappestruktur

```
helse_og_mestring_mvp/
├── README.md                      ← Denne filen (Dokumentasjon og hurtigstart)
├── app.py                         ← Streamlit Web-Dashboard for Helse og Mestring
├── requirements.txt               ← Avhengigheter (streamlit, pandas, numpy, duckdb)
├── config/
│   └── dax_and_rag_rules.md       ← DAX-formler, RAG-fargekoder og Kommuneloven-prompter
├── data/
│   └── helse_mestring_data.csv    ← Detaljerte regnskapsdata for Ansvar 5200 (M1–M8)
└── tests/
    └── test_helse_mestring_mvp.py ← Automatisert enhetstestsuite (unittest)
```

---

## 🚀 Hvordan kjøre applikasjonen lokalt

### 1. Installer avhengigheter
```bash
pip install -r requirements.txt
```

### 2. Start Streamlit Dashboard
```bash
streamlit run app.py
```

### 3. Kjør enhetstestene
```bash
python -m unittest tests/test_helse_mestring_mvp.py
```

---

## 🔑 Hovedfunksjoner i MVP-en

1. **Port 4 Local PII Scrubber**: Skjermer fødselsnumre (11 siffer), kontonumre og pasientinformasjon lokalt før AI-behandling.
2. **KOSTRA 254 Sub-funksjonsanalyse**: Oppsplitting på 253 (Hjemmesykepleie), 254 (Sykehjem/Helsehus) og 256 (Mestring/Psykiatri).
3. **NAV Refusjonsgap (Art 1600)**: Identifiserer uavstemte sykepengerefusjoner fra NAV jf. Folketrygdloven § 22-13.
4. **Monte Carlo Volatilitetssimulator**: Simulering av Q4-sykefravær og vikarutgifter (Art 1090/1100).
5. **Stage-Gate Port 9 & SHA-256 Revisorstempel**: Menneskelig godkjenning med kryptografisk forsegling for Kommunerevisjonen.
