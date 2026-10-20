from typing import Dict, Any
from app.schemas import UserContext, MonthlyUnitReportInput
from app.tools import calculate_monthly_report, query_erp_transactions_secure

class KrsKommuneAgent:
    def __init__(self):
        self.max_iterations = 5

    def run(self, user_prompt: str, user_context: UserContext) -> Dict[str, Any]:
        if "rapport" in user_prompt.lower() or "avvik" in user_prompt.lower():
            report = calculate_monthly_report(MonthlyUnitReportInput(
                ansvar_code=user_context.ansvar_code or "2530",
                period_month=8,
                user_context=user_context
            ))
            return {
                "response": f"Rapport for enhet {report['ansvar']}: Status er {report['status']}. Avvik er {report['avvik_nok']} NOK ({report['avvik_pct']}%). Driver: {report['driver']}.",
                "data": report
            }
        else:
            return {
                "response": "Jeg er din AI-Økonomirådgiver for Kristiansand kommune. Jeg kan hjelpe deg med månedsrapporter, EOY-prognoser, drill-down og omdisponeringer jf. kommuneloven § 14-5.",
                "data": None
            }
