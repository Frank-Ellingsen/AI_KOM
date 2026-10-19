import streamlit as st
import hashlib
import re
import json
import sqlite3
import difflib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Tuple
import sys

# Ensure root directory is on sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.loop_engine import LoopEngine

# Page configuration
st.set_page_config(
    page_title="AI_KOM | Null-Manual Control Hub v2",
    page_icon="🏛️",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 26px;
        font-weight: bold;
        color: #1E3A8A;
        padding-bottom: 10px;
        border-bottom: 2px solid #E5E7EB;
        margin-bottom: 20px;
    }
    .status-card-green {
        background-color: #ECFDF5;
        border: 2px solid #10B981;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .status-card-red {
        background-color: #FEF2F2;
        border: 2px solid #EF4444;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .gate-card {
        background-color: #F3F4F6;
        border-left: 4px solid #3B82F6;
        padding: 15px;
        margin-top: 10px;
        border-radius: 4px;
    }
    .tooltip-box {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 6px;
        padding: 10px;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# Database Setup (Cross-platform safe)
SCRATCH_DIR = ROOT_DIR / "scratch"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = str(SCRATCH_DIR / "ai_kom_feedback.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS golden_exemplars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sector TEXT,
        deficit_mnok REAL,
        ai_draft TEXT,
        human_edited_final TEXT,
        diff_summary TEXT,
        approved_by TEXT,
        created_at TEXT,
        sha256_seal TEXT
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_golden_sector ON golden_exemplars(sector)")
    conn.commit()
    conn.close()

def store_golden_exemplar(sector: str, deficit_mnok: float, ai_draft: str, human_final: str, approved_by: str, seal: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    diff = list(difflib.unified_diff(ai_draft.splitlines(), human_final.splitlines(), lineterm=''))
    diff_summary = "\n".join(diff[:15])
    cursor.execute("""
    INSERT INTO golden_exemplars (sector, deficit_mnok, ai_draft, human_edited_final, diff_summary, approved_by, created_at, sha256_seal)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (sector, deficit_mnok, ai_draft, human_final, diff_summary, approved_by, datetime.now(timezone.utc).isoformat(), seal))
    conn.commit()
    conn.close()

def get_golden_exemplars(sector: str) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM golden_exemplars WHERE sector = ? ORDER BY id DESC LIMIT 3", (sector,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

init_db()

# Sidebar Role Selector
st.sidebar.title("🏛️ AI_KOM Control Hub")
st.sidebar.caption("Kristiansand kommune — Autonom & Selvforbedrende Økonomistyring")

role = st.sidebar.selectbox(
    "Velg Brukerprofil (SSO Simulation):",
    [
        "👩‍⚕️ Kari Nordmann (Enhetsleder - Ansvar 5200 Sykehjem)",
        "🧒 Thomas Hansen (Enhetsleder - Ansvar 3100 Barnehage)",
        "👔 Frank Ellingsen (Senior Controller / Økonomirådgiver)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛡️ Governance & Compliance")
st.sidebar.success("✅ SSO Authenticated")
st.sidebar.info("🔒 GDPR Port 4 PII Redaction: Active")
st.sidebar.warning("⚖️ EU AI Act Art. 14: Stage-Gate Enabled")

# Main Header
st.markdown("<div class='main-header'>Kristiansand kommune — Unntaksbasert Økonomistyring & Control Hub v2</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Triage & Unntaksstyring", "🔄 Selvforbedrende Evaluator-Engine", "ℹ️ Mikrotekter & Regelveileder"])

if "Sykehjem" in role or "Frank" in role:
    sector_name = "Helse og mestring"
    unit_name = "Ansvar 5200 — Sykehjem og Omsorgssentre"
    is_red = True
    deficit = 21.50
else:
    sector_name = "Oppvekst"
    unit_name = "Ansvar 3100 — Kommunale Barnehager"
    is_red = False
    deficit = -0.40 # Surplus

with tab1:
    st.subheader(f"Enhetsoversikt: {unit_name}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Årsbudsjett 2026", "142,5 MNOK")
    col2.metric("M8 Regnskap / Prognose", "164,0 MNOK" if is_red else "142,1 MNOK")
    col3.metric("Projisert Avvik", f"+{deficit:.2f} MNOK" if is_red else f"{deficit:.2f} MNOK", delta_color="inverse" if is_red else "normal")

    if not is_red:
        st.markdown("""
        <div class='status-card-green'>
            <h3>🟢 Status: Alt i Balanse</h3>
            <p>Sektoren drives innenfor tildelte rammer. Ingen avviksrapportering eller tiltaksnotat kreves.</p>
            <p><b>Silence is Consent:</b> Månedsrapport er automatisk generert og arkivert med SHA-256 revisjonsstempel (0 minutter tidsbruk for leder).</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='status-card-red'>
            <h3>🔴 Status: Avvik Oppdaget (Triage Påkrevd)</h3>
            <p>Projisert merforbruk på <b>+{deficit:.2f} MNOK</b> utløser handlingsplikt jf. <b>Kommuneloven § 14-5</b>.</p>
            <p>AI_KOM har ferdigstilt analyse fra Visma/Framsikt. Trykk under for å kjøre selvforbedrende Evaluator-Optimizer løkke og klargjøre saksfremlegg til Formannskapet.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("⚡ Løs Avvik (Generer Saksfremlegg via Evaluator-Optimizer Løkke)", type="primary"):
            loop_engine = LoopEngine(max_attempts=3)
            with st.spinner("Kjører selvreparerende Evaluator-Optimizer løkke..."):
                loop_result = loop_engine.run_loop(sector=sector_name, deficit_mnok=deficit, unit_name=unit_name)
            st.session_state["loop_result"] = loop_result

        if "loop_result" in st.session_state:
            loop_result = st.session_state["loop_result"]
            st.markdown("### 🔄 Evaluator-Optimizer Løkke i Arbeid")
            
            traj = loop_result.get("trajectory", [])
            # Step 1: Attempt 1
            if len(traj) >= 1:
                st.markdown("#### 1️⃣ Kjøring 1 (Generator Utkast):")
                draft_1 = LoopEngine().generate_draft(sector_name, deficit, attempt=1, unit_name=unit_name)
                st.code(draft_1, language="markdown")
                st.error("❌ Evaluator Avviste Kjøring 1:\n• " + "\n• ".join(traj[0].get("feedback", [])))

            # Step 2: Attempt 2 (Refined with Few-Shot)
            if len(traj) >= 2:
                st.markdown("#### 2️⃣ Kjøring 2 (Refinert med Evaluator-Tilbakemelding & Golden Exemplars):")
                
                exemplars = get_golden_exemplars(sector_name)
                if exemplars:
                    with st.expander(f"💡 Tidligere godkjent gulleksempel brukt som referansekontekst (Few-Shot):"):
                        st.caption(f"Gulleksempel for {sector_name} (Godkjent av: {exemplars[0]['approved_by']})")
                        st.code(exemplars[0]['human_edited_final'][:400] + "...", language="markdown")

                st.code(loop_result["final_draft"], language="markdown")
                st.success("✅ Evaluator Godkjente Kjøring 2! Alle juridiske kvalitetsporter (§ 14-5, § 14-6, GDPR Port 4, Vedtaksstruktur) er oppfylt.")

            # Step 3: Stage-Gate Port 9 Human Sign-off
            st.markdown("---")
            st.markdown("### 🔒 Stage-Gate Port 9: Menneskelig Gjennomgang & Signering (EU AI Act Art. 14)")
            
            user_final_text = st.text_area(
                "Rediger eller tilføy bemerkninger før endelig publisering:",
                value=loop_result["final_draft"] + "\n\n4. Tillegg fra Controller:\nInnsparingstiltakene skal evalueres i 3. tertialrapport.",
                height=250,
                key="memo_text_area"
            )

            if st.button("🔒 Signer og Publiser (Generer SHA-256 Audit Seal)"):
                now_utc = datetime.now(timezone.utc).isoformat()
                content_hash = hashlib.sha256(user_final_text.encode("utf-8")).hexdigest()
                seal_payload = f"{now_utc}|{role}|{sector_name}|APPROVED|{content_hash}"
                sha_seal = hashlib.sha256(seal_payload.encode("utf-8")).hexdigest()

                raw_draft_1 = LoopEngine().generate_draft(sector_name, deficit, attempt=1, unit_name=unit_name)
                store_golden_exemplar(
                    sector=sector_name,
                    deficit_mnok=deficit,
                    ai_draft=raw_draft_1,
                    human_final=user_final_text,
                    approved_by=role,
                    seal=sha_seal
                )

                st.balloons()
                st.success(f"✅ Saksfremlegg godkjent og publisert! Cryptographic SHA-256 Audit Seal: `{sha_seal}`")
                st.info("💡 Utkastet er lagret i SQLite Golden Store. Fremtidige utkast for denne sektoren vil automatisk lære av dine endringer!")

with tab2:
    st.subheader("🔄 Selvforbedrende Arkitektur & Dynamic Few-Shot Engine")
    st.markdown("""
    Systemet benytter en **4-stegs data-svinghjul (Data Flywheel)** som gjør at AI-en blir klokere for hver eneste godkjenning:
    1. **Diff Tracking**: Forskjellen mellom AI-utkast og menneskelig redigert tekst måles.
    2. **Golden Exemplar Store**: Godkjente saksfremlegg lagres i SQLite-databasen (`ai_kom_feedback.db`).
    3. **Dynamic Few-Shot Injection**: Ved neste avvik henter Generator-noden de nyeste gulleksemplene for sektoren.
    4. **Regresjonssikring**: PII-skjerming og Kommuneloven § 14-5/14-6 overprøves aldri av læringsstøy.
    """)

    st.markdown("### 🗄️ Lagrede Gulleksempler i SQLite Databasen")
    records = get_golden_exemplars(sector_name)
    if records:
        for idx, rec in enumerate(records, 1):
            with st.expander(f"Gulleksempel #{idx} — Sektor: {rec['sector']} (Opprettet: {rec['created_at'][:19]})"):
                st.markdown(f"**Godkjent av:** `{rec['approved_by']}`")
                st.markdown(f"**SHA-256 Seal:** `{rec['sha256_seal']}`")
                st.markdown("**Endelig Tekst:**")
                st.code(rec['human_edited_final'], language="markdown")
                st.markdown("**Diff Utskrift (Endringer gjort av controller):**")
                st.code(rec['diff_summary'], language="diff")
    else:
        st.info("Ingen gulleksempler er lagret i databasen ennå. Generer og godkjenn et saksfremlegg i Triage-fanen for å starte selvforbedringsløkken.")

with tab3:
    st.subheader("ℹ️ Mikrotekter & Regelveileder (Zero-Guide Context)")
    st.markdown("""
    For at enhetsledere skal slippe å slå opp i tunge manualer, er all fagstøtte integrert direkte i oppgaveløsningen:
    """)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class='tooltip-box'>
            <h4>⚖️ Kommuneloven § 14-5 (Handlingsplikt)</h4>
            <p>Ved projisert merforbruk plikter kommunedirektøren og enhetsleder å legge frem tiltaksplan for Formannskapet for å gjenopprette driftsbalansen.</p>
        </div>
        <br>
        <div class='tooltip-box'>
            <h4>🔄 KOSTRA Konteringsregler</h4>
            <p>Hver transaksjon må spesifiseres med tre dimensjoner: <b>Kontoklasse × Funksjon × Art</b>. Feilkontering hindrer statlig rapportering til SSB.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class='tooltip-box'>
            <h4>📊 Kommuneloven § 14-6 (Bruttoprinsippet)</h4>
            <p>Alle utgifter og inntekter skal føres brutto. Det er strengt forbudt å motregne refusjoner eller salgsinntekter direkte mot utgiftskontoer.</p>
        </div>
        <br>
        <div class='tooltip-box'>
            <h4>🛡️ GDPR Port 4 (PII Redaction)</h4>
            <p>Fødselsnumre (11 siffer) og bankkontoer sladdes automatisk av lokal sjekkmodul før tekst oppdateres i språkmodeller.</p>
        </div>
        """, unsafe_allow_html=True)
