import streamlit as st
import sqlite3
import pandas as pd
import os
import sys

# Sikre at prosjektets rotmappe er i sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.schemas import (
    UserContext,
    MonthlyUnitReportInput,
    BudgetReallocationInput,
    ERPSQLQueryInput,
    EOYForecastInput
)
from app.agent import KrsKommuneAgent
from app.tools import (
    get_db_path,
    write_audit_log,
    calculate_monthly_report,
    process_budget_reallocation,
    query_erp_transactions_secure,
    eoy_forecast
)

st.set_page_config(
    page_title="Kristiansand Kommune — AI Control Office Hub",
    page_icon="🏛️",
    layout="wide"
)

# Custom Tufte Data-Ink Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .metric-val {
        font-size: 24px;
        font-weight: 700;
        color: #1b365d;
    }
    .metric-sub {
        font-size: 13px;
        color: #64748b;
    }
    .stTable td, .stTable th {
        border-left: none !important;
        border-right: none !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏛️ Kristiansand Kommune — Control Office Hub (AI_KOM)")
st.caption("AI-Beslutningsstøtte & Økonomirådgiver for Helse og Mestring | 7 Interaktive Moduler")

# Sidebar: Role-Based Access Control (RBAC)
st.sidebar.header("👤 Brukerkontekst (RBAC)")
role = st.sidebar.selectbox("Velg Rolle", ["enhetsleder", "kommunalsjef", "okonomidirektor", "revisor"])
default_ansvar = "2530" if role == "enhetsleder" else "2500"
ansvar = st.sidebar.text_input("Ansvarsnummer", default_ansvar)

user_context = UserContext(
    user_id="frank_ellingsen",
    role=role,
    ansvar_code=ansvar,
    kommunalsjef_område="Omsorgssentre" if role == "kommunalsjef" else None
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Aktiv rolle:** `{role}`")
st.sidebar.markdown(f"**Tildelt enhet:** `{ansvar}`")
st.sidebar.markdown(f"**Database:** `{os.path.basename(get_db_path())}`")
st.sidebar.markdown(f"**Loop Limit:** `max_iterations = 5`")

# 7 Tabs jf. AI_KOM Antigravity Clean arkitektur
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "💬 AI-Økonomirådgiver",
    "📊 Månedlig Rapport & Trafikklys",
    "📈 FT Visual Vocabulary",
    "🔮 EOY Prognose",
    "🔍 6-Nivås Drill-Down",
    "🔄 Omdisponering § 14-5",
    "📜 Audit-Logg (Revisor)"
])

agent = KrsKommuneAgent()

# ------------------------------------------------------------------------------
# TAB 1: 💬 AI-Økonomirådgiver
# ------------------------------------------------------------------------------
with tab1:
    st.header("💬 Chat med AI-Økonomirådgiver")
    st.info("Spør om månedsavvik, prognoser, overtid, vikarforbruk eller omdisponeringer jf. Kommuneloven § 14-5.")
    
    col_q1, col_q2, col_q3 = st.columns(3)
    preset_query = ""
    if col_q1.button("📋 Kjør månedsrapport for enheten"):
        preset_query = "Vis meg månedlig rapport og avvik for enheten min"
    if col_q2.button("🔮 Beregn rullende EOY-prognose"):
        preset_query = "Hva er forventet årsprognose (EOY/EAC)?"
    if col_q3.button("🔄 Fullmaktskontroll § 14-5"):
        preset_query = "Kan jeg omdisponere 350000 kr til vikarer ved høyt sykefravær?"
        
    user_prompt = st.text_input("Still et spørsmål til agenten:", value=preset_query)
    
    if st.button("Send forespørsel", type="primary") and user_prompt:
        with st.spinner("Agenten analyserer regnskapsdata og regelverk via Bounded Loop..."):
            res = agent.run(user_prompt, user_context)
            if res.get("hitl_required"):
                st.warning("⚠️ **Human-in-the-Loop Intercept:** Denne handlingen krever politisk sign-off i Bystyret.")
            st.markdown(res["response"])

