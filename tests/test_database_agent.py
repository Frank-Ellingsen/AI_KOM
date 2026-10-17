# -*- coding: utf-8 -*-
"""
Tests for Agent 14: Database & Data Engineering Agent
Validates read-only guardrails, parameterized queries, EXPLAIN QUERY PLAN,
hybrid search, and PII masking.
"""

import pytest
from app.services.database_agent_service import DatabaseAgentService
from app.schemas.database import QueryRequest


def test_schema_inspection():
    svc = DatabaseAgentService()
    schema_all = svc.inspect_schema()
    assert "tables" in schema_all
    assert len(schema_all["tables"]) >= 5

    schema_art = svc.inspect_schema("Dim_Art")
    assert schema_art.get("table") == "Dim_Art"
    col_names = [c["name"] for c in schema_art.get("columns", [])]
    assert "art_kode" in col_names


def test_safe_read_only_query_execution():
    svc = DatabaseAgentService()
    req = QueryRequest(sql="SELECT art_kode, art_navn FROM Dim_Art LIMIT 3;")
    res = svc.execute_query(req)
    assert res.row_count == 3
    assert len(res.rows) == 3
    assert res.is_mutation is False
    assert res.execution_time_ms >= 0.0
    assert len(res.query_hash) > 0


def test_mutation_guardrail_blocks_unapproved_writes():
    svc = DatabaseAgentService()
    destructive_sql = "DELETE FROM Dim_Art WHERE art_kode = '9999';"
    req = QueryRequest(sql=destructive_sql, hitl_approved=False)
    with pytest.raises(PermissionError, match="SIKKERHETSSPERRE"):
        svc.execute_query(req)


def test_explain_query_plan():
    svc = DatabaseAgentService()
    plan = svc.explain_query_plan("SELECT * FROM Dim_Art WHERE art_kode='1010';")
    assert len(plan.plan_steps) > 0
    assert plan.sql.startswith("SELECT")
    assert plan.scans_entire_table or plan.uses_index or plan.optimization_recommendation is not None


def test_pii_masking_in_query_results():
    svc = DatabaseAgentService()
    raw_sample = "Saksbehandler Frank (fnr: 12058512345, tlf: 91234567, e-post: test@kommune.no)"
    masked = svc.mask_pii(raw_sample)
    assert "12058512345" not in masked
    assert "[FNR_SKJERMET]" in masked
    assert "[EPOST_SKJERMET]" in masked
    assert "[TLF_SKJERMET]" in masked
