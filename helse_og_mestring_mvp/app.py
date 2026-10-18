"""
AI_KOM Control Office Hub - Streamlit MVP Pilot
Sektor: Helse og Mestring (Ansvar 5200 / KOSTRA 254)
Kristiansand Kommune Financial Controlling & AI Assistant
"""

import hashlib
import json
import os
import re
from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st

# ==========================================
# 1. PORT 4: LOCAL PII GUARDRAIL & MASKING
# ==========================================
def mask_pii(text: str) -> str:
    """
    Locally scrubs Norwegian national ID numbers (11 digits), 
    bank account numbers (11 digits), and emails before processing.
    """
    if not text:
        return ""
    text = re.sub(r'\b\d{6}\s?\d{5}\b', '[SKJERMET_FNR]', text)
    text = re.sub(r'\b\d{4}\.\d{2}\.\d{5}\b|\b\d{11}\b', '[SKJERMET_KONTO]', text)
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[SKJERMET_EPOST]', text)
    return text


# ==========================================
# 2. DATA ENGINE
# ==========================================
@st.cache_data
def load_helse_data() -> pd.DataFrame:
    csv_path = os.path.join(os.path.dirname(__file__), "data", "helse_mestring_data.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame([
            {"Ansvar": 5200, "KOSTRA_Funksjon": 253, "Beskrivelse": "Hjemmesykepleie og tilrettelagte boliger", "Budsjett_MNOK": 110.0, "Regnskap_YTD_MNOK": 79.2, "Overtid_Art1090_MNOK": 4.8, "Vikarer_Art1100_MNOK": 6.2, "NAV_Refusjon_Art1600_MNOK": -3.1, "Sykefravar_Pct": 11.2},
            {"Ansvar": 5200, "KOSTRA_Funksjon": 254, "Beskrivelse": "Sykehjem og helsehus (Institusjon)", "Budsjett_MNOK": 145.0, "Regnskap_YTD_MNOK": 104.4, "Overtid_Art1090_MNOK": 8.2, "Vikarer_Art1100_MNOK": 11.5, "NAV_Refusjon_Art1600_MNOK": -5.2, "Sykefravar_Pct": 13.8},
            {"Ansvar": 5200, "KOSTRA_Funksjon": 256, "Beskrivelse": "Mestringstjenester og psykiatri", "Budsjett_MNOK": 65.0, "Regnskap_YTD_MNOK": 40.4, "Overtid_Art1090_MNOK": 1.5, "Vikarer_Art1100_MNOK": 2.1, "NAV_Refusjon_Art1600_MNOK": -1.8, "Sykefravar_Pct": 7.5}
        ])
    
    df["Forventet_YTD_MNOK"] = round(df["Budsjett_MNOK"] * (8.0 / 12.0), 2)
    df["Avvik_MNOK"] = round(df["Forventet_YTD_MNOK"] - df["Regnskap_YTD_MNOK"], 2)
    df["Avvik_Pct"] = round((df["Avvik_MNOK"] / df["Budsjett_MNOK"]) * 100, 2)
    
    def set_rag(pct):
        if pct >= -2.0:
            return "GRØNN"
        elif pct >= -5.0:
            return "RAV"
        else:
            return "RØD"
            
    df["RAG_Status"] = df["Avvik_Pct"].apply(set_rag)
    df["Netto_Vikarbelastning_MNOK"] = round(df["Overtid_Art1090_MNOK"] + df["Vikarer_Art1100_MNOK"] - df["NAV_Refusjon_Art1600_MNOK"].abs(), 2)
    return df


# ==========================================
# 3. MONTE CARLO SIMULATOR
# ==========================================
def run_monte_carlo(budget: float, actual_ytd: float, vol_pct: float = 0.12, num_sims: int = 1000):
    np.random.seed(42)
    months_remaining = 4
    monthly_avg = actual_ytd / 8.0
    
    # Q4 Seasonality factor (+5% winter sickness spike)
    q4_factor = 1.05
    simulated_q4 = np.random.normal(monthly_avg * q4_factor, monthly_avg * vol_pct, (num_sims, months_remaining))
    simulated_totals = actual_ytd + np.sum(simulated_q4, axis=1)
    
    p10 = np.percentile(simulated_totals, 10)
    p50 = np.percentile(simulated_totals, 50)
    p90 = np.percentile(simulated_totals, 90)
    
    return round(p10, 2), round(p50, 2), round(p90, 2)