# ------------------------------------------------------------------------------
# TAB 2: 📊 Månedlig Rapport & Trafikklys
# ------------------------------------------------------------------------------
with tab2:
    st.header("📊 Månedlig Avviksrapport & RAG-Trafikklys")
    col_m1, col_m2 = st.columns([1, 2])
    with col_m1:
        selected_month = st.slider("Rapporteringsmåned (2026)", min_value=1, max_value=12, value=8)
        selected_unit = st.text_input("Enhetskode", value=user_context.ansvar_code or "2530")
        calc_btn = st.button("Beregn Månedsrapport")
        
    rep = calculate_monthly_report(MonthlyUnitReportInput(
        ansvar_code=selected_unit,
        period_month=selected_month,
        user_context=user_context
    ))
    
    with col_m2:
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Regnskap hittil", f"kr {rep['forbruk']:,.0f}")
        kpi2.metric("Budsjett hittil", f"kr {rep['budsjett']:,.0f}")
        kpi3.metric("Netto Avvik (CV)", f"kr {rep['avvik_nok']:,.0f}", delta=f"{rep['avvik_pct']}%", delta_color="inverse")
        kpi4.metric("RAG Status", rep['status'])
        
    st.markdown("---")
    st.subheader(f"Dekomponering etter KOSTRA-Art for Enhet {selected_unit}")
    cost_data = pd.DataFrame([
        {"Art": "1010 Fastlønn", "Forbruk (NOK)": rep['forbruk'] * 0.65, "Budsjett (NOK)": rep['budsjett'] * 0.68, "Status": "🟢 I balanse"},
        {"Art": "1020 Vikarer", "Forbruk (NOK)": rep['forbruk'] * 0.18, "Budsjett (NOK)": rep['budsjett'] * 0.12, "Status": "🔴 Merforbruk"},
        {"Art": "1040 Overtid", "Forbruk (NOK)": rep['forbruk'] * 0.08, "Budsjett (NOK)": rep['budsjett'] * 0.05, "Status": "🔴 Merforbruk"},
        {"Art": "1150 Kurs/Drift", "Forbruk (NOK)": rep['forbruk'] * 0.09, "Budsjett (NOK)": rep['budsjett'] * 0.15, "Status": "🟢 Mindreforbruk"},
    ])
    st.table(cost_data)

# ------------------------------------------------------------------------------
# TAB 3: 📈 FT Visual Vocabulary
# ------------------------------------------------------------------------------
with tab3:
    st.header("📈 Financial Times Visual Vocabulary Suite")
    st.markdown("""
    Visualiseringene følger **Financial Times Visual Vocabulary** og **Edward Tufte Data-Ink** prinsipper:
    * 0 unødige 3D-effekter, ingen vertikale rutenett i tabeller, direkte merking på akser.
    * Muted municipal fargepalett med rød/amber kun for aktive avvik.
    """)
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.subheader("1. Deviation: Netto Kostnadsavvik per Enhet")
        chart_data = pd.DataFrame({
            "Enhet": ["2510", "2520", "2530", "2540", "2550"],
            "Netto Avvik (kNOK)": [45, -120, -70, 85, -210]
        }).set_index("Enhet")
        st.bar_chart(chart_data)
        st.caption("Positive stolper angir mindreforbruk, negative angir merforbruk jf. § 14-5.")

    with col_v2:
        st.subheader("2. Correlation: Sykefravær vs. Overtidskostnad")
        corr_data = pd.DataFrame({
            "Sykefravær %": [4.2, 5.8, 7.1, 8.5, 9.2, 11.4],
            "Overtid (kNOK)": [12, 34, 55, 88, 110, 165]
        }).set_index("Sykefravær %")
        st.line_chart(corr_data)
        st.caption("Sterk korrelasjon mellom sykefravær og overtid/vikarer i helse og omsorg (HTA § 4).")

# ------------------------------------------------------------------------------
# TAB 4: 🔮 EOY Prognose
# ------------------------------------------------------------------------------
with tab4:
    st.header("🔮 Rullende Årssluttprognose (EOY / EAC)")
    st.markdown("Prognosemodellen kombinerer sesongprofil, Monte Carlo-usikkerhet og Earned Value Management (EVM).")
    
    forecast_data = eoy_forecast(EOYForecastInput(
        ansvar_code=user_context.ansvar_code or "2530",
        current_month=8,
        user_context=user_context
    ))
    
    col_p1, col_p2, col_p3 = st.columns(3)
    col_p1.metric("Vedtatt årsbudsjett (BAC)", f"kr {forecast_data['bac']:,.0f}")
    col_p2.metric("Forventet årsslutt (EAC P50)", f"kr {forecast_data['eac']:,.0f}", delta=f"{forecast_data['vac']:,.0f} NOK", delta_color="inverse")
    col_p3.metric("Kostnadsindeks (CPI)", f"{forecast_data['cpi']}", delta="Merforbruk" if forecast_data['cpi'] < 1.0 else "I balanse", delta_color="inverse")
    
    st.markdown("---")
    st.subheader("Monte Carlo Usikkerhetsspenn (P10 - P50 - P90)")
    mc_df = pd.DataFrame({
        "Persentil": ["P10 (Beste utfall)", "P50 (Forventet)", "P90 (Konservativt)"],
        "Prognose (NOK)": [
            forecast_data["monte_carlo"]["p10"],
            forecast_data["monte_carlo"]["p50"],
            forecast_data["monte_carlo"]["p90"]
        ],
        "Avvik mot ramme (VAC)": [
            forecast_data["bac"] - forecast_data["monte_carlo"]["p10"],
            forecast_data["bac"] - forecast_data["monte_carlo"]["p50"],
            forecast_data["bac"] - forecast_data["monte_carlo"]["p90"]
        ],
        "Tiltakskrav": ["Overvåking", "Månedlig oppfølging", "Tilleggsbevilgning § 14-5"]
    })
    st.table(mc_df)

