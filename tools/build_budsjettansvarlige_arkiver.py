#!/usr/bin/env python3
"""
Generator for Individuelle Rapportarkiver for Budsjettansvarlige
Kristiansand Kommune — AI Project Controller Hub
Lead Controller: Frank Ellingsen

Hovedfunksjon:
Oppretter et dedikert, personlig rapportarkiv for HVER enkelt budsjettansvarlig (41 enheter)
under reports/budsjettansvarlige_arkiv/{ansvar_id}/.

Struktur per enhetsarkiv:
  reports/budsjettansvarlige_arkiv/{ansvar_id}/
  ├── 01_Maanedsrapporter/
  │   ├── Maanedsrapport_M09_2026.pdf
  │   ├── Maanedsrapport_M09_2026.html
  │   ├── Maanedsrapport_M10_2026.pdf
  │   └── Maanedsrapport_M10_2026.html
  ├── 02_Kontoutskrifter/
  │   └── KONTOUTSKRIFT_{ansvar_id}_M10.html
  ├── 03_Saksdokumenter_og_Maler/
  │   ├── [Tilknyttet_mal.docx]
  │   ├── [Tilknyttet_mal.md]
  │   └── [Sektorspesifikke maler: HTA § 4, Bemanning, Refusjon, etc.]
  ├── 04_Framsikt_Omdisponering/
  │   ├── framsikt_kontering_{ansvar_id}.csv
  │   └── FRAMSIKT_KONTERINGSANVISNING.md
  ├── ARKIV_OVERSIKT.html   (Personlig lederdashboard med Tufte-design)
  └── README.md             (Sammendrag og filoversikt)

I tillegg genereres master-portalen:
  reports/budsjettansvarlige_arkiv/index.html (For Frank Ellingsen & ledergruppen)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys
from typing import Any, Dict, List

# Sikre UTF-8 i konsoll på Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "erp_data" / "kommune_golden_record.db"
TEMPLATES_DIR = ROOT_DIR / "templates"
KONTOUTSKRIFTER_DIR = ROOT_DIR / "reports" / "kontoutskrifter"
ARCHIVE_ROOT = ROOT_DIR / "reports" / "budsjettansvarlige_arkiv"
ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)

# Importer beregnings- og rapportgenerator-funksjoner fra generate_monthly_pdf_reports
sys.path.insert(0, str(ROOT_DIR / "tools"))
from generate_monthly_pdf_reports import (
    MONTH_NAMES,
    SEASONAL_WEIGHTS,
    SEKTOR_MAP,
    calculate_unit_metrics,
    generate_html_report,
    generate_pdf_report,
    get_budget_holders_from_db,
)


def get_sector_templates(sektor_kode: str, niva: str) -> List[Path]:
    """Returnerer relevante tilleggsmaler basert på enhetens sektor og nivå."""
    additional = []
    if sektor_kode == "HELSE":
        hta_docx = TEMPLATES_DIR / "MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.docx"
        hta_md = TEMPLATES_DIR / "MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.md"
        if hta_docx.exists():
            additional.append(hta_docx)
        if hta_md.exists():
            additional.append(hta_md)
    elif sektor_kode == "OPPVEKST":
        bem_xlsx = TEMPLATES_DIR / "MAL_BEMANNINGSPLAN_OG_VIKARBUDSJETT.xlsx"
        bem_md = TEMPLATES_DIR / "MAL_BEMANNINGSPLAN_OG_VIKARBUDSJETT.md"
        nav_xlsx = TEMPLATES_DIR / "MAL_NAV_REFUSJONSOPPFOLGING_OG_AVSTEMMING.xlsx"
        if bem_xlsx.exists():
            additional.append(bem_xlsx)
        if bem_md.exists():
            additional.append(bem_md)
        if nav_xlsx.exists():
            additional.append(nav_xlsx)
    elif niva in ["NIVA1", "NIVA2"]:
        sak_docx = TEMPLATES_DIR / "MAL_POLITISK_SAKSFREMLEGG_BUDSJETTENDRING.docx"
        sak_md = TEMPLATES_DIR / "MAL_POLITISK_SAKSFREMLEGG_BUDSJETTENDRING.md"
        if sak_docx.exists():
            additional.append(sak_docx)
        if sak_md.exists():
            additional.append(sak_md)

    return additional


def create_framsikt_unit_files(m_data: Dict[str, Any], target_dir: Path) -> Tuple[Path, Path]:
    """Genererer enhets-spesifikk Framsikt konterings-CSV og instruksjonsnotat."""
    holder = m_data["holder"]
    aid = holder["ansvar_id"]
    deb_kred = m_data["paraply"]["framsikt_deb_kred"]
    month = m_data["month"]

    # 1. CSV
    csv_path = target_dir / f"framsikt_kontering_{aid}.csv"
    reg_id = f"REG-2026-M{month}-{aid.replace('-', '')[:8]}"

    rows = [
        {
            "regulerings_id": reg_id,
            "periode": f"2026-M{month:02d}",
            "type": "RAMMEREGULERING",
            "ansvar_kode": deb_kred["avgiver_ansvar"],
            "art_kode": deb_kred["avgiver_art"].split()[0],
            "belop_nok": deb_kred["avgiver_belop"],
            "tekst": deb_kred["avgiver_tekst"],
            "fullmakt": "Kommunalsjef Nivå 1"
        },
        {
            "regulerings_id": reg_id,
            "periode": f"2026-M{month:02d}",
            "type": "RAMMEREGULERING",
            "ansvar_kode": deb_kred["mottaker_ansvar"],
            "art_kode": deb_kred["mottaker_art"].split()[0],
            "belop_nok": deb_kred["mottaker_belop"],
            "tekst": deb_kred["mottaker_tekst"],
            "fullmakt": "Kommunalsjef Nivå 1"
        }
    ]

    fieldnames = ["regulerings_id", "periode", "type", "ansvar_kode", "art_kode", "belop_nok", "tekst", "fullmakt"]
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)

    # 2. Markdown veiledning
    md_path = target_dir / "FRAMSIKT_KONTERINGSANVISNING.md"
    md_content = f"""# Framsikt EPM: Konteringsanvisning for {holder['enhet_navn']} (Ansvar {aid})

