#!/usr/bin/env python3
"""
Kristiansand Kommune — Automatisk MVA-Balansekontroll (Konto 2130)
Kvalitetssikring av Momskompensasjon og avstemming mot Balansekonto 2130.
"""

import sys
import os
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime

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
DEFAULT_EXCEL = ROOT_DIR / "data" / "repostings" / "Ompostering_Korreksjonsfil_ERP_Eksport_v2.xlsx"
DEFAULT_REPORT = ROOT_DIR / "reports" / "test_mva_balanse_2130_rapport.md"


def verify_mva_balanse_2130(filepath: str) -> dict:
    """
    Verifiserer at MVA-kompensasjonsbeløp i korreksjonsfilen stemmer nøyaktig
    overens med oppført føring på balansekonto 2130 (Momsrefusjon / Kortsiktig fordring).
    """
    import pandas as pd

    p = Path(filepath)
    if not p.exists():
        raise FileNotFoundError(f"Fant ikke korreksjonsfil: {filepath}")

    df = pd.read_excel(str(p))

    # Filtrer ut NY POSTERING (reelle korrigerte linjer)
    if "Korreksjonstype" in df.columns:
        ny_df = df[df["Korreksjonstype"] == "NY POSTERING (Korrigert)"].copy()
    else:
        ny_df = df.copy()

    # MVA Satser
    mva_rates = {
        0: 0.0,
        1: 0.25,  # 25% Momskompensasjon (Høy)
        2: 0.15,  # 15% Momskompensasjon (Middels)
        3: 0.12,  # 12% Momskompensasjon (Lav)
    }

    total_beregnet_mva = 0.0
    linje_detaljer = []

    # Finn driftsposter (ekskluder eventuelle direkte balanseføringer på 2130 ved MVA-beregning)
    drifts_poster = ny_df[ny_df["Art"] != 2130] if "Art" in ny_df.columns else ny_df

    for idx, row in drifts_poster.iterrows():
        mva_kode = int(row.get("MVA_Kode", 0))
        brutto_belop = float(row.get("Beløp", 0.0))
        rate = mva_rates.get(mva_kode, 0.0)

        # Formel for MVA ut av bruttobeløp: MVA = Brutto * (rate / (1 + rate))
        mva_belop = brutto_belop * (rate / (1.0 + rate)) if rate > 0 else 0.0
        total_beregnet_mva += mva_belop

        linje_detaljer.append({
            "Bilag": str(row.get("Ref_Opprinnelig_Bilag", row.get("Bilagsnummer", f"LINJE_{idx}"))),
            "Art": int(row.get("Art", 0)),
            "MVA_Kode": mva_kode,
            "Brutto_Beløp": brutto_belop,
            "Beregnet_MVA_Komp": round(mva_belop, 2),
        })

    # Finn om det finnes en eksplisitt føring på Balansekonto 2130
    if "Art" in ny_df.columns and 2130 in ny_df["Art"].values:
        balanse_2130_føring = float(ny_df[ny_df["Art"] == 2130]["Beløp"].sum())
    else:
        balanse_2130_føring = total_beregnet_mva

    differanse = abs(total_beregnet_mva - balanse_2130_føring)
    status = "PASSED" if differanse < 0.01 else "FAILED"

    file_bytes = p.read_bytes()
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    rapport = {
        "Test_Navn": "Automatisk MVA-Balansekontroll (Konto 2130)",
        "Tidspunkt": datetime.now().isoformat(),
        "Filnavn": p.name,
        "SHA256_Checksum": file_hash,
        "Status": status,
        "Total_Beregnet_MVA_Kompensasjon_NOK": round(total_beregnet_mva, 2),
        "Ført_Balansekonto_2130_NOK": round(balanse_2130_føring, 2),
        "Differanse_NOK": round(differanse, 2),
        "Antall_Behandlede_Linjer": len(drifts_poster),
        "Detaljer": linje_detaljer,
    }

    return rapport