# ------------------------------------------------------------------------------
# TAB 5: 🔍 6-Nivås Drill-Down
# ------------------------------------------------------------------------------
with tab5:
    st.header("🔍 6-Nivås Økonomisk Drill-Down")
    st.caption("Sektor (1) -> Kommunalsjef (2) -> Enhet (3) -> KOSTRA-Funksjon (4) -> KOSTRA-Art (5) -> Bilag (6)")
    
    dd_col1, dd_col2, dd_col3 = st.columns(3)
    dd_col1.selectbox("Nivå 1: Sektor", ["Helse og Mestring", "Oppvekst og Utdanning", "By- og stedsutvikling"])
    dd_col2.selectbox("Nivå 2: Kommunalsjefområde", ["Omsorgssentre", "Hjemmetjenester", "Mestring"])
    dd_col3.text_input("Nivå 3: Enhet/Ansvar", value=user_context.ansvar_code or "2530")
    
    st.subheader("Bilagstransaksjoner (Nivå 6) med håndhevet RBAC")
    sql_input = ERPSQLQueryInput(
        sql_query="SELECT * FROM stg_erp_transactions",
        user_context=user_context
    )
    result = query_erp_transactions_secure(sql_input)
    st.success(f"RBAC håndhevet: {'Ja (Kun tildelt enhet)' if result['rbac_applied'] else 'Nei (Overordnet rolle)'}")
    st.dataframe(pd.DataFrame(result["sample_data"]), use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 6: 🔄 Omdisponering § 14-5
# ------------------------------------------------------------------------------
with tab6:
    st.header("🔄 Budsjettomdisponering & Fullmaktskontroll")
    st.markdown("Automatisk kontroll av fullmaktsgrenser jf. **Kommuneloven § 14-5** og Kristiansand kommunes økonomireglement.")
    
    with st.form("realloc_form"):
        col_r1, col_r2 = st.columns(2)
        fra_ansvar = col_r1.text_input("Fra Ansvarsnummer", value=user_context.ansvar_code or "2530")
        til_ansvar = col_r2.text_input("Til Ansvarsnummer", value="2540")
        belop = st.number_input("Beløp (NOK)", min_value=1000.0, max_value=10000000.0, value=350000.0, step=10000.0)
        begrunnelse = st.text_area("Formell begrunnelse", value="Dekning av uforutsette vikarutgifter ved høyt sykefravær.")
        submitted = st.form_submit_button("Vurder fullmakt & generer saksframlegg")
        
    if submitted:
        realloc_res = process_budget_reallocation(BudgetReallocationInput(
            fra_ansvar=fra_ansvar,
            til_ansvar=til_ansvar,
            belop=belop,
            begrunnelse=begrunnelse,
            user_context=user_context
        ))
        st.subheader("Resultat av fullmaktskontroll")
        if realloc_res["krever_politisk_vedtak"]:
            st.warning(f"⚠️ **Krever Politisk Vedtak:** Beløpet eller sektorkryssingen krever godkjenning i **{realloc_res['vedtaksorgan']}**.")
        else:
            st.success(f"✅ **Administrativt Vedtak:** Omdisponeringen kan godkjennes administrativt av **{realloc_res['vedtaksorgan']}**.")
            
        st.text_area("Generert saksframlegg jf. Kommuneloven § 14-5:", value=realloc_res["saksframlegg_utkast"], height=140)

# ------------------------------------------------------------------------------
# TAB 7: 📜 Audit-Logg (Revisor)
# ------------------------------------------------------------------------------
with tab7:
    st.header("📜 Audit-Logg & Revisjonsspor (Arkivlova)")
    st.info("Uforanderlig endringslogg for Agder Kontrollutvalg og Kommunerevisjonen (NKRF) jf. Stage-Gate Port 9.")
    
    db_file = get_db_path()
    try:
        conn = sqlite3.connect(db_file)
        df_audit = pd.read_sql_query("SELECT * FROM audit_log ORDER BY id DESC LIMIT 100", conn)
        conn.close()
        if not df_audit.empty:
            st.dataframe(df_audit, use_container_width=True)
        else:
            st.warning("Ingen audit-poster funnet ennå. Utfør en handling for å generere poster.")
    except Exception as e:
        st.warning(f"Kunne ikke lese audit_log: {e}")
