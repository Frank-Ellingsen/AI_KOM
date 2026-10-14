#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Builder: Kommunale Word Rapporter & Styringsdokumenter 2026
Kristiansand Kommune — Styring på 5 Ledelsesnivåer

Standarder:
- Kommuneloven § 14-4, § 14-5 & § 14-6 bruttoprinsippet
- Edward Tufte Data-Ink Ratio (rene linjer, ingen vertikale rutenett)
- Financial Times Visual Storytelling (#1E3A8A overskrifter, 1.15 linjeavstand, 6 pt etter avsnitt)
- Public360 Metadata-arkivering (Saksnummer, Arkivkode, Tilgangskode)
- WCAG 2.1 AA (Repeat Table Headers w:tblHeader på tvers av sideskift)
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

from kommune_ai_guardrails.generators.word_saksfremlegg_generator import (
    generate_saksfremlegg_docx,
    generate_hop_notat_docx,
    generate_raadmann_notat_docx,
    generate_sektornotat_oppvekst_docx,
    generate_prosjektkontroll_capex_docx,
    generate_avviksnotat_enhetsleder_docx,
)

WORD_DIR = PROJECT_ROOT / "word"
WORD_DIR.mkdir(parents=True, exist_ok=True)

REPORTS = [
    {
        "id": "WORD-L1",
        "level": "Nivå 1: Bystyret & Formannskapet",
        "title": "Saksfremlegg: Endring av Årsbudsjett 2026 (Sak 26/0142)",
        "file": WORD_DIR / "Saksfremlegg_Bystyret_Budsjettendring_2026.docx",
        "func": generate_saksfremlegg_docx,
        "mandat": "Kommuneloven § 14-5 budsjettendring og fondsomdisponering kr 3,2M til Grunnskole",
    },
    {
        "id": "WORD-L2-HOP",
        "level": "Nivå 2: Kommunedirektøren / Konsern",
        "title": "Tertialrapport 2 & Notat Handlings- og Økonomiplan (HØP 2027–2030)",
        "file": WORD_DIR / "Tertialrapport_og_HOP_Notat_2026.docx",
        "func": generate_hop_notat_docx,
        "mandat": "Konsernoverblikk, KOSTRA-rammer og 4-årig finans- og investeringsstrategi",
    },
    {
        "id": "WORD-L2-RAAD",
        "level": "Nivå 2: Kommunedirektørens Ledergruppe",
        "title": "Månedsrapport Kommunedirektøren: Administrativ Strakstiltaksplan 2026",
        "file": WORD_DIR / "Manedsrapport_Kommunedirektor_Strakstiltak_2026.docx",
        "func": generate_raadmann_notat_docx,
        "mandat": "Månedlig konsernoppfølging, vikarstopp ACT-01 til ACT-04, internkontroll § 14-5",
    },
    {
        "id": "WORD-L3",
        "level": "Nivå 3: Kommunalsjef Oppvekst",
        "title": "Sektorstyringsnotat Oppvekst & Utdanning: Kapasitets- og Vikaranalyse",
        "file": WORD_DIR / "Sektorstyringsnotat_Kommunalsjef_Oppvekst_2026.docx",
        "func": generate_sektornotat_oppvekst_docx,
        "mandat": "Sektorstyring på 6 skoler, vikarutgifter, sykefraværsreduksjon og lærernorm",
    },
    {
        "id": "WORD-L4",
        "level": "Nivå 4: Prosjektkontroll / Capex Controller",
        "title": "Prosjektkontroll & Capex Statusnotat: Investeringsportefølje & EVM",
        "file": WORD_DIR / "Prosjektkontroll_Capex_Statusnotat_2026.docx",
        "func": generate_prosjektkontroll_capex_docx,
        "mandat": "ISO 21508 EVM (CPI/SPI), P85-usikkerhetsavsetning, EAC/ETC for 5 nøkkelprosjekter",
    },
    {
        "id": "WORD-L5",
        "level": "Nivå 5: Enhetsleder / Virksomhetsleder",
        "title": "Avviksnotat & Handlingsplan: Enhet 202 Grunnskole (MAL-AVVIK-EFFEKT-001)",
        "file": WORD_DIR / "Avviksnotat_og_Handlingsplan_Enhetsleder_2026.docx",
        "func": generate_avviksnotat_enhetsleder_docx,
        "mandat": "4-punkts operativ avviksrapport (Status, Årsak, Handlingsplan, Helårsprognose)",
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
    print("🏛️  KRISTIANSAND KOMMUNE — MASTER BUILDER FOR WORD RAPPORTER & STYRINGSNOTATER")
    print("Standard: Kommuneloven § 14-5 | Edward Tufte Data-Ink | Public360 | WCAG 2.1 AA")
    print("=" * 95)

    results = []
    for item in REPORTS:
        print(f"\nGenererer [{item['id']}] {item['title']}...")
        out_file = item["func"](str(item["file"]))
        path = Path(out_file)
        if not path.exists():
            raise FileNotFoundError(f"Feilet å generere {path}")
        size_kb = path.stat().st_size / 1024
        sha = compute_sha256(path)[:12]
        results.append({
            "id": item["id"],
            "level": item["level"],
            "name": path.name,
            "size": f"{size_kb:.1f} KB",
            "sha": sha,
            "mandat": item["mandat"],
        })
        print(f"  ✓ {path.name} ({size_kb:.1f} KB) - SHA-256: {sha}")

    print("\n" + "=" * 95)
    print(f"{'ID':<12} | {'Nivå':<30} | {'Filnavn':<45} | {'Størrelse':<10}")
    print("-" * 95)
    for r in results:
        print(f"{r['id']:<12} | {r['level']:<30} | {r['name']:<45} | {r['size']:<10}")
    print("=" * 95)
    print("🎉 Alle 6 kommunale Word-dokumenter er bygget og validert for Kristiansand kommune!")

if __name__ == "__main__":
    build_all()
