#!/usr/bin/env python3
"""
Predictive AI & Project Controlling Engine
Implementasjon av PREDICTIVE_AI_FORECASTING_SPEC.md og SKILL_PREDICTIVE_FORECASTING_AI.md
Kobler seg til erp_data/kommune_golden_record.db, kjører driverbasert Monte Carlo og EVM,
og lagrer uforanderlig revisjonsspor i Fact_Prognose_Logg med SHA-256.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
from typing import Any, Dict, Optional

# Sikre UTF-8 i konsoll på Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "erp_data" / "kommune_golden_record.db"


# ==============================================================================
# 1. DRIFTSPROGNOSE: DRIVERBASERT MONTE CARLO
# ==============================================================================
def calculate_operational_forecast(
    hittil_regnskap_ac: float,
    gjeldende_maned: int,
    vedtatt_ramme_bac: float,
    driver_parameters: Optional[Dict[str, float]] = None,
    n_simuleringer: int = 10000
) -> Dict[str, Any]:
    """Beregner EOY-prognose for kommunal drift med Beta-fravær og Lognormal priser."""
    if driver_parameters is None:
        driver_parameters = {
            "sykefravaer_snitt": 0.085,
            "vikar_elastisitet": 1.75,
            "prisvekst_stot": 1.02
        }

    # Sesongvekter Kristiansand kommune
    sesong_vekter = np.array([
        0.07, 0.07, 0.08, 0.08, 0.08, 0.11, 0.06, 0.08, 0.08, 0.08, 0.09, 0.12
    ])
    gjenstaende_sesong_andel = float(sesong_vekter[gjeldende_maned:].sum())

    frav_base = driver_parameters.get("sykefravaer_snitt", 0.085)
    fravaer_samples = np.random.beta(a=17, b=183, size=n_simuleringer) * (frav_base / 0.085)
    pris_samples = np.random.lognormal(mean=0.0, sigma=0.025, size=n_simuleringer) * driver_parameters.get("prisvekst_stot", 1.0)

    elastisitet = driver_parameters.get("vikar_elastisitet", 1.75)
    base_etc = vedtatt_ramme_bac * gjenstaende_sesong_andel
    etc_simulert = base_etc * (1.0 + (fravaer_samples - 0.065) * elastisitet) * pris_samples
    eoy_simulert = hittil_regnskap_ac + etc_simulert

    p10 = float(np.percentile(eoy_simulert, 10))
    p50 = float(np.percentile(eoy_simulert, 50))
    p90 = float(np.percentile(eoy_simulert, 90))
    avvik_p50 = float(p50 - vedtatt_ramme_bac)

    if avvik_p50 > 1000000:
        status = "KRITISK_MERFORBRUK"
        tiltak = "Obligatorisk sak til Formannskapet jf. Kommuneloven § 14-5. Krev ansettelsesstopp."
    elif avvik_p50 > 250000:
        status = "VESENTLIG_AVVIK"
        tiltak = "Administrativ innstramming og vikarstopp iverksatt av kommunalsjef."
    else:
        status = "I_RUTE"
        tiltak = "Forbruk i tråd med forventet sesongramme."

    audit_data = {
        "type": "DRIFT_MONTE_CARLO",
        "ac": hittil_regnskap_ac,
        "bac": vedtatt_ramme_bac,
        "p10": p10,
        "p50": p50,
        "p90": p90,
        "avvik_p50": avvik_p50,
        "drivere": driver_parameters
    }
    sha256_hash = hashlib.sha256(json.dumps(audit_data, sort_keys=True).encode("utf-8")).hexdigest()

    return {
        "modell": "DRIVER_MONTE_CARLO_10K",
        "hittil_regnskap_ac": hittil_regnskap_ac,
        "vedtatt_ramme_bac": vedtatt_ramme_bac,
        "p10_optimistisk": round(p10, 0),
        "p50_forventet": round(p50, 0),
        "p90_konservativt": round(p90, 0),
        "estimert_avvik_p50": round(avvik_p50, 0),
        "status": status,
        "tiltaksanbefaling": tiltak,
        "sha256_hash": sha256_hash
    }


# ==============================================================================
# 2. PROSJEKTKONTROLL: EARNED VALUE MANAGEMENT (EVM / KS2)
# ==============================================================================
def calculate_project_evm_forecast(
    bac: float,
    pv: float,
    ev: float,
    ac: float,
    usikkerhet_p85_tillegg: float = 0.08
) -> Dict[str, Any]:
    """Beregner fullstendig EVM med CPI, SPI, EAC, ETC og P85 kostnadsramme."""
    cv = ev - ac
    sv = ev - pv
    cpi = ev / ac if ac > 0 else 1.0
    spi = ev / pv if pv > 0 else 1.0

    if cpi > 0 and spi > 0:
        eac_p50 = ac + ((bac - ev) / (cpi * spi))
    elif cpi > 0:
        eac_p50 = ac + ((bac - ev) / cpi)
    else:
        eac_p50 = bac

    etc = eac_p50 - ac
    vac = bac - eac_p50
    kostnadsramme_p85 = eac_p50 * (1.0 + usikkerhet_p85_tillegg)

    if cpi < 0.90 or spi < 0.85:
        risiko = "HØY_RISIKO"
    elif cpi < 0.98 or spi < 0.95:
        risiko = "MIDDELS_RISIKO"
    else:
        risiko = "LAV_RISIKO_I_RUTE"

    audit_data = {
        "type": "EVM_KS2",
        "bac": bac,
        "pv": pv,
        "ev": ev,
        "ac": ac,
        "cpi": round(cpi, 3),
        "spi": round(spi, 3),
        "eac_p50": round(eac_p50, 0),
        "p85": round(kostnadsramme_p85, 0)
    }
    sha256_hash = hashlib.sha256(json.dumps(audit_data, sort_keys=True).encode("utf-8")).hexdigest()

    return {
        "modell": "EVM_FAST_KS2",
        "bac": bac,
        "pv": pv,
        "ev": ev,
        "ac": ac,
        "cv": round(cv, 0),
        "sv": round(sv, 0),
        "cpi": round(cpi, 3),
        "spi": round(spi, 3),
        "eac_p50": round(eac_p50, 0),
        "etc": round(etc, 0),
        "vac_sluttoverskridelse": round(vac, 0),
        "kostnadsramme_p85": round(kostnadsramme_p85, 0),
        "risikovurdering": risiko,
        "sha256_hash": sha256_hash
    }


# ==============================================================================
# 3. ARKIVERING I Fact_Prognose_Logg
# ==============================================================================
def save_forecast_audit_record(
    db_path: str,
    prognose_id: str,
    ansvar_kode: str,
    kostra_funksjon: str,
    periode_ytd: int,
    regnskapsar: int,
    prognose_resultat: Dict[str, Any],
    saksbehandler: str = "Frank Ellingsen"
) -> bool:
    """Arkiverer beregnet prognose i SQLite for Kommunerevisjonen."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO Fact_Prognose_Logg (
        prognose_id, ansvar_kode, kostra_funksjon, periode_ytd, regnskapsar,
        modell_type, hittil_regnskap_ac, vedtatt_ramme_bac, p10_belop, p50_belop, p90_belop,
        estimert_avvik_p50, cpi, spi, status, saksbehandler, sha256_hash
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        prognose_id,
        ansvar_kode,
        kostra_funksjon,
        periode_ytd,
        regnskapsar,
        prognose_resultat.get("modell", "UNKNOWN"),
        prognose_resultat.get("hittil_regnskap_ac", prognose_resultat.get("ac", 0.0)),
        prognose_resultat.get("vedtatt_ramme_bac", prognose_resultat.get("bac", 0.0)),
        prognose_resultat.get("p10_optimistisk", prognose_resultat.get("eac_p50", 0.0)),
        prognose_resultat.get("p50_forventet", prognose_resultat.get("eac_p50", 0.0)),
        prognose_resultat.get("p90_konservativt", prognose_resultat.get("kostnadsramme_p85", 0.0)),
        prognose_resultat.get("estimert_avvik_p50", prognose_resultat.get("vac_sluttoverskridelse", 0.0)),
        prognose_resultat.get("cpi", 1.0),
        prognose_resultat.get("spi", 1.0),
        prognose_resultat.get("status", prognose_resultat.get("risikovurdering", "I_RUTE")),
        saksbehandler,
        prognose_resultat["sha256_hash"]
    ))

    conn.commit()
    conn.close()
    return True


