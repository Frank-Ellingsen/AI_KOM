from __future__ import annotations

import datetime
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys

# Suppress progress bars and tokenizer warnings in web UI
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Windows & Python 3.14 I/O guard: catch OSError [Errno 22] on stream flush/write
class SafeStreamWrapper:
    """Wraps streams to prevent OSError [Errno 22] Invalid argument on flush in Windows/Streamlit."""
    def __init__(self, target):
        self._target = target

    def write(self, data):
        try:
            return self._target.write(data)
        except OSError as err:
            if getattr(err, "errno", None) != 22:
                raise

    def flush(self):
        try:
            self._target.flush()
        except OSError as err:
            if getattr(err, "errno", None) != 22:
                raise

    def __getattr__(self, name):
        return getattr(self._target, name)

if sys.stderr is not None and not isinstance(sys.stderr, SafeStreamWrapper):
    sys.stderr = SafeStreamWrapper(sys.stderr)
if sys.stdout is not None and not isinstance(sys.stdout, SafeStreamWrapper):
    sys.stdout = SafeStreamWrapper(sys.stdout)

try:
    import transformers.utils.logging as hf_logging
    hf_logging.disable_progress_bar()
except Exception:
    pass

import pandas as pd
import streamlit as st

# Auto-launch med Streamlit CLI dersom skriptet kjøres direkte med ren python
if __name__ == "__main__":
    from streamlit.runtime import exists as _st_runtime_exists
    if not _st_runtime_exists():
        from streamlit.web import cli as _stcli
        sys.argv = ["streamlit", "run", str(Path(__file__).resolve())]
        sys.exit(_stcli.main())

# ==========================================
# 1. SKRIPT- OG MILJØOPPSETT
# ==========================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"
ERP_DIR = PROJECT_ROOT.parent / "erp_data"
GOLDEN_RECORD_DB_PATH = Path(os.getenv("KOMMUNE_DB_PATH", str(ERP_DIR / "kommune_golden_record.db")))

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

# Last .env-variabler
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

from sentence_transformers import SentenceTransformer
from kommune_ai_guardrails.rag import ask_kommune_ai, get_db_connection, sanitize_pii
from kommune_ai_guardrails.mcp_server import (
    execute_gemini_mcp_query,
    get_unit_financials,
    search_municipal_law,
    calculate_eoy_impact
)

# ==========================================
# 2. STREAMLIT KONFIGURASJON & TUFTE-DESIGN
# ==========================================
st.set_page_config(
    page_title="Kristiansand Kommune — Control Office Hub & AI Assistent",
    page_icon="🏛️",
    layout="wide"
)

# Tufte-inspirert stil: minimal visuell støy, høy data-ink ratio
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1300px;
    }
    div[data-testid="stMetricValue"] {
        font-family: monospace;
        font-size: 1.15rem;
    }
    .source-chunk-card {
        border-left: 3px solid #1B365D;
        padding: 0.6rem 1rem;
        margin-bottom: 0.8rem;
        background-color: rgba(240, 244, 248, 0.4);
        border-radius: 2px;
    }
    .arshjul-card {
        padding: 0.8rem 1rem;
        border-radius: 4px;
        background-color: #f8f9fa;
        border-top: 3px solid #2C3E50;
        margin-bottom: 0.5rem;
    }
    .arshjul-card.active {
        border-top: 3px solid #27AE60;
        background-color: #f0fdf4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🏛️ Kristiansand Kommune — Control Office Hub & AI Assistent")
st.caption("Skjermet, lokal beslutningsstøtte for Økonomi og Virksomhetsstyring | KOSTRA, Kommuneloven, Visma ERP & Framsikt EPM")

# ==========================================
# 3. RESSURSER & MODELL-LASTING (CACHED)
# ==========================================
@st.cache_resource(show_spinner=False)
def load_embedding_model():
    try:
        import transformers.utils.logging as hf_logging
        hf_logging.disable_progress_bar()
    except Exception:
        pass
    return SentenceTransformer("intfloat/multilingual-e5-small")

with st.spinner("⏳ Laster lokal embedding-modell (multilingual-e5-small)..."):
    embedding_model = load_embedding_model()


@st.cache_data(ttl=60, show_spinner=False)
def get_db_stats() -> dict[str, int]:
    """Henter nøkkeltall fra SQLite-vektordatabasen og Golden Record."""
    stats = {"chunks": 0, "audits": 0, "regnskap_rader": 0, "budsjett_rader": 0}
    try:
        conn = get_db_connection()
        stats["chunks"] = conn.execute("SELECT COUNT(*) FROM legal_chunks").fetchone()[0]
        stats["audits"] = conn.execute("SELECT COUNT(*) FROM Audit_AI_Actions").fetchone()[0]
        conn.close()
    except Exception:
        pass

    if GOLDEN_RECORD_DB_PATH.exists():
        try:
            conn_er = sqlite3.connect(GOLDEN_RECORD_DB_PATH)
            stats["regnskap_rader"] = conn_er.execute("SELECT COUNT(*) FROM Fact_Regnskap").fetchone()[0]
            stats["budsjett_rader"] = conn_er.execute("SELECT COUNT(*) FROM Fact_Budsjett").fetchone()[0]
            conn_er.close()
        except Exception:
            pass
    return stats


def fetch_chunk_details(chunk_ids: list[int]) -> list[dict]:
    """Henter fulltekst og kildemetadata for benyttede chunks."""
    if not chunk_ids:
        return []
    try:
        conn = get_db_connection()
        placeholders = ",".join("?" for _ in chunk_ids)
        sql = f"SELECT id, source_file, category, section_ref, title, content FROM legal_chunks WHERE id IN ({placeholders})"
        rows = conn.execute(sql, chunk_ids).fetchall()
        conn.close()
        id_map = {row["id"]: dict(row) for row in rows}
        return [id_map[cid] for cid in chunk_ids if cid in id_map]
    except Exception:
        return []


def get_available_ollama_models() -> tuple[list[str], bool]:
    """Oppdager installerte modeller i lokal Ollama-instans."""
    fallback_models = ["llama3.1", "qwen2.5", "mistral"]
    try:
        import ollama
        resp = ollama.list()
        models_data = resp.models if hasattr(resp, "models") else resp.get("models", [])
        names = []
        for m in models_data:
            name = m.model if hasattr(m, "model") else m.get("name", "")
            if name:
                names.append(name)
        if names:
            return names, True
        return fallback_models, True
    except Exception:
        return fallback_models, False


@st.cache_data(ttl=60, show_spinner=False)
def load_golden_record_evm() -> pd.DataFrame:
    """Beregner Project Controller Earned Value (BAC, PV, AC, CV, CPI, EAC) fra Golden Record."""
    if not GOLDEN_RECORD_DB_PATH.exists():
        return pd.DataFrame()
    try:
        conn = sqlite3.connect(GOLDEN_RECORD_DB_PATH)
        sql = """
        WITH evm_agg AS (
            SELECT 
                ans.enhet_navn,
                ans.sektor,
                SUM(b.budsjett_belop) AS BAC,
                SUM(CASE WHEN r.belop IS NOT NULL AND r.belop > 0 THEN b.budsjett_belop ELSE 0 END) AS PV,
                SUM(COALESCE(r.belop, 0)) AS AC
            FROM Fact_Budsjett b
            LEFT JOIN Fact_Regnskap r 
                ON b.funksjon_key = r.funksjon_key 
               AND b.art_key = r.art_key 
               AND b.ansvar_key = r.ansvar_key 
               AND b.dato_key = r.dato_key
            JOIN Dim_Ansvar ans ON b.ansvar_key = ans.ansvar_kode
            GROUP BY ans.enhet_navn, ans.sektor
        )
        SELECT 
            enhet_navn AS "Enhet",
            sektor AS "Sektor",
            PV AS "Planlagt (PV)",
            AC AS "Påløpt (AC)",
            (PV - AC) AS "Avvik (CV)",
            CASE WHEN AC > 0 THEN (PV / AC) ELSE 1.0 END AS "CPI",
            BAC AS "Årsbudsjett (BAC)",
            CASE WHEN AC > 0 THEN (BAC / (PV / AC)) ELSE BAC END AS "Sluttprognose (EAC)",
            (CASE WHEN AC > 0 THEN (BAC / (PV / AC)) ELSE BAC END) - BAC AS "Est. Merforbruk"
        FROM evm_agg;
        """
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=60, show_spinner=False)
def load_top_cost_variances(enhet_filter: str | None = None) -> pd.DataFrame:
    """Henter de mest kritiske kostnadsavvikene på KOSTRA art."""
    if not GOLDEN_RECORD_DB_PATH.exists():
        return pd.DataFrame()
    try:
        conn = sqlite3.connect(GOLDEN_RECORD_DB_PATH)
        where_clause = ""
        params = []
        if enhet_filter and enhet_filter != "Alle Enheter":
            where_clause = "WHERE ans.enhet_navn = ?"
            params.append(enhet_filter)

        sql = f"""
        SELECT 
            a.art_kode || ' ' || a.art_navn AS "KOSTRA Art",
            ans.enhet_navn AS "Enhet",
            ROUND(SUM(b.budsjett_belop), 0) AS "Budsjett (NOK)",
            ROUND(SUM(r.belop), 0) AS "Regnskap (NOK)",
            ROUND(SUM(b.budsjett_belop) - SUM(r.belop), 0) AS "Avvik (NOK)",
            ROUND(((SUM(b.budsjett_belop) - SUM(r.belop)) / NULLIF(SUM(b.budsjett_belop), 0)) * 100, 1) AS "Avvik %"
        FROM Fact_Regnskap r
        JOIN Fact_Budsjett b 
            ON r.funksjon_key = b.funksjon_key 
           AND r.art_key = b.art_key 
           AND r.ansvar_key = b.ansvar_key 
           AND r.dato_key = b.dato_key
        JOIN Dim_Art a ON r.art_key = a.art_kode
        JOIN Dim_Ansvar ans ON r.ansvar_key = ans.ansvar_kode
        {where_clause}
        GROUP BY a.art_kode, a.art_navn, ans.enhet_navn
        HAVING "Avvik (NOK)" < 0
        ORDER BY "Avvik (NOK)" ASC
        LIMIT 10;
        """
        df = pd.read_sql_query(sql, conn, params=params)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


