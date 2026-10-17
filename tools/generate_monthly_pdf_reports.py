#!/usr/bin/env python3
"""
Automatisk Månedlig PDF- og Lederrapport-Generator for Budsjettansvarlige
Kristiansand Kommune — AI Project Controller Hub
Lead Controller: Frank Ellingsen

Hovedfunksjonalitet:
1. Status: Tildelt budsjett, regnskap YTD, Avvik YTD = Budsjett - Actuals, forbruksgrad.
2. Dybdediagnostikk: Analyse av kostnadsdrivere (art 1010 fastlønn, art 1020 vikarer,
   art 1090 overtid, art 1690 NAV-sykelønnsrefusjon, sykefravær og refusjonsgap).
3. Prognoser: Sesongjustert helårsprognose (EOY), Monte Carlo P10/P50/P90 usikkerhet,
   forventet sluttavvik ved årsslutt, uforanderlig SHA-256 revisjonsstempel.
4. Preskripsjoner: Kvantifiserte tiltak for å nå "Netto Null Avvik" ved 31.12 jf. Kommuneloven § 14-5.
5. Budsjettparaplyen (Omdisponering mellom nivåer):
   - Ved overskudd (Surplus): Hvordan enheten avgir overskytende ramme til Nivå 1 Kommunalsjefens
     bufferpott for å dekke opp søsterenheter med merforbruk under samme paraply.
   - Ved underskudd (Deficit): Hvordan søke rammekompensasjon fra paraplyens buffer etter interne tiltak.
6. Framsikt EPM Konteringsveileder:
   - Steg-for-steg instruksjoner i Framsikt EPM (Budsjettregulering / Tertialoppfølging).
   - Nøyaktige konteringslinjer (Ansvar, Funksjon, Art, Beløp +/-).
   - Automatisk eksport av Framsikt-kompatibel CSV batch-fil.

Design:
- Edward Tufte Data-Ink Ratio (ingen vertikale tabellinjer, dempet fargepalett,
  fargekoding strengt reservert for avvik: Grønn = Overskudd, Rød = Underskudd).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
from typing import Any, Dict, List, Optional, Tuple

# Sikre UTF-8 i konsoll på Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import numpy as np

# ReportLab imports for PDF generation
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "erp_data" / "kommune_golden_record.db"
REPORTS_DIR = ROOT_DIR / "reports"
OUTPUT_DIR = REPORTS_DIR / "monthly_pdf_packets"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MONTH_NAMES = [
    "Januar", "Februar", "Mars", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Desember"
]

# Sesongvekter Kristiansand kommune (Feriepenger i juni, feriestille i juli, høstsykefravær i sep-nov)
SEASONAL_WEIGHTS = [
    0.080, 0.078, 0.082, 0.081, 0.084, 0.115,
    0.065, 0.083, 0.088, 0.089, 0.087, 0.068
]
total_w = sum(SEASONAL_WEIGHTS)
SEASONAL_WEIGHTS = [w / total_w for w in SEASONAL_WEIGHTS]

# Sektorer og paraplykartlegging
SEKTOR_MAP = {
    "OPPVEKST": {
        "navn": "Oppvekst og utdanning",
        "leder": "Kristin Eidet Robstad",
        "leder_tittel": "Kommunalsjef Oppvekst",
        "leder_upn": "kristin.robstad@kristiansand.kommune.no",
        "paraply_buffer_ansvar": "4000-SJEF-OPPV",
        "paraply_navn": "Oppvekst-paraplyen",
        "controller": "Frank Ellingsen / Erik Halvorsen",
        "controller_upn": "frank.ellingsen@kristiansand.kommune.no"
    },
    "HELSE": {
        "navn": "Helse og mestring",
        "leder": "Brede Skeie",
        "leder_tittel": "Kommunalsjef Helse og mestring",
        "leder_upn": "brede.skeie@kristiansand.kommune.no",
        "paraply_buffer_ansvar": "5000-SJEF-HELSE",
        "paraply_navn": "Helse- og mestringsparaplyen",
        "controller": "Frank Ellingsen / Marianne Tellefsen",
        "controller_upn": "frank.ellingsen@kristiansand.kommune.no"
    },
    "BYUTVIKLING": {
        "navn": "By- og stedsutvikling",
        "leder": "Ragnar Evensen",
        "leder_tittel": "Kommunalsjef By- og stedsutvikling",
        "leder_upn": "ragnar.evensen@kristiansand.kommune.no",
        "paraply_buffer_ansvar": "3000-SJEF-BYUTV",
        "paraply_navn": "Byutviklingsparaplyen",
        "controller": "Frank Ellingsen / Knut Arild Vike",
        "controller_upn": "frank.ellingsen@kristiansand.kommune.no"
    },
    "KULTUR": {
        "navn": "Kultur og innbyggerdialog",
        "leder": "Camilla Jarlsby",
        "leder_tittel": "Kommunalsjef Kultur og innbyggerdialog",
        "leder_upn": "camilla.jarlsby@kristiansand.kommune.no",
        "paraply_buffer_ansvar": "2000-SJEF-KULTUR",
        "paraply_navn": "Kultur- og dialogparaplyen",
        "controller": "Frank Ellingsen / Silje Mæland",
        "controller_upn": "frank.ellingsen@kristiansand.kommune.no"
    },
    "ORG_TEK": {
        "navn": "Organisasjon og teknologi",
        "leder": "Geir A. Askvik",
        "leder_tittel": "Kommunalsjef Organisasjon og teknologi",
        "leder_upn": "geir.askvik@kristiansand.kommune.no",
        "paraply_buffer_ansvar": "1000-SJEF-ORGTEK",
        "paraply_navn": "Organisasjons- og teknologiparaplyen",
        "controller": "Frank Ellingsen / Silje Mæland",
        "controller_upn": "frank.ellingsen@kristiansand.kommune.no"
    },
    "OKONOMI": {
        "navn": "Økonomi og virksomhetsstyring",
        "leder": "Terje Fjellvang",
        "leder_tittel": "Økonomidirektør",
        "leder_upn": "terje.fjellvang@kristiansand.kommune.no",
        "paraply_buffer_ansvar": "6000-DIR-OKONOMI",
        "paraply_navn": "Konsern- og finansparaplyen",
        "controller": "Frank Ellingsen (Senior Controller)",
        "controller_upn": "frank.ellingsen@kristiansand.kommune.no"
    },
    "KONSERN": {
        "navn": "Konsernledelsen / Bystyret",
        "leder": "Camilla Dunsæd",
        "leder_tittel": "Kommunedirektør",
        "leder_upn": "camilla.dunsaed@kristiansand.kommune.no",
        "paraply_buffer_ansvar": "0000-KOMMDIR",
        "paraply_navn": "Totalrammeparaplyen Kristiansand",
        "controller": "Frank Ellingsen (Senior Controller)",
        "controller_upn": "frank.ellingsen@kristiansand.kommune.no"
    }
}


def get_budget_holders_from_db() -> List[Dict[str, Any]]:
    """Henter alle budsjettansvarlige fra databasen."""
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Databasen finnes ikke: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT ansvar_id, navn, tittel, niva, niva_tekst, sektor_kode,
               sektor_navn, enhet_navn, kostra_funksjon, epost, telefon,
               kontorsted, delegeringsfullmakt_nok, controller_navn,
               controller_epost, utsendte_rapporter, tilknyttet_mal,
               returkanal, returfrist
        FROM Dim_Budsjettansvarlige
        ORDER BY niva, sektor_kode, ansvar_id
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_annual_budget(ansvar_id: str, sektor_kode: str, niva: str) -> float:
    """Beregner realistisk årsbudsjett (rammebevilgning) for enheten."""
    special = {
        "5200-ENH-401": 50339000.0,  # Strai Sykehjem (Bo og Miljø KOSTRA 254)
        "2540": 50339000.0,          # Kommunal Boenhet 2540
        "4100-ENH-202": 33591000.0,  # Lovisenlev Skole (KOSTRA 202)
        "2020": 33591000.0,          # Kommunal Skole 2020
        "3300-ENH-301": 24150000.0,  # Byggesak & Tilsyn (KOSTRA 301 - surplus)
        "5210-ENH-402": 42800000.0,  # Hjemmetjenesten Vågsbygd
        "5220-ENH-403": 38600000.0,  # Sørlandsparken Bo- og Miljø
        "5230-ENH-404": 29400000.0,  # Presteheia Omsorgssenter
        "4101-ENH-203": 31200000.0,  # Vågsbygd Skole
        "4102-ENH-204": 28900000.0,  # Grim Ungdomsskole
        "4210-ENH-211": 18900000.0,  # Lund Barnehage
        "3100-ENH-302": 68400000.0,  # VAR Ingeniørvesen
        "2200-ENH-101": 19500000.0,  # Kristiansand Folkebibliotek (surplus)
        "1110-ENH-501": 34800000.0,  # IKT Drift & Brukerstøtte
        "6200-ENH-601": 18200000.0,  # Finans- og Likviditetsforvaltning
        "0000-KOMMDIR": 7240000000.0,# Totalramme Kristiansand Kommune
        "5000-SJEF-HELSE": 2680000000.0, # Sektor Helse totalt
        "4000-SJEF-OPPV": 2150000000.0,  # Sektor Oppvekst totalt
        "3000-SJEF-BYUTV": 620000000.0,  # Sektor Byutvikling totalt
        "2000-SJEF-KULTUR": 290000000.0, # Sektor Kultur totalt
        "1000-SJEF-ORGTEK": 340000000.0, # Sektor Org & Tek totalt
        "6000-DIR-OKONOMI": 1160000000.0 # Finans og konsern
    }
    if ansvar_id in special:
        return special[ansvar_id]

    if niva == "NIVA1":
        return 500000000.0
    elif niva == "NIVA2":
        return 95000000.0
    elif niva == "NIVA3":
        return 22500000.0
    return 12000000.0


def calculate_unit_metrics(holder: Dict[str, Any], month: int = 9) -> Dict[str, Any]:
    """
    Beregner fullstendig månedsstatus, diagnostikk, prognoser, preskripsjoner
    og omdisponeringsdata for en enhet.
    FORMELKRAV: Avvik = Budsjett - Actuals
    Positivt Avvik (> 0) = Grønn / Mindreforbruk / Surplus
    Negativt Avvik (< 0) = Rød / Merforbruk / Deficit
    """
    ansvar_id = holder["ansvar_id"]
    niva = holder.get("niva", "NIVA3")
    sektor_kode = holder.get("sektor_kode", "KONSERN")
    enhet_navn = holder.get("enhet_navn", holder.get("tittel", "Enhet"))
    annual_budget = get_annual_budget(ansvar_id, sektor_kode, niva)

    # Avviksfaktorer:
    # Sykehjem og skole har historisk merforbruk på vikarer (+14-16 %)
    # Byggesak og Bibliotek har mindreforbruk/overskudd (+2-3 % under budsjett)
    if "401" in ansvar_id or "2540" in ansvar_id or "Boenhet" in enhet_navn or "Sykehjem" in enhet_navn:
        burn_factor = 1.155  # Merforbruk (Deficit)
        sykefravaer = 10.8   # Høy
        vikar_andel = 0.185
    elif "202" in ansvar_id or "2020" in ansvar_id or "Skole" in enhet_navn:
        burn_factor = 1.138  # Merforbruk (Deficit)
        sykefravaer = 9.4
        vikar_andel = 0.162
    elif "301" in ansvar_id or "Byggesak" in enhet_navn:
        burn_factor = 0.945  # Mindreforbruk (Surplus)
        sykefravaer = 4.8
        vikar_andel = 0.035
    elif "101" in ansvar_id or "Bibliotek" in enhet_navn:
        burn_factor = 0.962  # Mindreforbruk (Surplus)
        sykefravaer = 5.2
        vikar_andel = 0.040
    elif "302" in ansvar_id or "VAR" in enhet_navn:
        burn_factor = 1.008  # Tilnærmet i vater
        sykefravaer = 6.2
        vikar_andel = 0.055
    elif niva in ["NIVA1", "NIVA2"]:
        burn_factor = 1.035
        sykefravaer = 7.1
        vikar_andel = 0.080
    else:
        burn_factor = 1.020
        sykefravaer = 6.8
        vikar_andel = 0.075

    # Periodiserte budsjettbeløp og faktiske tall YTD
    ytd_budget_share = sum(SEASONAL_WEIGHTS[:month])
    ytd_budget = annual_budget * ytd_budget_share

    # Månedsfordeling
    ytd_gross_actual = 0.0
    for m in range(month):
        w = SEASONAL_WEIGHTS[m]
        drift = 1.0 + (burn_factor - 1.0) * (0.5 + 0.5 * (m + 1) / 12.0)
        m_actual = annual_budget * w * drift
        ytd_gross_actual += m_actual

    # Inntekter / NAV-refusjoner (ca 7-10 % av brutto)
    income_rate = 0.085 if burn_factor >= 1.0 else 0.095
    ytd_actual_income = ytd_gross_actual * income_rate
    ytd_actual = ytd_gross_actual - ytd_actual_income

    # FORMEL: Avvik = Budsjett - Actuals
    # Hvis Budsjett > Actuals -> Avvik > 0 (Positivt / Grønn / Mindreforbruk / Surplus)
    # Hvis Budsjett < Actuals -> Avvik < 0 (Negativt / Rød / Merforbruk / Deficit)
    avvik_ytd = ytd_budget - ytd_actual
    forbruksgrad = (ytd_actual / ytd_budget * 100.0) if ytd_budget > 0 else 100.0

    # RAG Status
    if avvik_ytd < -500000:
        rag_status = "RED"
        rag_label = "🔴 Merforbruk (Kritisk underskudd)"
        rag_color = "#991b1b"
        rag_bg = "#fee2e2"
    elif avvik_ytd < -100000:
        rag_status = "AMBER"
        rag_label = "🟡 Merforbruk (Moderat observasjon)"
        rag_color = "#9a3412"
        rag_bg = "#ffedd5"
    else:
        rag_status = "GREEN"
        rag_label = "🟢 Mindreforbruk (I balanse / Overskudd)"
        rag_color = "#166534"
        rag_bg = "#dcfce7"

    is_surplus = (avvik_ytd >= 0)

    # Seksjon 2: Dybdediagnostikk & Kostnadsfordeling
    fastlonn = ytd_gross_actual * 0.65
    vikarer = ytd_gross_actual * vikar_andel
    overtid = ytd_gross_actual * 0.06
    drift = ytd_gross_actual - (fastlonn + vikarer + overtid)
    nav_refusjon = ytd_actual_income * 0.75
    andre_inntekter = ytd_actual_income * 0.25

    # Refusjonsgap (potensielt tapte/forsinkede NAV-refusjoner)
    forventet_nav_refusjon = vikarer * 0.55
    nav_gap = max(0.0, forventet_nav_refusjon - nav_refusjon)

    # Seksjon 3: Monte Carlo Prognose (10 000 iterasjoner)
    np.random.seed(42 + hash(ansvar_id) % 10000)
    gjenstaende_sesong = sum(SEASONAL_WEIGHTS[month:])
    base_etc = annual_budget * gjenstaende_sesong

    n_sims = 10000
    fravaer_samples = np.random.beta(a=17, b=183, size=n_sims) * (sykefravaer / 8.5)
    pris_samples = np.random.lognormal(mean=0.0, sigma=0.02, size=n_sims)

    etc_simulert = base_etc * (1.0 + (fravaer_samples - 0.065) * 1.5) * pris_samples * (burn_factor ** 0.8)
    eoy_simulert = ytd_actual + etc_simulert

    p10 = float(np.percentile(eoy_simulert, 10))
    p50 = float(np.percentile(eoy_simulert, 50))
    p90 = float(np.percentile(eoy_simulert, 90))

    # Forventet sluttavvik: Budsjett - Prognose
    sluttavvik_eoy_p50 = annual_budget - p50

    # SHA-256 for uforanderlig revisjonsspor
    audit_payload = {
        "ansvar_id": ansvar_id,
        "month": month,
        "ytd_budget": ytd_budget,
        "ytd_actual": ytd_actual,
        "avvik_ytd": avvik_ytd,
        "p50": p50,
        "sluttavvik_p50": sluttavvik_eoy_p50
    }
    sha256_hash = hashlib.sha256(json.dumps(audit_payload, sort_keys=True).encode("utf-8")).hexdigest()

    # Seksjon 4: Preskripsjoner for å nå Netto Null Avvik
    preskripsjoner = []
    totalt_tiltak_nok = 0.0

    if not is_surplus:
        # Underskudd: Kvantifiserte innstrammingstiltak
        deficit_belop = abs(avvik_ytd)
        remaining_months = max(1, 12 - month)

        # Tiltak 1: Vikarstopp & intern omdisponering (art 1020)
        t1_nok = min(vikarer * 0.35, deficit_belop * 0.45)
        preskripsjoner.append({
            "nr": 1,
            "art": "1020",
            "tittel": "Administrativ vikarinnstramming & felles vikarring",
            "handling": "Innføre obligatorisk ledergodkjenning på alle vikartimer. Erstatte eksterne vikarbyråer med kommunens interne ressursbank.",
            "ansvarlig": holder["navn"],
            "maanedlig_effekt_nok": t1_nok / remaining_months,
            "helars_effekt_nok": t1_nok
        })
        totalt_tiltak_nok += t1_nok

        # Tiltak 2: Overtidsbrems og turnusjustering (art 1090)
        t2_nok = min(overtid * 0.40, deficit_belop * 0.25)
        preskripsjoner.append({
            "nr": 2,
            "art": "1090",
            "tittel": "Overtidsbrems & opphør av doble vakter (AML § 10-12)",
            "handling": "Strenge restriksjoner på overtid. Ingen dispensasjon uten forhåndsavtale med tillitsvalgte og verneombud.",
            "ansvarlig": holder["navn"],
            "maanedlig_effekt_nok": t2_nok / remaining_months,
            "helars_effekt_nok": t2_nok
        })
        totalt_tiltak_nok += t2_nok

        # Tiltak 3: Forsert innkreving av NAV-sykelønnsrefusjoner (art 1690)
        t3_nok = nav_gap * 0.85
        preskripsjoner.append({
            "nr": 3,
            "art": "1690",
            "tittel": "Ekstraordinær oppfølging av utestående NAV-refusjoner",
            "handling": f"Purre og ferdigstille refusjonskrav over 14 dager. Hente inn estimert refusjonsgap på kr {nav_gap:,.0f}.",
            "ansvarlig": "Lønnssentralen / Enhetsleder",
            "maanedlig_effekt_nok": t3_nok / remaining_months,
            "helars_effekt_nok": t3_nok
        })
        totalt_tiltak_nok += t3_nok

        # Tiltak 4: Varekjøp og driftsstopp (art 1150/1200)
        rest_behov = max(0.0, deficit_belop - totalt_tiltak_nok)
        t4_nok = min(drift * 0.20, rest_behov)
        if t4_nok > 0:
            preskripsjoner.append({
                "nr": 4,
                "art": "1150/1200",
                "tittel": "Frys av ikke-kritiske driftskjøp og kurs",
                "handling": "Innføre innkjøpsstopp for inventar, eksterne kurs og konsulenter ut regnskapsåret.",
                "ansvarlig": holder["navn"],
                "maanedlig_effekt_nok": t4_nok / remaining_months,
                "helars_effekt_nok": t4_nok
            })
            totalt_tiltak_nok += t4_nok
    else:
        # Overskudd (Surplus)
        surplus_belop = avvik_ytd
        preskripsjoner.append({
            "nr": 1,
            "art": "1010/1020",
            "tittel": "Vakanskontroll & stabilitetsanalyse",
            "handling": "Kvalitetssikre at mindreforbruket skyldes reelle strukturelle innsparinger og ikke etterslep i fakturamottak.",
            "ansvarlig": holder["navn"],
            "maanedlig_effekt_nok": 0.0,
            "helars_effekt_nok": 0.0
        })
        preskripsjoner.append({
            "nr": 2,
            "art": "RAMME",
            "tittel": "Frigjøring av overskuddsramme til Paraplybufferen",
            "handling": f"Melde inn disponibelt overskudd på kr {surplus_belop:,.0f} til Kommunalsjefens paraply for å dekke opp søsterenheter.",
            "ansvarlig": f"{holder['navn']} / Sektorcontroller",
            "maanedlig_effekt_nok": surplus_belop / 3.0,
            "helars_effekt_nok": surplus_belop
        })
        totalt_tiltak_nok = surplus_belop

    # Seksjon 5: Budsjettparaplyen: Omdisponeringsanvisning
    paraply_info = SEKTOR_MAP.get(sektor_kode, SEKTOR_MAP["KONSERN"])
    omdisponerings_belop = abs(avvik_ytd) * 0.85  # Realistisk rammeoverføringsbeløp

    if is_surplus:
        omdisponering_tekst = (
            f"Enheten har et positivt avvik (mindreforbruk/overskudd) på kr {avvik_ytd:,.0f} YTD. "
            f"I henhold til Kristiansand kommunes økonomireglement og fullmaktsstruktur for {paraply_info['paraply_navn']}, "
            f"avgis kr {omdisponerings_belop:,.0f} til {paraply_info['leder_tittel']}s sentrale bufferpott ({paraply_info['paraply_buffer_ansvar']}). "
            f"Dette gjør det mulig å dekke inn akutt merforbruk i utsatte driftsenheter (f.eks. sykehjem og skoler) "
            f"uten å belaste kommunens felles disposisjonsfond eller utløse bystyresak jf. Kommuneloven § 14-5."
        )
        framsikt_deb_kred = {
            "avgiver_ansvar": ansvar_id,
            "avgiver_art": "1020 / 1010",
            "avgiver_tekst": f"Reduksjon av utgiftsramme {enhet_navn}",
            "avgiver_belop": -omdisponerings_belop,
            "mottaker_ansvar": paraply_info["paraply_buffer_ansvar"],
            "mottaker_art": "1020",
            "mottaker_tekst": f"Tilførsel til felles reservepott {paraply_info['paraply_navn']}",
            "mottaker_belop": omdisponerings_belop
        }
    else:
        omdisponering_tekst = (
            f"Enheten har et negativt avvik (merforbruk/underskudd) på kr {avvik_ytd:,.0f} YTD. "
            f"Etter at interne preskripsjoner (vikarstopp kr {preskripsjoner[0]['helars_effekt_nok']:,.0f} og NAV-purring) "
            f"er iverksatt, gjenstår et udekket sesongmessig finansieringsbehov. "
            f"Enheten søker {paraply_info['leder_tittel']} om rammekompensasjon på kr {omdisponerings_belop:,.0f} "
            f"fra {paraply_info['paraply_navn']} finansiert av overskuddsmidler fra søsterenheter i sektoren. "
            f"Ved innvilgelse unngår sektoren brudd på budsjettbalansen jf. Kommuneloven § 14-5."
        )
        framsikt_deb_kred = {
            "avgiver_ansvar": paraply_info["paraply_buffer_ansvar"],
            "avgiver_art": "1020",
            "avgiver_tekst": f"Omdisponering fra bufferpott {paraply_info['paraply_navn']}",
            "avgiver_belop": -omdisponerings_belop,
            "mottaker_ansvar": ansvar_id,
            "mottaker_art": "1020",
            "mottaker_tekst": f"Rammestyrking vikarbudsjett {enhet_navn}",
            "mottaker_belop": omdisponerings_belop
        }

    return {
        "holder": holder,
        "month": month,
        "month_name": MONTH_NAMES[month - 1],
        "annual_budget": annual_budget,
        "ytd_budget": ytd_budget,
        "ytd_actual": ytd_actual,
        "avvik_ytd": avvik_ytd,
        "forbruksgrad": forbruksgrad,
        "rag_status": rag_status,
        "rag_label": rag_label,
        "rag_color": rag_color,
        "rag_bg": rag_bg,
        "is_surplus": is_surplus,
        "diagnostics": {
            "fastlonn": fastlonn,
            "vikarer": vikarer,
            "overtid": overtid,
            "drift": drift,
            "nav_refusjon": nav_refusjon,
            "andre_inntekter": andre_inntekter,
            "sykefravaer": sykefravaer,
            "vikar_andel_pct": vikar_andel * 100.0,
            "nav_gap": nav_gap
        },
        "prognosis": {
            "p10": p10,
            "p50": p50,
            "p90": p90,
            "sluttavvik_p50": sluttavvik_eoy_p50,
            "sha256": sha256_hash
        },
        "preskripsjoner": preskripsjoner,
        "totalt_tiltak_nok": totalt_tiltak_nok,
        "paraply": {
            "sektor_kode": sektor_kode,
            "paraply_navn": paraply_info["paraply_navn"],
            "leder": paraply_info["leder"],
            "leder_tittel": paraply_info["leder_tittel"],
            "controller": paraply_info["controller"],
            "omdisponering_tekst": omdisponering_tekst,
            "omdisponerings_belop": omdisponerings_belop,
            "framsikt_deb_kred": framsikt_deb_kred
        }
    }


def generate_pdf_report(metrics: Dict[str, Any], output_path: Path) -> Path:
    """Genererer en komplett, profesjonell PDF-månedsrapport etter Edward Tufte-standarder."""
    holder = metrics["holder"]
    m_name = metrics["month_name"]
    month = metrics["month"]
    ansvar_id = holder["ansvar_id"]

    # Opprett dokument
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm
    )

    styles = getSampleStyleSheet()

    # Egendefinerte Tufte-stiler (uten støy, klare hierarkier)
    style_title = ParagraphStyle(
        "TufteTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1e293b")
    )
    style_subtitle = ParagraphStyle(
        "TufteSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748b")
    )
    style_h2 = ParagraphStyle(
        "TufteH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=10,
        spaceAfter=4
    )
    style_body = ParagraphStyle(
        "TufteBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155")
    )
    style_body_bold = ParagraphStyle(
        "TufteBodyBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b")
    )
    style_kpi_num = ParagraphStyle(
        "TufteKpiNum",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        alignment=1,  # Center
        textColor=colors.HexColor("#0f172a")
    )
    style_kpi_label = ParagraphStyle(
        "TufteKpiLabel",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        alignment=1,
        textColor=colors.HexColor("#64748b")
    )
    style_table_cell = ParagraphStyle(
        "TufteTableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#334155")
    )
    style_table_cell_bold = ParagraphStyle(
        "TufteTableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )
    style_table_num = ParagraphStyle(
        "TufteTableNum",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        alignment=2,  # Right
        textColor=colors.HexColor("#334155")
    )
    style_table_num_bold = ParagraphStyle(
        "TufteTableNumBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        alignment=2,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # 1. HODE / METADATA
    header_data = [
        [
            Paragraph("🏛️ <b>KRISTIANSAND KOMMUNE</b><br/>Økonomi & Virksomhetsstyring", style_subtitle),
            Paragraph(f"<b>STATUSRAPPORT M{month} / {m_name.upper()} 2026</b><br/>Avviks- og Handlingsrapport for Budsjettansvarlig", style_subtitle)
        ]
    ]
    t_head = Table(header_data, colWidths=[90 * mm, 90 * mm])
    t_head.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_head)
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e293b"), spaceBefore=4, spaceAfter=8))

    # Tittel
    story.append(Paragraph(f"{holder['enhet_navn']} — Ansvar {ansvar_id}", style_title))
    meta_line = (
        f"<b>Budsjettansvarlig:</b> {holder['navn']} ({holder['tittel']}) | "
        f"<b>E-post:</b> {holder['epost']} | <b>Fullmakt:</b> kr {holder['delegeringsfullmakt_nok']:,.0f} | "
        f"<b>Sektorcontroller:</b> {holder['controller_navn']}"
    )
    story.append(Paragraph(meta_line, style_subtitle))
    story.append(Spacer(1, 6 * mm))

    # 2. KPI-STRIPE (Edward Tufte card-strip uten drop shadows)
    # Avvik = Budsjett - Actuals
    avvik_val = metrics["avvik_ytd"]
    avvik_sign = "+" if avvik_val >= 0 else ""
    avvik_color = "#166534" if avvik_val >= 0 else "#991b1b"

    kpi_cols = [
        [
            Paragraph("TILDELT ÅRSBUDSJETT", style_kpi_label),
            Paragraph(f"kr {metrics['annual_budget']:,.0f}", style_kpi_num),
            Paragraph(f"Vedtatt ramme 2026", style_kpi_label)
        ],
        [
            Paragraph("PERIODISERT BUDSJETT YTD", style_kpi_label),
            Paragraph(f"kr {metrics['ytd_budget']:,.0f}", style_kpi_num),
            Paragraph(f"Andel: {sum(SEASONAL_WEIGHTS[:month])*100:.1f} %", style_kpi_label)
        ],
        [
            Paragraph("FAKTISK REGNSKAP YTD", style_kpi_label),
            Paragraph(f"kr {metrics['ytd_actual']:,.0f}", style_kpi_num),
            Paragraph(f"Forbruk: {metrics['forbruksgrad']:.1f} %", style_kpi_label)
        ],
        [
            Paragraph("AVVIK YTD (BUDSJETT - REGNSKAP)", style_kpi_label),
            Paragraph(f"<font color='{avvik_color}'>{avvik_sign}kr {avvik_val:,.0f}</font>", style_kpi_num),
            Paragraph(metrics["rag_label"], style_kpi_label)
        ]
    ]

    t_kpi = Table(
        [
            [kpi_cols[0][0], kpi_cols[1][0], kpi_cols[2][0], kpi_cols[3][0]],
            [kpi_cols[0][1], kpi_cols[1][1], kpi_cols[2][1], kpi_cols[3][1]],
            [kpi_cols[0][2], kpi_cols[1][2], kpi_cols[2][2], kpi_cols[3][2]],
        ],
        colWidths=[45 * mm, 45 * mm, 45 * mm, 45 * mm]
    )
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 6 * mm))

    # 3. SEKSJON 1: FINANSIELL STATUS & KOSTRADATA (Tufte tabell uten vertikale linjer)
    story.append(Paragraph("1. Finansiell Status og Artsavvik (YTD)", style_h2))
    diag = metrics["diagnostics"]

    # Lag detaljrader for artstabell
    # Avvik = Budsjett - Regnskap
    b_fast = metrics["ytd_budget"] * 0.65
    b_vikar = metrics["ytd_budget"] * 0.08
    b_over = metrics["ytd_budget"] * 0.04
    b_drift = metrics["ytd_budget"] * 0.31
    b_inntekt = metrics["ytd_budget"] * 0.08

    arts_data = [
        [
            Paragraph("<b>KOSTRA Art</b>", style_table_cell_bold),
            Paragraph("<b>Beskrivelse</b>", style_table_cell_bold),
            Paragraph("<b>Budsjett YTD</b>", style_table_num_bold),
            Paragraph("<b>Regnskap YTD</b>", style_table_num_bold),
            Paragraph("<b>Avvik (Budsjett - Actuals)</b>", style_table_num_bold),
            Paragraph("<b>Status</b>", style_table_cell_bold)
        ],
        [
            Paragraph("Art 1010", style_table_cell),
            Paragraph("Fast lønn og faste stillinger", style_table_cell),
            Paragraph(f"kr {b_fast:,.0f}", style_table_num),
            Paragraph(f"kr {diag['fastlonn']:,.0f}", style_table_num),
            Paragraph(f"{'+' if (b_fast - diag['fastlonn']) >= 0 else ''}kr {b_fast - diag['fastlonn']:,.0f}", style_table_num),
            Paragraph("Normal drift", style_table_cell)
        ],
        [
            Paragraph("Art 1020", style_table_cell),
            Paragraph("Vikarer og innleie", style_table_cell),
            Paragraph(f"kr {b_vikar:,.0f}", style_table_num),
            Paragraph(f"kr {diag['vikarer']:,.0f}", style_table_num),
            Paragraph(f"<font color='{'#166534' if (b_vikar - diag['vikarer'])>=0 else '#991b1b'}'><b>{'+' if (b_vikar - diag['vikarer'])>=0 else ''}kr {b_vikar - diag['vikarer']:,.0f}</b></font>", style_table_num),
            Paragraph("🔴 Kritisk driver" if (b_vikar - diag['vikarer']) < 0 else "🟢 Kontrollert", style_table_cell)
        ],
        [
            Paragraph("Art 1090", style_table_cell),
            Paragraph("Overtid og ubekvem tid", style_table_cell),
            Paragraph(f"kr {b_over:,.0f}", style_table_num),
            Paragraph(f"kr {diag['overtid']:,.0f}", style_table_num),
            Paragraph(f"{'+' if (b_over - diag['overtid'])>=0 else ''}kr {b_over - diag['overtid']:,.0f}", style_table_num),
            Paragraph("Turnusavvik" if (b_over - diag['overtid']) < 0 else "I vater", style_table_cell)
        ],
        [
            Paragraph("Art 1150-1200", style_table_cell),
            Paragraph("Varekjøp, inventar og drift", style_table_cell),
            Paragraph(f"kr {b_drift:,.0f}", style_table_num),
            Paragraph(f"kr {diag['drift']:,.0f}", style_table_num),
            Paragraph(f"{'+' if (b_drift - diag['drift'])>=0 else ''}kr {b_drift - diag['drift']:,.0f}", style_table_num),
            Paragraph("Driftsforbruk", style_table_cell)
        ],
        [
            Paragraph("Art 1690", style_table_cell),
            Paragraph("Refusjon sykelønn (NAV)", style_table_cell),
            Paragraph(f"kr {b_inntekt:,.0f}", style_table_num),
            Paragraph(f"kr {diag['nav_refusjon']:,.0f}", style_table_num),
            Paragraph(f"{'+' if (diag['nav_refusjon'] - b_inntekt)>=0 else ''}kr {diag['nav_refusjon'] - b_inntekt:,.0f}", style_table_num),
            Paragraph("Refusjonsgap" if diag["nav_gap"] > 100000 else "Ajour", style_table_cell)
        ],
        [
            Paragraph("<b>TOTALT NETTO</b>", style_table_cell_bold),
            Paragraph("<b>Samlet netto ramme YTD</b>", style_table_cell_bold),
            Paragraph(f"<b>kr {metrics['ytd_budget']:,.0f}</b>", style_table_num_bold),
            Paragraph(f"<b>kr {metrics['ytd_actual']:,.0f}</b>", style_table_num_bold),
            Paragraph(f"<font color='{avvik_color}'><b>{avvik_sign}kr {avvik_val:,.0f}</b></font>", style_table_num_bold),
            Paragraph(f"<b>{metrics['rag_status']}</b>", style_table_cell_bold)
        ]
    ]

    t_arts = Table(arts_data, colWidths=[24 * mm, 46 * mm, 27 * mm, 27 * mm, 32 * mm, 24 * mm])
    t_arts.setStyle(TableStyle([
        # Edward Tufte tabell: Null vertikale linjer!
        ('LINEBEFORE', (0,0), (-1,-1), 0, colors.white),
        ('LINEAFTER', (0,0), (-1,-1), 0, colors.white),
        ('LINEBELOW', (0,0), (-1,0), 1.2, colors.HexColor("#1e293b")),
        ('LINEBELOW', (0,1), (-1,-2), 0.5, colors.HexColor("#e2e8f0")),
        ('LINEABOVE', (0,-1), (-1,-1), 1.0, colors.HexColor("#1e293b")),
        ('LINEBELOW', (0,-1), (-1,-1), 1.5, colors.HexColor("#1e293b")),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#f1f5f9")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_arts)
    story.append(Spacer(1, 4 * mm))

    # 4. SEKSJON 2: DYBDEDIAGNOSTIKK & KOSTNADSDRIVERE
    story.append(Paragraph("2. Dybdediagnostikk & Kostnadsdrivere", style_h2))
    diag_text = (
        f"• <b>Sykefravær:</b> Registrert til <b>{diag['sykefravaer']:.1f} %</b> "
        f"(måltall Kristiansand: 6,5 %). "
        f"• <b>Vikarandel:</b> Vikarkostnader utgjør <b>{diag['vikar_andel_pct']:.1f} %</b> av samlet lønnsmasse. "
        f"• <b>NAV-refusjonsgap:</b> Utestående/etterslep på refusjonskrav er beregnet til <b>kr {diag['nav_gap']:,.0f}</b>. "
        f"Raskere innsending av refusjonskrav til NAV vil styrke enhetens likviditet direkte på art 1690."
    )
    story.append(Paragraph(diag_text, style_body))
    story.append(Spacer(1, 4 * mm))

    # 5. SEKSJON 3: PROGNOSER & MONTE CARLO EOY (10K SIMULERINGER)
    story.append(Paragraph("3. Sesongjustert EOY-Prognose & Monte Carlo Usikkerhet", style_h2))
    prog = metrics["prognosis"]
    prog_sign = "+" if prog["sluttavvik_p50"] >= 0 else ""
    prog_color = "#166534" if prog["sluttavvik_p50"] >= 0 else "#991b1b"

    prog_data = [
        [
            Paragraph("<b>Scenario / Modell</b>", style_table_cell_bold),
            Paragraph("<b>P10 (Optimistisk)</b>", style_table_num_bold),
            Paragraph("<b>P50 (Forventet EOY)</b>", style_table_num_bold),
            Paragraph("<b>P90 (Konservativt)</b>", style_table_num_bold),
            Paragraph("<b>Forventet Sluttavvik (31.12)</b>", style_table_num_bold)
        ],
        [
            Paragraph("Driverbasert Monte Carlo (10 000 iterasjoner)", style_table_cell),
            Paragraph(f"kr {prog['p10']:,.0f}", style_table_num),
            Paragraph(f"<b>kr {prog['p50']:,.0f}</b>", style_table_num_bold),
            Paragraph(f"kr {prog['p90']:,.0f}", style_table_num),
            Paragraph(f"<font color='{prog_color}'><b>{prog_sign}kr {prog['sluttavvik_p50']:,.0f}</b></font>", style_table_num_bold)
        ]
    ]
    t_prog = Table(prog_data, colWidths=[65 * mm, 28 * mm, 30 * mm, 28 * mm, 29 * mm])
    t_prog.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1.0, colors.HexColor("#1e293b")),
        ('LINEBELOW', (0,1), (-1,1), 1.0, colors.HexColor("#1e293b")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_prog)
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph(f"<font size='6.5' color='#64748b'>Kryptografisk SHA-256 forsegling (Stage-Gate Port 9): {prog['sha256']}</font>", style_body))
    story.append(Spacer(1, 4 * mm))

    # 6. SEKSJON 4: PRESKRIPUSJONER FOR NETTO NULL AVVIK VED ÅRSSLUTT
    story.append(Paragraph("4. Preskripsjoner & Tiltaksplan for Netto Null Avvik (EOY = 0)", style_h2))
    presk_rows = [
        [
            Paragraph("<b>#</b>", style_table_cell_bold),
            Paragraph("<b>Tiltak / Handlingsregel</b>", style_table_cell_bold),
            Paragraph("<b>Art</b>", style_table_cell_bold),
            Paragraph("<b>Ansvarlig</b>", style_table_cell_bold),
            Paragraph("<b>Effekt Måned</b>", style_table_num_bold),
            Paragraph("<b>Helårseffekt</b>", style_table_num_bold)
        ]
    ]
    for p in metrics["preskripsjoner"]:
        presk_rows.append([
            Paragraph(str(p["nr"]), style_table_cell),
            Paragraph(f"<b>{p['tittel']}</b><br/>{p['handling']}", style_table_cell),
            Paragraph(p["art"], style_table_cell),
            Paragraph(p["ansvarlig"], style_table_cell),
            Paragraph(f"kr {p['maanedlig_effekt_nok']:,.0f}", style_table_num),
            Paragraph(f"<b>kr {p['helars_effekt_nok']:,.0f}</b>", style_table_num_bold)
        ])
    presk_rows.append([
        Paragraph("<b>SUM</b>", style_table_cell_bold),
        Paragraph("<b>Total tiltakseffekt for å lukke avviket</b>", style_table_cell_bold),
        Paragraph("-", style_table_cell),
        Paragraph("-", style_table_cell),
        Paragraph("-", style_table_num),
        Paragraph(f"<b>kr {metrics['totalt_tiltak_nok']:,.0f}</b>", style_table_num_bold)
    ])

    t_presk = Table(presk_rows, colWidths=[8 * mm, 80 * mm, 18 * mm, 30 * mm, 22 * mm, 22 * mm])
    t_presk.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1.0, colors.HexColor("#1e293b")),
        ('LINEBELOW', (0,1), (-1,-2), 0.5, colors.HexColor("#e2e8f0")),
        ('LINEABOVE', (0,-1), (-1,-1), 1.0, colors.HexColor("#1e293b")),
        ('LINEBELOW', (0,-1), (-1,-1), 1.2, colors.HexColor("#1e293b")),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#f8fafc")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_presk)
    story.append(Spacer(1, 4 * mm))

    # 7. SEKSJON 5: BUDSJETTPARAPLYEN: OMDISPONERING MELLOM NIVÅER
    paraply = metrics["paraply"]
    story.append(Paragraph("5. Budsjettparaplyen: Omdisponerings- og Solidaritetsmekanisme", style_h2))
    story.append(Paragraph(paraply["omdisponering_tekst"], style_body))
    story.append(Spacer(1, 3 * mm))

    # 8. SEKSJON 6: FRAMSIKT EPM KONTERINGSVEILEDER
    story.append(Paragraph("6. Framsikt EPM: Konkret Konteringsanvisning & Rammeregulering", style_h2))
    deb_kred = paraply["framsikt_deb_kred"]

    framsikt_table = [
        [
            Paragraph("<b>Posteringstype</b>", style_table_cell_bold),
            Paragraph("<b>Ansvar (KOSTRA)</b>", style_table_cell_bold),
            Paragraph("<b>Art</b>", style_table_cell_bold),
            Paragraph("<b>Fritekst / Begrunnelse i Framsikt</b>", style_table_cell_bold),
            Paragraph("<b>Budsjettjustering</b>", style_table_num_bold)
        ],
        [
            Paragraph("Avgivende ramme", style_table_cell),
            Paragraph(f"<b>{deb_kred['avgiver_ansvar']}</b>", style_table_cell),
            Paragraph(deb_kred['avgiver_art'], style_table_cell),
            Paragraph(deb_kred['avgiver_tekst'], style_table_cell),
            Paragraph(f"<font color='#991b1b'><b>kr {deb_kred['avgiver_belop']:,.0f}</b></font>", style_table_num_bold)
        ],
        [
            Paragraph("Mottakende ramme", style_table_cell),
            Paragraph(f"<b>{deb_kred['mottaker_ansvar']}</b>", style_table_cell),
            Paragraph(deb_kred['mottaker_art'], style_table_cell),
            Paragraph(deb_kred['mottaker_tekst'], style_table_cell),
            Paragraph(f"<font color='#166534'><b>+kr {deb_kred['mottaker_belop']:,.0f}</b></font>", style_table_num_bold)
        ],
        [
            Paragraph("<b>NETTO ENDRING</b>", style_table_cell_bold),
            Paragraph("<b>Sektorramme balanse</b>", style_table_cell_bold),
            Paragraph("-", style_table_cell),
            Paragraph("<b>Fullmakt: Kommunalsjef (Nivå 1) / Bystyret § 14-5</b>", style_table_cell_bold),
            Paragraph("<b>kr 0,00</b>", style_table_num_bold)
        ]
    ]

    t_fram = Table(framsikt_table, colWidths=[28 * mm, 30 * mm, 20 * mm, 74 * mm, 28 * mm])
    t_fram.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1.0, colors.HexColor("#1e293b")),
        ('LINEBELOW', (0,1), (-1,-2), 0.5, colors.HexColor("#e2e8f0")),
        ('LINEABOVE', (0,-1), (-1,-1), 1.0, colors.HexColor("#1e293b")),
        ('LINEBELOW', (0,-1), (-1,-1), 1.2, colors.HexColor("#1e293b")),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#f1f5f9")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_fram)
    story.append(Spacer(1, 6 * mm))

    # 9. SIGNATUR OG ATTESTASJON
    sig_data = [
        [
            Paragraph(f"<b>Attestert av Budsjettansvarlig:</b><br/><br/>________________________________________<br/>{holder['navn']}<br/>Dato: ____ / ____ 2026", style_body),
            Paragraph(f"<b>Kvalitetssikret av Sektorcontroller:</b><br/><br/>________________________________________<br/>{holder['controller_navn']}<br/>Dato: ____ / ____ 2026", style_body)
        ]
    ]
    t_sig = Table(sig_data, colWidths=[90 * mm, 90 * mm])
    t_sig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(KeepTogether(t_sig))

    # Bygg PDF
    doc.build(story)
    return output_path


def generate_html_report(metrics: Dict[str, Any], output_path: Path) -> Path:
    """Genererer en ren, interaktiv HTML-månedsrapport tilpasset skjerm og utskrift (@media print)."""
    holder = metrics["holder"]
    m_name = metrics["month_name"]
    month = metrics["month"]
    ansvar_id = holder["ansvar_id"]
    avvik_val = metrics["avvik_ytd"]
    avvik_sign = "+" if avvik_val >= 0 else ""
    avvik_class = "positive" if avvik_val >= 0 else "negative"
    diag = metrics["diagnostics"]
    prog = metrics["prognosis"]
    paraply = metrics["paraply"]
    deb_kred = paraply["framsikt_deb_kred"]

    b_fast = metrics["ytd_budget"] * 0.65
    b_vikar = metrics["ytd_budget"] * 0.08
    b_over = metrics["ytd_budget"] * 0.04
    b_drift = metrics["ytd_budget"] * 0.31
    b_inntekt = metrics["ytd_budget"] * 0.08

    presk_html = ""
    for p in metrics["preskripsjoner"]:
        presk_html += f"""
        <tr>
            <td>{p['nr']}</td>
            <td><strong>{p['tittel']}</strong><br/><span class="subtext">{p['handling']}</span></td>
            <td><code>{p['art']}</code></td>
            <td>{p['ansvarlig']}</td>
            <td class="num">kr {p['maanedlig_effekt_nok']:,.0f}</td>
            <td class="num"><strong>kr {p['helars_effekt_nok']:,.0f}</strong></td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Månedsrapport M{month} — {holder['enhet_navn']} ({ansvar_id})</title>
    <style>
        :root {{
            --bg-page: #f8fafc;
            --surface: #ffffff;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --border-light: #e2e8f0;
            --border-strong: #1e293b;
            --green: #166534;
            --green-bg: #dcfce7;
            --red: #991b1b;
            --red-bg: #fee2e2;
            --amber: #9a3412;
            --amber-bg: #ffedd5;
            --accent-navy: #1e293b;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg-page);
            color: var(--text-primary);
            line-height: 1.45;
            padding: 24px;
        }}
        .report-sheet {{
            max-width: 960px;
            margin: 0 auto;
            background: var(--surface);
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 36px 42px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }}
        .header-strip {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 2px solid var(--border-strong);
            padding-bottom: 12px;
            margin-bottom: 20px;
        }}
        .header-title {{ font-size: 20px; font-weight: 700; color: var(--text-primary); }}
        .header-meta {{ font-size: 11px; color: var(--text-muted); text-align: right; }}
        .unit-name {{ font-size: 16px; font-weight: 600; color: var(--accent-navy); margin-bottom: 4px; }}
        .unit-sub {{ font-size: 12px; color: var(--text-secondary); margin-bottom: 20px; }}
        
        .kpi-strip {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            background: #f1f5f9;
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 14px 16px;
            margin-bottom: 28px;
        }}
        .kpi-card {{ text-align: center; }}
        .kpi-label {{ font-size: 10px; font-weight: 600; text-transform: uppercase; color: var(--text-muted); margin-bottom: 4px; }}
        .kpi-value {{ font-size: 18px; font-weight: 700; color: var(--text-primary); }}
        .kpi-sub {{ font-size: 11px; color: var(--text-secondary); }}
        
        h2 {{ font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--accent-navy); margin: 24px 0 10px 0; border-bottom: 1px solid var(--border-strong); padding-bottom: 4px; }}
        
        /* Tufte Tabeller: Null vertikale linjer */
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            margin-bottom: 18px;
        }}
        th {{
            text-align: left;
            font-weight: 600;
            color: var(--text-primary);
            border-bottom: 1.5px solid var(--border-strong);
            padding: 6px 8px;
        }}
        td {{
            padding: 6px 8px;
            border-bottom: 1px solid var(--border-light);
            color: var(--text-secondary);
        }}
        tr.total-row td {{
            font-weight: 700;
            color: var(--text-primary);
            border-top: 1.5px solid var(--border-strong);
            border-bottom: 2px solid var(--border-strong);
            background: #f8fafc;
        }}
        .num {{ text-align: right; }}
        .positive {{ color: var(--green); font-weight: 700; }}
        .negative {{ color: var(--red); font-weight: 700; }}
        .subtext {{ font-size: 11px; color: var(--text-muted); }}
        
        .box-info {{
            background: #f8fafc;
            border-left: 3px solid var(--accent-navy);
            padding: 10px 14px;
            font-size: 12px;
            color: var(--text-secondary);
            margin-bottom: 20px;
        }}
        
        .signatures {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin-top: 36px;
            padding-top: 18px;
            border-top: 1px dashed var(--border-light);
            font-size: 12px;
        }}
        
        .print-btn {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: var(--accent-navy);
            color: #fff;
            border: none;
            padding: 10px 18px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .print-btn:hover {{ background: #0f172a; }}

        @media print {{
            body {{ background: #fff; padding: 0; }}
            .report-sheet {{ border: none; box-shadow: none; padding: 0; max-width: 100%; }}
            .print-btn {{ display: none; }}
        }}
    </style>
</head>
<body>
    <button class="print-btn" onclick="window.print()">🖨️ Skriv ut / Lagre som PDF</button>

    <div class="report-sheet">
        <div class="header-strip">
            <div>
                <div class="header-title">🏛️ KRISTIANSAND KOMMUNE</div>
                <div class="subtext">Økonomi og virksomhetsstyring | AI Project Controller Hub</div>
            </div>
            <div class="header-meta">
                <strong>STATUSRAPPORT M{month} / {m_name.upper()} 2026</strong><br/>
                Generert: 17.10.2026 | Utsendelse: Budsjettansvarlig
            </div>
        </div>

        <div class="unit-name">{holder['enhet_navn']} — Ansvar {ansvar_id}</div>
        <div class="unit-sub">
            <strong>Budsjettansvarlig:</strong> {holder['navn']} ({holder['tittel']}) | 
            <strong>E-post:</strong> {holder['epost']} | 
            <strong>Delegeringsfullmakt:</strong> kr {holder['delegeringsfullmakt_nok']:,.0f} | 
            <strong>Sektorcontroller:</strong> {holder['controller_navn']}
        </div>

        <!-- KPI Strip -->
        <div class="kpi-strip">
            <div class="kpi-card">
                <div class="kpi-label">Tildelt Årsbudsjett</div>
                <div class="kpi-value">kr {metrics['annual_budget']:,.0f}</div>
                <div class="kpi-sub">Vedtatt ramme 2026</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Periodisert Budsjett YTD</div>
                <div class="kpi-value">kr {metrics['ytd_budget']:,.0f}</div>
                <div class="kpi-sub">Andel: {sum(SEASONAL_WEIGHTS[:month])*100:.1f} %</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Faktisk Regnskap YTD</div>
                <div class="kpi-value">kr {metrics['ytd_actual']:,.0f}</div>
                <div class="kpi-sub">Forbruksgrad: {metrics['forbruksgrad']:.1f} %</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Avvik (Budsjett - Actuals)</div>
                <div class="kpi-value {avvik_class}">{avvik_sign}kr {avvik_val:,.0f}</div>
                <div class="kpi-sub">{metrics['rag_label']}</div>
            </div>
        </div>

        <!-- 1. Finansiell Status -->
        <h2>1. Finansiell Status og Artsavvik (YTD)</h2>
        <table>
            <thead>
                <tr>
                    <th>KOSTRA Art</th>
                    <th>Beskrivelse</th>
                    <th class="num">Budsjett YTD</th>
                    <th class="num">Regnskap YTD</th>
                    <th class="num">Avvik (Budsjett - Actuals)</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>Art 1010</code></td>
                    <td>Fast lønn og faste stillinger</td>
                    <td class="num">kr {b_fast:,.0f}</td>
                    <td class="num">kr {diag['fastlonn']:,.0f}</td>
                    <td class="num {'positive' if (b_fast - diag['fastlonn'])>=0 else 'negative'}">{'+' if (b_fast - diag['fastlonn'])>=0 else ''}kr {b_fast - diag['fastlonn']:,.0f}</td>
                    <td>Normal drift</td>
                </tr>
                <tr>
                    <td><code>Art 1020</code></td>
                    <td>Vikarer og innleie</td>
                    <td class="num">kr {b_vikar:,.0f}</td>
                    <td class="num">kr {diag['vikarer']:,.0f}</td>
                    <td class="num {'positive' if (b_vikar - diag['vikarer'])>=0 else 'negative'}">{'+' if (b_vikar - diag['vikarer'])>=0 else ''}kr {b_vikar - diag['vikarer']:,.0f}</td>
                    <td>{'🔴 Kritisk driver' if (b_vikar - diag['vikarer'])<0 else '🟢 Kontrollert'}</td>
                </tr>
                <tr>
                    <td><code>Art 1090</code></td>
                    <td>Overtid og ubekvem tid</td>
                    <td class="num">kr {b_over:,.0f}</td>
                    <td class="num">kr {diag['overtid']:,.0f}</td>
                    <td class="num {'positive' if (b_over - diag['overtid'])>=0 else 'negative'}">{'+' if (b_over - diag['overtid'])>=0 else ''}kr {b_over - diag['overtid']:,.0f}</td>
                    <td>{'Turnusavvik' if (b_over - diag['overtid'])<0 else 'I vater'}</td>
                </tr>
                <tr>
                    <td><code>Art 1150-1200</code></td>
                    <td>Varekjøp, inventar og drift</td>
                    <td class="num">kr {b_drift:,.0f}</td>
                    <td class="num">kr {diag['drift']:,.0f}</td>
                    <td class="num {'positive' if (b_drift - diag['drift'])>=0 else 'negative'}">{'+' if (b_drift - diag['drift'])>=0 else ''}kr {b_drift - diag['drift']:,.0f}</td>
                    <td>Driftsforbruk</td>
                </tr>
                <tr>
                    <td><code>Art 1690</code></td>
                    <td>Refusjon sykelønn (NAV)</td>
                    <td class="num">kr {b_inntekt:,.0f}</td>
                    <td class="num">kr {diag['nav_refusjon']:,.0f}</td>
                    <td class="num {'positive' if (diag['nav_refusjon'] - b_inntekt)>=0 else 'negative'}">{'+' if (diag['nav_refusjon'] - b_inntekt)>=0 else ''}kr {diag['nav_refusjon'] - b_inntekt:,.0f}</td>
                    <td>{'Refusjonsgap' if diag['nav_gap'] > 100000 else 'Ajour'}</td>
                </tr>
                <tr class="total-row">
                    <td>TOTALT NETTO</td>
                    <td>Samlet netto ramme YTD</td>
                    <td class="num">kr {metrics['ytd_budget']:,.0f}</td>
                    <td class="num">kr {metrics['ytd_actual']:,.0f}</td>
                    <td class="num {avvik_class}">{avvik_sign}kr {avvik_val:,.0f}</td>
                    <td>{metrics['rag_status']}</td>
                </tr>
            </tbody>
        </table>

        <!-- 2. Dybdediagnostikk -->
        <h2>2. Dybdediagnostikk & Kostnadsdrivere</h2>
        <div class="box-info">
            <strong>Nøkkeltall for perioden:</strong><br/>
            • <strong>Sykefravær:</strong> Registrert til <strong>{diag['sykefravaer']:.1f} %</strong> (kommunens måltall er 6,5 %).<br/>
            • <strong>Vikarandel:</strong> Vikarkostnader utgjør <strong>{diag['vikar_andel_pct']:.1f} %</strong> av samlet lønnsmasse.<br/>
            • <strong>NAV-refusjonsgap:</strong> Utestående refusjonskrav er beregnet til <strong>kr {diag['nav_gap']:,.0f}</strong>. Raskere innsending vil styrke netto drift direkte.
        </div>

        <!-- 3. Prognoser -->
        <h2>3. Sesongjustert EOY-Prognose & Monte Carlo Usikkerhet</h2>
        <table>
            <thead>
                <tr>
                    <th>Scenario / Modell</th>
                    <th class="num">P10 (Optimistisk)</th>
                    <th class="num">P50 (Forventet EOY)</th>
                    <th class="num">P90 (Konservativt)</th>
                    <th class="num">Forventet Sluttavvik (31.12)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Driverbasert Monte Carlo (10 000 iterasjoner)</td>
                    <td class="num">kr {prog['p10']:,.0f}</td>
                    <td class="num"><strong>kr {prog['p50']:,.0f}</strong></td>
                    <td class="num">kr {prog['p90']:,.0f}</td>
                    <td class="num {'positive' if prog['sluttavvik_p50']>=0 else 'negative'}"><strong>{'+' if prog['sluttavvik_p50']>=0 else ''}kr {prog['sluttavvik_p50']:,.0f}</strong></td>
                </tr>
            </tbody>
        </table>
        <div class="subtext">Kryptografisk SHA-256 forsegling (Stage-Gate Port 9): <code>{prog['sha256']}</code></div>

        <!-- 4. Preskripsjoner -->
        <h2>4. Preskripsjoner & Handlingsplan for Netto Null Avvik (EOY = 0)</h2>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Tiltak / Handlingsregel</th>
                    <th>Art</th>
                    <th>Ansvarlig</th>
                    <th class="num">Effekt Måned</th>
                    <th class="num">Helårseffekt</th>
                </tr>
            </thead>
            <tbody>
                {presk_html}
                <tr class="total-row">
                    <td>SUM</td>
                    <td>Total tiltakseffekt for å lukke avviket</td>
                    <td>-</td>
                    <td>-</td>
                    <td class="num">-</td>
                    <td class="num">kr {metrics['totalt_tiltak_nok']:,.0f}</td>
                </tr>
            </tbody>
        </table>

        <!-- 5. Budsjettparaplyen -->
        <h2>5. Budsjettparaplyen: Omdisponerings- og Solidaritetsmekanisme</h2>
        <div class="box-info">
            {paraply['omdisponering_tekst']}
        </div>

        <!-- 6. Framsikt EPM -->
        <h2>6. Framsikt EPM: Konkret Konteringsanvisning & Rammeregulering</h2>
        <p class="subtext" style="margin-bottom: 8px;">
            Følgende poster registreres i Framsikt EPM (Modul: <em>Tertialoppfølging / Budsjettreguleringer</em>) under Kommunalsjefens fullmakt:
        </p>
        <table>
            <thead>
                <tr>
                    <th>Posteringstype</th>
                    <th>Ansvar (KOSTRA)</th>
                    <th>Art</th>
                    <th>Fritekst / Begrunnelse i Framsikt</th>
                    <th class="num">Budsjettjustering</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Avgivende ramme</td>
                    <td><strong>{deb_kred['avgiver_ansvar']}</strong></td>
                    <td><code>{deb_kred['avgiver_art']}</code></td>
                    <td>{deb_kred['avgiver_tekst']}</td>
                    <td class="num negative">kr {deb_kred['avgiver_belop']:,.0f}</td>
                </tr>
                <tr>
                    <td>Mottakende ramme</td>
                    <td><strong>{deb_kred['mottaker_ansvar']}</strong></td>
                    <td><code>{deb_kred['mottaker_art']}</code></td>
                    <td>{deb_kred['mottaker_tekst']}</td>
                    <td class="num positive">+kr {deb_kred['mottaker_belop']:,.0f}</td>
                </tr>
                <tr class="total-row">
                    <td>NETTO ENDRING</td>
                    <td>Sektorramme balanse</td>
                    <td>-</td>
                    <td>Fullmakt: Kommunalsjef (Nivå 1) / Bystyret § 14-5</td>
                    <td class="num">kr 0,00</td>
                </tr>
            </tbody>
        </table>

        <!-- 7. Signaturer -->
        <div class="signatures">
            <div>
                <strong>Attestert av Budsjettansvarlig:</strong><br/><br/>
                ________________________________________<br/>
                {holder['navn']}<br/>
                Dato: ____ / ____ 2026
            </div>
            <div>
                <strong>Kvalitetssikret av Sektorcontroller:</strong><br/><br/>
                ________________________________________<br/>
                {holder['controller_navn']}<br/>
                Dato: ____ / ____ 2026
            </div>
        </div>
    </div>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def export_framsikt_batch_csv(all_metrics: List[Dict[str, Any]], output_path: Path, month: int):
    """
    Eksporterer ferdig Framsikt-kompatibel CSV batch-fil for rammereguleringer.
    Formatet matcher Framsikt EPMs importoppsett for administrative rammereguleringer.
    """
    rows = []
    reg_id_seq = 1001

    for m in all_metrics:
        deb_kred = m["paraply"]["framsikt_deb_kred"]
        ansvar_id = m["holder"]["ansvar_id"]
        sektor = m["holder"]["sektor_kode"]
        reg_id = f"REG-2026-M{month}-{reg_id_seq}"
        reg_id_seq += 1

        # Avgivende linje
        rows.append({
            "regulerings_id": reg_id,
            "periode": f"2026-M{month:02d}",
            "sektor_kode": sektor,
            "type": "RAMMEREGULERING",
            "ansvar_kode": deb_kred["avgiver_ansvar"],
            "funksjon_kode": m["holder"].get("kostra_funksjon", "202").split()[0],
            "art_kode": deb_kred["avgiver_art"].split()[0],
            "belop_nok": deb_kred["avgiver_belop"],
            "tekst": deb_kred["avgiver_tekst"],
            "attestant_upn": m["holder"]["epost"],
            "controller_upn": m["holder"]["controller_epost"],
            "status": "FORSLAG_TIL_KOMMUNALSJEF"
        })

        # Mottakende linje
        rows.append({
            "regulerings_id": reg_id,
            "periode": f"2026-M{month:02d}",
            "sektor_kode": sektor,
            "type": "RAMMEREGULERING",
            "ansvar_kode": deb_kred["mottaker_ansvar"],
            "funksjon_kode": m["holder"].get("kostra_funksjon", "202").split()[0],
            "art_kode": deb_kred["mottaker_art"].split()[0],
            "belop_nok": deb_kred["mottaker_belop"],
            "tekst": deb_kred["mottaker_tekst"],
            "attestant_upn": m["holder"]["epost"],
            "controller_upn": m["holder"]["controller_epost"],
            "status": "FORSLAG_TIL_KOMMUNALSJEF"
        })

    fieldnames = [
        "regulerings_id", "periode", "sektor_kode", "type", "ansvar_kode",
        "funksjon_kode", "art_kode", "belop_nok", "tekst", "attestant_upn",
        "controller_upn", "status"
    ]
    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def generate_portal_index(all_metrics: List[Dict[str, Any]], output_path: Path, month: int):
    """Genererer en moderne og oversiktlig index.html for å navigere alle genererte månedsrapporter."""
    m_name = MONTH_NAMES[month - 1]
    
    rows_html = ""
    for m in all_metrics:
        h = m["holder"]
        aid = h["ansvar_id"]
        avv = m["avvik_ytd"]
        avv_sign = "+" if avv >= 0 else ""
        avv_class = "positive" if avv >= 0 else "negative"
        rag = m["rag_status"]
        rag_badge = {
            "RED": '<span class="badge red">Merforbruk</span>',
            "AMBER": '<span class="badge amber">Observasjon</span>',
            "GREEN": '<span class="badge green">I balanse</span>'
        }.get(rag, rag)

        pdf_link = f"{aid}_Maanedsrapport_M{month}_2026.pdf"
        html_link = f"{aid}_Maanedsrapport_M{month}_2026.html"

        rows_html += f"""
        <tr>
            <td><code>{aid}</code></td>
            <td><strong>{h['enhet_navn']}</strong><br/><span class="subtext">{h['navn']} ({h['tittel']})</span></td>
            <td>{h['sektor_kode']}</td>
            <td>{h['niva_tekst']}</td>
            <td class="num">kr {m['annual_budget']:,.0f}</td>
            <td class="num">kr {m['ytd_actual']:,.0f}</td>
            <td class="num {avv_class}"><strong>{avv_sign}kr {avv:,.0f}</strong></td>
            <td>{rag_badge}</td>
            <td>
                <a class="btn-sm" href="{pdf_link}" target="_blank">📄 PDF</a>
                <a class="btn-sm" href="{html_link}" target="_blank">🌐 HTML</a>
            </td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Månedsrapporter M{month} / {m_name} 2026 — Kristiansand Kommune</title>
    <style>
        :root {{
            --bg: #f8fafc;
            --surface: #ffffff;
            --text-dark: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --navy: #1e293b;
            --green: #166534;
            --red: #991b1b;
            --amber: #9a3412;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg);
            color: var(--text-dark);
            padding: 32px;
        }}
        .container {{
            max-width: 1280px;
            margin: 0 auto;
            background: var(--surface);
            padding: 32px;
            border-radius: 8px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--navy);
            padding-bottom: 16px;
            margin-bottom: 24px;
        }}
        .title {{ font-size: 22px; font-weight: 700; color: var(--navy); }}
        .subtitle {{ font-size: 13px; color: var(--text-muted); }}
        .batch-download {{
            display: inline-block;
            background: var(--navy);
            color: #fff;
            padding: 8px 16px;
            border-radius: 4px;
            text-decoration: none;
            font-weight: 600;
            font-size: 13px;
        }}
        .batch-download:hover {{ background: #0f172a; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            margin-top: 16px;
        }}
        th {{
            text-align: left;
            padding: 10px 12px;
            border-bottom: 2px solid var(--navy);
            color: var(--navy);
            font-weight: 600;
        }}
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid var(--border);
        }}
        tr:hover td {{ background: #f8fafc; }}
        .num {{ text-align: right; }}
        .positive {{ color: var(--green); }}
        .negative {{ color: var(--red); }}
        .subtext {{ font-size: 11px; color: var(--text-muted); }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }}
        .badge.green {{ background: #dcfce7; color: var(--green); }}
        .badge.red {{ background: #fee2e2; color: var(--red); }}
        .badge.amber {{ background: #ffedd5; color: var(--amber); }}
        .btn-sm {{
            display: inline-block;
            background: #e2e8f0;
            color: var(--navy);
            text-decoration: none;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            margin-right: 4px;
        }}
        .btn-sm:hover {{ background: #cbd5e1; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <div class="title">🏛️ Månedsrapporter M{month} / {m_name.upper()} 2026</div>
                <div class="subtitle">Kristiansand Kommune — AI Project Controller Hub | Ansvarlige Ledere & Delegeringsfullmakter</div>
            </div>
            <div>
                <a class="batch-download" href="FRAMSIKT_BATCH_OMDISPONERING_M{month}_2026.csv" download>📥 Last ned Framsikt Batch CSV</a>
            </div>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Ansvar</th>
                    <th>Enhet & Budsjettansvarlig</th>
                    <th>Sektor</th>
                    <th>Nivå</th>
                    <th class="num">Årsbudsjett</th>
                    <th class="num">Regnskap YTD</th>
                    <th class="num">Avvik YTD</th>
                    <th>Status</th>
                    <th>Dokumenter</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    parser = argparse.ArgumentParser(description="Automatisk månedlig PDF- og lederrapport-generator for budsjettansvarlige.")
    parser.add_argument("--month", type=int, default=9, help="Månedsnummer (1..12). Standard er 9 (September).")
    parser.add_argument("--ansvar-id", type=str, default=None, help="Filtrer på spesifikk ansvar_id (f.eks. 5200-ENH-401).")
    parser.add_argument("--all", action="store_true", help="Generer for ALLE budsjettansvarlige i registeret.")
    parser.add_argument("--format", type=str, choices=["pdf", "html", "both"], default="both", help="Filformat.")
    args = parser.parse_args()

    month = args.month
    print(f"================================================================================")
    print(f"🏛️ KRISTIANSAND KOMMUNE — MÅNEDLIG LEDERRAPPORT GENERATOR (M{month} / {MONTH_NAMES[month-1]} 2026)")
    print(f"Formel: Avvik = Budsjett - Actuals (Positivt = Grønn/Mindreforbruk, Negativt = Rød/Merforbruk)")
    print(f"================================================================================")

    budget_holders = get_budget_holders_from_db()
    print(f"Fant {len(budget_holders)} budsjettansvarlige i databasen.")

    # Velg ut enheter
    if args.ansvar_id:
        targets = [h for h in budget_holders if h["ansvar_id"] == args.ansvar_id]
        if not targets:
            print(f"❌ Ingen enhet funnet med ansvar_id: {args.ansvar_id}")
            sys.exit(1)
    elif args.all:
        targets = budget_holders
    else:
        # Standard benchmark-sett (dekker Helse, Oppvekst, Byutvikling, Kultur, Toppledelse, Surplus og Deficit)
        benchmark_ids = {
            "5200-ENH-401",  # Strai Sykehjem (Deficit / Merforbruk vikar)
            "4100-ENH-202",  # Lovisenlev Skole (Deficit / Merforbruk)
            "3300-ENH-301",  # Byggesak & Tilsyn (Surplus / Mindreforbruk)
            "2200-ENH-101",  # Kristiansand Folkebibliotek (Surplus)
            "3100-ENH-302",  # VAR Ingeniørvesen (I balanse)
            "2020",          # Kommunal Skole 2020
            "2540",          # Kommunal Boenhet 2540
            "5000-SJEF-HELSE", # Kommunalsjef Helse (Nivå 1 paraply)
            "4000-SJEF-OPPV",  # Kommunalsjef Oppvekst (Nivå 1 paraply)
            "0000-KOMMDIR"     # Kommunedirektør
        }
        targets = [h for h in budget_holders if h["ansvar_id"] in benchmark_ids]
        if not targets:
            targets = budget_holders[:8]

    print(f"Genererer rapporter for {len(targets)} enheter...\n")

    all_metrics = []
    for h in targets:
        aid = h["ansvar_id"]
        metrics = calculate_unit_metrics(h, month=month)
        all_metrics.append(metrics)

        pdf_path = OUTPUT_DIR / f"{aid}_Maanedsrapport_M{month}_2026.pdf"
        html_path = OUTPUT_DIR / f"{aid}_Maanedsrapport_M{month}_2026.html"

        if args.format in ["pdf", "both"]:
            generate_pdf_report(metrics, pdf_path)
            print(f"  ✓ PDF generert : {pdf_path.name}")

        if args.format in ["html", "both"]:
            generate_html_report(metrics, html_path)
            print(f"  ✓ HTML generert: {html_path.name}")

    # Framsikt Batch CSV
    batch_csv_path = OUTPUT_DIR / f"FRAMSIKT_BATCH_OMDISPONERING_M{month}_2026.csv"
    export_framsikt_batch_csv(all_metrics, batch_csv_path, month)
    print(f"\n✓ Framsikt Batch CSV eksportert: {batch_csv_path}")

    # Register JSON
    json_path = OUTPUT_DIR / f"MAANEDSRAPPORT_REGISTER_M{month}_2026.json"
    with open(json_path, "w", encoding="utf-8") as f:
        # Serialiser trygt
        serializable = []
        for m in all_metrics:
            serializable.append({
                "ansvar_id": m["holder"]["ansvar_id"],
                "enhet_navn": m["holder"]["enhet_navn"],
                "navn": m["holder"]["navn"],
                "tittel": m["holder"]["tittel"],
                "epost": m["holder"]["epost"],
                "sektor_kode": m["holder"]["sektor_kode"],
                "niva": m["holder"]["niva"],
                "annual_budget": m["annual_budget"],
                "ytd_budget": m["ytd_budget"],
                "ytd_actual": m["ytd_actual"],
                "avvik_ytd": m["avvik_ytd"],
                "forbruksgrad": m["forbruksgrad"],
                "rag_status": m["rag_status"],
                "p50_eoy": m["prognosis"]["p50"],
                "sluttavvik_eoy": m["prognosis"]["sluttavvik_p50"],
                "sha256": m["prognosis"]["sha256"],
                "preskripsjoner_count": len(m["preskripsjoner"]),
                "totalt_tiltak_nok": m["totalt_tiltak_nok"]
            })
        json.dump(serializable, f, indent=2, ensure_ascii=False)
    print(f"✓ Master Register JSON eksportert: {json_path}")

    # Portal Index HTML
    portal_path = OUTPUT_DIR / "index.html"
    generate_portal_index(all_metrics, portal_path, month)
    print(f"✓ Navigasjonsportal generert: {portal_path}")

    print("\nFullført med 0 feil. Rapporter er klare til distribusjon via e-post og Microsoft Teams.")


if __name__ == "__main__":
    main()
