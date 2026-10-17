#!/usr/bin/env python3
"""
Streamlit Web Portal: MVP-Pilot Kommunal Økonomistyring (Bo og Miljø)
Human-in-the-Loop AI Controller Dashboard with Excel Writeback
"""

import sys
from pathlib import Path
from datetime import datetime

# Sikre at pilotmappen alltid er i sys.path uansett hvor streamlit startes fra
PILOT_DIR = Path(__file__).resolve().parent
if str(PILOT_DIR) not in sys.path:
    sys.path.insert(0, str(PILOT_DIR))

import streamlit as st
import pandas as pd
import sqlite3

# Importer lokale pilot-moduler
from config import EXCEL_SOURCE, EXCEL_RAPPORT_BO_MILJO, DB_SQLITE, DB_DUCKDB, DEFAULT_ENHET_NAVN, DEFAULT_KOSTRA_FUNKSJON, DEFAULT_SAKSBEHANDLER, OLLAMA_BASE_URL
from etl import ingest_excel_to_databases

# Selvreparerende sjekk: hvis databasen ikke finnes, kjør ETL automatisk
if not DB_DUCKDB.exists() or not DB_SQLITE.exists():
    ingest_excel_to_databases()

from eac_forecasting import compute_eac_forecasts
from prescriptive_agent import evaluate_measures_with_ai, DEFAULT_CANDIDATE_MEASURES, call_ollama
from hitl_governance import apply_decisions_and_writeback
from executive_report import generate_executive_memo

st.set_page_config(
    page_title="Kristiansand EPM · AI-Styring Bo og Miljø",
    page_icon="🏛️",
    layout="wide"
)

# Tufte-inspirert stilren CSS
st.markdown("""
<style>
    .reportview-container { background: #FAFBFD; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    h1, h2, h3 { color: #1A202C; font-weight: 600; }
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .metric-val { font-size: 1.5rem; font-weight: 700; color: #1A202C; margin-top: 4px; }
    .metric-sub { font-size: 0.85rem; color: #718096; }
    .badge-red { background: #FFF5F5; color: #C53030; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.75rem; }
    .badge-green { background: #F0FFF4; color: #22543D; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.75rem; }
</style>
""", unsafe_allow_html=True)

# Tittel og kontekst
st.title("Kristiansand EPM · AI-Pilot: Bo og Miljø")
st.caption(f"Enhet: {DEFAULT_ENHET_NAVN} (KOSTRA funksjon {DEFAULT_KOSTRA_FUNKSJON}) | Excel-rapporter: {EXCEL_RAPPORT_BO_MILJO.name} & {EXCEL_SOURCE.name}")

# Last data
forecast_data = compute_eac_forecasts()
annual_budget = forecast_data["annual_budget"]
actual_ytd = forecast_data["actual_ytd"]
ytd_variance = forecast_data["ytd_variance"]
budget_ytd = actual_ytd + ytd_variance
eac_ai = forecast_data["models"]["driver_based_ai"]["eac"]

# Hent godkjente tiltak fra audit tabell
con = sqlite3.connect(DB_SQLITE)
cur = con.cursor()
cur.execute("""
    SELECT measure_id, estimated_effect, decision, control_documented, justification, approved_by, timestamp
    FROM Audit_AI_Actions
    ORDER BY action_id DESC;
""")
audit_history = cur.fetchall()
con.close()

approved_measures = {row[0]: row[1] for row in audit_history if row[2] == "Godkjent" and row[3] == "Ja"}
total_approved_effect = sum(approved_measures.values())
eac_revidert = eac_ai - total_approved_effect
rest_avvik = annual_budget - eac_revidert

# KPI-linje
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"""<div class="metric-card"><div class="metric-sub">Årsbudsjett (BAC)</div><div class="metric-val">{annual_budget:,.0f} kr</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="metric-card"><div class="metric-sub">Bokført Regnskap YTD</div><div class="metric-val">{actual_ytd:,.0f} kr</div></div>""", unsafe_allow_html=True)
with col3:
    col_color_3 = "#2F855A" if ytd_variance >= 0 else "#C53030"
    badge_cls_3 = "badge-green" if ytd_variance >= 0 else "badge-red"
    sign_3 = "+" if ytd_variance >= 0 else ""
    st.markdown(f"""<div class="metric-card"><div class="metric-sub">Avvik YTD (Budsjett - Regnskap)</div><div class="metric-val" style="color: {col_color_3};">{sign_3}{ytd_variance:,.0f} kr <span class="{badge_cls_3}">{sign_3}{(ytd_variance/budget_ytd)*100:.1f} %</span></div></div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="metric-card"><div class="metric-sub">Godkjent AI-Effekt (HITL)</div><div class="metric-val" style="color: #2F855A;">+{total_approved_effect:,.0f} kr <span class="badge-green">{len(approved_measures)} godkjent</span></div></div>""", unsafe_allow_html=True)
