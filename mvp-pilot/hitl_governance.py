#!/usr/bin/env python3
"""
Human-in-the-Loop (HITL) Governance & Excel Writeback Module
Audits decisions into SQLite and synchronizes approved measures back to
both 'Rapport Enhet Bo og Miljø.xlsx' and 'Mini_case_AI_kommunal_okonomistyring.xlsx'.
"""

from pathlib import Path
from datetime import datetime
import sqlite3
import shutil
import openpyxl

try:
    from config import EXCEL_SOURCE, EXCEL_RAPPORT_BO_MILJO, DB_SQLITE, DEFAULT_ENHET, DEFAULT_SAKSBEHANDLER
    from prescriptive_agent import DEFAULT_CANDIDATE_MEASURES
except ImportError:
    from mvp_pilot.config import EXCEL_SOURCE, EXCEL_RAPPORT_BO_MILJO, DB_SQLITE, DEFAULT_ENHET, DEFAULT_SAKSBEHANDLER
    from mvp_pilot.prescriptive_agent import DEFAULT_CANDIDATE_MEASURES


def record_audit_action(
    enhet_kode: str,
    ai_model: str,
    measure_id: str,
    measure_title: str,
    estimated_effect: float,
    confidence_score: float,
    decision: str,
    control_documented: str,
    justification: str,
    approved_by: str,
    db_path: Path = DB_SQLITE
):
    """Lagrer et formelt, kryptografisk forseglet revisjonsspor i Audit_AI_Actions tabellen i SQLite."""
    import hashlib
    raw_signature = f"{enhet_kode}|{measure_id}|{estimated_effect}|{decision}|{control_documented}|{approved_by}"
    sha256_hash = hashlib.sha256(raw_signature.encode("utf-8")).hexdigest()

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO Audit_AI_Actions (
            enhet_kode, ai_model, measure_id, measure_title, estimated_effect,
            confidence_score, decision, control_documented, justification, approved_by, sha256_hash
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        enhet_kode, ai_model, measure_id, measure_title, estimated_effect,
        confidence_score, decision, control_documented, justification, approved_by, sha256_hash
    ))
    con.commit()
    con.close()
    print(f"[AUDIT] Vedtak logget i SQLite med SHA-256 [{sha256_hash[:12]}...] for tiltak {measure_id}: {decision} av {approved_by}")


