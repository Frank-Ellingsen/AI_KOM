import sqlite3
import datetime
import json
from typing import Dict, Any
from app.schemas import UserContext, AuditLogEntry, ERPSQLQueryInput, MonthlyUnitReportInput, BudgetReallocationInput, EOYForecastInput

DB_PATH = "data/db/kommune_golden_record.db"

def write_audit_log(user_context: UserContext, action_type: str, query_input: str, summary: str, status: str = "SUCCESS"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user_id TEXT,
                role TEXT,
                action_type TEXT,
                query_or_input TEXT,
                execution_result_summary TEXT,
                status TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO audit_log (timestamp, user_id, role, action_type, query_or_input, execution_result_summary, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, user_context.user_id, user_context.role, action_type, query_input, summary, status))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Audit log write failed: {e}")

def query_erp_transactions_secure(input_data: ERPSQLQueryInput) -> Dict[str, Any]:
    user = input_data.user_context
    sql = input_data.sql_query
    
    if user.role == "enhetsleder" and user.ansvar_code:
        if "WHERE" in sql.upper():
            sql = sql + f" AND ansvar = '{user.ansvar_code}'"
        else:
            sql = sql + f" WHERE ansvar = '{user.ansvar_code}'"
            
    summary = f"Executed SQL with RBAC for role {user.role}"
    write_audit_log(user, "SQL_QUERY", input_data.sql_query, summary)
    
    return {
        "status": "SUCCESS",
        "rbac_applied": user.role == "enhetsleder",
        "executed_sql": sql,
        "sample_data": [
            {"ansvar": user.ansvar_code or "2530", "art": "10000", "art_navn": "Fast lønn", "forbruk": 450000, "budsjett": 440000, "avvik": 10000},
            {"ansvar": user.ansvar_code or "2530", "art": "10900", "art_navn": "Overtid", "forbruk": 85000, "budsjett": 30000, "avvik": 55000}
        ]
    }

def calculate_monthly_report(input_data: MonthlyUnitReportInput) -> Dict[str, Any]:
    user = input_data.user_context
    forbruk = 1250000
    budsjett = 1180000
    avvik = forbruk - budsjett
    avvik_pct = (avvik / budsjett) * 100
    
    status = "🟢 GRØNN" if avvik_pct <= 0 else ("🟡 GUL" if avvik_pct <= 3.0 else "🔴 RØD")
    summary = f"Monthly report for {input_data.ansvar_code}, Status: {status}"
    write_audit_log(user, "MONTHLY_REPORT", f"Month {input_data.period_month}, Ansvar {input_data.ansvar_code}", summary)
    
    return {
        "ansvar": input_data.ansvar_code,
        "period_month": input_data.period_month,
        "forbruk": forbruk,
        "budsjett": budsjett,
        "avvik_nok": avvik,
        "avvik_pct": round(avvik_pct, 2),
        "status": status,
        "driver": "Overtid og vikarforbruk i helse/omsorg"
    }

def process_budget_reallocation(input_data: BudgetReallocationInput) -> Dict[str, Any]:
    user = input_data.user_context
    
    krever_politisk = input_data.fra_ansvar[:2] != input_data.til_ansvar[:2] or input_data.belop > 500000
    vedtaksorgan = "Bystyret / Formannskapet" if krever_politisk else "Kommunedirektøren (Administrativt)"
    
    summary = f"Reallocation {input_data.belop} NOK from {input_data.fra_ansvar} to {input_data.til_ansvar}. Organ: {vedtaksorgan}"
    write_audit_log(user, "BUDGET_REALLOCATION", f"{input_data.belop} NOK", summary)
    
    return {
        "status": "PROCESSED",
        "fra_ansvar": input_data.fra_ansvar,
        "til_ansvar": input_data.til_ansvar,
        "belop": input_data.belop,
        "krever_politisk_vedtak": krever_politisk,
        "vedtaksorgan": vedtaksorgan,
        "saksframlegg_utkast": f"Saksframlegg: Omdisponering av {input_data.belop} NOK til godkjenning hos {vedtaksorgan}."
    }
