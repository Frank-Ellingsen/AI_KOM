#!/usr/bin/env python3
"""
Kristiansand Kommune — Triage Router CLI
Kommandolinjeverktøy for å teste og rute henvendelser via Fast-Path Triage Router.
"""

import sys
import json
import argparse
from pathlib import Path

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

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.schemas.triage import TriageRequest
from app.core.triage_router import TriageRouter


def main():
    parser = argparse.ArgumentParser(description="Kristiansand Kommune — Triage Router CLI")
    parser.add_argument("prompt", nargs="?", default="Hva sier Kommuneloven § 14-5 om overskridelse av årsbudsjett?", help="Brukerhenvendelse")
    parser.add_argument("--session", default="cli-session-001", help="Økt-ID")
    parser.add_argument("--persona", default="CONTROLLER", help="Aktiv persona (CONTROLLER, ENHETSLEDER, TOPPLEDELSE)")
    parser.add_argument("--unit", default="2020", help="Aktiv enhets-ID")
    parser.add_argument("--period", default="M10_2026", help="Regnskapsperiode")
    parser.add_argument("--json", action="store_true", help="Skriv ut resultat som rå JSON")

    args = parser.parse_args()

    router = TriageRouter()
    req = TriageRequest(
        prompt=args.prompt,
        session_id=args.session,
        user_persona=args.persona,
        active_unit_id=args.unit,
        active_period=args.period
    )

    decision = router.classify_and_route_sync(req)

    if args.json:
        print(decision.model_dump_json(indent=2))
    else:
        print("=" * 70)
        print("🏛️  KRISTIANSAND KOMMUNE — FAST-PATH TRIAGE ROUTER BESLUTNING")
        print("=" * 70)
        print(f"Kategori:           {decision.primary_category.value}")
        print(f"Konfidens:          {decision.confidence_score * 100:.1f} %")
        print(f"Prioritet:          {decision.priority.value}")
        print(f"Begrunnelse:        {decision.reasoning_trace}")
        if decision.required_mcp_connectors:
            print(f"MCP-konnektorer:    {', '.join(decision.required_mcp_connectors)}")
        if decision.rag_search_filters:
            print(f"RAG-filtre:         {decision.rag_search_filters}")
        if decision.skill_workflow_target:
            print(f"Skill-mål:          {decision.skill_workflow_target}")
        print(f"SHA-256 Sjekksum:   {decision.sha256_audit_hash}")
        print("=" * 70)


if __name__ == "__main__":
    main()
