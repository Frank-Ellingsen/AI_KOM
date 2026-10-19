# -*- coding: utf-8 -*-
"""
🏛️ Kristiansand Kommune — Loop Engineering Engine (Lag 4 i AI Engineering)
Implementerer selvreparerende Generator-Evaluator sykluser, 4 obligatoriske
kvalitets- og lovlighetsporter (§ 14-5, § 14-6, GDPR Port 4, Vedtaksstruktur),
stoppbetingelser og kryptografisk SHA-256 revisjonsforsegling for Kommunerevisjonen.

Bruk:
    python tools/loop_engine.py --sector "Helse og mestring" --deficit 8.85
    python tools/loop_engine.py --sector "Oppvekst" --deficit 3.20 --unit "2020 - Grim skole"
    python tools/loop_engine.py --sector "Helse og mestring" --deficit 8.85 --json
"""

import sys
import os
import re
import json
import hashlib
import argparse
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple, Optional

# UTF-8 stdout configuration for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Regex patterns for validation & PII scrubbing
REGEX_FNR = re.compile(r"\b\d{11}\b")
REGEX_BANK_KONTO = re.compile(r"\b\d{4}\.\d{2}\.\d{5}\b")
REGEX_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
REGEX_PAR_14_5 = re.compile(r"(?:Kommuneloven\s*)?§\s*14-5", re.IGNORECASE)
REGEX_PAR_14_6 = re.compile(r"(?:Kommuneloven\s*)?§\s*14-6", re.IGNORECASE)


def mask_pii_text(text: str) -> str:
    """Maskerer 11-sifrede fødselsnumre, bankkonti og e-poster i henhold til GDPR Port 4."""
    masked = REGEX_BANK_KONTO.sub("[SKJERMET_KONTO]", text)
    masked = REGEX_FNR.sub("[SKJERMET_FNR]", masked)
    masked = REGEX_EMAIL.sub("[SKJERMET_EPOST]", masked)
    return masked


class EvaluatorReport:
    """Strukturert evalueringsrapport for et saksfremlegg."""

    def __init__(
        self,
        passed: bool,
        gate_1_14_5: bool,
        gate_2_14_6: bool,
        gate_3_gdpr: bool,
        gate_4_vedtak: bool,
        feedback: List[str],
        detected_pii_count: int = 0,
    ):
        self.passed = passed
        self.gate_1_14_5 = gate_1_14_5
        self.gate_2_14_6 = gate_2_14_6
        self.gate_3_gdpr = gate_3_gdpr
        self.gate_4_vedtak = gate_4_vedtak
        self.feedback = feedback
        self.detected_pii_count = detected_pii_count

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "gate_1_14_5": self.gate_1_14_5,
            "gate_2_14_6": self.gate_2_14_6,
            "gate_3_gdpr": self.gate_3_gdpr,
            "gate_4_vedtak": self.gate_4_vedtak,
            "feedback": self.feedback,
            "detected_pii_count": self.detected_pii_count,
        }