with col5:
    col_color_5 = "#2F855A" if rest_avvik >= 0 else "#C53030"
    sign_5 = "+" if rest_avvik >= 0 else ""
    st.markdown(f"""<div class="metric-card"><div class="metric-sub">Revidert Restavvik EOY</div><div class="metric-val" style="color: {col_color_5};">{sign_5}{rest_avvik:,.0f} kr</div></div>""", unsafe_allow_html=True)

st.write("")

# Tabs
tab_status, tab_eac, tab_tiltak, tab_audit = st.tabs([
    "1. Nåsituasjon & Drivere",
    "2. Prediktiv EAC/ETC",
    "3. Preskriptiv AI & Godkjenning (HITL)",
    "4. Revisjonsspor & Saksfremlegg"
])

with tab_status:
    st.subheader("Bokførte avviksdrivere (Status per 2. tertial)")
    st.write("Identifisering av drivere i KOSTRA-kontoplanen som overskrider budsjettert ramme:")
    
    top_drivers = pd.DataFrame(forecast_data["top_drivers"])
    if not top_drivers.empty:
        top_drivers.columns = ["KOSTRA Art", "Kontonavn", "YTD Merforbruk (kr)", "Månedsgjennomsnitt (kr)", "Estimert T3 (kr)"]
        st.dataframe(
            top_drivers.style.format({
                "YTD Merforbruk (kr)": "{:,.0f}",
                "Månedsgjennomsnitt (kr)": "{:,.0f}",
                "Estimert T3 (kr)": "{:,.0f}"
            }),
            use_container_width=True
        )

with tab_eac:
    st.subheader("Prediktiv Prognose (End of Year - EAC)")
    st.write("Sammenligning mellom manuell sjablong, mekanisk run-rate og AI-modellert sesongjustert EAC:")
    
    eac_comparison = []
    for k, m in forecast_data["models"].items():
        eac_comparison.append({
            "Modell": m["name"],
            "EAC Prognose (kr)": m["eac"],
            "Prognosert Avvik (kr)": m["variance"],
            "Avvik %": m["variance_pct"]
        })
    df_eac = pd.DataFrame(eac_comparison)
    st.dataframe(df_eac.style.format({
        "EAC Prognose (kr)": "{:,.0f}",
        "Prognosert Avvik (kr)": "{:,.0f}",
        "Avvik %": "{:.1f} %"
    }), use_container_width=True)

    p = forecast_data["confidence_interval"]
    st.info(f"**AI Konfidensintervall (Monte Carlo / Historisk volatilitet):**\n- P10 (Beste utfall): **{p['p10']:,.0f} kr**\n- P50 (Forventningsrett): **{p['p50']:,.0f} kr**\n- P90 (Stresstest/Worst-case): **{p['p90']:,.0f} kr**")

    st.subheader("Kumulativ Kostnadskurve & Prognoseløp (Tufte S-Kurve Standard)")
    st.caption("Viser påløpt faktisk kostnad (mnd 1–8), budsjettbaseline og AI-modellert prognosebane (mnd 9–12) uten vertikale gitterlinjer.")
    
    # Hent månedstall fra DuckDB
    con_c = duckdb.connect(str(DB_DUCKDB), read_only=True)
    monthly_df = con_c.execute("""
        SELECT 
            Måned_Nr,
            Måned,
            SUM(Budsjett) AS Budsjett_Mnd,
            SUM(CASE WHEN Status = 'Bokført' THEN Regnskap ELSE 0 END) AS Regnskap_Mnd
        FROM fact_bomiljo
        GROUP BY Måned_Nr, Måned
        ORDER BY Måned_Nr;
    """).df()
    con_c.close()

    monthly_df["Kumulativt Budsjett (BAC)"] = monthly_df["Budsjett_Mnd"].cumsum()
    
    # Faktisk kumulativt for måned 1-8
    regnskap_cum = []
    curr_act = 0.0
    for _, row in monthly_df.iterrows():
        if row["Måned_Nr"] <= 8:
            curr_act += row["Regnskap_Mnd"]
            regnskap_cum.append(curr_act)
        else:
            regnskap_cum.append(None)
    monthly_df["Faktisk Påløpt (AC)"] = regnskap_cum

    # AI EAC forløp (mnd 8 til 12)
    etc_rest = eac_ai - actual_ytd
    ai_cum = []
    for _, row in monthly_df.iterrows():
        m_nr = row["Måned_Nr"]
        if m_nr < 8:
            ai_cum.append(None)
        elif m_nr == 8:
            ai_cum.append(actual_ytd)
        else:
            step = (m_nr - 8) / 4.0
            ai_cum.append(round(actual_ytd + (etc_rest * step), 2))
    monthly_df["AI Sesongprognose (EAC)"] = ai_cum

    chart_data = monthly_df.set_index("Måned")[["Kumulativt Budsjett (BAC)", "Faktisk Påløpt (AC)", "AI Sesongprognose (EAC)"]]
    st.line_chart(chart_data)