def writeback_to_bo_miljo_report(
    decisions_dict: dict,
    excel_path: Path = EXCEL_RAPPORT_BO_MILJO,
    approved_by: str = DEFAULT_SAKSBEHANDLER
) -> dict:
    """Oppdaterer sheet '4 HITL Signoff & Governance' i Rapport Enhet Bo og Miljø.xlsx."""
    if not excel_path.exists():
        return {"updated": False, "reason": "Filen finnes ikke"}

    wb = openpyxl.load_workbook(excel_path, data_only=False)
    sheet_name = "4 HITL Signoff & Governance"
    if sheet_name not in wb.sheetnames:
        return {"updated": False, "reason": f"Mangler arket '{sheet_name}'"}

    ws = wb[sheet_name]
    today_str = datetime.now().strftime("%Y-%m-%d")

    total_godkjent_effekt = 0.0
    antall_godkjente = 0

    # Rader 8 til 13 er tiltakene T1..T6
    for r in range(8, 14):
        mid = str(ws.cell(r, 1).value or "").strip()
        if mid in decisions_dict:
            dec_info = decisions_dict[mid]
            status = dec_info.get("decision", "Kandidat")
            kontroll = dec_info.get("control_documented", "Nei")
            begrunnelse = dec_info.get("justification", "")

            # F: Beslutning
            ws.cell(r, 6).value = status
            # G: Kontroll dokumentert
            ws.cell(r, 7).value = kontroll
            # H: Formel bevares (=IF(AND(F8="Godkjent",G8="Ja"),C8,0))
            ws.cell(r, 8).value = f'=IF(AND(F{r}="Godkjent",G{r}="Ja"),C{r},0)'
            # I: Faglig begrunnelse
            if begrunnelse:
                ws.cell(r, 9).value = begrunnelse
            # J: Godkjent Av
            ws.cell(r, 10).value = approved_by
            # K: Sign-off Dato
            ws.cell(r, 11).value = today_str
            # L: Formel for revisjonsstatus
            ws.cell(r, 12).value = f'=IF(AND(F{r}="Godkjent",G{r}="Ja"),"GYLDIG VEDTAK",IF(F{r}="Godkjent","MANGLER KONTROLL",IF(F{r}="Avvist","AVVIST","KANDIDAT")))'

            effekt = float(ws.cell(r, 3).value or 0.0)
            if status == "Godkjent" and kontroll == "Ja":
                total_godkjent_effekt += effekt
                antall_godkjente += 1

    try:
        wb.save(excel_path)
        print(f"[HITL] Oppdatert '{excel_path.name}' -> {antall_godkjente} godkjente tiltak ({total_godkjent_effekt:,.2f} kr)")
        return {
            "updated": True,
            "file": str(excel_path),
            "antall_godkjente": antall_godkjente,
            "godkjent_effekt": total_godkjent_effekt
        }
    except PermissionError:
        print(f"[HITL ADVARSEL] Kunne ikke lagre til {excel_path.name}: Filen er åpen i Excel.")
        return {
            "updated": False,
            "file": str(excel_path),
            "reason": "Filen er åpen i Excel. Lukk arbeidsboken for å skrive tilbake.",
            "antall_godkjente": antall_godkjente,
            "godkjent_effekt": total_godkjent_effekt
        }


def writeback_to_mini_case(
    decisions_dict: dict,
    excel_path: Path = EXCEL_SOURCE,
    create_backup: bool = True
) -> dict:
    """Oppdaterer sheet '3 AI tiltak og effekt' i Mini_case_AI_kommunal_okonomistyring.xlsx."""
    if not excel_path.exists():
        return {"updated": False, "reason": "Filen finnes ikke"}

    if create_backup:
        backup_path = excel_path.parent / f"{excel_path.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        try:
            shutil.copy2(excel_path, backup_path)
        except PermissionError:
            pass

    wb = openpyxl.load_workbook(excel_path, data_only=False)
    sheet_name = "3 AI tiltak og effekt"
    if sheet_name not in wb.sheetnames:
        return {"updated": False, "reason": f"Mangler arket '{sheet_name}'"}

    ws = wb[sheet_name]
    total_godkjent_effekt = 0.0
    antall_godkjente = 0

    for r in range(6, 12):
        # Sjekk både kolonne 1 og kolonne 2 for mid
        c1_val = str(ws.cell(r, 1).value or "").strip()
        c2_val = str(ws.cell(r, 2).value or "").strip()
        mid = c1_val if c1_val.startswith("T") else c2_val

        if mid in decisions_dict:
            dec_info = decisions_dict[mid]
            status = dec_info.get("decision", "Kandidat")
            kontroll = dec_info.get("control_documented", "Nei")
            begrunnelse = dec_info.get("justification", "")

            # Kolonne M: Beslutning (col 13)
            ws.cell(r, 13).value = status
            # Kolonne N: Kontroll dokumentert (col 14)
            ws.cell(r, 14).value = kontroll

            if begrunnelse:
                ws.cell(r, 16).value = f"{ws.cell(r, 16).value or ''} | Notat: {begrunnelse}".strip(" |")

            effekt = float(ws.cell(r, 8).value or 0.0)
            if status == "Godkjent" and kontroll == "Ja":
                total_godkjent_effekt += effekt
                antall_godkjente += 1

    try:
        wb.save(excel_path)
        print(f"[HITL] Oppdatert '{excel_path.name}' -> {antall_godkjente} godkjente tiltak ({total_godkjent_effekt:,.2f} kr)")
        return {
            "updated": True,
            "file": str(excel_path),
            "antall_godkjente": antall_godkjente,
            "godkjent_effekt": total_godkjent_effekt
        }
    except PermissionError:
        print(f"[HITL ADVARSEL] Kunne ikke lagre til {excel_path.name}: Filen er åpen i Excel.")
        return {
            "updated": False,
            "file": str(excel_path),
            "reason": "Filen er åpen i Excel. Lukk arbeidsboken for å skrive tilbake.",
            "antall_godkjente": antall_godkjente,
            "godkjent_effekt": total_godkjent_effekt
        }


