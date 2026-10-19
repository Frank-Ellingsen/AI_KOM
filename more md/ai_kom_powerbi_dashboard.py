"""
🏛️ AI_KOM Power BI Control Hub - Kristiansand Kommune
Interactive Financial Controlling Dashboard for 6 Virksomhetsområder and 81 Enheter
"""

import hashlib
import json
import re
from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

# ==========================================
# 1. DATA ENGINE (6 Virksomhetsområder, 81 Enheter)
# ==========================================
@st.cache_data
def load_kristiansand_data() -> pd.DataFrame:
    np.random.seed(2026)

    virksomhetsomraader = {
        "Oppvekst": (2000, 2999, 18, [201, 202, 211, 220, 231]),
        "Helse og mestring": (5000, 5999, 22, [253, 254, 256, 261, 273]),
        "Stedsutvikling": (3000, 3999, 12, [301, 302, 303, 310]),
        "Kultur og innbyggerdialog": (4000, 4999, 10, [332, 333, 338, 345]),
        "Infrastruktur og miljø": (6000, 6999, 11, [340, 345, 353, 360]),
        "Organisasjon og styring": (1000, 1999, 8, [100, 120, 130, 180])
    }

    unit_names_pool = {
        "Oppvekst": [
            "Grim skole", "Karuss skole", "Møglestu skole", "Tangvall skole", "Flekkerøy skole",
            "Vågsbygd videregående", "Krossen skole", "Slettheia skole", "Søgne ungdomsskole",
            "Songdalen ungdomsskole", "Wilds Minne skole", "Presteheia skole", "Fagerholt skole",
            "Lovisenlund skole", "Solholmen skole", "Nygård skole", "Hånes skole", "Strømme skole"
        ],
        "Helse og mestring": [
            "Valhalla helsehus", "Eg sykehjem", "Stener Heyerdahl boliger", "Søgne omsorgssenter",
            "Songdalen helsetun", "Vågsbygd sykehjem", "Kløvertun opptreningssenter", "Hjemmetjenesten Øst",
            "Hjemmetjenesten Vest", "Hjemmetjenesten Sentrum", "Psykisk helse og avhengighet",
            "Ergoterapi og fysioterapi", "Kompenserende ytelse og bolig", "Slettheia omsorgsboliger",
            "Lund hjemmesykepleie", "Grim hjemmesykepleie", "Hånes omsorgssenter", "Strax-huset rehabilitering",
            "Borettslag for tilrettelagte boliger", "NAV Kristiansand Helse", "Tannhelsetjenesten", "Respit omsorg"
        ],
        "Stedsutvikling": [
            "Byggesak og tilsyn", "Reguleringsplan og kart", "Klima og miljøenheten", "Geodata og oppmåling",
            "Næring og eiendomsutvikling", "Havnevesenet", "Brann og redning Vennesla/KRS", "Trafikk og parkering",
            "Kommuneplanavdelingen", "Byutvikling Sentrum", "Søgne lokalutvikling", "Songdalen lokalutvikling"
        ],
        "Kultur og innbyggerdialog": [
            "Kristiansand folkebibliotek", "Kilden teater og konserthus", "Søgne kunst- og kultursenter",
            "Kulturskolen i Kristiansand", "Ungdomsklubbene Sentrum/Vågsbygd", "Innbyggertorget Rådhuset",
            "Samsen kulturhus", "Fritidsetaten Øst", "Fritidsetaten Vest", "Arkivet freds- og menneskerettighetssenter"
        ],
        "Infrastruktur og miljø": [
            "Ingeniørvesenet Veg og park", "Vann og avløp (VAR Selvkost)", "Renovasjon og gjenvinning",
            "Kommunalteknisk prosjektering", "Eiendomsdrift og vedlikehold", "Idrettsanlegg og haller",
            "Kristiansand Havn IKS", "Energiledelse og solceller", "Flom og skredsikring", "Parkvesenet Sentrum", "Søgne VAR"
        ],
        "Organisasjon og styring": [
            "Kommunedirektørens stab", "Økonomi og virksomhetsstyring", "HR og kompetanseutvikling",
            "IT og digitalisering (AI_KOM Hub)", "Dokumentsenter og arkiv", "Innkjøp og anskaffelser",
            "Kommunikasjon og enhetsdialog", "Kommunerevisjonen og kontroll"
        ]
    }

    data_rows = []

    for v_navn, (a_min, a_max, count, funksjoner) in virksomhetsomraader.items():
        names = unit_names_pool[v_navn]
        for i in range(count):
            ansvar_nr = a_min + (i * 35 + 12) % (a_max - a_min)
            u_name = names[i] if i < len(names) else f"{v_navn} Enhet {i+1}"
            funksjon = funksjoner[i % len(funksjoner)]
            
            budget = round(np.random.uniform(15.0, 180.0), 2)
            actual = round(budget * np.random.uniform(0.92, 1.14), 2)
            variance = round(budget - actual, 2)  # Positive = Less spend (Savings), Negative = Overrun
            var_pct = round((variance / budget) * 100, 2)
            
            rag = "GRØNN" if var_pct >= -2.0 else ("RAV" if var_pct >= -5.0 else "RØD")
            
            data_rows.append({
                "Virksomhetsområde": v_navn,
                "Ansvar": ansvar_nr,
                "Enhet_Navn": f"{ansvar_nr} - {u_name}",
                "KOSTRA_Funksjon": funksjon,
                "Budsjett_MNOK": budget,
                "Regnskap_MNOK": actual,
                "Avvik_MNOK": variance,
                "Avvik_Prosent": var_pct,
                "RAG_Status": rag,
                "Overtid_Art1090_kNOK": round(np.random.uniform(100, 4500), 0),
                "NAV_Refusjon_Art1600_kNOK": round(np.random.uniform(80, 3200), 0)
            })

    return pd.DataFrame(data_rows)