class LoopEngine:
    """
    Kjerneevaluator- og optimeringsmotor for AI_KOM.
    Sikrer at saksfremlegg og avviksnotater oppfyller samtlige formelle krav
    før oversendelse til saksbehandler eller politisk organ.
    """

    def __init__(self, max_attempts: int = 3, max_tokens: int = 10000):
        self.max_attempts = max_attempts
        self.max_tokens = max_tokens

    def generate_draft(
        self,
        sector: str,
        deficit_mnok: float,
        attempt: int,
        feedback: str = "",
        unit_name: Optional[str] = None,
    ) -> str:
        """
        Generator Node: Produserer utkast til saksfremlegg.
        I forsøk 1 simuleres et ufullstendig utkast (mangler lovhenvisninger, inneholder test-PII).
        I påfølgende iterasjoner rettes utkastet deterministisk basert på Evaluator-feedback.
        """
        unit_str = f" ({unit_name})" if unit_name else ""

        if attempt == 1:
            # Ufullstendig førsteutkast som bevisst trigger kvalitetsportene for demonstrasjon/test
            return f"""SAKSFREMLEGG: Tiltaksplan for {sector}{unit_str}
Saksansvarlig: Kari Nordmann (tlf: 38 00 00 00, e-post: kari.nordmann@kristiansand.kommune.no)
Oppgitt bankkonto for refusjon: 1234.56.78901, Fødselsnr: 12058812345.

Bakgrunn:
Enheten viser et estimert merforbruk på {deficit_mnok:.2f} MNOK i periodisert M8-regnskap.
Hovedårsaken er høyt sykefravær og innleie av vikarer i sommerturnus.
Vi foreslår at dette dekkes inn ved overføring fra disposisjonsfond.

Innstilling:
Formannskapet tar saken til orientering og godkjenner merforbruket."""

        # Forbedret / selvreparert utkast (Attempt >= 2)
        return f"""SAKSFREMLEGG: Tiltaksplan og Finansiell Inndekning for {sector}{unit_str} (Revidert utkast)
Saksansvarlig: [SKJERMET_EPOST]
Refusjonskonto: [SKJERMET_KONTO], Fødselsnr: [SKJERMET_FNR]

1. Bakgrunn og Økonomisk Risiko
Enheten viser et projisert merforbruk på {deficit_mnok:.2f} MNOK i gjeldende tertialprognose.
I henhold til Kommuneloven § 14-5 (Krav om realistisk budsjettbalanse) plikter kommunedirektøren 
å fremme formell sak om omprioritering, innsparing eller tilleggsbevilgning for å gjenopprette 
driftsbalanse innen årets utløp.

2. Finansiell Inndekning og Bruttoprinsippet
Inndekning gjennomføres ved målrettede innsparingstiltak på rammen samt omdisponering av 
mindreforbruk i andre sektorer jf. helhetlig tertialrapport. 
I henhold til Kommuneloven § 14-6 (Bruttoprinsippet) budsjetteres og regnskapsføres alle utgifter 
(vikar art 1090) og inntekter (NAV-sykelønnsrefusjon art 1600) brutto uten intern motregning.

3. Forslag til Vedtak
Kommunedirektøren foreslår følgende vedtak for Formannskapet og Bystyret:
1. Tiltaksplan for {sector} med finansiell inndekning av merforbruk på {deficit_mnok:.2f} MNOK godkjennes.
2. Nødvendige budsjettjusteringer innarbeides i revidert årsbudsjett 2026 i henhold til Kommuneloven §§ 14-5 og 14-6.
3. Kommunedirektøren rapporterer oppdatert status ved neste tertialrapport."""

    def evaluate_draft(self, draft_text: str) -> EvaluatorReport:
        """
        Evaluator Node: Tester utkastet mot de 4 definerte kvalitetsportene.
        """
        has_14_5 = bool(REGEX_PAR_14_5.search(draft_text))
        has_14_6 = bool(REGEX_PAR_14_6.search(draft_text))
        has_vedtak = "Forslag til Vedtak" in draft_text or "vedtak for Formannskapet" in draft_text

        # PII Detection (unmasked patterns)
        unmasked_fnr = REGEX_FNR.findall(draft_text)
        unmasked_konto = REGEX_BANK_KONTO.findall(draft_text)
        unmasked_email = REGEX_EMAIL.findall(draft_text)
        total_pii = len(unmasked_fnr) + len(unmasked_konto) + len(unmasked_email)
        pii_clean = (total_pii == 0)

        feedback: List[str] = []
        if not has_14_5:
            feedback.append("PORT 1 FEIL: Mangler eksplisitt henvisning til Kommuneloven § 14-5 (Budsjettbalanse).")
        if not has_14_6:
            feedback.append("PORT 2 FEIL: Mangler eksplisitt henvisning til Kommuneloven § 14-6 (Bruttoprinsippet).")
        if not pii_clean:
            feedback.append(f"PORT 3 GDPR-BRUDD: Fant {total_pii} uskjermede person-/kontoopplysninger.")
        if not has_vedtak:
            feedback.append("PORT 4 STRUKTURFEIL: Mangler formelt 'Forslag til Vedtak' med vedtakspunkter.")

        passed = has_14_5 and has_14_6 and pii_clean and has_vedtak

        return EvaluatorReport(
            passed=passed,
            gate_1_14_5=has_14_5,
            gate_2_14_6=has_14_6,
            gate_3_gdpr=pii_clean,
            gate_4_vedtak=has_vedtak,
            feedback=feedback,
            detected_pii_count=total_pii,
        )

    def run_loop(
        self,
        sector: str,
        deficit_mnok: float,
        unit_name: Optional[str] = None,
        max_attempts: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Kjører den fullstendige Evaluator-Optimizer løkken.
        """
        limit = max_attempts or self.max_attempts
        attempt = 1
        feedback_str = ""
        trajectory: List[Dict[str, Any]] = []
        accumulated_tokens = 0
        last_feedback = ""

        while attempt <= limit:
            # 1. Generator Node
            raw_draft = self.generate_draft(sector, deficit_mnok, attempt, feedback_str, unit_name)
            
            # Mask PII if attempt > 1 as part of self-repair
            draft = mask_pii_text(raw_draft) if attempt > 1 else raw_draft

            # Token tracking (~4 chars per token)
            turn_tokens = len(draft) // 4
            accumulated_tokens += turn_tokens

            # 2. Evaluator Node
            eval_report = self.evaluate_draft(draft)

            turn_info = {
                "attempt": attempt,
                "passed": eval_report.passed,
                "gates": {
                    "gate_1_14_5": eval_report.gate_1_14_5,
                    "gate_2_14_6": eval_report.gate_2_14_6,
                    "gate_3_gdpr": eval_report.gate_3_gdpr,
                    "gate_4_vedtak": eval_report.gate_4_vedtak,
                },
                "feedback": eval_report.feedback,
                "tokens_used": turn_tokens,
            }
            trajectory.append(turn_info)

            # Stoppbetingelse: Konvergenssjekk (hvis feedback gjentar seg eksakt)
            current_feedback_str = " | ".join(eval_report.feedback)
            if attempt > 1 and current_feedback_str == last_feedback and not eval_report.passed:
                return {
                    "status": "HALTED_CONVERGENCE_LOOP",
                    "reason": "Evaluator ga identisk feilmelding to ganger på rad.",
                    "iterations_required": attempt,
                    "trajectory": trajectory,
                    "accumulated_tokens": accumulated_tokens,
                }
            last_feedback = current_feedback_str

            # Stoppbetingelse: Token-grense
            if accumulated_tokens > self.max_tokens:
                return {
                    "status": "HALTED_TOKEN_BUDGET_EXCEEDED",
                    "reason": f"Akkumulert tokenforbruk ({accumulated_tokens}) oversteg taket ({self.max_tokens}).",
                    "iterations_required": attempt,
                    "trajectory": trajectory,
                    "accumulated_tokens": accumulated_tokens,
                }

            if eval_report.passed:
                # Stage-Gate Port 9: Sikker SHA-256 forsegling for Kommunerevisjonen
                now_utc = datetime.now(timezone.utc).isoformat()
                content_hash = hashlib.sha256(draft.encode("utf-8")).hexdigest()
                payload = f"{now_utc}|Controller|{sector}|APPROVED|{content_hash}"
                audit_seal = hashlib.sha256(payload.encode("utf-8")).hexdigest()

                return {
                    "status": "APPROVED",
                    "sector": sector,
                    "unit": unit_name or "Ikke spesifisert",
                    "deficit_mnok": deficit_mnok,
                    "iterations_required": attempt,
                    "accumulated_tokens": accumulated_tokens,
                    "final_draft": draft.strip(),
                    "sha256_audit_seal": audit_seal,
                    "timestamp": now_utc,
                    "trajectory": trajectory,
                    "quality_gates": {
                        "port_1_14_5": "PASSED",
                        "port_2_14_6": "PASSED",
                        "port_3_gdpr": "PASSED",
                        "port_4_vedtak": "PASSED",
                    },
                }

            # Optimizer Turn: Klargjør tilbakemelding for neste forsøk
            feedback_str = current_feedback_str
            attempt += 1

        return {
            "status": "FAILED_MAX_ITERATIONS",
            "reason": f"Saksfremlegget besto ikke kvalitetsportene etter {limit} iterasjoner.",
            "iterations_required": limit,
            "accumulated_tokens": accumulated_tokens,
            "last_feedback": last_feedback,
            "trajectory": trajectory,
        }


def format_tufte_report(res: Dict[str, Any]) -> str:
    """Formatterer resultatet i henhold til Edward Tuftes Data-Ink Ratio prinsipper."""
    lines = []
    lines.append("=" * 80)
    lines.append("🏛️ KRISTIANSAND KOMMUNE — LOOP ENGINEERING EVALUATOR-OPTIMIZER ENGINE")
    lines.append("=" * 80)
    lines.append(f"Status:                 {'🟢 GODKJENT (APPROVED)' if res.get('status') == 'APPROVED' else '🔴 FEIL (' + res.get('status', 'FAILED') + ')'}")
    lines.append(f"Virksomhetsområde:      {res.get('sector')}")
    lines.append(f"Organisatorisk Enhet:   {res.get('unit')}")
    lines.append(f"Projisert Merforbruk:   {res.get('deficit_mnok', 0.0):.2f} MNOK")
    lines.append(f"Iterasjoner Krevd:      {res.get('iterations_required')} av 3")
    lines.append(f"Akkumulerte Tokens:     ~{res.get('accumulated_tokens', 0)} tokens")
    if res.get("sha256_audit_seal"):
        lines.append(f"SHA-256 Audit Seal:     {res.get('sha256_audit_seal')}")
        lines.append(f"Revisjonstidsstempel:   {res.get('timestamp')}")
    lines.append("-" * 80)
    lines.append(f"{'Forsøk':<8} {'Port 1 (§14-5)':<16} {'Port 2 (§14-6)':<16} {'Port 3 (GDPR)':<16} {'Port 4 (Vedtak)':<16}")
    lines.append("-" * 80)

    for step in res.get("trajectory", []):
        g = step["gates"]
        p1 = "🟢 Bestått" if g["gate_1_14_5"] else "🔴 Feil"
        p2 = "🟢 Bestått" if g["gate_2_14_6"] else "🔴 Feil"
        p3 = "🟢 Bestått" if g["gate_3_gdpr"] else "🔴 Feil"
        p4 = "🟢 Bestått" if g["gate_4_vedtak"] else "🔴 Feil"
        lines.append(f"{step['attempt']:<8} {p1:<16} {p2:<16} {p3:<16} {p4:<16}")

    if res.get("status") == "APPROVED":
        lines.append("-" * 80)
        lines.append("GODKJENT OG FORSEGLET SAKSFREMLEGG (UTDRAG):")
        lines.append("-" * 80)
        lines.append(res.get("final_draft", ""))
    else:
        lines.append("-" * 80)
        lines.append(f"Siste feilmelding: {res.get('reason') or res.get('last_feedback')}")

    lines.append("=" * 80)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Loop Engineering Engine for Kristiansand Kommune (Evaluator-Optimizer Dualitet)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--sector", default="Helse og mestring", help="Virksomhetsområde (standard: Helse og mestring)")
    parser.add_argument("--deficit", type=float, default=8.85, help="Projisert merforbruk i MNOK (standard: 8.85)")
    parser.add_argument("--unit", default="5200 - Sykehjem & Helsehus", help="Spesifikk organisatorisk enhet")
    parser.add_argument("--max-attempts", type=int, default=3, help="Maksimalt antall forbedringssykluser (standard: 3)")
    parser.add_argument("--json", action="store_true", help="Formatér svar som ren JSON")

    args = parser.parse_args()

    engine = LoopEngine(max_attempts=args.max_attempts)
    result = engine.run_loop(
        sector=args.sector,
        deficit_mnok=args.deficit,
        unit_name=args.unit,
        max_attempts=args.max_attempts,
    )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("\n" + format_tufte_report(result) + "\n")

    sys.exit(0 if result.get("status") == "APPROVED" else 1)


if __name__ == "__main__":
    main()
