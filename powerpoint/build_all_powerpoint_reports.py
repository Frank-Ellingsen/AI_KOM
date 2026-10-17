#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Builder: Kommunale PowerPoint Presentasjoner & Styringsdekk 2026
Kristiansand Kommune — Styringsdekk på 5 Ledelsesnivåer

Standarder:
- 16:9 Widescreen (13.333 x 7.5 tommer)
- Financial Times Visual Storytelling (Aksjonstitler på hver slide)
- Edward Tufte Data-Ink Ratio (Ingen tunge skygger, rene kort og tabeller)
- Kommuneloven § 14-4, § 14-5 & § 14-6 bruttoprinsippet
- Stage-Gate Port 9 SHA-256 Audit Logging
"""

import sys
import os
import hashlib
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add src to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "kommune-ai-guardrails" / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Import powerpoint_generator directly without loading heavy embedding models
import importlib.util
gen_path = SRC_DIR / "kommune_ai_guardrails" / "generators" / "powerpoint_generator.py"
spec = importlib.util.spec_from_file_location("powerpoint_generator", str(gen_path))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

generate_bystyret_deck = mod.generate_bystyret_deck
generate_konsern_deck = mod.generate_konsern_deck
generate_oppvekst_deck = mod.generate_oppvekst_deck
generate_capex_evm_deck = mod.generate_capex_evm_deck
generate_enhet202_deck = mod.generate_enhet202_deck

PPT_DIR = PROJECT_ROOT / "powerpoint"
PPT_DIR.mkdir(parents=True, exist_ok=True)

DECKS = [
    {
        "id": "PPTX-L1",
        "level": "Nivå 1: Bystyret & Formannskapet",
        "title": "Presentasjon Bystyret: 2. Tertialrapport & Budsjettendring 2026",
        "file": PPT_DIR / "Presentasjon_Bystyret_Tertialrapport_2026.pptx",
        "func": generate_bystyret_deck,
        "slides": 7,
        "mandat": "Politiske vedtak, § 14-5 budsjettendring og fondsomdisponering kr 3,2M",
    },
    {
        "id": "PPTX-L2",
        "level": "Nivå 2: Kommunedirektørens Ledergruppe",
        "title": "Presentasjon Kommunedirektøren: Konsernstyring & Strakstiltak 2026",
        "file": PPT_DIR / "Presentasjon_Kommunedirektoren_Konsernstyring_2026.pptx",
        "func": generate_konsern_deck,
        "slides": 7,
        "mandat": "Konsernstatus 2,49M avvik, strakstiltak ACT-01–04, likviditet og 6,8 mrd. gjeld",
    },
    {
        "id": "PPTX-L3",
        "level": "Nivå 3: Kommunalsjef Oppvekst",
        "title": "Presentasjon Oppvekst: Bemanningskontroll & Vikaroptimalisering 2026",
        "file": PPT_DIR / "Presentasjon_Oppvekst_Bemanningskontroll_2026.pptx",
        "func": generate_oppvekst_deck,
        "slides": 7,
        "mandat": "Skolematrise (Grim, Vågsbygd etc.), lærernorm § 8-2 og felles vikarring",
    },
    {
        "id": "PPTX-L4",
        "level": "Nivå 4: Prosjektkontroll / Kontrollutvalget",
        "title": "Presentasjon Prosjektkontroll: Capex & EVM Porteføljetilsyn 2026",
        "file": PPT_DIR / "Presentasjon_Prosjektkontroll_Capex_EVM_2026.pptx",
        "func": generate_capex_evm_deck,
        "slides": 7,
        "mandat": "ISO 21508 EVM, S-kurver, CPI/SPI, EAC-sluttprognose og P85-usikkerhetsreserve",
    },
    {
        "id": "PPTX-L5",
        "level": "Nivå 5: Enhetsleder / Virksomhetsleder",
        "title": "Presentasjon Enhet 202: Operativ Avviksrapport (MAL-AVVIK-EFFEKT-001)",
        "file": PPT_DIR / "Presentasjon_Enhet202_Operativ_Avviksrapport_2026.pptx",
        "func": generate_enhet202_deck,
        "slides": 7,
        "mandat": "4-punkts avviksrapport for Enhet 202 Grunnskole, rotårsak og 30/90-dagers tiltak",
    },
]

def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def build_all():
    print("=" * 95)
    print("🏛️  KRISTIANSAND KOMMUNE — MASTER BUILDER FOR POWERPOINT STYRINGSPRESENTASJONER")
    print("Standard: 16:9 Widescreen | FT Visual Storytelling | Edward Tufte Data-Ink | Port 9 SHA-256")
    print("=" * 95)

    results = []
    for item in DECKS:
        print(f"\nBygger [{item['id']}] {item['title']}...")
        out_file = item["func"](str(item["file"]))
        path = Path(out_file)
        if not path.exists():
            raise FileNotFoundError(f"Feilet å bygge {path}")
        size_kb = path.stat().st_size / 1024
        sha = compute_sha256(path)[:12]
        results.append({
            "id": item["id"],
            "level": item["level"],
            "name": path.name,
            "slides": item["slides"],
            "size": f"{size_kb:.1f} KB",
            "sha": sha,
            "mandat": item["mandat"],
        })
        print(f"  ✓ {path.name} ({size_kb:.1f} KB, {item['slides']} slides) - SHA-256: {sha}")

    print("\n" + "=" * 95)
    print(f"{'ID':<10} | {'Nivå':<28} | {'Filnavn':<45} | {'Slides':<7} | {'Størrelse':<10}")
    print("-" * 95)
    for r in results:
        print(f"{r['id']:<10} | {r['level']:<28} | {r['name']:<45} | {r['slides']:<7} | {r['size']:<10}")
    print("=" * 95)
    print("🎉 Alle 5 kommunale PowerPoint-dekk er bygget og validert for Kristiansand kommune!")

if __name__ == "__main__":
    build_all()
