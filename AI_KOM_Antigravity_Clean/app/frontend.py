import streamlit as st
import sqlite3
import pandas as pd
from app.schemas import UserContext
from app.agent import KrsKommuneAgent
from app.tools import write_audit_log

st.set_page_config(page_title="Kristiansand Kommune — AI Control Office", layout="wide")

st.title("🏛️ Kristiansand Kommune — AI Økonomirådgiver")
st.caption("Beslutningsstøtte for Helse og Mestring | Control Office Hub")

st.sidebar.header("👤 Brukerkontekst (RBAC)")
role = st.sidebar.selectbox("Velg Rolle", ["enhetsleder", "kommunalsjef", "okonomidirektor", "revisor"])
ansvar = st.sidebar.text_input("Ansvarsnummer", "2530" if role == "enhetsleder" else "2500")

user_context = UserContext(
    user_id="demo_user_1",
    role=role,
    ansvar_code=ansvar
)

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

with tab1:
    st.header("💬 Chat med AI-Økonomirådgiver")
    user_prompt = st.text_input("Still et spørsmål om økonomi, avvik eller prognose:")
    if st.button("Send forespørsel"):
        res = agent.run(user_prompt, user_context)
        st.success(res["response"])

with tab7:
    st.header("📜 Audit-Logg & Revisjonsspor (Arkivlova)")
    st.info("Uforanderlig endringslogg for Agder Kontrollutvalg og Kommunerevisjonen (NKRF).")
    try:
        conn = sqlite3.connect("data/db/kommune_golden_record.db")
        df = pd.read_sql_query("SELECT * FROM audit_log ORDER BY id DESC LIMIT 50", conn)
        st.dataframe(df, use_container_width=True)
        conn.close()
    except Exception as e:
        st.warning("Ingen audit-poster funnet ennå eller databasen er under opprettelse.")
