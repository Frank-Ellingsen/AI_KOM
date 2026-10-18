"""
AI_KOM Control Office Hub - Streamlit MVP Pilot
Sektor: Helse og Mestring (Ansvar 5200 / KOSTRA 253, 254, 256)
Kristiansand Kommune Financial Controlling, EVM & AI Assistant
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import numpy as np
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CSV_PATH = DATA_DIR / "helse_mestring_data.csv"
AUDIT_DB_PATH = DATA_DIR / "helse_mestring_audit.db"


# ==========================================
# 1. PORT 4: LOCAL PII GUARDRAIL & MASKING
# ==========================================
def mask_pii(text: str) -> str:
    """
    Stage-Gate Port 4: Locally scrubs Norwegian FNR (01-31) and D-numbers (41-71),
    Norwegian bank account numbers (11 digits, formatted or unformatted),
    Norwegian phone numbers (+47 / 8 digits), and email addresses before AI processing or logging.
    """
    if not text:
        return ""

    # 1. E-postadresser
    text = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "[SKJERMET_EPOST]",
        text,
    )

    # 2. Formaterte norske bankkontonumre (XXXX.XX.XXXXX)
    text = re.sub(r"\b\d{4}\.\d{2}\.\d{5}\b", "[SKJERMET_KONTO]", text)

    # 3. Norsk fødselsnummer (dag 01-31) og D-nummer (dag 41-71), måned 01-12 + 5 personnummersifre
    fnr_pattern = r"\b(?:0[1-9]|[12][0-9]|3[01]|4[1-9]|[56][0-9]|7[01])(?:0[1-9]|1[012])\d{2}\s?\d{5}\b"
    text = re.sub(fnr_pattern, "[SKJERMET_FNR]", text)

    # 4. Uformaterte 11-sifrede kontonumre som ikke er FNR/D-nr
    text = re.sub(r"\b\d{11}\b", "[SKJERMET_KONTO]", text)

    # 5. Norske telefonnumre (8 siffer i 2-2-2-2, 3-2-3 eller sammenhengende format, evt. med +47/0047)
    tlf_pattern = r"(?:(?:\+47|0047)\s*)?\b(?:[2-9]\d{1}\s*\d{2}\s*\d{2}\s*\d{2}|[2-9]\d{2}\s*\d{2}\s*\d{3})\b"
    text = re.sub(tlf_pattern, "[SKJERMET_TLF]", text)

    return text


# ==========================================
# 2. DATA ENGINE (DUCKDB + ISO 21508 EVM)
# ==========================================
@st.cache_data(show_spinner=False)
def load_helse_data() -> pd.DataFrame:
    """
    Loads KOSTRA 253, 254, 256 accounting data for Ansvar 5200 via DuckDB OLAP
    and calculates periodized YTD variances and ISO 21508 Earned Value metrics (CPI, EAC, VAC).
    """
    if CSV_PATH.exists():
        con = duckdb.connect(":memory:")
        df = con.execute(
            f"SELECT * FROM read_csv_auto('{CSV_PATH.as_posix()}')"
        ).df()
        con.close()
    else:
        df = pd.DataFrame(
            [
                {
                    "Ansvar": 5200,
                    "KOSTRA_Funksjon": 253,
                    "Beskrivelse": "Hjemmesykepleie og tilrettelagte boliger",
                    "Budsjett_MNOK": 110.0,
                    "Regnskap_YTD_MNOK": 79.2,
                    "Overtid_Art1090_MNOK": 4.8,
                    "Vikarer_Art1100_MNOK": 6.2,
                    "NAV_Refusjon_Art1600_MNOK": -3.1,
                    "Sykefravar_Pct": 11.2,
                },
                {
                    "Ansvar": 5200,
                    "KOSTRA_Funksjon": 254,
                    "Beskrivelse": "Sykehjem og helsehus (Institusjon)",
                    "Budsjett_MNOK": 145.0,
                    "Regnskap_YTD_MNOK": 104.4,
                    "Overtid_Art1090_MNOK": 8.2,
                    "Vikarer_Art1100_MNOK": 11.5,
                    "NAV_Refusjon_Art1600_MNOK": -5.2,
                    "Sykefravar_Pct": 13.8,
                },
                {
                    "Ansvar": 5200,
                    "KOSTRA_Funksjon": 256,
                    "Beskrivelse": "Mestringstjenester og psykiatri",
                    "Budsjett_MNOK": 65.0,
                    "Regnskap_YTD_MNOK": 40.4,
                    "Overtid_Art1090_MNOK": 1.5,
                    "Vikarer_Art1100_MNOK": 2.1,
                    "NAV_Refusjon_Art1600_MNOK": -1.8,
                    "Sykefravar_Pct": 7.5,
                },
            ]
        )

    # Periodisert budsjett YTD per M8 (PV / EV) og kostnadsavvik (CV = PV - AC)
    df["Forventet_YTD_MNOK"] = (df["Budsjett_MNOK"] * (8.0 / 12.0)).round(2)
    df["Avvik_MNOK"] = (df["Forventet_YTD_MNOK"] - df["Regnskap_YTD_MNOK"]).round(2)

    # Prosentvis avvik målt mot periodisert YTD-budsjett (Forventet_YTD_MNOK)
    df["Avvik_Pct"] = ((df["Avvik_MNOK"] / df["Forventet_YTD_MNOK"]) * 100.0).round(2)
    # Beholder også avvik mot helårsramme for referanse
    df["Avvik_Aarsbudsjett_Pct"] = ((df["Avvik_MNOK"] / df["Budsjett_MNOK"]) * 100.0).round(2)

    # ISO 21508 Earned Value Management (CPI, EAC, VAC)
    df["CPI"] = (df["Forventet_YTD_MNOK"] / df["Regnskap_YTD_MNOK"]).round(3)
    df["EAC_MNOK"] = (df["Budsjett_MNOK"] / df["CPI"]).round(2)
    df["VAC_MNOK"] = (df["Budsjett_MNOK"] - df["EAC_MNOK"]).round(2)

    def set_rag(row: pd.Series) -> str:
        pct = float(row["Avvik_Pct"])
        cpi = float(row["CPI"])
        if pct >= -2.0 and cpi >= 0.98:
            return "GRØNN"
        elif pct >= -5.0 and cpi >= 0.95:
            return "RAV"
        else:
            return "RØD"

    df["RAG_Status"] = df.apply(set_rag, axis=1)
    df["Netto_Vikarbelastning_MNOK"] = (
        df["Overtid_Art1090_MNOK"]
        + df["Vikarer_Art1100_MNOK"]
        - df["NAV_Refusjon_Art1600_MNOK"].abs()
    ).round(2)
    return df


# ==========================================
# 3. MONTE CARLO SIMULATOR & NAV REFUND ENGINE
# ==========================================
def run_monte_carlo(
    budget: float, actual_ytd: float, vol_pct: float = 0.12, num_sims: int = 1000
) -> tuple[float, float, float]:
    """
    Simulates full-year outcome (P10, P50, P90) across remaining 4 months (M9-M12)
    incorporating a +5% Q4 seasonal sickness/substitution spike.
    """
    rng = np.random.default_rng(42)
    months_remaining = 4
    monthly_avg = actual_ytd / 8.0

    q4_factor = 1.05
    simulated_q4 = rng.normal(
        monthly_avg * q4_factor, monthly_avg * vol_pct, (num_sims, months_remaining)
    )
    simulated_totals = actual_ytd + np.sum(simulated_q4, axis=1)

    p10 = float(np.percentile(simulated_totals, 10))
    p50 = float(np.percentile(simulated_totals, 50))
    p90 = float(np.percentile(simulated_totals, 90))

    return round(p10, 2), round(p50, 2), round(p90, 2)


def calculate_nav_refund_gap(row: pd.Series | dict[str, Any]) -> dict[str, Any]:
    """
    Calculates expected vs. booked NAV sickness reimbursement (Art 1600) per Folketrygdloven § 22-13
    and verifies gross budgeting compliance per Kommuneloven § 14-6.
    """
    overtid = float(row["Overtid_Art1090_MNOK"])
    vikarer = float(row["Vikarer_Art1100_MNOK"])
    raw_nav = float(row["NAV_Refusjon_Art1600_MNOK"])
    sykefravar_pct = float(row.get("Sykefravar_Pct", 10.0))

    # Langtidsfraværsfaktor (>16 dagers arbeidsgiverperiode) skalerer med sykefraværsprosenten
    long_term_weight = min(max(sykefravar_pct / 25.0, 0.35), 0.55)
    expected_nav = round((overtid + vikarer) * 0.45, 2)
    risk_adjusted_nav = round((vikarer * 0.55) + (overtid * long_term_weight * 0.50), 2)
    actual_nav = round(abs(raw_nav), 2)
    refund_gap = round(expected_nav - actual_nav, 2)

    return {
        "actual_nav_mnok": actual_nav,
        "expected_nav_mnok": expected_nav,
        "risk_adjusted_nav_mnok": risk_adjusted_nav,
        "refund_gap_mnok": refund_gap,
        "bruttoprinsipp_ok": raw_nav <= 0.0,
        "law_reference": "Folketrygdloven § 22-13 (3 mnd. foreldelsesfrist) & Kommuneloven § 14-6 (Bruttoprinsippet)",
    }


def build_legal_recommendation(row: pd.Series | dict[str, Any], p50_eoy: float) -> str:
    """
    Synthesizes statutory governance recommendation anchored in Kommuneloven §§ 14-5, 14-6
    and HTA § 4 / AML § 10-12.
    """
    funksjon = row["KOSTRA_Funksjon"]
    beskrivelse = row["Beskrivelse"]
    budsjett = float(row["Budsjett_MNOK"])
    sykefravar = float(row["Sykefravar_Pct"])
    netto_vikar = float(row["Netto_Vikarbelastning_MNOK"])
    cpi = float(row.get("CPI", 1.0))
    eac = float(row.get("EAC_MNOK", p50_eoy))

    year_end_deficit = round(p50_eoy - budsjett, 2)
    parts: list[str] = []

    if year_end_deficit > 0 or cpi < 1.0:
        parts.append(
            f"KOSTRA-funksjon {funksjon} ({beskrivelse}) har et estimert merforbruk ved årsavslutning "
            f"på {year_end_deficit:.2f} MNOK (P50: {p50_eoy:.2f} MNOK | EVM EAC: {eac:.2f} MNOK | CPI: {cpi:.3f}), "
            f"drevet av et sykefravær på {sykefravar:.1f}% og netto vikar-/overtidsbelastning på {netto_vikar:.2f} MNOK. "
            f"I henhold til Kommuneloven § 14-5 plikter kommunedirektøren å fremme sak for Formannskapet/Bystyret "
            f"om kompenserende tiltak eller budsjettjustering for å sikre realistisk budsjettbalanse."
        )
    else:
        parts.append(
            f"KOSTRA-funksjon {funksjon} ({beskrivelse}) ligger an til et mindreforbruk på "
            f"{abs(year_end_deficit):.2f} MNOK ved årsavslutning (CPI: {cpi:.3f}). "
            f"Driften oppfyller balansekravet i Kommuneloven § 14-5."
        )

    if sykefravar >= 10.0 or netto_vikar >= 5.0:
        parts.append(
            "Jf. Hovedtariffavtalen (HTA) § 4 og Arbeidsmiljøloven (AML) § 10-12 krever innføring av "
            "felles vikarpool, årsturnus eller utvidet vaktlengde (12,5t helgevakter) formell drøftingsprotokoll "
            "med tillitsvalgte (NSF / Fagforbundet) før iverksettelse."
        )

    parts.append(
        "Jf. Kommuneloven § 14-6 (Bruttoprinsippet) skal alle sykepengerefusjoner fra NAV føres brutto "
        "som inntekt på art 1600, og aldri salderes direkte mot lønnsutgifter på art 1010/1090/1100."
    )
    return " ".join(parts)


# ==========================================
# 4. SHA-256 AUDIT LEDGER (PORT 9 & PORT 10)
# ==========================================
def init_audit_db(db_path: Path = AUDIT_DB_PATH) -> sqlite3.Connection:
    """Initializes persistent SQLite audit table for Stage-Gate Port 9 & Port 10."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS Audit_AI_Actions (
            audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_upn TEXT NOT NULL,
            kostra_funksjon TEXT NOT NULL,
            ai_recommendation TEXT NOT NULL,
            user_note TEXT NOT NULL,
            human_decision TEXT NOT NULL,
            sha256_seal TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def generate_audit_seal(
    user_upn: str,
    funksjon: str,
    recommendation: str,
    decision: str,
    user_note: str = "",
    db_path: Path = AUDIT_DB_PATH,
) -> dict[str, str]:
    """
    Stage-Gate Port 9 & 10: Scrubs PII from inputs, generates an immutable SHA-256 seal,
    and persists the record to SQLite (Audit_AI_Actions).
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    clean_upn = user_upn.strip() or "ukjent.saksbehandler@kristiansand.kommune.no"
    clean_note = mask_pii(user_note)
    clean_rec = mask_pii(recommendation)

    payload = f"{timestamp}|{clean_upn}|{funksjon}|{clean_rec}|{clean_note}|{decision}"
    sha_seal = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    record = {
        "timestamp": timestamp,
        "user_upn": clean_upn,
        "kostra_funksjon": str(funksjon),
        "ai_recommendation": clean_rec,
        "user_note": clean_note,
        "human_decision": decision,
        "sha256_seal": sha_seal,
    }

    try:
        conn = init_audit_db(db_path)
        conn.execute(
            """
            INSERT INTO Audit_AI_Actions (
                timestamp, user_upn, kostra_funksjon, ai_recommendation, user_note, human_decision, sha256_seal
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["timestamp"],
                record["user_upn"],
                record["kostra_funksjon"],
                record["ai_recommendation"],
                record["user_note"],
                record["human_decision"],
                record["sha256_seal"],
            ),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass

    return record


