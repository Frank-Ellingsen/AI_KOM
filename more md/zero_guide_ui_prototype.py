"""
Økonomi_KOM - Null-Manual Grensesnitt (Interactive Prototype)
Kristiansand Kommune Financial Control UI
"""

import hashlib
import json
import re
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="Økonomi_KOM Null-Manual UI", layout="wide")

# Custom CSS for Zero-Guide Clean UI
st.markdown("""
<style>
    .header-box {
        background-color: #002B49;
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .welcome-box {
        background-color: #E3F2FD;
        border-left: 5px solid #1565C0;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    .red-card {
        background-color: #FFEBEE;
        border: 2px solid #EF5350;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .green-card {
        background-color: #E8F5E9;
        border: 1.5px solid #81C784;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .tooltip-box {
        background-color: #FFF8E1;
        border: 1px solid #FFE082;
        padding: 10px;
        border-radius: 4px;
        font-size: 0.9em;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar
st.markdown("""
<div class="header-box">
    <h2 style="margin:0; color:white;">🏛️ Kristiansand kommune — Økonomi_KOM</h2>
    <p style="margin:5px 0 0 0; color:#E2EFDA; font-size:0.9em;">Null-Manual Brukergrensesnitt for Enhetsledere (Zero-Guide Context UI)</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Simulation
st.sidebar.header("🔑 Brukerprofil (SSO Auto-Detect)")
user_person = st.sidebar.selectbox("Simuler Innlogging", [
    "Kari Nordmann — Enhetsleder (Ansvar 5200 Sykehjem)",
    "Ola Hansen — Enhetsleder (Ansvar 2100 Barnehage)",
    "Per Olsen — Controller (Sektor Helse og mestring)"
])

if "5200" in user_person:
    role_type = "enhetsleder_red"
elif "2100" in user_person:
    role_type = "enhetsleder_green"
else:
    role_type = "controller"

st.markdown(f"""
<div class="welcome-box">
    <h4 style="margin:0; color:#0D47A1;">Velkommen tilbake!</h4>
    <p style="margin:5px 0 0 0; color:#1565C0;">
        <b>Identifisert enhet:</b> {user_person.split('—')[1]} | <b>Status for Måned 8:</b> Automatisk synkronisert fra Visma & Framsikt.
    </p>
</div>
""", unsafe_allow_html=True)

# UI Display based on Exception State
if role_type == "enhetsleder_red" or role_type == "controller":
    st.subheader("⚠️ Unntaksbasert Triage (Management by Exception)")
    
    st.markdown("""
    <div class="red-card">
        <span style="background-color:#D32F2F; color:white; padding:4px 10px; border-radius:4px; font-weight:bold; font-size:0.85em;">🔴 AVVIK OPPDAGET</span>
        <h3 style="color:#B71C1C; margin:10px 0 5px 0;">Sykehjem & Helsehus har et projisert merforbruk på -350 000 kr i M8</h3>
        <p style="margin:0; color:#333;"><b>Årsbudsjett:</b> 145,0 MNOK &nbsp;|&nbsp; <b>Forbruk YTD:</b> 101,8 MNOK &nbsp;|&nbsp; <b>Projisert Årsavslutning:</b> 145,35 MNOK</p>
        <p style="margin-top:8px; color:#555;"><b>Hovedårsak:</b> Vikar- og overtidskostnader (Art 1090) fanges opp mot forsinkede NAV-sykelønnsrefusjoner (Art 1600).</p>
        <div class="tooltip-box">
            ℹ️ <b>Juridisk regel (Kommuneloven § 14-5):</b> Ved merforbruk plikter kommunedirektøren å fremme sak om inndekning eller omdisponering for Formannskapet.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📝 1-Klikk Løsning: Generer og Godkjenn Avviksnotat til Formannskapet"):
        st.write("**AI-Generert Utkast til Saksfremlegg:**")
        default_text = "Enheten viser et merforbruk på 350 000 kr i M8 grunnet vikarbruk. Refusjoner fra NAV (Art 1600) forventes godskrevet i Q4."
        saksnotat = st.text_area("Rediger notat om nødvendig (Innebygget GDPR Port 4 PII-skjerming):", default_text)
        
        # Local PII Scrub check
        clean_text = re.sub(r'\b\d{6}\s?\d{5}\b', '[SKJERMET_FNR]', saksnotat)
        
        if st.button("⚡ Godkjenn og Send til Formannskapet (SHA-256 Revisorstempel)"):
            timestamp = datetime.now().isoformat()
            hash_seal = hashlib.sha256(f"{timestamp}|{user_person}|APPROVED|{clean_text}".encode('utf-8')).hexdigest()
            
            st.success("✅ Saksnotat godkjent og registrert!")
            st.json({
                "Tidsstempel": timestamp,
                "Saksbehandler": user_person,
                "Status": "GODKJENT_FOR_FORMANNSKAPET",
                "SHA256_Revisorstempel": hash_seal
            })

if role_type == "enhetsleder_green" or role_type == "controller":
    if role_type == "controller":
        st.markdown("---")
        st.subheader("🟢 Balanserte Enheter (Automatisk Arkivert)")

    st.markdown("""
    <div class="green-card">
        <span style="background-color:#388E3C; color:white; padding:4px 10px; border-radius:4px; font-weight:bold; font-size:0.85em;">🟢 BALANSE</span>
        <h3 style="color:#1B5E20; margin:10px 0 5px 0;">Barnehager & Oppvekst (Ansvar 2100) er i full budsjettbalanse</h3>
        <p style="margin:0; color:#2E7D32;"><b>Disponibelt i år:</b> +1,2 MNOK. Ingen tiltak kreves.</p>
        <p style="margin-top:5px; font-size:0.9em; color:#555;">Månedsoppgjør arkiveres automatisk i bakgrunnen med SHA-256 revisjonsstempel. Leder forstyrres ikke.</p>
    </div>
    """, unsafe_allow_html=True)

st.caption("🔒 GDPR Port 4 PII-skjerming Aktiv  |  🛡️ EU AI Act Art. 14 Revisorstempel Genereres Automatisk")
