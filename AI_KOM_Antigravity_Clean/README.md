# 🏛️ Kristiansand Kommune — AI Økonomirådgiver & Control Office Hub

En agentisk AI-beslutningsstøttemodell for helhetlig kommunal økonomistyring i Kristiansand kommune (spesielt tilpasset Helse og Mestring). Systemet kombinerer eksakte SQL-spørringer mot ERP-transaksjoner, Grounded RAG-søk i kommunale styringsdokumenter, månedlig avviksanalyse med RAG-trafikklys, Financial Times Visual Vocabulary, prediktiv årsprognose (EOY), preskriptive balansetiltak (Kommuneloven § 14-5), rollestyring (RBAC) og uforanderlig revisjonslogg jf. arkivlova.

---

## 📁 Prosjektstruktur

```text
AI_KOM/
├── .env.example                  # Mal for API-nøkler (GEMINI_API_KEY, SERPER_API_KEY)
├── Dockerfile                    # Produksjonsklar Docker-containerisering
├── docker-compose.yml            # Kjøreoppsett med 'docker compose up --build'
├── .dockerignore                 # Docker ekskluderingsregler
├── requirements.txt              # Nødvendige Python-pakker
├── README.md                     # Hoveddokumentasjon (Dette dokumentet)
├── index.html                    # GitHub Pages portal / landingpage for Antigravity
│
├── docs/                         # Utvidet dokumentasjon
│   ├── ARCHITECTURE.md           # Systemarkitektur & Multi-Agent LangGraph Veikart
│   ├── PILOT_MANDATE.md          # Prosjektmandat, saksframlegg & KPI-matrise
│   └── ANTIGRAVITY_INSTRUCTIONS.md # Prompting- og utviklingsguide for Antigravity
│
└── app/                          # Konsolidert kildekode
    ├── __init__.py
    ├── schemas.py                # Pydantic v2 datakontrakter, RBAC & AuditLog
    ├── tools.py                  # SQL, RAG, EOY, Omdisponering & Audit-funksjoner
    ├── agent.py                  # Agentorkestrering (Gemini 2.0 Flash)
    ├── build_rag_index.py        # Bygger SQLite-database og RAG-vektorindeks
    └── frontend.py               # Streamlit web-grensesnitt (7 interaktive faner)
```

---

## 🚀 Oppstart og Kjøring

### Alternativ A: Kjøring med Docker (Anbefalt)
```bash
# 1. Klone repositoryet og opprett .env
cp .env.example .env

# 2. Start hele løsningen i container
docker compose up --build
```
Åpne nettleseren på `http://localhost:8501`.

### Alternativ B: Lokal Python-kjøring
```bash
# 1. Installér avhengigheter
pip install -r requirements.txt

# 2. Sett API-nøkkel
export GEMINI_API_KEY="din-gemini-api-nøkkel"

# 3. Bygg database og indeksér dokumenter
python app/build_rag_index.py

# 4. Start Streamlit Dashboard
python -m streamlit run app/frontend.py
```

---

## 📊 De 7 Dashbord-fanene i Streamlit

1. **💬 AI-Økonomirådgiver**: Direkte interaktiv dialog med agenten for komplekse spørringer.
2. **📊 Månedlig Rapport & Trafikklys**: Automatisk beregning av avvik og status (🟢 Grønn, 🟡 Gul, 🔴 Rød).
3. **📈 FT Visual Vocabulary**: Grafisk visualisering tilpasset Financial Times' standarder.
4. **🔮 EOY Prognose & Lønnsbudsjett**: Prediktiv årsprognose for lønn, overtid, AGA og pensjon.
5. **🔍 6-Nivås Drill-Down**: Fra sektornivå helt ned til laveste transaksjonsbilag.
6. **🔄 Omdisponering & Eskalering**: Automatisk sjekk av fullmaktsgrenser jf. Kommuneloven § 14-5.
7. **📜 Audit-Logg (Revisorvisning)**: Uforanderlig endringslogg for Kommunerevisjonen (NKRF) og Kontrollutvalget.

---

## 🏛️ Livssyklus og Stage-Gate Framework

Prosjektet følger en 5-faset utviklingsmodell:
* **Fase 1 (Uke 1–4):** Pydantic v2 schemas & verktøykontrakter.
* **Fase 2 (Uke 5–8):** Grounded RAG & SQL-integrasjon.
* **Fase 3 (Uke 9–12):** Agentorkestrering, RBAC & Audit Trail.
* **Fase 4 (Uke 13–16):** Production, Docker & GitHub Packaging.
* **Fase 5 (Videre drift):** Day-2 Operations, Continuous Evals (Langfuse) & Multi-Agent LangGraph undergrafer.