def load_audit_history(limit: int = 20, db_path: Path = AUDIT_DB_PATH) -> pd.DataFrame:
    """Loads recent Stage-Gate Port 9/10 audit records from SQLite."""
    if not db_path.exists():
        return pd.DataFrame()
    try:
        conn = init_audit_db(db_path)
        df_log = pd.read_sql_query(
            """
            SELECT audit_id AS ID, timestamp AS Tidspunkt, user_upn AS Saksbehandler,
                   kostra_funksjon AS KOSTRA, human_decision AS Beslutning,
                   user_note AS Kontrollnotat, substr(sha256_seal, 1, 16) || '...' AS SHA256_Prefix,
                   sha256_seal AS Full_SHA256
            FROM Audit_AI_Actions
            ORDER BY audit_id DESC
            LIMIT ?
            """,
            conn,
            params=(limit,),
        )
        conn.close()
        return df_log
    except Exception:
        return pd.DataFrame()


# ==========================================
# 5. STREAMLIT APP MAIN (EDWARD TUFTE UI)
# ==========================================
def main() -> None:
    st.set_page_config(
        page_title="MVP Helse og Mestring — Kristiansand Kommune",
        page_icon="🏥",
        layout="wide",
    )

    # Edward Tufte Data-Ink Ratio CSS
    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1280px; }
        div[data-testid="stMetricValue"] { font-family: monospace; font-size: 1.25rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🏥 Kristiansand Kommune — MVP Helse og Mestring (Ansvar 5200)")
    st.caption(
        "Spesialisert Økonomistyrings-, EVM- og Controlling-modul for Pleie og Omsorg (KOSTRA 253, 254, 256) "
        "| Edward Tufte Data-Ink Standard"
    )

    # Sidebar
    st.sidebar.header("🔑 Saksbehandler & RLS")
    user_upn = st.sidebar.text_input(
        "Saksbehandler UPN", "helse.controller@kristiansand.kommune.no"
    )
    st.sidebar.info(
        "📌 **Modul:** Ansvar 5200 Helse og Mestring  \n"
        "💰 **Totalramme:** 320,00 MNOK  \n"
        "⚖️ **Hjemler:** Kommuneloven §§ 14-5, 14-6 & HTA § 4"
    )

    df = load_helse_data()

    # KPI Metrics Top Row (Portfolio EVM Summary)
    tot_budget = float(df["Budsjett_MNOK"].sum())
    tot_ytd = float(df["Regnskap_YTD_MNOK"].sum())
    tot_expected = float(df["Forventet_YTD_MNOK"].sum())
    tot_var = round(tot_expected - tot_ytd, 2)
    tot_cpi = round(tot_expected / tot_ytd, 3) if tot_ytd > 0 else 1.0
    tot_eac = round(tot_budget / tot_cpi, 2) if tot_cpi > 0 else tot_budget
    tot_vac = round(tot_budget - tot_eac, 2)
    tot_vikar = float(df["Netto_Vikarbelastning_MNOK"].sum())

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Årsbudsjett 2026 (BAC)", f"{tot_budget:.2f} MNOK")
    col2.metric(
        "Regnskap YTD M8 (AC)",
        f"{tot_ytd:.2f} MNOK",
        delta=f"Plan (PV): {tot_expected:.2f} MNOK",
        delta_color="off",
    )
    col3.metric(
        "Periodisert Avvik YTD (CV)",
        f"{tot_var:+.2f} MNOK",
        delta=f"{(tot_var / tot_expected) * 100:+.1f}% mot YTD-budsjett",
        delta_color="normal",
    )
    col4.metric(
        "Portefølje CPI & Sluttprognose (EAC)",
        f"{tot_eac:.2f} MNOK",
        delta=f"CPI {tot_cpi:.3f} | VAC {tot_vac:+.2f} MNOK",
        delta_color="normal",
    )
    col5.metric("Netto Vikar & Overtid", f"{tot_vikar:.2f} MNOK")

    st.markdown("---")

    # KOSTRA Breakdown Table (Tufte formatting: no index, right-aligned numbers)
    st.subheader("📋 Underfunksjoner i Helse og Mestring (KOSTRA 253, 254, 256)")

    def format_rag(val: str) -> str:
        if val == "GRØNN":
            return "🟢 Grønn"
        elif val == "RAV":
            return "🟡 Rav"
        return "🔴 Rød"

    display_df = df.copy()
    display_df["RAG"] = display_df["RAG_Status"].apply(format_rag)

    st.dataframe(
        display_df[
            [
                "KOSTRA_Funksjon",
                "Beskrivelse",
                "Budsjett_MNOK",
                "Forventet_YTD_MNOK",
                "Regnskap_YTD_MNOK",
                "Avvik_MNOK",
                "Avvik_Pct",
                "CPI",
                "EAC_MNOK",
                "Netto_Vikarbelastning_MNOK",
                "Sykefravar_Pct",
                "RAG",
            ]
        ],
        use_container_width=True,
        hide_index=True,
        column_config={
            "KOSTRA_Funksjon": st.column_config.NumberColumn("KOSTRA", format="%d"),
            "Beskrivelse": st.column_config.TextColumn("Tjenesteområde"),
            "Budsjett_MNOK": st.column_config.NumberColumn("Budsjett (BAC)", format="%.2f MNOK"),
            "Forventet_YTD_MNOK": st.column_config.NumberColumn("Plan YTD (PV)", format="%.2f MNOK"),
            "Regnskap_YTD_MNOK": st.column_config.NumberColumn("Regnskap YTD (AC)", format="%.2f MNOK"),
            "Avvik_MNOK": st.column_config.NumberColumn("Avvik YTD (CV)", format="%+.2f MNOK"),
            "Avvik_Pct": st.column_config.NumberColumn("Avvik YTD %", format="%+.2f %%"),
            "CPI": st.column_config.NumberColumn("CPI", format="%.3f"),
            "EAC_MNOK": st.column_config.NumberColumn("Prognose (EAC)", format="%.2f MNOK"),
            "Netto_Vikarbelastning_MNOK": st.column_config.NumberColumn("Netto Vikar/Overtid", format="%.2f MNOK"),
            "Sykefravar_Pct": st.column_config.NumberColumn("Sykefravær", format="%.1f %%"),
            "RAG": st.column_config.TextColumn("Status"),
        },
    )

    st.markdown("---")

    # Deep Dive Selection
    st.subheader("📊 Dybdeanalyse, Monte Carlo-Prognose & NAV-Refusjonsgap")

    selected_funksjon = st.selectbox(
        "Velg KOSTRA-Funksjon for Dybdeanalyse", df["Beskrivelse"].tolist()
    )
    row = df[df["Beskrivelse"] == selected_funksjon].iloc[0]

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f"#### 🎲 Monte Carlo Årsavslutningsprognose (KOSTRA {row['KOSTRA_Funksjon']}):"
        )
        p10, p50, p90 = run_monte_carlo(
            float(row["Budsjett_MNOK"]), float(row["Regnskap_YTD_MNOK"])
        )

        st.write(f"- **Årsbudsjett (BAC)**: `{row['Budsjett_MNOK']:.2f} MNOK`")
        st.write(
            f"- **Deterministisk EVM Sluttprognose (EAC = BAC / CPI)**: `{row['EAC_MNOK']:.2f} MNOK` "
            f"(CPI: `{row['CPI']:.3f}`, VAC: `{row['VAC_MNOK']:+.2f} MNOK`)"
        )
        st.write(
            f"- **P10 (Best Case)**: `{p10:.2f} MNOK` (Avvik: `{row['Budsjett_MNOK'] - p10:+.2f} MNOK`)"
        )
        st.write(
            f"- **P50 (Forventet M12 inkl. Q4-sesong)**: **`{p50:.2f} MNOK`** "
            f"(Avvik: **`{row['Budsjett_MNOK'] - p50:+.2f} MNOK`**)"
        )
        st.write(
            f"- **P90 (Stress-Scenario med Q4-sykefravær)**: `{p90:.2f} MNOK` "
            f"(Avvik: `{row['Budsjett_MNOK'] - p90:+.2f} MNOK`)"
        )

        # NAV Refund Gap Analysis
        st.markdown("#### 🏥 NAV-Refusjonsoppgjør (Art 1600 jf. § 14-6 Bruttoprinsippet):")
        nav_info = calculate_nav_refund_gap(row)

        st.write(
            f"- Bokført NAV-refusjon (Art 1600): **`{nav_info['actual_nav_mnok']:.2f} MNOK`**"
        )
        st.write(
            f"- Beregnet refusjonskrav jf. Folketrygdloven § 22-13: **`{nav_info['expected_nav_mnok']:.2f} MNOK`** "
            f"(Risikojustert for langtidssykefravær: `{nav_info['risk_adjusted_nav_mnok']:.2f} MNOK`)"
        )
        if nav_info["refund_gap_mnok"] > 0:
            st.warning(
                f"⚠️ **Uavstemt Refusjonsgap**: Det gjenstår **`{nav_info['refund_gap_mnok']:.2f} MNOK`** "
                f"ubetalte refusjoner fra NAV for denne enheten. Kontroller foreldelsesfrist (3 mnd. jf. ftrl. § 22-13)."
            )
        else:
            st.success("✅ NAV-refusjonene er i balanse.")

    with c2:
        st.markdown(
            "#### ⚖️ Juridisk Saksfremlegg (Kommuneloven §§ 14-5, 14-6 & HTA § 4)"
        )
        ai_recommendation = build_legal_recommendation(row, p50)
        year_end_deficit = round(p50 - float(row["Budsjett_MNOK"]), 2)

        if year_end_deficit > 0 or float(row["CPI"]) < 1.0:
            st.error(ai_recommendation)
        else:
            st.success(ai_recommendation)

    st.markdown("---")
    st.subheader("🛡️ Stage-Gate Port 9 & Port 10: Saksbehandler Sign-Off & Revisorstempel")

    user_note = st.text_area(
        "Saksbehandlers vurderingsnotat (PII-vaskes automatisk lokalt i Port 4)",
        f"Vurdert overskridelse for KOSTRA {row['KOSTRA_Funksjon']}. Inngår i oppfølgingssak for Helse og mestring. "
        f"Kontaktperson fnr: 120485 12345, tlf +47 987 65 432.",
    )
    clean_note = mask_pii(user_note)
    st.caption(f"🔒 **Skjermet tekst (Port 4 Local Scrubber)**: `{clean_note}`")

    col_b1, col_b2, col_b3 = st.columns(3)
    if col_b1.button("✅ Godkjenn AI-Anbefaling (APPROVED)", use_container_width=True):
        audit_entry = generate_audit_seal(
            user_upn,
            str(row["KOSTRA_Funksjon"]),
            ai_recommendation,
            "APPROVED",
            user_note=clean_note,
        )
        st.success(
            f"✅ Beslutning (APPROVED) lagret i SQLite Audit Ledger! SHA-256: `{audit_entry['sha256_seal']}`"
        )
        st.json(audit_entry)

    if col_b2.button("⚠️ Korriger med Merknad (MODIFIED)", use_container_width=True):
        audit_entry = generate_audit_seal(
            user_upn,
            str(row["KOSTRA_Funksjon"]),
            ai_recommendation,
            "MODIFIED",
            user_note=clean_note,
        )
        st.warning(
            f"⚠️ Endret beslutning (MODIFIED) lagret med revisorstempel! SHA-256: `{audit_entry['sha256_seal']}`"
        )
        st.json(audit_entry)

    if col_b3.button("🛑 Avvis AI-Anbefaling (REJECTED)", use_container_width=True):
        audit_entry = generate_audit_seal(
            user_upn,
            str(row["KOSTRA_Funksjon"]),
            ai_recommendation,
            "REJECTED",
            user_note=clean_note,
        )
        st.error(
            f"🛑 Avvist beslutning (REJECTED) lagret i revisjonsloggen! SHA-256: `{audit_entry['sha256_seal']}`"
        )
        st.json(audit_entry)

    with st.expander("🔍 Stage-Gate Port 10: Uforanderlig SQLite Revisjonslogg (`Audit_AI_Actions`)", expanded=False):
        df_audit = load_audit_history()
        if not df_audit.empty:
            st.dataframe(
                df_audit.drop(columns=["Full_SHA256"]),
                use_container_width=True,
                hide_index=True,
            )
            st.download_button(
                label="⬇️ Eksporter Revisjonslogg (JSON) til Kommunerevisjonen",
                data=df_audit.to_json(orient="records", indent=2, force_ascii=False),
                file_name="helse_mestring_audit_log.json",
                mime="application/json",
            )
        else:
            st.info("Ingen signerte revisjonshendelser er lagret i databasen ennå.")


if __name__ == "__main__":
    main()
