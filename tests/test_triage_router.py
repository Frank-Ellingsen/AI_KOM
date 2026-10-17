"""
Tests for Antigravity Triage Router
Tester fast-path klassifisering, ruteringslogikk og kryptografisk SHA-256 forsegling.
"""

import pytest
import asyncio
from app.schemas.triage import TriageRequest, TriageCategory, ExecutionPriority
from app.core.triage_router import TriageRouter


def test_triage_ompostering_hybrid():
    """Validerer hybrid routing for forespørsler som krever både datahenting, regler og skill."""
    router = TriageRouter()
    req = TriageRequest(
        prompt="Kjør ompostering for feilførte IT-lisenser på Vågsbygd skole og sjekk MVA-balansen mot Visma.",
        session_id="test-session-123",
        user_persona="CONTROLLER",
        active_unit_id="120100"
    )
    decision = asyncio.run(router.classify_and_route(req))
    assert decision.primary_category in [TriageCategory.SKILL_WORKFLOW, TriageCategory.HYBRID_COMPOSITE]
    assert decision.sha256_audit_hash is not None
    assert len(decision.sha256_audit_hash) == 64
    assert decision.confidence_score >= 0.90


def test_triage_rag_legal_lookup():
    """Validerer juridisk RAG-oppslag for spørsmål om Kommuneloven § 14-5."""
    router = TriageRouter()
    req = TriageRequest(
        prompt="Hva sier Kommuneloven § 14-5 om overskridelse av årsbudsjett?",
        session_id="test-session-456",
        user_persona="ENHETSLEDER"
    )
    decision = asyncio.run(router.classify_and_route(req))
    assert decision.primary_category == TriageCategory.RAG_LOOKUP
    assert "kommuneloven" in decision.rag_search_filters["tags"]
    assert len(decision.sha256_audit_hash) == 64


def test_triage_direct_mcp():
    """Validerer sanntidsoppslag i ERP-fagsystemer via MCP."""
    router = TriageRouter()
    req = TriageRequest(
        prompt="Vis saldo og utgifter fra Visma for Enhet 202 per september.",
        session_id="test-session-789",
        user_persona="CONTROLLER"
    )
    decision = router.classify_and_route_sync(req)
    assert decision.primary_category == TriageCategory.DIRECT_MCP
    assert "visma_erp" in decision.required_mcp_connectors
    assert decision.priority == ExecutionPriority.HIGH_REALTIME


def test_triage_skill_forecasting_workflow():
    """Validerer aktivering av Skill Workflow for prediktiv prognoseberegning."""
    router = TriageRouter()
    req = TriageRequest(
        prompt="Generer P10, P50 og P90 Monte Carlo prognose for helse- og mestringssektoren.",
        session_id="test-session-999",
        user_persona="CONTROLLER"
    )
    decision = router.classify_and_route_sync(req)
    assert decision.primary_category == TriageCategory.SKILL_WORKFLOW
    assert decision.skill_workflow_target == "predictive_forecasting_engine"
    assert len(decision.sha256_audit_hash) == 64
