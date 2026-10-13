#!/usr/bin/env python3
"""
Prescriptive AI Agent: Integrates with local Ollama to evaluate and rank
candidate mitigation measures with risk scoring and governance gates.
"""

import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Any

try:
    from config import OLLAMA_BASE_URL, DEFAULT_OLLAMA_MODEL
    from eac_forecasting import compute_eac_forecasts
except ImportError:
    from mvp_pilot.config import OLLAMA_BASE_URL, DEFAULT_OLLAMA_MODEL
    from mvp_pilot.eac_forecasting import compute_eac_forecasts


# Standard baseline tiltak fra Excel (T1 - T6)
DEFAULT_CANDIDATE_MEASURES = [
    {
        "id": "T1",
        "title": "Oppfølging refusjoner og inntektskrav",
        "horizon": "Kort",
        "effect_base": 732705.0,
        "rate": 0.08,
        "probability": 0.85,
        "eoy_effect": 41323.94,
        "service_risk": 0.05,
        "hr_tariff_risk": 0.05,
        "governance_need": "KREVER FAGKONTROLL",
        "annual_effect": 41323.94,
        "next_step": "Avstem refusjonskrav mot grunnlagsbilag; fagkontroll før inndriving."
    },
    {
        "id": "T2",
        "title": "Redusere unødvendig vikarbruk via intern dekning",
        "horizon": "Kort",
        "effect_base": 612450.15,
        "rate": 0.10,
        "probability": 0.70,
        "eoy_effect": 28871.51,
        "service_risk": 0.15,
        "hr_tariff_risk": 0.25,
        "governance_need": "KREVER HR/TARIFF",
        "annual_effect": 28871.51,
        "next_step": "Analyser turnus og ledig intern kapasitet; HR/tariff og tjenestekvalitet må godkjenne."
    },
    {
        "id": "T3",
        "title": "Redusere overtid gjennom planlegging",
        "horizon": "Kort",
        "effect_base": 1105443.81,
        "rate": 0.08,
        "probability": 0.75,
        "eoy_effect": 55076.63,
        "service_risk": 0.15,
        "hr_tariff_risk": 0.25,
        "governance_need": "KREVER HR/TARIFF",
        "annual_effect": 55076.63,
        "next_step": "Gjennomgå overtidsårsaker og arbeidsplan; avklar HR/tariff og HMS."
    },
    {
        "id": "T4",
        "title": "Kontroll av ikke-kritiske kjøp",
        "horizon": "Kort",
        "effect_base": 155776.0,
        "rate": 0.10,
        "probability": 0.90,
        "eoy_effect": 9519.84,
        "service_risk": 0.10,
        "hr_tariff_risk": 0.05,
        "governance_need": "KREVER FAGKONTROLL",
        "annual_effect": 9519.84,
        "next_step": "Gjennomgå innkjøpslinjer og avtaler; faglig vurdering før endring."
    },
    {
        "id": "T5",
        "title": "Turnus- og kapasitetsanalyse",
        "horizon": "Lang",
        "effect_base": 4789478.56,
        "rate": 0.02,
        "probability": 0.60,
        "eoy_effect": 27473.74,
        "service_risk": 0.10,
        "hr_tariff_risk": 0.25,
        "governance_need": "KREVER HR/TARIFF",
        "annual_effect": 48079.05,
        "next_step": "Utarbeid kapasitets- og turnusanalyse; HR/tariff og tjenesteleder vurderer."
    },
    {
        "id": "T6",
        "title": "Digital oppfølging og planprosess",
        "horizon": "Lang",
        "effect_base": 17233691.0,
        "rate": 0.005,
        "probability": 0.60,
        "eoy_effect": 30701.07,
        "service_risk": 0.05,
        "hr_tariff_risk": 0.05,
        "governance_need": "KREVER FAGKONTROLL",
        "annual_effect": 42981.50,
        "next_step": "Test digital oppfølgingsprosess i liten skala; fagkontroll og gevinstmåling."
    }
]


def call_ollama(prompt: str, model: str = DEFAULT_OLLAMA_MODEL, timeout_sec: int = 60) -> str:
    """Kaller lokal Ollama-instans via HTTP REST API."""
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 256
        }
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            return res_json.get("response", "")
    except Exception as e:
        print(f"[Prescriptive Agent] Ollama advarsel: {e}. Bruker heuristisk regelmotor.")
        return ""


def evaluate_measures_with_ai(model_name: str = DEFAULT_OLLAMA_MODEL) -> List[Dict[str, Any]]:
    """
    Kjører analyse av kandidattiltakene basert på driverne og lokal LLM-vurdering.
    """
    forecast_data = compute_eac_forecasts()
    top_drivers = forecast_data.get("top_drivers", [])
    
    drivers_summary = "\n".join([
        f"- Art {d['art']} ({d['navn']}): YTD-merforbruk {d['ytd_merforbruk']:,.0f} kr, mnd-snitt {d['mnd_snitt']:,.0f} kr"
        for d in top_drivers
    ])

    prompt = f"""Du er en erfaren kommunal økonomirådgiver og controller for Kristiansand kommune.
Vurder følgende avviksdrivere for Bo og Miljø (funksjon 254):
{drivers_summary}

Kandidattiltak:
- T1: Oppfølging av refusjoner (NAV sykelønn).
- T2: Redusere unødvendig vikarbruk via intern dekning (krever HTA § 4 drøfting).
- T3: Redusere overtid gjennom planlegging (krever AML § 10-6 og tariffkontroll).
- T4: Innkjøpskontroll på ikke-kritiske driftskjøp.
- T5: Turnus- og kapasitetsanalyse (strukturelt tiltak).
- T6: Digital plan- og oppfølgingsprosess.

Gi en kort, konsis vurdering (maks 3 setninger) av hvilke to tiltak som bør prioriteres først for raskest EOY-effekt uten å svekke forsvarlig bemanning.
"""

    llm_assessment = call_ollama(prompt, model=model_name)

    evaluated_measures = []
    for m in DEFAULT_CANDIDATE_MEASURES:
        measure = dict(m)
        # Beregn risikovektet netto nyttefaktor
        risk_penalty = 1.0 - (measure["service_risk"] + measure["hr_tariff_risk"])
        measure["net_score"] = round(measure["eoy_effect"] * measure["probability"] * risk_penalty, 2)
        measure["status"] = "Kandidat"
        measure["control_documented"] = "Nei"
        measure["approved_effect"] = 0.0
        measure["decision_signal"] = "RØD"
        evaluated_measures.append(measure)

    # Sorter etter nettoscore (høyest effekt med lavest risiko først)
    evaluated_measures.sort(key=lambda x: x["net_score"], reverse=True)

    return {
        "llm_commentary": llm_assessment.strip() if llm_assessment else "Prioriter T1 (refusjoner) og T3 (overtidsstyring) for umiddelbar kontanteffekt før T2 (vikarer) drøftes iht. HTA § 4.",
        "measures": evaluated_measures
    }


if __name__ == "__main__":
    result = evaluate_measures_with_ai()
    print("=" * 65)
    print("PRESCRIPTIVE AI TILTAKSMENY (KANDIDATER)")
    print("=" * 65)
    print(f"AI Vurdering:\n{result['llm_commentary']}\n")
    print("-" * 65)
    for m in result["measures"]:
        print(f"[{m['id']}] {m['title']:<38} EOY: {m['eoy_effect']:8,.0f} kr | Netto: {m['net_score']:8,.0f} | {m['governance_need']}")