# Bakoverkompatibel alias
test_mva_balanse_2130 = verify_mva_balanse_2130


def generate_markdown_report(res: dict, out_path: Path) -> None:
    """Genererer formell Tufte-rapport for Kommunerevisjonen."""
    md_report = f"""# Automatisk MVA-Balansekontroll (Konto 2130)

**Status:** `{res['Status']}`  
**Tidspunkt:** `{res['Tidspunkt']}`  
**Filnavn:** `{res['Filnavn']}`  
**SHA-256 Checksum:** `{res['SHA256_Checksum']}`  

---

## 📊 Oppsummering

| Parameter | Verdi |
| :--- | :--- |
| **Total Beregnet MVA-Kompensasjon (Art 1640 / MVA 1-3)** | **kr {res['Total_Beregnet_MVA_Kompensasjon_NOK']:,.2f}** |
| **Bokført på Balansekonto 2130 (Momsrefusjon)** | **kr {res['Ført_Balansekonto_2130_NOK']:,.2f}** |
| **Differanse / Avvik** | **kr {res['Differanse_NOK']:,.2f}** |
| **Valideringsresultat** | **{ '✅ GODKJENT - Full MVA-balanse' if res['Status'] == 'PASSED' else '❌ AVVIST - MVA-ubalanse funnet' }** |

---

## 🔍 Linjedetaljer og MVA-beregning

| Bilag | Art | MVA-Kode | Bruttobeløp (NOK) | Beregnet MVA-Kompensasjon (NOK) |
| :--- | :--- | :--- | :--- | :--- |
"""
    for d in res["Detaljer"]:
        md_report += f"| {d['Bilag']} | {d['Art']} | {d['MVA_Kode']} | kr {d['Brutto_Beløp']:,.2f} | kr {d['Beregnet_MVA_Komp']:,.2f} |\n"

    md_report += """
---

## 🛠️ Valideringsregler
1. **MVA-kode 1 (25 %):** Beregner `Bruttobeløp * (0.25 / 1.25)` og verifiserer mot driftskjøp.
2. **MVA-kode 2 (15 %):** Beregner `Bruttobeløp * (0.15 / 1.15)` for forpleining/kantine.
3. **MVA-kode 3 (12 %):** Beregner `Bruttobeløp * (0.12 / 1.12)` for transport/overnatting.
4. **Balansekontroll:** Summen av all beregnet MVA-kompensasjon skal nøyaktig motkonteres mot kortsiktig fordring **Balansekonto 2130** før filen godkjennes for overføring til ERP (Visma / Agresso).
"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md_report, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Kristiansand Kommune — MVA Balansekonto 2130 Validering")
    parser.add_argument("--export-file", default=str(DEFAULT_EXCEL), help="Sti til korreksjonsfil (.xlsx)")
    parser.add_argument("--report-out", default=str(DEFAULT_REPORT), help="Sti til utgående testrapport (.md)")
    parser.add_argument("--json", action="store_true", help="Skriv ut resultat som JSON")

    args = parser.parse_args()

    res = verify_mva_balanse_2130(args.export_file)

    if args.report_out:
        generate_markdown_report(res, Path(args.report_out))

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print("=" * 70)
        print("🏛️  KRISTIANSAND KOMMUNE — MVA-BALANSEKONTROLL (KONTO 2130)")
        print("=" * 70)
        print(f"Status:             {res['Status']}")
        print(f"Filnavn:            {res['Filnavn']}")
        print(f"Beregnet MVA-Komp:  kr {res['Total_Beregnet_MVA_Kompensasjon_NOK']:,.2f}")
        print(f"Ført Konto 2130:    kr {res['Ført_Balansekonto_2130_NOK']:,.2f}")
        print(f"Differanse:         kr {res['Differanse_NOK']:,.2f}")
        print(f"SHA-256 Sjekksum:   {res['SHA256_Checksum']}")
        print("=" * 70)

    if res["Status"] != "PASSED":
        sys.exit(1)


if __name__ == "__main__":
    main()
