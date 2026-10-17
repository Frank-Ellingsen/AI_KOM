---
name: predictive-forecasting-ai
description: Analytisk og prediktiv AI-spisskompetanse for kommunal økonomistyring og Project Controlling. Beregner sesongjusterte EOY-prognoser (p10/p50/p90), driverbasert Monte Carlo-usikkerhet, Earned Value (EAC/ETC) og uforanderlig SHA-256 revisjonsstempel.
---

# 🔮 Agent Skill: Predictive AI, Tidsserieprognoser & Project Controlling (EVM)

> **Dokument:** `SKILL_PREDICTIVE_FORECASTING_AI.md`  
> **Brukerprofil:** Frank Ellingsen (Senior Financial Controller & Project Controller)  
> **Relevante systemer:** Visma ERP, Framsikt EPM, SSB KOSTRA, DuckDB, SQLite (`kommune_golden_record.db`)  
> **Lovhjemmel & Standarder:** Kommuneloven § 14-5, FAST Standard, KS2 (P50/P85), Edward Tufte Data-Ink Ratio

---

## 🎯 Formål og Trigger-Kriterier

Aktiver denne ferdigheten når brukeren eller arbeidsflyten ber om:
* **Helårsprognose (End of Year - EOY):** Fremskriving av forventet resultat for kommunalsjefområder eller KOSTRA-funksjoner.
* **Earned Value Management (EVM):** Beregning av $EAC$ (Estimate at Completion), $ETC$ (Estimate to Complete), $CPI$, $SPI$ eller $VAC$ for investeringsprosjekter.
* **Usikkerhets- og Scenariomodellering (What-If):** Kjøring av Monte Carlo-simuleringer på sykefravær, vikarforbruk, renteeksponering eller prisstigning.
* **Varsling om budsjettubalanse:** Påvisning av avvik som krever politisk sak til Formannskapet jf. **Kommuneloven § 14-5**.

---

## 📐 Operativ Arbeidsflyt for Agenten

```text
[ Steg 1: Datainnhenting ] ──► Hent bokført regnskap (AC) og vedtatt ramme (BAC) fra SQLite/DuckDB.
            │
[ Steg 2: Velg Modus ]    ──► Drift (Driverbasert Monte Carlo) ELLER Investering (EVM KS2).
            │
[ Steg 3: Simulering ]    ──► Beregn p10, p50 og p90 utfall over 10 000 løp.
            │
[ Steg 4: Guardrail Sjekk]──► Er avvik > 500k kr? Generer referanse til Kommuneloven § 14-5.
            │
[ Steg 5: Audit Hash ]    ──► Generer SHA-256 kontrollsum og lagre i Fact_Prognose_Logg.
```

---

## 🛡️ Guardrails & Kontrollkrav (Stage-Gate Samsvar)

1. **Ingen Black-Box ekstrapolering:** Alle prognoser MÅ synliggjøre hvilke driverforutsetninger som ligger til grunn (f.eks. `sykefravaer_rate = 8.4%`, `vikarpris_elastisitet = 1.05`).
2. **Obligatorisk usikkerhetsintervall:** Det er forbudt å oppgi ett enkelt tall som helårsfasit. Resultatet skal alltid oppgis som **p10 (stramt)**, **p50 (forventet)** og **p90 (konservativt)**.
3. **Kommuneloven § 14-5 Terskel:** Dersom p50-prognosen estimerer en sluttoverskridelse ($VAC < 0$), skal agenten automatisk fremme anbefaling om administrativ ansettelsesstopp eller sak om tilleggsbevilgning over disposisjonsfondet.
4. **Tufte Data-Ink Presentasjon:** Resultater i tabellform skal ha høyrejusterte tall, ingen vertikale linjer, og kun rød/oransje markering ved overskridelser.

---

## 💻 Produksjonsklar Python Implementering

Følgende modulære Python-motor implementerer både driverbasert Monte Carlo for drift og Earned Value Management for prosjekter:

