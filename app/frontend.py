import streamlit as st
import sqlite3
import pandas as pd
import os
from app.schemas import (
    UserContext,
    MonthlyUnitReportInput,
    BudgetReallocationInput,
    ERPSQLQueryInput,
)
from app.agent import KrsKommuneAgent
from app.tools import (
    get_db_path,
    write_audit_log,
    calculate_monthly_report,
    process_budget_reallocation,
    query_erp_transactions_secure,
)

st.set_page_config(
    page_title="Kristiansand Kommune — AI Control Office",
    page_icon="🏛️",
    layout="wide"
)

# Custom Tufte Styling
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
</style>
""", unsafe_allow_html=True)

st.title("🏛️ Kristiansand Kommune — AI Økonomirådgiver")
st.caption("Beslutningsstøtte for Helse og Mestring & Virksomhetsstyring | Control Office Hub")

# Sidebar: RBAC Context
st.sidebar.header("👤 Brukerkontekst (RBAC)")
role = st.sidebar.selectbox("Velg Rolle", ["enhetsleder", "kommunalsjef", "okonomidirektor", "revisor"])
ansvar = st.sidebar.text_input("Ansvarsnummer", "2530" if role == "enhetsleder" else "2500")

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
    if col_q1.button("📋 Kjør månedsrapport"):
        preset_query = "Vis meg månedlig rapport og avvik for enheten min"
    if col_q2.button("🔮 Hent EOY-prognose"):
        preset_query = "Hva er forventet årsprognose (EOY/EAC)?"
    if col_q3.button("🔄 Sjekk omdisponering"):
        preset_query = "Kan jeg omdisponere 350000 kr til vikarer?"
        
    user_prompt = st.text_input("Still et spørsmål til agenten:", value=preset_query)
    
    if st.button("Send forespørsel", type="primary") and user_prompt:
        with st.spinner("Agenten analyserer regnskapsdata og regelverk..."):
            res = agent.run(user_prompt, user_context)
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
        calc_btn = st.button("Beregn Rapport")
        
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
    st.subheader(f"Dekomponering for Enhet {selected_unit}")
    cost_data = pd.DataFrame([
        {"Art": "1010 Fastlønn", "Forbruk": rep['forbruk'] * 0.65, "Budsjett": rep['budsjett'] * 0.68, "Status": "🟢 I balanse"},
        {"Art": "1020 Vikarer", "Forbruk": rep['forbruk'] * 0.18, "Budsjett": rep['budsjett'] * 0.12, "Status": "🔴 Merforbruk"},
        {"Art": "1040 Overtid", "Forbruk": rep['forbruk'] * 0.08, "Budsjett": rep['budsjett'] * 0.05, "Status": "🔴 Merforbruk"},
        {"Art": "1150 Opplæring/Drift", "Forbruk": rep['forbruk'] * 0.09, "Budsjett": rep['budsjett'] * 0.15, "Status": "🟢 Mindreforbruk"},
    ])
    st.table(cost_data)

# ------------------------------------------------------------------------------
# TAB 3: 📈 FT Visual Vocabulary & 60 Time Visuals EDA Suite
# ------------------------------------------------------------------------------
with tab3:
    st.header("📈 Financial Times & Andy Kriebel 60 Time Visuals (Master Sandbox Suite)")
    st.markdown("""
    Visualiseringene følger **Financial Times Visual Vocabulary** (Alan Smith), **Andy Kriebel 60 Ways to Visualize Time** (EDA) og **Edward Tufte Data-Ink** prinsipper:
    * **96 Master Visuals**: 36 Financial Times kjernevisuals + 60 Andy Kriebel Exploratory Data Analysis (EDA) tidsserievisuals.
    * 0 unødige 3D-elementer, 0 vertikale rutenett i tabeller, direkte merking på akser.
    * Muted municipal fargepalett (`#1b365d`) med rød/gul kun for aktive avvik (§ 14-5).
    """)
    st.success("✨ **Master Visual Sandbox er fullt integrert i portalen!** Åpne [index.html#visual-sandbox](index.html#visual-sandbox) for å utforske alle **96 SVG-diagrammer** med interaktiv DAX-drawer for hver enkelt visual.")

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.subheader("1. Deviation: Netto Kostnadsavvik (CV)")
        chart_data = pd.DataFrame({
            "Enhet": ["2510", "2520", "2530", "2540", "2550"],
            "Netto Avvik (kNOK)": [45, -120, -70, 85, -210]
        }).set_index("Enhet")
        st.bar_chart(chart_data)
        st.caption("Grønne/positive stolper angir mindreforbruk, negative angir merforbruk jf. § 14-5.")

    with col_v2:
        st.subheader("2. Correlation: Sykefravær vs. Overtidskostnad")
        corr_data = pd.DataFrame({
            "Sykefravær %": [4.2, 5.8, 7.1, 8.5, 9.2, 11.4],
            "Overtid (kNOK)": [12, 34, 55, 88, 110, 165]
        }).set_index("Sykefravær %")
        st.line_chart(corr_data)
        st.caption("Sterk korrelasjon mellom sykefravær og overtid/vikarer i helse og mestring (HTA § 4).")

    st.markdown("---")
    st.subheader("⏱️ Andy Kriebel: 60 Ways to Visualize Time — EDA Explorer")
    st.caption("Utforsk de 60 visualiseringene fra Time-Visuals.pdf optimalisert for kommunal Exploratory Data Analysis (EDA).")

    eda_cats = {
        "1. Linjer & Trender (01–10)": [
            ("01 Discrete Line Chart", "Viser diskrete tertial-/kvartalsnivåer (T1–T3) uten kunstig interpolering.", "[EDA_01_Discrete_Line_NOK] = CALCULATE(SUM(Fact_Regnskap[belop]), ALLEXCEPT(Dim_Dato, Dim_Dato[tertial], Dim_Dato[aar]))"),
            ("02 Continuous Line Chart", "Kontinuerlig månedskurve for helhetlig driftstrend over hele året.", "[EDA_02_Continuous_Line_NOK] = SUM(Fact_Regnskap[belop])"),
            ("05 Dashed Line Chart", "Skiller faktisk bokførte måneder (solid) fra usikre framtidige prognosemåneder (stiplet).", "[EDA_05_Dashed_Forecast_NOK] = VAR _M = MAX(Dim_Dato[maned_nr]) RETURN IF(_M > 10, CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Dato[maned_nr] <= 10) * 1.02, BLANK())"),
            ("07 Stepped Line Chart", "Trappetrinnsgraf som viser at bevilgede rammer er faste inntil formelt Bystyrevedtak.", "[EDA_07_Stepped_BudgetCap_NOK] = CALCULATE(SUM(Fact_Budsjett[budsjett_belop]), FILTER(ALL(Dim_Dato), Dim_Dato[dato_key] <= MAX(Dim_Dato[dato_key])))"),
            ("10 Line Ends of Line Labels", "Tufte direkte merking ved kurvens høyre ende uten separat tegnforklaring.", "[EDA_10_EndLabel_Val] = IF(MAX(Dim_Dato[maned_nr]) = 10, SUM(Fact_Regnskap[belop]), BLANK())")
        ],
        "2. Arealer & Glatting (11–18)": [
            ("11 Moving Average", "Glidende 3-måneders snitt som demper månedlig støy fra feriepenger og sesongtopper.", "[EDA_11_MovingAvg_3M_NOK] = AVERAGEX(DATESINPERIOD(Dim_Dato[dato_key], MAX(Dim_Dato[dato_key]), -3, MONTH), SUM(Fact_Regnskap[belop]))"),
            ("16 Stacked Area Chart", "Viser hvordan lønn, vikarer og drift bygger opp den samlede kostnadsprofilen.", "[EDA_16_Stacked_Area_Art] = CALCULATE(SUM(Fact_Regnskap[belop]), KEEPFILTERS(Dim_Art[art_gruppe]))"),
            ("17 % of Total Area Chart", "Normaliserer månedene til 100 % for å avdekke strukturell forskyvning i kostnadsmiksen.", "[EDA_17_Pct_Total_Area] = DIVIDE(SUM(Fact_Regnskap[belop]), CALCULATE(SUM(Fact_Regnskap[belop]), ALL(Dim_Art[art_gruppe])), 0)")
        ],
        "3. Avvik & Vekstrater (19–25)": [
            ("19 Difference from Previous", "Måned-for-måned nominell differanse (MoM Δ) for å fange brå kostnadshopp.", "[EDA_19_Diff_From_Previous_MoM] = VAR _Prev = CALCULATE(SUM(Fact_Regnskap[belop]), DATEADD(Dim_Dato[dato_key], -1, MONTH)) RETURN SUM(Fact_Regnskap[belop]) - _Prev"),
            ("20 % Difference from Previous", "Månedlig vekstrate i prosent som måler om forbruket akselererer eller bremser opp.", "[EDA_20_Pct_Diff_From_Previous] = VAR _Prev = CALCULATE(SUM(Fact_Regnskap[belop]), DATEADD(Dim_Dato[dato_key], -1, MONTH)) RETURN DIVIDE(SUM(Fact_Regnskap[belop]) - _Prev, _Prev, 0)"),
            ("23 Running Total", "Akkumulert YTD-kostnadskurve som viser gjenstående budsjettrom fram mot årsslutt.", "[EDA_23_Running_Total_YTD] = TOTALYTD(SUM(Fact_Regnskap[belop]), Dim_Dato[dato_key])")
        ],
        "4. Stolper & Referanser (26–33)": [
            ("29 Paired Column Chart", "Faktisk vs. Periodisert budsjett side-om-side per måned for umiddelbar visuell avstemming.", "[EDA_29_Paired_Actual] = SUM(Fact_Regnskap[belop])\n[EDA_29_Paired_Budget] = SUM(Fact_Budsjett[budsjett_belop])"),
            ("31 Lollipop Chart", "Slank søyle med topp-sirkel; minimerer blekkmengden og leder blikket presist til måleverdien.", "[EDA_31_Lollipop_Value_NOK] = SUM(Fact_Regnskap[belop])"),
            ("32 Bar-in-Bar Chart", "Smal faktisk søyle inni en bredere budsjettsøyle; kompakt måloppnåelse uten behov for to diagrammer.", "[EDA_32_BarInBar_Actual] = SUM(Fact_Regnskap[belop])\n[EDA_32_BarInBar_Budget] = SUM(Fact_Budsjett[budsjett_belop])")
        ],
        "5. Multi-Mål & Snitt (34–39)": [
            ("34 Dual Axis w/ Different Measures", "Forbruk i Mkr på venstre akse mot sykefravær i % på høyre akse for å avdekke samvariasjon.", "[EDA_34_DualAxis_Spend_MNOK] = DIVIDE(SUM(Fact_Regnskap[belop]), 1000000, 0)\n[EDA_34_DualAxis_Frav_Pct] = [FT_Corr_Sykefravaer_Pct]"),
            ("35 Dual Axis w/ Related Measures", "Brutto utgifter og inntekter på felles synkronisert skala jf. bruttoprinsippet § 14-6.", "[EDA_35_DualAxis_Expenses] = CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Art[art_kode] < '1600')\n[EDA_35_DualAxis_Revenues] = CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Art[art_kode] >= '1600')"),
            ("38 Cycle Plot", "Sammenligner alle januarmåneder, februarmåneder osv. over 3 regnskapsår for å skille sann sesong fra tilfeldigheter.", "[EDA_38_Cycle_Plot_Seasonal_Mean] = AVERAGEX(KEEPFILTERS(VALUES(Dim_Dato[aar])), SUM(Fact_Regnskap[belop]))")
        ],
        "6. Helning & Sommerfugl (40–45)": [
            ("40 Discrete Slope Graph", "Sammenligner sektorenes kostnadsnivå mellom T1 og T2 med rette linjer for å vise endringshastighet.", "[EDA_40_Slope_Start] = CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Dato[tertial] = 'T1')\n[EDA_40_Slope_End] = CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Dato[tertial] = 'T2')"),
            ("42 Butterfly Chart Single Axis", "Speilvendte stolper på felles nullakse: Utgifter til venstre, inntekter til høyre for selvkostområder.", "[EDA_42_Butterfly_Expense] = -ABS(CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Art[art_kode] < '1600'))\n[EDA_42_Butterfly_Revenue] = ABS(CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Art[art_kode] >= '1600'))"),
            ("45 Barcode Chart", "Tette vertikale linjer der linjetettheten gjenspeiler fakturafrekvens og periodiseringspropper.", "[EDA_45_Barcode_Tx_Density] = DISTINCTCOUNT(Fact_Regnskap[transaksjon_hash])")
        ],
        "7. Mikro & Forløp (46–51)": [
            ("46 Sparklines", "Aksefrie miniatyrkurver designet for tabeller; gir 81 enhetsledere en umiddelbar 12-måneders visuell puls.", "[EDA_46_Sparkline_Monthly] = SUM(Fact_Regnskap[belop])"),
            ("49 Connected Dot Plot", "Viser spennet fra M1 til M10 for hver sektor med direkte forbindelsesstrek mellom punktene.", "[EDA_49_Dumbbell_Start] = CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Dato[maned_nr] = 1)\n[EDA_49_Dumbbell_End] = CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Dato[maned_nr] = 10)"),
            ("51 Circle Timeline", "Sirkler skalert proporsjonalt med budsjettavvikets størrelse plassert langs tidslinjen.", "[EDA_51_Circle_Timeline_Radius] = SQRT(ABS(SUM(Fact_Regnskap[belop]) - SUM(Fact_Budsjett[budsjett_belop])))")
        ],
        "8. Avansert EDA & Volatilitet (52–60)": [
            ("52 Bump Chart", "Viser hvordan de 6 sektorenes rangering etter merforbruk endrer seg fra M1 til M10.", "[EDA_52_Bump_Sector_Rank] = RANKX(ALL(Dim_Ansvar[sektor]), SUM(Fact_Regnskap[belop]), , DESC, Dense)"),
            ("53 Seismogram", "Høyfrekvente svingninger rundt null; fanger likviditetsbølger, skattetrekk og store momsoppgjør.", "[EDA_53_Seismogram_Daily_Shock] = SUM(Fact_Regnskap[belop]) - AVERAGEX(ALL(Dim_Dato[dato_key]), SUM(Fact_Regnskap[belop]))"),
            ("60 Stock Chart (High-Low-Close)", "Minste dagsforbruk, høyeste dagsforbruk og saldo ved månedsslutt; overvåker likviditetsrisiko.", "[EDA_60_Stock_High] = MAXX(VALUES(Dim_Dato[dato_key]), CALCULATE(SUM(Fact_Regnskap[belop])))\n[EDA_60_Stock_Low] = MINX(VALUES(Dim_Dato[dato_key]), CALCULATE(SUM(Fact_Regnskap[belop])))\n[EDA_60_Stock_Close] = CALCULATE(SUM(Fact_Regnskap[belop]), LASTDATE(Dim_Dato[dato_key]))")
        ]
    }

    sel_eda_cat = st.selectbox("Velg EDA Gruppe", list(eda_cats.keys()))
    chart_opts = eda_cats[sel_eda_cat]
    sel_chart_name = st.selectbox("Velg Visual fra Andy Kriebels liste", [c[0] for c in chart_opts])
    sel_chart_obj = next(c for c in chart_opts if c[0] == sel_chart_name)

    st.info(f"**EDA Formål:** {sel_chart_obj[1]}")
    st.code(sel_chart_obj[2], language="sql")
    st.caption("Komplett masterfil med samtlige 60 DAX-mål finnes i `powerbi/09_Andy_Kriebel_60_Time_Visuals_EDA_Measures.dax`.")

# ------------------------------------------------------------------------------
# TAB 4: 🔮 EOY Prognose
# ------------------------------------------------------------------------------
with tab4:
    st.header("🔮 Rullende Årssluttprognose (EOY / EAC)")
    st.markdown("Prognosemodellen kombinerer historisk sesongprofil, Monte Carlo-usikkerhet og Earned Value Management (EVM).")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    col_p1.metric("Vedtatt årsbudsjett (BAC)", "kr 17 900 000")
    col_p2.metric("Forventet årsslutt (EAC P50)", "kr 18 450 000", delta="-550 000", delta_color="inverse")
    col_p3.metric("Kostnadsindeks (CPI)", "0.96", delta="Merforbruk", delta_color="inverse")
    
    st.markdown("---")
    st.subheader("Monte Carlo Usikkerhetsspenn (P10 - P50 - P90)")
    mc_df = pd.DataFrame({
        "Persentil": ["P10 (Beste utfall)", "P50 (Forventet)", "P90 (Konservativt)"],
        "Prognose (NOK)": [18100000, 18450000, 18920000],
        "Avvik mot ramme (VAC)": [-200000, -550000, -1020000],
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
    dd_col2.selectbox("Nivå 2: Område", ["Omsorgssentre", "Hjemmetjenester", "Mestring"])
    dd_col3.text_input("Nivå 3: Enhet/Ansvar", value=user_context.ansvar_code or "2530")
    
    st.subheader("Bilagstransaksjoner (Nivå 6) med RBAC")
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
    st.markdown("Automatisk kontroll av fullmaktsgrenser jf. **Kommuneloven § 14-5** og kommunens økonomireglement.")
    
    with st.form("realloc_form"):
        col_r1, col_r2 = st.columns(2)
        fra_ansvar = col_r1.text_input("Fra Ansvarsnummer", value=user_context.ansvar_code or "2530")
        til_ansvar = col_r2.text_input("Til Ansvarsnummer", value="2540")
        belop = st.number_input("Beløp (NOK)", min_value=1000.0, max_value=5000000.0, value=350000.0, step=10000.0)
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