# PII Masking Engine
def mask_pii(text: str) -> str:
    text = re.sub(r'\b\d{6}\s?\d{5}\b', '[SKJERMET_FNR]', text)
    text = re.sub(r'\b\d{4}\.\d{2}\.\d{5}\b|\b\d{11}\b', '[SKJERMET_KONTO]', text)
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[SKJERMET_EPOST]', text)
    return text

# SHA-256 Audit Seal
def generate_audit_seal(user_upn: str, enhet: str, recommendation: str, decision: str) -> dict:
    timestamp = datetime.utcnow().isoformat() + "Z"
    payload = f"{timestamp}|{user_upn}|{enhet}|{recommendation}|{decision}"
    sha_seal = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    
    return {
        "timestamp": timestamp,
        "user_upn": user_upn,
        "enhet": enhet,
        "ai_recommendation": recommendation,
        "human_decision": decision,
        "sha256_seal": sha_seal
    }

# Monte Carlo Engine
def run_monte_carlo(budget: float, actual_ytd: float, months_elapsed: int = 8, num_sims: int = 1000):
    months_remaining = 12 - months_elapsed
    monthly_rate = actual_ytd / months_elapsed
    sims = np.random.normal(monthly_rate, monthly_rate * 0.08, (num_sims, months_remaining))
    totals = actual_ytd + np.sum(sims, axis=1)
    return np.percentile(totals, 10), np.percentile(totals, 50), np.percentile(totals, 90)

