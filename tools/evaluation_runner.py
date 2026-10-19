# -*- coding: utf-8 -*-
"""
Evaluation & QA Runner CLI (Agent 13)
Usage:
    python tools/evaluation_runner.py --golden
    python tools/evaluation_runner.py --gate
    python tools/evaluation_runner.py --json
"""

import sys
import argparse
import json
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from app.services.evaluation_service import EvaluationService


def main():
    parser = argparse.ArgumentParser(
        description="Agent 13: Evaluation & Quality Assurance Runner for Kommune AI"
    )
    parser.add_argument(
        "--golden", action="store_true", help="Kjør evaluering mot Golden Dataset"
    )
    parser.add_argument(
        "--gate", action="store_true", help="Valider og håndhev 90 %% CI/CD kvalitetsport"
    )
    parser.add_argument(
        "--include-exemplars", action="store_true", help="Inkluder godkjente HITL gulleksempler fra SQLite"
    )
    parser.add_argument(
        "--sync-exemplars", action="store_true", help="Synkroniser og berik golden_evaluation_dataset.json fra SQLite"
    )
    parser.add_argument(
        "--json", action="store_true", help="Skriv ut rapport som formatert JSON"
    )

    args = parser.parse_args()
    svc = EvaluationService()

    if args.sync_exemplars:
        synced = svc.sync_exemplars_to_golden_file()
        if args.json:
            print(json.dumps({"synced_exemplars": synced, "ok": True}))
        else:
            print(f"[*] Synkroniserte {synced} nye HITL gulleksempler inn i golden_evaluation_dataset.json.")
        if not args.golden and not args.gate:
            sys.exit(0)

    # Standard er å kjøre golden suite
    report = svc.run_golden_suite(include_exemplars=args.include_exemplars)

    if args.gate:
        try:
            svc.enforce_ci_cd_gate(report)
            gate_status = "PASSED (>= 90 % Factual Consistency)"
            exit_code = 0
        except ValueError as e:
            gate_status = f"FAILED: {e}"
            exit_code = 1
    else:
        gate_status = "PASSED" if report.ci_cd_gate_passed else "FAILED"
        exit_code = 0

    if args.json:
        print(json.dumps(report.model_dump(), indent=2, ensure_ascii=False))
        sys.exit(exit_code)

    # Edward Tufte Data-Ink ASCII Dashboard
    print("\n" + "=" * 80)
    print("🏛️ KRISTIANSAND KOMMUNE — AGENT 13 EVALUATION & QA RUNNER (CI/CD GATE)")
    print("=" * 80)
    print(f"Kjørings-ID:            {report.run_id}")
    print(f"Tidsstempel:            {report.timestamp}")
    print(f"Testtilfeller i Golden: {report.total_tests}")
    print(f"Beståtte tester:        {report.passed_tests} / {report.total_tests}")
    print(f"Samlet Troverdighet:    {report.overall_faithfulness * 100:.1f} % (Minstekrav: 90.0 %)")
    print(f"Gjenfinningspresisjon:  {report.overall_precision * 100:.1f} %")
    print(f"CI/CD Port Status:      {gate_status}")
    print(f"SHA-256 Audit Seal:     {report.sha256_seal}")
    print("-" * 80)
    print(f"{'Test ID':<12} {'Kategori':<12} {'Troverdighet':<15} {'Recall@k':<12} {'Status'}")
    print("-" * 80)

    for res in report.results:
        status_sym = "🟢 BESTÅTT" if res["passed"] else "🔴 FEIL"
        print(
            f"{res['test_id']:<12} {res['category']:<12} "
            f"{res['faithfulness']*100:>6.1f} %         "
            f"{res['recall_at_k']*100:>6.1f} %     "
            f"{status_sym}"
        )

    print("=" * 80 + "\n")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
