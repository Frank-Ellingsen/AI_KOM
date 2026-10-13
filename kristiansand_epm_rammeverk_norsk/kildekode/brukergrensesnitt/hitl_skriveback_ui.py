"""
============================================================================
KRISTIANSAND KOMMUNE - HUMAN-IN-THE-LOOP (HITL) WRITE-BACK UI
Purpose: Glass-box AI audit, review, and human sign-off application.
Stack: Streamlit + SQLite Golden Record (kristiansand_golden_record.db)
============================================================================
"""

import sqlite3
import datetime
import json
import pandas as pd
import streamlit as st

DB_PATH = "kristiansand_golden_record.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_audit_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Audit_AI_Actions (
        action_id TEXT PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id TEXT NOT NULL,
        sektor TEXT NOT NULL,
        enhet TEXT NOT NULL,
        kostra_art TEXT NOT NULL,
        ai_reasoning_chain TEXT NOT NULL,
        ai_recommended_action TEXT NOT NULL,
        confidence_score REAL NOT NULL,
        governance_reference TEXT NOT NULL,
        user_action TEXT NOT NULL CHECK (user_action IN ('APPROVED', 'REJECTED', 'MODIFIED')),
        user_notes TEXT,
        status TEXT DEFAULT 'COMPLETED'
    );
    """)
    conn.commit()
    conn.close()

# Initialize Page Config
st.set_page_config(
    page_title="Kristiansand Kommune - HITL AI Governance Portal",
    page_icon="🏛️",
    layout="wide"
)

init_audit_table()

st.title("🏛️ Kristiansand Kommune — AI Glass-Box & HITL Sign-off Portal")
st.markdown("**Styremodell:** Stage-Gate 3 (Human-in-the-Loop) | EU AI Act Art. 14 Oversight | GDPR Art. 35 DPIA")

st.divider()

# Sidebar: User Authentication Context
st.sidebar.header("👤 Saksbehandler Identitet")
user_name = st.sidebar.text_input("Saksbehandler / Rådgiver", "Frank Ellingsen")
user_role = st.sidebar.selectbox("Rolle / Fullmakt", ["Rådgiver Økonomi", "Enhetsleder Skole", "Enhetsleder Boenhet", "Kommunalsjef"])
sektor_select = st.sidebar.selectbox("Sektor", ["Oppvekst", "Helse og mestring", "By- og stedsutvikling"])

# Section 1: Active Variance Case Review
st.subheader("1. Velg Registrert Avvikssak for AI-Diagnose")

cases = {
    "CASE-2026-001": {
        "Enhet": "Kommunal Skole",
        "Sektor": "Oppvekst",
        "KOSTRA_Art": "1020 Sykemeldte vikarer",
        "YTD_Avvik": 47000.0,
        "Budsjett_YTD": 30000.0,
        "Regnskap_YTD": 77000.0,
        "Related_Art_1690": -25000.0,
        "AI_Reasoning": [
            "1. Art 1020 (Sykemeldte vikarer) viser et akkumulert merforbruk på +kr 47 000 per T1.",
            "2. Koblet analyse mot Art 1690 (NAV-refusjon) avdekker uinntektsført refusjon på kr 25 000 som følge av forsinkelser i Visma ERP-omleggingen.",
            "3. Underliggende reell merbelastning på vikarbruk er reduktivt kr 22 000 (innenfor 5 % akseptabel driftsmargin).",
            "4. Ingen faste stillingshjemler er overskredet."
        ],
        "AI_Action": "Opprett formell purring mot NAV for ubetalt refusjon (art 1690). Omdisponer kr 22 000 fra ubenyttet lønnsreserve på art 1010.",
        "Governance_Ref": "Kommuneloven § 14-6 (Bruttoprinsippet) & KOSTRA Veileder Art 1690",
        "Confidence": 0.94
    },
    "CASE-2026-002": {
        "Enhet": "Kommunal Boenhet",
        "Sektor": "Helse og mestring",
        "KOSTRA_Art": "1090 Overtid helgetillegg",
        "YTD_Avvik": 117000.0,
        "Budsjett_YTD": 60000.0,
        "Regnskap_YTD": 177000.0,
        "Related_Art_1690": -40000.0,
        "AI_Reasoning": [
            "1. Art 1090 (Overtid) viser kritisk avvik på +kr 117 000 (+195 % mot periodisert budget).",
            "2. Turnusanalysen indikerer 24/7-dekning ved vakanser og sammensatte brukerbehov i helgeadministrasjon.",
            "3. Høy vikarinnleie fra eksterne byråer har forsterket avviket.",
            "4. NAV-refusjon etterslep er estimert til kr 40 000."
        ],
        "AI_Action": "Aktiver kommunal intern vikarpool for helgedekning T2. Fremme sak for kommunalsjef om rammeregulering dersom brukerpågang vedvarer.",
        "Governance_Ref": "Arbeidsmiljøloven § 10-6 & Delegeringsreglementet Kristiansand Kommune",
        "Confidence": 0.89
    }
}

selected_case_id = st.selectbox("Velg sak fra oversikten:", list(cases.keys()))
case_data = cases[selected_case_id]

# Display Case Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Enhet", case_data["Enhet"])
col2.metric("KOSTRA Art", case_data["KOSTRA_Art"])
col3.metric("YTD Avvik", f"kr {case_data['YTD_Avvik']:,.0f}")
col4.metric("NAV Etterslep (Art 1690)", f"kr {case_data['Related_Art_1690']:,.0f}")

st.divider()

# Section 2: Transparent AI Glass-Box Explanation
st.subheader("2. 🔍 AI Glass-Box Årsaksforklaring & RAG-Begrunnelse")

with st.expander("Se AI-modellens stegvis resonneringsrekke (Ingen Black Box)", expanded=True):
    st.write("**Forklaringskjede (Chain of Thought):**")
    for step in case_data["AI_Reasoning"]:
        st.write(f"- {step}")
    
    st.info(f"📜 **Regelverksforankring (RAG):** {case_data['Governance_Ref']}")
    st.caption(f"🤖 **Modellens konfidensscore:** {case_data['Confidence']*100:.1f} %")

st.divider()

# Section 3: Human Sign-off and Action Execution Form
st.subheader("3. ✍️ Saksbehandlers Beslutning & Sign-off (HITL)")

with st.form("hitl_signoff_form"):
    st.write(f"**Anbefalt administrative tiltak:** {case_data['AI_Action']}")
    
    user_action = st.radio(
        "Velg din beslutning som saksbehandler:",
        ["APPROVED", "MODIFIED", "REJECTED"],
        format_func=lambda x: {
            "APPROVED": "✅ Godkjenn tiltak (Full overensstemmelse)",
            "MODIFIED": "✏️ Godkjenn med modifikasjoner",
            "REJECTED": "❌ Avvis tiltak (Krever begrunnelse)"
        }[x]
    )
    
    user_notes = st.text_area(
        "Saksbehandlers begrunnelse / Notat til revisjonssporet:",
        placeholder="Skriv inn kommentar om lokal kontekst, vurdering eller endring i tiltaket..."
    )
    
    submitted = st.form_submit_button("🔒 Bekreft og Før i Audit Trail")

if submitted:
    action_id = f"ACT-{datetime.datetime.now().strftime('%Y%m%m%H%M%S')}"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Audit_AI_Actions (
            action_id, user_id, sektor, enhet, kostra_art,
            ai_reasoning_chain, ai_recommended_action, confidence_score,
            governance_reference, user_action, user_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        action_id, user_name, case_data["Sektor"], case_data["Enhet"], case_data["KOSTRA_Art"],
        json.dumps(case_data["AI_Reasoning"]), case_data["AI_Action"], case_data["Confidence"],
        case_data["Governance_Ref"], user_action, user_notes
    ))
    conn.commit()
    conn.close()
    st.success(f"Saken er behandlet og signert av {user_name}! Unik Audit ID: `{action_id}` er registrert i `Audit_AI_Actions`.")

st.divider()

# Section 4: Display Audit Log
st.subheader("4. 📋 Offisiell Audit Trail Logg (SQLite Golden Record)")
conn = get_db_connection()
df_audit = pd.read_sql_query("SELECT action_id, timestamp, user_id, enhet, user_action, user_notes FROM Audit_AI_Actions ORDER BY timestamp DESC", conn)
conn.close()

st.dataframe(df_audit, use_container_width=True)
