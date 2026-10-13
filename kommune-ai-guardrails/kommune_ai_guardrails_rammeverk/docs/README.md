# 🏛️ Kommune AI Guardrails — Rammeverk for Kommunal AI & RAG

> **Et modulært, generisk og sikkert rammeverk for lokal AI-styring, hybrid RAG (Retrieval-Augmented Generation) og etterrettelig beslutningsstøtte i kommunesektoren.**

---

## 📌 Formål og Generelt Bruksområde

**Kommune AI Guardrails** er utformet som en fleksibel, gjenbrukbar og produksjonsklar arkitektur for kommunale virksomheter. Rammeverket gjør det mulig å ta i bruk store språkmodeller (LLM-er) og avanserte søkesystemer (RAG) på tvers av ulike fagområder (økonomi, byggesak, helse og omsorg, oppvekst, HR/rekruttering) uten å gå på kompromiss med personvern, datasikkerhet eller juridiske krav.

Systemet kjører **100 % lokalt** (via Ollama og SQLite-vec), krever ingen deling av sensitive data med eksterne skytjenester, og overholder kravene i **EU AI Act**, **GDPR**, **Kommuneloven** og **Offentleglova**.

---

## 🧱 Prosjektstruktur

```text
kommune-ai-guardrails/
├── app/                        # Web-grensesnitt og CLI
│   ├── app.py                  # Interaktiv Streamlit AI-assistent og Audit-portal (med auto-launcher)
│   └── main.py                 # Frittstående CLI-runner
├── config/                     # Konfigurasjonsfiler
│   ├── config.yaml             # Modeller, stier og hybride søkeparametere
│   └── system_prompts.yaml     # Glass-box systeminstrukser
├── data/                       # Datastyring og oppbevaring
│   ├── db/                     # SQLite-vektordatabase (sqlite-vec + FTS5)
│   ├── processed/              # Vaskede og strukturerte tekster/chunks
│   └── raw/                    # Rå kildedokumenter (.pdf, .csv, .md)
├── src/                        # Kildekode (Kjernefunksjonalitet)
│   └── kommune_ai_guardrails/
│       ├── config.py           # Konfigurasjonsstyring og miljøvariabler
│       ├── ingest.py           # Paragraf-chunking og vektorgenerering
│       └── rag.py              # Hybridsøk (BM25 + sqlite-vec), PII-skjerming & SHA-256 audit
├── docs/                       # Dokumentasjonsarkiv
│   ├── STAGE_GATE_FRAMEWORK.md # Kommunal portmodell for AI-styring
│   ├── RAG_ARCHITECTURE_SPEC.md# Teknisk RAG-spesifikasjon
│   ├── SKILLS_AND_TOOLS_CATALOG.md # AI Skills, Tools & Guardrails
│   ├── USER_GUIDE_SOP.md       # Brukerveiledning og SOP
│   └── DEVELOPER_SETUP_GUIDE.md# Utvikler- og oppsettsveileder
├── tests/                      # Enhetstester og verifisering
├── requirements.txt            # Python-avhengigheter
└── README.md                   # Hoveddokumentasjon
```

---

## 🚀 Hurtigstart (Quickstart)

### 1. Forutsetninger
* Python 3.10+
* Ollama installert lokalt (`ollama pull llama3.1` eller `qwen2.5`)

### 2. Installasjon
```powershell
# Klone og naviger til prosjekt
cd kommune-ai-guardrails

# Opprett virtuelt miljø
python -m venv venv
.\\venv\\Scripts\\Activate.ps1

# Installer avhengigheter
pip install -r requirements.txt
```

### 3. Bygg vektordatabase (Ingestion)
```powershell
python src/kommune_ai_guardrails/ingest.py
```

### 4. Start Web-App (Streamlit)
```powershell
# Kan startes direkte med Streamlit CLI eller ren Python:
streamlit run app/app.py
# eller: python app/app.py
```

---

## 🛡️ Hovedprinsipper for Kommunal AI

1. **100 % Lokalt Personvern:** Ingen følsomme data eller spørringer sendes ut av kommunens eget nettverk.
2. **Kildestyrt Forankring (Zero Hallucination):** Svar genereres utelukkende basert på bekreftede kildedokumenter med eksakte §-sitater.
3. **Uforanderlig Audit Log (Stage-Gate Port 9):** Alle spørringer, kilde-chunks og svar signeres med SHA-256 for Kommunerevisjonen.
4. **Menneskelig Kontroll (Human-in-the-Loop):** AI gir kun rådgivende beslutningsstøtte — saksbehandler har det fulle ansvar for alle vedtak.
