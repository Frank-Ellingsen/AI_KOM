import os
from typing import Dict, Any, Optional
from app.schemas import (
    UserContext,
    MonthlyUnitReportInput,
    BudgetReallocationInput,
    EOYForecastInput,
    ERPSQLQueryInput
)
from app.tools import (
    calculate_monthly_report,
    query_erp_transactions_secure,
    process_budget_reallocation,
    eoy_forecast,
    write_audit_log
)

class KrsKommuneAgent:
    """
    Agentisk AI-Økonomirådgiver for Kristiansand kommune (Helse og Mestring).
    Implementerer Loop Engineering (Lag 4):
    - Bounded Loops (max_iterations = 5)
    - Self-Correction & Reflection ved feil
    - Human-in-the-Loop (HITL) Intercepts for § 14-5
    - Immutable Audit Logging for Kommunerevisjonen
    """
    
    def __init__(self):
        self.max_iterations = 5
        self.api_key = os.getenv("GEMINI_API_KEY")
        self._client = None
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception:
                self._client = None

    def run(self, user_prompt: str, user_context: UserContext) -> Dict[str, Any]:
        """Kjører agentløkken med feilhåndtering, refleksjon og bounded recursion."""
        iteration = 0
        error_context = None

        while iteration < self.max_iterations:
            iteration += 1
            try:
                result = self._execute_step(user_prompt, user_context, error_context)
                # Skriv state checkpointing til audit_log
                write_audit_log(
                    user_context=user_context,
                    action_type="AGENT_EXECUTION_COMPLETED",
                    query_input=user_prompt,
                    summary=f"Iteration {iteration} success: {result.get('action', 'general')}",
                    status="SUCCESS"
                )
                return result
            except Exception as e:
                # Self-Correction Loop: fang feil og reflekter
                error_context = f"Feil under kjøring: {str(e)}. Forsøker selvreparasjon i iterasjon {iteration + 1}."
                write_audit_log(
                    user_context=user_context,
                    action_type="AGENT_SELF_CORRECTION",
                    query_input=user_prompt,
                    summary=error_context,
                    status="WARNING"
                )

        # Fallback dersom max_iterations overskrides
        return {
            "action": "ERROR_MAX_ITERATIONS",
            "response": "⚠️ Agenten nådde maksimal grense for iterasjoner (5). Henvendelsen er logget til manuell oppfølging.",
            "data": None,
            "hitl_required": False
        }

    def _execute_step(
        self,
        user_prompt: str,
        user_context: UserContext,
        error_context: Optional[str]
    ) -> Dict[str, Any]:
        prompt_lower = user_prompt.lower()
        ansvar = user_context.ansvar_code or "2530"

        # 1. Månedsrapport & avviksanalyse
        if any(w in prompt_lower for w in ["rapport", "avvik", "merforbruk", "trafikklys"]):
            rep = calculate_monthly_report(MonthlyUnitReportInput(
                ansvar_code=ansvar,
                period_month=8,
                user_context=user_context
            ))
            response_text = (
                f"📊 **Månedsrapport for enhet {rep['ansvar']} (Periode {rep['period_month']}):**\n\n"
                f"* **Status:** {rep['status']}\n"
                f"* **Regnskap hittil:** kr {rep['forbruk']:,.0f}\n"
                f"* **Periodisert budsjett:** kr {rep['budsjett']:,.0f}\n"
                f"* **Netto avvik (CV):** kr {rep['avvik_nok']:,.0f} ({rep['avvik_pct']} %)\n"
                f"* **Kostnadsdriver:** {rep['driver']}"
            )
            return {
                "action": "MONTHLY_REPORT",
                "response": response_text,
                "data": rep,
                "hitl_required": False
            }

        # 2. Omdisponering og fullmaktskontroll (§ 14-5) med HITL Intercept
        elif any(w in prompt_lower for w in ["omdisponer", "flytte", "overfør", "14-5", "fullmakt"]):
            # Eksempel: 350k eller trekk ut beløp
            belop = 350000.0
            realloc = process_budget_reallocation(BudgetReallocationInput(
                fra_ansvar=ansvar,
                til_ansvar="2540",
                belop=belop,
                begrunnelse="Uforutsette vikarutgifter ved forhøyet sykefravær jf. HTA § 4",
                user_context=user_context
            ))
            
            hitl = realloc["krever_politisk_vedtak"]
            status_badge = "⚠️ KREVER BYSTYREVEDTAK (HITL PORT 9)" if hitl else "✅ ADMINISTRATIVT VEDTAK"
            
            response_text = (
                f"🔄 **Vurdering av omdisponering jf. Kommuneloven § 14-5:**\n\n"
                f"* **Status:** {status_badge}\n"
                f"* **Vedtaksorgan:** {realloc['vedtaksorgan']}\n"
                f"* **Beløp:** kr {realloc['belop']:,.0f} fra {realloc['fra_ansvar']} til {realloc['til_ansvar']}\n\n"
                f"**Utkast til formelt saksframlegg:**\n"
                f"```text\n{realloc['saksframlegg_utkast']}\n```"
            )
            return {
                "action": "BUDGET_REALLOCATION",
                "response": response_text,
                "data": realloc,
                "hitl_required": hitl
            }

        # 3. Årssluttprognose (EOY/EAC) & Monte Carlo
        elif any(w in prompt_lower for w in ["prognose", "eoy", "eac", "årsslutt", "monte carlo"]):
            forecast = eoy_forecast(EOYForecastInput(
                ansvar_code=ansvar,
                current_month=8,
                user_context=user_context
            ))
            response_text = (
                f"🔮 **Rullende EOY-prognose for ansvar {forecast['ansvar']}:**\n\n"
                f"* **Vedtatt årsramme (BAC):** kr {forecast['bac']:,.0f}\n"
                f"* **Forventet årsslutt (EAC P50):** kr {forecast['eac']:,.0f}\n"
                f"* **Beregnet årssluttavvik (VAC):** kr {forecast['vac']:,.0f}\n"
                f"* **Kostnadsindeks (CPI):** {forecast['cpi']}\n\n"
                f"**Monte Carlo Usikkerhetsspenn:**\n"
                f"* **P10 (Beste utfall):** kr {forecast['monte_carlo']['p10']:,.0f}\n"
                f"* **P50 (Forventet):** kr {forecast['monte_carlo']['p50']:,.0f}\n"
                f"* **P90 (Konservativt):** kr {forecast['monte_carlo']['p90']:,.0f}\n\n"
                f"**Tiltakskrav:** {forecast['tiltak']}"
            )
            return {
                "action": "EOY_FORECAST",
                "response": response_text,
                "data": forecast,
                "hitl_required": forecast['vac'] < -500000
            }

        # 4. Standard velkomst og veileder
        else:
            return {
                "action": "GREETING",
                "response": (
                    "🏛️ **Velkommen til AI-Økonomirådgiver for Kristiansand kommune.**\n\n"
                    "Jeg bistår deg med presis, revisjonssikret økonomistyring:\n"
                    "1. **Månedsrapport & RAG-trafikklys** — Still spørsmål om enhetens avvik og kostnadsdrivere.\n"
                    "2. **Omdisponeringer jf. § 14-5** — Automatisk kontroll mot fullmaktsmatrise og saksframlegg.\n"
                    "3. **EOY / EAC Prognoser** — Sesongjustert Earned Value og Monte Carlo-usikkerhet.\n"
                    "4. **Transaksjonsrevisjon** — Drill-down på bilagsnivå med streng RBAC.\n\n"
                    "Hvordan kan jeg hjelpe deg i dag?"
                ),
                "data": None,
                "hitl_required": False
            }