## 1. Bakgrunn for Rammeregulering
* **Budsjettansvarlig:** {holder['navn']} ({holder['tittel']})
* **Sektor / Paraply:** {m_data['paraply']['paraply_navn']}
* **Status YTD:** {m_data['rag_label']}
* **Beregnet avvik:** kr {m_data['avvik_ytd']:,.0f} (Budsjett - Actuals)

## 2. Omdisponeringsmekanisme i Framsikt EPM
{m_data['paraply']['omdisponering_tekst']}

## 3. Konkret Føring i Framsikt EPM (Modul: Tertialoppfølging ➜ Budsjettreguleringer)

| Linje | Postering | Ansvar | Art | Beløp (NOK) | Konteringstekst |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | Avgiver (Kredit) | `{deb_kred['avgiver_ansvar']}` | `{deb_kred['avgiver_art']}` | **{deb_kred['avgiver_belop']:,.0f}** | {deb_kred['avgiver_tekst']} |
| **2** | Mottaker (Debet) | `{deb_kred['mottaker_ansvar']}` | `{deb_kred['mottaker_art']}` | **+{deb_kred['mottaker_belop']:,.0f}** | {deb_kred['mottaker_tekst']} |
| **SUM** | **Netto Balanse** | - | - | **kr 0,00** | **I balanse innen rammeområdet** |

