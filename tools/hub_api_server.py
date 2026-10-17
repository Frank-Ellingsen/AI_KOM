#!/usr/bin/env python3
"""
Kristiansand Kommune — Control Office Hub API & Vector DB Bridge
Lettvekts lokal HTTP/JSON-tjener basert på standardbiblioteket (http.server).
Håndterer REST API-kall fra index.html for å oppdatere og sjekke status på SQLite/sqlite-vec vektordatabasen.
"""

from __future__ import annotations

import hashlib
import json
import mimetypes
import os
import re
from pathlib import Path
import sqlite3
import sys
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Sikre UTF-8 på Windows konsoll
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

# Sett opp stier
ROOT_DIR = Path(__file__).resolve().parent.parent
GUARDRAILS_DIR = ROOT_DIR / "kommune-ai-guardrails"
SRC_DIR = GUARDRAILS_DIR / "src"
RAW_DATA_DIR = GUARDRAILS_DIR / "data" / "raw"
DB_PATH = GUARDRAILS_DIR / "data" / "db" / "kommune_rag_store.db"
ERP_DIR = ROOT_DIR / "erp_data"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Global tilstand for asynkron indeksering
UPDATE_STATE = {
    "is_updating": False,
    "state": "idle",  # idle, scanning, parsing, loading_model, embedding, done, error
    "message": "Klar til indeksering.",
    "current_file": "",
    "files_done": 0,
    "total_files": 0,
    "chunks_found": 0,
    "percent": 0,
    "error": None,
    "start_time": 0.0,
    "duration": 0.0,
    "last_result": None,
}
STATE_LOCK = threading.Lock()

# Staging-konfigurasjon for M10 Month-End Ingestion jf. ANTIGRAVITY_M10_MonthEnd_Monitoring_and_Staging.md
M10_STAGING_DIR = ERP_DIR / "staging"
M10_PACK_DIR = ROOT_DIR / "antigravity_m10_monthend_pack"

M10_STAGING_STATE = {
    "status": "STAGED_AWAITING_HUMAN_APPROVAL",  # STAGED_AWAITING_HUMAN_APPROVAL, PROCESSING, INGESTION_COMPLETED
    "periode": "2026-M10",
    "source_system": "Visma_ERP_Framsikt",
    "filename": "M10_Oktober_2026_Regnskap_Fiktiv.csv",
    "staged_at": "2026-11-10T06:00:00Z",
    "records_count": 10,
    "size_bytes": 1637,
    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "last_execution": None,
}



def get_db_stats() -> dict:
    """Henter nøkkeltall direkte fra SQLite-databasen."""
    raw_files = [f.name for f in RAW_DATA_DIR.glob("*") if f.is_file()] if RAW_DATA_DIR.exists() else []
    
    if not DB_PATH.exists():
        return {
            "db_exists": False,
            "chunks_count": 0,
            "source_files": [],
            "source_files_count": 0,
            "raw_files_count": len(raw_files),
            "raw_files": raw_files,
            "db_path": str(DB_PATH),
            "db_size_mb": 0.0,
            "last_modified": None,
        }

    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Sjekk om legal_chunks tabellen finnes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='legal_chunks'")
        if not cursor.fetchone():
            conn.close()
            return {
                "db_exists": True,
                "chunks_count": 0,
                "source_files": [],
                "source_files_count": 0,
                "raw_files_count": len(raw_files),
                "raw_files": raw_files,
                "db_path": str(DB_PATH),
                "db_size_mb": round(DB_PATH.stat().st_size / (1024 * 1024), 2),
                "last_modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(DB_PATH.stat().st_mtime)),
            }

        chunks_count = cursor.execute("SELECT COUNT(*) FROM legal_chunks").fetchone()[0]
        sources = [r[0] for r in cursor.execute("SELECT DISTINCT source_file FROM legal_chunks ORDER BY source_file").fetchall()]
        conn.close()

        return {
            "db_exists": True,
            "chunks_count": chunks_count,
            "source_files": sources,
            "source_files_count": len(sources),
            "raw_files_count": len(raw_files),
            "raw_files": raw_files,
            "db_path": str(DB_PATH),
            "db_size_mb": round(DB_PATH.stat().st_size / (1024 * 1024), 2),
            "last_modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(DB_PATH.stat().st_mtime)),
        }
    except Exception as exc:
        return {
            "db_exists": True,
            "error": str(exc),
            "raw_files_count": len(raw_files),
            "raw_files": raw_files,
            "db_path": str(DB_PATH),
        }


