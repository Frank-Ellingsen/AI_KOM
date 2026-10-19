# Power BI Reporting Package - Kristiansand Kommune (AI_KOM)

Dette er den komplette rapport- og datamodellpakken for **Power BI / Streamlit** i Kristiansand kommune (`AI_KOM`). 

Pakken dekker alle **6 Virksomhetsområder** og **81 organisatoriske enheter** med dynamiske slicere, DAX-måltall, RLS (Row-Level Security), EVM Monte Carlo-prognoser og EU AI Act SHA-256 revisjonsforsegling.

---

## 📁 Struktur i pakken

```
powerbi_md_package/
├── README.md                          # Hovedveileder og arkitekturoversikt
├── powerbi_data_model_spec.md         # Stjerneschema-spesifikasjon & RLS-regler
├── config/
│   └── dax_measures_catalog.md        # Komplett DAX-måltallskatalog & RAG-fargekoder
├── app.py                             # Interaktiv Power BI-stil Streamlit Dashboard App
├── data/
│   └── kristiansand_81_enheter.csv   # Komplett regnskapssett for 81 enheter (7,24 mrd. kr)
├── requirements.txt                   # Avhengigheter for lokal kjøring
└── tests/
    └── test_powerbi_dashboard.py      # Automatisert unittest-suite
```

---

## 🚀 Hurtigstart

1. Installer avhengigheter:
   ```bash
   pip install -r requirements.txt
   ```

2. Kjør Power BI Dashboardet (Streamlit):
   ```bash
   streamlit run app.py
   ```

3. Kjøre enhetstester:
   ```bash
   python -m unittest tests/test_powerbi_dashboard.py
   ```

---

## 🏛️ De 6 Virksomhetsområdene og 81 Enhetene

* **Oppvekst** (18 enheter – KOSTRA 202 Grunnskole, Barnehage)
* **Helse og mestring** (22 enheter – KOSTRA 253, 254 Sykehjem/Hjemmetjeneste, 256 Psykiatri)
* **Stedsutvikling** (12 enheter – KOSTRA 301 Plan/Bygg, Kart)
* **Kultur og innbyggerdialog** (10 enheter – KOSTRA 332 Kultur, Bibliotek)
* **Infrastruktur og miljø** (11 enheter – KOSTRA 340 Vei, Park, VAR)
* **Organisasjon og styring** (8 enheter – KOSTRA 100 Administrasjon, HR, Økonomi)

---

## 🛡️ Governance & Sikkerhet

* **OWASP ASI06 Spotlighting**: Skjerming av råtekst fra uautoriserte dokumenter.
* **GDPR Port 4 PII Scrubber**: Lokal maskering av fødselsnummer (11 siffer), kontonumre og e-poster.
* **EU AI Act Art. 14 Audit Ledger**: Hver godkjenning av saksnotat / avviksnotat genererer et cryptografisk **SHA-256 stempel** for Kommunerevisjonen.