with tab_tiltak:
    st.subheader("Preskriptive Kandidattiltak · Human-in-the-Loop (HITL)")
    st.write("Vurder tiltakene i henhold til Kommuneloven § 14-5 og HTA § 4. Ingen effekt tas med i regnskapsprognosen før kontroll er dokumentert.")

    ai_eval = evaluate_measures_with_ai()
    st.caption(f"💡 **AI Rådgiver (Ollama LLM):** {ai_eval['llm_commentary']}")

    with st.form("hitl_approval_form"):
        decisions_input = {}
        for m in DEFAULT_CANDIDATE_MEASURES:
            mid = m["id"]
            is_currently_approved = mid in approved_measures

            st.markdown(f"#### [{mid}] {m['title']}")
            c1, c2, c3, c4 = st.columns([2, 1.5, 1.5, 3])
            with c1:
                st.write(f"**EOY-effekt:** {m['eoy_effect']:,.0f} kr  \n**Krav:** `{m['governance_need']}`")
            with c2:
                dec = st.selectbox(
                    f"Beslutning for {mid}",
                    ["Kandidat", "Godkjent", "Avvist"],
                    index=1 if is_currently_approved else 0,
                    key=f"dec_{mid}"
                )
            with c3:
                dok = st.selectbox(
                    f"Kontroll dokumentert {mid}",
                    ["Nei", "Ja"],
                    index=1 if is_currently_approved else 0,
                    key=f"dok_{mid}"
                )
            with c4:
                begrunnelse = st.text_input(
                    f"Faglig begrunnelse ({mid})",
                    value="Avklart iht. saksbehandling." if is_currently_approved else m["next_step"],
                    key=f"begr_{mid}"
                )
            decisions_input[mid] = {
                "decision": dec,
                "control_documented": dok,
                "justification": begrunnelse
            }
            st.divider()

        saksbehandler = st.text_input("Ansvarlig saksbehandler/controller", value=DEFAULT_SAKSBEHANDLER)
        submit_btn = st.form_submit_button("💾 Lagre vedtak & Skriv tilbake til Excel-arbeidsbok")

        if submit_btn:
            result = apply_decisions_and_writeback(
                decisions_dict=decisions_input,
                target_excel=EXCEL_SOURCE,
                create_backup=True,
                approved_by=saksbehandler
            )
            warnings = []
            if not result.get("bo_miljo_report", {}).get("updated"):
                warnings.append(result.get("bo_miljo_report", {}).get("reason", "Rapport Enhet Bo og Miljø ikke oppdatert"))
            if not result.get("mini_case", {}).get("updated"):
                warnings.append(result.get("mini_case", {}).get("reason", "Mini case ikke oppdatert"))
                
            if warnings:
                st.warning("⚠️ " + " | ".join(warnings))
            else:
                st.success(f"✓ {result['antall_godkjente']} tiltak godkjent! Oppdatert i {Path(result['target_file']).name} og logget i revisjonssporet.")
            st.rerun()

with tab_audit:
    st.subheader("Revisjonsspor (Audit Trail · EU AI Act Art. 14 / GDPR)")
    if audit_history:
        audit_df = pd.DataFrame(audit_history, columns=["Tiltak", "Effekt (kr)", "Beslutning", "Kontroll", "Begrunnelse", "Godkjent Av", "Tidspunkt"])
        st.dataframe(audit_df.style.format({"Effekt (kr)": "{:,.0f}"}), use_container_width=True)
    else:
        st.info("Ingen handlinger logget ennå.")

    if st.button("📄 Generer Tufte Økonominotat til Kommunalsjef"):
        report_path = generate_executive_memo(approver=DEFAULT_SAKSBEHANDLER)
        st.success(f"Notat opprettet: {report_path.name}")
        report_text = report_path.read_text(encoding="utf-8")
        st.download_button(
            label="⬇️ Last ned økonominotat (.md)",
            data=report_text,
            file_name=report_path.name,
            mime="text/markdown"
        )
        st.markdown(report_text)