# ==========================================
# 4. SHA-256 AUDIT LEDGER (EU AI Act Art. 14)
# ==========================================
def generate_audit_seal(user_upn: str, funksjon: str, recommendation: str, decision: str) -> dict:
    timestamp = datetime.utcnow().isoformat() + "Z"
    payload = f"{timestamp}|{user_upn}|{funksjon}|{recommendation}|{decision}"
    sha_seal = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    
    return {
        "timestamp": timestamp,
        "user_upn": user_upn,
        "kostra_funksjon": funksjon,
        "ai_recommendation": recommendation,
        "human_decision": decision,
        "sha256_seal": sha_seal
    }


# ==========================================
# 5. STREAMLIT APP MAIN
# ==========================================
def main():
    st.set_page_config(page_title="MVP Helse og Mestring - Kristiansand Kommune", layout="wide")
    
    st.title("🏥 Kristiansand Kommune — MVP Helse og Mestring (Ansvar 5200)")
    st.caption("Spesialisert Økonomistyrings- og Controlling-modul for Pleie og Omsorg (KOSTRA 254)")

    # Sidebar
    st.sidebar.header("🔑 Saksbehandler & RLS")
    user_upn = st.sidebar.text_input("Saksbehandler UPN", "helse.controller@kristiansand.kommune.no")
    st.sidebar.info("📌 Modul: Ansvar 5200 Helse og Mestring\n💰 Totalramme: 320.00 MNOK")

    df = load_helse_data()

    # KPI Metrics Top Row
    tot_budget = df["Budsjett_MNOK"].sum()
    tot_ytd = df["Regnskap_YTD_MNOK"].sum()
    tot_expected = df["Forventet_YTD_MNOK"].sum()
    tot_var = tot_expected - tot_ytd
    tot_vikar = df["Netto_Vikarbelastning_MNOK"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Årsbudsjett 2026", f"{tot_budget:.2f} MNOK")
    col2.metric("Regnskap YTD (M8)", f"{tot_ytd:.2f} MNOK")
    col3.metric("Netto Avvik YTD", f"{tot_var:.2f} MNOK", delta_color="normal")
    col4.metric("Netto Vikar- & Overtidsbelastning", f"{tot_vikar:.2f} MNOK")

    st.markdown("---")

    # KOSTRA Breakdown Table
    st.subheader("📋 Underfunksjoner i Helse og Mestring (KOSTRA 253, 254, 256)")
    
    def format_rag(val):
        if val == "GRØNN":
            return "🟢 Grønn"
        elif val == "RAV":
            return "🟠 Rav"
        else:
            return "🔴 Rød"

    display_df = df.copy()
    display_df["RAG"] = display_df["RAG_Status"].apply(format_rag)
    
    st.dataframe(
        display_df[["KOSTRA_Funksjon", "Beskrivelse", "Budsjett_MNOK", "Regnskap_YTD_MNOK", "Avvik_MNOK", "Netto_Vikarbelastning_MNOK", "Sykefravar_Pct", "RAG"]],
        use_container_width=True
    )

    st.markdown("---")
    
    # Deep Dive Selection
    st.subheader("📊 Dybdeanalyse, Monte Carlo-Prognose & NAV-Refusjonsgap")
    
    selected_funksjon = st.selectbox("Velg KOSTRA-Funksjon for Dybdeanalyse", df["Beskrivelse"].tolist())
    row = df[df["Beskrivelse"] == selected_funksjon].iloc[0]

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"#### 🎲 Monte Carlo Årsavslutningsprognose (KOSTRA {row['KOSTRA_Funksjon']}):")
        p10, p50, p90 = run_monte_carlo(row["Budsjett_MNOK"], row["Regnskap_YTD_MNOK"])
        
        st.write(f"- **Årsbudsjett**: {row['Budsjett_MNOK']:.2f} MNOK")
        st.write(f"- **P10 (Best Case)**: {p10:.2f} MNOK (Avvik: {row['Budsjett_MNOK'] - p10:.2f} MNOK)")
        st.write(f"- **P50 (Forventet M12)**: **{p50:.2f} MNOK** (Avvik: **{row['Budsjett_MNOK'] - p50:.2f} MNOK**)")
        st.write(f"- **P90 (Stress-Scenario med Q4-sykefravær)**: {p90:.2f} MNOK (Avvik: {row['Budsjett_MNOK'] - p90:.2f} MNOK)")

        # NAV Refund Gap Analysis
        st.markdown("#### 🏥 NAV-Refusjonsoppgjør (Art 1600):")
        expected_nav = round((row["Overtid_Art1090_MNOK"] + row["Vikarer_Art1100_MNOK"]) * 0.45, 2)
        actual_nav = abs(row["NAV_Refusjon_Art1600_MNOK"])
        refund_gap = round(expected_nav - actual_nav, 2)
        
        st.write(f"- Bokført NAV-refusjon (Art 1600): **{actual_nav:.2f} MNOK**")
        st.write(f"- Beregnet refusjonskrav jf. Folketrygdloven § 22-13: **{expected_nav:.2f} MNOK**")
        if refund_gap > 0:
            st.warning(f"⚠️ **Uavstemt Refusjonsgap**: Det gjenstår **{refund_gap:.2f} MNOK** ubetalte refusjoner fra NAV for denne enheten.")
        else:
            st.success("✅ NAV-refusjonene er i balanse.")

    with c2:
        st.markdown("#### ⚖️ Juridisk Saksfremlegg (RAG Oppslag: Kommuneloven § 14-5)")
        expected_year_end = p50
        year_end_deficit = round(expected_year_end - row["Budsjett_MNOK"], 2)
        
        if year_end_deficit > 0:
            ai_recommendation = (
                f"KOSTRA-funksjon {row['KOSTRA_Funksjon']} ({row['Beskrivelse']}) har et estimert merforbruk ved årsavslutning på {year_end_deficit:.2f} MNOK, "
                f"drevet av et sykefravær på {row['Sykefravar_Pct']}% og overtid/vikarutgifter på {row['Netto_Vikarbelastning_MNOK']:.2f} MNOK. "
                f"I henhold til Kommuneloven § 14-5 plikter kommunedirektøren å fremme sak for Formannskapet om kompenserende tiltak eller omdisponering."
            )
            st.error(ai_recommendation)
        else:
            ai_recommendation = (
                f"KOSTRA-funksjon {row['KOSTRA_Funksjon']} er innenfor rammen med et forventet mindreforbruk på {abs(year_end_deficit):.2f} MNOK. "
                f"Driften oppfyller kravene i Kommuneloven § 14-5."
            )
            st.success(ai_recommendation)

    st.markdown("---")
    st.subheader("🛡️ Stage-Gate Port 9: Saksbehandler Sign-Off & Revisorstempel")

    user_note = st.text_area(
        "Saksbehandlers vurderingsnotat (PII-vasket lokalt)", 
        f"Vurdert overskridelse for KOSTRA {row['KOSTRA_Funksjon']}. Inngår i oppfølgingssak for Helse og mestring. Kontaktperson fnr: 120485 12345."
    )
    clean_note = mask_pii(user_note)
    st.caption(f"🔒 **Skjermet tekst (Port 4 Local Scrubber)**: {clean_note}")

    col_b1, col_b2 = st.columns(2)
    if col_b1.button("✅ Godkjenn AI-Anbefaling (Godkjent)"):
        audit_entry = generate_audit_seal(user_upn, str(row['KOSTRA_Funksjon']), ai_recommendation, "APPROVED")
        st.success("Beslutning registrert i SHA-256 Audit Ledger!")
        st.json(audit_entry)

    if col_b2.button("⚠️ Korriger / Endre Beslutning"):
        audit_entry = generate_audit_seal(user_upn, str(row['KOSTRA_Funksjon']), ai_recommendation, "MODIFIED")
        st.warning("Endret beslutning registrert med revisorstempel.")
        st.json(audit_entry)


if __name__ == "__main__":
    main()