# ==========================================
# 2. MAIN APPLICATION
# ==========================================
def main():
    st.set_page_config(
        page_title="Kristiansand Kommune — Power BI Control Hub",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom Power BI Theme CSS
    st.markdown("""
        <style>
        .main { background-color: #F8F9FA; }
        .stMetric {
            background-color: #FFFFFF;
            padding: 15px;
            border-radius: 8px;
            border-left: 5px solid #002B49;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .pbi-card {
            background-color: #002B49;
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🏛️ Power BI Control Hub — Kristiansand Kommune")
    st.caption("Interaktiv Styrings- og Økonomidashboard (6 Virksomhetsområder, 81 Enheter) | EVM Monte Carlo & RAG Standards")

    df_raw = load_kristiansand_data()

    # ==========================================
    # 3. POWER BI SLICERS & FILTERS (SIDEBAR)
    # ==========================================
    st.sidebar.header("🎛️ Power BI Slicers & Filters")
    st.sidebar.markdown("---")

    # Slicer 1: Virksomhetsområde (6 areas)
    all_v_omraader = ["(Velg alle)"] + sorted(df_raw["Virksomhetsområde"].unique().tolist())
    selected_v_omraader = st.sidebar.multiselect(
        "1. Virksomhetsområde (6 Sektorer)",
        options=all_v_omraader,
        default=["(Velg alle)"]
    )

    if "(Velg alle)" in selected_v_omraader or not selected_v_omraader:
        df_filtered_v = df_raw.copy()
    else:
        df_filtered_v = df_raw[df_raw["Virksomhetsområde"].isin(selected_v_omraader)]

    # Slicer 2: Enhet / Ansvarssted (81 units)
    available_enheter = ["(Velg alle)"] + sorted(df_filtered_v["Enhet_Navn"].unique().tolist())
    selected_enheter = st.sidebar.multiselect(
        f"2. Enhet / Ansvarssted ({len(df_filtered_v)} tilgjengelige)",
        options=available_enheter,
        default=["(Velg alle)"]
    )

    if "(Velg alle)" in selected_enheter or not selected_enheter:
        df_filtered = df_filtered_v.copy()
    else:
        df_filtered = df_filtered_v[df_filtered_v["Enhet_Navn"].isin(selected_enheter)]

    # Slicer 3: RAG Status Slicer
    rag_filter = st.sidebar.radio(
        "3. RAG-Status Slicer",
        options=["Alle", "🔴 Rød (Merforbruk > 5%)", "🟠 Rav (Merforbruk 2–5%)", "🟢 Grønn (I Balanse)"]
    )

    if "Rød" in rag_filter:
        df_filtered = df_filtered[df_filtered["RAG_Status"] == "RØD"]
    elif "Rav" in rag_filter:
        df_filtered = df_filtered[df_filtered["RAG_Status"] == "RAV"]
    elif "Grønn" in rag_filter:
        df_filtered = df_filtered[df_filtered["RAG_Status"] == "GRØNN"]

    # Slicer 4: KOSTRA Funksjon Slicer
    all_kostra = ["Alle"] + [str(x) for x in sorted(df_filtered["KOSTRA_Funksjon"].unique().tolist())]
    selected_kostra = st.sidebar.selectbox("4. KOSTRA Funksjon", options=all_kostra)
    if selected_kostra != "Alle":
        df_filtered = df_filtered[df_filtered["KOSTRA_Funksjon"] == int(selected_kostra)]

    # Search filter
    search_query = st.sidebar.text_input("🔍 Søk i Enheter / Ansvar", "")
    if search_query:
        df_filtered = df_filtered[df_filtered["Enhet_Navn"].str.contains(search_query, case=False, na=False)]

    st.sidebar.markdown("---")
    st.sidebar.caption("🔑 **Brukeridentitet**: controller@kristiansand.kommune.no")

    # ==========================================
    # 4. EXECUTIVE POWER BI KPI CARDS
    # ==========================================
    tot_budget = df_filtered["Budsjett_MNOK"].sum()
    tot_actual = df_filtered["Regnskap_MNOK"].sum()
    tot_variance = df_filtered["Avvik_MNOK"].sum()
    var_pct = (tot_variance / tot_budget * 100) if tot_budget > 0 else 0.0

    if var_pct >= -2.0:
        overall_rag_code = "🟢 GRØNN (I Balanse)"
    elif var_pct >= -5.0:
        overall_rag_code = "🟠 RAV (Moderat Avvik)"
    else:
        overall_rag_code = "🔴 RØD (Kritisk Merforbruk)"

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Totalt Budsjett", f"{tot_budget:,.1f} MNOK")
    kpi2.metric("Regnskap YTD", f"{tot_actual:,.1f} MNOK")
    kpi3.metric("Nettavvik (MNOK)", f"{tot_variance:,.2f} MNOK", delta=f"{tot_variance:.2f} MNOK")
    kpi4.metric("Avvik %", f"{var_pct:.2f}%")
    kpi5.metric("RAG Status", overall_rag_code)

    st.markdown("---")

    # ==========================================
    # 5. DASHBOARD TABS
    # ==========================================
    tab_dash, tab_enheter, tab_dax, tab_audit = st.tabs([
        "📊 Executive Dashboard (Power BI View)",
        "🏢 Enhetsmatrise & Drill-Down (81 Enheter)",
        "📐 Power BI DAX & Data Export",
        "🛡️ EU AI Act Audit Ledger (Port 9)"
    ])

    # ------------------------------------------
    # TAB 1: EXECUTIVE DASHBOARD
    # ------------------------------------------
    with tab_dash:
        st.subheader("📊 Sektorfordeling & Budsjett vs Regnskap")
        
        c_chart1, c_chart2 = st.columns(2)

        with c_chart1:
            st.markdown("#### Budsjett vs Regnskap per Virksomhetsområde (MNOK)")
            sektor_agg = df_filtered.groupby("Virksomhetsområde")[["Budsjett_MNOK", "Regnskap_MNOK"]].sum().reset_index()
            
            fig, ax = plt.subplots(figsize=(8, 4.5))
            x = np.arange(len(sektor_agg))
            width = 0.35
            
            ax.bar(x - width/2, sektor_agg["Budsjett_MNOK"], width, label="Budsjett (MNOK)", color="#002B49")
            ax.bar(x + width/2, sektor_agg["Regnskap_MNOK"], width, label="Regnskap (MNOK)", color="#D32F2F")
            
            ax.set_ylabel("MNOK")
            ax.set_xticks(x)
            ax.set_xticklabels(sektor_agg["Virksomhetsområde"], rotation=25, ha="right")
            ax.legend()
            ax.grid(axis="y", linestyle="--", alpha=0.5)
            plt.tight_layout()
            st.pyplot(fig)

        with c_chart2:
            st.markdown("#### RAG-Status Fordeling på Tvers av Enheter")
            rag_counts = df_filtered["RAG_Status"].value_counts().reset_index()
            rag_counts.columns = ["RAG_Status", "Antall"]
            
            colors_map = {"GRØNN": "#388E3C", "RAV": "#F57C00", "RØD": "#D32F2F"}
            bar_colors = [colors_map.get(status, "#002B49") for status in rag_counts["RAG_Status"]]
            
            fig2, ax2 = plt.subplots(figsize=(8, 4.5))
            ax2.bar(rag_counts["RAG_Status"], rag_counts["Antall"], color=bar_colors)
            ax2.set_ylabel("Antall Enheter")
            ax2.grid(axis="y", linestyle="--", alpha=0.5)
            plt.tight_layout()
            st.pyplot(fig2)

        st.markdown("---")
        st.markdown("#### 🔝 Top 5 Største Merforbruk (Røde Enheter)")
        top_overruns = df_filtered.sort_values(by="Avvik_MNOK", ascending=True).head(5)
        st.dataframe(
            top_overruns[["Virksomhetsområde", "Enhet_Navn", "KOSTRA_Funksjon", "Budsjett_MNOK", "Regnskap_MNOK", "Avvik_MNOK", "Avvik_Prosent", "RAG_Status"]],
            use_container_width=True
        )

    # ------------------------------------------
    # TAB 2: ENHETSMATRISE & DRILL-DOWN
    # ------------------------------------------
    with tab_enheter:
        st.subheader(f"🏢 Komplett Enhetsmatrise ({len(df_filtered)} Enheter Visning)")
        
        def format_rag(val):
            if val == "GRØNN": return "🟢 Grønn"
            elif val == "RAV": return "🟠 Rav"
            else: return "🔴 Rød"

        styled_matrise = df_filtered.copy()
        styled_matrise["RAG"] = styled_matrise["RAG_Status"].apply(format_rag)

        st.dataframe(
            styled_matrise[["Virksomhetsområde", "Enhet_Navn", "KOSTRA_Funksjon", "Budsjett_MNOK", "Regnskap_MNOK", "Avvik_MNOK", "Avvik_Prosent", "Overtid_Art1090_kNOK", "NAV_Refusjon_Art1600_kNOK", "RAG"]],
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("🔍 Enkeltenhet Deep Dive & Monte Carlo EVM Prognose")
        
        single_unit = st.selectbox("Velg Enhet for Detaljert Analyse", df_filtered["Enhet_Navn"].tolist())
        unit_row = df_filtered[df_filtered["Enhet_Navn"] == single_unit].iloc[0]

        u_col1, u_col2 = st.columns(2)
        with u_col1:
            st.write(f"**Enhet**: {unit_row['Enhet_Navn']}")
            st.write(f"**Virksomhetsområde**: {unit_row['Virksomhetsområde']}")
            st.write(f"**KOSTRA Funksjon**: {unit_row['KOSTRA_Funksjon']}")
            st.write(f"**Budsjett**: {unit_row['Budsjett_MNOK']:.2f} MNOK | **Regnskap YTD**: {unit_row['Regnskap_MNOK']:.2f} MNOK")
            st.write(f"**Avvik**: {unit_row['Avvik_MNOK']:.2f} MNOK ({unit_row['Avvik_Prosent']:.2f}%)")
            st.write(f"**Overtid (Art 1090)**: {unit_row['Overtid_Art1090_kNOK']:,.0f} kNOK")
            st.write(f"**NAV Refusjon (Art 1600)**: {unit_row['NAV_Refusjon_Art1600_kNOK']:,.0f} kNOK")

        with u_col2:
            st.markdown("#### 🎲 Monte Carlo Årsavslutningsprognose (M8-M12)")
            p10, p50, p90 = run_monte_carlo(unit_row["Budsjett_MNOK"], unit_row["Regnskap_MNOK"])
            st.write(f"- **P10 (Best-Case)**: {p10:.2f} MNOK")
            st.write(f"- **P50 (Forventet)**: {p50:.2f} MNOK")
            st.write(f"- **P90 (Stress-Scenario)**: {p90:.2f} MNOK")
            
            exp_var = unit_row["Budsjett_MNOK"] - p50
            if exp_var < 0:
                st.error(f"⚠️ Forventet merforbruk ved årsavslutning: {abs(exp_var):.2f} MNOK. Krever tiltaksplan jf. Kommuneloven § 14-5.")
            else:
                st.success(f"✅ Forventet mindreforbruk ved årsavslutning: {exp_var:.2f} MNOK.")

    # ------------------------------------------
    # TAB 3: POWER BI DAX & EXPORT
    # ------------------------------------------
    with tab_dax:
        st.subheader("📐 Power BI DAX Måltalls-Katalog")
        st.markdown("Kopier disse DAX-formlene direkte inn i Power BI Desktop for sømløs integrasjon mot Visma/Framsikt datamodellen:")

        dax_code = """
-- 1. Totalt Budsjett (MNOK)
Total Budsjett MNOK = 
SUM(Fact_Regnskap[Budsjett_MNOK])

-- 2. Totalt Regnskap YTD (MNOK)
Total Regnskap MNOK = 
SUM(Fact_Regnskap[Regnskap_MNOK])

-- 3. Nettovariasjon / Avvik (MNOK)
-- Retningsregel: Budsjett - Regnskap (Positivt = Mindreforbruk/Innsparing, Negativt = Merforbruk/Underskudd)
Avvik MNOK = 
[Total Budsjett MNOK] - [Total Regnskap MNOK]

-- 4. Avvik Prosent
Avvik Pct = 
DIVIDE([Avvik MNOK], [Total Budsjett MNOK], 0) * 100

-- 5. RAG Status Code
RAG Status Code = 
SWITCH(
    TRUE(),
    [Avvik Pct] >= -2.0, "GRØNN",
    [Avvik Pct] >= -5.0, "RAV",
    "RØD"
)

-- 6. RAG Hex Color for Conditional Formatting
RAG Hex Color = 
SWITCH(
    [RAG Status Code],
    "GRØNN", "#388E3C",
    "RAV", "#F57C00",
    "RØD", "#D32F2F",
    "#002B49"
)
        """
        st.code(dax_code, language="sql")

        st.markdown("---")
        st.subheader("📥 Eksporter Filtrert Datagrunnlag for Power BI")
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Last ned filtrerte data (CSV)",
            data=csv_data,
            file_name="kristiansand_powerbi_data.csv",
            mime="text/csv"
        )

    # ------------------------------------------
    # TAB 4: EU AI ACT AUDIT LEDGER
    # ------------------------------------------
    with tab_audit:
        st.subheader("🛡️ Stage-Gate Port 9: Saksbehandler Sign-Off & Revisorstempel")
        st.markdown("Logg godkjente saksnotater og omdisponeringer med kryptografisk SHA-256 forsegling for Kommunerevisjonen (EU AI Act Art. 14).")

        audit_unit = st.selectbox("Velg Enhet for Sign-Off", df_filtered["Enhet_Navn"].tolist(), key="audit_unit_select")
        audit_row = df_filtered[df_filtered["Enhet_Navn"] == audit_unit].iloc[0]

        st.info(f"Valgt Enhet: **{audit_row['Enhet_Navn']}** | Avvik: **{audit_row['Avvik_MNOK']:.2f} MNOK** | RAG: **{audit_row['RAG_Status']}**")

        user_note = st.text_area("Saksbehandlers merknad / Tiltaksplan", f"Vurdert tiltaksplan for {audit_row['Enhet_Navn']}. Sykelønnsrefusjoner følges opp mot NAV.")
        clean_note = mask_pii(user_note)

        st.caption(f"🔒 **Skjermet merknad (Port 4 PII Scrubber)**: {clean_note}")

        c_act1, c_act2 = st.columns(2)
        if c_act1.button("✅ Godkjenn Tiltak & Generer SHA-256 Stempel"):
            rec_str = f"Avvik på {audit_row['Avvik_MNOK']:.2f} MNOK vurdert for {audit_row['Enhet_Navn']}."
            audit_entry = generate_audit_seal("controller@kristiansand.kommune.no", audit_row["Enhet_Navn"], rec_str, "APPROVED")
            st.success("Beslutning registrert i SHA-256 Audit Ledger!")
            st.json(audit_entry)

        if c_act2.button("⚠️ Krever Endring / Behandles i Formannskapet"):
            rec_str = f"Avvik på {audit_row['Avvik_MNOK']:.2f} MNOK vurdert for {audit_row['Enhet_Navn']}."
            audit_entry = generate_audit_seal("controller@kristiansand.kommune.no", audit_row["Enhet_Navn"], rec_str, "MODIFIED_FOR_POLITICAL_HEARING")
            st.warning("Sak flagget for politisk behandling i Formannskapet.")
            st.json(audit_entry)

if __name__ == "__main__":
    main()
