# -*- coding: utf-8 -*-
"""
AI Engineering & Infrastructure Runner CLI (Agent 15)
Usage:
    python tools/ai_engineering_runner.py --status
    python tools/ai_engineering_runner.py --compact "Kommuneloven § 14-5 stiller krav..."
    python tools/ai_engineering_runner.py --benchmark
    python tools/ai_engineering_runner.py --cache-stats
    python tools/ai_engineering_runner.py --json
"""

import sys
import argparse
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from app.services.ai_engineering_service import AIEngineeringService
from app.schemas.ai_engineering import ContextCompactionRequest


def main():
    parser = argparse.ArgumentParser(
        description="Agent 15: AI Engineering & Infrastructure Runner for Kommune AI"
    )
    parser.add_argument(
        "--status", action="store_true", help="Vis helsestatus for de 4 arkitekturlagene"
    )
    parser.add_argument(
        "--compact", type=str, help="Kjør kontekstkomprimering og bevaring av lovhenvisninger"
    )
    parser.add_argument(
        "--benchmark", action="store_true", help="Mål inferenslatens, TTFT og tokengjennomstrømming"
    )
    parser.add_argument(
        "--cache-stats", action="store_true", help="Vis statistikk og besparelser for semantisk cache"
    )
    parser.add_argument(
        "--json", action="store_true", help="Skriv ut rapport som formatert JSON"
    )

    args = parser.parse_args()
    svc = AIEngineeringService()

    if args.compact:
        req = ContextCompactionRequest(raw_context=args.compact)
        res = svc.compact_context(req)
        if args.json:
            print(json.dumps(res.model_dump(), indent=2, ensure_ascii=False))
        else:
            print("\n" + "=" * 80)
            print("🏛️ KRISTIANSAND KOMMUNE — AGENT 15 CONTEXT COMPACTION")
            print("=" * 80)
            print(f"Opprinnelige tegn:  {res.original_chars}")
            print(f"Komprimerte tegn:   {res.compacted_chars}")
            print(f"Komprimeringsrate:  {res.compression_ratio * 100:.1f} %")
            print(f"Funnet lovhenvisn.: {', '.join(res.extracted_statutes) if res.extracted_statutes else 'Ingen'}")
            print("-" * 80)
            print("Komprimert tekst:")
            print(res.compacted_text)
            print("=" * 80 + "\n")
        return

    if args.benchmark:
        bench = svc.benchmark_latency()
        if args.json:
            print(json.dumps(bench.model_dump(), indent=2, ensure_ascii=False))
        else:
            print("\n" + "=" * 80)
            print("🏛️ KRISTIANSAND KOMMUNE — AGENT 15 INFERENCE LATENCY BENCHMARK")
            print("=" * 80)
            print(f"Modell:                 {bench.model_name}")
            print(f"Time-To-First-Token:    {bench.time_to_first_token_ms} ms")
            print(f"Total Latens:           {bench.total_latency_ms} ms")
            print(f"Genererte Tokens:       {bench.tokens_generated}")
            print(f"Gjennomstrømming:       {bench.tokens_per_second:.1f} tokens/sekund")
            print(f"Estimert Tokenkostnad:  {bench.token_cost_nok:.6f} NOK")
            print("=" * 80 + "\n")
        return

    if args.cache_stats:
        stats = svc.cache.get_stats()
        if args.json:
            print(json.dumps(stats.model_dump(), indent=2, ensure_ascii=False))
        else:
            print("\n" + "=" * 80)
            print("🏛️ KRISTIANSAND KOMMUNE — AGENT 15 SEMANTIC CACHE TELEMETRY")
            print("=" * 80)
            print(f"Cache-oppføringer:      {stats.total_entries}")
            print(f"Cache Hits:             {stats.cache_hits}")
            print(f"Cache Misses:           {stats.cache_misses}")
            print(f"Treffrate:              {stats.hit_rate_pct:.1f} %")
            print(f"Innsparer tokens:       {stats.saved_tokens}")
            print(f"Estimert besparelse:    {stats.estimated_cost_saved_nok:.4f} NOK")
            print("=" * 80 + "\n")
        return

    # Standard visning: 4-layer status
    status = svc.get_4_layer_status()
    if args.json:
        print(json.dumps(status.model_dump(), indent=2, ensure_ascii=False))
    else:
        print("\n" + "=" * 80)
        print("🏛️ KRISTIANSAND KOMMUNE — AGENT 15 AI ENGINEERING 4-LAYER HARNESS")
        print("=" * 80)
        print("1. MODEL LAYER (Foundation Models):")
        for k, v in status.model_layer.items():
            print(f"   • {k:<15}: {v}")
        print("\n2. HARNESS LAYER (Sandboxing & Execution):")
        for k, v in status.harness_layer.items():
            print(f"   • {k:<15}: {v}")
        print("\n3. FRAMEWORK LAYER (Multi-Agent Orchestration):")
        for k, v in status.framework_layer.items():
            print(f"   • {k:<15}: {v}")
        print("\n4. PLATFORM LAYER (Governance & Stage-Gate Port 9):")
        for k, v in status.platform_layer.items():
            print(f"   • {k:<15}: {v}")
        print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