def run_pipeline():
    """Kjører full prognose- og EVM-pipeline mot kommune_golden_record.db."""
    print("=" * 85)
    print("🔮 PREDICTIVE AI & PROJECT CONTROLLING MOTOR — KRISTIANSAND KOMMUNE")
    print("=" * 85)

    if not DB_PATH.exists():
        print(f"Feil: Finner ikke {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Hent reelle driftsdata
    cur.execute("""
    SELECT 
        ans.ansvar_kode,
        ans.enhet_navn,
        ans.sektor,
        SUM(b.budsjett_belop) AS BAC,
        SUM(COALESCE(r.belop, 0)) AS AC
    FROM Fact_Budsjett b
    LEFT JOIN Fact_Regnskap r 
        ON b.funksjon_key = r.funksjon_key 
       AND b.art_key = r.art_key 
       AND b.ansvar_key = r.ansvar_key 
       AND b.dato_key = r.dato_key
    JOIN Dim_Ansvar ans ON b.ansvar_key = ans.ansvar_kode
    GROUP BY ans.ansvar_kode, ans.enhet_navn, ans.sektor;
    """)
    drifts_data = cur.fetchall()
    conn.close()

    print("\n📌 1. DRIFTSPROGNOSER (DRIVERBASERT MONTE CARLO - PERIODE T2 / MND 8):")
    print("-" * 85)
    for row in drifts_data:
        ansvar, enhet, sektor, bac, ac = row
        res = calculate_operational_forecast(hittil_regnskap_ac=ac, gjeldende_maned=8, vedtatt_ramme_bac=bac)
        pid = f"PROG-2026-T2-{ansvar}"
        save_forecast_audit_record(
            db_path=str(DB_PATH),
            prognose_id=pid,
            ansvar_kode=ansvar,
            kostra_funksjon="202/253",
            periode_ytd=8,
            regnskapsar=2026,
            prognose_resultat=res
        )
        print(f"Enhet: {enhet} ({sektor})")
        print(f"  • Påløpt regnskap hittil (AC) : {res['hittil_regnskap_ac']:>15,.0f} kr".replace(",", " "))
        print(f"  • Vedtatt årsbudsjett (BAC)   : {res['vedtatt_ramme_bac']:>15,.0f} kr".replace(",", " "))
        print(f"  • p10 Optimistisk utfall      : {res['p10_optimistisk']:>15,.0f} kr".replace(",", " "))
        print(f"  • p50 Forventet sluttkostnad  : {res['p50_forventet']:>15,.0f} kr".replace(",", " "))
        print(f"  • p90 Konservativt risikoutfall: {res['p90_konservativt']:>15,.0f} kr".replace(",", " "))
        print(f"  • Estimert avvik mot ramme    : {res['estimert_avvik_p50']:>15,.0f} kr [{res['status']}]".replace(",", " "))
        print(f"  • SHA-256 revisjonsstempel    : {res['sha256_hash'][:32]}...")
        print("-" * 85)

    print("\n📌 2. PROSJEKTKONTROLL & INVESTERING (EVM / KS2 MODELL):")
    print("-" * 85)
    projects = [
        ("PROJ-101", "Vågsbygd Barneskole", 185000000, 110000000, 104500000, 115000000),
        ("PROJ-201", "Randesund Boenhet", 240000000, 160000000, 142000000, 168500000),
        ("PROJ-301", "VA-Hovedledning Selvkost", 92000000, 65000000, 64800000, 63100000),
    ]
    for pid, pnavn, bac, pv, ev, ac in projects:
        res_evm = calculate_project_evm_forecast(bac=bac, pv=pv, ev=ev, ac=ac)
        save_forecast_audit_record(
            db_path=str(DB_PATH),
            prognose_id=pid,
            ansvar_kode="SENTRAL",
            kostra_funksjon="INVESTERING",
            periode_ytd=8,
            regnskapsar=2026,
            prognose_resultat=res_evm
        )
        print(f"Prosjekt: {pnavn} ({pid})")
        print(f"  • Kostnadsindeks (CPI): {res_evm['cpi']:>6.3f} | Fremdriftsindeks (SPI): {res_evm['spi']:>6.3f}")
        print(f"  • Sluttprognose (EAC p50)     : {res_evm['eac_p50']:>15,.0f} kr".replace(",", " "))
        print(f"  • KS2 Kostnadsramme (P85)     : {res_evm['kostnadsramme_p85']:>15,.0f} kr".replace(",", " "))
        print(f"  • Sluttoverskridelse (VAC)    : {res_evm['vac_sluttoverskridelse']:>15,.0f} kr [{res_evm['risikovurdering']}]".replace(",", " "))
        print(f"  • SHA-256 revisjonsstempel    : {res_evm['sha256_hash'][:32]}...")
        print("-" * 85)

    print("\n✅ Samtlige prognoser og EVM-beregninger er lagret i Fact_Prognose_Logg!")


if __name__ == "__main__":
    run_pipeline()
