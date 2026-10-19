"""
AI_KOM Power BI Dashboard - Kristiansand Kommune
Komplett styringsdashboard med 6 Virksomhetsområder, 81 Enheter og Slicers
"""

import hashlib
import json
import re
from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st

def mask_pii(text: str) -> str:
    text = re.sub(r'\b\d{6}\s?\d{5}\b', '[SKJERMET_FNR]', text)
    text = re.sub(r'\b\d{4}\.\d{2}\.\d{5}\b|\b\d{11}\b', '[SKJERMET_KONTO]', text)
    return text

@st.cache_data
def load_data():
    return pd.read_csv("data/kristiansand_81_enheter.csv")

def run_monte_carlo(budget, actual_ytd, months_elapsed=8, sims=1000):
    months_rem = 12 - months_elapsed
    rate = actual_ytd / months_elapsed
    sim_rem = np.random.normal(rate, rate * 0.08, (sims, months_rem))
    sim_totals = actual_ytd + np.sum(sim_rem, axis=1)
    return np.percentile(sim_totals, 10), np.percentile(sim_totals, 50), np.percentile(sim_totals, 90)

def generate_sha256_seal(user, unit, rec, decision):
    ts = datetime.utcnow().isoformat() + "Z"
    payload = f"{ts}|{user}|{unit}|{rec}|{decision}"
    return {
        "timestamp": ts,
        "user_upn": user,
        "enhet": unit,
        "recommendation": rec,
        "decision": decision,
        "sha256_seal": hashlib.sha256(payload.encode()).hexdigest()
    }

def main():
    st.set_page_config(page_title="AI_KOM Power BI Dashboard", layout="wide")
    st.title("🏛️ Kristiansand Kommune — Power BI Control Office Hub")
    st.caption("Visuell Styringsrapport for 6 Virksomhetsområder & 81 Organisatoriske Enheter")

    df = load_data()

    # --- SIDEBAR POWER BI SLICERS ---
    st.sidebar.header("🎛️ Power BI Slicers & Filtere")
    
    # Slicer 1: Virksomhetsområder
    all_sectors = sorted(df["Virksomhetsomrade"].unique())
    selected_sectors = st.sidebar.multiselect("Virksomhetsområde (6)", all_sectors, default=all_sectors)
    
    filtered_df = df[df["Virksomhetsomrade"].isin(selected_sectors)]
    
    # Slicer 2: Enhet (Cascading)
    all_units = sorted(filtered_df["Enhet_Navn"].unique())
    selected_units = st.sidebar.multiselect("Enhet (81)", all_units, default=all_units)
    
    filtered_df = filtered_df[filtered_df["Enhet_Navn"].isin(selected_units)]

    # Slicer 3: RAG Status
    all_rag = ["GRØNN", "RAV", "RØD"]
    selected_rag = st.sidebar.multiselect("RAG Status", all_rag, default=all_rag)
    filtered_df = filtered_df[filtered_df["RAG_Status"].isin(selected_rag)]

    # Slicer 4: Search Filter
    search_query = st.sidebar.text_input("🔍 Søk Enhet / Ansvar", "")
    if search_query:
        filtered_df = filtered_df[
            filtered_df["Enhet_Navn"].str.contains(search_query, case=False) | 
            filtered_df["Ansvar"].astype(str).str.contains(search_query)
        ]

    # --- TOP KPI CARDS ---
    tot_budget = filtered_df["Budsjett_MNOK"].sum()
    tot_actual = filtered_df["Regnskap_YTD_MNOK"].sum()
    tot_var = filtered_df["Avvik_MNOK"].sum()
    var_pct = (tot_var / tot_budget * 100) if tot_budget > 0 else 0.0

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Totalt Budsjett", f"{tot_budget:.2f} MNOK")
    kpi2.metric("Regnskap YTD", f"{tot_actual:.2f} MNOK")
    kpi3.metric("Nettavvik", f"{tot_var:.2f} MNOK", delta_color="normal")
    kpi4.metric("Avvik %", f"{var_pct:.2f}%")
    kpi5.metric("RAG Status", "RØD" if var_pct < -5 else ("RAV" if var_pct < -2 else "GRØNN"))

    st.markdown("---")

    # --- TABLE VIEW ---
    st.subheader(f"📊 Regnskapstabell ({len(filtered_df)} enheter valgt)")
    
    def format_rag_str(v):
        return "🟢 Grønn" if v == "GRØNN" else ("🟠 Rav" if v == "RAV" else "🔴 Rød")

    display_df = filtered_df.copy()
    display_df["RAG"] = display_df["RAG_Status"].apply(format_rag_str)
    
    st.dataframe(
        display_df[["Virksomhetsomrade", "Ansvar", "Enhet_Navn", "KOSTRA_Funksjon", "Budsjett_MNOK", "Regnskap_YTD_MNOK", "Avvik_MNOK", "Avvik_Prosent", "RAG"]],
        use_container_width=True
    )

    st.markdown("---")
    
    # --- DRILL-DOWN ANALYSES ---
    st.subheader("🔍 Enhets-Drilldown & Monte Carlo Prognose")
    if not filtered_df.empty:
        sel_unit = st.selectbox("Velg Enhet for Detaljanalyse", filtered_df["Enhet_Navn"].tolist())
        unit_row = filtered_df[filtered_df["Enhet_Navn"] == sel_unit].iloc[0]

        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Enhet**: {unit_row['Enhet_Navn']} (Ansvar {unit_row['Ansvar']})")
            st.write(f"**Virksomhetsområde**: {unit_row['Virksomhetsomrade']}")
            st.write(f"**Budsjett**: {unit_row['Budsjett_MNOK']} MNOK | **YTD**: {unit_row['Regnskap_YTD_MNOK']} MNOK")
            st.write(f"**Avvik**: {unit_row['Avvik_MNOK']} MNOK ({unit_row['Avvik_Prosent']}%)")
            
            p10, p50, p90 = run_monte_carlo(unit_row["Budsjett_MNOK"], unit_row["Regnskap_YTD_MNOK"])
            st.markdown("**Årsavslutningsprognose (Monte Carlo P10/P50/P90):**")
            st.write(f"- P10 (Best Case): {p10:.2f} MNOK")
            st.write(f"- P50 (Forventet): {p50:.2f} MNOK")
            st.write(f"- P90 (Stress Case): {p90:.2f} MNOK")

        with c2:
            st.markdown("**⚖️ Kommuneloven § 14-5 Vurdering & Revisorstempel:**")
            if unit_row["Avvik_MNOK"] < 0:
                rec = f"Enheten har et merforbruk på {abs(unit_row['Avvik_MNOK']):.2f} MNOK. Krever tiltaksplan."
                st.error(rec)
            else:
                rec = f"Enheten er i balanse med et mindreforbruk på {unit_row['Avvik_MNOK']:.2f} MNOK."
                st.success(rec)

            note = st.text_area("Saksbehandlers merknad", f"Vurdert avvik for {unit_row['Enhet_Navn']}.")
            clean_note = mask_pii(note)
            
            if st.button("✅ Signer og generer SHA-256 Revisorstempel"):
                seal = generate_sha256_seal("controller@kristiansand.kommune.no", unit_row["Enhet_Navn"], rec, "APPROVED")
                st.success("Revisorstempel opprettet!")
                st.json(seal)

if __name__ == "__main__":
    main()
