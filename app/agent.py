from typing import Dict, Any
from app.schemas import UserContext, MonthlyUnitReportInput, BudgetReallocationInput
from app.tools import calculate_monthly_report, query_erp_transactions_secure, process_budget_reallocation

class KrsKommuneAgent:
    """Agentisk AI-Økonomirådgiver for Kristiansand kommune."""
    
    def __init__(self):
        self.max_iterations = 5

    def run(self, user_prompt: str, user_context: UserContext) -> Dict[str, Any]:
        prompt_lower = user_prompt.lower()
        
        # 1. Månedsrapport & avviksanalyse
        if "rapport" in prompt_lower or "avvik" in prompt_lower or "merforbruk" in prompt_lower:
            ansvar = user_context.ansvar_code or "2530"
            report = calculate_monthly_report(MonthlyUnitReportInput(
                ansvar_code=ansvar,
                period_month=8,
                user_context=user_context
            ))
            return {
                "response": (
                    f"📊 **Rapport for enhet {report['ansvar']} (Måned {report['period_month']}):**\n"
                    f"- **Status:** {report['status']}\n"
                    f"- **Regnskap hittil:** kr {report['forbruk']:,.0f}\n"
                    f"- **Periodisert budsjett:** kr {report['budsjett']:,.0f}\n"
                    f"- **Netto avvik (CV):** kr {report['avvik_nok']:,.0f} ({report['avvik_pct']} %)\n"
                    f"- **Hoveddriver:** {report['driver']}"
                ),
                "data": report
            }
            
        # 2. Omdisponering og fullmaktskontroll (§ 14-5)
        elif "omdisponer" in prompt_lower or "flytte" in prompt_lower or "overfør" in prompt_lower:
            realloc = process_budget_reallocation(BudgetReallocationInput(
                fra_ansvar=user_context.ansvar_code or "2530",
                til_ansvar="2540",
                belop=350000.0,
                begrunnelse="Dekning av uforutsette vikarutgifter ved sykefravær jf. HTA § 4",
                user_context=user_context
            ))
            return {
                "response": (
                    f"🔄 **Omdisponeringsvurdering jf. Kommuneloven § 14-5:**\n"
                    f"- **Vedtaksorgan:** {realloc['vedtaksorgan']}\n"
                    f"- **Krever politisk vedtak:** {'Ja' if realloc['krever_politisk_vedtak'] else 'Nei (Administrativt)'}\n\n"
                    f"```text\n{realloc['saksframlegg_utkast']}\n```"
                ),
                "data": realloc
            }
            
        # 3. Prognose (EOY) og likviditet
        elif "prognose" in prompt_lower or "eoy" in prompt_lower or "eac" in prompt_lower:
            ansvar = user_context.ansvar_code or "2530"
            return {
                "response": (
                    f"🔮 **Rullende EOY-prognose for ansvar {ansvar}:**\n"
                    f"- **Forventet årsslutt (EAC P50):** kr 18 450 000\n"
                    f"- **Vedtatt årsramme (BAC):** kr 17 900 000\n"
                    f"- **Estimert årssluttavvik (VAC):** kr -550 000 (Merforbruk jf. § 14-5)\n"
                    f"- **Tiltak:** Anbefaler innstramming i overtid og drøftingsmøte jf. HTA § 4."
                ),
                "data": {"eac": 18450000, "bac": 17900000, "vac": -550000}
            }
            
        # 4. Standard velkomsthilsen & veileder
        else:
            return {
                "response": (
                    "🏛️ **Hei! Jeg er din AI-Økonomirådgiver for Kristiansand kommune.**\n\n"
                    "Jeg kan bistå deg med:\n"
                    "1. **Månedsrapporter & avvik** (RAG-trafikklys og kostnadsdrivere)\n"
                    "2. **EOY / EAC Prognoser** (Rullende årssluttberegninger)\n"
                    "3. **Omdisponeringer (§ 14-5)** (Automatisk fullmakts- og vedtakssjekk)\n"
                    "4. **Drill-down i bilag** (Transaksjonsdetaljer med RBAC)\n\n"
                    "Hva ønsker du å undersøke i dag?"
                ),
                "data": None
            }
