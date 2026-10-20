# 🏛️ Kristiansand Kommune — Control Office Hub (AI_KOM)

AI_KOM er en agentisk beslutningsstøtte- og økonomirådgivermodell bygget for Helse og Mestring i Kristiansand kommune. Systemet kombinerer eksakte SQL-spørringer mot ERP-transaksjoner, Grounded RAG-oppslag i kommunale styringsdokumenter og tertialrapporter, månedlig avviksanalyse med RAG-trafikklys (🟢, 🟡, 🔴), Financial Times Visual Vocabulary, prediktive EOY-årsprognoser og automatiske forslag til balansetiltak (§ 14-5).

---

## 📁 Prosjektstruktur

AI_KOM/
├── README.md                     # Hoveddokumentasjon
├── index.html                    # GitHub Pages portal for Antigravity
├── Dockerfile                    # Container-oppsett
├── docker-compose.yml            # Kjøreoppsett ('docker compose up --build')
├── .dockerignore
├── .env.example                  # Mal for API-nøkler
├── requirements.txt              # Python-avhengigheter
│
├── docs/                         # Spesialisert dokumentasjon
│   ├── ARCHITECTURE.md           # 6-Nivås budsjetthierarki, RAG/SQL & Loop Engineering
│   ├── PILOT_MANDATE.md          # Prosjektmandat, saksframlegg & KPI-matrise
│   └── ANTIGRAVITY_INSTRUCTIONS.md # Utviklingsguide for Antigravity AI Agent
│
└── app/                          # Kildekode
    ├── __init__.py
    ├── schemas.py                # Pydantic v2 datakontrakter, RBAC & AuditLog
    ├── tools.py                  # Parameterisert SQL, RAG, EOY, Omdisponering & Audit
    ├── agent.py                  # Agentorkestrering (Gemini 2.0 Flash)
    ├── build_rag_index.py        # Bygger SQLite-database og RAG-vektorindeks
    └── frontend.py               # Streamlit web-grensesnitt (7 interaktive faner)

---

## 🚀 Oppstart med Docker

```bash
# 1. Opprett .env-fil med dine API-nøkler
cp .env.example .env

# 2. Start applikasjonen
docker compose up --build
```