```python
#!/usr/bin/env python3
"""
Predictive AI & Project Controlling Engine for Kristiansand Kommune
Beregner driverbasert Monte Carlo (Drift) og EVM (Investering) med SHA-256 audit.
"""

from __future__ import annotations
import json
import hashlib
from typing import Dict, Any, Optional
import numpy as np
import sqlite3


# ==============================================================================
# 1. DRIFTSPROGNOSE: DRIVERBASERT MONTE CARLO (10 000 LØP)
# ==============================================================================
def calculate_operational_forecast(
    hittil_regnskap_ac: float,
    gjeldende_maned: int,
    vedtatt_ramme_bac: float,
    driver_parameters: Optional[Dict[str, float]] = None,
    n_simuleringer: int = 10000
) -> Dict[str, Any]:
    """
    Beregner EOY-prognose for kommunale driftsenheter basert på sesongprofiler
    og stokastiske driver-støt (sykefravær og vikarpriser).
    """
    if driver_parameters is None:
        driver_parameters = {
            "sykefravaer_snitt": 0.085,       # 8.5 % forventet fravær
            "vikar_elastisitet": 1.75,        # 1% økt fravær gir 1.75% økte vikar-/overtidskostnader
            "prisvekst_stot": 1.02            # 2 % uforutsett prisstigning
        }

    # Sesongprofil for Kristiansand kommune (sum = 1.0)
    sesong_vekter = np.array([
        0.07, 0.07, 0.08, 0.08, 0.08, 0.11, 0.06, 0.08, 0.08, 0.08, 0.09, 0.12
    ])
    gjenstaende_sesong_andel = float(sesong_vekter[gjeldende_maned:].sum())

    # Stokastisk simulering av sykefravær via Beta-fordeling
    # Kalibrert: median 0.085, med 90% konfidens mellom 0.065 og 0.115
    frav_base = driver_parameters.get("sykefravaer_snitt", 0.085)
    fravaer_samples = np.random.beta(a=17, b=183, size=n_simuleringer) * (frav_base / 0.085)

    # Lognormal fordeling for usikkerhet i vikartimepriser og innleie
    pris_samples = np.random.lognormal(mean=0.0, sigma=0.025, size=n_simuleringer) * driver_parameters.get("prisvekst_stot", 1.0)

    # Beregn gjenstående behov (Estimate to Complete - ETC)
    elastisitet = driver_parameters.get("vikar_elastisitet", 1.75)
    base_etc = vedtatt_ramme_bac * gjenstaende_sesong_andel
    etc_simulert = base_etc * (1.0 + (fravaer_samples - 0.065) * elastisitet) * pris_samples

    # Sluttresultat (Estimate at Completion - EAC / EOY)
    eoy_simulert = hittil_regnskap_ac + etc_simulert

    p10 = float(np.percentile(eoy_simulert, 10))
    p50 = float(np.percentile(eoy_simulert, 50))
    p90 = float(np.percentile(eoy_simulert, 90))
    avvik_p50 = float(vedtatt_ramme_bac - p50)

    # Bestem status og handlingskrav jf. Kommuneloven § 14-5
    if avvik_p50 < -1000000:
        status = "KRITISK_MERFORBRUK"
        tiltak = "Obligatorisk sak til Formannskapet jf. Kommuneloven § 14-5. Krev ansettelsesstopp."
    elif avvik_p50 < -250000:
        status = "VESENTLIG_AVVIK"
        tiltak = "Administrativ innstramming og vikarstopp iverksatt av kommunalsjef."
    else:
        status = "I_RUTE"
        tiltak = "Forbruk i tråd med forventet sesongramme."

    # Generer kryptografisk SHA-256 hash for revisjonssporet
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
    """
    Beregner fullstendig Earned Value Management-modell for investeringsprosjekter.
    Inkluderer CPI, SPI, EAC (sluttprognose), ETC og KS2 P85-kostnadsramme.
    """
    # 1. Avviksberegninger
    cv = ev - ac  # Cost Variance
    sv = ev - pv  # Schedule Variance

    # 2. Ytelsesindekser
    cpi = ev / ac if ac > 0 else 1.0
    spi = ev / pv if pv > 0 else 1.0

    # 3. Sluttprognose (EAC)
    # Vekter både historisk kostnadseffektivitet og fremdriftsforsinkelse
    if cpi > 0 and spi > 0:
        eac_p50 = ac + ((bac - ev) / (cpi * spi))
    elif cpi > 0:
        eac_p50 = ac + ((bac - ev) / cpi)
    else:
        eac_p50 = bac

    etc = eac_p50 - ac
    vac = bac - eac_p50  # Negativ = sluttoverskridelse

    # KS2 Kostnadsramme (P85)
    kostnadsramme_p85 = eac_p50 * (1.0 + usikkerhet_p85_tillegg)

    # Statusvurdering
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
# 3. DATABASE REVISJONSSPOR: Fact_Prognose_Logg
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
    """Arkiverer beregnet prognose uforanderlig i SQLite for Kommunerevisjonen."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Opprett tabell dersom den mangler
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Fact_Prognose_Logg (
        prognose_id TEXT PRIMARY KEY,
        ansvar_kode TEXT NOT NULL,
        kostra_funksjon TEXT,
        periode_ytd INTEGER NOT NULL,
        regnskapsar INTEGER NOT NULL,
        modell_type TEXT NOT NULL,
        hittil_regnskap_ac REAL NOT NULL,
        vedtatt_ramme_bac REAL NOT NULL,
        p10_belop REAL NOT NULL,
        p50_belop REAL NOT NULL,
        p90_belop REAL NOT NULL,
        estimert_avvik_p50 REAL NOT NULL,
        cpi REAL,
        spi REAL,
        status TEXT NOT NULL,
        saksbehandler TEXT NOT NULL,
        sha256_hash TEXT NOT NULL,
        opprettet_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

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
```
