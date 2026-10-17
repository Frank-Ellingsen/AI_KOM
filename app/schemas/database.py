# -*- coding: utf-8 -*-
"""
Pydantic Schemas for Database & Data Engineering Agent (Agent 14)
Adheres to database-agent.md: Read-Only default, Parameterized SQL, Hybrid Search, and PII masking.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Forespørsel om SQL-kjøring."""
    sql: str = Field(..., description="SQL-spørring som skal kjøres")
    params: List[Any] = Field(default_factory=list, description="Parametriserte variabler")
    hitl_approved: bool = Field(False, description="Må være True for destruktiv DDL/DML")
    limit: int = Field(100, ge=1, le=1000, description="Maks antall rader")


class QueryResult(BaseModel):
    """Resultat av SQL-kjøring med telemetri."""
    columns: List[str]
    rows: List[Dict[str, Any]]
    row_count: int
    execution_time_ms: float
    is_mutation: bool
    hitl_confirmed: bool
    query_hash: str
    pii_masked: bool = True


class QueryPlanExplanation(BaseModel):
    """Forklaring og analyse av spørreplan (EXPLAIN QUERY PLAN)."""
    sql: str
    plan_steps: List[str]
    uses_index: bool
    scans_entire_table: bool
    optimization_recommendation: Optional[str] = None


class HybridSearchResult(BaseModel):
    """Resultat av hybridsøk (Sparse FTS5 + Dense Vektor)."""
    id: str
    table_name: str
    matched_text: str
    sparse_score: float
    dense_score: float
    hybrid_score: float
    metadata: Dict[str, Any] = Field(default_factory=dict)