## 4. Godkjenningsflyt
1. **Attestert av fagcontroller:** {holder['controller_navn']} ({holder['controller_epost']})
2. **Signert av ansvarlig leder:** {holder['navn']} ({holder['epost']})
3. **Endelig rammegodkjenning:** {m_data['paraply']['leder_tittel']} ({m_data['paraply']['leder']})
"""
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return csv_path, md_path


def generate_personal_archive_html(holder: Dict[str, Any], m9: Dict[str, Any], m10: Dict[str, Any], out_path: Path):
    """Genererer personlig Edward Tufte-dashboard for denne lederens eget rapportarkiv."""
    aid = holder["ansvar_id"]
    avv = m9["avvik_ytd"]
    avv_sign = "+" if avv >= 0 else ""
    avv_class = "positive" if avv >= 0 else "negative"

    html = f"""<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapportarkiv — {holder['enhet_navn']} ({aid})</title>
    <style>
        :root {{
            --bg-page: #f8fafc;
            --surface: #ffffff;
            --navy-dark: #1e293b;
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
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg-page);
            color: var(--text-primary);
            line-height: 1.5;
            padding: 28px;
        }}
        .container {{
            max-width: 1080px;
            margin: 0 auto;
            background: var(--surface);
            border: 1px solid var(--border-light);
            border-radius: 6px;
            padding: 36px 42px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }}
        .top-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            font-size: 12px;
        }}
        .back-link {{
            color: var(--navy-dark);
            text-decoration: none;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        .back-link:hover {{ text-decoration: underline; }}
        .header-box {{
            border-bottom: 2px solid var(--navy-dark);
            padding-bottom: 16px;
            margin-bottom: 24px;
        }}
        .unit-title {{ font-size: 24px; font-weight: 700; color: var(--navy-dark); margin-bottom: 4px; }}
        .unit-meta {{ font-size: 13px; color: var(--text-secondary); }}
        
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
        .positive {{ color: var(--green); }}
        .negative {{ color: var(--red); }}
        
        h2 {{ font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--navy-dark); margin: 28px 0 12px 0; border-bottom: 1px solid var(--navy-dark); padding-bottom: 4px; }}
        
        .archive-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .archive-card {{
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 16px;
            background: #ffffff;
            transition: border-color 0.15s, box-shadow 0.15s;
        }}
        .archive-card:hover {{
            border-color: var(--navy-dark);
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        }}
        .card-title {{ font-size: 13px; font-weight: 700; color: var(--navy-dark); margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }}
        .card-desc {{ font-size: 11.5px; color: var(--text-secondary); margin-bottom: 12px; }}
        .file-list {{ list-style: none; font-size: 12px; }}
        .file-list li {{ margin-bottom: 6px; }}
        .file-link {{
            color: var(--navy-dark);
            text-decoration: none;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }}
        .file-link:hover {{ text-decoration: underline; }}
        
        .info-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            margin-bottom: 24px;
        }}
        .info-table th {{
            text-align: left;
            padding: 8px 10px;
            border-bottom: 1.5px solid var(--navy-dark);
            font-weight: 600;
        }}
        .info-table td {{
            padding: 8px 10px;
            border-bottom: 1px solid var(--border-light);
            color: var(--text-secondary);
        }}
        .info-table tr:hover td {{ background: #f8fafc; }}
        
        .footer-strip {{
            margin-top: 36px;
            padding-top: 16px;
            border-top: 1px dashed var(--border-light);
            font-size: 11px;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="top-nav">
            <a class="back-link" href="../index.html">⬅️ Tilbake til Hovedregister over alle Budsjettansvarlige</a>
            <span>Kristiansand Kommune — AI Project Controller Hub</span>
        </div>

        <div class="header-box">
            <div class="unit-title">📁 Rapportarkiv: {holder['enhet_navn']}</div>
            <div class="unit-meta">
                <strong>Ansvar:</strong> {aid} | <strong>Leder:</strong> {holder['navn']} ({holder['tittel']}) | 
                <strong>E-post:</strong> {holder['epost']} | <strong>Telefon:</strong> {holder['telefon']} | 
                <strong>Kontorsted:</strong> {holder['kontorsted']}
            </div>
            <div class="unit-meta" style="margin-top: 4px;">
                <strong>Sektor:</strong> {holder['sektor_navn']} | <strong>KOSTRA-funksjon:</strong> {holder['kostra_funksjon']} | 
                <strong>Delegeringsfullmakt:</strong> kr {holder['delegeringsfullmakt_nok']:,.0f} | 
                <strong>Sektorcontroller:</strong> {holder['controller_navn']} ({holder['controller_epost']})
            </div>
        </div>

        <!-- KPI Strip -->
        <div class="kpi-strip">
            <div class="kpi-card">
                <div class="kpi-label">Tildelt Årsbudsjett</div>
                <div class="kpi-value">kr {m9['annual_budget']:,.0f}</div>
                <div class="kpi-sub">Vedtatt ramme 2026</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Faktisk Regnskap YTD (M9)</div>
                <div class="kpi-value">kr {m9['ytd_actual']:,.0f}</div>
                <div class="kpi-sub">Forbruksgrad: {m9['forbruksgrad']:.1f} %</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Avvik (Budsjett - Actuals)</div>
                <div class="kpi-value {avv_class}">{avv_sign}kr {avv:,.0f}</div>
                <div class="kpi-sub">{m9['rag_label']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">EOY Prognose (P50)</div>
                <div class="kpi-value">kr {m9['prognosis']['p50']:,.0f}</div>
                <div class="kpi-sub">Sluttavvik: kr {m9['prognosis']['sluttavvik_p50']:,.0f}</div>
            </div>
        </div>

        <!-- Dokumentmapper i arkivet -->
        <h2>Enhetens Dedikerte Rapporter og Dokumentmapper</h2>
        <div class="archive-grid">
            <div class="archive-card">
                <div class="card-title">📄 01. Månedsrapporter</div>
                <div class="card-desc">Offisielle 2-siders PDF- og HTML-avviksrapporter med status, diagnostikk, Monte Carlo og preskripsjoner.</div>
                <ul class="file-list">
                    <li><a class="file-link" href="01_Maanedsrapporter/Maanedsrapport_M09_2026.pdf" target="_blank">📄 Maanedsrapport M09 (PDF)</a></li>
                    <li><a class="file-link" href="01_Maanedsrapporter/Maanedsrapport_M09_2026.html" target="_blank">🌐 Maanedsrapport M09 (HTML)</a></li>
                    <li><a class="file-link" href="01_Maanedsrapporter/Maanedsrapport_M10_2026.pdf" target="_blank">📄 Maanedsrapport M10 (PDF)</a></li>
                    <li><a class="file-link" href="01_Maanedsrapporter/M10_Maanedsrapport_M10_2026.html" target="_blank">🌐 Maanedsrapport M10 (HTML)</a></li>
                </ul>
            </div>

            <div class="archive-card">
                <div class="card-title">🏦 02. Kontoutskrift (Nettbank)</div>
                <div class="card-desc">Månedlige pedagogiske bankutskrifter for ledere uten økonomiutdanning med disponibel saldo ut året.</div>
                <ul class="file-list">
                    <li><a class="file-link" href="02_Kontoutskrifter/KONTOUTSKRIFT_{aid}_M10.html" target="_blank">🏦 Kontoutskrift M10 (Nettbank)</a></li>
                </ul>
            </div>

            <div class="archive-card">
                <div class="card-title">📝 03. Saksdokumenter &amp; Maler</div>
                <div class="card-desc">Tilknyttede kommunale maler for avviksnotat, tiltaksplan, HTA § 4 og bemanningsplaner.</div>
                <ul class="file-list">
                    <li><a class="file-link" href="03_Saksdokumenter_og_Maler/{Path(holder['tilknyttet_mal']).name}" target="_blank">📝 {Path(holder['tilknyttet_mal']).name}</a></li>
                    <li><span class="card-desc">Returkanal: {holder['returkanal']}</span></li>
                    <li><span class="card-desc">Returfrist: <strong>{holder['returfrist']}</strong></span></li>
                </ul>
            </div>

            <div class="archive-card">
                <div class="card-title">🔄 04. Framsikt Rammeregulering</div>
                <div class="card-desc">Enhetsspesifikke konteringslinjer for omdisponering av overskudd eller dekning av underskudd.</div>
                <ul class="file-list">
                    <li><a class="file-link" href="04_Framsikt_Omdisponering/framsikt_kontering_{aid}.csv" download>📥 Framsikt Batch CSV</a></li>
                    <li><a class="file-link" href="04_Framsikt_Omdisponering/FRAMSIKT_KONTERINGSANVISNING.md" target="_blank">📖 Konteringsveileder</a></li>
                </ul>
            </div>
        </div>

        <!-- Delegeringsavtale og Retningslinjer -->
        <h2>Delegeringsavtale &amp; Saksbehandlingskrav</h2>
        <table class="info-table">
            <thead>
                <tr>
                    <th>Felt</th>
                    <th>Spesifikasjon</th>
                    <th>Instruks for leder</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Delegeringsfullmakt</strong></td>
                    <td>kr {holder['delegeringsfullmakt_nok']:,.0f}</td>
                    <td>Attestasjonsfullmakt på art 1000–1270. Attestasjon skjer i Visma ERP.</td>
                </tr>
                <tr>
                    <td><strong>Utsendte rapporter</strong></td>
                    <td>{holder['utsendte_rapporter']}</td>
                    <td>Mottas månedlig via e-post og dedikert Microsoft Teams-kanal.</td>
                </tr>
                <tr>
                    <td><strong>Returfrist</strong></td>
                    <td><strong>{holder['returfrist']}</strong></td>
                    <td>Ved merforbruk (rødt trafikklys) må avviksnotat returneres innen fristen.</td>
                </tr>
                <tr>
                    <td><strong>Returkanal</strong></td>
                    <td><code>{holder['returkanal']}</code></td>
                    <td>Sendes til angitt e-postadresse eller via Websak / Public 360.</td>
                </tr>
                <tr>
                    <td><strong>Sektorcontroller</strong></td>
                    <td>{holder['controller_navn']} ({holder['controller_epost']})</td>
                    <td>Sparringspartner for turnusjustering, vikarstopp og Framsikt-omdisponeringer.</td>
                </tr>
            </tbody>
        </table>

        <div class="footer-strip">
            <span>Kristiansand Kommune — Arkiv for Budsjettansvarlig {aid}</span>
            <span>Kryptografisk revisjonssegl (Stage-Gate Port 9): {m9['prognosis']['sha256'][:16]}...</span>
        </div>
    </div>
</body>
</html>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)


def generate_personal_readme(holder: Dict[str, Any], m9: Dict[str, Any], out_path: Path):
    """Genererer en markdown README i enhetens arkivmappe."""
    aid = holder["ansvar_id"]
    content = f"""# 📁 Personlig Rapportarkiv: {holder['enhet_navn']}
**Ansvar:** `{aid}` | **Leder:** {holder['navn']} ({holder['tittel']})  
**E-post:** {holder['epost']} | **Telefon:** {holder['telefon']} | **Kontorsted:** {holder['kontorsted']}  
**Sektor:** {holder['sektor_navn']} | **KOSTRA-funksjon:** {holder['kostra_funksjon']}  
**Delegeringsfullmakt:** kr {holder['delegeringsfullmakt_nok']:,.0f}  
**Sektorcontroller:** {holder['controller_navn']} ({holder['controller_epost']})  

---

## 📊 Finansiell Nøkkelstatus (M9 YTD)
* **Tildelt Årsbudsjett:** kr {m9['annual_budget']:,.0f}
* **Faktisk Regnskap YTD:** kr {m9['ytd_actual']:,.0f} (Forbruksgrad: {m9['forbruksgrad']:.1f} %)
* **Avvik YTD (Budsjett - Actuals):** kr {m9['avvik_ytd']:,.0f}
* **Trafikklys:** {m9['rag_label']}
* **Sesongjustert EOY Sluttprognose (P50):** kr {m9['prognosis']['p50']:,.0f} (Sluttavvik: kr {m9['prognosis']['sluttavvik_p50']:,.0f})
* **SHA-256 Revisjonsstempel:** `{m9['prognosis']['sha256']}`

---

## 📂 Innhold i dette arkivet
1. `01_Maanedsrapporter/`:
   - `Maanedsrapport_M09_2026.pdf` og `Maanedsrapport_M09_2026.html`
   - `Maanedsrapport_M10_2026.pdf` og `Maanedsrapport_M10_2026.html`
2. `02_Kontoutskrifter/`:
   - `KONTOUTSKRIFT_{aid}_M10.html` (Nettbank kontoutskrift for enhetsleder)
3. `03_Saksdokumenter_og_Maler/`:
   - Enhetens tilknyttede saks- og rapportmaler jf. retningslinjer
4. `04_Framsikt_Omdisponering/`:
   - `framsikt_kontering_{aid}.csv` (Batch-linjer for rammeregulering)
   - `FRAMSIKT_KONTERINGSANVISNING.md` (Veiledning for føring i Framsikt)
5. `ARKIV_OVERSIKT.html`:
   - Interaktivt nettleserdashboard for denne enheten

---
*Returkanal for avviksnotater:* `{holder['returkanal']}`  
*Returfrist:* **{holder['returfrist']}**
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)


def generate_master_archive_index(all_holders_data: List[Dict[str, Any]], out_path: Path):
    """Genererer masterportalen reports/budsjettansvarlige_arkiv/index.html med søk og filter."""
    rows_html = ""
    for item in all_holders_data:
        h = item["holder"]
        m = item["m9"]
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

        archive_folder_link = f"{aid}/ARKIV_OVERSIKT.html"

        rows_html += f"""
        <tr data-sektor="{h['sektor_kode']}" data-niva="{h['niva']}" data-status="{rag}">
            <td><code>{aid}</code></td>
            <td>
                <strong><a href="{archive_folder_link}" style="color: #1e293b; text-decoration: none;">{h['enhet_navn']}</a></strong><br/>
                <span class="subtext">Leder: {h['navn']} ({h['tittel']}) | {h['epost']}</span>
            </td>
            <td><span class="pill-sektor">{h['sektor_kode']}</span></td>
            <td>{h['niva_tekst'].split(':')[0]}</td>
            <td class="num">kr {m['annual_budget']:,.0f}</td>
            <td class="num">kr {m['ytd_actual']:,.0f}</td>
            <td class="num {avv_class}"><strong>{avv_sign}kr {avv:,.0f}</strong></td>
            <td>{rag_badge}</td>
            <td>
                <a class="btn-arkiv" href="{archive_folder_link}">📁 Åpne Arkiv</a>
            </td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Masterarkiv — Budsjettansvarlige | Kristiansand Kommune</title>
    <style>
        :root {{
            --bg-page: #f8fafc;
            --surface: #ffffff;
            --navy-dark: #1e293b;
            --navy-light: #334155;
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
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg-page);
            color: var(--text-primary);
            padding: 32px;
        }}
        .container {{
            max-width: 1280px;
            margin: 0 auto;
            background: var(--surface);
            border: 1px solid var(--border-light);
            border-radius: 6px;
            padding: 32px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-bottom: 2px solid var(--navy-dark);
            padding-bottom: 16px;
            margin-bottom: 24px;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .title h1 {{ font-size: 22px; font-weight: 700; color: var(--navy-dark); }}
        .title p {{ font-size: 13px; color: var(--text-secondary); margin-top: 4px; }}
        .meta-stats {{ font-size: 12px; color: var(--text-muted); text-align: right; }}
        
        .filter-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #f1f5f9;
            padding: 10px 14px;
            border-radius: 4px;
            margin-bottom: 20px;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .filter-group {{ display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }}
        .filter-btn {{
            background: #ffffff;
            border: 1px solid var(--border-light);
            color: var(--text-primary);
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s;
        }}
        .filter-btn:hover {{ background: #e2e8f0; }}
        .filter-btn.active {{
            background: var(--navy-dark);
            color: #ffffff;
            border-color: var(--navy-dark);
        }}
        .search-input {{
            padding: 6px 12px;
            font-size: 12px;
            border: 1px solid var(--border-light);
            border-radius: 4px;
            width: 240px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }}
        th {{
            text-align: left;
            padding: 10px 12px;
            border-bottom: 2px solid var(--navy-dark);
            color: var(--navy-dark);
            font-weight: 600;
        }}
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid var(--border-light);
            color: var(--text-secondary);
        }}
        tr:hover td {{ background: #f8fafc; }}
        .num {{ text-align: right; }}
        .positive {{ color: var(--green); }}
        .negative {{ color: var(--red); }}
        .subtext {{ font-size: 11px; color: var(--text-muted); }}
        
        .badge {{
            display: inline-block;
            padding: 2px 7px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 600;
        }}
        .badge.green {{ background: var(--green-bg); color: var(--green); }}
        .badge.red {{ background: var(--red-bg); color: var(--red); }}
        .badge.amber {{ background: var(--amber-bg); color: var(--amber); }}
        
        .pill-sektor {{
            background: #e2e8f0;
            color: var(--navy-dark);
            font-size: 10.5px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        
        .btn-arkiv {{
            display: inline-block;
            background: var(--navy-dark);
            color: #ffffff;
            text-decoration: none;
            padding: 5px 10px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 11.5px;
        }}
        .btn-arkiv:hover {{ background: #0f172a; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">
                <h1>🏛️ Masterarkiv — Budsjettansvarlige (41 Enhetsarkiver)</h1>
                <p>Kristiansand Kommune — AI Project Controller Hub | Lead Controller: Frank Ellingsen</p>
            </div>
            <div class="meta-stats">
                <div>Totalt: <strong>41 budsjettansvarlige</strong></div>
                <div>Status: <span class="badge green">RLS &amp; Stage-Gate Port 9 Aktiv</span></div>
            </div>
        </div>

        <div class="filter-bar">
            <div class="filter-group">
                <span style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Sektor:</span>
                <button class="filter-btn active" onclick="filterSektor('ALL', this)">Alle (41)</button>
                <button class="filter-btn" onclick="filterSektor('HELSE', this)">🏥 Helse (12)</button>
                <button class="filter-btn" onclick="filterSektor('OPPVEKST', this)">🎓 Oppvekst (12)</button>
                <button class="filter-btn" onclick="filterSektor('BYUTVIKLING', this)">🏗️ Byutvikling (6)</button>
                <button class="filter-btn" onclick="filterSektor('KULTUR', this)">🎭 Kultur (3)</button>
                <button class="filter-btn" onclick="filterSektor('ORG_TEK', this)">💻 Org &amp; Tek (3)</button>
                <button class="filter-btn" onclick="filterSektor('OKONOMI', this)">📊 Økonomi &amp; Finans (5)</button>
            </div>
            <div>
                <input class="search-input" id="search-box" type="text" placeholder="🔍 Søk enhet, leder, ansvar..." onkeyup="filterSearch(this.value)">
            </div>
        </div>

        <table id="arkiv-table">
            <thead>
                <tr>
                    <th>Ansvar</th>
                    <th>Enhet &amp; Budsjettansvarlig</th>
                    <th>Sektor</th>
                    <th>Nivå</th>
                    <th class="num">Årsbudsjett</th>
                    <th class="num">Regnskap YTD</th>
                    <th class="num">Avvik (Budsjett - Actuals)</th>
                    <th>Status</th>
                    <th>Handlinger</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>

    <script>
        let currentSektor = 'ALL';

        function filterSektor(sektor, btn) {{
            currentSektor = sektor;
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            applyFilters();
        }}

        function filterSearch(query) {{
            applyFilters();
        }}

        function applyFilters() {{
            const q = document.getElementById('search-box').value.toLowerCase().trim();
            const rows = document.querySelectorAll('#arkiv-table tbody tr');

            rows.forEach(r => {{
                const s = r.getAttribute('data-sektor');
                const text = r.textContent.toLowerCase();

                const matchSektor = (currentSektor === 'ALL' || s === currentSektor);
                const matchSearch = (!q || text.includes(q));

                if (matchSektor && matchSearch) {{
                    r.style.display = '';
                }} else {{
                    r.style.display = 'none';
                }}
            }});
        }}
    </script>
</body>
</html>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)


def build_all_archives():
    """Hovedfunksjon: Bygger alle 41 individuelle rapportarkiver."""
    holders = get_budget_holders_from_db()
    print(f"Bygger individuelle rapportarkiver for {len(holders)} budsjettansvarlige...")

    all_holders_data = []

    for i, h in enumerate(holders, 1):
        aid = h["ansvar_id"]
        safe_aid = aid.strip()
        unit_dir = ARCHIVE_ROOT / safe_aid

        # 4 undermapper per enhet
        dir_maanedsrapporter = unit_dir / "01_Maanedsrapporter"
        dir_kontoutskrifter = unit_dir / "02_Kontoutskrifter"
        dir_saksdokumenter = unit_dir / "03_Saksdokumenter_og_Maler"
        dir_framsikt = unit_dir / "04_Framsikt_Omdisponering"

        for d in [dir_maanedsrapporter, dir_kontoutskrifter, dir_saksdokumenter, dir_framsikt]:
            d.mkdir(parents=True, exist_ok=True)

        # 1. Beregn nøkkeltall for M9 og M10
        m9 = calculate_unit_metrics(h, month=9)
        m10 = calculate_unit_metrics(h, month=10)

        # 2. Generer månedlige PDF- og HTML-rapporter inn i 01_Maanedsrapporter/
        pdf_m9 = dir_maanedsrapporter / "Maanedsrapport_M09_2026.pdf"
        html_m9 = dir_maanedsrapporter / "Maanedsrapport_M09_2026.html"
        pdf_m10 = dir_maanedsrapporter / "Maanedsrapport_M10_2026.pdf"
        html_m10 = dir_maanedsrapporter / "Maanedsrapport_M10_2026.html"

        generate_pdf_report(m9, pdf_m9)
        generate_html_report(m9, html_m9)
        generate_pdf_report(m10, pdf_m10)
        generate_html_report(m10, html_m10)

        # 3. Knytt til kontoutskrift i 02_Kontoutskrifter/
        source_konto = KONTOUTSKRIFTER_DIR / f"KONTOUTSKRIFT_{aid.replace('-', '_')}_M10.html"
        dest_konto = dir_kontoutskrifter / f"KONTOUTSKRIFT_{aid}_M10.html"
        if source_konto.exists():
            shutil.copy2(source_konto, dest_konto)
        else:
            # Fallback til standard kontoutskriftsvisning
            with open(dest_konto, "w", encoding="utf-8") as f:
                f.write(f"<!DOCTYPE html><html><body><h1>Kontoutskrift {aid}</h1><p>Disponibel saldo og transaksjoner for {h['enhet_navn']}.</p></body></html>")

        # 4. Knytt til saksdokumenter og maler i 03_Saksdokumenter_og_Maler/
        primary_mal_rel = h.get("tilknyttet_mal", "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx")
        primary_mal_docx = ROOT_DIR / primary_mal_rel
        primary_mal_md = ROOT_DIR / primary_mal_rel.replace(".docx", ".md")

        if primary_mal_docx.exists():
            shutil.copy2(primary_mal_docx, dir_saksdokumenter / primary_mal_docx.name)
        if primary_mal_md.exists():
            shutil.copy2(primary_mal_md, dir_saksdokumenter / primary_mal_md.name)

        # Tilleggsmaler etter sektor
        for t in get_sector_templates(h["sektor_kode"], h["niva"]):
            if t.exists():
                shutil.copy2(t, dir_saksdokumenter / t.name)

        # 5. Framsikt omdisponeringsfiler i 04_Framsikt_Omdisponering/
        create_framsikt_unit_files(m9, dir_framsikt)

        # 6. Personlig arkivdashbord og README i rot av enhetsmappen
        overview_html = unit_dir / "ARKIV_OVERSIKT.html"
        readme_md = unit_dir / "README.md"
        generate_personal_archive_html(h, m9, m10, overview_html)
        generate_personal_readme(h, m9, readme_md)

        all_holders_data.append({
            "holder": h,
            "m9": m9,
            "m10": m10
        })

        if i % 10 == 0 or i == len(holders):
            print(f"  ✓ {i}/{len(holders)} enhetsarkiver fullført...")

    # 7. Generer Master Index over alle 41 arkiver
    master_index_path = ARCHIVE_ROOT / "index.html"
    generate_master_archive_index(all_holders_data, master_index_path)
    print(f"\n✓ Masterarkiv-portal generert: {master_index_path}")
    print(f"✓ Totalt {len(holders)} individuelle rapportarkiver opprettet i: {ARCHIVE_ROOT}")


def main():
    parser = argparse.ArgumentParser(description="Bygg individuelle rapportarkiver for budsjettansvarlige.")
    parser.add_argument("--unit", type=str, default=None, help="Filtrer på spesifikk ansvar_id.")
    args = parser.parse_args()

    build_all_archives()


if __name__ == "__main__":
    main()
