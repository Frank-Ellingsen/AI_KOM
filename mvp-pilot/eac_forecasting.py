#!/usr/bin/env python3
"""
Predictive AI & Project Controlling: EAC / ETC Forecasting Engine
Replaces the naive 50% trend rule with driver-based, statistical EAC models.
"""

from pathlib import Path
import duckdb
import pandas as pd

try:
    from config import DB_DUCKDB
except ImportError:
    from mvp_pilot.config import DB_DUCKDB


def compute_eac_forecasts(db_path: Path = DB_DUCKDB, season_weights: dict = None) -> dict:
    """
    Beregner Estimate at Completion (EAC) og Estimate to Complete (ETC)
    basert på faktiske drivere i KOSTRA-kontoplanen.
    """
    con = duckdb.connect(str(db_path), read_only=True)

    # Standard sesongvekter for T3 (kan overstyres)
    weights = {
        "overtid": 1.15,       # Art 1040
        "vikarer": 1.10,       # Art 1020, 1030, 1050, 1270 (vikarbyrå)
        "refusjoner": 1.25     # Art 1710, 1700, 1770 (NAV-sykepenger / motposter)
    }
    if season_weights:
        weights.update(season_weights)

    # 1. Grunnlagstall YTD og gjenstående budsjett
    summary = con.execute("""
        SELECT 
            SUM(CASE WHEN Status = 'Bokført' THEN Budsjett ELSE 0 END) AS budsjett_ytd,
            SUM(CASE WHEN Status = 'Bokført' THEN Regnskap ELSE 0 END) AS regnskap_ytd,
            SUM(CASE WHEN Status = 'Bokført' THEN Merforbruk ELSE 0 END) AS merforbruk_ytd,
            SUM(CASE WHEN Status != 'Bokført' THEN Budsjett ELSE 0 END) AS budsjett_rest,
            SUM(Budsjett) AS arsbudsjett
        FROM fact_bomiljo;
    """).df().to_dict(orient="records")[0]

    actual_ytd = summary["regnskap_ytd"]
    budget_rest = summary["budsjett_rest"]
    ytd_variance = summary["budsjett_ytd"] - summary["regnskap_ytd"]
    annual_budget = summary["arsbudsjett"]

    # 2. Modell 1: Excel Sjablong (50% av YTD merforbruk)
    trend_share = 0.50
    overrun_ytd = max(-ytd_variance, 0)
    eac_sjablong = actual_ytd + budget_rest + (overrun_ytd * trend_share)
    var_sjablong = annual_budget - eac_sjablong

    # 3. Modell 2: Lineær Run-rate (8 måneder skalert til 12 måneder)
    eac_run_rate = (actual_ytd / 8.0) * 12.0
    var_run_rate = annual_budget - eac_run_rate

    # 4. Modell 3: Driver-basert KOSTRA EAC (Analyse pr art)
    # Lønn, overtid, vikarer og refusjoner har ulik dynamikk i T3
    drivers_df = con.execute("""
        SELECT 
            Undergruppe,
            KOSTRA_Art,
            Kontonavn,
            SUM(Budsjett) AS Budsjett_YTD,
            SUM(Regnskap) AS Regnskap_YTD,
            SUM(Merforbruk) AS Merforbruk_YTD,
            AVG(Regnskap) AS Mnd_Snitt
        FROM fact_bomiljo
        WHERE Status = 'Bokført'
        GROUP BY Undergruppe, KOSTRA_Art, Kontonavn
        ORDER BY Merforbruk_YTD DESC;
    """).df()

    # Beregn sesongkorrigert ETC for gjenstående 4 måneder (Sept-Des)
    # Sesongeffekter i pleie og omsorg:
    # - Overtid (1040) øker i nov/des (+15%)
    # - Vikarer og innleie (1020, 1030, 1270) øker i nov/des (+10%)
    # - Refusjoner (1710 NAV) har 2-3 mnd etterslep som forventes bokført mot slutten av året (1.25x fradrag)
    etc_driver_based = 0.0
    drift_detaljer = []

    for _, row in drivers_df.iterrows():
        art = str(row["KOSTRA_Art"])
        snitt_mnd = row["Mnd_Snitt"]
        merforbruk = row["Merforbruk_YTD"]

        # Sesongjusteringsfaktor for høsttertialet (4 måneder)
        if art in ["1040"]:
            multiplier = weights["overtid"]
        elif art in ["1020", "1030", "1050", "1051", "1270"]:
            multiplier = weights["vikarer"]
        elif art in ["1700", "1710", "1729", "1770"]:
            multiplier = weights["refusjoner"]
        else:
            multiplier = 1.00

        projected_4m = snitt_mnd * 4.0 * multiplier
        etc_driver_based += projected_4m

        if abs(merforbruk) > 20000:
            drift_detaljer.append({
                "art": art,
                "navn": row["Kontonavn"],
                "ytd_merforbruk": merforbruk,
                "mnd_snitt": snitt_mnd,
                "estimert_t3": projected_4m
            })

    eac_driver_based = actual_ytd + etc_driver_based
    var_driver_based = annual_budget - eac_driver_based

    # Beregn konfidensintervall (P10, P50, P90)
    p10 = min(eac_sjablong, eac_run_rate, eac_driver_based) * 0.985
    p50 = eac_driver_based
    p90 = max(eac_sjablong, eac_run_rate, eac_driver_based) * 1.015

    con.close()

    return {
        "actual_ytd": actual_ytd,
        "budget_rest": budget_rest,
        "annual_budget": annual_budget,
        "ytd_variance": ytd_variance,
        "models": {
            "sjablong_50pct": {
                "name": "Excel Sjablong (50 % trend)",
                "eac": eac_sjablong,
                "variance": var_sjablong,
                "variance_pct": (var_sjablong / annual_budget) * 100
            },
            "run_rate": {
                "name": "Lineær Run-rate (YTD x 12/8)",
                "eac": eac_run_rate,
                "variance": var_run_rate,
                "variance_pct": (var_run_rate / annual_budget) * 100
            },
            "driver_based_ai": {
                "name": "Driver-basert KOSTRA EAC (AI / Sesongjustert)",
                "eac": eac_driver_based,
                "variance": var_driver_based,
                "variance_pct": (var_driver_based / annual_budget) * 100
            }
        },
        "confidence_interval": {
            "p10": p10,
            "p50": p50,
            "p90": p90
        },
        "top_drivers": drift_detaljer[:8]
    }


if __name__ == "__main__":
    forecasts = compute_eac_forecasts()
    print("=" * 65)
    print("PREDIKTIV EAC / ETC ANALYSE (PROSJEKTCONTROLLING)")
    print("=" * 65)
    print(f"Årsbudsjett (BAC):      {forecasts['annual_budget']:14,.2f} kr")
    print(f"Bokført YTD (ACWP):      {forecasts['actual_ytd']:14,.2f} kr")
    print(f"Bokført avvik YTD:       {forecasts['ytd_variance']:14,.2f} kr")
    print("-" * 65)
    for key, mod in forecasts["models"].items():
        print(f"{mod['name']:<42} EAC: {mod['eac']:12,.2f} kr | Avvik: {mod['variance']:10,.2f} kr ({mod['variance_pct']:.1f} %)")
    print("-" * 65)
    print(f"Konfidensintervall (P10-P50-P90): {forecasts['confidence_interval']['p10']:,.0f} -> {forecasts['confidence_interval']['p50']:,.0f} -> {forecasts['confidence_interval']['p90']:,.0f} kr")
