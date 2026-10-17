# -*- coding: utf-8 -*-
"""
Pydantic Schemas for Evaluation & Quality Assurance Agent (Agent 13)
Adheres to evaluation-agent.md, RAG triad metrics, and CI/CD 90% deployment gate.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class GoldenTestCase(BaseModel):
    """Representerer et testtilfelle i Golden Dataset."""
    id: str = Field(..., description="Unik ID, f.eks. GOLDEN-001")
    prompt: str = Field(..., description="Bruker- eller lederforespørsel")
    category: str = Field(..., description="Kategori: legal_rag, kostra, evm, cash, mva")
    expected_tool: Optional[str] = Field(None, description="Forventet verktøykall")
    expected_keywords: List[str] = Field(default_factory=list, description="Kjernenøkkelord som må gjenfinnes")
    ground_truth_context: str = Field(..., description="Faktisk autoritativ kildetekst")
    min_faithfulness: float = Field(0.90, description="Minstekrav for troverdighet/groundedness")


class RagEvalResult(BaseModel):
    """Resultat av RAG-evaluering."""
    query: str
    recall_at_k: float = Field(..., ge=0.0, le=1.0)
    precision_at_k: float = Field(..., ge=0.0, le=1.0)
    mrr: float = Field(..., ge=0.0, le=1.0, description="Mean Reciprocal Rank")
    faithfulness_score: float = Field(..., ge=0.0, le=1.0, description="Groundedness uten hallusinasjoner")
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    passed: bool


class TrajectoryEvalResult(BaseModel):
    """Evaluering av agent-trajektorie og verktøykall-sekvens."""
    goal: str
    step_count: int
    loop_detected: bool = False
    tool_precision: float = Field(..., ge=0.0, le=1.0)
    schema_valid: bool = True
    passed: bool


class LLMJudgeScore(BaseModel):
    """Rubrikkbasert LLM-as-a-Judge evaluering."""
    metric: str
    score: int = Field(..., ge=1, le=5)
    rationale: str
    position_swap_consistent: bool = True
    verbosity_penalty_applied: bool = False


class EvaluationRunReport(BaseModel):
    """Samlet evalueringsrapport for CI/CD gates."""
    run_id: str
    timestamp: str
    total_tests: int
    passed_tests: int
    overall_faithfulness: float
    overall_precision: float
    ci_cd_gate_passed: bool
    sha256_seal: str
    results: List[Dict[str, Any]] = Field(default_factory=list)