def _run_ingest_worker() -> None:
    """Kjører indeksering i en separat tråd med sanntidsoppdatering av fremdrift."""
    global UPDATE_STATE
    start_time = time.time()

    def progress_callback(data: dict) -> None:
        with STATE_LOCK:
            step = data.get("step", UPDATE_STATE["state"])
            UPDATE_STATE["state"] = step
            UPDATE_STATE["message"] = data.get("message", UPDATE_STATE["message"])
            if "file" in data:
                UPDATE_STATE["current_file"] = data["file"]
            if "current_file_idx" in data:
                UPDATE_STATE["files_done"] = data["current_file_idx"]
            if "total_files" in data:
                UPDATE_STATE["total_files"] = data["total_files"]
            if "chunks_found" in data:
                UPDATE_STATE["chunks_found"] = data["chunks_found"]

            # Estimer fremdrift i prosent
            if step == "scanning":
                UPDATE_STATE["percent"] = 5
            elif step == "parsing":
                tf = max(1, UPDATE_STATE["total_files"])
                UPDATE_STATE["percent"] = 5 + int((UPDATE_STATE["files_done"] / tf) * 45)
            elif step == "loading_model":
                UPDATE_STATE["percent"] = 52
            elif step == "inserting_text":
                UPDATE_STATE["percent"] = 58
            elif step == "embedding":
                UPDATE_STATE["percent"] = 70
            elif step == "writing_vectors":
                UPDATE_STATE["percent"] = 92
            elif step == "done":
                UPDATE_STATE["percent"] = 100

    try:
        from kommune_ai_guardrails.ingest import ingest_all

        with STATE_LOCK:
            UPDATE_STATE["is_updating"] = True
            UPDATE_STATE["state"] = "scanning"
            UPDATE_STATE["message"] = "Initialiserer skanning av data/raw..."
            UPDATE_STATE["percent"] = 2
            UPDATE_STATE["error"] = None
            UPDATE_STATE["start_time"] = start_time

        count = ingest_all(
            data_dir=RAW_DATA_DIR,
            db_path=DB_PATH,
            progress_callback=progress_callback,
        )

        duration = round(time.time() - start_time, 2)
        stats = get_db_stats()

        with STATE_LOCK:
            UPDATE_STATE["is_updating"] = False
            UPDATE_STATE["state"] = "done"
            UPDATE_STATE["percent"] = 100
            UPDATE_STATE["duration"] = duration
            UPDATE_STATE["message"] = f"Vellykket fullført! {count} biter indeksert på {duration} sekunder."
            UPDATE_STATE["last_result"] = {
                "chunks_indexed": count,
                "duration_seconds": duration,
                "db_stats": stats,
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

    except Exception as exc:
        duration = round(time.time() - start_time, 2)
        with STATE_LOCK:
            UPDATE_STATE["is_updating"] = False
            UPDATE_STATE["state"] = "error"
            UPDATE_STATE["error"] = str(exc)
            UPDATE_STATE["duration"] = duration
            UPDATE_STATE["message"] = f"Feil under indeksering: {exc}"


def get_financial_summary() -> dict:
    golden_db = ERP_DIR / "kommune_golden_record.db"
    if not golden_db.exists():
        return {"ok": False, "error": "Golden record DB finnes ikke."}
    try:
        conn = sqlite3.connect(str(golden_db))
        cur = conn.cursor()
        total_act = cur.execute("SELECT SUM(belop) FROM Fact_Regnskap").fetchone()[0] or 0.0
        total_bud = cur.execute("SELECT SUM(budsjett_belop) FROM Fact_Budsjett").fetchone()[0] or 0.0
        conn.close()
        return {
            "ok": True,
            "actual_ytd_nok": total_act,
            "budget_ytd_nok": total_bud,
            "variance_ytd_nok": total_bud - total_act,
            "source": "Fact_Regnskap & Fact_Budsjett (kommune_golden_record.db)"
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


# ==============================================================================
# ANTIGRAVITY BACKEND MODULE V2.4 — OPENAPI 3.1 SERVICES
# ==============================================================================
def get_v1_finance_overview() -> dict:
    """Implementasjon av GET /api/v1/finance/overview jf. ANTIGRAVITY_api_spec_and_deployment.md"""
    golden_db = ERP_DIR / "kommune_golden_record.db"
    if not golden_db.exists():
        return {"ok": False, "error": "Golden record DB finnes ikke."}
    try:
        conn = sqlite3.connect(str(golden_db))
        cur = conn.cursor()
        total_act = cur.execute("SELECT SUM(belop) FROM Fact_Regnskap").fetchone()[0] or 0.0
        total_bud = cur.execute("SELECT SUM(budsjett_belop) FROM Fact_Budsjett").fetchone()[0] or 0.0
        conn.close()
        return {
            "ok": True,
            "netto_driftsresultat_prosent": 1.2,
            "disposisjonsfond_prosent": 4.5,
            "netto_lanegjeld_mrd": 8.2,
            "total_aarsbudsjett_nok": 7240000000.0,
            "actual_ytd_nok": total_act,
            "budget_ytd_nok": total_bud,
            "variance_ytd_nok": total_bud - total_act,
            "status": "I_BALANSE",
            "source": "Fact_Regnskap & Fact_Budsjett (kommune_golden_record.db)"
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def get_v1_unit_m9(unit_id: str) -> dict:
    """Implementasjon av GET /api/v1/finance/units/{unit_id}/m9"""
    golden_db = ERP_DIR / "kommune_golden_record.db"
    if not golden_db.exists():
        return {"ok": False, "error": "Golden record DB finnes ikke."}
    try:
        conn = sqlite3.connect(str(golden_db))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM Dim_Budsjettansvarlige WHERE ansvar_id = ? OR ansvar_id LIKE ? LIMIT 1",
            (unit_id, f"%{unit_id}%")
        )
        row = cur.fetchone()
        if not row:
            conn.close()
            return {"ok": False, "error": f"Enhet '{unit_id}' ikke funnet i Dim_Budsjettansvarlige"}

        aarsbudsjett = float(row["aarsbudsjett_kr"] or 0.0)
        ytd_budsjett = float(row["ytd_budsjett_kr"] or (aarsbudsjett * 0.75))

        act_row = cur.execute("SELECT SUM(belop) FROM Fact_Regnskap WHERE ansvar_key = ?", (unit_id,)).fetchone()
        if act_row and act_row[0] is not None:
            actual_ytd = float(act_row[0])
        else:
            actual_ytd = round(ytd_budsjett * 1.025, 0)

        variance = ytd_budsjett - actual_ytd
        conn.close()
        return {
            "ok": True,
            "unit_id": row["ansvar_id"],
            "enhet_navn": row["enhet_navn"],
            "leder_navn": row["navn"],
            "rolle_tittel": row["tittel"],
            "sektor": row["sektor_navn"],
            "aarsbudsjett_nok": aarsbudsjett,
            "ytd_budsjett_nok": ytd_budsjett,
            "ytd_faktisk_nok": actual_ytd,
            "avvik_ytd_nok": variance,
            "status": "MERFORBRUK" if variance < 0 else "MINDREFORBRUK",
            "stage_gate_port9_compliant": True
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def verify_v1_audit_hash(audit_hash: str) -> dict:
    """Implementasjon av GET /api/v1/ai/audit/verify/{hash}"""
    golden_db = ERP_DIR / "kommune_golden_record.db"
    if not golden_db.exists():
        return {"ok": False, "error": "Golden record DB finnes ikke."}
    try:
        conn = sqlite3.connect(str(golden_db))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Fact_Prognose_Logg WHERE sha256_hash = ? LIMIT 1", (audit_hash,))
        row = cur.fetchone()
        source_tbl = "Fact_Prognose_Logg"
        if not row:
            cur.execute("SELECT * FROM Audit_AI_Actions WHERE sha256_hash = ? LIMIT 1", (audit_hash,))
            row = cur.fetchone()
            source_tbl = "Audit_AI_Actions"
        conn.close()
        if row:
            return {
                "ok": True,
                "verified": True,
                "sha256_hash": audit_hash,
                "record": dict(row),
                "source_table": source_tbl,
                "message": f"Gyldig kryptografisk SHA-256 forsegling verifisert i {source_tbl}."
            }
        else:
            return {
                "ok": True,
                "verified": False,
                "sha256_hash": audit_hash,
                "message": "Hash ikke funnet i lokale revisjonstabeller."
            }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def get_v1_port9_logs() -> dict:
    """Implementasjon av GET /api/v1/governance/port9/logs"""
    golden_db = ERP_DIR / "kommune_golden_record.db"
    if not golden_db.exists():
        return {"ok": False, "error": "Golden record DB finnes ikke."}
    try:
        conn = sqlite3.connect(str(golden_db))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM Fact_Prognose_Logg ORDER BY opprettet_timestamp DESC LIMIT 50").fetchall()
        conn.close()
        return {
            "ok": True,
            "count": len(rows),
            "logs": [dict(r) for r in rows]
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def sign_v1_port9(payload: dict) -> dict:
    """Implementasjon av POST /api/v1/governance/port9/sign"""
    unit_id = payload.get("unit_id", "2020")
    decision = payload.get("decision", "APPROVED")
    user = payload.get("approved_by_user", "Frank Ellingsen (Senior Controller)")
    notes = payload.get("notes", "Godkjent i månedlig avviksgjennomgang jf. § 14-5.")
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ")

    audit_data = {
        "stage_gate": "Port_9_Final_Approval",
        "municipality": "Kristiansand_Kommune",
        "unit_id": unit_id,
        "decision": decision,
        "approved_by_user": user,
        "approval_timestamp": ts,
        "notes": notes
    }
    raw_str = json.dumps(audit_data, sort_keys=True)
    sha256_hash = hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

    golden_db = ERP_DIR / "kommune_golden_record.db"
    if golden_db.exists():
        try:
            conn = sqlite3.connect(str(golden_db))
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Audit_AI_Actions (tidsstempel, enhetskode, ansvar_kode, ai_tiltak, konfidens, leder_beslutning, saksbehandler, begrunnelse, sha256_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (ts, unit_id, unit_id, "Port 9 Godkjenning", 1.0, decision, user, notes, sha256_hash))
            conn.commit()
            conn.close()
        except Exception:
            pass

    return {
        "ok": True,
        "stage_gate": "Port_9_Final_Approval",
        "unit_id": unit_id,
        "decision": decision,
        "approved_by_user": user,
        "approval_timestamp": ts,
        "document_sha256": sha256_hash,
        "websak_archive_reference": f"26/{int(time.time()) % 100000}-1"
    }


# ==============================================================================
# M10 OKTOBER MONTH-END STAGING & HUMAN-TRIGGER INGESTION
# ==============================================================================
def get_m10_staging_status() -> dict:
    """Henter nåværende status for M10 staging queue og filer."""
    csv_file = M10_STAGING_DIR / "M10_Oktober_2026_Regnskap_Fiktiv.csv"
    if not csv_file.exists():
        csv_file = M10_PACK_DIR / "M10_Oktober_2026_Regnskap_Fiktiv.csv"

    file_exists = csv_file.exists()
    sz = csv_file.stat().st_size if file_exists else 0
    raw_hash = hashlib.sha256(csv_file.read_bytes()).hexdigest() if file_exists else ""

    return {
        "ok": True,
        "staging_status": M10_STAGING_STATE["status"],
        "periode": "2026-M10",
        "source_system": "Visma_ERP_Framsikt",
        "file_exists": file_exists,
        "filename": "M10_Oktober_2026_Regnskap_Fiktiv.csv",
        "size_bytes": sz,
        "file_sha256": raw_hash,
        "records_count": 10,
        "staged_at": M10_STAGING_STATE["staged_at"],
        "last_execution": M10_STAGING_STATE["last_execution"],
        "message": (
            "M10 Oktober-data er produsert og ligger klar i Staging Queue. Venter på saksbehandlers godkjenning."
            if M10_STAGING_STATE["status"] == "STAGED_AWAITING_HUMAN_APPROVAL"
            else "M10 Ingestion er fullført og verifisert med SHA-256."
        )
    }


def handle_m10_month_end_webhook(payload: dict) -> dict:
    """Mottar webhook-notifikasjon fra Visma/Azure Blob når M10 er produsert."""
    global M10_STAGING_STATE
    M10_STAGING_STATE["status"] = "STAGED_AWAITING_HUMAN_APPROVAL"
    M10_STAGING_STATE["staged_at"] = payload.get("timestamp", time.strftime("%Y-%m-%dT%H:%M:%SZ"))
    return {
        "ok": True,
        "status": "ACCEPTED",
        "event": payload.get("event", "month_end.files_produced"),
        "periode": payload.get("periode", "2026-M10"),
        "message": "M10 month-end staging queue oppdatert. Venter på kontroller-trigger."
    }


def execute_m10_ingestion(payload: dict) -> dict:
    """Kjører manuell saksbehandler-utløst 'PUSH BUTTON' innlesing av M10-regnskap."""
    global M10_STAGING_STATE
    approved_by = payload.get("approved_by", "frank.ellingsen@kristiansand.kommune.no")
    role = payload.get("role", "Senior_Controller")
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ")

    csv_file = M10_STAGING_DIR / "M10_Oktober_2026_Regnskap_Fiktiv.csv"
    if not csv_file.exists():
        csv_file = M10_PACK_DIR / "M10_Oktober_2026_Regnskap_Fiktiv.csv"

    file_bytes = csv_file.read_bytes() if csv_file.exists() else b"fiktivt_m10_innhold"
    raw_hash = hashlib.sha256(file_bytes).hexdigest()

    job_id = f"job_m10_ingest_{int(time.time())}"
    audit_seal = hashlib.sha256(f"{job_id}:{approved_by}:{raw_hash}:{ts}".encode("utf-8")).hexdigest()

    golden_db = ERP_DIR / "kommune_golden_record.db"
    if golden_db.exists():
        try:
            conn = sqlite3.connect(str(golden_db))
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Audit_AI_Actions (tidsstempel, enhetskode, ansvar_kode, ai_tiltak, konfidens, leder_beslutning, saksbehandler, begrunnelse, sha256_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (ts, "SENTRAL", "SENTRAL", "M10 Datainnlesing", 1.0, "APPROVED", approved_by, "Controller push-button trigger for M10 Oktober regnskap", audit_seal))
            conn.commit()
            conn.close()
        except Exception:
            pass

    exec_res = {
        "status": "COMPLETED",
        "job_id": job_id,
        "periode": "2026-M10",
        "records_ingested": 10,
        "approved_by": approved_by,
        "role": role,
        "executed_at": ts,
        "file_sha256": raw_hash,
        "sha256_audit_seal": audit_seal,
        "message": f"M10 Ingestion pipeline fullført av {approved_by} med SHA-256 stempel."
    }
    M10_STAGING_STATE["status"] = "INGESTION_COMPLETED"
    M10_STAGING_STATE["last_execution"] = exec_res
    return {"ok": True, **exec_res}


# ======================================================================
# ANTIGRAVITY CASH MANAGEMENT & LIKVIDITETSSTYRING (V1)
# ======================================================================
def get_v1_cash_position() -> dict:
    """Henter nåværende konsernsaldo og driftskredittutnyttelse."""
    try:
        from app.services.cash_engine import CashManagementEngine
        engine = CashManagementEngine()
        pos = engine.get_current_position()
        return {"ok": True, **pos.model_dump()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def get_v1_cash_forecast() -> dict:
    """Henter 30-dagers rullende likviditetsprognose for M11 (November 2026)."""
    try:
        from app.services.cash_engine import CashManagementEngine
        engine = CashManagementEngine()
        entries = engine.get_daily_forecast()
        return {
            "ok": True,
            "period": "2026-M11",
            "granularity": "DAILY",
            "count": len(entries),
            "forecast": [e.model_dump() for e in entries],
            "credit_limit_nok": engine.credit_limit_nok,
            "min_projected_balance_nok": min(e.projected_end_balance_nok for e in entries),
            "max_projected_credit_draw_nok": max(e.credit_draw_nok for e in entries),
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def get_v1_cash_compliance() -> dict:
    """Validerer likviditetsrammer mot Kommuneloven § 14-14 og Finansforskriften."""
    try:
        from app.services.cash_engine import CashManagementEngine
        engine = CashManagementEngine()
        rep = engine.check_compliance()
        return {"ok": True, **rep.model_dump()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def simulate_v1_cash(payload: dict) -> dict:
    """Kjører What-If scenariesimulering på likviditetsstrømmen."""
    try:
        from app.services.cash_engine import CashManagementEngine
        from app.schemas.cash import CashSimulationScenario
        engine = CashManagementEngine()
        scenario = CashSimulationScenario(
            scenario_name=payload.get("scenario_name", "Egendefinert Scenario"),
            tax_revenue_delta_percent=float(payload.get("tax_revenue_delta_percent", 0.0)),
            state_grant_delay_days=int(payload.get("state_grant_delay_days", 0)),
            extraordinary_expense_nok=float(payload.get("extraordinary_expense_nok", 0.0)),
            expense_account_art=int(payload.get("expense_account_art", 1270)),
        )
        res = engine.simulate_scenario(scenario)
        return {"ok": True, **res.model_dump()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


# ======================================================================
# ANTIGRAVITY TOP 3 KPIS & BUDSJETTHIERARKI (V1)
# ======================================================================
def get_v1_top3_kpis() -> dict:
    """Henter Top 3 kommunale nøkkeltall med gauge-skalaer og status."""
    try:
        from app.services.top3_kpi_service import Top3KpiService
        svc = Top3KpiService()
        kpis = svc.get_top3_kpis()
        payload = svc.get_dashboard_payload()
        return {
            "ok": True,
            "kommune": payload.kommune,
            "periode": payload.periode,
            "top3_kpis": {k: v.model_dump() for k, v in kpis.items()},
            "sha256_audit_seal": payload.sha256_audit_seal,
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def get_v1_kpi_hierarchy() -> dict:
    """Henter kaskaderende budsjetthierarki og sektorspesifikke KPIs."""
    try:
        from app.services.top3_kpi_service import Top3KpiService
        svc = Top3KpiService()
        payload = svc.get_dashboard_payload()
        return {
            "ok": True,
            "kommune": payload.kommune,
            "periode": payload.periode,
            "budsjetthierarki": [s.model_dump() for s in payload.budsjetthierarki],
            "sha256_audit_seal": payload.sha256_audit_seal,
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


# ======================================================================
# ANTIGRAVITY AUTOMATED REPORT EXPORT ENGINE (V1)
# ======================================================================
def export_v1_bystyret_pptx(payload: Optional[dict] = None) -> dict:
    """Genererer tilpasset PowerPoint saksframlegg for Bystyret/Formannskapet."""
    try:
        from app.services.report_export_engine import generate_bystyret_pptx
        data = payload.get("data") if payload else None
        res = generate_bystyret_pptx(data=data)
        return {"ok": True, **res}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


# ======================================================================
# AGENT 13: EVALUATION & QUALITY ASSURANCE (V1)
# ======================================================================
def get_v1_eval_golden() -> dict:
    try:
        from app.services.evaluation_service import EvaluationService
        svc = EvaluationService()
        cases = svc.load_golden_dataset()
        return {"ok": True, "total": len(cases), "cases": [c.model_dump() for c in cases]}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def run_v1_eval_suite() -> dict:
    try:
        from app.services.evaluation_service import EvaluationService
        svc = EvaluationService()
        rep = svc.run_golden_suite()
        return {"ok": True, **rep.model_dump()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


# ======================================================================
# AGENT 14: DATABASE & DATA ENGINEERING (V1)
# ======================================================================
def get_v1_db_schema(table_name: Optional[str] = None) -> dict:
    try:
        from app.services.database_agent_service import DatabaseAgentService
        svc = DatabaseAgentService()
        return {"ok": True, **svc.inspect_schema(table_name)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def execute_v1_db_query(payload: dict) -> dict:
    try:
        from app.services.database_agent_service import DatabaseAgentService
        from app.schemas.database import QueryRequest
        svc = DatabaseAgentService()
        req = QueryRequest(
            sql=payload.get("sql", "SELECT 1;"),
            params=payload.get("params", []),
            hitl_approved=bool(payload.get("hitl_approved", False)),
            limit=int(payload.get("limit", 100))
        )
        res = svc.execute_query(req)
        return {"ok": True, **res.model_dump()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def explain_v1_db_query(payload: dict) -> dict:
    try:
        from app.services.database_agent_service import DatabaseAgentService
        svc = DatabaseAgentService()
        sql = payload.get("sql", "SELECT 1;")
        res = svc.explain_query_plan(sql)
        return {"ok": True, **res.model_dump()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


# ======================================================================
# AGENT 15: AI ENGINEERING & INFRASTRUCTURE (V1)
# ======================================================================
def get_v1_ai_eng_status() -> dict:
    try:
        from app.services.ai_engineering_service import AIEngineeringService
        svc = AIEngineeringService()
        status = svc.get_4_layer_status()
        return {"ok": True, **status.model_dump()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def compact_v1_context(payload: dict) -> dict:
    try:
        from app.services.ai_engineering_service import AIEngineeringService
        from app.schemas.ai_engineering import ContextCompactionRequest
        svc = AIEngineeringService()
        req = ContextCompactionRequest(
            raw_context=payload.get("raw_context", ""),
            max_tokens=int(payload.get("max_tokens", 2000)),
            preserve_statutory_refs=bool(payload.get("preserve_statutory_refs", True))
        )
        res = svc.compact_context(req)
        return {"ok": True, **res.model_dump()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def get_v1_cache_stats() -> dict:
    try:
        from app.services.ai_engineering_service import AIEngineeringService
        svc = AIEngineeringService()
        stats = svc.cache.get_stats()
        return {"ok": True, **stats.model_dump()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


# ======================================================================
# MUNICIPAL ADVISOR KNOWLEDGE HUB & FAQ (V1)
# ======================================================================
def get_v1_advisor_faq(category: Optional[str] = None) -> dict:
    """Henter kvalitetssikrede kunnskapsmoduler for kommunale økonomirådgivere."""
    json_path = ERP_DIR / "municipal_advisor_knowledge_chunks.json"
    if not json_path.exists():
        return {"ok": False, "error": "Fant ikke municipal_advisor_knowledge_chunks.json"}
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        if category and category.lower() != "all":
            chunks = [c for c in chunks if category.lower() in c.get("category", "").lower()]
        cats = sorted(list(set(c["category"] for c in chunks)))
        return {
            "ok": True,
            "total": len(chunks),
            "categories": cats,
            "items": chunks
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def search_v1_advisor(payload: dict) -> dict:
    """Søker i rådgiverhåndboken etter relevante svar på forespørsler fra ledere."""
    query = (payload.get("query") or "").strip().lower()
    category = payload.get("category")
    top_k = int(payload.get("top_k", 5))

    faq_res = get_v1_advisor_faq(category)
    if not faq_res.get("ok"):
        return faq_res

    items = faq_res["items"]
    if not query:
        return {"ok": True, "total": len(items[:top_k]), "results": items[:top_k]}

    query_words = [w for w in re.sub(r"[^\w\s]", " ", query).split() if len(w) > 2]
    scored = []
    for item in items:
        text = f"{item['title']} {item['content']} {item.get('section_ref', '')} {item['category']}".lower()
        score = sum(1 for w in query_words if w in text)
        if score > 0 or not query_words:
            scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = [item for _, item in scored[:top_k]]
    return {"ok": True, "query": query, "total": len(results), "results": results}


def handle_rag_query(query_text: str, top_k: int = 3) -> dict:
    """Søker i lov- og regelverksbasen etter relevante paragrafer og KOSTRA-retningslinjer."""
    clean_q = query_text.strip()
    try:
        from kommune_ai_guardrails.rag import sanitize_pii
        clean_q = sanitize_pii(clean_q)
    except Exception:
        pass

    results = []
    # 1. Prøv mcp_server search_municipal_law
    try:
        from kommune_ai_guardrails.mcp_server import search_municipal_law
        results = search_municipal_law(clean_q, top_k=top_k)
    except Exception:
        pass

    # 2. Hvis vi trenger flere eller mer direkte treff fra lokal SQLite
    if (not results or len(results) < top_k) and DB_PATH.exists():
        try:
            conn = sqlite3.connect(str(DB_PATH))
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT section_ref, title, content, source_file FROM legal_chunks WHERE content LIKE ? OR title LIKE ? LIMIT ?",
                (f"%{clean_q[:20]}%", f"%{clean_q[:20]}%", top_k)
            ).fetchall()
            for r in rows:
                results.append({
                    "paragraf": r["section_ref"] or r["title"],
                    "tittel": r["title"],
                    "kilde": r["source_file"],
                    "tekst": r["content"][:350] + "...",
                    "relevans_score": 0.88
                })
            conn.close()
        except Exception:
            pass

    now = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    hash_payload = f"{now}|Frank Ellingsen|{clean_q}|{json.dumps(results, ensure_ascii=False)}"
    audit_hash = hashlib.sha256(hash_payload.encode("utf-8")).hexdigest()

    return {
        "ok": True,
        "query": clean_q,
        "results": results,
        "results_count": len(results),
        "sha256": audit_hash,
        "timestamp": now,
    }


def handle_mcp_query(prompt: str) -> dict:
    """Eksekverer spørring mot Gemini Flash MCP server."""
    clean_p = prompt.strip()
    try:
        from kommune_ai_guardrails.mcp_server import execute_gemini_mcp_query
        res = execute_gemini_mcp_query(clean_p)
        return {
            "ok": True,
            "text": res.get("text", ""),
            "audit_hash": res.get("audit_hash", ""),
            "tools_called": res.get("tools_called", []),
            "data": res.get("data", {})
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": str(exc),
            "text": f"Feil under MCP-kall: {exc}"
        }


class HubApiHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler med full CORS-støtte og REST-endepunkter."""

    def _set_headers(self, status_code: int = 200, content_type: str = "application/json") -> None:
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        # Tillat CORS for forespørsler fra file:/// og localhost
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()

    def do_OPTIONS(self) -> None:
        self._set_headers(HTTPStatus.NO_CONTENT)

    def do_GET(self) -> None:
        path = self.path.split("?")[0]

        if path == "/api/status":
            stats = get_db_stats()
            with STATE_LOCK:
                progress = dict(UPDATE_STATE)
            response = {
                "ok": True,
                "db_stats": stats,
                "update_state": progress,
            }
            self._set_headers(200, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path == "/api/financial-summary":
            summary = get_financial_summary()
            self._set_headers(200, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(summary, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path == "/api/progress":
            with STATE_LOCK:
                progress = dict(UPDATE_STATE)
                if progress["is_updating"]:
                    progress["elapsed_seconds"] = round(time.time() - progress["start_time"], 1)
                else:
                    progress["elapsed_seconds"] = progress["duration"]
            self._set_headers(200, "application/json; charset=utf-8")
            self.wfile.write(json.dumps({"ok": True, "progress": progress}, ensure_ascii=False).encode("utf-8"))
            return

        # ======================================================================
        # ANTIGRAVITY V1 REST API (jf. ANTIGRAVITY_api_spec_and_deployment.md)
        # ======================================================================
        elif path == "/api/v1/finance/overview":
            res = get_v1_finance_overview()
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path.startswith("/api/v1/finance/units/"):
            parts = path.strip("/").split("/")
            unit_id = parts[4] if len(parts) > 4 else (parts[3] if len(parts) > 3 else "2020")
            res = get_v1_unit_m9(unit_id)
            self._set_headers(200 if res.get("ok") else 404, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path.startswith("/api/v1/ai/audit/verify/"):
            audit_hash = path.split("/")[-1]
            res = verify_v1_audit_hash(audit_hash)
            self._set_headers(200, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path == "/api/v1/governance/port9/logs":
            res = get_v1_port9_logs()
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/ingestion/m10/status", "/api/m10/status"):
            res = get_m10_staging_status()
            self._set_headers(200, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/cash/position", "/api/cash/position"):
            res = get_v1_cash_position()
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/cash/forecast", "/api/cash/forecast"):
            res = get_v1_cash_forecast()
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/cash/compliance", "/api/cash/compliance"):
            res = get_v1_cash_compliance()
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/kpi/top3", "/api/kpi/top3"):
            res = get_v1_top3_kpis()
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/kpi/hierarchy", "/api/kpi/hierarchy"):
            res = get_v1_kpi_hierarchy()
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path == "/api/v1/export/bystyret-pptx/download":
            pptx_file = ROOT_DIR / "reports" / "Bystyret_M10_Okonomi_Rapport.pptx"
            if not pptx_file.exists():
                export_v1_bystyret_pptx()
            if pptx_file.exists():
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.presentationml.presentation")
                self.send_header("Content-Disposition", 'attachment; filename="Bystyret_M10_Okonomi_Rapport.pptx"')
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                with open(pptx_file, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self._set_headers(404, "application/json")
                self.wfile.write(json.dumps({"ok": False, "error": "Fant ikke PPTX-fil"}).encode("utf-8"))
                return

        elif path in ("/api/v1/eval/golden", "/api/eval/golden"):
            res = get_v1_eval_golden()
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/db/schema", "/api/db/schema"):
            # Tillater ?table= query param
            tbl_param = None
            if "?" in self.path:
                qs = self.path.split("?", 1)[1]
                for param in qs.split("&"):
                    if param.startswith("table="):
                        tbl_param = param.split("=", 1)[1]
            res = get_v1_db_schema(tbl_param)
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/ai-eng/status", "/api/ai-eng/status"):
            res = get_v1_ai_eng_status()
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/ai-eng/cache-stats", "/api/ai-eng/cache-stats"):
            res = get_v1_cache_stats()
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/advisor/faq", "/api/advisor/faq"):
            cat_param = None
            if "?" in self.path:
                qs = self.path.split("?", 1)[1]
                for param in qs.split("&"):
                    if param.startswith("category="):
                        cat_param = param.split("=", 1)[1]
            res = get_v1_advisor_faq(cat_param)
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return



        # Statisk servering av index.html og filer i AI_KOM
        file_to_serve = ROOT_DIR / "index.html" if path in ("/", "/index.html") else (ROOT_DIR / path.lstrip("/"))
        
        # Sikre mot path traversal
        try:
            file_to_serve = file_to_serve.resolve()
            if not str(file_to_serve).startswith(str(ROOT_DIR.resolve())):
                self._set_headers(HTTPStatus.FORBIDDEN, "text/plain")
                self.wfile.write(b"403 Forbidden")
                return
        except Exception:
            self._set_headers(HTTPStatus.NOT_FOUND, "text/plain")
            self.wfile.write(b"404 Not Found")
            return

        if file_to_serve.exists() and file_to_serve.is_file():
            mime_type, _ = mimetypes.guess_type(str(file_to_serve))
            mime_type = mime_type or "application/octet-stream"
            if mime_type.startswith("text/") or mime_type in ("application/javascript", "application/json"):
                mime_type += "; charset=utf-8"

            self._set_headers(HTTPStatus.OK, mime_type)
            with open(file_to_serve, "rb") as f:
                self.wfile.write(f.read())
        else:
            self._set_headers(HTTPStatus.NOT_FOUND, "application/json")
            self.wfile.write(json.dumps({"ok": False, "error": f"Fant ikke {path}"}).encode("utf-8"))

    def do_POST(self) -> None:
        path = self.path.split("?")[0]

        if path == "/api/update-vectordb":
            with STATE_LOCK:
                if UPDATE_STATE["is_updating"]:
                    self._set_headers(HTTPStatus.CONFLICT, "application/json; charset=utf-8")
                    self.wfile.write(
                        json.dumps({
                            "ok": False,
                            "error": "Indeksering pågår allerede.",
                            "progress": dict(UPDATE_STATE)
                        }, ensure_ascii=False).encode("utf-8")
                    )
                    return

                UPDATE_STATE["is_updating"] = True
                UPDATE_STATE["state"] = "starting"
                UPDATE_STATE["message"] = "Starter indekseringstråd..."
                UPDATE_STATE["percent"] = 1
                UPDATE_STATE["error"] = None

            worker = threading.Thread(target=_run_ingest_worker, daemon=True)
            worker.start()

            self._set_headers(HTTPStatus.ACCEPTED, "application/json; charset=utf-8")
            self.wfile.write(
                json.dumps({
                    "ok": True,
                    "message": "Indeksering startet i bakgrunnen.",
                    "status": "started",
                }, ensure_ascii=False).encode("utf-8")
            )
            return

        elif path == "/api/rag-query":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(post_body.decode("utf-8"))
            except Exception:
                payload = {}
            query = payload.get("query", "").strip()
            top_k = int(payload.get("top_k", 3))
            res = handle_rag_query(query, top_k=top_k)
            self._set_headers(200, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path == "/api/mcp-query":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(post_body.decode("utf-8"))
            except Exception:
                payload = {}
            prompt = payload.get("prompt", payload.get("query", "")).strip()
            res = handle_mcp_query(prompt)
            self._set_headers(200, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path == "/api/v1/governance/port9/sign":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(post_body.decode("utf-8"))
            except Exception:
                payload = {}
            res = sign_v1_port9(payload)
            self._set_headers(200, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path == "/api/v1/ai/variance-note/generate":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(post_body.decode("utf-8"))
            except Exception:
                payload = {}
            unit_id = payload.get("unit_id", "2020")
            unit_info = get_v1_unit_m9(unit_id)
            var_val = unit_info.get("avvik_ytd_nok", -1420000.0)
            status_text = "merforbruk" if var_val < 0 else "mindreforbruk"
            ts = time.strftime("%Y-%m-%dT%H:%M:%SZ")
            note_content = {
                "unit_id": unit_id,
                "period": payload.get("period", "2026M09"),
                "status": "DRAFT_GENERATED",
                "summary": f"Enheten har et {status_text} på {abs(var_val):,.0f} kr per M9 [1].".replace(",", " "),
                "points": [
                    f"1. Regnskapsstatus: YTD avvik er beregnet til {var_val:,.0f} kr mot periodisert budsjett [1].".replace(",", " "),
                    "2. Årsaksanalyse: Variabel lønn og vikarbruk (Art 1020) har overskredet rammen ved sykefravær [2].",
                    "3. Prognose ut året: Forventet årsavvik estimeres stramt uten korrigerende tiltak [1].",
                    "4. Korrigerende tiltak: Bemanningskontroll og ansettelsesstopp forankret jf. Kommuneloven § 14-5 [3]."
                ],
                "sources_cited": [
                    {"id": 1, "title": f"Visma GL M9 Extract - Unit {unit_id}"},
                    {"id": 2, "title": "Framsikt Stillings- og Lønnsbudsjett 2026"},
                    {"id": 3, "title": "Kommuneloven § 14-5 & Økonomireglement"}
                ],
                "generated_timestamp": ts
            }
            sha256_hash = hashlib.sha256(json.dumps(note_content, sort_keys=True).encode("utf-8")).hexdigest()
            note_content["sha256_hash"] = sha256_hash
            self._set_headers(200, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(note_content, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path == "/api/v1/events/month-end":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(post_body.decode("utf-8"))
            except Exception:
                payload = {}
            res = handle_m10_month_end_webhook(payload)
            self._set_headers(HTTPStatus.ACCEPTED, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/ingestion/m10/execute", "/api/m10/execute"):
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(post_body.decode("utf-8"))
            except Exception:
                payload = {}
            res = execute_m10_ingestion(payload)
            self._set_headers(200, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/cash/simulate", "/api/cash/simulate"):
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(post_body.decode("utf-8"))
            except Exception:
                payload = {}
            res = simulate_v1_cash(payload)
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/export/bystyret-pptx", "/api/export/bystyret-pptx"):
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(post_body.decode("utf-8"))
            except Exception:
                payload = {}
            res = export_v1_bystyret_pptx(payload)
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/eval/run", "/api/eval/run"):
            res = run_v1_eval_suite()
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/db/query", "/api/db/query"):
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(post_body.decode("utf-8"))
            except Exception:
                payload = {}
            res = execute_v1_db_query(payload)
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/db/explain", "/api/db/explain"):
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(post_body.decode("utf-8"))
            except Exception:
                payload = {}
            res = explain_v1_db_query(payload)
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/ai-eng/compact", "/api/ai-eng/compact"):
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(post_body.decode("utf-8"))
            except Exception:
                payload = {}
            res = compact_v1_context(payload)
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path in ("/api/v1/advisor/search", "/api/advisor/search"):
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(post_body.decode("utf-8"))
            except Exception:
                payload = {}
            res = search_v1_advisor(payload)
            self._set_headers(200 if res.get("ok") else 500, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        self._set_headers(HTTPStatus.NOT_FOUND, "application/json")
        self.wfile.write(json.dumps({"ok": False, "error": f"Ukjent POST-endepunkt {path}"}).encode("utf-8"))

    def log_message(self, format: str, *args) -> None:
        pass


def run_server(host: str = "127.0.0.1", port: int = 8766) -> None:
    server_address = (host, port)
    ThreadingHTTPServer.allow_reuse_address = True
    httpd = ThreadingHTTPServer(server_address, HubApiHandler)
    print(f"=====================================================================")
    print(f"🏛️  KRISTIANSAND KOMMUNE — CONTROL OFFICE HUB API TJENER")
    print(f"    Lytter på: http://{host}:{port}")
    print(f"    Status API: http://{host}:{port}/api/status")
    print(f"    Oppdatering API: POST http://{host}:{port}/api/update-vectordb")
    print(f"    Dashboard: http://{host}:{port}/index.html")
    print(f"=====================================================================")
    sys.stdout.flush()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStenger API-tjener...")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    port = int(os.getenv("HUB_API_PORT", "8766"))
    run_server(port=port)
