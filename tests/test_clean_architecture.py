import os
import pytest
from app.schemas import (
    UserContext,
    AuditLogEntry,
    ERPSQLQueryInput,
    MonthlyUnitReportInput,
    BudgetReallocationInput,
    EOYForecastInput,
)
from app.tools import (
    get_db_path,
    write_audit_log,
    calculate_monthly_report,
    process_budget_reallocation,
    query_erp_transactions_secure,
)
from app.agent import KrsKommuneAgent


def test_clean_architecture_files_exist():
    """Verifiser at alle filer fra AI_KOM_Antigravity_Clean er til stede."""
    expected_files = [
        "Dockerfile",
        "docker-compose.yml",
        ".dockerignore",
        "requirements.txt",
        "app/__init__.py",
        "app/tools.py",
        "app/agent.py",
        "app/build_rag_index.py",
        "app/frontend.py",
        "app/schemas/advisor.py",
        "docs/ARCHITECTURE.md",
        "docs/PILOT_MANDATE.md",
        "docs/ANTIGRAVITY_INSTRUCTIONS.md",
    ]
    for rel_path in expected_files:
        assert os.path.exists(rel_path), f"Fil mangler: {rel_path}"


def test_clean_pydantic_schemas():
    """Tester Pydantic v2 schemas for UserContext og verktøy."""
    user = UserContext(
        user_id="frank_e",
        role="enhetsleder",
        ansvar_code="2530",
        kommunalsjef_område="Omsorgssentre",
    )
    assert user.role == "enhetsleder"
    assert user.ansvar_code == "2530"

    realloc = BudgetReallocationInput(
        fra_ansvar="2530",
        til_ansvar="2540",
        belop=250000.0,
        begrunnelse="Vikarer ved sykefravær",
        user_context=user,
    )
    assert realloc.belop == 250000.0


def test_clean_tools_and_rbac():
    """Tester verktøy for månedsrapport, RBAC og fullmaktskontroll."""
    user = UserContext(user_id="frank_e", role="enhetsleder", ansvar_code="2530")

    # Månedsrapport
    rep = calculate_monthly_report(
        MonthlyUnitReportInput(ansvar_code="2530", period_month=8, user_context=user)
    )
    assert rep["ansvar"] == "2530"
    assert rep["period_month"] == 8
    assert "status" in rep
    assert rep["status"] in ["🟢 GRØNN", "🟡 GUL", "🔴 RØD"]

    # Omdisponering under 500k innen samme sektor
    realloc_adm = process_budget_reallocation(
        BudgetReallocationInput(
            fra_ansvar="2530",
            til_ansvar="2540",
            belop=200000.0,
            begrunnelse="Driftsjustering",
            user_context=user,
        )
    )
    assert realloc_adm["krever_politisk_vedtak"] is False
    assert "Kommunedirektøren" in realloc_adm["vedtaksorgan"]

    # Omdisponering over 500k (krever politisk)
    realloc_pol = process_budget_reallocation(
        BudgetReallocationInput(
            fra_ansvar="2530",
            til_ansvar="2540",
            belop=650000.0,
            begrunnelse="Større tiltak",
            user_context=user,
        )
    )
    assert realloc_pol["krever_politisk_vedtak"] is True
    assert "Bystyret" in realloc_pol["vedtaksorgan"]


def test_clean_agent_execution():
    """Tester KrsKommuneAgent orkestrering."""
    agent = KrsKommuneAgent()
    user = UserContext(user_id="frank_e", role="enhetsleder", ansvar_code="2530")

    # Rapportforespørsel
    res_rep = agent.run("Kan du gi meg rapport for enheten min?", user)
    assert res_rep["data"] is not None
    assert "Rapport for enhet" in res_rep["response"]

    # Omdisponeringsforespørsel
    res_realloc = agent.run("Jeg vil omdisponere midler", user)
    assert res_realloc["data"] is not None
    assert "14-5" in res_realloc["response"]

    # Prognoseforespørsel
    res_prog = agent.run("Hva er årsprognose og eoy?", user)
    assert res_prog["data"] is not None
    assert "EAC" in res_prog["response"]
