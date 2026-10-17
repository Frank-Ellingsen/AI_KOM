# -*- coding: utf-8 -*-
"""
Pydantic Schemas for AI Engineering & Infrastructure Agent (Agent 15)
Adheres to ai-engineering-agent.md: 4-layer architecture, context compaction,
semantic caching, and latency/token budgeting.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class LayerArchitectureStatus(BaseModel):
    """Status for de 4 arkitekturlagene."""
    model_layer: Dict[str, Any] = Field(..., description="Modelltilgjengelighet (Gemini, Ollama)")
    harness_layer: Dict[str, Any] = Field(..., description="Agent-løkke og sandkasse")
    framework_layer: Dict[str, Any] = Field(..., description="Multi-agent orkestrering")
    platform_layer: Dict[str, Any] = Field(..., description="Sikkerhet, RBAC, Stage-Gate Port 9")


class ContextCompactionRequest(BaseModel):
    """Forespørsel om kontekstkomprimering."""
    raw_context: str
    max_tokens: int = Field(2000, ge=100, le=32000)
    preserve_statutory_refs: bool = Field(True, description="Bevarer lovreferanser (§)")


class ContextCompactionResponse(BaseModel):
    """Resultat av kontekstkomprimering."""
    original_chars: int
    compacted_chars: int
    compression_ratio: float
    compacted_text: str
    extracted_statutes: List[str]


class SemanticCacheStats(BaseModel):
    """Statistikk for semantisk cache."""
    total_entries: int
    cache_hits: int
    cache_misses: int
    hit_rate_pct: float
    saved_tokens: int
    estimated_cost_saved_nok: float


class LatencyBenchmarkReport(BaseModel):
    """Måling av inferenslatens og tokengjennomstrømming."""
    model_name: str
    time_to_first_token_ms: float
    total_latency_ms: float
    tokens_generated: int
    tokens_per_second: float
    token_cost_nok: float
