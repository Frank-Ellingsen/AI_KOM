import os
import sys
import pytest

# Legg til Clean2 prosjektmappen i sys.path
CLEAN2_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "AI_KOM_Antigravity_Clean2", "AI_KOM"))
if CLEAN2_ROOT not in sys.path:
    sys.path.insert(0, CLEAN2_ROOT)

def test_clean2_files_exist():
    """Verifiser at alle filer i AI_KOM_Antigravity_Clean2 er på plass og ikke-tomme."""
    expected = [
        "Dockerfile",
        "docker-compose.yml",
        ".dockerignore",
        ".env.example",
        "requirements.txt",
        "README.md",
        "index.html",
        "app/__init__.py",
        "app/schemas.py",
        "app/tools.py",
        "app/agent.py",
        "app/build_rag_index.py",
        "app/frontend.py",
        "docs/ANTIGRAVITY_INSTRUCTIONS.md",
        "docs/ARCHITECTURE.md",
        "docs/PILOT_MANDATE.md",
    ]
    for rel_path in expected:
        full_path = os.path.join(CLEAN2_ROOT, rel_path)
        assert os.path.exists(full_path), f"Clean2 fil mangler: {rel_path}"
        assert os.path.getsize(full_path) > 10, f"Clean2 fil er tom: {rel_path}"

def test_clean2_schemas_and_tools():
    """Tester Pydantic v2 schemas og verktøy i Clean2."""
    from app.schemas import UserContext, MonthlyUnitReportInput, BudgetReallocationInput, EOYForecastInput
    from app.tools import calculate_monthly_report, process_budget_reallocation, eoy_forecast

    user = UserContext(
        user_id="frank_e",
        role="enhetsleder",
        ansvar_code="2530",
        kommunalsjef_område="Omsorgssentre"
    )
    assert user.role == "enhetsleder"
    assert user.ansvar_code == "2530"

    # Månedsrapport
    rep = calculate_monthly_report(MonthlyUnitReportInput(
        ansvar_code="2530",
        period_month=8,
        user_context=user
    ))
    assert rep["ansvar"] == "2530"
    assert "status" in rep
    assert rep["status"] in ["🟢 GRØNN", "🟡 GUL", "🔴 RØD"]

    # Omdisponering under 500k innen samme sektor
    realloc_adm = process_budget_reallocation(BudgetReallocationInput(
        fra_ansvar="2530",
        til_ansvar="2540",
        belop=250000.0,
        begrunnelse="Vikarer ved høyt fravær",
        user_context=user
    ))
    assert realloc_adm["krever_politisk_vedtak"] is False
    assert "Kommunedirektøren" in realloc_adm["vedtaksorgan"]

    # Omdisponering over 500k
    realloc_pol = process_budget_reallocation(BudgetReallocationInput(
        fra_ansvar="2530",
        til_ansvar="2540",
        belop=750000.0,
        begrunnelse="Større tiltak",
        user_context=user
    ))
    assert realloc_pol["krever_politisk_vedtak"] is True
    assert "Bystyret" in realloc_pol["vedtaksorgan"]

    # EOY Prognose
    fc = eoy_forecast(EOYForecastInput(
        ansvar_code="2530",
        current_month=8,
        user_context=user
    ))
    assert "eac" in fc
    assert "monte_carlo" in fc
    assert fc["monte_carlo"]["p50"] > 0

def test_clean2_agent_execution():
    """Tester Agent loop og HITL intercept i Clean2."""
    from app.schemas import UserContext
    from app.agent import KrsKommuneAgent

    agent = KrsKommuneAgent()
    user = UserContext(user_id="frank_e", role="enhetsleder", ansvar_code="2530")

    # Månedsrapport
    res_rep = agent.run("Vis rapport for enheten min", user)
    assert res_rep["data"] is not None
    assert "Rapport for enhet" in res_rep["response"]
    assert res_rep["hitl_required"] is False

    # Omdisponering
    res_realloc = agent.run("Jeg vil omdisponere midler jf. § 14-5", user)
    assert res_realloc["data"] is not None
    assert "14-5" in res_realloc["response"]

    # Prognose
    res_eoy = agent.run("Hva er forventet EOY prognose og årsslutt?", user)
    assert res_eoy["data"] is not None
    assert "EOY-prognose" in res_eoy["response"]
