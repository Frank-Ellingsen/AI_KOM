"""
Kristiansand Kommune AI Hub — Triage Router Schemas
Pydantic v2 datamodeller for forespørselsklassifisering og ruting.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TriageCategory(str, Enum):
    DIRECT_MCP = "DIRECT_MCP"
    RAG_LOOKUP = "RAG_LOOKUP"
    SKILL_WORKFLOW = "SKILL_WORKFLOW"
    MEMORY_CONTEXT = "MEMORY_CONTEXT"
    HYBRID_COMPOSITE = "HYBRID_COMPOSITE"


class ExecutionPriority(str, Enum):
    HIGH_REALTIME = "HIGH_REALTIME"
    STANDARD = "STANDARD"
    BACKGROUND_BATCH = "BACKGROUND_BATCH"


class TriageRequest(BaseModel):
    prompt: str = Field(..., description="Innkommende tekst eller spørsmål fra brukeren")
    session_id: str = Field(..., description="Unik økt-ID fra Redis session store")
    user_persona: str = Field(default="ENHETSLEDER", description="Aktiv persona: ENHETSLEDER, CONTROLLER, TOPPLEDELSE")
    active_unit_id: Optional[str] = Field(None, description="Aktivert enhets-ID, f.eks. 120100 Vågsbygd skole")
    active_period: str = Field(default="M10_2026", description="Gjeldende regnskapsperiode")


class ToolTarget(BaseModel):
    tool_name: str
    action: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class TriageDecision(BaseModel):
    primary_category: TriageCategory
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    priority: ExecutionPriority = ExecutionPriority.STANDARD
    required_mcp_connectors: List[str] = Field(default_factory=list)
    rag_search_filters: Dict[str, Any] = Field(default_factory=dict)
    skill_workflow_target: Optional[str] = None
    target_tools: List[ToolTarget] = Field(default_factory=list)
    reasoning_trace: str = Field(..., description="Forklaring på hvorfor denne ruten ble valgt")
    sha256_audit_hash: str = Field(..., description="Kryptografisk stempel for audit log")