def apply_decisions_and_writeback(
    decisions_dict: dict,
    target_excel: Path = None,
    create_backup: bool = True,
    approved_by: str = DEFAULT_SAKSBEHANDLER
) -> dict:
    """
    Overordnet synkroniseringsmetode som oppdaterer:
    1. 'Rapport Enhet Bo og Miljø.xlsx' (hovedrapport for Bo og Miljø)
    2. 'Mini_case_AI_kommunal_okonomistyring.xlsx' (dersom tilstede)
    3. SQLite Audit_AI_Actions revisjonslogg
    """
    measures_by_id = {m["id"]: m for m in DEFAULT_CANDIDATE_MEASURES}

    # 1. Logg til SQLite revisjonsspor
    for mid, dec_info in decisions_dict.items():
        m_meta = measures_by_id.get(mid, {})
        status = dec_info.get("decision", "Kandidat")
        kontroll = dec_info.get("control_documented", "Nei")
        begrunnelse = dec_info.get("justification", "")
        effekt = m_meta.get("eoy_effect", 0.0)

        record_audit_action(
            enhet_kode=DEFAULT_ENHET,
            ai_model="Ollama llama3.1 (Prescriptive Agent)",
            measure_id=mid,
            measure_title=m_meta.get("title", f"Tiltak {mid}"),
            estimated_effect=effekt,
            confidence_score=m_meta.get("probability", 0.8),
            decision=status,
            control_documented=kontroll,
            justification=begrunnelse,
            approved_by=approved_by
        )

    # 2. Skriv tilbake til Rapport Enhet Bo og Miljø.xlsx
    res_bo = writeback_to_bo_miljo_report(decisions_dict, EXCEL_RAPPORT_BO_MILJO, approved_by)

    # 3. Skriv tilbake til Mini_case hvis target_excel er spesifisert eller standard kilde
    res_mini = writeback_to_mini_case(decisions_dict, target_excel or EXCEL_SOURCE, create_backup)

    antall_godkjente = res_bo.get("antall_godkjente", res_mini.get("antall_godkjente", 0))
    godkjent_effekt = res_bo.get("godkjent_effekt", res_mini.get("godkjent_effekt", 0.0))

    return {
        "bo_miljo_report": res_bo,
        "mini_case": res_mini,
        "target_file": str(target_excel or EXCEL_RAPPORT_BO_MILJO),
        "antall_godkjente": antall_godkjente,
        "godkjent_effekt": godkjent_effekt,
        "approved_by": approved_by
    }


if __name__ == "__main__":
    # Testkjøring med godkjenning av T1 og T2
    test_decisions = {
        "T1": {
            "decision": "Godkjent",
            "control_documented": "Ja",
            "justification": "Krav avstemt mot NAV refusjonsportal; 41k bekreftet."
        },
        "T2": {
            "decision": "Godkjent",
            "control_documented": "Ja",
            "justification": "Drøftet med tillitsvalgt iht. HTA § 4; vikarstopp på dagtid."
        },
        "T3": {
            "decision": "Kandidat",
            "control_documented": "Nei",
            "justification": "Drøftes videre i turnusutvalg."
        }
    }
    res = apply_decisions_and_writeback(test_decisions, create_backup=False)
    print("Fullført writeback:", res)