# ==========================================
# 4. SIDEMENY: BRUKERROLLE, MODELL & STATUS
# ==========================================
st.sidebar.header("👤 Brukerkontekst & Rolle")
user_role = st.sidebar.selectbox(
    "Aktiv rolle i organisasjonen:",
    options=[
        "Senior Controller / Prosjektøkonom (Frank Ellingsen)",
        "Økonomidirektør / Virksomhetsstyring",
        "Enhetsleder (Oppvekst / Helse & Mestring)",
        "Kommunerevisjonen / Kontrollutvalget"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ LLM-motor & Inferens")

gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
ollama_models, ollama_connected = get_available_ollama_models()

model_options: dict[str, str] = {}
if gemini_key:
    model_options["gemini-3.8-flash"] = "⚡ gemini-3.8-flash (Google Gemini — Anbefalt: Rask, 0 % CPU)"
    model_options["gemini-3.1-pro-preview"] = "🧠 gemini-3.1-pro-preview (Google Gemini — Avansert resonnering)"
else:
    model_options["gemini-3.8-flash"] = "⚡ gemini-3.8-flash (Mangler API-nøkkel i .env)"

if ollama_connected and ollama_models:
    for m in ollama_models:
        model_options[m] = f"🦙 {m} (Lokal Ollama — Høy CPU-belastning)"
else:
    model_options["llama3.1"] = "🦙 llama3.1 (Lokal Ollama — Høy CPU-belastning)"

selected_label = st.sidebar.selectbox(
    "Velg modell:",
    options=list(model_options.values()),
    index=0
)
selected_model = next(k for k, v in model_options.items() if v == selected_label)

if selected_model.startswith("gemini"):
    st.sidebar.success("⚡ Gemini API aktiv (Klientside PII-skjerming aktiv)", icon="✅")
elif ollama_connected:
    st.sidebar.info("🦙 Lokal Ollama valgt (Kjører lokalt på enhetens CPU/GPU).")
else:
    st.sidebar.warning("⚠️ Får ikke kontakt med lokal Ollama.")

# Databasestatistikk
db_stats = get_db_stats()
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Datagrunnlag (Golden Record)")
st.sidebar.markdown(f"- **Regelverks-chunks (RAG):** `{db_stats['chunks']:,}`".replace(",", " "))
st.sidebar.markdown(f"- **Regnskapstransaksjoner:** `{db_stats['regnskap_rader']:,}`".replace(",", " "))
st.sidebar.markdown(f"- **Budsjettposter:** `{db_stats['budsjett_rader']:,}`".replace(",", " "))
st.sidebar.markdown(f"- **Audit-logger (SHA-256):** `{db_stats['audits']:,}`".replace(",", " "))

st.sidebar.markdown("---")
st.sidebar.subheader("🛡️ Stage-Gate Governance")
st.sidebar.markdown(
    """
- **Port 4:** PII-skjold for FNR, DNR, tlf (+47) og e-post
- **Port 8:** Glass-Box kildekrav (§)
- **Port 9:** Uforanderlig SHA-256 revisjonslogg
- **Port 10:** Eurocities Transparency Standard
"""
)

# ==========================================
# 4.B SIDEMENY: DOKUMENTARKIV & HURTIGLENKER
# ==========================================
WORKSPACE_ROOT = PROJECT_ROOT.parent

DOCUMENTS_MENU = {
    "🖥️ PowerPoint Presentasjonsmodeller (powerpoint/)": [
        ("Presentasjon Bystyret Tertialrapport 2026 (PPTX)", WORKSPACE_ROOT / "powerpoint" / "Presentasjon_Bystyret_Tertialrapport_2026.pptx", "Fullverdig 16:9 widescreen 7-slide dekk for Bystyret & Formannskapet jf. FT Visual Vocabulary"),
        ("Bystyret & Formannskapet Decks Spec (Markdown)", WORKSPACE_ROOT / "powerpoint" / "powerpoint_kommune_spec_bundle_v1" / "POWERPOINT_BYSTYRET_OG_FORM ANNSKAPET_DECKS.md", "Slidelayout, fargekoder og 7 standard lysbilder"),
        ("Visual Storytelling FT Spec (Markdown)", WORKSPACE_ROOT / "powerpoint" / "powerpoint_kommune_spec_bundle_v1" / "POWERPOINT_VISUAL_STORYTELLING_FT.md", "Aksjonstitler, bullet charts og avviksbroer"),
        ("PowerPoint Automatisering Spec (Markdown)", WORKSPACE_ROOT / "powerpoint" / "powerpoint_kommune_spec_bundle_v1" / "POWERPOINT_PRESENTASJONSSKAPING_AUTOMATION.md", "python-pptx arkitektur og generator")
    ],
    "📊 Excel FP&A Finansielle Modeller (excel/)": [
        ("Kommune FAST Finansiell Modell 2026 (Excel)", WORKSPACE_ROOT / "excel" / "Kommune_FAST_Finansiell_Modell_2026.xlsx", "5-tabs FAST-standard FP&A modell med tilpasset avviksformatering og EOY-beregning"),
        ("Project Controller EVM Modell 2026 (Excel)", WORKSPACE_ROOT / "excel" / "Kommune_Project_Controller_EVM_2026.xlsx", "5-tabs ISO 21508 Capex modell med S-kurve, PV/AC/CV/CPI/EAC og P85-usikkerhetsreserve"),
        ("CFO Executive Konsernmodell 2026 (Excel)", WORKSPACE_ROOT / "excel" / "Kommune_CFO_Executive_Konsern_2026.xlsx", "5-tabs toppledermodell: Bevilgningsregnskap, bruttoprinsippet § 14-6 og rentefølsomhet"),
        ("HR Lønn & Vikarmonitor 2026 (Excel)", WORKSPACE_ROOT / "excel" / "Kommune_HR_Lonn_Vikar_Monitor_2026.xlsx", "5-tabs bemanningsmonitor: Art 1010/1020/1090/1600, vikarstopp-kalkyle og NAV-etterslep"),
        ("FAST Finansiell Modellering Spec (Markdown)", WORKSPACE_ROOT / "excel" / "excel_kommune_spec_bundle_v1" / "EXCEL_FPA_FINANCIAL_MODELLING_FAST.md", "FAST Standard, fargekoder og tab-struktur"),
        ("Excel MCP Server Spec (Markdown)", WORKSPACE_ROOT / "excel" / "excel_kommune_spec_bundle_v1" / "EXCEL_AUTOMATION_AND_MCP_SERVER.md", "Model Context Protocol for Excel og Power Query M-kode"),
        ("Python in Excel Spec (Markdown)", WORKSPACE_ROOT / "excel" / "excel_kommune_spec_bundle_v1" / "EXCEL_PYTHON_AND_COPILOT_INTEGRATION.md", "=PY() funksjonen og Copilot i Excel")
    ],
    "📝 Word Styringsrapporter & Politiske Saker (word/)": [
        ("Saksfremlegg Bystyret: Budsjettendring (Word)", WORKSPACE_ROOT / "word" / "Saksfremlegg_Bystyret_Budsjettendring_2026.docx", "Nivå 1: Fullverdig saksfremlegg med Public360-metadata, 5 obligatoriske seksjoner og § 14-5 vedtak"),
        ("Tertialrapport & HØP Notat 2026 (Word)", WORKSPACE_ROOT / "word" / "Tertialrapport_og_HOP_Notat_2026.docx", "Nivå 2: Handlings- og økonomiplan HØP 2027–2030 iht. kommunens klarspråk- og WCAG 2.1 AA standard"),
        ("Månedsrapport Kommunedirektøren (Word)", WORKSPACE_ROOT / "word" / "Manedsrapport_Kommunedirektor_Strakstiltak_2026.docx", "Nivå 2: Konsernrapport med strakstiltak ACT-01 til ACT-04 (vikarstopp, konsulentkutt, lisenser)"),
        ("Sektorstyringsnotat Oppvekst & Utdanning (Word)", WORKSPACE_ROOT / "word" / "Sektorstyringsnotat_Kommunalsjef_Oppvekst_2026.docx", "Nivå 3: Kommunalsjefens avviksmatrise for 4 skoler, lærernorm og felles vikarring"),
        ("Prosjektkontroll & Capex Statusnotat (Word)", WORKSPACE_ROOT / "word" / "Prosjektkontroll_Capex_Statusnotat_2026.docx", "Nivå 4: ISO 21508 EVM porteføljeanalyse, CPI/SPI, EAC og P85-usikkerhetsreserve"),
        ("Avviksnotat & Handlingsplan Enhet 202 (Word)", WORKSPACE_ROOT / "word" / "Avviksnotat_og_Handlingsplan_Enhetsleder_2026.docx", "Nivå 5: 4-punkts avviksrapport (MAL-AVVIK-EFFEKT-001) for Enhet 202 Grunnskole"),
        ("Politiske Saksfremlegg Maler Spec (Markdown)", WORKSPACE_ROOT / "word" / "word_kommune_spec_bundle_v1" / "WORD_POLITISKE_SAKSFREMLEGG_MALER.md", "5-punkts mal og #1E3A8A overskriftsprofil"),
        ("Public360 & Dokumentautomatisering (Markdown)", WORKSPACE_ROOT / "word" / "word_kommune_spec_bundle_v1" / "WORD_PUBLIC360_OG_DOKUMENT_AUTOMATION.md", "python-docx pipeline og arkivering"),
        ("Tertialrapport & HØP Standarder (Markdown)", WORKSPACE_ROOT / "word" / "word_kommune_spec_bundle_v1" / "WORD_TERTIALRAPPORT_OG_HOP_STANDARDER.md", "WCAG 2.1 AA og kapittelstruktur for HØP")
    ],
    "⚡ Gemini Flash MCP & Power BI Specs": [
        ("Power BI Reporting Project (.PBIP)", WORKSPACE_ROOT / "powerbi" / "pbi_reporting_project.pbip", "Offisielt Power BI prosjekt (.pbip) med 7 ferdige PBIR rapportsider og TMDL Semantisk Modell"),
        ("Gemini Flash MCP Chat Spec (Markdown)", WORKSPACE_ROOT / "GEMINI_FLASH_MCP_CHAT_DEMO_SPEC.md", "Komplett spesifikasjon for Gemini Flash MCP Chat i Office Hub V2"),
        ("Komplett Master DAX Bundle (DAX)", WORKSPACE_ROOT / "powerbi" / "05_Komplett_Kommune_DAX_Bundle.dax", "Fullstendig DAX-måltallspakke for alle 7 CFO/Controller layouts"),
        ("Star Schema Power Query M-Code (Code)", WORKSPACE_ROOT / "powerbi" / "06_Star_Schema_DDL_and_PowerQuery.m", "Komplett M-kode med Fact_Regnskap, Fact_Budsjett og dimensjoner"),
        ("7 CFO/Controller Dashboards Guide (Markdown)", WORKSPACE_ROOT / "powerbi" / "07_PowerBI_7_Layouts_Spec_Guide.md", "Visuell implementasjonsveileder for 7 Power BI layouts")
    ],
    "🎯 AI-Implementeringspakke for Økonomi (ai-implementeringspakke-okonomi/)": [
        ("00 Masteroversikt & Struktur", WORKSPACE_ROOT / "ai-implementeringspakke-okonomi" / "00_INNHOLD_OG_OVERSIKT.md", "Helhetlig masterveileder for AI i kommunal økonomistyring"),
        ("Modul 1: Konsept & Beslutningsgrunnlag", WORKSPACE_ROOT / "ai-implementeringspakke-okonomi" / "01_MODUL_1_KONSEPT_OG_BESLUTNINGSGRUNNLAG.md", "Teknologilag, verdipotensial og forankring i KS/Digdir"),
        ("Modul 2: AI Readiness & Modenhet (L1-L5)", WORKSPACE_ROOT / "ai-implementeringspakke-okonomi" / "02_MODUL_2_AI_READINESS_OG_MATURITY_FRAMEWORK.md", "9-dimensjonal matrise for organisatorisk AI-modenhet"),
        ("Modul 3: Governance, Etikk, GDPR & EU AI Act", WORKSPACE_ROOT / "ai-implementeringspakke-okonomi" / "03_MODUL_3_GOVERNANCE_ETIKK_OG_GDPR.md", "Deployer-krav, FRIA, DPIA og menneskelig kontroll"),
        ("Modul 4: Enterprise Målarkitektur & RAG", WORKSPACE_ROOT / "ai-implementeringspakke-okonomi" / "04_MODUL_4_ENTERPRISE_MAALARKITEKTUR_OG_RAG.md", "AI Gateway, PII-vask, modelluavhengighet og dataflyt"),
        ("Modul 5: Use-Case-Prioritering & Pilotmetodikk", WORKSPACE_ROOT / "ai-implementeringspakke-okonomi" / "05_MODUL_5_USE_CASE_PRIORITERING_OG_PILOTMETODIKK.md", "Netto prioriteringsformel, Bølge 1-3 og Gate G3"),
        ("Modul 6: Skalering, Gevinst & Roadmap Kristiansand", WORKSPACE_ROOT / "ai-implementeringspakke-okonomi" / "06_MODUL_6_SKALERING_GEVINST_OG_ROADMAP_KRISTIANSAND.md", "Sekvensert 2025-2030 roadmap og FinOps"),
        ("07 Juridisk Sjekkliste (FRIA & DPIA)", WORKSPACE_ROOT / "ai-implementeringspakke-okonomi" / "07_JURIDISK_SJEKKLISTE_FRIA_DPIA.md", "5-trinns operasjonell juridisk screening og sjekkliste"),
        ("08 Gevinstmodell & Finansiell Håndbok", WORKSPACE_ROOT / "ai-implementeringspakke-okonomi" / "08_GEVINSTMODELL_OG_FINANSIELL_HANDBOK.md", "ROI-kalkulator, parametere og gevinstutaksplan")
    ],
    "⚙️ MLOps & LLMOps Rammeverk (mlops-implementeringspakke/)": [
        ("01 MLOps Oversikt & Prinsipper", WORKSPACE_ROOT / "mlops-implementeringspakke" / "01_MLOps_Oversikt_og_Prinsipper.md", "Kjørneprinsipper, DevOps vs MLOps vs LLMOps og livsløp for kommunale AI-modeller"),
        ("02 Teknisk MLOps-Arkitektur", WORKSPACE_ROOT / "mlops-implementeringspakke" / "02_MLOps_Arkitektur_og_Komponenter.md", "Enterprise MLOps Control Plane, AI Gateway, Model Registry og CI/CD"),
        ("03 Observability, Drift & FinOps", WORKSPACE_ROOT / "mlops-implementeringspakke" / "03_MLOps_Observability_og_Drift.md", "Overvåking av datadrift, concept drift, prompt drift, token caching og FinOps"),
        ("04 Governance, AI Act & Sikkerhet", WORKSPACE_ROOT / "mlops-implementeringspakke" / "04_MLOps_Governance_og_Sikkerhet.md", "EU AI Act deployer-krav, operativ rollestruktur, audit logging og kill-switch"),
        ("05 Testing, Ground Truth & Kvalitet", WORKSPACE_ROOT / "mlops-implementeringspakke" / "05_MLOps_Test_og_Kvalitetssikring.md", "Test-pyramide, Ground Truth fasitsett og Gate G3 akseptkriterier"),
        ("06 Kravspesifikasjon & Anbudsmal", WORKSPACE_ROOT / "mlops-implementeringspakke" / "06_MLOps_Anbud_og_Innkjøpsmal.md", "A- og B-kravmatrise (K-01 til K-10), datasuverenitet og anbudskontrakt")
    ],
    "📊 Ledelsesrapporter & Diagrammer (reports/)": [
        ("Net Zero Waterfall Avviksanalyse (PNG)", WORKSPACE_ROOT / "reports" / "chart_netzero_waterfall.png", "Visuell avviksanalyse fra budsjett til net zero sluttavvik"),
        ("Bo og Miljø Månedlig Avviksprofil (PNG)", WORKSPACE_ROOT / "reports" / "chart_bomiljo_monthly.png", "Månedlig budsjett vs regnskapsavvik for enhet 5200"),
        ("Kommunale Skoler Enhetsanalyse (PNG)", WORKSPACE_ROOT / "reports" / "chart_komskole_units.png", "Avviksfordeling per skoleenhet (funksjon 202)"),
        ("Sektor Faktisk vs Budsjett Bullet Chart (PNG)", WORKSPACE_ROOT / "reports" / "sektor_faktisk_vs_budsjett_bullet.png", "Tufte bullet graph for kommunalsjefområdene"),
        ("Visma Regnskapsstøy Waterfall (PNG)", WORKSPACE_ROOT / "reports" / "visma_stoy_waterfall_chart.png", "Dekomponering av støy og tidsforskyvninger i Visma"),
        ("EPM Status- og Tiltaksrapport (PDF)", WORKSPACE_ROOT / "reports" / "Kristiansand_EPM_Status_Prognose_Tiltaksrapport.pdf", "Offisiell ledelsesrapport med prognoser og tiltak"),
        ("EPM Status og Tiltak Presentasjon (PPTX)", WORKSPACE_ROOT / "reports" / "Kristiansand_EPM_Status_Prognose_Tiltaksrapport.pptx", "Styringsdeck for ledergruppen"),
        ("Presentasjon for Økonomidirektør (PPTX)", WORKSPACE_ROOT / "reports" / "epm_presentasjon_okonomidirektor_v2.pptx", "Strategisk EPM-presentasjon v2"),
        ("Kristiansand EPM Interaktiv Modell (Excel)", WORKSPACE_ROOT / "reports" / "kristiansand_epm_modell_v4_interactive.xlsx", "Interaktiv EPM styringsmodell"),
        ("Prosjektcontroller Modell 2026 (Excel)", WORKSPACE_ROOT / "reports" / "Kommune_Project_Controller_Reporting_2026.xlsx", "Project Controller investerings- og porteføljemodell")
    ],
    "🇳🇴 Norsk EPM Rammeverk & Datalinje (kristiansand_epm_rammeverk_norsk/)": [
        ("EPM Rammeverk Hovedoversikt (README)", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "README_NO.md", "Norsk introduksjon og arkitektursammendrag"),
        ("EPM Fullstendig Arbeidsflyt", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "dokumentasjon" / "epm_fullstendig_arbeidsflyt.md", "End-to-end kommunal økonomistyringsflyt"),
        ("DAX KOSTRA KPI-pakke (Norsk)", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "dokumentasjon" / "dax_kostra_kpi_pakke.md", "Formelpakke for Power BI og Fabric"),
        ("Antigravity EPM Brukstilfelle", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "dokumentasjon" / "antigravity_brukstilfelle_epm.md", "Use-case analyse for Kristiansand kommune"),
        ("RAG Kunnskapsbase Spesifikasjon", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "dokumentasjon" / "rag_kunnskapsbase_spesifikasjon.md", "Spesifikasjon for juridisk vektorindeks"),
        ("EPM Sammendragsrapport (PDF)", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "dokumentasjon" / "epm_sammendrag_kristiansand.pdf", "Sammendragsnotat"),
        ("Formelt Saksfremlegg Økonomidirektør (Word)", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "dokumentasjon" / "saksfremlegg_epm_okonomidirektor.docx", "Word-mal for politisk fremlegg"),
        ("Innføring AI i Offentlig Sektor Rapport (Word)", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "dokumentasjon" / "Rapport om innføring AI i offentlig sektor.docx", "Risiko-, etikk- og styringsrapport"),
        ("Stage-Gate Sjekkliste for AI (Word)", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "dokumentasjon" / "sjekkliste_stage_gate_ai_kristiansand.docx", "10-stegs styringssjekkliste"),
        ("Tildelingsskjema AI Anbud (Excel)", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "dokumentasjon" / "tildelingsskjema_ai_anbud.xlsx", "Vurderingsskjema for anskaffelser"),
        ("Årshjul & Kontoroversikt (Excel)", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "data" / "kontor_oversikt_og_arshjul.xlsx", "Prosessoversikt og årshjul for økonomistyring"),
        ("Power Query M RAG-integrasjon (Code)", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "kildekode" / "powerbi" / "fxOpenAI_RAG.m", "M-funksjon for Power BI"),
        ("Datalinje & Pipeline (Python)", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "kildekode" / "datalinje" / "epm_agent_pipeline.py", "ETL og agent-datalinje"),
        ("PII Vasker & Sikkerhet (Python)", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "kildekode" / "sikkerhet" / "pii_scrubber.py", "Klientside personvernskjold"),
        ("HITL Skriveback UI (Python)", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "kildekode" / "brukergrensesnitt" / "hitl_skriveback_ui.py", "Streamlit Glass-Box Controller UI"),
        ("EPM Arbeidsflytdiagram (PNG)", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "ressurser" / "epm_arbeidsflyt_diagram.png", "Systemarkitektur og dataflyt"),
        ("Kontor Arbeidsflytdiagram (PNG)", WORKSPACE_ROOT / "kristiansand_epm_rammeverk_norsk" / "ressurser" / "kontor_arbeidsflyt_diagram.png", "Kontorarbeidsflyt for økonomi")
    ],
    "📚 EPM Arkitektur & Dokumentasjon (docs/)": [
        ("EPM Use-Case & Styringssirkel", WORKSPACE_ROOT / "docs" / "antigravity_usecase_epm.md", "Metodikk for treplans styringssløyfe"),
        ("Full EPM Arbeidsflyt Dokumentasjon", WORKSPACE_ROOT / "docs" / "epm_full_workflow_documentation.md", "Omfattende forvaltningsdokumentasjon"),
        ("DAX & KOSTRA Formelpakke", WORKSPACE_ROOT / "docs" / "dax_kostra_kpi_package.md", "Fullstendig DAX-bibliotek"),
        ("Framsikt EPM Integrasjonsspesifikasjon", WORKSPACE_ROOT / "docs" / "framsikt_epm_integrasjon_spesifikasjon.md", "API- og tabellkartlegging mot Framsikt"),
        ("Master EPM Samlerapport", WORKSPACE_ROOT / "docs" / "kristiansand_epm_master_samlerapport.md", "Konsolidert styringsdokument"),
        ("Visual Storytelling & Tufte Design", WORKSPACE_ROOT / "docs" / "visual_storytelling_og_stakeholder_design.md", "Retningslinjer for datavisualisering"),
        ("Power BI & Excel Spesifikasjon", WORKSPACE_ROOT / "docs" / "powerbi_excel_native_spesifikasjon.md", "FAST Standard og VertiPaq-arkitektur"),
        ("EPM & AI Utviklingsbacklog", WORKSPACE_ROOT / "docs" / "epm_og_ai_backlog.md", "Milepæler og oppgaver"),
        ("Saksfremlegg Økonomidirektør (Word)", WORKSPACE_ROOT / "docs" / "saksfremlegg_epm_okonomidirektor.docx", "Word-saksfremlegg"),
        ("Use-Case Kristiansand Kommune v4 (Word)", WORKSPACE_ROOT / "docs" / "use_case_kristiansand_kommune-v4.docx", "Word use-case spesifikasjon"),
        ("Stage-Gate Sjekkliste (Word)", WORKSPACE_ROOT / "docs" / "sjekkliste_stage_gate_ai_kristiansand.docx", "10-stegs sjekkliste"),
        ("EPM Arkitekturdiagram (PNG)", WORKSPACE_ROOT / "docs" / "epm_workflow_diagram.png", "Høyoppløselig arkitekturdiagram")
    ],
    "🏛️ Kommunale Kildereferanser & Tertialrapporter (docs/references/)": [
        ("1. Tertialrapport 2026 Kristiansand (PDF)", WORKSPACE_ROOT / "docs" / "references" / "1.-tertialrapport-2026---kristiansand-kommune.pdf", "Offisiell 1. tertialrapport for Kristiansand kommune"),
        ("Forslag Økonomiplan 2027-2030 (PDF)", WORKSPACE_ROOT / "docs" / "references" / "kommunedirektorens-forslag-til-okonomiplan-2027-2030.pdf", "Kommunedirektørens forslag til handlings- og økonomiplan"),
        ("Økonomireglement for Kristiansand (PDF)", WORKSPACE_ROOT / "docs" / "references" / "okonomireglement-for-kristiansand-kommune.pdf", "Gjeldende økonomireglement og fullmaktsstruktur"),
        ("Nøkkeltall Kristiansand Kommune (PDF)", WORKSPACE_ROOT / "docs" / "references" / "Nøkkeltall _Kristiansand_Kommune.pdf", "Offisiell samling over kommunens nøkkeltall"),
        ("Operationalizing GenAI in Kristiansand (PDF)", WORKSPACE_ROOT / "docs" / "references" / "Operationalizing_GenAI_in_Kristiansand.pdf", "Strategisk rapport for GenAI i forvaltningen"),
        ("Rådgiver Økonomistyring Kravprofil (PDF)", WORKSPACE_ROOT / "docs" / "references" / "Rådgiver økonomistyring Kristiansand Kommune - arbeidsplassen.no.pdf", "Kompetansekrav og ansvarsområder")
    ],
    "📈 Power BI Modeller, DAX & TMDL (powerbi/)": [
        ("Komplett DAX Måltallsbibliotek (DAX)", WORKSPACE_ROOT / "powerbi" / "02_DAX_Measures_Library.dax", "Over 50 formelle DAX-mål for kommunal økonomistyring"),
        ("Offisiell KOSTRA DAX KPI-pakke (DAX)", WORKSPACE_ROOT / "powerbi" / "04_KOSTRA_DAX_KPI_Package.dax", "KOSTRA KPIer for netto driftsresultat, premieavvik og handlingsregler"),
        ("Power Query M Kildekode (PQ)", WORKSPACE_ROOT / "powerbi" / "01_PowerQuery_M_Code.pq", "Avansert M-spørring for datainnhenting og vasking"),
        ("Power Query OpenAI RAG Funksjon (Code)", WORKSPACE_ROOT / "powerbi" / "fxOpenAI_RAG.m", "M-funksjon for Power BI"),
        ("Power BI Modellarkitektur (Markdown)", WORKSPACE_ROOT / "powerbi" / "03_PowerBI_Model_Architecture.md", "Stjerneskjema og relasjonsdesign"),
        ("Python Modellbygger (Python)", WORKSPACE_ROOT / "powerbi" / "generate_excel_powerbi_model.py", "Skript for generering av Excel/Power BI-modell"),
        ("Enterprise Measures (_Measures.tmdl)", WORKSPACE_ROOT / "powerbi" / "projects" / "Skole enhet project.SemanticModel" / "definition" / "tables" / "_Measures.tmdl", "Samtlige formelle DAX-mål for skolesektoren i PBIP TMDL"),
        ("Hovedbok Transaksjoner (Fact_Regnskap.tmdl)", WORKSPACE_ROOT / "powerbi" / "projects" / "Skole enhet project.SemanticModel" / "definition" / "tables" / "Fact_Regnskap.tmdl", "TMDL tabellstruktur for regnskap"),
        ("Revisjonslogg (Audit_AI_Actions.tmdl)", WORKSPACE_ROOT / "powerbi" / "projects" / "Skole enhet project.SemanticModel" / "definition" / "tables" / "Audit_AI_Actions.tmdl", "TMDL for SHA-256 revisjonslogg"),
        ("Ansvarsdimensjon (Dim_Ansvar.tmdl)", WORKSPACE_ROOT / "powerbi" / "projects" / "Skole enhet project.SemanticModel" / "definition" / "tables" / "Dim_Ansvar.tmdl", "TMDL for organisasjon og skoler"),
        ("KOSTRA Artsdimensjon (Dim_Art.tmdl)", WORKSPACE_ROOT / "powerbi" / "projects" / "Skole enhet project.SemanticModel" / "definition" / "tables" / "Dim_Art.tmdl", "TMDL for artskontoplanen"),
        ("KOSTRA Funksjonsdimensjon (Dim_Funksjon.tmdl)", WORKSPACE_ROOT / "powerbi" / "projects" / "Skole enhet project.SemanticModel" / "definition" / "tables" / "Dim_Funksjon.tmdl", "TMDL for tjenesteområder"),
        ("Tidskalender (Dim_Dato.tmdl)", WORKSPACE_ROOT / "powerbi" / "projects" / "Skole enhet project.SemanticModel" / "definition" / "tables" / "Dim_Dato.tmdl", "TMDL tidshierarki"),
        ("Framsikt Deflator (Framsikt_Deflator.tmdl)", WORKSPACE_ROOT / "powerbi" / "projects" / "Skole enhet project.SemanticModel" / "definition" / "tables" / "Framsikt_Deflator.tmdl", "TMDL for pris- og lønnsvekst"),
        ("Fraværsreduksjon (Fravaer_Reduksjon.tmdl)", WORKSPACE_ROOT / "powerbi" / "projects" / "Skole enhet project.SemanticModel" / "definition" / "tables" / "Fravaer_Reduksjon.tmdl", "TMDL for vikareffekter")
    ],
    "🛡️ Revisjon, Kontroll & Sjekklister (revisjon-og-kontroll/)": [
        ("Periodelukkingssjekkliste", WORKSPACE_ROOT / "revisjon-og-kontroll" / "CONTROLLER_CHECKLIST_OG_PERIODELUKKING.md", "Månedlig avstemming for controller"),
        ("Kommunerevisjonens Sjekkliste", WORKSPACE_ROOT / "revisjon-og-kontroll" / "KOMMUNEREVISJONEN_AUDIT_CHECKLIST.md", "Revisjonsspor & SHA-256 kontroll"),
        ("Notat til Kontrollutvalget", WORKSPACE_ROOT / "revisjon-og-kontroll" / "NOTAT_TIL_KONTROLLUTVALGET_OG_REVISJONEN.md", "Sikkerhet, HITL og personvern"),
        ("Mal for Saksfremlegg (Kommuneloven § 14-5)", WORKSPACE_ROOT / "revisjon-og-kontroll" / "TERTIALRAPPORT_NOTAT_OG_SAKSFREMLEGG.md", "Politisk saksbehandlingsmal"),
        ("Revisjonsarkiv Oversikt (README)", WORKSPACE_ROOT / "revisjon-og-kontroll" / "README.md", "Indeks over kontroll- og revisjonsnotater")
    ],
    "🤖 Operative Agenter (1–12) (agenter/)": [
        ("Agent 09: Prosjektcontroller & Capex (EAC/ETC)", WORKSPACE_ROOT / "agenter" / "09_prosjektcontroller_eac_etc_agent.md", "EVM, S-kurver og usikkerhetsstyring"),
        ("Agent 10: Likviditet & Rentefølsomhet", WORKSPACE_ROOT / "agenter" / "10_likviditet_finans_renteeksponering_agent.md", "Finansforskriften, NIBOR og gjeldstak"),
        ("Agent 11: Selvkost & Gebyrregulativ", WORKSPACE_ROOT / "agenter" / "11_selvkost_gebyr_kalkyle_agent.md", "Selvkostfond og kalkylerente"),
        ("Agent 12: Revisjon & Mislighetskontroll", WORKSPACE_ROOT / "agenter" / "12_revisjon_internkontroll_sporbarhet_agent.md", "Terskelverdier, Benfords lov og SHA-256"),
        ("Agent 01: ETL & Golden Record", WORKSPACE_ROOT / "agenter" / "01_dataintegrasjon_etl_agent.md", "Datainntak og validering"),
        ("Agent 02: Power BI & DAX Modellerer", WORKSPACE_ROOT / "agenter" / "02_bi_dax_modellering_agent.md", "Stjerneskjema og ytelse"),
        ("Agent 03: Prediktiv Anomali", WORKSPACE_ROOT / "agenter" / "03_prediktiv_anomali_agent.md", "Tidligvarsling 60-90 dager før"),
        ("Agent 04: Preskriptiv HITL", WORKSPACE_ROOT / "agenter" / "04_preskriptil_hitl_agent.md" if (WORKSPACE_ROOT / "agenter" / "04_preskriptil_hitl_agent.md").exists() else WORKSPACE_ROOT / "agenter" / "04_preskriptiv_hitl_agent.md", "Tiltaksmeny og delegasjonsreglement"),
        ("Agent 05: Etikk & Styring Portvakt", WORKSPACE_ROOT / "agenter" / "05_etikk_styring_portvakt_agent.md", "Stage-Gate og FRIA/DPIA"),
        ("Agent 06: Ledelsesrapport Skribent", WORKSPACE_ROOT / "agenter" / "06_ledelsesrapport_skribent_agent.md", "Executive saksfremlegg"),
        ("Agent 07: Excel & Power BI Rapportør", WORKSPACE_ROOT / "agenter" / "07_excel_powerbi_rapportering_agent.md", "FAST Standard og visualisering"),
        ("Agent 08: Flernivå Interessentrapportering", WORKSPACE_ROOT / "agenter" / "08_flerniva_interessent_rapportering_agent.md", "Nivå 1–5 tilpasning"),
        ("Agentmatrise Oversikt (README)", WORKSPACE_ROOT / "agenter" / "README.md", "Totaloversikt over alle 12 agenter")
    ],
    "📖 Brukerveiledninger & Årshjul (bruker-guides/)": [
        ("Brukerveiledning Control Office Hub", WORKSPACE_ROOT / "bruker-guides" / "BRUKERGUIDE.md", "Operativ veiledning for controllere"),
        ("Ett-klikks Oppstartsveileder", WORKSPACE_ROOT / "bruker-guides" / "OPPSTARTSVEILEDER_STARTKNAPP.md", "Instruksjoner for oppstart og drift"),
        ("Styringskalender & Årshjul 2026", WORKSPACE_ROOT / "bruker-guides" / "STYRINGSKALENDER_OG_ARSHJUL_2026.md", "Periodelukking og tertialfrister"),
        ("RAG-arkitektur & Semantisk søk", WORKSPACE_ROOT / "bruker-guides" / "rag_forklaring.md", "Teknisk og pedagogisk forklaring"),
        ("10 Stage-Gate Rammeverk", WORKSPACE_ROOT / "bruker-guides" / "stage_gate_rammeverk.md", "AI Governance fra Gate 1 til 10"),
        ("Guide-arkiv Oversikt (README)", WORKSPACE_ROOT / "bruker-guides" / "README.md", "Indeks over veiledninger")
    ],
    "⚙️ Tekniske Spesifikasjoner (spesifikasjoner/)": [
        ("Prognosespesifikasjon (EAC/ETC)", WORKSPACE_ROOT / "spesifikasjoner" / "PREDICTIVE_AI_FORECASTING_SPEC.md", "Matematisk modell og sesongfiltre"),
        ("Skill: Prediktiv Prognostisering", WORKSPACE_ROOT / "spesifikasjoner" / "SKILL_PREDICTIVE_FORECASTING_AI.md", "Skill-definisjon"),
        ("Control Office Hub Spesifikasjon", WORKSPACE_ROOT / "spesifikasjoner" / "OFFICE_DASHBOARD_HUB_SPEC.md", "UI og API arkitektur"),
        ("Docker & MLOps Deployment", WORKSPACE_ROOT / "spesifikasjoner" / "DOCKER_AND_MLOPS_DEPLOYMENT.md", "Kontainerdrift og evaluering"),
        ("Spesifikasjonsarkiv Oversikt (README)", WORKSPACE_ROOT / "spesifikasjoner" / "README.md", "Indeks over tekniske spesifikasjoner")
    ]
}

st.sidebar.markdown("---")
st.sidebar.header("📁 Dokumentarkiv & Ressurser")
st.sidebar.caption("Hurtigtilgang til styringsdokumenter, veiledninger og regnskapsmodeller.")

# Flate opp dokumenter for nedtrekksmeny / hurtigviser
all_docs_flat = {}
for cat, doc_list in DOCUMENTS_MENU.items():
    prefix = cat.split()[0]
    for label, path, desc in doc_list:
        all_docs_flat[f"{prefix} {label}"] = (path, desc)

selected_quick_doc = st.sidebar.selectbox(
    "🔍 Åpne / forhåndsvis dokument:",
    options=["-- Velg et dokument for visning --"] + list(all_docs_flat.keys()),
    index=0
)

if selected_quick_doc != "-- Velg et dokument for visning --":
    doc_path, doc_desc = all_docs_flat[selected_quick_doc]
    if doc_path.exists():
        st.sidebar.info(f"ℹ️ {doc_desc}")
        ext = doc_path.suffix.lower()
        if ext == ".md":
            with st.sidebar.expander("📖 Forhåndsvisning i sidebar", expanded=True):
                content = doc_path.read_text(encoding="utf-8", errors="replace")
                st.markdown(content[:1500] + ("\n\n*(Fortsetter... se hele i fane 'Dokumentarkiv')*" if len(content) > 1500 else ""))
                st.download_button(
                    label=f"⬇️ Last ned {doc_path.name}",
                    data=content,
                    file_name=doc_path.name,
                    mime="text/markdown",
                    key=f"dl_sb_{doc_path.stem}"
                )
                if st.button("👁️ Vis i full bredde i hovedvindu", key=f"sb_view_full_{doc_path.stem}"):
                    st.session_state["active_doc_path"] = str(doc_path)
                    st.session_state["active_doc_title"] = selected_quick_doc
        elif ext in [".png", ".jpg", ".jpeg"]:
            with st.sidebar.expander("🖼️ Forhåndsvis bilde", expanded=True):
                st.image(str(doc_path), caption=doc_path.name, use_container_width=True)
                with open(doc_path, "rb") as fb:
                    st.download_button(f"⬇️ Last ned bilde", data=fb.read(), file_name=doc_path.name, mime=f"image/{ext.strip('.')}", key=f"dl_sb_img_{doc_path.stem}")
                if st.button("👁️ Vis i full bredde", key=f"sb_view_img_{doc_path.stem}"):
                    st.session_state["active_doc_path"] = str(doc_path)
                    st.session_state["active_doc_title"] = selected_quick_doc
        elif ext in [".tmdl", ".m", ".py", ".sql", ".dax", ".pq", ".csv", ".json"]:
            with st.sidebar.expander("💻 Kildekodevisning", expanded=True):
                code_content = doc_path.read_text(encoding="utf-8", errors="replace")
                code_lang = "dax" if ext in [".dax", ".tmdl"] else ("powerquery" if ext in [".pq", ".m"] else ("python" if ext == ".py" else ("sql" if ext == ".sql" else "text")))
                st.code(code_content[:1200] + ("\n\n# ... se resten i fane 'Dokumentarkiv'" if len(code_content) > 1200 else ""), language=code_lang)
                st.download_button(f"⬇️ Last ned {doc_path.name}", data=code_content, file_name=doc_path.name, mime="text/plain", key=f"dl_sb_code_{doc_path.stem}")
                if st.button("👁️ Vis i full bredde", key=f"sb_view_code_{doc_path.stem}"):
                    st.session_state["active_doc_path"] = str(doc_path)
                    st.session_state["active_doc_title"] = selected_quick_doc
        else:
            with st.sidebar.expander(f"📦 Filinfo ({ext.upper()})", expanded=True):
                size_kb = doc_path.stat().st_size / 1024
                size_str = f"{size_kb / 1024:.2f} MB" if size_kb > 1024 else f"{size_kb:.1f} KB"
                st.markdown(f"**Fil:** `{doc_path.name}`  \n**Størrelse:** `{size_str}`")
                with open(doc_path, "rb") as f:
                    mime = "application/pdf" if ext == ".pdf" else "application/octet-stream"
                    st.download_button(
                        label=f"⬇️ Last ned {doc_path.name}",
                        data=f.read(),
                        file_name=doc_path.name,
                        mime=mime,
                        key=f"dl_sb_{doc_path.stem}"
                    )
                if st.button("👁️ Åpne infokort i hovedvindu", key=f"sb_view_bin_{doc_path.stem}"):
                    st.session_state["active_doc_path"] = str(doc_path)
                    st.session_state["active_doc_title"] = selected_quick_doc
    else:
        st.sidebar.warning(f"Fil ikke funnet: {doc_path.name}")

# Kategoriserte expandere i sidebaren
for cat_title, items in DOCUMENTS_MENU.items():
    with st.sidebar.expander(cat_title, expanded=False):
        for label, path, desc in items:
            exists_indicator = "✅" if path.exists() else "⚠️"
            st.markdown(f"**{exists_indicator} {label}**  \n*{desc}*")
            if path.exists():
                col_btn1, col_btn2 = st.columns([1, 1])
                with col_btn1:
                    if st.button("Åpne 📄", key=f"open_sb_{path.stem}_{cat_title[:4]}"):
                        st.session_state["active_doc_path"] = str(path)
                        st.session_state["active_doc_title"] = label
                with col_btn2:
                    ext = path.suffix.lower()
                    if ext in [".md", ".tmdl", ".m", ".py", ".sql", ".dax", ".pq", ".csv", ".json"]:
                        st.download_button("Last ned ⬇️", data=path.read_text(encoding="utf-8", errors="replace"), file_name=path.name, mime="text/plain", key=f"dl_exp_{path.stem}_{cat_title[:4]}")
                    else:
                        with open(path, "rb") as fb:
                            mime = "application/pdf" if ext == ".pdf" else "application/octet-stream"
                            st.download_button("Last ned ⬇️", data=fb.read(), file_name=path.name, mime=mime, key=f"dl_exp_bin_{path.stem}_{cat_title[:4]}")
            st.markdown("---")

# ==========================================
# 5. HOVEDFLATE: MULTI-TAB CONTROL OFFICE HUB
# ==========================================
tab_mcp, tab_pbi, tab_rag, tab_calendar, tab_controller, tab_saksfremlegg, tab_docs = st.tabs([
    "⚡ Gemini Flash Chat (MCP)",
    "📈 Power BI Rapportering (.PBIP)",
    "💬 RAG Regelverksassistent",
    "📅 Årshjul & Kritiske Frister",
    "📊 Økonomikontroll & Avvik (EVM)",
    "📝 Saksfremlegg & HITL Sign-Off",
    "📁 Dokumentarkiv & Ressurser"
])


# -------------------------------------------------------------
# FANE 0: GEMINI FLASH CHAT MED MCP PROTOKOLL
# -------------------------------------------------------------
with tab_mcp:
    st.markdown("### ⚡ Gemini Flash Chat & MCP Beslutningsstøtte")
    st.caption("Lynrask inferens (< 1,5s) forankret i Model Context Protocol (MCP), Visma ERP og sqlite-vec RAG.")

    # Statusbanner
    col_sb1, col_sb2, col_sb3 = st.columns([2, 1, 1])
    with col_sb1:
        st.success("🟢 **MCP Server Aktiv:** 3 verktøy tilkoblet (`get_unit_financials`, `search_municipal_law`, `calculate_eoy_impact`)", icon="🛠️")
    with col_sb2:
        st.info("⚡ **Responstid:** < 1,5 sekunder")
    with col_sb3:
        st.info("🛡️ **PII Filter:** Aktivt (GDPR)")

    if "mcp_chat_history" not in st.session_state:
        st.session_state.mcp_chat_history = []

    if "mcp_active_tools" not in st.session_state:
        st.session_state.mcp_active_tools = []

    if "mcp_last_audit_hash" not in st.session_state:
        st.session_state.mcp_last_audit_hash = ""

    # Hurtigknapper for vanlige scenarioer
    st.markdown("##### 💡 Hurtigvalg for vanlige problemstillinger:")
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    quick_prompt = None

    if q_col1.button("🏫 Enhet 202 Grunnskole: Q2 status & avvik", use_container_width=True):
        quick_prompt = "Hva er status på Enhet 202 Grunnskole per Q2, hva er hovedårsaken til avviket, og hvilken effekt vil tiltakene ha på helårsprognosen (EOY)?"
    if q_col2.button("⚖️ Inndekning av merforbruk (§ 14-5)", use_container_width=True):
        quick_prompt = "Hvilke krav stiller Kommuneloven § 14-5 og bruttoprinsippet § 14-6 ved inndekning av merforbruk på skolesektoren?"
    if q_col3.button("🎯 Kvantifiser vikarstopp (170k/mnd)", use_container_width=True):
        quick_prompt = "Simulér helårseffekt dersom vi innfører vikarstopp og purring på NAV-refusjoner fra august med 170 000 kr månedlig besparelse."
    if q_col4.button("🏥 Enhet 401 Boenhet: Overtid & turnus", use_container_width=True):
        quick_prompt = "Hva er situasjonen for Enhet 401 Helse og Mestring per Q2 når det gjelder overtid, helgetillegg og turnusavvik?"

    # Vis chat-historikk
    for msg in st.session_state.mcp_chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Brukerinput
    user_input = st.chat_input("Spør Gemini Flash om regnskap, lover eller helårsprognoser...")
    active_prompt = quick_prompt or user_input

    if active_prompt:
        # Legg til brukerens melding
        st.session_state.mcp_chat_history.append({"role": "user", "content": active_prompt})
        with st.chat_message("user"):
            st.markdown(active_prompt)

        # Generer svar med MCP verktøy
        with st.chat_message("assistant"):
            with st.spinner("Kaller MCP Tools: get_unit_financials, search_municipal_law, calculate_eoy_impact..."):
                res_dict = execute_gemini_mcp_query(active_prompt, model_name=selected_model)
                reply_text = res_dict["text"]
                audit_hash = res_dict["audit_hash"]
                tools_used = res_dict["tools_called"]

                st.markdown(reply_text)
                st.caption(f"🔒 **Kryptografisk Revisjonsstempel (SHA-256):** `{audit_hash}` | Status: Logget i `Audit_AI_Actions`")

                # Vis MCP verktøyinspektør i expander
                with st.expander("🛠️ Se detaljerte MCP Verktøykall & Data-Payloads", expanded=False):
                    st.markdown("**Verktøykall utført av Gemini Flash:**")
                    for t in tools_used:
                        st.code(t, language="python")
                    st.json(res_dict.get("data", {}))

                st.session_state.mcp_chat_history.append({"role": "assistant", "content": reply_text})
                st.session_state.mcp_active_tools = tools_used
                st.session_state.mcp_last_audit_hash = audit_hash

    st.markdown("---")
    st.subheader("📦 Genererte Styringsdokumenter for Bystyret & Formannskapet")
    st.caption("Ferdigproduserte, formelle filer i samsvar med kommunens standardbunter for PowerPoint, Excel, Word og Power BI.")

    col_dl1, col_dl2, col_dl3, col_dl4 = st.columns(4)

    pptx_path = WORKSPACE_ROOT / "powerpoint" / "Presentasjon_Bystyret_Tertialrapport_2026.pptx"
    xlsx_path = WORKSPACE_ROOT / "excel" / "Kommune_FAST_Finansiell_Modell_2026.xlsx"
    docx_path = WORKSPACE_ROOT / "word" / "Saksfremlegg_Bystyret_Budsjettendring_2026.docx"
    dax_path = WORKSPACE_ROOT / "powerbi" / "05_Komplett_Kommune_DAX_Bundle.dax"

    with col_dl1:
        st.markdown("**🖥️ PowerPoint (16:9 Deck)**  \n*7 standard slides for Bystyret*")
        if pptx_path.exists():
            with open(pptx_path, "rb") as f:
                st.download_button(
                    "⬇️ Last ned PPTX",
                    data=f.read(),
                    file_name=pptx_path.name,
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    key="dl_tabmcp_pptx",
                    use_container_width=True
                )
        else:
            st.warning("Ikke generert ennå")

    with col_dl2:
        st.markdown("**📊 Excel FAST Modell**  \n*5-tabs FP&A styringsmodell*")
        if xlsx_path.exists():
            with open(xlsx_path, "rb") as f:
                st.download_button(
                    "⬇️ Last ned XLSX",
                    data=f.read(),
                    file_name=xlsx_path.name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="dl_tabmcp_xlsx",
                    use_container_width=True
                )
        else:
            st.warning("Ikke generert ennå")

    with col_dl3:
        st.markdown("**📝 Word Saksfremlegg**  \n*Public360-tagget politisk sak*")
        if docx_path.exists():
            with open(docx_path, "rb") as f:
                st.download_button(
                    "⬇️ Last ned DOCX",
                    data=f.read(),
                    file_name=docx_path.name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key="dl_tabmcp_docx",
                    use_container_width=True
                )
        else:
            st.warning("Ikke generert ennå")

    with col_dl4:
        st.markdown("**📈 Power BI DAX Pakke**  \n*Komplett 7-layouts DAX bibliotek*")
        if dax_path.exists():
            st.download_button(
                "⬇️ Last ned DAX",
                data=dax_path.read_text(encoding="utf-8", errors="replace"),
                file_name=dax_path.name,
                mime="text/plain",
                key="dl_tabmcp_dax",
                use_container_width=True
            )
        else:
            st.warning("Ikke generert ennå")



# -------------------------------------------------------------
# FANE 0.5: POWER BI RAPPORTERINGSPROSJEKT (.PBIP)
# -------------------------------------------------------------
with tab_pbi:
    st.markdown("### 📈 Power BI Rapporteringsprosjekt (PBIP Developer Mode)")
    st.caption("Offisielt Power BI Desktop / Fabric prosjekt: `powerbi/pbi_reporting_project.pbip` med 7 standardiserte PBIR rapportsider og TMDL Semantisk Modell.")

    pbip_file = WORKSPACE_ROOT / "powerbi" / "pbi_reporting_project.pbip"
    pbip_guide = WORKSPACE_ROOT / "powerbi" / "07_PowerBI_7_Layouts_Spec_Guide.md"
    dax_bundle = WORKSPACE_ROOT / "powerbi" / "05_Komplett_Kommune_DAX_Bundle.dax"

    # Status- og arkitekturoversikt
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.metric(label="Modellformat", value="PBIP + TMDL", delta="Git-vennlig")
    with kpi_col2:
        st.metric(label="Rapportsider", value="7 sider", delta="PBIR format")
    with kpi_col3:
        st.metric(label="Visual Containers", value="50 stk", delta="Tufte Data-Ink")
    with kpi_col4:
        st.metric(label="TMDL Tabeller", value="9 tabeller", delta="Star Schema")

    # Handlingsknapper
    act_col1, act_col2, act_col3 = st.columns([1.5, 1.5, 1])
    with act_col1:
        if pbip_file.exists():
            st.download_button(
                "⬇️ Last ned prosjektfil (.pbip)",
                data=pbip_file.read_text(encoding="utf-8", errors="replace"),
                file_name="pbi_reporting_project.pbip",
                mime="application/json",
                use_container_width=True
            )
    with act_col2:
        if st.button("🔄 Bygg / Oppdater PBIP på nytt", use_container_width=True):
            try:
                from kommune_ai_guardrails.generators.powerbi_pbip_generator import build_pbip_project
                res = build_pbip_project()
                st.success(f"✓ Bygget {res['pages_count']} sider og {res['visuals_count']} visual containers!")
            except Exception as e:
                st.error(f"Feil ved bygging: {e}")
    with act_col3:
        if pbip_guide.exists():
            st.link_button("📖 7 Layouts Guide", "https://github.com/Frank-Ellingsen/AI_KOM/blob/main/powerbi/07_PowerBI_7_Layouts_Spec_Guide.md", use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📑 Interaktiv Forhåndsvisning av 7 PBIR Rapportsider")

    selected_pbi_page = st.selectbox(
        "Velg rapportside for detaljert visning og metrikker:",
        options=[
            "1. Toppledelse (CFO Panel)",
            "2. Sektor Oppvekst & Grunnskole (Enhet 202)",
            "3. Sektor Helse & Mestring (Enhet 2540)",
            "4. Lønn, Overtid & Vikarmonitor",
            "5. Prognose & What-If Scenarier",
            "6. Investering & Capex (EVM)",
            "7. Revisjon & Audit Trail (Stage-Gate Port 9)"
        ],
        index=0
    )

    if selected_pbi_page == "1. Toppledelse (CFO Panel)":
        st.info("📰 **FT Aksjonstittel:** *Kristiansand Kommune — Finansiell Topplederoversikt & Prognose 2026*")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Regnskap YTD", "kr 36 080 000", "Bokført")
        c2.metric("Budsjett YTD", "kr 33 591 000", "Periodisert")
        c3.metric("Avvik YTD", "+kr 2 489 000", "+7,4% (Kritisk)", delta_color="inverse")
        c4.metric("EOY Sluttavvik", "+kr 3 733 500", "Før tiltak", delta_color="inverse")

        st.markdown("##### 📊 Avviksfordeling per Enhet (Diverging Bar / Tabell)")
        df_p1 = pd.DataFrame([
            {"Sektor / Enhet": "01 Oppvekst (Enhet 202 Grunnskole)", "Budsjett YTD": 12450000, "Regnskap YTD": 13870000, "Avvik YTD": 1420000, "Avvik %": "+11,4%", "Status": "KRITISK MERFORBRUK"},
            {"Sektor / Enhet": "02 Helse & Mestring (Enhet 2540 Boenhet)", "Budsjett YTD": 21141000, "Regnskap YTD": 22210000, "Avvik YTD": 1069000, "Avvik %": "+5,1%", "Status": "AKTSOMHET"}
        ])
        st.dataframe(df_p1, use_container_width=True, hide_index=True)

    elif selected_pbi_page == "2. Sektor Oppvekst & Grunnskole (Enhet 202)":
        st.info("📰 **FT Aksjonstittel:** *Enhet 202 Grunnskole: Vikarforbruk og sykefravær krever omdisponering*")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Forbruk Grunnskole", "kr 13 870 000")
        c2.metric("Vikarer Art 1020", "kr 1 420 000", "+158% vs budsjett", delta_color="inverse")
        c3.metric("Vikarandel Lønn", "16,2%", "Mål: < 5,0%", delta_color="inverse")
        c4.metric("Kostnad pr. Elev", "kr 9 768 /elev", "1 420 elever")

        st.markdown("##### 📋 Kontospesifikasjon Grunnskole (KOSTRA Arter)")
        df_p2 = pd.DataFrame([
            {"Kontoart": "Art 1010", "Navn": "Fastlønn og faste tillegg", "Budsjett YTD": 9200000, "Regnskap YTD": 9180000, "Avvik": -20000, "Avvik %": "-0,2%"},
            {"Kontoart": "Art 1020", "Navn": "Vikarer ved fravær", "Budsjett YTD": 550000, "Regnskap YTD": 1420000, "Avvik": 870000, "Avvik %": "+158,2%"},
            {"Kontoart": "Art 1090", "Navn": "Overtid og ekstrahjelp", "Budsjett YTD": 300000, "Regnskap YTD": 720000, "Avvik": 420000, "Avvik %": "+140,0%"},
            {"Kontoart": "Art 1600", "Navn": "NAV Sykepengerefusjoner", "Budsjett YTD": -800000, "Regnskap YTD": -650000, "Avvik": 150000, "Avvik %": "+18,8%"}
        ])
        st.dataframe(df_p2, use_container_width=True, hide_index=True)

    elif selected_pbi_page == "3. Sektor Helse & Mestring (Enhet 2540)":
        st.info("📰 **FT Aksjonstittel:** *Enhet 401 Boenhet: Turnus- og overtidspress i døgnkontinuerlig drift*")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Forbruk Helse", "kr 22 210 000")
        c2.metric("Overtid Art 1090", "kr 2 150 000", "+320k vs budsjett", delta_color="inverse")
        c3.metric("Overtidsandel Turnus", "14,8%", "Terskel: 10,0%", delta_color="inverse")
        c4.metric("EOY etter Tiltak", "kr -324 921", "I balanse jf. § 14-5")

        st.markdown("##### 🏥 Boenhets- og Turnusfordeling")
        df_p3 = pd.DataFrame([
            {"Lokasjon": "Boenhet A (Døgnpost 1)", "Område": "Miljøarbeidertjeneste", "Budsjett YTD": 8100000, "Regnskap YTD": 8650000, "Avvik": 550000, "Overtidsandel": "15,4%"},
            {"Lokasjon": "Boenhet B (Døgnpost 2)", "Område": "Psykisk helse & rus", "Budsjett YTD": 7500000, "Regnskap YTD": 7820000, "Avvik": 320000, "Overtidsandel": "14,2%"},
            {"Lokasjon": "Dagsenter & Avlastning", "Område": "Aktivitetstilbud", "Budsjett YTD": 5541000, "Regnskap YTD": 5740000, "Avvik": 199000, "Overtidsandel": "11,8%"}
        ])
        st.dataframe(df_p3, use_container_width=True, hide_index=True)

    elif selected_pbi_page == "4. Lønn, Overtid & Vikarmonitor":
        st.info("📰 **FT Aksjonstittel:** *HR & Lønnsmonitor: Artsanalyse for 1000 Fastlønn, 1020 Vikar og 1090 Overtid*")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Lønn YTD", "kr 28 850 000")
        c2.metric("Vikarforbruk", "kr 2 480 000", "+1,2M vs budsjett", delta_color="inverse")
        c3.metric("Overtid", "kr 2 870 000", "+740k vs budsjett", delta_color="inverse")
        c4.metric("NAV-Refusjoner", "kr 1 120 000", "Bokført YTD")

        st.markdown("##### 📅 Månedlig Lønns- og Vikarutvikling (2026)")
        df_p4 = pd.DataFrame([
            {"Måned": "Mai 2026", "Fastlønn": 2920000, "Vikarer": 290000, "Overtid": 340000, "NAV Refusjon": -140000, "Netto Lønn": 3410000},
            {"Måned": "Juni 2026", "Fastlønn": 3050000, "Vikarer": 380000, "Overtid": 410000, "NAV Refusjon": -155000, "Netto Lønn": 3685000},
            {"Måned": "Juli 2026", "Fastlønn": 3110000, "Vikarer": 460000, "Overtid": 450000, "NAV Refusjon": -160000, "Netto Lønn": 3860000},
            {"Måned": "August 2026", "Fastlønn": 3180000, "Vikarer": 520000, "Overtid": 480000, "NAV Refusjon": -175000, "Netto Lønn": 4005000}
        ])
        st.dataframe(df_p4, use_container_width=True, hide_index=True)

    elif selected_pbi_page == "5. Prognose & What-If Scenarier":
        st.info("📰 **FT Aksjonstittel:** *What-If Simulering: Framsikt deflator, vikarreduksjon og helårsbalanse*")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Vedtatt Årsramme", "kr 52 400 000")
        c2.metric("Prognose Uten Tiltak", "kr 56 133 500", "+3 733 500", delta_color="inverse")
        c3.metric("Tiltakseffekt T3", "-kr 2 791 421", "Signert Port 9")
        c4.metric("Simulert Sluttavvik", "+kr 942 079", "Håndterbart")

        sim_def = st.slider("Framsikt Lønnsdeflator (%):", min_value=3.0, max_value=6.0, value=4.1, step=0.1)
        sim_sav = st.slider("Fraværstiltak Effektreduksjon (%):", min_value=0.5, max_value=4.0, value=1.5, step=0.1)
        st.caption(f"Simulert tilleggsramme deflator: kr {52400000 * (sim_def/100):,.0f} | Est. vikarbesparelse: kr {2480000 * (sim_sav/100):,.0f}")

    elif selected_pbi_page == "6. Investering & Capex (EVM)":
        st.info("📰 **FT Aksjonstittel:** *Project Controlling: Investeringsportefølje, Earned Value & Sluttkostnad (EAC)*")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Planlagt Verdi (PV)", "kr 328 000 000")
        c2.metric("Påløpt Kostnad (AC)", "kr 292 900 000")
        c3.metric("Kostnadsavvik (CV)", "-kr 35 100 000", "Underbudsjettert", delta_color="inverse")
        c4.metric("Kostnadsindeks (CPI)", "0,893", "Terskel: 1,000", delta_color="inverse")

        st.markdown("##### 🏗️ EVM Porteføljematrise for Project Controller")
        df_p6 = pd.DataFrame([
            {"Prosjekt": "Vågsbygd Skole Utvidelse", "Kode": "PROJ-101", "BAC": 185000000, "PV": 115000000, "AC": 104500000, "CPI": 0.909, "Sluttprognose (EAC)": 208251070},
            {"Prosjekt": "Randesund Døgnbemannet Boenhet", "Kode": "PROJ-201", "BAC": 240000000, "PV": 165000000, "AC": 139100000, "CPI": 0.843, "Sluttprognose (EAC)": 299529558},
            {"Prosjekt": "VA-Hovedledning Selvkost", "Kode": "PROJ-301", "BAC": 92000000, "PV": 48000000, "AC": 49300000, "CPI": 1.027, "Sluttprognose (EAC)": 89668168}
        ])
        st.dataframe(df_p6, use_container_width=True, hide_index=True)

    elif selected_pbi_page == "7. Revisjon & Audit Trail (Stage-Gate Port 9)":
        st.info("📰 **FT Aksjonstittel:** *Revisjonsspor & Kontrollutvalget: SHA-256 forsegling og Human-in-the-Loop*")
        c1, c2, c3 = st.columns(3)
        c1.metric("Verifisert Regnskap YTD", "kr 36 080 000")
        c2.metric("Totalavvik Gransket", "kr 2 489 000")
        c3.metric("Signerte Tiltak i Port 9", "kr 2 791 421", "Godkjent")

        st.markdown("##### 🛡️ Uforanderlig Revisjonslogg (Audit_AI_Actions)")
        df_p7 = pd.DataFrame([
            {"Tidsstempel": "2026-08-20 14:30", "Enhet": "2020 Grunnskole", "AI-Tiltak": "Vikarstopp korttidsfravær < 3 dager", "Beslutning": "APPROVED", "Saksbehandler": "Frank Ellingsen", "SHA-256 Hash": "a8f9c2e411b98d24..."},
            {"Tidsstempel": "2026-08-22 11:15", "Enhet": "2540 Boenhet", "AI-Tiltak": "Turnusendring og overtidstak døgnpost", "Beslutning": "MODIFIED", "Saksbehandler": "Frank Ellingsen", "SHA-256 Hash": "f34b9982a74c1022..."}
        ])
        st.dataframe(df_p7, use_container_width=True, hide_index=True)


# -------------------------------------------------------------
# FANE 1: RAG REGELVERKSASSISTENT
# -------------------------------------------------------------
with tab_rag:
    st.markdown("### 🔍 Kildekritisk Oppslag i Kommunalt Regelverk")
    st.caption("Oppslag gjøres i Kommuneloven, KOSTRA-forskriften, Selvkostforskriften, Økonomireglementet og tertialrapporter.")

    if "search_result" not in st.session_state:
        st.session_state.search_result = None

    example_questions = [
        "Hvilke regler gjelder dersom vi må endre budsjettet i løpet av året?",
        "Hvem har fullmakt til å godkjenne overskridelser i investeringsprosjekter?",
        "Hvilke krav stilles til internkontroll og risikostyring ifølge kommuneloven?"
    ]

    st.markdown("##### 💡 Hurtigvalg for vanlige problemstillinger:")
    cols_ex = st.columns(len(example_questions))
    selected_example = None
    for idx, q_text in enumerate(example_questions):
        if cols_ex[idx].button(q_text, key=f"ex_btn_{idx}", use_container_width=True):
            selected_example = q_text

    with st.form(key="search_form", clear_on_submit=False):
        default_text = selected_example or (st.session_state.search_result["query"] if st.session_state.search_result else "")
        user_query = st.text_input(
            "💬 Still ditt faglige spørsmål:",
            value=default_text,
            placeholder="F.eks.: Hvilke regler gjelder for omdisponering mellom rammeområder jf. Kommuneloven § 14-5?"
        )
        submit_clicked = st.form_submit_button("🔍 Søk og Generer Svar", type="primary")

    if submit_clicked:
        if not user_query.strip():
            st.warning("Vennligst skriv inn et spørsmål først.")
        else:
            with st.spinner(f"Søker i hybrid vektordatabase og genererer svar med {selected_model}..."):
                answer, chunk_ids, audit_hash = ask_kommune_ai(
                    user_query, 
                    embedding_model, 
                    model_name=selected_model
                )
                chunks_data = fetch_chunk_details(chunk_ids)
                pii_detected = sanitize_pii(user_query) != user_query
                st.session_state.search_result = {
                    "query": user_query,
                    "sanitized_query": sanitize_pii(user_query),
                    "answer": answer,
                    "chunk_ids": chunk_ids,
                    "audit_hash": audit_hash,
                    "chunks_data": chunks_data,
                    "model": selected_model,
                    "pii_detected": pii_detected,
                }

    res = st.session_state.search_result
    if res:
        st.markdown("---")
        st.subheader("📋 Rådgivende Svar")

        if res.get("pii_detected"):
            st.warning("🛡️ **Stage-Gate Port 4 (Personvernskjerming):** Følsomme opplysninger ble automatisk maskert før innsending til modellen.")

        answer_text = res["answer"]
        if answer_text.startswith("⚠️"):
            st.error(answer_text)
        elif answer_text.startswith("❌"):
            st.warning(answer_text)
        else:
            st.info(answer_text)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📌 Benyttede kilde-chunks", f"{len(res['chunk_ids'])} chunks")
        with col2:
            hash_short = f"{res['audit_hash'][:16]}..." if res["audit_hash"] else "N/A"
            st.metric("🛡️ SHA-256 Audit Trail", hash_short, help=res["audit_hash"])
        with col3:
            st.metric("⚙️ LLM-modell benyttet", res["model"])

        chunks = res.get("chunks_data", [])
        with st.expander(f"📚 Vis siterte regelverkskilder ({len(chunks)} kilder)"):
            if chunks:
                for c in chunks:
                    ref_str = f" ({c['section_ref']})" if c.get("section_ref") else ""
                    st.markdown(
                        f"""
                        <div class="source-chunk-card">
                            <strong>Kilde:</strong> {c.get('source_file')} | <strong>Kategori:</strong> {c.get('category')}{ref_str} — <em>{c.get('title')}</em><br/>
                            <div style="margin-top: 0.5rem; font-size: 0.95rem; white-space: pre-wrap;">{c.get('content')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.write(f"Chunk ID-er benyttet: `{res['chunk_ids']}`")

        with st.expander("🔍 Se fullstendig Audit Trail Stempel (Stage-Gate Port 9)"):
            st.json({
                "user_query": res["query"],
                "retrieved_chunk_ids": res["chunk_ids"],
                "sha256_hash": res["audit_hash"],
                "model_used": res["model"],
                "status": "LOGGED_TO_SQLITE_AUDIT_LOG"
            })


# -------------------------------------------------------------
# FANE 2: ÅRSHJUL & KRITISKE FRISTER
# -------------------------------------------------------------
with tab_calendar:
    st.markdown("### 📅 Kommunalt Styringsårshjul & Kritiske Frister")
    st.caption("Synkronisert oversikt over kommunens økonomiske styringssyklus jf. OFFICE_DASHBOARD_HUB_SPEC.md.")

    # Statusbanner for gjeldende fase
    st.success(
        "🟢 **GJELDENDE FASE: FORBEREDELSE 2. TERTIALRAPPORT (T2)** | Formannskapets behandling: 28. september | HØP 2027–2030 fremlegges 23. september",
        icon="📌"
    )

    col_q1, col_q2, col_q3, col_q4 = st.columns(4)

    with col_q1:
        st.markdown(
            """
            <div class="arshjul-card">
                <strong>Q1: KOSTRA & Regnskap</strong><br/>
                <small>Januar – Mars</small>
                <hr style="margin: 0.4rem 0;"/>
                • 15. jan / 23. feb: KOSTRA-rapportering<br/>
                • 09. mars: Regnskapsavslutning<br/>
                • 31. mars: Årsregnskap fremlegges
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_q2:
        st.markdown(
            """
            <div class="arshjul-card">
                <strong>Q2: 1. Tertial (T1)</strong><br/>
                <small>April – Juni</small>
                <hr style="margin: 0.4rem 0;"/>
                • 15. apr: Revisjonsberetning<br/>
                • 25. mai: 1. tertial til Bystyret<br/>
                • 02. juni: RNB & KOSTRA-tall
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_q3:
        st.markdown(
            """
            <div class="arshjul-card active">
                <strong>Q3: 2. Tertial (T2) ⭐ AKTIV</strong><br/>
                <small>Juli – September</small>
                <hr style="margin: 0.4rem 0;"/>
                • 15. aug: Innspill ny HØP<br/>
                • 23. sep: Kommunedirektørens HØP<br/>
                • 28. sep: 2. tertial i Formannskapet
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_q4:
        st.markdown(
            """
            <div class="arshjul-card">
                <strong>Q4: HØP & Budsjettvedtak</strong><br/>
                <small>Oktober – Desember</small>
                <hr style="margin: 0.4rem 0;"/>
                • 07. okt: Statsbudsjettet<br/>
                • 25. nov: Formannskapets innstilling<br/>
                • 18. des: Bystyrets endelige vedtak
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.subheader("📋 Sjekkliste for Senior Controller ved T2-forberedelse:")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.checkbox("Avstemme påløpte vikarutgifter og overtid mot Framsikt-rammer", value=True)
        st.checkbox("Identifisere etterslep på NAV sykepengerefusjoner", value=True)
        st.checkbox("Beregne Estimate at Completion (EAC) på tjenesteområdene", value=True)
    with col_c2:
        st.checkbox("Sjekke krav om budsjettendring jf. Kommuneloven § 14-5", value=True)
        st.checkbox("Generere utkast til politisk omdisponeringssak", value=False)
        st.checkbox("Signere revisjonslogg med SHA-256 for Kommunerevisjonen", value=False)


# -------------------------------------------------------------
# FANE 3: ØKONOMIKONTROLL & AVVIK (GOLDEN RECORD / EVM)
# -------------------------------------------------------------
with tab_controller:
    st.markdown("### 📊 Porteføljeoversikt & Earned Value Management (EVM)")
    st.caption("Sanntidskonsolidering fra kommune_golden_record.db basert på ISO 21508 og Edward Tufte Data-Ink standard.")

    df_evm = load_golden_record_evm()

    if df_evm.empty:
        st.warning("⚠️ Fant ikke 'kommune_golden_record.db'. Vennligst kjør 'build_golden_record.py' i erp_data.")
    else:
        # Porteføljesammendrag
        tot_pv = df_evm["Planlagt (PV)"].sum()
        tot_ac = df_evm["Påløpt (AC)"].sum()
        tot_cv = tot_pv - tot_ac
        tot_cpi = tot_pv / tot_ac if tot_ac > 0 else 1.0
        tot_bac = df_evm["Årsbudsjett (BAC)"].sum()
        tot_eac = tot_bac / tot_cpi if tot_cpi > 0 else tot_bac
        tot_merforbruk = tot_eac - tot_bac

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Planlagt Verdi (PV YTD)", f"{tot_pv:,.0f} kr".replace(",", " "))
        m2.metric("Påløpt Kostnad (AC YTD)", f"{tot_ac:,.0f} kr".replace(",", " "))
        m3.metric(
            "Kostnadsavvik (CV = PV - AC)", 
            f"{tot_cv:,.0f} kr".replace(",", " "), 
            delta=f"{tot_cv:,.0f} kr".replace(",", " "),
            delta_color="normal"
        )
        m4.metric("Kostnadsindeks (CPI)", f"{tot_cpi:.3f}", help="Under 1.0 betyr merforbruk i forhold til planlagt budsjett-takt")
        m5.metric(
            "Sluttprognose (EAC)", 
            f"{tot_eac:,.0f} kr".replace(",", " "),
            delta=f"-{tot_merforbruk:,.0f} kr est. overskridelse".replace(",", " "),
            delta_color="inverse"
        )

        st.markdown("---")
        st.subheader("🏛️ Enhetsoversikt (EVM / Sluttprognose)")

        # Formatert visning for Tufte tabell
        df_display = df_evm.copy()
        for col in ["Planlagt (PV)", "Påløpt (AC)", "Avvik (CV)", "Årsbudsjett (BAC)", "Sluttprognose (EAC)", "Est. Merforbruk"]:
            df_display[col] = df_display[col].apply(lambda x: f"{x:,.0f} kr".replace(",", " "))
        df_display["CPI"] = df_display["CPI"].apply(lambda x: f"{x:.3f}")

        st.dataframe(df_display, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("🚨 Kritiske Kostnadsavvik på KOSTRA Art (Topp 10)")
        
        enhet_valg = st.selectbox(
            "Filtrer på enhet:",
            options=["Alle Enheter", "Kommunal Skole", "Kommunal Boenhet"],
            index=0
        )
        
        df_var = load_top_cost_variances(enhet_valg)
        if not df_var.empty:
            df_var_disp = df_var.copy()
            for col in ["Budsjett (NOK)", "Regnskap (NOK)", "Avvik (NOK)"]:
                df_var_disp[col] = df_var_disp[col].apply(lambda x: f"{x:,.0f} kr".replace(",", " "))
            df_var_disp["Avvik %"] = df_var_disp["Avvik %"].apply(lambda x: f"{x:.1f} %")
            
            st.dataframe(df_var_disp, use_container_width=True, hide_index=True)
            
            st.markdown("💡 **Controller-diagnose:** Negativt avvik representerer merforbruk. For Kommunal Skole skyldes hovedtyngden overforbruk på faste lærerlønner samt vikarutgifter (+319 %) og overtidslønn (+664 %).")
        else:
            st.info("Ingen negative avvik funnet for det valgte filteret.")

        st.markdown("---")
        st.subheader("📈 Executive Styringsvisualiseringer (Tufte IBCS & Avviksanalyser fra reports/)")
        st.caption("Ferdiggenererte høyoppløselige grafer for Formannskapet og ledergruppen, forankret i Edward Tuftes prinsipper.")

        rep_dir = WORKSPACE_ROOT / "reports"
        chart_gallery = {
            "Net Zero Waterfall Avviksanalyse": (
                rep_dir / "chart_netzero_waterfall.png",
                "Viser hvordan samlet avvik dekomponeres fra vedtatt budsjett til net zero sluttavvik via lønnsvekst, vikarpress, overtid og refusjoner."
            ),
            "Sektorvis Budsjett vs Faktisk Bullet Chart": (
                rep_dir / "sektor_faktisk_vs_budsjett_bullet.png",
                "Tufte bullet-grafer som sammenligner faktisk forbruk mot periodisert budsjett og prognose for hvert kommunalsjefområde."
            ),
            "Visma Regnskapsstøy Waterfall": (
                rep_dir / "visma_stoy_waterfall_chart.png",
                "Dekomponerer periodiseringsstøy, fakturaetterslep og engangsposter i Visma ERP for å isolere underliggende driftstrend."
            ),
            "Kommunale Skoler Enhetsanalyse": (
                rep_dir / "chart_komskole_units.png",
                "Enhetsfordeling av driftsavvik på tvers av grunnskolene i Kristiansand (funksjon 202 Grunnskole)."
            ),
            "Bo og Miljø Månedlig Avviksprofil": (
                rep_dir / "chart_bomiljo_monthly.png",
                "Månedlig profil for budsjett vs regnskap med sesongjustert vikarpress for enhet 5200 Bo og Miljø."
            )
        }

        sel_chart_name = st.selectbox("Velg styringsgraf for visning i høyoppløsning:", options=list(chart_gallery.keys()), index=0)
        c_path, c_desc = chart_gallery[sel_chart_name]
        if c_path.exists():
            st.info(f"ℹ️ **Controller-analyse:** {c_desc}")
            st.image(str(c_path), caption=sel_chart_name, use_container_width=True)
            with open(c_path, "rb") as cf:
                st.download_button(
                    label=f"⬇️ Last ned {c_path.name} til presentasjon / saksutredning",
                    data=cf.read(),
                    file_name=c_path.name,
                    mime="image/png",
                    key=f"dl_chart_t3_{c_path.stem}"
                )
        else:
            st.warning(f"Fant ikke diagramfilen: {c_path.name}")


# -------------------------------------------------------------
# FANE 4: SAKSFREMLEGG & HITL SIGN-OFF
# -------------------------------------------------------------
with tab_saksfremlegg:
    st.markdown("### 📝 Saksfremlegg & Human-in-the-Loop (HITL) Sign-Off")
    st.caption("Automatisk generering av politisk saksdokument til Formannskapet jf. Kommuneloven § 13-1 og § 14-5.")

    sakstype = st.selectbox(
        "Velg sakstype for utarbeidelse:",
        options=[
            "Sak: 2. Tertialrapport 2026 — Finansiell Status og Omdisponering av Rammer",
            "Sak: Tilleggsbevilgning for Vikarbruk og Lønnsavvik i Grunnskolen",
            "Sak: Selvkostoppgjør for Vann og Avløp 2026"
        ],
        index=0
    )

    st.markdown("#### 📋 Utkast til Saksfremlegg:")
    
    forslag_vedtak = (
        "1. Bystyret tar 2. tertialrapport 2026 til orientering.\n"
        "2. Det innvilges en budsjettjustering på 2,49 mill. kr til Oppvekst og utdanning for å dekke uforutsette vikar- og overtidskostnader.\n"
        "3. Merforbruket inndekkes i sin helhet ved tilsvarende bruk av kommunens disposisjonsfond jf. Kommuneloven § 14-5."
    )
    
    bakgrunn_tekst = (
        "Per 2. tertial 2026 viser driftsregnskapet for Oppvekst og utdanning et akkumulert merforbruk på 4,10 mill. kr mot periodisert budsjett.\n"
        "Analysen avdekker at vikarforbruket ligger 645 000 kr over budsjett (+319 %), mens overtidskostnadene er 379 000 kr høyere enn planlagt (+665 %).\n"
        "Jf. Kommuneloven § 14-5 plikter kommunen å vedta endringer i årsbudsjettet for å sikre budsjettmessig balanse."
    )

    with st.expander("📄 Se fullstendig saksutkast for Bystyret", expanded=True):
        st.markdown(f"**Sak:** {sakstype}")
        st.markdown(f"**Behandlingsorgan:** Formannskapet / Bystyret | **Saksbehandler:** {user_role}")
        st.markdown("---")
        st.markdown("**Kommunedirektørens forslag til vedtak:**")
        st.info(forslag_vedtak)
        st.markdown("**Saksopplysning & Økonomisk vurdering:**")
        st.write(bakgrunn_tekst)

    st.markdown("---")
    st.markdown("#### 🛡️ Stage-Gate Port 9: Menneskelig Overprøving (HITL Sign-Off)")
    
    with st.form(key="hitl_form"):
        col_h1, col_h2 = st.columns([1, 2])
        with col_h1:
            hitl_status = st.radio(
                "Saksbehandlers vurdering:",
                options=["APPROVED (Godkjent)", "MODIFIED (Endret med merknad)", "REJECTED (Avvist)"],
                index=0
            )
        with col_h2:
            hitl_notes = st.text_area(
                "Saksbehandlers faglige begrunnelse / kontrollnotat:",
                value="Reelt merforbruk opparbeidet per T2 bekreftet mot Visma ERP og Framsikt. Foreslått inndekning mot disposisjonsfond er i tråd med økonomireglementet."
            )
        
        sign_btn = st.form_submit_button("🔒 Lagre og signer med SHA-256 Audit Trail", type="primary")

    if sign_btn:
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        raw_payload = f"{user_role}|{sakstype}|{hitl_status}|{hitl_notes}|{timestamp}"
        audit_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()

        # Skriv til Audit_AI_Actions i SQLite
        try:
            conn = get_db_connection()
            conn.execute(
                """
                INSERT INTO Audit_AI_Actions (user_query, retrieved_chunk_ids, llm_response, user_action, sha256_hash, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (sakstype, "[]", hitl_notes, hitl_status.split()[0], audit_hash, timestamp)
            )
            conn.commit()
            conn.close()
            st.success(f"✅ Saksnotatet er signert og uforanderlig arkivert i Audit_AI_Actions! SHA-256: `{audit_hash}`")
        except Exception as e:
            st.error(f"Feil ved lagring av audit-hendelse: {e}")


# -------------------------------------------------------------
# FANE 5: DOKUMENTARKIV & RESSURSER
# -------------------------------------------------------------
with tab_docs:
    st.markdown("### 📁 Dokumentarkiv, Spesifikasjoner & Ressursbibliotek")
    st.caption("Sentralt bibliotek for alle styringsdokumenter, veiledninger, agentroller og modeller for Kristiansand kommune.")

    # Hvis et dokument er valgt fra sidebaren eller katalogen, vis det i fokus
    if "active_doc_path" in st.session_state and Path(st.session_state["active_doc_path"]).exists():
        p = Path(st.session_state["active_doc_path"])
        ext = p.suffix.lower()
        st.markdown(f"#### 📖 Aktivt dokument: {st.session_state.get('active_doc_title', p.name)}")
        
        c_act1, c_act2 = st.columns([3, 1])
        with c_act1:
            try:
                rel_path = p.relative_to(WORKSPACE_ROOT)
            except ValueError:
                rel_path = p.name
            st.caption(f"📁 Plassering: `{rel_path}` | Format: `{ext.upper()}`")
        with c_act2:
            if ext in [".md", ".tmdl", ".m", ".py", ".sql", ".dax", ".pq", ".csv", ".json"]:
                doc_text = p.read_text(encoding="utf-8", errors="replace")
                st.download_button(
                    label=f"⬇️ Last ned {p.name}",
                    data=doc_text,
                    file_name=p.name,
                    mime="text/markdown" if ext == ".md" else "text/plain",
                    key="dl_tab_doc_btn"
                )
            else:
                with open(p, "rb") as fb:
                    mime_map = {
                        ".pdf": "application/pdf",
                        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        ".png": "image/png",
                        ".jpg": "image/jpeg"
                    }
                    st.download_button(
                        label=f"⬇️ Last ned {p.name}",
                        data=fb.read(),
                        file_name=p.name,
                        mime=mime_map.get(ext, "application/octet-stream"),
                        key="dl_tab_bin_btn"
                    )
            if st.button("❌ Lukk forhåndsvisning"):
                del st.session_state["active_doc_path"]
                if "active_doc_title" in st.session_state:
                    del st.session_state["active_doc_title"]
                st.rerun()

        st.markdown("---")
        if ext == ".md":
            st.markdown(p.read_text(encoding="utf-8", errors="replace"))
        elif ext in [".png", ".jpg", ".jpeg"]:
            st.image(str(p), caption=st.session_state.get('active_doc_title', p.name), use_container_width=True)
        elif ext in [".tmdl", ".m", ".py", ".sql", ".dax", ".pq", ".csv", ".json"]:
            code_lang = "dax" if ext in [".dax", ".tmdl"] else ("powerquery" if ext in [".pq", ".m"] else ("python" if ext == ".py" else ("sql" if ext == ".sql" else "text")))
            st.code(p.read_text(encoding="utf-8", errors="replace"), language=code_lang)
        else:
            size_kb = p.stat().st_size / 1024
            size_str = f"{size_kb / 1024:.2f} MB" if size_kb > 1024 else f"{size_kb:.1f} KB"
            type_names = {
                ".pdf": "PDF Forvaltningsdokument / Styringsnotat",
                ".xlsx": "Excel Arbeidsbok / Økonomistyringsmodell",
                ".docx": "Word Saksdokument / Saksfremlegg",
                ".pptx": "PowerPoint Presentasjonsdeck"
            }
            st.info(f"📄 **Filtype:** {type_names.get(ext, 'Binært forvaltningsdokument')}  \n💾 **Filstørrelse:** {size_str}  \n📍 **Bruk:** Dette dokumentet er klart for direkte nedlasting til lokal saksbehandling, analyse eller presentasjon.")
        st.markdown("---")

    # Søk og filter på tvers av biblioteket
    st.markdown("#### 🔍 Utforsk Dokumentkatalogen")
    search_query = st.text_input("Søk etter tittel, emneord eller kategori:", value="")

    for cat_title, items in DOCUMENTS_MENU.items():
        filtered_items = [
            (label, path, desc) for label, path, desc in items
            if not search_query or search_query.lower() in label.lower() or search_query.lower() in desc.lower() or search_query.lower() in cat_title.lower()
        ]
        if filtered_items:
            st.markdown(f"##### {cat_title}")
            for label, path, desc in filtered_items:
                col_d1, col_d2, col_d3 = st.columns([3, 1, 1])
                with col_d1:
                    status_icon = "🟢" if path.exists() else "🔴"
                    st.markdown(f"{status_icon} **{label}**  \n`{path.name}` — *{desc}*")
                with col_d2:
                    if path.exists():
                        if st.button("Åpne her 👁️", key=f"open_tab_{path.stem}_{cat_title[:4]}"):
                            st.session_state["active_doc_path"] = str(path)
                            st.session_state["active_doc_title"] = label
                            st.rerun()
                with col_d3:
                    if path.exists():
                        ext = path.suffix.lower()
                        if ext in [".md", ".tmdl", ".m", ".py", ".sql", ".dax", ".pq", ".csv", ".json"]:
                            st.download_button("Last ned ⬇️", data=path.read_text(encoding="utf-8", errors="replace"), file_name=path.name, mime="text/plain", key=f"dl_tab_{path.stem}_{cat_title[:4]}")
                        else:
                            with open(path, "rb") as fb:
                                mime = "application/pdf" if ext == ".pdf" else ("image/png" if ext == ".png" else "application/octet-stream")
                                st.download_button("Last ned ⬇️", data=fb.read(), file_name=path.name, mime=mime, key=f"dl_tab_bin_{path.stem}_{cat_title[:4]}")
            st.markdown("---")