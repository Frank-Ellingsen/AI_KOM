# -*- coding: utf-8 -*-
"""
Database & Data Engineering Runner CLI (Agent 14)
Usage:
    python tools/database_runner.py --inspect-schema [TABLE]
    python tools/database_runner.py --query "SELECT * FROM Dim_Enhet LIMIT 5"
    python tools/database_runner.py --explain "SELECT * FROM Dim_Enhet WHERE Enhet_ID='2020-101'"
    python tools/database_runner.py --hybrid-search "Vågsbygd Skole"
    python tools/database_runner.py --json
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

from app.services.database_agent_service import DatabaseAgentService
from app.schemas.database import QueryRequest


def main():
    parser = argparse.ArgumentParser(
        description="Agent 14: Database & Data Engineering Runner for Kommune AI"
    )
    parser.add_argument(
        "--inspect-schema", nargs="?", const="ALL", default=None,
        help="Inspiser tabellskjema, kolonner og indekser (oppgi tabellnavn eller la stå tom for alle)"
    )
    parser.add_argument(
        "--query", type=str, help="Kjør parametrisert SQL-spørring (Read-Only standard)"
    )
    parser.add_argument(
        "--explain", type=str, help="Kjør EXPLAIN QUERY PLAN og gi indeksråd"
    )
    parser.add_argument(
        "--hybrid-search", type=str, help="Kjør hybridsøk (Sparse FTS5 + Dense Vektor)"
    )
    parser.add_argument(
        "--hitl", action="store_true", help="Bekreft Human-in-the-Loop for skriveoperasjon"
    )
    parser.add_argument(
        "--limit", type=int, default=50, help="Maks antall rader (standard: 50)"
    )
    parser.add_argument(
        "--json", action="store_true", help="Skriv ut rapport som formatert JSON"
    )

    args = parser.parse_args()
    svc = DatabaseAgentService()

    if args.inspect_schema:
        tbl = None if args.inspect_schema == "ALL" else args.inspect_schema
        schema = svc.inspect_schema(tbl)
        if args.json:
            print(json.dumps(schema, indent=2, ensure_ascii=False))
        else:
            print("\n" + "=" * 80)
            print("🏛️ KRISTIANSAND KOMMUNE — AGENT 14 DATABASE SCHEMA INSPECTION")
            print("=" * 80)
            if tbl:
                print(f"Tabell: {schema.get('table')}")
                print("-" * 80)
                print(f"{'Kolonne':<30} {'Type':<15} {'Not Null':<12} {'Primærnøkkel'}")
                print("-" * 80)
                for col in schema.get("columns", []):
                    print(f"{col['name']:<30} {col['type']:<15} {str(col['notnull']):<12} {str(col['pk'])}")
                print("-" * 80)
                print("Indekser:")
                for idx in schema.get("indexes", []):
                    print(f"  - {idx['name']} (Unik: {idx['unique']})")
            else:
                print(f"Database: {schema.get('database')}")
                print(f"Totalt antall tabeller/views: {len(schema.get('tables', []))}")
                print("-" * 80)
                for t in schema.get("tables", []):
                    print(f"  - [{t['type'].upper()}] {t['name']}")
            print("=" * 80 + "\n")
        return

    if args.explain:
        plan = svc.explain_query_plan(args.explain)
        if args.json:
            print(json.dumps(plan.model_dump(), indent=2, ensure_ascii=False))
        else:
            print("\n" + "=" * 80)
            print("🏛️ KRISTIANSAND KOMMUNE — AGENT 14 EXPLAIN QUERY PLAN")
            print("=" * 80)
            print(f"SQL:                  {plan.sql}")
            print(f"Bruker Indeks:        {'🟢 JA' if plan.uses_index else '🟡 NEI'}")
            print(f"Full Tabellskanning:  {'🔴 JA (SCAN TABLE)' if plan.scans_entire_table else '🟢 NEI'}")
            if plan.optimization_recommendation:
                print(f"Råd:                  {plan.optimization_recommendation}")
            print("-" * 80)
            print("Spørreplan:")
            for s in plan.plan_steps:
                print(f"  • {s}")
            print("=" * 80 + "\n")
        return

    if args.hybrid_search:
        results = svc.hybrid_search(args.hybrid_search, top_k=5)
        if args.json:
            print(json.dumps([r.model_dump() for r in results], indent=2, ensure_ascii=False))
        else:
            print("\n" + "=" * 80)
            print("🏛️ KRISTIANSAND KOMMUNE — AGENT 14 HYBRID SEARCH")
            print("=" * 80)
            print(f"Søkefrase:   '{args.hybrid_search}'")
            print(f"Treff:       {len(results)}")
            print("-" * 80)
            for r in results:
                print(f"[{r.table_name}] ID: {r.id} | Hybrid: {r.hybrid_score:.4f} (Sparse: {r.sparse_score:.2f}, Dense: {r.dense_score:.2f})")
                print(f"  Tekst: {r.matched_text}")
            print("=" * 80 + "\n")
        return

    if args.query:
        req = QueryRequest(sql=args.query, hitl_approved=args.hitl, limit=args.limit)
        try:
            res = svc.execute_query(req)
            if args.json:
                print(json.dumps(res.model_dump(), indent=2, ensure_ascii=False))
            else:
                print("\n" + "=" * 80)
                print("🏛️ KRISTIANSAND KOMMUNE — AGENT 14 PARAMETERIZED SQL RESULT")
                print("=" * 80)
                print(f"SQL:             {args.query}")
                print(f"Rader hentet:    {res.row_count}")
                print(f"Kjøretid:        {res.execution_time_ms} ms")
                print(f"Query Hash:      {res.query_hash}")
                print(f"PII-Skjermet:    {'🟢 JA' if res.pii_masked else 'NEI'}")
                print("-" * 80)
                if res.rows:
                    cols = res.columns
                    header = " | ".join(f"{c:<18}" for c in cols[:6])
                    print(header)
                    print("-" * len(header))
                    for r in res.rows[:15]:
                        row_line = " | ".join(f"{str(r.get(c, '')):<18}" for c in cols[:6])
                        print(row_line)
                    if len(res.rows) > 15:
                        print(f"... og {len(res.rows) - 15} flere rader.")
                else:
                    print("Ingen rader returnert.")
                print("=" * 80 + "\n")
        except PermissionError as e:
            print(f"\n❌ SIKKERHETSSPERRE: {e}\n")
            sys.exit(1)
        return

    # Standard visning: vis databaseskjema
    schema = svc.inspect_schema()
    print("\n" + "=" * 80)
    print("🏛️ KRISTIANSAND KOMMUNE — AGENT 14 DATABASE & DATA ENGINEERING")
    print("=" * 80)
    print(f"Database: {schema.get('database')}")
    print(f"Tabeller: {len(schema.get('tables', []))}")
    print("-" * 80)
    for t in schema.get("tables", [])[:10]:
        print(f"  • [{t['type'].upper()}] {t['name']}")
    if len(schema.get("tables", [])) > 10:
        print(f"  ... og {len(schema.get('tables', [])) - 10} flere.")
    print("\nKjør med --help for alle operasjoner (inspect-schema, query, explain, hybrid-search).")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
